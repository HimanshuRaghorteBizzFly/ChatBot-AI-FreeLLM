"""
Vision Studio View.
Multimodal image analysis, OCR text extraction, and scene interpretation via Google Gemini Vision.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.services.vision import analyze_vision_image

def render():
    render_navbar("👁️ AI Vision Studio", "Multimodal Image Understanding, OCR, Scene Reasoning & Q&A")

    col_upload, col_result = st.columns([1.3, 1.7])

    with col_upload:
        st.markdown("### 📷 Upload Visual Media")
        uploaded_file = st.file_uploader(
            "Upload Image (PNG, JPG, WEBP)",
            type=["png", "jpg", "jpeg", "webp"],
            key="vision_uploader"
        )

        model = st.selectbox(
            "Vision Engine",
            options=["gemini-3.1-flash-lite", "gemini-3.8-flash"],
            index=0,
            key="vision_model_select"
        )

        prompt = st.text_area(
            "Question / Instructions",
            value="Describe this image in detail. Extract any visible text or code, identify key objects and layout patterns, and summarize its primary contents.",
            height=120,
            key="vision_prompt_input"
        )

        if uploaded_file:
            st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

        analyze_clicked = st.button("🔍 Analyze Image", type="primary", use_container_width=True, key="btn_run_vision")

    with col_result:
        st.markdown("### 💡 Multimodal Analysis Output")
        if analyze_clicked:
            if not uploaded_file:
                st.warning("Please upload an image first.")
            else:
                with st.spinner("Processing visual features with Gemini Vision..."):
                    img_bytes = uploaded_file.getvalue()
                    mime_type = uploaded_file.type or "image/jpeg"
                    analysis = analyze_vision_image(
                        image_bytes=img_bytes,
                        prompt=prompt,
                        model=model,
                        mime_type=mime_type
                    )
                    st.markdown(analysis)
                    st.download_button(
                        "📥 Download Analysis (.txt)",
                        data=analysis,
                        file_name=f"vision_analysis_{uploaded_file.name}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        else:
            st.info("💡 Upload an image and click **Analyze Image** to see multimodal reasoning here.")
