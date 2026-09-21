"""
content/signos.py — Tema: Ley de signos.

Cubre:
    - Suma y resta con números negativos
    - 2 a 5 términos
    - Diferentes posiciones de los negativos
    - Doble signo (restar un negativo)

Contrato del tema (ver core/registry.py):
    TEMA, NOMBRE, NIVELES      -> identidad
    teoria(nivel) -> list[dict]     -> bloques de teoría
    generar(nivel) -> dict          -> nuevo ejercicio aleatorio
    explicar(ejercicio) -> list[str] -> pasos desarrollados
"""

import random


# --- Identidad del tema -------------------------------------------------
TEMA = "signos"
NOMBRE = "➕➖ Ley de signos"
NIVELES = ["basico", "intermedio", "avanzado"]


# --- Teoría -------------------------------------------------------------
_TEORIA = {
    "basico": [
        {
            "titulo": "¿Qué es un número negativo?",
            "texto": (
                "Un número negativo representa una cantidad **por debajo de cero**: "
                "una deuda, una temperatura bajo cero, un movimiento hacia atrás. "
                "En la recta numérica viven a la izquierda del 0."
            ),
            "latex": r"-5 \;<\; -3 \;<\; 0 \;<\; 2 \;<\; 4",
        },
        {
            "titulo": "Sumar dos del mismo signo",
            "texto": (
                "Cuando los dos números tienen el mismo signo, "
                "**sumas sus valores absolutos** y conservas el signo común."
            ),
            "latex": r"3 + 5 = 8 \qquad (-3) + (-5) = -8",
        },
        {
            "titulo": "Sumar dos de signos opuestos",
            "texto": (
                "Cuando los signos son opuestos, **restas el menor valor absoluto "
                "del mayor** y el resultado lleva el signo del que tenía mayor "
                "valor absoluto."
            ),
            "latex": r"(-7) + 4 = -3 \qquad 9 + (-5) = 4",
        },
    ],
    "intermedio": [
        {
            "titulo": "Restar es sumar el opuesto",
            "texto": (
                "Esta es la clave para manejar todos los signos: "
                "restar un número es lo mismo que **sumar su opuesto**."
            ),
            "latex": r"a - b \;=\; a + (-b)",
        },
        {
            "titulo": 'El temido "menos por menos"',
            "texto": (
                "Restar un número negativo es **sumar** su valor absoluto. "
                "Dos negaciones seguidas se cancelan."
            ),
            "latex": r"5 - (-3) = 5 + 3 = 8 \qquad (-2) - (-7) = -2 + 7 = 5",
        },
    ],
    "avanzado": [
        {
            "titulo": "Cadenas largas (4-5 términos)",
            "texto": (
                "Con varios términos, trabájalos **de izquierda a derecha**, "
                "reescribiendo cada resta como suma del opuesto."
            ),
            "latex": (
                r"-11 + 18 - (-4) + 7 - (-3) "
                r"\;=\; -11 + 18 + 4 + 7 + 3 \;=\; 21"
            ),
        },
    ],
}


def teoria(nivel: str = "basico") -> list[dict]:
    """Devuelve los bloques de teoría para el nivel dado."""
    if nivel not in _TEORIA:
        nivel = "basico"
    return list(_TEORIA[nivel])


# --- Núcleo del generador ----------------------------------------------
def _nivel_params(nivel: str) -> tuple[int, int, int]:
    """(min_terminos, max_terminos, rango_absoluto)"""
    if nivel == "intermedio":
        return (3, 4, 20)
    if nivel == "avanzado":
        return (4, 5, 20)
    return (2, 3, 10)  # basico


def _generar_ops(n: int, rango: int) -> list[tuple[str, int]]:
    """
    Devuelve n pares (operador, valor) donde operador ∈ {'+', '-'}
    y valor es un entero NO nulo (puede ser positivo o negativo).

    El primer operador siempre es '+' (no se muestra en el display).

    Ejemplo: [('+', -11), ('+', 18), ('-', -4), ('+', 7), ('-', -3)]
    Se mostrará como: -11 + 18 - (-4) + 7 - (-3)
    Y su valor efectivo será: -11 + 18 + 4 + 7 + 3 = 21
    """
    def _rand_valor() -> int:
        v = 0
        while v == 0:
            v = random.randint(-rango, rango)
        return v

    ops: list[tuple[str, int]] = [("+", _rand_valor())]
    for _ in range(n - 1):
        signo = random.choice(["+", "-"])
        ops.append((signo, _rand_valor()))
    return ops


def _formatear(ops: list[tuple[str, int]]) -> str:
    """
    Convierte la lista de operaciones en un string legible.
    - Primer término: se muestra el valor tal cual (con su signo).
    - Términos siguientes: '{op} {valor}' o '{op} ({valor})' si valor < 0.
    """
    partes = []
    for i, (op, v) in enumerate(ops):
        if i == 0:
            partes.append(str(v))
        elif v < 0:
            partes.append(f"{op} ({v})")
        else:
            partes.append(f"{op} {v}")
    return " ".join(partes)


def _evaluar(ops: list[tuple[str, int]]) -> int:
    """Calcula el valor efectivo: suma si op='+', resta si op='-'."""
    total = ops[0][1]
    for op, v in ops[1:]:
        total = total + v if op == "+" else total - v
    return total


def _pasos(ops: list[tuple[str, int]]) -> list[str]:
    """Lista de pasos LaTeX mostrando la acumulación."""
    pasos = []
    acc = ops[0][1]
    for op, v in ops[1:]:
        if op == "+":
            nuevo = acc + v
            if v < 0:
                pasos.append(rf"{acc} + ({v}) = {nuevo}")
            else:
                pasos.append(rf"{acc} + {v} = {nuevo}")
        else:  # op == '-'
            nuevo = acc - v
            if v < 0:
                pasos.append(rf"{acc} - ({v}) = {acc} + {abs(v)} = {nuevo}")
            else:
                pasos.append(rf"{acc} - {v} = {nuevo}")
        acc = nuevo
    return pasos


def generar(nivel: str = "basico") -> dict:
    """Genera un ejercicio aleatorio de ley de signos."""
    min_t, max_t, rango = _nivel_params(nivel)
    n = random.randint(min_t, max_t)
    ops = _generar_ops(n, rango)

    return {
        "display": _formatear(ops),
        "answer": _evaluar(ops),
        "answer_type": "int",
        "hint": r"Restar un negativo = sumar. Ej: $a - (-b) = a + b$.",
        "steps": _pasos(ops),
        "nivel": nivel,
    }


def explicar(ejercicio: dict) -> list[str]:
    """Devuelve los pasos LaTeX para un ejercicio dado."""
    return list(ejercicio.get("steps", []))