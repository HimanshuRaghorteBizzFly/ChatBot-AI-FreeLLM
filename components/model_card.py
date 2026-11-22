"""
Responsive Model Card component matching LLM Studio Pro reference layout.
"""
import streamlit as st
from backend.schemas.types import ModelCatalogItem

def render_model_card(model: ModelCatalogItem, on_try_key: str = None):
    """Renders a model card matching the reference image layout."""
    is_free = model.is_free
    badge_html = '<span class="badge-free">Free</span>' if is_free else '<span class="badge-premium">⭐ Premium</span>'
    
    ctx_str = f"{model.context_length // 1000}K ctx" if model.context_length else "Adaptive ctx"
    price_val = getattr(model, "pricing", None)
    price_str = price_val or ("Free" if is_free else "$5 / 1M")
    free_tier_str = '<span class="free-tier-tag">Free tier</span>' if is_free else '<span>Commercial</span>'

    # Brand icon mapping
    icon_display = model.icon or "🤖"

    st.markdown(
        f"""
        <div class="model-card-ref">
            <div>
                <div class="card-top-line">
                    <div class="card-brand-title">
                        <span style="font-size: 1.25rem;">{icon_display}</span>
                        <span>{model.name.split(':')[0]}</span>
                    </div>
                    <div>{badge_html}</div>
                </div>

                <div class="card-tags-row">
                    {' '.join([f'<span class="tag-pill">{c.title()}</span>' for c in model.capabilities[:3]])}
                </div>

                <div class="card-desc">
                    {model.description}
                </div>

                <div class="card-specs-row">
                    <span>{ctx_str}</span>
                    <span>•</span>
                    <span>{price_str}</span>
                    <span>•</span>
                    {free_tier_str}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Action Buttons: Try Now & Details
    col_try, col_key = st.columns([1.2, 1.2])
    with col_try:
        button_key = on_try_key or f"try_{model.id}"
        if st.button("▷ Try Now", key=button_key, use_container_width=True, type="primary"):
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
        popover_label = "View Details" if not is_free else "Get API Key"
        with st.popover(popover_label, use_container_width=True):
            st.markdown(f"### {model.name}")
            st.markdown(f"**Provider:** {model.provider}")
            st.markdown(f"**Model ID:** `{model.id}`")
            st.markdown(f"**Context Window:** {ctx_str}")
            st.markdown(f"**Pricing:** {price_str}")
            st.markdown(f"**Capabilities:** {', '.join(model.capabilities)}")
            st.markdown(f"**Status:** {'🟢 100% Free Tier Available' if is_free else '🔑 API Key Configurable'}")
            st.markdown(f"_{model.description}_")
            if st.button("Open in Chat", key=f"pop_try_{model.id}", use_container_width=True):
                st.session_state.current_page = "Chat Playground"
                st.session_state.selected_model = model.id
                st.rerun()
