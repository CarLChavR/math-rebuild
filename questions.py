"""
Banco de preguntas del Motor de Diagnóstico v2 — CON NÚMEROS ALEATORIOS
Cada sesión genera 10 ejercicios nuevos.
"""

import random
from fractions import Fraction


SKILL_LABELS = {
    "ley_de_signos": "Ley de signos",
    "jerarquia_operaciones": "Jerarquía de operaciones",
    "fracciones_heterogeneas": "Fracciones heterogéneas",
}


def _frac_str(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def gen_signo() -> dict:
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    kind = random.choice(["sum_neg", "sum_dos_neg", "sub_neg", "tres_terminos"])

    if kind == "sum_neg":
        prompt = f"{a} + (-{b})"
        answer = a - b
        hint = f"Sumar -{b} es restar {b}: {a} - {b} = {answer}."
    elif kind == "sum_dos_neg":
        prompt = f"-{a} + (-{b})"
        answer = -(a + b)
        hint = f"Dos negativos se suman y conservan el signo: -({a}+{b}) = {answer}."
    elif kind == "sub_neg":
        prompt = f"{a} - (-{b})"
        answer = a + b
        hint = f"Restar un negativo es sumar: {a} + {b} = {answer}."
    else:
        c = random.randint(2, 9)
        prompt = f"{a} - (-{b}) + (-{c})"
        answer = a + b - c
        hint = f"Paso 1: {a} - (-{b}) = {a+b}. Paso 2: {a+b} + (-{c}) = {answer}."

    return {
        "id": f"signos_{random.randint(10000, 99999)}",
        "skill": "ley_de_signos",
        "prompt": f"{prompt} = ?",
        "answer": str(answer),
        "explanation": f"El resultado es {answer}.",
        "hint": hint,
        "error_common": None,
    }


def gen_jerarquia() -> dict:
    a = random.randint(2, 12)
    b = random.randint(2, 6)
    c = random.randint(2, 6)
    kind = random.choice(["mult_first", "paren", "mixto"])

    if kind == "mult_first":
        prompt = f"{a} + {b} × {c}"
        answer = a + b * c
        hint = f"Multiplicación primero: {b} × {c} = {b*c}. Luego {a} + {b*c} = {answer}."
    elif kind == "paren":
        prompt = f"({a} + {b}) × {c}"
        answer = (a + b) * c
        hint = f"Paréntesis primero: {a} + {b} = {a+b}. Luego {a+b} × {c} = {answer}."
    else:
        d = random.randint(1, 8)
        prompt = f"{a} - {b} × {c} + {d}"
        answer = a - b * c + d
        hint = (f"Multiplicación primero: {b} × {c} = {b*c}. "
                f"Luego: {a} - {b*c} + {d} = {answer}.")

    return {
        "id": f"jera_{random.randint(10000, 99999)}",
        "skill": "jerarquia_operaciones",
        "prompt": f"{prompt} = ?",
        "answer": str(answer),
        "explanation": f"El resultado es {answer}.",
        "hint": hint,
        "error_common": None,
    }


def gen_fraccion() -> dict:
    d1 = random.choice([2, 3, 4, 5, 6, 7, 8])
    d2 = random.choice([2, 3, 4, 5, 6, 7, 8])
    while d1 == d2:
        d2 = random.choice([2, 3, 4, 5, 6, 7, 8])

    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    op = random.choice(["+", "-"])

    f1, f2 = Fraction(n1, d1), Fraction(n2, d2)

    if op == "+":
        if f1 + f2 > 2:
            return gen_fraccion()
        result = f1 + f2
        prompt = f"{n1}/{d1} + {n2}/{d2}"
        latex = rf"\frac{{{n1}}}{{{d1}}} + \frac{{{n2}}}{{{d2}}}"
        hint = f"Encuentra el MCM de {d1} y {d2} y convierte cada fracción."
    else:
        if f1 <= f2:
            f1, f2 = f2, f1
            n1, d1, n2, d2 = f1.numerator, f1.denominator, f2.numerator, f2.denominator
        result = f1 - f2
        prompt = f"{n1}/{d1} - {n2}/{d2}"
        latex = rf"\frac{{{n1}}}{{{d1}}} - \frac{{{n2}}}{{{d2}}}"
        hint = f"Encuentra el MCM de {d1} y {d2} y convierte cada fracción."

    return {
        "id": f"frac_{random.randint(10000, 99999)}",
        "skill": "fracciones_heterogeneas",
        "prompt": f"{prompt} = ?",
        "latex": f"{latex} = ?",
        "answer": _frac_str(result),
        "explanation": f"El resultado simplificado es {_frac_str(result)}.",
        "hint": hint,
        "error_common": None,
    }


def build_diagnostic() -> list:
    """
    Genera una nueva lista de 10 ejercicios aleatorios:
    4 de ley de signos, 3 de jerarquía, 3 de fracciones.
    """
    questions = []
    for _ in range(4):
        questions.append(gen_signo())
    for _ in range(3):
        questions.append(gen_jerarquia())
    for _ in range(3):
        questions.append(gen_fraccion())

    random.shuffle(questions)
    return questions