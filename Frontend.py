"""
AI ChatBot & Vision Studio — Simple, Clean & User-Friendly Frontend.
Supports seamless Light & Dark Mode, zero code-block glitches, and fast multi-model inference.
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
    page_title="AI Studio • Simple & Fast Multi-Model AI",
    page_icon="🤖",
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

# 3. Load Base CSS
css_file = ROOT_DIR / "styles" / "theme.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 4. Clean Dynamic Light & Dark Mode Overrides
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #1E293B !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #1E293B !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
        }
        h1, h2, h3, h4, h5, h6, label, [data-testid="stMarkdownContainer"] p {
            color: #F8FAFC !important;
        }
        .card-desc, [data-testid="stMarkdownContainer"] .card-desc {
            color: #94A3B8 !important;
        }
        .stButton > button, button[kind="secondary"] {
            background-color: #334155 !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }
        .stButton > button:hover, button[kind="secondary"]:hover {
            background-color: #475569 !important;
            color: #60A5FA !important;
            border-color: #60A5FA !important;
        }
        .stButton > button[kind="primary"], button[kind="primary"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #2563EB !important;
        }
        .stButton > button[kind="primary"]:hover, button[kind="primary"]:hover {
            background-color: #3B82F6 !important;
            border-color: #3B82F6 !important;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        [data-testid="stRadio"] label span, [data-testid="stCheckbox"] label span {
            color: #F8FAFC !important;
        }
        .tag-pill {
            background: rgba(96, 165, 250, 0.15) !important;
            color: #93C5FD !important;
        }
        section[data-testid="stSidebar"] .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            width: 100% !important;
            padding: 0.55rem 0.85rem !important;
            border-radius: 8px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.15rem !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            color: #94A3B8 !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            background-color: #334155 !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, #3730A3 0%, #4338CA 100%) !important;
            color: #FFFFFF !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: #1E293B !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #F8FAFC !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #0F172A !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        h1, h2, h3, h4, h5, h6, label, [data-testid="stMarkdownContainer"] p {
            color: #0F172A !important;
        }
        .card-desc, [data-testid="stMarkdownContainer"] .card-desc {
            color: #475569 !important;
        }
        .stButton > button, button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }
        .stButton > button:hover, button[kind="secondary"]:hover {
            background-color: #F1F5F9 !important;
            border-color: #2563EB !important;
            color: #2563EB !important;
        }
        .stButton > button[kind="primary"], button[kind="primary"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #2563EB !important;
        }
        .stButton > button[kind="primary"]:hover, button[kind="primary"]:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }
        [data-testid="stRadio"] label span, [data-testid="stCheckbox"] label span {
            color: #0F172A !important;
        }
        .tag-pill {
            background: rgba(37, 99, 235, 0.08) !important;
            color: #2563EB !important;
        }
        section[data-testid="stSidebar"] .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            width: 100% !important;
            padding: 0.55rem 0.85rem !important;
            border-radius: 8px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.15rem !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            color: #475569 !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            background-color: #F1F5F9 !important;
            border-color: #E2E8F0 !important;
            color: #0F172A !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, #2563EB 0%, #4338CA 100%) !important;
            color: #FFFFFF !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 5. Render Clean Navigation Sidebar
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
