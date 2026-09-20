"""
MathRebuild - Reconstrucción Matemática desde Cero
Versión 0.2.1 - Motor de Diagnóstico v0.1 (fix de navegación)
"""

import streamlit as st
from questions import QUESTIONS, SKILL_LABELS

st.set_page_config(
    page_title="MathRebuild",
    page_icon="🧮",
    layout="centered",
)

# --- Estado de la sesión ---
if "index" not in st.session_state:
    st.session_state.index = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "answered" not in st.session_state:
    st.session_state.answered = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None

st.title("🧮 MathRebuild")
st.subheader("Diagnóstico v0.1 — Aritmética y fracciones")

total = len(QUESTIONS)
i = st.session_state.index

# --- Pantalla de resultados finales ---
if i >= total:
    st.success(f"Diagnóstico completado. Acertaste {st.session_state.correct} de {total}.")
    st.markdown("### Resumen por habilidad")
    resumen = {}
    for h in st.session_state.history:
        resumen.setdefault(h["skill"], {"ok": 0, "total": 0})
        resumen[h["skill"]]["total"] += 1
        resumen[h["skill"]]["ok"] += int(h["correct"])
    for skill, datos in resumen.items():
        st.write(f"**{SKILL_LABELS.get(skill, skill)}:** {datos['ok']}/{datos['total']}")
    if st.button("Reiniciar diagnóstico"):
        st.session_state.index = 0
        st.session_state.correct = 0
        st.session_state.history = []
        st.session_state.answered = False
        st.session_state.feedback = None
        st.rerun()
    st.stop()

# --- Pantalla de pregunta ---
q = QUESTIONS[i]
st.progress(i / total)
st.caption(f"Pregunta {i + 1} de {total}  ·  Habilidad: {SKILL_LABELS.get(q['skill'], q['skill'])}")
st.markdown(f"### {q['prompt']}")

# --- FASE 1: preguntar (solo si no ha respondido) ---
if not st.session_state.answered:
    respuesta = st.text_input("Tu respuesta:", key=f"input_{i}")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Enviar"):
            user = respuesta.strip().replace(" ", "")
            expected = q["answer"].replace(" ", "")
            correct = (user == expected)

            st.session_state.feedback = {
                "correct": correct,
                "user": user,
                "expected": q["answer"],
                "explanation": q["explanation"],
                "hint": q["hint"],
                "error_common": q["error_common"],
            }
            st.session_state.history.append({
                "id": q["id"], "skill": q["skill"],
                "correct": correct, "answer": user,
            })
            if correct:
                st.session_state.correct += 1
            st.session_state.answered = True
            st.rerun()

    with col2:
        if st.button("No lo sé / Saltar"):
            st.session_state.feedback = {
                "correct": False,
                "user": "",
                "expected": q["answer"],
                "explanation": q["explanation"],
                "hint": q["hint"],
                "error_common": q["error_common"],
            }
            st.session_state.history.append({
                "id": q["id"], "skill": q["skill"],
                "correct": False, "answer": "",
            })
            st.session_state.answered = True
            st.rerun()

# --- FASE 2: mostrar feedback (solo si ya respondió) ---
else:
    fb = st.session_state.feedback
    if fb["correct"]:
        st.success(f"✅ ¡Correcto! {fb['explanation']}")
    else:
        st.error(f"❌ No exactamente. Respuesta correcta: **{fb['expected']}**")
        st.info(f"💡 Pista: {fb['hint']}")
        st.caption(f"Explicación: {fb['explanation']}")
        if fb["user"] == fb["error_common"]:
            st.warning("⚠️ Detectamos un error típico. Esto es información valiosa para tu perfil.")

    if st.button("Siguiente →"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.feedback = None
        st.rerun()