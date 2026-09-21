"""
app.py — MathRebuild v2

Router minimalista:
  1. Lee los temas registrados en core/registry.py.
  2. Por cada tema, muestra 3 pestañas: Teoría | Practicar | Mis métricas.
  3. Guarda cada intento en data/student_state.json (persistente).

Toda la matemática vive en content/*.py.
Toda la presentación vive en core/ui.py.
Toda la persistencia vive en core/state.py.
Este archivo solo ORQUESTA.
"""

from fractions import Fraction

import streamlit as st

from core import state as S
from core import ui
from core.registry import listar, buscar, cargar_modulo


# --- Configuración de página (debe ir primero) -------------------------
st.set_page_config(
    page_title="MathRebuild",
    page_icon="🧮",
    layout="wide",
)

st.title("🧮 MathRebuild")
st.caption("Sistema Adaptativo de Reconstrucción Matemática")


# --- Sidebar: selector de tema y nivel ---------------------------------
temas_disponibles = listar()

if not temas_disponibles:
    st.error(
        "No hay temas registrados. Revisa `core/registry.py` — "
        "la lista `TEMAS` está vacía."
    )
    st.stop()

opciones_tema = {t.id: f"{t.nombre}  ({t.fase})" for t in temas_disponibles}
tema_id = st.sidebar.selectbox(
    "📚 Tema:",
    options=list(opciones_tema.keys()),
    format_func=lambda k: opciones_tema[k],
)

tema_meta = buscar(tema_id)
modulo = cargar_modulo(tema_id)

if modulo is None:
    st.error(
        f"El tema **{tema_meta.nombre}** está registrado pero su módulo "
        f"`{tema_meta.modulo}` no existe todavía. "
        f"Crea el archivo y vuelve a intentar."
    )
    st.stop()

# Selector de nivel (solo si el tema define niveles)
niveles = getattr(modulo, "NIVELES", [])
if niveles:
    nivel = st.sidebar.selectbox(
        "🎚️ Nivel:",
        options=niveles,
        format_func=lambda n: n.capitalize(),
    )
else:
    nivel = "basico"

st.sidebar.divider()
st.sidebar.caption(
    f"Fase: **{tema_meta.fase}**  \n"
    f"Módulo: `{tema_meta.modulo}`"
)


# --- Pestañas ----------------------------------------------------------
tab_teoria, tab_practicar, tab_metricas = st.tabs(
    ["📖 Teoría", "🎯 Practicar", "📊 Mis métricas"]
)


# --- TAB 1: Teoría -----------------------------------------------------
with tab_teoria:
    st.subheader(f"Teoría — {tema_meta.nombre}")
    bloques = modulo.teoria(nivel)
    if not bloques:
        st.info("Aún no hay teoría para este nivel.")
    for b in bloques:
        st.markdown(f"#### {b['titulo']}")
        st.markdown(b["texto"])
        if "latex" in b:
            st.latex(b["latex"])
        st.divider()


# --- TAB 2: Practicar --------------------------------------------------
with tab_practicar:
    # Claves de session_state separadas por tema+nivel
    key_ejercicio = f"ej_{tema_id}_{nivel}"
    key_fase      = f"fase_{tema_id}_{nivel}"
    key_ultimo_ok = f"ok_{tema_id}_{nivel}"
    key_contador  = f"n_{tema_id}_{nivel}"

    if key_ejercicio not in st.session_state:
        st.session_state[key_ejercicio] = modulo.generar(nivel)
        st.session_state[key_fase] = "asking"
        st.session_state[key_ultimo_ok] = None
        st.session_state[key_contador] = 0

    def _nuevo_ejercicio():
        st.session_state[key_ejercicio] = modulo.generar(nivel)
        st.session_state[key_fase] = "asking"
        st.session_state[key_ultimo_ok] = None
        st.session_state[key_contador] += 1

    ejercicio = st.session_state[key_ejercicio]
    fase = st.session_state[key_fase]

    if fase == "asking":
        ui.mostrar_ejercicio(ejercicio)

        input_key = f"input_{tema_id}_{nivel}_{st.session_state[key_contador]}"
        respuesta_str = st.text_input(
            "Tu respuesta:",
            key=input_key,
            placeholder="Ej: -8   ó   7/4   ó   0.75",
        )

        col1, col2 = st.columns(2)
        with col1:
            verificar = st.button(
                "✅ Verificar", type="primary", use_container_width=True
            )
        with col2:
            saltar = st.button("⏭️ Saltar", use_container_width=True)

        if verificar:
            if not respuesta_str.strip():
                st.warning("Escribe una respuesta antes de verificar.")
            else:
                try:
                    tipo = ejercicio["answer_type"]
                    if tipo == "int":
                        respuesta = int(respuesta_str.strip().replace(",", "."))
                    elif tipo == "frac":
                        respuesta = Fraction(respuesta_str.strip())
                    else:
                        respuesta = respuesta_str.strip()

                    correcto = (respuesta == ejercicio["answer"])

                    # Persistimos el evento en el estado global (JSON)
                    S.registrar_evento(tema_id, correcto)

                    st.session_state[key_ultimo_ok] = correcto
                    st.session_state[key_fase] = "feedback"
                    st.rerun()

                except (ValueError, ZeroDivisionError):
                    st.error(
                        "No pude interpretar tu respuesta. "
                        "Usa un entero (ej. `-8`) o fracción (ej. `7/4`)."
                    )

        if saltar:
            _nuevo_ejercicio()
            st.rerun()

    else:  # fase == "feedback"
        correcto = st.session_state[key_ultimo_ok]
        ui.mostrar_ejercicio(ejercicio)
        ui.mostrar_feedback(correcto, ejercicio)

        if st.button(
            "⏭️ Siguiente ejercicio",
            type="primary",
            use_container_width=True,
        ):
            _nuevo_ejercicio()
            st.rerun()

    st.divider()
    ui.mostrar_metricas(tema_id)


# --- TAB 3: Métricas ---------------------------------------------------
with tab_metricas:
    st.subheader("📊 Tu progreso")
    ui.mostrar_metricas(tema_id)

    st.divider()
    with st.expander("⚙️ Opciones avanzadas"):
        st.caption(
            "El progreso se guarda en `data/student_state.json` "
            "y se conserva entre sesiones."
        )
        if st.button("🗑️ Reiniciar TODO mi progreso"):
            S.reiniciar()
            st.success("Progreso borrado. Recargando…")
            st.rerun()