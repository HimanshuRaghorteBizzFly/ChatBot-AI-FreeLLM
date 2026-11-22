"""
Reranking View.
Scores and sorts candidate documents against a search query using cross-attention semantic relevance.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.services.reranking import rerank_documents

def render():
    render_navbar("📊 Document Reranking Studio", "Cross-Attention Semantic Scoring and Precision Retrieval Ranking")

    col_in, col_out = st.columns([1.4, 1.6])

    with col_in:
        st.markdown("### 🔍 Search Query & Documents")
        query = st.text_input(
            "Search Query",
            value="How does GPU quantization accelerate LLM inference?",
            key="rerank_query_in"
        )

        st.caption("Enter Candidate Documents (separated by double newlines or blank lines):")
        sample_docs = (
            "Model quantization reduces parameter precision from 16-bit to 4-bit, slashing VRAM bandwidth bottlenecks and speeding up matrix multiplications on tensor cores.\n\n"
            "The capital city of France is Paris, known for its cafe culture and the Eiffel Tower.\n\n"
            "FlashAttention-2 optimizes memory reads from HBM to SRAM to minimize memory overhead during multi-head attention passes.\n\n"
            "Baking sourdough bread requires flour, water, salt, and a wild yeast fermentation starter."
        )
        docs_raw = st.text_area("Candidate Documents", value=sample_docs, height=220, key="rerank_docs_in")

        rerank_clicked = st.button("🚀 Rerank Documents", type="primary", use_container_width=True, key="btn_run_rerank")

    with col_out:
        st.markdown("### 🏆 Semantic Ranking Results")
        if rerank_clicked:
            documents = [d.strip() for d in docs_raw.split("\n\n") if d.strip()]
            if not query.strip() or not documents:
                st.warning("Please provide both a search query and candidate documents.")
            else:
                with st.spinner("Computing cross-attention relevance scores..."):
                    ranked = rerank_documents(query=query, documents=documents)
                    
                    for item in ranked:
                        score = item["score"]
                        badge_color = "#10B981" if score > 0.6 else "#F59E0B" if score > 0.3 else "#EF4444"
                        
                        st.markdown(
                            f"""
                            <div style="padding: 1rem; border-radius: 12px; margin-bottom: 0.8rem; background: rgba(37, 99, 235, 0.04); border: 1px solid rgba(226, 232, 240, 0.8);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                                    <span style="font-weight: 800; font-size: 1.1rem; color: #2563EB;">Rank #{item['rank']}</span>
                                    <span style="background: {badge_color}20; color: {badge_color}; border: 1px solid {badge_color}; padding: 0.2rem 0.6rem; border-radius: 9999px; font-weight: 700; font-size: 0.85rem;">
                                        Score: {score:.4f}
                                    </span>
                                </div>
                                <div style="font-size: 0.9rem; line-height: 1.45; color: #1E293B;">{item['document']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.info("💡 Enter your query and candidate documents, then click **Rerank Documents**.")
