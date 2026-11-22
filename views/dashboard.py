"""
Dashboard View.
Overview metrics, fast actions, dynamic model explorer, and recent activities.
"""
import streamlit as st
from components.navbar import render_navbar
from components.model_card import render_model_card
from backend.services.catalog import get_catalog_models, filter_catalog
from backend.repositories.storage import get_usage_summary, list_conversations, list_saved_prompts
from backend.providers.registry import registry

def render():
    render_navbar("📊 Dashboard Overview", "Enterprise Multi-LLM, Vision & Media Intelligence")

    usage = get_usage_summary()
    conversations = list_conversations(limit=5)
    all_models = get_catalog_models()

    # 1. Top Metrics Bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Requests</div>
                <div class="metric-value" style="color: #2563EB;">{usage.get('total_requests', 0):,}</div>
                <div style="font-size: 0.8rem; color: #10B981;">⚡ Real-time tracked</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Tokens Processed</div>
                <div class="metric-value" style="color: #7C3AED;">{usage.get('total_tokens', 0):,}</div>
                <div style="font-size: 0.8rem; color: #64748B;">Prompt & completion</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Estimated Spend</div>
                <div class="metric-value" style="color: #059669;">${usage.get('total_cost', 0.0):.4f}</div>
                <div style="font-size: 0.8rem; color: #10B981;">🟢 Free tier active</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Catalog Models</div>
                <div class="metric-value" style="color: #06B6D4;">{len(all_models)}</div>
                <div style="font-size: 0.8rem; color: #64748B;">Across 8 modalities</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Quick Actions
    st.markdown("### ⚡ Quick Launch")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        if st.button("💬 Launch AI Chat", use_container_width=True):
            st.session_state.current_page = "Chat Playground"
            st.rerun()
    with q_col2:
        if st.button("🎨 Open Image Studio", use_container_width=True):
            st.session_state.current_page = "Image Studio"
            st.rerun()
    with q_col3:
        if st.button("👁️ Visual Image Q&A", use_container_width=True):
            st.session_state.current_page = "Vision Studio"
            st.rerun()
    with q_col4:
        if st.button("🔑 Manage API Keys", use_container_width=True):
            st.session_state.current_page = "API Keys"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Model Search & Category Filter
    st.markdown("### 🤖 Featured AI Model Showcase")
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("🔍 Search Models", placeholder="Search by name, provider, or ID...", label_visibility="collapsed")
    with f_col2:
        category_filter = st.selectbox(
            "Category",
            options=["All", "Text", "Image", "Video", "Speech", "Vision", "Reasoning", "Embeddings", "Reranking"],
            label_visibility="collapsed"
        )
    with f_col3:
        free_only = st.checkbox("Free Models Only", value=False)

    filtered_models = filter_catalog(
        category=category_filter,
        is_free=True if free_only else None,
        search=search_query
    )

    # Render models in 3 columns
    if filtered_models:
        cols = st.columns(3)
        for idx, m in enumerate(filtered_models[:6]):
            with cols[idx % 3]:
                render_model_card(m)
                if st.button(f"Try {m.name.split(':')[0]}", key=f"dash_try_{m.id}", use_container_width=True):
                    if "image" in m.capabilities:
                        st.session_state.current_page = "Image Studio"
                    elif "vision" in m.capabilities:
                        st.session_state.current_page = "Vision Studio"
                    elif "embeddings" in m.capabilities:
                        st.session_state.current_page = "Embeddings"
                    else:
                        st.session_state.current_page = "Chat Playground"
                        st.session_state.selected_model = m.id
                    st.rerun()
    else:
        st.info("No models matched your search criteria.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Recent Activity & Conversations
    st.markdown("### 📜 Recent Conversations")
    if conversations:
        for c in conversations:
            r_col1, r_col2, r_col3 = st.columns([3, 2, 1])
            with r_col1:
                st.markdown(f"**{c['title']}**")
                st.caption(f"Provider: {c['provider']} • Model: {c['model']}")
            with r_col2:
                st.markdown(f"🕒 {c['updated_at']}")
                st.caption(f"Messages: {c['message_count']}")
            with r_col3:
                if st.button("Open", key=f"open_dash_conv_{c['id']}", use_container_width=True):
                    st.session_state.active_conversation_id = c["id"]
                    st.session_state.current_page = "Chat Playground"
                    st.rerun()
            st.divider()
    else:
        st.caption("No conversations yet. Launch the AI Chat Playground to start your first session!")
