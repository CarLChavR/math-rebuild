"""
Módulo de Reparación v3 — Fracciones heterogéneas
Con LaTeX renderizado y método visual de la mariposa.
"""

import random
from fractions import Fraction
from math import gcd


def frac_str(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def parse_user(s: str):
    s = (s or "").strip().replace(" ", "")
    if not s:
        return None
    try:
        if "/" in s:
            n, d = s.split("/")
            return Fraction(int(n), int(d))
        return Fraction(int(s))
    except Exception:
        return None


# ---------- GENERADORES (igual que antes) ----------

def gen_same_denom():
    d = random.choice([3, 4, 5, 6, 7, 8])
    n1 = random.randint(1, d - 1)
    n2 = random.randint(1, d - 1)
    op = random.choice(["+", "-"])
    if op == "+":
        if n1 + n2 > d:
            return gen_same_denom()
    else:
        if n1 <= n2:
            n1, n2 = n2, n1
            if n1 == n2:
                return gen_same_denom()
    return n1, d, n2, d, op


def gen_multiple_denom():
    while True:
        d_small = random.choice([2, 3, 4, 5])
        k = random.choice([2, 3])
        d_big = d_small * k
        n_small = random.randint(1, d_small - 1)
        n_big = random.randint(1, d_big - 1)
        op = random.choice(["+", "-"])
        f1, f2 = Fraction(n_small, d_small), Fraction(n_big, d_big)
        if op == "+" and f1 + f2 > 1:
            continue
        if op == "-" and f1 - f2 <= 0:
            continue
        if random.random() < 0.5:
            return n_small, d_small, n_big, d_big, op
        return n_big, d_big, n_small, d_small, op


def gen_coprime():
    pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5), (5, 6), (2, 7), (3, 7)]
    while True:
        d1, d2 = random.choice(pairs)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        op = random.choice(["+", "-"])
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        if op == "+" and f1 + f2 > 1:
            continue
        if op == "-" and f1 - f2 <= 0:
            continue
        if random.random() < 0.5:
            return n1, d1, n2, d2, op
        return n2, d2, n1, d1, op


def gen_common_factor():
    pairs = [(4, 6), (6, 8), (6, 9), (8, 12), (4, 8), (6, 10), (9, 12), (10, 15)]
    while True:
        d1, d2 = random.choice(pairs)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        op = random.choice(["+", "-"])
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        if op == "+" and f1 + f2 > 1:
            continue
        if op == "-" and f1 - f2 <= 0:
            continue
        if random.random() < 0.5:
            return n1, d1, n2, d2, op
        return n2, d2, n1, d1, op


GENERATORS = {
    "same_denom": gen_same_denom,
    "multiple_denom": gen_multiple_denom,
    "coprime": gen_coprime,
    "common_factor": gen_common_factor,
}


def build_exercise(case_id: str) -> dict:
    n1, d1, n2, d2, op = GENERATORS[case_id]()
    f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
    result = f1 + f2 if op == "+" else f1 - f2
    lcm = d1 * d2 // gcd(d1, d2)
    return {
        "prompt": f"{n1}/{d1} {op} {n2}/{d2}",
        "latex": rf"\frac{{{n1}}}{{{d1}}} {op} \frac{{{n2}}}{{{d2}}}",
        "answer": result,
        "hint": f"MCM({d1}, {d2}) = {lcm}. Convierte cada fracción al MCM.",
    }


# ---------- TEORÍA CON LATEX ----------

