"""
AI ChatBot & Vision Studio — LLM Studio Pro SaaS Application.
Main frontend entrypoint orchestrating all views, custom styling,
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

# 3. Load & Inject Global CSS
css_file = ROOT_DIR / "styles" / "theme.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 4. Dynamic Light / Dark Mode Overrides
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        /* Dark Mode Canvas */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
        }
        [data-testid="stHeader"] {
            background-color: rgba(11, 15, 25, 0.85) !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }
        /* Cards, Containers & Hub Hero */
        [data-testid="stVerticalBlockBorderWrapper"] > div,
        .hero-hub-container,
        .studio-topbar,
        .model-card-ref,
        .usage-box,
        .sidebar-go-pro-card {
            background-color: #151D30 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
        }
        .hero-text-block h1 {
            color: #FFFFFF !important;
        }
        .hero-text-block p {
            color: #94A3B8 !important;
        }
        .floating-brand-badge {
            background-color: #1E293B !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }
        /* All Text & Headings */
        h1, h2, h3, h4, h5, h6, label, [data-testid="stMarkdownContainer"] p {
            color: #F8FAFC !important;
        }
        .card-desc, .action-subtitle {
            color: #94A3B8 !important;
        }
        /* Buttons */
        .stButton > button, button[kind="secondary"] {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover, button[kind="secondary"]:hover {
            background-color: #2D3B55 !important;
            border-color: #60A5FA !important;
            color: #60A5FA !important;
        }
        .stButton > button[kind="primary"], button[kind="primary"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #2563EB !important;
            border-radius: 8px !important;
        }
        .stButton > button[kind="primary"]:hover, button[kind="primary"]:hover {
            background-color: #3B82F6 !important;
            border-color: #3B82F6 !important;
        }
        /* Form Inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #131B2E !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 8px !important;
        }
        /* Radio & Checkboxes */
        [data-testid="stRadio"] label span, [data-testid="stCheckbox"] label span {
            color: #F8FAFC !important;
        }
        /* Badges & Tags */
        .tag-pill {
            background-color: #1E293B !important;
            color: #93C5FD !important;
        }
        .card-specs-row {
            color: #94A3B8 !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        /* Light Mode Canvas */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }
        [data-testid="stHeader"] {
            background-color: rgba(248, 250, 252, 0.85) !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #0F172A !important;
        }
        /* Cards, Containers & Hub Hero */
        [data-testid="stVerticalBlockBorderWrapper"] > div,
        .hero-hub-container,
        .studio-topbar,
        .model-card-ref,
        .usage-box,
        .sidebar-go-pro-card {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        .hero-text-block h1 {
            color: #0F172A !important;
        }
        .hero-text-block p {
            color: #64748B !important;
        }
        .floating-brand-badge {
            background-color: #FFFFFF !important;
            border-color: #E2E8F0 !important;
        }
        /* All Text & Headings */
        h1, h2, h3, h4, h5, h6, label, [data-testid="stMarkdownContainer"] p {
            color: #0F172A !important;
        }
        .card-desc, .action-subtitle {
            color: #475569 !important;
        }
        /* Buttons */
        .stButton > button, button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover, button[kind="secondary"]:hover {
            background-color: #F1F5F9 !important;
            border-color: #94A3B8 !important;
            color: #2563EB !important;
        }
        .stButton > button[kind="primary"], button[kind="primary"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #2563EB !important;
            border-radius: 8px !important;
        }
        .stButton > button[kind="primary"]:hover, button[kind="primary"]:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
        }
        /* Form Inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }
        /* Radio & Checkboxes */
        [data-testid="stRadio"] label span, [data-testid="stCheckbox"] label span {
            color: #0F172A !important;
        }
        /* Badges & Tags */
        .tag-pill {
            background-color: #F1F5F9 !important;
            color: #475569 !important;
        }
        .card-specs-row {
            color: #64748B !important;
            border-color: #F1F5F9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 5. Render Navigation Sidebar
render_sidebar()

# 6. Route to Active View
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
