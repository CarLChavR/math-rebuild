# --- TAB 1: Teoría -----------------------------------------------------
def _anim_for_block(tema_id: str, idx: int, bloque: dict):
    """
    Returns (scene_code, scene_class) for a given theory block.
    Falls back to None if no animation is available.
    """
    # --- signos: custom per-block animations ---
    if tema_id == "signos":
        if idx == 0:   # ¿Qué es un número negativo?
            return MH.number_line_scene(value=-3)
        if idx == 1:   # Sumar dos del mismo signo
            return MH.two_numbers_scene(a=-3, b=-5, result=-8)
        if idx == 2:   # Sumar dos de signos opuestos
            return MH.two_numbers_scene(a=-7, b=4, result=-3)

    # --- fallback: generic number line ---
    return MH.number_line_scene(value=0)


with tab_teoria:
    st.subheader(f"Teoría — {tema_meta.nombre}")
    bloques = modulo.teoria(nivel)
    if not bloques:
        st.info("Aún no hay teoría para este nivel.")

    for idx, b in enumerate(bloques):
        st.markdown(f"#### {b['titulo']}")
        st.markdown(b["texto"])
        if "latex" in b:
            st.latex(b["latex"])

        # --- Botón de animación específico por bloque ---
        anim_key = f"anim_teoria_{tema_id}_{nivel}_{idx}"
        if st.button("🎬 Ver animación", key=f"btn_{anim_key}"):
            with st.spinner("Renderizando animación… (30–60 s)"):
                result = _anim_for_block(tema_id, idx, b)
                if result is None:
                    st.warning("No hay animación definida para este bloque.")
                else:
                    code, cls = result
                    video_bytes = render_manim_scene(code, cls)
                    if video_bytes:
                        st.session_state[anim_key] = video_bytes
                    else:
                        st.error("No se pudo renderizar la animación.")

        if anim_key in st.session_state:
            st.video(st.session_state[anim_key])

        st.divider()