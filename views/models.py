"""
All AI Models Catalog View.
Search, multi-modality filtering, specification inspector, and model redirection.
"""
import streamlit as st
from components.navbar import render_navbar
from components.model_card import render_model_card
from backend.services.catalog import get_catalog_models, filter_catalog

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
                render_model_card(m)
                
                # Action Buttons
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button("🚀 Try Model", key=f"cat_try_{m.id}", use_container_width=True):
                        if "image" in m.capabilities:
                            st.session_state.current_page = "Image Studio"
                        elif "vision" in m.capabilities:
                            st.session_state.current_page = "Vision Studio"
                        elif "embeddings" in m.capabilities:
                            st.session_state.current_page = "Embeddings"
                        elif "reranking" in m.capabilities:
                            st.session_state.current_page = "Reranking"
                        elif "speech" in m.capabilities or "stt" in m.capabilities:
                            st.session_state.current_page = "Speech Studio"
                        elif "video" in m.capabilities:
                            st.session_state.current_page = "Video Studio"
                        else:
                            st.session_state.current_page = "Chat Playground"
                            st.session_state.selected_model = m.id
                        st.rerun()
                with b_col2:
                    with st.popover("ℹ️ Specs"):
                        st.markdown(f"### {m.name}")
                        st.markdown(f"**Provider:** {m.provider}")
                        st.markdown(f"**Actual Model ID:** `{m.id}`")
                        st.markdown(f"**Context Window:** {f'{m.context_length:,} tokens' if m.context_length else 'N/A'}")
                        st.markdown(f"**Pricing:** {m.pricing or ('100% Free' if m.is_free else 'Pay per token')}")
                        st.markdown(f"**Capabilities:** {', '.join(m.capabilities)}")
                        st.markdown(f"**Description:** {m.description}")
    else:
        st.info("No AI models found matching your criteria.")
