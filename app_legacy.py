"""
MathRebuild - Reconstrucción Matemática desde Cero
Versión 0.4.1 - Diagnóstico aleatorio + Reparación v3
"""

import streamlit as st
from questions import build_diagnostic, SKILL_LABELS
from repair import build_curriculum, build_exercise, parse_user, frac_str

st.set_page_config(page_title="MathRebuild", page_icon="🧮", layout="centered")


def init_state():
    defaults = {
        "mode": "diagnostico",
        # Diagnóstico
        "index": 0, "correct": 0, "history": [],
        "answered": False, "feedback": None,
        "questions": None,
        # Reparación
        "repair_screen": 0, "screens": None,
        "practice_exercise": None, "practice_streak": 0,
        "feynman_text": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# Generar set aleatorio la primera vez en esta sesión
if st.session_state.questions is None:
    st.session_state.questions = build_diagnostic()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🧮 MathRebuild")
    st.caption("FASE PRE-0 · Master Prompt v9.0")
    st.divider()
    opciones = ["🔬 Diagnóstico", "🛠️ Reparación — Fracciones"]
    idx = 0 if st.session_state.mode == "diagnostico" else 1
    eleccion = st.radio("Modo:", opciones, index=idx)
    st.session_state.mode = "diagnostico" if eleccion.startswith("🔬") else "reparacion"
    st.divider()
    st.caption(f"🔑 Set actual: {st.session_state.questions[0]['id']}")
    st.caption("📌 Los errores son datos, no fracasos.")


# ---------- DIAGNÓSTICO ----------
def render_diagnostico():
    st.title("🧮 MathRebuild")
    st.subheader("Diagnóstico v0.1 — Aritmética y fracciones")

    qs = st.session_state.questions
    total = len(qs)
    i = st.session_state.index

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
        st.divider()
        if st.button("🛠️ Ir al módulo de reparación"):
            st.session_state.mode = "reparacion"
            st.session_state.repair_screen = 0
            st.session_state.screens = None
            st.session_state.practice_exercise = None
            st.session_state.practice_streak = 0
            st.rerun()
        if st.button("🔄 Reiniciar con 10 preguntas NUEVAS"):
            st.session_state.questions = build_diagnostic()   # ← generador
            st.session_state.index = 0
            st.session_state.correct = 0
            st.session_state.history = []
            st.session_state.answered = False
            st.session_state.feedback = None
            st.rerun()
        return

    q = qs[i]
    st.progress(i / total)
    st.caption(f"Pregunta {i+1} de {total} · Habilidad: {SKILL_LABELS.get(q['skill'], q['skill'])}")
    if q.get("latex"):
        st.markdown(f"### $${q['latex']}$$")
    else:
        st.markdown(f"### {q['prompt']}")

    if not st.session_state.answered:
        respuesta = st.text_input("Tu respuesta:", key=f"input_{i}_{q['id']}")
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("Enviar"):
                user = respuesta.strip().replace(" ", "")
                expected = q["answer"].replace(" ", "")
                correct = (user == expected)
                st.session_state.feedback = {
                    "correct": correct, "user": user, "expected": q["answer"],
                    "explanation": q["explanation"], "hint": q["hint"],
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
        with c2:
            if st.button("No lo sé / Saltar"):
                st.session_state.feedback = {
                    "correct": False, "user": "", "expected": q["answer"],
                    "explanation": q["explanation"], "hint": q["hint"],
                    "error_common": q["error_common"],
                }
                st.session_state.history.append({
                    "id": q["id"], "skill": q["skill"], "correct": False, "answer": "",
                })
                st.session_state.answered = True
                st.rerun()
    else:
        fb = st.session_state.feedback
        if fb["correct"]:
            st.success(f"✅ ¡Correcto! {fb['explanation']}")
        else:
            st.error(f"❌ Respuesta correcta: **{fb['expected']}**")
            st.info(f"💡 {fb['hint']}")
            st.caption(f"Explicación: {fb['explanation']}")
            if fb.get("error_common") and fb["user"] == fb["error_common"]:
                st.warning("⚠️ Error típico detectado.")
        if st.button("Siguiente →"):
            st.session_state.index += 1
            st.session_state.answered = False
            st.session_state.feedback = None
            st.rerun()


# ---------- REPARACIÓN ----------
def render_reparacion():
    if st.session_state.screens is None:
        st.session_state.screens = build_curriculum()

    screens = st.session_state.screens
    i = st.session_state.repair_screen

    if i >= len(screens):
        st.success("🎉 ¡Módulo completado!")
        return

    screen = screens[i]
    st.title("🛠️ Reparación — Fracciones heterogéneas")
    st.progress(i / len(screens))
    st.caption(f"Pantalla {i+1} de {len(screens)}")
    st.markdown(f"## {screen['title']}")

    if screen["type"] in ("theory", "case_intro", "example"):
        if screen["type"] == "example":
            for idx_step, step in enumerate(screen["steps"], 1):
                st.markdown(f"**Paso {idx_step}:** {step}")
        else:
            st.markdown(screen["body"])
        if st.button("Siguiente →", key=f"next_{i}"):
            st.session_state.repair_screen += 1
            st.session_state.practice_exercise = None
            st.session_state.practice_streak = 0
            st.rerun()

    elif screen["type"] == "practice":
        if st.session_state.practice_exercise is None:
            st.session_state.practice_exercise = build_exercise(screen["case_id"])

        ex = st.session_state.practice_exercise
        streak = st.session_state.practice_streak

        st.info(f"Necesitas **2 correctas seguidas**. Llevas: **{streak}/2**. "
                "Si fallas, los números cambian y el contador vuelve a 0.")
        st.markdown(f"### $${ex['latex']} = ?$$")

        resp = st.text_input("Tu respuesta (ej: 3/4 o 5):",
                             key=f"pinput_{i}_{streak}_{ex['prompt']}")

        if st.button("Comprobar", key=f"pcheck_{i}_{streak}_{ex['prompt']}"):
            user = parse_user(resp)
            if user is None:
                st.warning("Escribe una fracción válida (ej: 3/4).")
            elif user == ex["answer"]:
                new_streak = streak + 1
                if new_streak >= 2:
                    st.success(f"✅ ¡Correcto! Era {frac_str(ex['answer'])}. ¡Caso completado!")
                    st.session_state.repair_screen += 1
                    st.session_state.practice_exercise = None
                    st.session_state.practice_streak = 0
                    st.rerun()
                else:
                    st.session_state.practice_streak = new_streak
                    st.session_state.practice_exercise = build_exercise(screen["case_id"])
                    st.rerun()
            else:
                st.error(f"❌ Era **{frac_str(ex['answer'])}**. Contador reiniciado.")
                st.info(f"💡 {ex['hint']}")
                st.session_state.practice_streak = 0
                st.session_state.practice_exercise = build_exercise(screen["case_id"])
                st.rerun()

    elif screen["type"] == "feynman":
        st.markdown("Explica con tus palabras, en 2 o 3 líneas, "
                    "**por qué NO se puede sumar $\\frac{1}{2} + \\frac{1}{3}$ como $\\frac{2}{5}$**.")
        texto = st.text_area("Tu explicación:", key="feynman_text", height=150)
        if st.button("Guardar y continuar →", key=f"fnext_{i}"):
            if len(texto.strip()) < 15:
                st.warning("Escribe al menos 2 o 3 líneas.")
            else:
                st.session_state.repair_screen += 1
                st.rerun()

    elif screen["type"] == "done":
        st.success("🎉 ¡Has completado la reparación de fracciones heterogéneas!")
        st.markdown("""
**Lo que lograste:**
- Teoría completa con visualización de las 4 operaciones.
- 8 ejemplos guiados con método de la mariposa y del MCM.
- 4 casos con práctica aleatoria.

**Siguiente paso:** volver al diagnóstico y verificar tu mejora.
""")
        st.balloons()
        if st.button("🔄 Volver al diagnóstico"):
            st.session_state.mode = "diagnostico"
            st.rerun()


# ---------- ROUTER ----------
if st.session_state.mode == "diagnostico":
    render_diagnostico()
else:
    render_reparacion()