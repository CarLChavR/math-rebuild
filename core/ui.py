"""
core/ui.py — Helpers visuales reutilizables.

Centraliza la presentación para que los temas (content/*.py) no
contengan código de Streamlit ni de formato.

Si cambias un color, un emoji, o el formato del feedback, lo cambias
AQUÍ y se actualiza en todas las páginas que lo usen.
"""

from fractions import Fraction

import streamlit as st

from core import state as S


# --- Estados de dominio → (emoji, color hex, etiqueta legible) ----------
ESTADO_META = {
    S.NO_EVALUADO:   ("○", "#888888", "No evaluado"),
    S.NO_DOMINADO:   ("●", "#d32f2f", "No dominado"),
    S.EN_DESARROLLO: ("◐", "#f57c00", "En desarrollo"),
    S.FUNCIONAL:     ("◕", "#1976d2", "Funcional"),
    S.DOMINADO:      ("●", "#388e3c", "Dominado"),
}


# --- Badge de estado ----------------------------------------------------
def badge_estado(estado: str) -> str:
    """
    Devuelve HTML con el badge del estado.
    Úsalo así: st.markdown(badge_estado(estado), unsafe_allow_html=True)
    """
    emoji, color, etiqueta = ESTADO_META.get(estado, ESTADO_META[S.NO_EVALUADO])
    return (
        f"<span style='color:{color}; font-weight:600; font-size:1.05em'>"
        f"{emoji} {etiqueta}</span>"
    )


# --- Renderizado de respuestas -----------------------------------------
def respuesta_a_latex(respuesta, tipo: str) -> str:
    """
    Convierte la respuesta (int, Fraction, str) a una cadena LaTeX.
    - Enteros → '7'
    - Fracciones → '\\frac{a}{b}' (con signo normalizado al numerador)
    """
    if tipo == "frac" and isinstance(respuesta, Fraction):
        num, den = respuesta.numerator, respuesta.denominator
        if den == 1:
            return str(num)
        if den < 0:
            num, den = -num, -den
        return rf"\frac{{{num}}}{{{den}}}"
    return str(respuesta)


# --- Bloques de presentación -------------------------------------------
def mostrar_ejercicio(ejercicio: dict) -> None:
    """Renderiza el enunciado del ejercicio como bloque LaTeX."""
    st.markdown("### Resuelve:")
    st.latex(ejercicio["display"])


def mostrar_feedback(correcto: bool, ejercicio: dict) -> None:
    """
    Muestra el feedback tras verificar. Si fue error, despliega
    los pasos desarrollados y la pista.
    """
    if correcto:
        st.success("✅ ¡Correcto!")
    else:
        st.error("❌ Incorrecto. Vamos paso a paso:")
        pasos = ejercicio.get("steps") or []
        for i, paso in enumerate(pasos, 1):
            st.latex(rf"\text{{{i}.}}\quad {paso}")
        if ejercicio.get("hint"):
            st.info(f"💡 **Pista:** {ejercicio['hint']}")

    st.markdown("**Respuesta correcta:**")
    st.latex(respuesta_a_latex(ejercicio["answer"], ejercicio["answer_type"]))


def mostrar_metricas(habilidad: str) -> None:
    """
    Muestra racha, aciertos, intentos + badge de estado para una
    habilidad. Si no hay datos todavía, lo indica.
    """
    datos = next(
        (h for h in S.resumen() if h["habilidad"] == habilidad),
        None,
    )
    if not datos:
        st.caption("Aún sin datos para esta habilidad.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Racha", datos["racha"])
    c2.metric("✅ Aciertos", datos["aciertos"])
    c3.metric("🎯 Intentos", datos["intentos"])
    st.markdown(badge_estado(datos["estado"]), unsafe_allow_html=True)
