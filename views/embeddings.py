"""
Embeddings View.
Dense vector embeddings generation and semantic cosine similarity tester.
"""
import json
import streamlit as st
from components.navbar import render_navbar
from backend.services.embeddings import generate_text_embedding, cosine_similarity

def render():
    render_navbar("🧬 Vector Embeddings Studio", "Generate Dense Semantic Vector Representations & Compute Similarity")

    tab1, tab2 = st.tabs(["📊 Generate Embeddings", "📐 Semantic Cosine Similarity Tester"])

    with tab1:
        e_col1, e_col2 = st.columns([1.5, 1.5])
        with e_col1:
            st.markdown("### 📝 Input Text")
            text = st.text_area(
                "Text to Embed",
                value="Artificial intelligence models transform high-dimensional semantic spaces into numerical vector representations.",
                height=140,
                key="embed_text_in"
            )
            embed_model = st.selectbox("Embedding Model", options=["text-embedding-004", "gemini-embedding-v1"], index=0, key="embed_model_sel")
            
            gen_clicked = st.button("⚡ Generate Vector", type="primary", use_container_width=True, key="btn_gen_emb")

        with e_col2:
            st.markdown("### 🧬 Embedding Metrics & Sample")
            if gen_clicked:
                if not text.strip():
                    st.warning("Please enter text to generate embeddings.")
                else:
                    with st.spinner("Generating dense vector representation..."):
                        res = generate_text_embedding(text, model=embed_model)
                        if res.get("error"):
                            st.error(res["error"])
                        else:
                            vec = res.get("vector", [])
                            st.success(f"Generated {len(vec)}-dimensional dense embedding!")
                            st.metric("Vector Dimension", len(vec))
                            st.text_area("Sample Dimensions (First 15)", value=str(vec[:15]), height=90)
                            st.download_button(
                                "📥 Download Full Vector (.json)",
                                data=json.dumps(vec),
                                file_name="embedding_vector.json",
                                mime="application/json",
                                use_container_width=True
                            )
            else:
                st.info("💡 Enter text on the left and click Generate Vector to inspect dimensions.")

    with tab2:
        st.markdown("### 📐 Semantic Cosine Similarity Calculator")
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            text_a = st.text_area("Text A", value="The quick brown fox jumps over the lazy dog.", height=90, key="sim_text_a")
        with s_col2:
            text_b = st.text_area("Text B", value="A fast auburn canine leaps across an inactive pup.", height=90, key="sim_text_b")

        if st.button("⚖️ Compare Semantic Similarity", type="primary", use_container_width=True, key="btn_calc_sim"):
            with st.spinner("Computing cosine distance between semantic vectors..."):
                res_a = generate_text_embedding(text_a)
                res_b = generate_text_embedding(text_b)
                score = cosine_similarity(res_a.get("vector", []), res_b.get("vector", []))
                
                pct = round(score * 100, 2)
                st.markdown(f"### Similarity Score: `{score:.4f}` ({pct}%)")
                st.progress(max(0.0, min(1.0, score)))
                if score > 0.8:
                    st.success("🟢 Highly similar semantic meaning!")
                elif score > 0.5:
                    st.info("🟡 Moderately related concepts.")
                else:
                    st.warning("🔴 Low semantic correlation.")
