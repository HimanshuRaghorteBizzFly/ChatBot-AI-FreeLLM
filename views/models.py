"""
All AI Models Catalog View.
Search, multi-modality filtering, specification inspector, and model redirection.
"""
import streamlit as st
from components.navbar import render_navbar
from components.model_card import render_model_card
from components.sidebar import set_page
from backend.services.catalog import filter_catalog

def render():
    render_navbar("🤖 All AI Models Catalog", "Browse, Filter, and Benchmark Foundation Models Across All Modalities")

    # Search & Filter Controls
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.2, 1, 1])
    with f_col1:
        query = st.text_input("Search Models", placeholder="Search by name, provider, architecture, or ID...", key="models_search")
    with f_col2:
        category = st.selectbox(
            "Modality / Category",
            options=["All", "Text", "Image", "Video", "Speech", "Vision", "Reasoning", "Embeddings", "Reranking", "Multimodal"],
            index=0,
            key="models_cat"
        )
    with f_col3:
        pricing_filter = st.selectbox("Pricing", options=["All", "Free Only", "Paid Only"], index=0, key="models_price")
    with f_col4:
        sort_by = st.selectbox("Sort By", options=["Name", "Context Window"], index=0, key="models_sort")

    is_free = None
    if pricing_filter == "Free Only":
        is_free = True
    elif pricing_filter == "Paid Only":
        is_free = False

    models = filter_catalog(category=category, is_free=is_free, search=query)

    if sort_by == "Context Window":
        models = sorted(models, key=lambda m: m.context_length or 0, reverse=True)
    else:
        models = sorted(models, key=lambda m: m.name)

    st.markdown(f"**Showing {len(models)} Models**")
    st.divider()

    # Render Grid
    if models:
        cols = st.columns(3)
        for idx, m in enumerate(models):
            with cols[idx % 3]:
                render_model_card(m, on_try_key=f"cat_card_{m.id}_{idx}")
    else:
        st.info("No AI models found matching your criteria.")
