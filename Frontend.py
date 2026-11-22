"""
AI ChatBot & Vision Studio — Enterprise SaaS Application.
Main frontend entrypoint orchestrating the 16 functional pages, custom styling,
and multi-provider inference.
"""
import os
import sys
from pathlib import Path
import streamlit as st

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database import init_db
from components.sidebar import render_sidebar
from views import (
    dashboard,
    chat,
    models,
    image_studio,
    video_studio,
    speech_studio,
    vision,
    embeddings,
    reranking,
    comparison,
    providers,
    api_keys,
    usage,
    billing,
    saved_prompts,
    history,
    settings
)

# 1. Page Configuration
st.set_page_config(
    page_title="LLM Studio Pro • 100% Free AI Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize Database & Session State
init_db()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Load & Inject CSS
css_file = ROOT_DIR / "styles" / "theme.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Dynamic Light / Dark Theme Injection
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0B0D14 !important;
            color: #F1F5F9 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #111420 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        .metric-card, .model-card, .saas-navbar {
            background-color: #131622 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #F1F5F9 !important;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #181C2E !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F8FAFF !important;
            color: #111827 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        .metric-card, .model-card, .saas-navbar {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #111827 !important;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #CBD5E1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 4. Render Navigation Sidebar
render_sidebar()

# 5. Route to Active View
PAGE_ROUTER = {
    "Dashboard": dashboard.render,
    "Chat Playground": chat.render,
    "All Models": models.render,
    "Image Studio": image_studio.render,
    "Video Studio": video_studio.render,
    "Speech Studio": speech_studio.render,
    "Vision Studio": vision.render,
    "Embeddings": embeddings.render,
    "Reranking": reranking.render,
    "Model Comparison": comparison.render,
    "Providers": providers.render,
    "API Keys": api_keys.render,
    "Usage & Limits": usage.render,
    "Plans & Billing": billing.render,
    "Saved Prompts": saved_prompts.render,
    "Chat History": history.render,
    "Settings": settings.render,
}

active_page = st.session_state.get("current_page", "Dashboard")
view_func = PAGE_ROUTER.get(active_page, dashboard.render)
view_func()
