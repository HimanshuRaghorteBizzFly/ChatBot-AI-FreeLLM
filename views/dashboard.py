"""
Dashboard / All-in-One Hub View.
Simple, clean, user-friendly UI with quick tool launchers, model explorer,
and instant chat starter.
"""
import streamlit as st
from components.navbar import render_navbar
from components.model_card import render_model_card
from backend.services.catalog import filter_catalog

def render():
    render_navbar("All-in-One AI Studio", "Chat with top LLMs, generate photorealistic images & analyze vision • 100% Free")

    # 1. Quick Launch Tool Cards (Simple 4-Column Grid)
    st.markdown("### ⚡ Quick Launch Tools")
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        with st.container(border=True):
            st.markdown("#### 💬 AI Chat")
            st.caption("Multi-turn reasoning with Nemotron, Gemini & Groq")
            if st.button("Open Chat", key="hub_open_chat", use_container_width=True, type="primary"):
                st.session_state.current_page = "Chat Playground"
                st.rerun()

    with t2:
        with st.container(border=True):
            st.markdown("#### 🎨 Image Studio")
            st.caption("High-res art generation with Microsoft MAI")
            if st.button("Generate Art", key="hub_open_img", use_container_width=True):
                st.session_state.current_page = "Image Studio"
                st.rerun()

    with t3:
        with st.container(border=True):
            st.markdown("#### 👁️ Vision Studio")
            st.caption("Upload images & ask questions with Gemini Vision")
            if st.button("Analyze Image", key="hub_open_vision", use_container_width=True):
                st.session_state.current_page = "Vision Studio"
                st.rerun()

    with t4:
        with st.container(border=True):
            st.markdown("#### 🎙️ Voice & Audio")
            st.caption("Whisper transcription & neural voice synthesis")
            if st.button("Open Audio", key="hub_open_voice", use_container_width=True):
                st.session_state.current_page = "Speech Studio"
                st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 2. Featured AI Models Explorer (Simple, Uncluttered)
    st.markdown("### 🤖 Featured AI Models")
    
    f1, f2 = st.columns([2.5, 1.5])
    with f1:
        search_query = st.text_input("Search Models", placeholder="🔍 Search by name, provider, or capability...", label_visibility="collapsed", key="simple_hub_search")
    with f2:
        cat_filter = st.selectbox(
            "Filter Category",
            options=["All", "Free Only", "Text", "Image", "Vision", "Speech", "Reasoning"],
            index=0,
            label_visibility="collapsed",
            key="simple_hub_cat"
        )

    is_free = True if cat_filter == "Free Only" else None
    actual_cat = "All" if cat_filter == "Free Only" else cat_filter

    models = filter_catalog(category=actual_cat, is_free=is_free, search=search_query)

    # Render clean 3-column cards
    if models:
        for i in range(0, min(len(models), 9), 3):
            chunk = models[i:i+3]
            cols = st.columns(3)
            for idx, m in enumerate(chunk):
                with cols[idx]:
                    render_model_card(m, on_try_key=f"dash_card_{m.id}_{i}_{idx}")
    else:
        st.info("No models match your search criteria.")
