"""
Responsive Model Card component.
"""
import streamlit as st
from backend.schemas.types import ModelCatalogItem

def render_model_card(model: ModelCatalogItem, on_try_click=None):
    price_tag = "100% Free" if model.is_free else "Paid / Usage"
    badge_class = "badge-success" if model.is_free else "badge-secondary"
    
    st.markdown(
        f"""
        <div class="model-card">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.3rem;">{model.icon}</span>
                    <span class="badge-pill {badge_class}">{price_tag}</span>
                </div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 0.2rem;">{model.name}</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.6rem;">{model.provider} • ID: <code>{model.id}</code></div>
                <div style="font-size: 0.85rem; margin-bottom: 0.8rem; line-height: 1.4;">{model.description}</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.6rem;">
                {' '.join([f'<span class="badge-pill badge-primary">{c}</span>' for c in model.capabilities])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