THEORY = [
    {
        "title": "0. Recordatorio visual: las 4 operaciones",
        "body": r"""
Antes de empezar, aquí tienes las **4 formas visuales** de operar con fracciones.

**Multiplicación** (línea recta — directo):
$$\frac{A}{B} \times \frac{C}{D} = \frac{A \times C}{B \times D}$$

**División** (zig-zag — cruzar):
$$\frac{A}{B} \div \frac{C}{D} = \frac{A \times D}{B \times C}$$

**Suma** (mariposa — tres productos):
$$\frac{A}{B} + \frac{C}{D} = \frac{(A \times D) + (B \times C)}{B \times D}$$

**Resta** (mariposa, mismo flujo):
$$\frac{A}{B} - \frac{C}{D} = \frac{(A \times D) - (B \times C)}{B \times D}$$

En este módulo nos enfocamos en **suma y resta** (mariposa).
""",
    },
    {
        "title": "1. ¿Qué es una fracción?",
        "body": r"""
Una fracción es **una parte de un todo**. Si partes una pizza en 4 trozos y tomas 1:

$$\frac{1}{4}$$

- **Numerador** (arriba): cuántos trozos tomas.
- **Denominador** (abajo): en cuántos trozos dividiste el todo.

**Ejemplos:**
- $\frac{3}{8}$ → 3 de 8 trozos.
- $\frac{5}{5} = 1$ → la pizza completa.
- $\frac{2}{4} = \frac{1}{2}$ → la misma cantidad, expresada distinto.

**Idea clave:** una fracción es **un número**, no dos números separados.
""",
    },
    {
        "title": "2. ¿Por qué NO se suman directo?",
        "body": r"""
Si ves $\frac{1}{2} + \frac{1}{3}$ y sumas así:

$$\frac{1}{2} + \frac{1}{3} \neq \frac{2}{5} \quad \text{(MAL)}$$

**¿Por qué?** Los denominadores son distintos ($2$ y $3$). Son "tamaños de trozo" diferentes. **No puedes apilarlos** directamente.

**Regla crítica:** nunca sumes denominadores. Solo se suman los numeradores, y solo cuando los denominadores son iguales.
""",
    },
    {
        "title": "3. Método de la Mariposa (visual)",
        "body": r"""
El método de la **mariposa** (o carita feliz) resuelve suma y resta con **3 productos**:

$$\frac{A}{B} + \frac{C}{D} = \frac{(A \times D) + (B \times C)}{B \times D}$$

**Visualmente, las flechas van así:**

1. **Diagonal 1:** $A \times D$ (arriba-izquierda × abajo-derecha)
2. **Diagonal 2:** $B \times C$ (abajo-izquierda × arriba-derecha)
3. **Horizontal:** $B \times D$ (denominador común)

**Ejemplo numérico:**
$$\frac{1}{3} + \frac{2}{5} = \frac{(1 \times 5) + (3 \times 2)}{3 \times 5} = \frac{5 + 6}{15} = \frac{11}{15}$$

**Mnemotecnia:** "arriba cruza abajo, abajo cruza arriba, y abajo por abajo".
""",
    },
    {
        "title": "4. Método del MCM (alternativa)",
        "body": r"""
Otra forma (más lenta pero más intuitiva) es usar el **Mínimo Común Múltiplo**.

**Ejemplo:** $\frac{1}{2} + \frac{1}{3}$

**Paso 1** — MCM(2, 3) = $6$.
**Paso 2** — Convierte cada fracción a sextos:
$$\frac{1}{2} = \frac{1 \times 3}{2 \times 3} = \frac{3}{6} \quad , \quad \frac{1}{3} = \frac{1 \times 2}{3 \times 2} = \frac{2}{6}$$
**Paso 3** — Suma:
$$\frac{3}{6} + \frac{2}{6} = \frac{5}{6}$$

**Ventaja:** entiendes *por qué* funciona.
**Desventaja:** más pasos que la mariposa.
""",
    },
]


# ---------- CASOS CON LATEX ----------

