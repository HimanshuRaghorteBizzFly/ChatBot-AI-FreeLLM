"""
Plans & Billing View.
Displays the 100% Free Community Edition tier and transparent model quotas.
"""
import streamlit as st
from components.navbar import render_navbar

def render():
    render_navbar("Billing")

    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0 2rem 0;">
            <span style="background: #EFF6FF; color: #2563EB; font-weight: 700; font-size: 0.85rem; padding: 0.3rem 0.85rem; border-radius: 9999px; border: 1px solid #BFDBFE;">
                ✨ 100% Free & Open AI Studio
            </span>
            <h1 style="font-size: 2.4rem; font-weight: 800; color: #0F172A; margin: 0.8rem 0 0.4rem 0;">
                Transparent, Open-Source & <span style="background: linear-gradient(135deg, #2563EB, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Zero-Cost Forever</span>
            </h1>
            <p style="color: #64748B; font-size: 1.05rem; max-width: 620px; margin: 0 auto;">
                Enjoy unlimited access to frontier LLMs, high-resolution diffusion imaging, and neural audio without paywalls or hidden subscriptions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 2px solid #2563EB; border-radius: 16px; padding: 2rem; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.1); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.35rem; font-weight: 800; color: #0F172A;">Community Free Edition</span>
                        <span class="badge-free">Active Forever</span>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #0F172A; margin-bottom: 0.5rem;">
                        $0 <span style="font-size: 1rem; color: #64748B; font-weight: 500;">/ month</span>
                    </div>
                    <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 1.5rem;">
                        Everything you need for full-stack AI development, vision analytics, and generative art.
                    </p>
                    <hr style="border: none; border-top: 1px solid #E2E8F0; margin-bottom: 1.5rem;">
                    <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.92rem; color: #334155;">
                        <li style="margin-bottom: 0.75rem;">✅ <b>120+ AI Models</b> (OpenRouter, Gemini, Groq, Free AI, Ollama)</li>
                        <li style="margin-bottom: 0.75rem;">✅ <b>High-Speed Image Studio</b> with local disk rendering & downloads</li>
                        <li style="margin-bottom: 0.75rem;">✅ <b>Whisper Large V3 Speech-to-Text</b> & Multi-Voice TTS</li>
                        <li style="margin-bottom: 0.75rem;">✅ <b>Gemini Vision Q&A</b> and scene multimodal extraction</li>
                        <li style="margin-bottom: 0.75rem;">✅ <b>Dense Vector Embeddings</b> & Semantic Document Reranking</li>
                        <li style="margin-bottom: 0.75rem;">✅ <b>Zero Credit Card Required</b> & No Paywalls</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.button("✅ Current Active Plan", key="btn_free_plan_active", use_container_width=True, disabled=True)

    with col2:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1E1B4B 0%, #2563EB 50%, #4F46E5 100%); border-radius: 16px; padding: 2rem; color: #FFFFFF; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF;">Pro Community Pass</span>
                        <span style="background: rgba(255,255,255,0.2); color: #FFFFFF; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">100% Unlocked</span>
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.5rem;">
                        $0 <span style="font-size: 1rem; color: #C7D2FE; font-weight: 500;">/ complimentary</span>
                    </div>
                    <p style="color: #E0E7FF; font-size: 0.9rem; margin-bottom: 1.5rem;">
                        Enterprise-tier concurrency, priority API keys, and custom model endpoints.
                    </p>
                    <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin-bottom: 1.5rem;">
                    <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.92rem; color: #EEF2FF;">
                        <li style="margin-bottom: 0.75rem;">👑 <b>All Pro Models Unlocked</b> (Nemotron, Claude, GPT-4o, Groq)</li>
                        <li style="margin-bottom: 0.75rem;">👑 <b>Custom API Key Bring-Your-Own-Key</b> support</li>
                        <li style="margin-bottom: 0.75rem;">👑 <b>Local Offline Storage</b> with SQLite database auditing</li>
                        <li style="margin-bottom: 0.75rem;">👑 <b>Unlimited Prompt Library</b> & CSV Usage Export</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚀 Explore All Models", key="btn_explore_from_bill", use_container_width=True, type="primary"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
