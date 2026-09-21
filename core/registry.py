"""
core/registry.py — Índice de temas disponibles.

Cuando crees un nuevo tema en content/ (por ejemplo content/decimales.py),
lo registras aquí una vez y aparece automáticamente en la app.

Cada tema debe exponer en su módulo:
    TEMA    : str  -> id interno (ej. "signos")
    NOMBRE  : str  -> etiqueta visible (ej. "➕➖ Ley de signos")
    NIVELES : list -> subniveles (ej. ["basico", "intermedio", "avanzado"])
    teoria(nivel) -> list[dict]     # bloques de LaTeX
    generar(nivel) -> dict          # nuevo ejercicio aleatorio
    explicar(ejercicio) -> list     # pasos desarrollados
"""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Tema:
    """Descriptor de un tema registrado."""
    id: str
    nombre: str
    modulo: str           # ruta del módulo (ej. "content.signos")
    fase: str             # "pre-0" | "0" | "1" ... (para ordenar)
    descripcion: str = ""


# --- Registro central ---------------------------------------------------
# Para agregar un tema: agrega una línea aquí. Nada más.
TEMAS: list[Tema] = [
    Tema(
        id="signos",
        nombre="➕➖ Ley de signos",
        modulo="content.signos",
        fase="pre-0",
        descripcion="Suma y resta con números negativos, 2 a 5 términos.",
    ),
    # Próximos (los descomentamos cuando existan los archivos):
    # Tema(id="jerarquia",     nombre="🔢 Jerarquía (PEMDAS)", modulo="content.jerarquia",     fase="pre-0"),
    # Tema(id="fracciones",    nombre="🍕 Fracciones",          modulo="content.fracciones",    fase="pre-0"),
    # Tema(id="decimales",     nombre="💯 Decimales",           modulo="content.decimales",     fase="pre-0"),
    # Tema(id="factorizacion", nombre="🧩 Factorización",       modulo="content.factorizacion", fase="pre-0"),
    # Tema(id="potencias",     nombre="⚡ Potencias y raíces",  modulo="content.potencias",     fase="pre-0"),
    # Tema(id="proporciones",  nombre="📐 Proporciones",        modulo="content.proporciones",  fase="pre-0"),
]


# --- Utilidades ---------------------------------------------------------
def listar() -> list[Tema]:
    """Devuelve todos los temas registrados."""
    return list(TEMAS)


def buscar(tema_id: str) -> Tema | None:
    """Devuelve el tema con ese id, o None si no existe."""
    for t in TEMAS:
        if t.id == tema_id:
            return t
    return None


def cargar_modulo(tema_id: str):
    """
    Importa dinámicamente el módulo del tema.
    Devuelve None si no existe (para no romper la app en desarrollo).
    """
    import importlib
    t = buscar(tema_id)
    if t is None:
        return None
    try:
        return importlib.import_module(t.modulo)
    except ModuleNotFoundError as e:
        # Silenciamos el error: en desarrollo es normal tener temas
        # registrados cuyo archivo aún no existe.
        print(f"[registry] Módulo no encontrado: {t.modulo} ({e})")
        return None