CASES = [
    {
        "id": "same_denom",
        "title": "Caso 1: Mismo denominador",
        "intro": r"""
Los denominadores **ya son iguales**. Solo opera los numeradores y deja el denominador igual.

**Fórmula:**
$$\frac{A}{D} + \frac{B}{D} = \frac{A + B}{D}$$

**Ejemplo visual:** $\frac{2}{5} + \frac{1}{5} = \frac{2 + 1}{5} = \frac{3}{5}$
""",
        "examples": [
            {
                "title": "Ejemplo 1: 2/5 + 1/5",
                "steps": [
                    r"Denominadores iguales ($5 = 5$) ✅",
                    r"Sumamos numeradores: $2 + 1 = 3$",
                    r"Denominador se queda: $5$",
                    r"Resultado: $\frac{3}{5}$",
                ],
            },
            {
                "title": "Ejemplo 2: 4/7 - 1/7",
                "steps": [
                    r"Denominadores iguales ($7 = 7$) ✅",
                    r"Restamos numeradores: $4 - 1 = 3$",
                    r"Denominador: $7$",
                    r"Resultado: $\frac{3}{7}$",
                ],
            },
        ],
    },
    {
        "id": "multiple_denom",
        "title": "Caso 2: Un denominador es múltiplo del otro",
        "intro": r"""
Cuando un denominador es múltiplo del otro (ej. $2$ y $4$, $3$ y $6$), el **MCM es el denominador grande**.

**Ejemplo:** MCM(2, 4) = $4$ → solo conviertes la fracción con denominador chico.
""",
        "examples": [
            {
                "title": "Ejemplo 1: 1/2 + 1/4",
                "steps": [
                    r"MCM(2, 4) = $4$ (porque 4 es múltiplo de 2)",
                    r"Convierte $\frac{1}{2}$ a cuartos: $\frac{1 \times 2}{2 \times 2} = \frac{2}{4}$",
                    r"Ahora: $\frac{2}{4} + \frac{1}{4} = \frac{3}{4}$",
                    r"Resultado: $\frac{3}{4}$",
                ],
            },
            {
                "title": "Ejemplo 2: 3/4 - 1/2",
                "steps": [
                    r"MCM(4, 2) = $4$",
                    r"Convierte $\frac{1}{2}$: $\frac{1 \times 2}{2 \times 2} = \frac{2}{4}$",
                    r"Ahora: $\frac{3}{4} - \frac{2}{4} = \frac{1}{4}$",
                    r"Resultado: $\frac{1}{4}$",
                ],
            },
        ],
    },
    {
        "id": "coprime",
        "title": "Caso 3: Denominadores coprimos (Mariposa)",
        "intro": r"""
Cuando los denominadores no comparten factores (ej. $2$ y $3$, $3$ y $5$), el **MCM es su producto**.

**Aplica la mariposa:**
$$\frac{A}{B} + \frac{C}{D} = \frac{(A \times D) + (B \times C)}{B \times D}$$

**Ejemplo visual:**
$$\frac{1}{2} + \frac{1}{3} = \frac{(1 \times 3) + (2 \times 1)}{2 \times 3} = \frac{3 + 2}{6} = \frac{5}{6}$$
""",
        "examples": [
            {
                "title": "Ejemplo 1: 1/2 + 1/3",
                "steps": [
                    r"Numerador (mariposa): $(1 \times 3) + (2 \times 1) = 3 + 2 = 5$",
                    r"Denominador (horizontal): $2 \times 3 = 6$",
                    r"Resultado: $\frac{5}{6}$",
                ],
            },
            {
                "title": "Ejemplo 2: 2/3 - 1/5",
                "steps": [
                    r"Numerador (mariposa resta): $(2 \times 5) - (3 \times 1) = 10 - 3 = 7$",
                    r"Denominador: $3 \times 5 = 15$",
                    r"Resultado: $\frac{7}{15}$",
                ],
            },
        ],
    },
    {
        "id": "common_factor",
        "title": "Caso 4: Denominadores con factor común",
        "intro": r"""
Cuando los denominadores **sí comparten factores** (ej. $4$ y $6$, $6$ y $8$), el MCM **no es el producto**.

**Ejemplo:** MCM(4, 6) = $12$, no $24$. La mariposa sigue funcionando, pero el resultado final se simplifica.
""",
        "examples": [
            {
                "title": "Ejemplo 1: 1/4 + 1/6",
                "steps": [
                    r"Mariposa: numerador = $(1 \times 6) + (4 \times 1) = 6 + 4 = 10$",
                    r"Denominador = $4 \times 6 = 24$",
                    r"Resultado antes de simplificar: $\frac{10}{24}$",
                    r"Simplifica: divide entre 2 → $\frac{5}{12}$",
                ],
            },
            {
                "title": "Ejemplo 2: 5/6 - 1/4",
                "steps": [
                    r"Mariposa (resta): numerador = $(5 \times 4) - (6 \times 1) = 20 - 6 = 14$",
                    r"Denominador = $6 \times 4 = 24$",
                    r"Resultado antes de simplificar: $\frac{14}{24}$",
                    r"Simplifica: divide entre 2 → $\frac{7}{12}$",
                ],
            },
        ],
    },
]


def build_curriculum():
    screens = []
    for t in THEORY:
        screens.append({"type": "theory", "title": t["title"], "body": t["body"]})
    for case in CASES:
        screens.append({"type": "case_intro", "title": case["title"], "body": case["intro"]})
        for ex in case["examples"]:
            screens.append({"type": "example", "title": ex["title"], "steps": ex["steps"]})
        screens.append({"type": "practice", "case_id": case["id"], "title": f"Práctica — {case['title']}"})
    screens.append({"type": "feynman", "title": "Explicación Feynman"})
    screens.append({"type": "done", "title": "Módulo completado ✅"})
    return screens