"""
Speech Studio View.
Text-to-Speech synthesis (gTTS) and Speech-to-Text transcription (Groq Whisper Large V3).
"""
import os
import streamlit as st
from components.navbar import render_navbar
from backend.services.speech import text_to_speech, transcribe_audio

def render():
    render_navbar("🎙️ AI Speech & Audio Studio", "Neural Voice Synthesis & Whisper Large V3 Speech-to-Text Transcription")

    tab_tts, tab_stt = st.tabs(["🔊 Text-to-Speech (TTS)", "🎧 Speech-to-Text (STT Transcription)"])

    # --- 1. Text-to-Speech ---
    with tab_tts:
        t_col1, t_col2 = st.columns([1.6, 1.4])
        with t_col1:
            st.markdown("### 🗣️ Neural Voice Synthesis")
            text_input = st.text_area(
                "Text to Speak",
                placeholder="Welcome to the next generation of artificial intelligence, featuring ultra-fast multimodal inference...",
                height=130,
                key="tts_text_input"
            )
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                lang = st.selectbox(
                    "Language",
                    options=[
                        ("English (US)", "en"),
                        ("Spanish (ES)", "es"),
                        ("French (FR)", "fr"),
                        ("German (DE)", "de"),
                        ("Hindi (IN)", "hi")
                    ],
                    format_func=lambda x: x[0],
                    key="tts_lang_select"
                )
            with p_col2:
                speed = st.selectbox("Speed", options=["Normal", "Slow"], index=0, key="tts_speed_sel")

            if st.button("🎵 Generate Voice Audio", type="primary", use_container_width=True, key="btn_gen_tts"):
                if not text_input.strip():
                    st.warning("Please enter text to synthesize into speech.")
                else:
                    with st.spinner("Synthesizing neural audio waveform..."):
                        audio_res = text_to_speech(
                            text=text_input,
                            lang=lang[1],
                            slow=(speed == "Slow")
                        )
                        audio_path = audio_res.get("path")
                        if audio_path and os.path.exists(audio_path):
                            st.session_state.active_tts_path = audio_path
                            st.success("Voice synthesized successfully!")
                        else:
                            st.error(audio_res.get("notice", "Failed to synthesize speech."))

        with t_col2:
            st.markdown("### 📻 Audio Player & Download")
            active_audio = st.session_state.get("active_tts_path")
            if active_audio and os.path.exists(active_audio):
                with open(active_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        "📥 Download MP3 Audio",
                        data=audio_bytes,
                        file_name=os.path.basename(active_audio),
                        mime="audio/mp3",
                        use_container_width=True
                    )
            else:
                st.info("💡 Type text on the left and click **Generate Voice Audio** to listen here.")

    # --- 2. Speech-to-Text ---
    with tab_stt:
        s_col1, s_col2 = st.columns([1.5, 1.5])
        with s_col1:
            st.markdown("### 🎙️ Audio Transcription")
            uploaded_audio = st.file_uploader(
                "Upload Audio File for Transcription",
                type=["mp3", "wav", "m4a", "ogg"],
                key="stt_file_upload"
            )
            if uploaded_audio:
                st.audio(uploaded_audio)
                if st.button("⚡ Transcribe with Groq Whisper Large V3", type="primary", use_container_width=True, key="btn_transcribe"):
                    with st.spinner("Transcribing speech with microsecond Whisper LPU inference..."):
                        audio_bytes = uploaded_audio.read()
                        result = transcribe_audio(audio_bytes=audio_bytes, filename=uploaded_audio.name)
                        st.session_state.transcription_text = result.get("text", "")

        with s_col2:
            st.markdown("### 📝 Transcription Output")
            transcription = st.session_state.get("transcription_text", "")
            if transcription:
                st.text_area("Extracted Transcript", value=transcription, height=220)
                st.download_button(
                    "📥 Download Transcript (.txt)",
                    data=transcription,
                    file_name="whisper_transcript.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("💡 Upload an audio file and click transcribe to view text output.")
