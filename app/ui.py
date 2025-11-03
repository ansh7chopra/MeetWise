import streamlit as st
from app.transcription import transcribe_audio
from app.utils import query_llm

st.set_page_config(page_title="MeetWise AI", layout="wide")

def apply_style():
    st.markdown(
        """
        <style>
        /* Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #e8f3ff 0%, #ffffff 100%);
        }

        /* Title */
        h1 {
            text-align: center;
            font-weight: 800 !important;
            color: #1a3c66 !important;
        }

        /* Upload box */
        .stFileUploader {
            border: 2px dashed #639bff !important;
            padding: 15px;
            border-radius: 12px;
            background: rgba(255,255,255,0.7);
        }

        /* Buttons */
        .stButton > button {
            background: #4b8ae6;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            transition: 0.2s ease;
            width: 100%;
        }
        .stButton > button:hover {
            background: #3a7bd5;
            transform: translateY(-2px);
        }

        /* Input box */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #4b8ae6;
        }

        /* Make content centered and wide */
        .block-container {
            max-width: 900px;
            padding-top: 20px;
            margin: auto;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 14px;
            padding: 12px;
            opacity: 0.9;
            font-weight: 500;
            color: #1a3c66;
        }

        .footer a {
            text-decoration: none;
            color: inherit; /* Keep same color */
            font-weight: 700;
        }

        .footer a:hover {
            text-decoration: underline;
        }
        </style>

        <div class="footer">
            Made by <a href="https://www.linkedin.com/in/ansh-chopra-a73174235?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank">Ansh</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    apply_style()

    st.title("MeetWise — AI Meeting Assistant")

    col1, col2 = st.columns([1.3, 1])

    if "transcript" not in st.session_state:
        st.session_state.transcript = ""
    if "response" not in st.session_state:
        st.session_state.response = ""

    # -------- LEFT PANEL --------
    with col1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("🎧 Upload & Transcribe")

        audio = st.file_uploader("Upload audio (mp3/wav/m4a)", type=["mp3", "wav", "m4a"])

        if audio and st.button("Transcribe Audio 📝"):
            with st.spinner("Transcribing..."):
                st.session_state.transcript = transcribe_audio(audio)
            st.success("✅ Transcription Complete")

        st.text_area("Transcript", value=st.session_state.transcript, height=300)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- RIGHT PANEL --------
    with col2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.subheader("🤖 Ask MeetWise")

        # Summary Button
        if st.button("✨ Get Summary"):
            if st.session_state.transcript.strip() == "":
                st.warning("Upload and transcribe audio first.")
            else:
                with st.spinner("Generating summary..."):
                    st.session_state.response = query_llm(st.session_state.transcript, "Summarize this meeting")
                st.success("✅ Summary Ready")

        # Custom prompt input
        prompt = st.text_input("Enter custom prompt")

        if st.button("Generate Response"):
            if st.session_state.transcript.strip() == "":
                st.warning("Upload and transcribe audio first.")
            elif prompt.strip() == "":
                st.warning("Enter a prompt.")
            else:
                with st.spinner("Generating response..."):
                    st.session_state.response = query_llm(
                        st.session_state.transcript, prompt
                    )
                st.success("✅ Done")

        st.text_area("MeetWise Output", value=st.session_state.response, height=300)

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()


# streamlit run run.py