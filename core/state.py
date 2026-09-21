"""
core/state.py — Persistencia del progreso del estudiante.

Guarda y carga el "Master Learning State" en data/student_state.json.
Sobrevive a reruns de Streamlit y a cerrar la app.

Estructura del JSON:
{
  "version": "1.0",
  "ultimo_update": "2026-09-20T10:30:00",
  "habilidades": {
    "signos": {
      "estado": "funcional",
      "racha": 3,
      "aciertos": 12,
      "intentos": 15
    }
  },
  "historial": [
    {"ts": "...", "habilidad": "signos", "correcto": true}
  ]
}
"""

import json
from datetime import datetime
from pathlib import Path

# --- Rutas ---------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
DATA_DIR = RAIZ / "data"
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "student_state.json"

# --- Estados de dominio (Master Prompt v9.0) -----------------------------
NO_EVALUADO    = "no_evaluado"
NO_DOMINADO    = "no_dominado"
EN_DESARROLLO  = "en_desarrollo"
FUNCIONAL      = "funcional"
DOMINADO       = "dominado"

# Umbrales (puedes ajustarlos)
RACHA_FUNCIONAL = 3
RACHA_DOMINADO  = 5

# --- Plantilla por defecto ----------------------------------------------
_ESTADO_INICIAL = {
    "version": "1.0",
    "ultimo_update": None,
    "habilidades": {},
    "historial": [],
}


# --- API pública ---------------------------------------------------------
def cargar() -> dict:
    """Devuelve el estado. Si no existe el archivo, devuelve la plantilla."""
    if not STATE_FILE.exists():
        return json.loads(json.dumps(_ESTADO_INICIAL))  # copia profunda
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Si el archivo se corrompió, lo reiniciamos sin perder la app
        return json.loads(json.dumps(_ESTADO_INICIAL))


def guardar(estado: dict) -> None:
    """Escribe el estado a disco. Actualiza 'ultimo_update'."""
    estado["ultimo_update"] = datetime.now().isoformat(timespec="seconds")
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def registrar_evento(habilidad: str, correcto: bool) -> dict:
    """
    Registra un intento y devuelve la entrada actualizada de esa habilidad.
    Reglas:
      - Acierto -> sube racha, sube aciertos.
      - Fallo   -> racha = 0, sube intentos.
      - Estado se recalcula según la racha.
    """
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

    # Historial (guardamos solo lo esencial)
    estado["historial"].append({
        "ts": datetime.now().isoformat(timespec="seconds"),
        "habilidad": habilidad,
        "correcto": correcto,
    })
    # Limitamos el historial a 1000 eventos para que no crezca infinito
    estado["historial"] = estado["historial"][-1000:]

    guardar(estado)
    return hab


def reiniciar() -> None:
    """Borra todo el progreso (útil para depurar)."""
    guardar(json.loads(json.dumps(_ESTADO_INICIAL)))


def resumen() -> list[dict]:
    """Devuelve lista de habilidades con su estado, ordenada por nombre."""
    estado = cargar()
    return [
        {"habilidad": k, **v}
        for k, v in sorted(estado["habilidades"].items())
    ]