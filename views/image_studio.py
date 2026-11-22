"""
Image Studio View.
Full text-to-image synthesis, aspect ratio controls, negative prompts,
direct local rendering to prevent broken icons, and media gallery.
"""
import os
import streamlit as st
from components.navbar import render_navbar
from backend.services.images import generate_image_studio
from backend.repositories.storage import list_generated_media

def render():
    render_navbar("🎨 AI Image Studio", "High-Resolution Diffusion Synthesis with Microsoft MAI & FLUX Engines")

    c1, c2 = st.columns([1.8, 1.2])

    with c1:
        st.markdown("### 🪄 Create Visual Artwork")
        prompt = st.text_area(
            "Image Prompt",
            placeholder="A cinematic futuristic Tokyo street in heavy rain with neon reflections, hyper-detailed 8k resolution, volumetric fog...",
            height=120,
            key="img_studio_prompt"
        )

        with st.expander("🛠️ Advanced Settings & Negative Prompt", expanded=False):
            negative_prompt = st.text_input(
                "Negative Prompt",
                placeholder="blurry, distorted, ugly, low quality, artifacts, watermark",
                key="img_studio_neg"
            )
            col_ar, col_mod = st.columns(2)
            with col_ar:
                aspect_ratio = st.selectbox(
                    "Aspect Ratio",
                    options=["1:1 (Square)", "16:9 (Landscape)", "9:16 (Portrait)", "4:3 (Standard)"],
                    index=0,
                    key="img_studio_ar"
                )
            with col_mod:
                model = st.selectbox(
                    "Model Engine",
                    options=[
                        "microsoft/mai-image-2.7-flash",
                        "black-forest-labs/flux-1-schnell",
                        "stabilityai/sdxl-turbo"
                    ],
                    index=0,
                    key="img_studio_model"
                )

        clean_ar = aspect_ratio.split()[0]
        generate_clicked = st.button("🚀 Generate Visual Artwork", type="primary", use_container_width=True, key="btn_gen_img")

    with c2:
        st.markdown("### 🖼️ Live Studio Preview")
        if generate_clicked:
            if not prompt.strip():
                st.warning("Please enter an image prompt first.")
            else:
                with st.spinner("✨ Synthesizing pixels and downloading high-res binary..."):
                    result = generate_image_studio(
                        prompt=prompt,
                        model=model,
                        aspect_ratio=clean_ar
                    )
                    local_path = result.get("path")
                    if local_path and os.path.exists(local_path):
                        st.image(local_path, caption=f"Prompt: {prompt}", use_container_width=True)
                        st.success(result.get("notice", "Image generated successfully!"))
                        
                        try:
                            with open(local_path, "rb") as f:
                                st.download_button(
                                    "📥 Download Artwork (High-Res)",
                                    data=f.read(),
                                    file_name=os.path.basename(local_path),
                                    mime="image/jpeg",
                                    use_container_width=True,
                                    key="dl_live_studio_img"
                                )
                        except Exception:
                            pass
                    else:
                        st.error(result.get("notice", "Failed to render image."))
        else:
            st.info("💡 Enter your prompt on the left and click **Generate** to render your image here.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Past Media Gallery
    st.markdown("### 🗂️ Studio Generation History")
    past_images = list_generated_media(media_type="image", limit=12)

    if past_images:
        g_cols = st.columns(3)
        for idx, item in enumerate(past_images):
            with g_cols[idx % 3]:
                file_path = item.get("file_path")
                if file_path and os.path.exists(file_path):
                    st.image(file_path, caption=item.get("prompt", "")[:60], use_container_width=True)
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                f"📥 Download #{item['id']}",
                                data=f.read(),
                                file_name=os.path.basename(file_path),
                                mime="image/jpeg",
                                use_container_width=True,
                                key=f"dl_gal_{item['id']}"
                            )
                    except Exception:
                        pass
                    st.caption(f"Engine: {item.get('model')} • {item.get('created_at', '')}")
    else:
        st.caption("No previously generated media in storage. Create your first image above!")
