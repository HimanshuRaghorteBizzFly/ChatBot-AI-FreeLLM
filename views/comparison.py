"""
Model Comparison View.
Side-by-side benchmark of two distinct models running on the same prompt.
"""
import time
import streamlit as st
from components.navbar import render_navbar
from backend.services.catalog import get_catalog_models
from backend.providers.registry import registry

def render():
    render_navbar("⚖️ AI Model Comparison", "Side-by-Side Response, Latency, and Reasoning Benchmark")

    all_models = [m for m in get_catalog_models() if "chat" in m.capabilities]
    model_names = [f"{m.provider} - {m.name} ({m.id})" for m in all_models]
    model_map = {f"{m.provider} - {m.name} ({m.id})": m for m in all_models}

    c_sel1, c_sel2 = st.columns(2)
    with c_sel1:
        sel_a = st.selectbox("Model A (Baseline)", options=model_names, index=0, key="cmp_model_a")
    with c_sel2:
        default_b_idx = 1 if len(model_names) > 1 else 0
        sel_b = st.selectbox("Model B (Challenger)", options=model_names, index=default_b_idx, key="cmp_model_b")

    prompt = st.text_area(
        "Benchmark Prompt",
        value="Explain the architectural differences between Transformer Attention and State Space Models (Mamba) in 3 concise bullet points.",
        height=90,
        key="cmp_prompt"
    )

    compare_clicked = st.button("⚡ Run Side-by-Side Benchmark", type="primary", use_container_width=True, key="btn_run_cmp")

    if compare_clicked:
        model_item_a = model_map[sel_a]
        model_item_b = model_map[sel_b]

        col_a, col_b = st.columns(2)

        # Execution Model A
        with col_a:
            st.markdown(f"### 🔵 {model_item_a.name}")
            st.caption(f"Provider: {model_item_a.provider} • ID: `{model_item_a.id}`")
            with st.spinner(f"Running {model_item_a.name}..."):
                start_a = time.time()
                provider_a = registry.get_provider(model_item_a.provider.split("/")[0].strip())
                resp_text_a = ""
                if provider_a:
                    try:
                        stream = provider_a.chat_stream([{"role": "user", "content": prompt}], model=model_item_a.id)
                        resp_text_a = "".join(list(stream))
                    except Exception as e:
                        resp_text_a = f"⚠️ Error: {str(e)}"
                else:
                    resp_text_a = "Provider not active."
                dur_a = time.time() - start_a

                words_a = len(resp_text_a.split())
                st.metric("Latency", f"{dur_a:.2f}s", f"{words_a} words")
                st.markdown(resp_text_a)

        # Execution Model B
        with col_b:
            st.markdown(f"### 🟣 {model_item_b.name}")
            st.caption(f"Provider: {model_item_b.provider} • ID: `{model_item_b.id}`")
            with st.spinner(f"Running {model_item_b.name}..."):
                start_b = time.time()
                provider_b = registry.get_provider(model_item_b.provider.split("/")[0].strip())
                resp_text_b = ""
                if provider_b:
                    try:
                        stream = provider_b.chat_stream([{"role": "user", "content": prompt}], model=model_item_b.id)
                        resp_text_b = "".join(list(stream))
                    except Exception as e:
                        resp_text_b = f"⚠️ Error: {str(e)}"
                else:
                    resp_text_b = "Provider not active."
                dur_b = time.time() - start_b

                words_b = len(resp_text_b.split())
                st.metric("Latency", f"{dur_b:.2f}s", f"{words_b} words")
                st.markdown(resp_text_b)
    else:
        st.info("💡 Select two models and click **Run Side-by-Side Benchmark** to compare outputs.")
