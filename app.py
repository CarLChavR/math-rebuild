"""
MathRebuild - Reconstrucción Matemática desde Cero
Versión 0.1 - Verificación inicial de la aplicación
"""

import streamlit as st

st.set_page_config(
    page_title="MathRebuild",
    page_icon="🧮",
    layout="centered",
)

st.title("🧮 MathRebuild")
st.subheader("Reconstrucción Matemática desde Cero")

st.markdown("""
Bienvenido, Carlos.

Este es el primer prototipo de tu sistema de aprendizaje adaptativo.

**Estado del proyecto:**
- ✅ Repositorio creado en GitHub
- ✅ PyCharm configurado con entorno virtual
- ✅ Streamlit, pandas y sympy instalados
- ⏳ Esperando el primer módulo de diagnóstico

### ¿Qué sigue?
En las próximas sesiones construiremos el **Motor de Diagnóstico**
para identificar tu punto de partida real en aritmética y fracciones.

El sistema seguirá la lógica del **Master Prompt v9.0**:
diagnóstico → prerrequisitos → reparación → práctica → dominio por evidencia.
""")

st.divider()

st.info("Presiona el botón para verificar que la aplicación funciona correctamente.")

if st.button("✅ Verificar funcionamiento"):
    st.success("¡La aplicación está corriendo correctamente!")
    st.balloons()