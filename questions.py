"""
Banco de preguntas del Motor de Diagnóstico v0.1
Cubre: ley de signos, jerarquía de operaciones, fracciones heterogéneas.
"""

# Cada pregunta tiene:
#   id: identificador único
#   skill: habilidad evaluada (para el modelo del estudiante)
#   prompt: enunciado
#   answer: respuesta correcta (string; se compara con la del estudiante)
#   explanation: por qué es esa respuesta (para el feedback)
#   hint: pista si el estudiante se equivoca
#   error_common: error típico esperado (para diagnóstico)

QUESTIONS = [
    {
        "id": "signos_01",
        "skill": "ley_de_signos",
        "prompt": "8 + (-3) = ?",
        "answer": "5",
        "explanation": "Sumar un negativo equivale a restar: 8 - 3 = 5.",
        "hint": "Sumar -3 es moverte 3 unidades a la izquierda desde 8.",
        "error_common": "11",
    },
    {
        "id": "signos_02",
        "skill": "ley_de_signos",
        "prompt": "-8 + (-3) = ?",
        "answer": "-11",
        "explanation": "Dos negativos se suman y conservan el signo: -8 - 3 = -11.",
        "hint": "Estás debiendo 8 y pides prestado 3 más. ¿Cuánto debes en total?",
        "error_common": "-5",
    },
    {
        "id": "signos_03",
        "skill": "ley_de_signos",
        "prompt": "7 - (-4) = ?",
        "answer": "11",
        "explanation": "Restar un negativo es sumar: 7 + 4 = 11.",
        "hint": "Restar -4 equivale a quitar una deuda de 4.",
        "error_common": "3",
    },
    {
        "id": "signos_04",
        "skill": "ley_de_signos",
        "prompt": "-5 - (-2) = ?",
        "answer": "-3",
        "explanation": "-5 - (-2) = -5 + 2 = -3.",
        "hint": "Dos negativos seguidos se convierten en positivo.",
        "error_common": "-7",
    },
    {
        "id": "jerarquia_01",
        "skill": "jerarquia_operaciones",
        "prompt": "2 + 3 × 4 = ?",
        "answer": "14",
        "explanation": "Primero la multiplicación: 3 × 4 = 12. Luego la suma: 2 + 12 = 14.",
        "hint": "¿Qué operación tiene prioridad, la suma o la multiplicación?",
        "error_common": "20",
    },
    {
        "id": "jerarquia_02",
        "skill": "jerarquia_operaciones",
        "prompt": "(2 + 3) × 4 = ?",
        "answer": "20",
        "explanation": "Los paréntesis primero: 2 + 3 = 5. Luego: 5 × 4 = 20.",
        "hint": "El paréntesis cambia el orden. Primero lo de adentro.",
        "error_common": "14",
    },
    {
        "id": "jerarquia_03",
        "skill": "jerarquia_operaciones",
        "prompt": "10 - 2 × 3 + 1 = ?",
        "answer": "5",
        "explanation": "Multiplicación primero: 2 × 3 = 6. Luego izquierda a derecha: 10 - 6 + 1 = 5.",
        "hint": "Aplica PEMDAS: primero multiplicación, luego sumas y restas de izquierda a derecha.",
        "error_common": "25",
    },
    {
        "id": "fracciones_01",
        "skill": "fracciones_heterogeneas",
        "prompt": "1/2 + 1/3 = ?",
        "answer": "5/6",
        "explanation": "Común denominador 6: 3/6 + 2/6 = 5/6.",
        "hint": "Busca el mínimo común múltiplo de 2 y 3.",
        "error_common": "2/5",
    },
    {
        "id": "fracciones_02",
        "skill": "fracciones_heterogeneas",
        "prompt": "3/4 - 1/2 = ?",
        "answer": "1/4",
        "explanation": "Común denominador 4: 3/4 - 2/4 = 1/4.",
        "hint": "Convierte 1/2 a cuartos: 1/2 = 2/4.",
        "error_common": "2/2",
    },
    {
        "id": "fracciones_03",
        "skill": "fracciones_heterogeneas",
        "prompt": "2/3 × 3/5 = ?",
        "answer": "2/5",
        "explanation": "Multiplica numeradores y denominadores: (2×3)/(3×5) = 6/15 = 2/5.",
        "hint": "Multiplica arriba con arriba y abajo con abajo. Luego simplifica.",
        "error_common": "6/8",
    },
]

# Etiquetas legibles para mostrar en la app
SKILL_LABELS = {
    "ley_de_signos": "Ley de signos",
    "jerarquia_operaciones": "Jerarquía de operaciones",
    "fracciones_heterogeneas": "Fracciones heterogéneas",
}