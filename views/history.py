"""
Chat History View.
Full conversation history management, search, renaming, transcript inspection, and export.
"""
import json
import streamlit as st
from components.navbar import render_navbar
from backend.repositories.storage import (
    list_conversations,
    get_conversation_messages,
    rename_conversation,
    delete_conversation
)

def render():
    render_navbar("📜 Conversation History", "Audit Past Sessions, Search Transcripts, Rename & Export")

    search_query = st.text_input("🔍 Search Past Chats", placeholder="Filter by title, provider, or model...", key="hist_search")
    conversations = list_conversations(limit=100)

    if search_query:
        conversations = [
            c for c in conversations
            if search_query.lower() in c["title"].lower() or search_query.lower() in c["provider"].lower() or search_query.lower() in c["model"].lower()
        ]

    st.markdown(f"**Found {len(conversations)} Conversations**")
    st.divider()

    if conversations:
        for c in conversations:
            c_col1, c_col2 = st.columns([3, 1])

            with c_col1:
                st.markdown(f"### 💬 {c['title']}")
                st.caption(f"Provider: **{c['provider']}** • Model: **{c['model']}** • Last Active: {c['updated_at']} • {c['message_count']} messages")

            with c_col2:
                act1, act2 = st.columns(2)
                with act1:
                    if st.button("Resume", key=f"hist_resume_{c['id']}", use_container_width=True):
                        st.session_state.active_conversation_id = c["id"]
                        st.session_state.current_page = "Chat Playground"
                        st.rerun()
                with act2:
                    if st.button("Delete", key=f"hist_del_{c['id']}", use_container_width=True):
                        delete_conversation(c["id"])
                        st.rerun()

            # Transcript expander
            with st.expander(f"📜 View Transcript for #{c['id']}", expanded=False):
                msgs = get_conversation_messages(c["id"])
                for m in msgs:
                    st.markdown(f"**{m['role'].upper()}:** {m['content']}")
                    st.divider()

                # Export buttons
                d_c1, d_c2 = st.columns(2)
                with d_c1:
                    st.download_button(
                        "📥 Export JSON",
                        data=json.dumps(msgs, indent=2),
                        file_name=f"chat_export_{c['id']}.json",
                        mime="application/json",
                        key=f"dl_json_{c['id']}"
                    )
                with d_c2:
                    md_text = f"# {c['title']}\n\n" + "\n\n".join([f"**{m['role'].upper()}:**\n{m['content']}" for m in msgs])
                    st.download_button(
                        "📥 Export Markdown",
                        data=md_text,
                        file_name=f"chat_export_{c['id']}.md",
                        mime="text/markdown",
                        key=f"dl_md_{c['id']}"
                    )

            st.divider()
    else:
        st.info("No conversations found.")
