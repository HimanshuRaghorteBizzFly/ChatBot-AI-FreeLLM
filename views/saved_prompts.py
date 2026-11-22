"""
Saved Prompts View.
Prompt library, custom prompt creator, category filtering, and one-click chat launcher.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.repositories.storage import list_saved_prompts, create_saved_prompt, delete_saved_prompt

def render():
    render_navbar("💡 Saved Prompts & Templates", "Enterprise Prompt Engineering Library & One-Click Execution")

    col_lib, col_add = st.columns([1.7, 1.3])

    with col_lib:
        st.markdown("### 📚 Prompt Library")
        cat_filter = st.selectbox("Category Filter", options=["All", "Coding", "Engineering", "Career", "General"], index=0, key="sp_cat_filter")
        
        prompts = list_saved_prompts(category=cat_filter)
        if prompts:
            for p in prompts:
                st.markdown(
                    f"""
                    <div style="padding: 1rem; border-radius: 12px; margin-bottom: 0.8rem; background: #FFFFFF; border: 1px solid #E2E8F0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span style="font-weight: 700; font-size: 1.05rem; color: #111827;">{p['title']}</span>
                            <span class="badge-pill badge-primary">{p['category']}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #475569; line-height: 1.4; margin-bottom: 0.6rem;">{p['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                b1, b2 = st.columns([1, 4])
                with b1:
                    if st.button("🚀 Use in Chat", key=f"sp_use_{p['id']}", use_container_width=True):
                        st.session_state.pending_prompt = p["content"]
                        st.session_state.current_page = "Chat Playground"
                        st.rerun()
                with b2:
                    if st.button("🗑️ Delete", key=f"sp_del_{p['id']}"):
                        delete_saved_prompt(p["id"])
                        st.success("Prompt deleted.")
                        st.rerun()
                st.divider()
        else:
            st.info("No prompts found for this category.")

    with col_add:
        st.markdown("### ➕ Create New Prompt Template")
        new_title = st.text_input("Prompt Title", placeholder="e.g. SQL Query Optimizer", key="sp_new_title")
        new_cat = st.selectbox("Category", options=["Coding", "Engineering", "Career", "Vision", "General"], index=0, key="sp_new_cat")
        new_content = st.text_area("Prompt Content", placeholder="Enter the detailed instruction prompt...", height=140, key="sp_new_content")
        new_tags = st.text_input("Tags (comma separated)", placeholder="sql,database,optimization", key="sp_new_tags")

        if st.button("💾 Save to Library", type="primary", use_container_width=True, key="btn_save_sp"):
            if not new_title.strip() or not new_content.strip():
                st.warning("Please provide both a title and prompt content.")
            else:
                create_saved_prompt(title=new_title, content=new_content, category=new_cat, tags=new_tags)
                st.success("Prompt successfully added to your library!")
                st.rerun()
