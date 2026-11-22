"""
Simple, user-friendly Model Card component.
100% native Streamlit components with zero raw code block artifacts.
"""
import streamlit as st
from backend.schemas.types import ModelCatalogItem
from components.sidebar import set_page

def render_model_card(model: ModelCatalogItem, on_try_key: str = None):
    """Renders a clean, user-friendly model card."""
    is_free = model.is_free
    icon = model.icon or "🤖"
    clean_name = model.name.split(":")[0].strip()
    ctx_str = f"{model.context_length // 1000}K ctx" if model.context_length else "Adaptive ctx"
    price_str = getattr(model, "pricing", None) or ("Free" if is_free else "$5 / 1M")

    with st.container(border=True):
        # Header: Icon + Name on left, Badge on right
        c_title, c_badge = st.columns([2.8, 1.2])
        with c_title:
            st.markdown(f"**{icon} {clean_name}**")
        with c_badge:
            badge_class = "badge-free" if is_free else "badge-premium"
            badge_label = "Free" if is_free else "⭐ Pro"
            st.markdown(f"<div style='text-align: right;'><span class='{badge_class}'>{badge_label}</span></div>", unsafe_allow_html=True)

        # Capabilities tags
        tags_html = " ".join([f"<span class='tag-pill'>{c.title()}</span>" for c in model.capabilities[:3]])
        st.markdown(f"<div style='margin: 0.2rem 0 0.5rem 0;'>{tags_html}</div>", unsafe_allow_html=True)

        # Description
        desc = model.description or "High-performance AI model."
        st.caption(desc)

        # Specs row
        st.markdown(f"<div style='font-size: 0.8rem; opacity: 0.7; margin-bottom: 0.8rem;'>{ctx_str} • {price_str} • {model.provider}</div>", unsafe_allow_html=True)

        # Action Button
        btn_key = on_try_key or f"try_{model.id}"
        action_label = "🎨 Generate Image" if "image" in model.capabilities else "👁️ Analyze Vision" if "vision" in model.capabilities else "💬 Launch in Chat"
        if st.button(action_label, key=btn_key, use_container_width=True, type="primary"):
            if "image" in model.capabilities:
                set_page("Image Studio")
            elif "vision" in model.capabilities:
                set_page("Vision Studio")
            elif "speech" in model.capabilities or "speech_to_text" in model.capabilities:
                set_page("Speech Studio")
            elif "video" in model.capabilities:
                set_page("Video Studio")
            else:
                set_page("Chat Playground")
                st.session_state.selected_model = model.id
            st.rerun()
