"""
AI Chat Playground View.
Multi-turn conversational interface with streaming, reasoning traces, parameter tuning,
and SQLAlchemy database persistence.
"""
import json
import streamlit as st
from components.navbar import render_navbar
from backend.services.chat import stream_chat_response
from backend.repositories.storage import (
    create_conversation,
    list_conversations,
    get_conversation_messages,
    add_message
)
from backend.providers.openrouter import OPENROUTER_MODELS, format_openrouter_model_name
from backend.providers.registry import registry
from backend.config import get_config_var

def render():
    render_navbar("💬 AI Chat Playground", "Multi-Turn Streaming with Deep Reasoning & Model Switching")

    # Ensure active conversation ID exists in session state
    if "active_conversation_id" not in st.session_state or not st.session_state.active_conversation_id:
        st.session_state.active_conversation_id = create_conversation(
            title="New Chat",
            provider="OpenRouter",
            model="nvidia/nemotron-3.5-super-vl:free"
        )

    # Provider & Model selection bar
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 2, 1])

    with ctrl_col1:
        provider_name = st.selectbox(
            "AI Provider",
            options=["OpenRouter", "Google Gemini", "Groq", "Free AI", "Ollama"],
            index=0,
            key="chat_provider_select"
        )

    with ctrl_col2:
        if provider_name == "OpenRouter":
            model_options = OPENROUTER_MODELS
            selected_model = st.selectbox(
                "Model",
                options=model_options,
                format_func=format_openrouter_model_name,
                index=0,
                key="chat_model_select"
            )
        elif provider_name == "Google Gemini":
            gemini_provider = registry.get_provider("Google Gemini")
            models = [m.id for m in gemini_provider.list_models()] if gemini_provider else ["gemini-3.1-flash-lite"]
            selected_model = st.selectbox("Model", options=models, index=0, key="chat_model_select")
        elif provider_name == "Groq":
            groq_provider = registry.get_provider("Groq")
            models = [m.id for m in groq_provider.list_models()] if groq_provider else ["openai/gpt-oss-120b"]
            selected_model = st.selectbox("Model", options=models, index=0, key="chat_model_select")
        elif provider_name == "Free AI":
            selected_model = "Free GPT-4o Mini"
            st.selectbox("Model", options=["Free GPT-4o Mini (Cloud)"], index=0, disabled=True, key="chat_model_select")
        else:
            ollama_provider = registry.get_provider("Ollama")
            models = [m.id for m in ollama_provider.list_models()] if ollama_provider else ["llama3.2"]
            selected_model = st.selectbox("Model", options=models, index=0, key="chat_model_select")

    with ctrl_col3:
        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.active_conversation_id = create_conversation(
                title="New Chat",
                provider=provider_name,
                model=selected_model
            )
            st.rerun()

    # Advanced Configuration Expander
    with st.expander("⚙️ System Prompt & Advanced Parameters", expanded=False):
        sys_col, prm_col = st.columns([2, 1])
        with sys_col:
            system_prompt = st.text_area(
                "System Prompt",
                value="You are an expert, insightful, and helpful AI assistant. Provide clear, structured, and accurate responses.",
                height=90,
                key="chat_system_prompt"
            )
        with prm_col:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.05, key="chat_temp")
            max_tokens = st.slider("Max Tokens", min_value=256, max_value=4096, value=2048, step=128, key="chat_max_tok")

    st.divider()

    # Load messages for the current conversation
    conv_id = st.session_state.active_conversation_id
    messages = get_conversation_messages(conv_id)

    # Render previous messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            if msg.get("reasoning"):
                with st.expander("🧠 View Chain of Thought"):
                    st.markdown(msg["reasoning"])
            st.markdown(msg["content"])
            if msg.get("image_path"):
                st.image(msg["image_path"], use_container_width=True)

    # Chat Input Box
    user_prompt = st.chat_input("Type your message or question here...")
    if user_prompt:
        # Display and save user message
        with st.chat_message("user"):
            st.markdown(user_prompt)
        add_message(conv_id, role="user", content=user_prompt)

        # Build message history for provider context
        history = get_conversation_messages(conv_id)
        api_messages = [{"role": m["role"], "content": m["content"]} for m in history]

        # Assistant response with streaming
        with st.chat_message("assistant"):
            stream_gen = stream_chat_response(
                conversation_id=conv_id,
                provider_name=provider_name,
                model=selected_model,
                messages=api_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt
            )
            response_text = st.write_stream(stream_gen)

        st.rerun()

    # Bottom Actions: Export & Delete
    if messages:
        st.markdown("<br>", unsafe_allow_html=True)
        exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 4])
        with exp_col1:
            # Markdown export
            md_content = f"# Chat Export: Session #{conv_id}\n\n"
            for m in messages:
                md_content += f"### {m['role'].upper()}:\n{m['content']}\n\n"
            st.download_button(
                "📥 Export (.md)",
                data=md_content,
                file_name=f"chat_session_{conv_id}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with exp_col2:
            # JSON export
            json_content = json.dumps(messages, indent=2)
            st.download_button(
                "📥 Export (.json)",
                data=json_content,
                file_name=f"chat_session_{conv_id}.json",
                mime="application/json",
                use_container_width=True
            )
