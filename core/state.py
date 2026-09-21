"""
core/state.py — Persistencia del progreso del estudiante.

Backend conmutable:
  - MongoDB Atlas si hay URI en .streamlit/secrets.toml (o st.secrets)
  - Archivo JSON local como fallback (data/student_state.json)

La API publica (cargar, guardar, registrar_evento, reiniciar, resumen)
es identica sin importar el backend.
"""

import json
from datetime import datetime
from pathlib import Path

# --- Rutas y constantes ------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
DATA_DIR = RAIZ / "data"
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "student_state.json"

# ID del documento unico en Mongo (toda la app usa un solo doc)
MONGO_DOC_ID = "main"

# Estados de dominio (Master Prompt v9.0)
NO_EVALUADO    = "no_evaluado"
NO_DOMINADO    = "no_dominado"
EN_DESARROLLO  = "en_desarrollo"
FUNCIONAL      = "funcional"
DOMINADO       = "dominado"

# Umbrales
RACHA_FUNCIONAL = 3
RACHA_DOMINADO  = 5

# Plantilla base
_ESTADO_INICIAL = {
    "version": "1.0",
    "ultimo_update": None,
    "habilidades": {},
    "historial": [],
}


# --- Deteccion de backend ----------------------------------------------
def _leer_uri_mongo():
    """
    Devuelve la URI de Mongo si esta configurada, si no None.
    Orden:
      1. Archivo .streamlit/secrets.toml (local / scripts)
      2. st.secrets (Streamlit Cloud)
    """
    # Intento 1: archivo local
    secrets_path = RAIZ / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            import tomllib
            with open(secrets_path, "rb") as f:
                data = tomllib.load(f)
            uri = data.get("mongo", {}).get("uri")
            if uri:
                return uri
        except Exception:
            pass

    # Intento 2: st.secrets (nube)
    try:
        import streamlit as st
        uri = st.secrets.get("mongo", {}).get("uri")
        if uri:
            return uri
    except Exception:
        pass

    return None


# --- Backend Mongo -----------------------------------------------------
_mongo_client = None
_mongo_db = None


def _mongo_init(uri):
    """Inicializa el cliente Mongo una sola vez."""
    global _mongo_client, _mongo_db
    if _mongo_client is None:
        from pymongo import MongoClient
        _mongo_client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        _mongo_db = _mongo_client["math_rebuild"]
    return _mongo_db


def _mongo_cargar(uri):
    db = _mongo_init(uri)
    doc = db["student_state"].find_one({"_id": MONGO_DOC_ID}, {"_id": 0})
    if doc is None:
        return json.loads(json.dumps(_ESTADO_INICIAL))
    return doc


def _mongo_guardar(uri, estado):
    db = _mongo_init(uri)
    estado = {k: v for k, v in estado.items() if k != "_id"}
    db["student_state"].update_one(
        {"_id": MONGO_DOC_ID},
        {"$set": estado},
        upsert=True,
    )


def _mongo_reiniciar(uri):
    db = _mongo_init(uri)
    db["student_state"].delete_one({"_id": MONGO_DOC_ID})


# --- Backend JSON (fallback) -------------------------------------------
def _json_cargar():
    if not STATE_FILE.exists():
        return json.loads(json.dumps(_ESTADO_INICIAL))
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return json.loads(json.dumps(_ESTADO_INICIAL))


def _json_guardar(estado):
    estado["ultimo_update"] = datetime.now().isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


# --- API publica (identica sin importar el backend) --------------------
def backend_activo():
    """Devuelve 'mongo' o 'json'. Util para mostrar en la UI."""
    return "mongo" if _leer_uri_mongo() else "json"


def cargar():
    uri = _leer_uri_mongo()
    if uri:
        try:
            return _mongo_cargar(uri)
        except Exception as e:
            print(f"[state] Mongo fallo, usando JSON: {e}")
    return _json_cargar()


def guardar(estado):
    uri = _leer_uri_mongo()
    if uri:
        try:
            _mongo_guardar(uri, estado)
            return
        except Exception as e:
            print(f"[state] Mongo fallo al guardar, usando JSON: {e}")
    _json_guardar(estado)


def registrar_evento(habilidad, correcto):
    """Registra un intento y devuelve la entrada actualizada de esa habilidad."""
    estado = cargar()
    hab = estado["habilidades"].setdefault(habilidad, {
        "estado": NO_EVALUADO,
        "racha": 0,
        "aciertos": 0,
        "intentos": 0,
    })

    hab["intentos"] += 1
    if correcto:
        hab["aciertos"] += 1
        hab["racha"]    += 1
    else:
        hab["racha"] = 0

    # Recalcular estado
    if hab["racha"] >= RACHA_DOMINADO:
        hab["estado"] = DOMINADO
    elif hab["racha"] >= RACHA_FUNCIONAL:
        hab["estado"] = FUNCIONAL
    elif hab["intentos"] > 0:
        hab["estado"] = EN_DESARROLLO if hab["aciertos"] > 0 else NO_DOMINADO
    else:
        hab["estado"] = NO_EVALUADO

    # Historial
    estado["historial"].append({
        "ts": datetime.now().isoformat(timespec="seconds"),
        "habilidad": habilidad,
        "correcto": correcto,
    })
    estado["historial"] = estado["historial"][-1000:]

    guardar(estado)
    return hab


def reiniciar():
    """Borra todo el progreso (util para depurar o empezar de cero)."""
    uri = _leer_uri_mongo()
    if uri:
        try:
            _mongo_reiniciar(uri)
            return
        except Exception as e:
            print(f"[state] Mongo fallo al reiniciar, usando JSON: {e}")
    _json_guardar(json.loads(json.dumps(_ESTADO_INICIAL)))


def resumen():
    """Devuelve lista de habilidades con su estado, ordenada por nombre."""
    estado = cargar()
    return [
        {"habilidad": k, **v}
        for k, v in sorted(estado["habilidades"].items())
    ]