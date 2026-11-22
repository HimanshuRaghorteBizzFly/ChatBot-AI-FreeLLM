"""
Responsive Model Card component matching LLM Studio Pro reference layout.
Built using native Streamlit containers and zero-indent HTML to guarantee
zero code-block or raw HTML leaks.
"""
import streamlit as st
from backend.schemas.types import ModelCatalogItem

def render_model_card(model: ModelCatalogItem, on_try_key: str = None):
    """Renders a user-friendly model card with zero raw HTML/JSON code blocks."""
    is_free = model.is_free
    icon_display = model.icon or "🤖"
    clean_name = model.name.split(":")[0].strip()

    ctx_str = f"{model.context_length // 1000}K ctx" if model.context_length else "Adaptive ctx"
    price_val = getattr(model, "pricing", None)
    price_str = price_val or ("Free" if is_free else "$5 / 1M")
    free_tier_str = '<span class="free-tier-tag">Free tier</span>' if is_free else '<span>Commercial</span>'

    # Native Streamlit card container
    with st.container(border=True):
        # Header line: Icon + Title on left, Badge on right
        c_title, c_badge = st.columns([2.6, 1.2])
        with c_title:
            st.markdown(f"<div style='font-weight: 700; font-size: 1rem; display: flex; align-items: center; gap: 0.4rem;'><span>{icon_display}</span> <span>{clean_name}</span></div>", unsafe_allow_html=True)
        with c_badge:
            if is_free:
                st.markdown("<div style='text-align: right;'><span class='badge-free'>Free</span></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align: right;'><span class='badge-premium'>⭐ Premium</span></div>", unsafe_allow_html=True)

        # Modality Tags (Single line, zero indent)
        caps = model.capabilities[:3]
        tags_html = "".join([f"<span class='tag-pill'>{c.title()}</span> " for c in caps])
        st.markdown(f"<div style='margin: 0.4rem 0 0.5rem 0;'>{tags_html}</div>", unsafe_allow_html=True)

        # Description text
        desc = model.description or "Advanced foundation intelligence model."
        st.markdown(f"<div class='card-desc'>{desc}</div>", unsafe_allow_html=True)

        # Specs row (Context • Pricing • Free tier)
        st.markdown(f"<div class='card-specs-row'><span>{ctx_str}</span> <span>•</span> <span>{price_str}</span> <span>•</span> {free_tier_str}</div>", unsafe_allow_html=True)

        # Action Buttons
        col_try, col_key = st.columns([1.2, 1.2])
        with col_try:
            btn_key = on_try_key or f"try_{model.id}"
            if st.button("▷ Try Now", key=btn_key, use_container_width=True, type="primary"):
                if "image" in model.capabilities:
                    st.session_state.current_page = "Image Studio"
                elif "vision" in model.capabilities:
                    st.session_state.current_page = "Vision Studio"
                elif "speech" in model.capabilities or "speech_to_text" in model.capabilities:
                    st.session_state.current_page = "Speech Studio"
                elif "video" in model.capabilities:
                    st.session_state.current_page = "Video Studio"
                else:
                    st.session_state.current_page = "Chat Playground"
                    st.session_state.selected_model = model.id
                st.rerun()

        with col_key:
            pop_label = "Get API Key" if is_free else "View Details"
            with st.popover(pop_label, use_container_width=True):
                st.markdown(f"### {model.name}")
                st.markdown(f"**Provider:** {model.provider}")
                st.markdown(f"**Model ID:** `{model.id}`")
                st.markdown(f"**Context Window:** {ctx_str}")
                st.markdown(f"**Pricing:** {price_str}")
                st.markdown(f"**Capabilities:** {', '.join(model.capabilities)}")
                st.markdown(f"**Access:** {'🟢 100% Free Forever' if is_free else '🔑 Custom API Key'}")
                st.caption(desc)
                if st.button("Open in Chat", key=f"pop_open_{model.id}", use_container_width=True):
                    st.session_state.current_page = "Chat Playground"
                    st.session_state.selected_model = model.id
                    st.rerun()
