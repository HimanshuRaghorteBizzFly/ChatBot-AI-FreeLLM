"""
Dashboard / All-in-One Hub View.
Matches LLM Studio Pro reference layout without any raw HTML/JSON code blocks,
with responsive cards, native progress bars, and full dark/light mode support.
"""
import streamlit as st
from components.navbar import render_navbar
from components.model_card import render_model_card
from backend.services.catalog import filter_catalog
from backend.repositories.storage import get_usage_summary

def render():
    # 1. Top Navbar
    render_navbar("Models")

    # 2. Main Two-Column Layout (Center Hub + Right Panel)
    col_main, col_right = st.columns([2.8, 1.1])

    with col_main:
        # --- Hero Banner with 3D Floating Brand Stage (Zero Indent to prevent Markdown Code Blocks) ---
        hero_html = """<div class="hero-hub-container">
<div class="hero-text-block">
<h1>All-in-One <span>LLM Studio</span></h1>
<p>Access 100+ AI models from OpenRouter, GitHub, and top providers — for Chat, Image, Video, and Speech in one place.</p>
</div>
<div class="hero-floating-stage">
<div class="floating-brand-badge" title="OpenAI">⚡</div>
<div class="floating-brand-badge" style="transform: translateY(-10px);" title="Google Gemini">✨</div>
<div class="floating-brand-badge" style="transform: translateY(-4px);" title="Meta Llama">🦙</div>
<div class="floating-brand-badge" style="transform: translateY(-14px);" title="Anthropic">🧠</div>
<div class="floating-brand-badge" title="Groq">⚡</div>
</div>
</div>"""
        st.markdown(hero_html, unsafe_allow_html=True)

        # --- Big Search Input ---
        search_query = st.text_input(
            "Hub Search",
            placeholder="🔍 Search models, e.g. \"GPT-4o\", \"Gemini\", \"Flux\", \"Claude\"... (Ctrl K)",
            label_visibility="collapsed",
            key="hub_search_input"
        )

        # --- Category Pills Row ---
        if "hub_category" not in st.session_state:
            st.session_state.hub_category = "All"

        pills = [
            ("All Models (120+)", "All"),
            ("Text & Chat (45+)", "Text"),
            ("Image (18+)", "Image"),
            ("Video (12+)", "Video"),
            ("Speech (10+)", "Speech"),
            ("Reasoning (15+)", "Reasoning"),
            ("Embeddings (8+)", "Embeddings")
        ]

        p_cols = st.columns(len(pills))
        for idx, (label, cat_val) in enumerate(pills):
            with p_cols[idx]:
                is_active = (st.session_state.hub_category == cat_val)
                btn_type = "primary" if is_active else "secondary"
                if st.button(label, key=f"cat_btn_{cat_val}", use_container_width=True, type=btn_type):
                    st.session_state.hub_category = cat_val
                    st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # --- Popular Providers Section ---
        st.markdown("<div style='font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem;'>Popular Providers</div>", unsafe_allow_html=True)
        
        if "hub_provider" not in st.session_state:
            st.session_state.hub_provider = "All"

        providers = [
            ("🌐 OpenRouter", "OpenRouter"),
            ("⚡ OpenAI", "OpenAI"),
            ("✨ Google Gemini", "Google"),
            ("🧠 Anthropic", "Anthropic"),
            ("⚡ Groq", "Groq"),
            ("🟢 NVIDIA", "NVIDIA"),
            ("🦙 Meta Llama", "Meta"),
            ("All Providers", "All")
        ]

        pr_cols = st.columns(len(providers))
        for idx, (p_label, p_val) in enumerate(providers):
            with pr_cols[idx]:
                is_sel = (st.session_state.hub_provider == p_val)
                btn_style = "primary" if is_sel else "secondary"
                if st.button(p_label, key=f"prov_btn_{p_val}", use_container_width=True, type=btn_style):
                    st.session_state.hub_provider = p_val
                    st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # --- Explore Models Section ---
        ex_col1, ex_col2, ex_col3 = st.columns([2, 1.2, 1])
        with ex_col1:
            st.markdown("<div class='explore-title'>Explore Models (120+ Models)</div>", unsafe_allow_html=True)
        with ex_col2:
            filter_choice = st.radio(
                "Filter",
                options=["All (120+)", "Free (42)", "Paid (78)"],
                index=0,
                horizontal=True,
                label_visibility="collapsed",
                key="hub_price_radio"
            )
        with ex_col3:
            sort_choice = st.selectbox("Sort", ["Popular", "Context Length", "Name"], label_visibility="collapsed", key="hub_sort_select")

        # Determine filtering
        free_filter = None
        if "Free" in filter_choice:
            free_filter = True
        elif "Paid" in filter_choice:
            free_filter = False

        models = filter_catalog(
            category=st.session_state.hub_category,
            is_free=free_filter,
            search=search_query
        )

        if st.session_state.hub_provider != "All":
            models = [m for m in models if st.session_state.hub_provider.lower() in m.provider.lower()]

        if sort_choice == "Context Length":
            models = sorted(models, key=lambda m: m.context_length or 0, reverse=True)
        elif sort_choice == "Name":
            models = sorted(models, key=lambda m: m.name)

        # Render 4 Columns per row matching reference image
        if models:
            for i in range(0, len(models), 4):
                chunk = models[i:i+4]
                grid_cols = st.columns(4)
                for c_idx, m in enumerate(chunk):
                    with grid_cols[c_idx]:
                        render_model_card(m, on_try_key=f"hub_try_{m.id}_{i}_{c_idx}")
        else:
            st.info("No models match your current filters. Select 'All Models' or reset your search query.")

    # 3. Right Sidebar / Quick Panel
    with col_right:
        # --- Quick Actions (Container with Native Buttons) ---
        with st.container(border=True):
            st.markdown("#### ⚡ Quick Actions")
            actions = [
                ("💬 New Chat", "Talk with any LLM", "Chat Playground"),
                ("🖼️ Generate Image", "Create images from text", "Image Studio"),
                ("🎬 Generate Video", "Text to video", "Video Studio"),
                ("🎙️ Text to Speech", "Synthesize voice", "Speech Studio"),
                ("🎧 Speech to Text", "Transcribe audio", "Speech Studio")
            ]

            for title, sub, target_page in actions:
                if st.button(f"{title} • {sub}", key=f"qa_{title}", use_container_width=True):
                    st.session_state.current_page = target_page
                    st.rerun()

        # --- Your Usage (This Month) (Using Native Streamlit Progress Bars) ---
        with st.container(border=True):
            st.markdown("#### 📊 Your Usage (This Month)")
            usage_data = get_usage_summary()
            tokens_val = min(usage_data.get("total_tokens", 45000), 500000)

            st.write(f"**Text Tokens:** {tokens_val // 1000}K / 500K")
            st.progress(min(1.0, max(0.04, tokens_val / 500000)))

            st.write("**Image Generation:** 12 / 200")
            st.progress(0.06)

            st.write("**Speech (TTS):** 5 / 100")
            st.progress(0.05)
            st.caption("🟢 All Free Tier Quotas Active")

        # --- Upgrade to Pro / Free Forever Card (Zero Indent) ---
        with st.container(border=True):
            pro_card_html = """<div class="pro-banner-card">
<h3 style="margin: 0 0 0.5rem 0; color: #FFFFFF !important; font-size: 1.15rem; font-weight: 800;">👑 Upgrade to Pro</h3>
<div style="font-size: 0.85rem; color: #E0E7FF; line-height: 1.6; margin-bottom: 0.8rem;">
<div>✓ Access premium & latest models</div>
<div>✓ Higher rate limits</div>
<div>✓ Priority processing</div>
<div>✓ Commercial usage rights</div>
</div>
</div>"""
            st.markdown(pro_card_html, unsafe_allow_html=True)
            if st.button("View Plans & Pricing ➔", key="btn_right_view_plans", use_container_width=True, type="primary"):
                st.session_state.current_page = "Plans & Billing"
                st.rerun()
