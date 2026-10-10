"""
core/state.py — Persistencia del progreso del estudiante.

Backend conmutable:
  - MongoDB Atlas si hay URI en .streamlit/secrets.toml (o st.secrets)
  - Archivo JSON local como fallback (data/student_state.json)
"""

import json
from datetime import datetime
from pathlib import Path

# --- Rutas y constantes ------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
DATA_DIR = RAIZ / "data"
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "student_state.json"

MONGO_DOC_ID = "main"

NO_EVALUADO    = "no_evaluado"
NO_DOMINADO    = "no_dominado"
EN_DESARROLLO  = "en_desarrollo"
FUNCIONAL      = "funcional"
DOMINADO       = "dominado"

RACHA_FUNCIONAL = 3
RACHA_DOMINADO  = 5

_ESTADO_INICIAL = {
    "version": "1.0",
    "ultimo_update": None,
    "habilidades": {},
    "historial": [],
}


# --- Deteccion de backend ----------------------------------------------
def _leer_mongo_config():
    """Devuelve dict con uri/db_name/collection_name, o None si no hay."""
    # Intento 1: archivo local .streamlit/secrets.toml
    secrets_path = RAIZ / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            import tomllib
            with open(secrets_path, "rb") as f:
                data = tomllib.load(f)
            m = data.get("mongo", {})
            if m.get("uri"):
                return {
                    "uri": m["uri"],
                    "db_name": m.get("db_name", "math_rebuild"),
                    "collection_name": m.get("collection_name", "student_state"),
                }
        except Exception:
            pass

    # Intento 2: st.secrets (Streamlit Cloud)
    try:
        import streamlit as st
        m = st.secrets.get("mongo", {})
        if m.get("uri"):
            return {
                "uri": m["uri"],
                "db_name": m.get("db_name", "math_rebuild"),
                "collection_name": m.get("collection_name", "student_state"),
            }
    except Exception:
        pass

    return None


# --- Backend Mongo -----------------------------------------------------
_mongo_client = None
_mongo_db = None
_mongo_coll_name = None


def _mongo_init(cfg):
    global _mongo_client, _mongo_db, _mongo_coll_name
    if _mongo_client is None:
        from pymongo import MongoClient
        _mongo_client = MongoClient(cfg["uri"], serverSelectionTimeoutMS=10000)
        _mongo_db = _mongo_client[cfg["db_name"]]
        _mongo_coll_name = cfg["collection_name"]
    return _mongo_db[_mongo_coll_name]


def _mongo_cargar(cfg):
    coll = _mongo_init(cfg)
    doc = coll.find_one({"_id": MONGO_DOC_ID}, {"_id": 0})
    if doc is None:
        return json.loads(json.dumps(_ESTADO_INICIAL))
    return doc


def _mongo_guardar(cfg, estado):
    coll = _mongo_init(cfg)
    estado = {k: v for k, v in estado.items() if k != "_id"}
    coll.update_one(
        {"_id": MONGO_DOC_ID},
        {"$set": estado},
        upsert=True,
    )


def _mongo_reiniciar(cfg):
    coll = _mongo_init(cfg)
    coll.delete_one({"_id": MONGO_DOC_ID})


# --- Backend JSON ------------------------------------------------------
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


# --- API publica -------------------------------------------------------
def backend_activo():
    return "mongo" if _leer_mongo_config() else "json"


def cargar():
    cfg = _leer_mongo_config()
    if cfg:
        try:
            return _mongo_cargar(cfg)
        except Exception as e:
            print(f"[state] Mongo fallo, usando JSON: {e}")
    return _json_cargar()


def guardar(estado):
    cfg = _leer_mongo_config()
    if cfg:
        try:
            _mongo_guardar(cfg, estado)
            return
        except Exception as e:
            print(f"[state] Mongo fallo al guardar, usando JSON: {e}")
    _json_guardar(estado)


def registrar_evento(habilidad, correcto):
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

    if hab["racha"] >= RACHA_DOMINADO:
        hab["estado"] = DOMINADO
    elif hab["racha"] >= RACHA_FUNCIONAL:
        hab["estado"] = FUNCIONAL
    elif hab["intentos"] > 0:
        hab["estado"] = EN_DESARROLLO if hab["aciertos"] > 0 else NO_DOMINADO
    else:
        hab["estado"] = NO_EVALUADO

    estado["historial"].append({
        "ts": datetime.now().isoformat(timespec="seconds"),
        "habilidad": habilidad,
        "correcto": correcto,
    })
    estado["historial"] = estado["historial"][-1000:]

    guardar(estado)
    return hab


def reiniciar():
    cfg = _leer_mongo_config()
    if cfg:
        try:
            _mongo_reiniciar(cfg)
            return
        except Exception as e:
            print(f"[state] Mongo fallo al reiniciar, usando JSON: {e}")
    _json_guardar(json.loads(json.dumps(_ESTADO_INICIAL)))


def resumen():
    estado = cargar()
    return [
        {"habilidad": k, **v}
        for k, v in sorted(estado["habilidades"].items())
    ]