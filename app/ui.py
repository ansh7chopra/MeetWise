import streamlit as st
from app.transcription import transcribe_audio
from app.utils import query_llm

st.set_page_config(page_title="MeetWise AI", layout="wide")

def apply_style():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #e8eaf6);
        color: #1a1a1a;
    }

    .block-container {
        max-width: 95% !important;
        padding-top: 2rem;
    }

    .glass-box {
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(200,200,200,0.4);
        backdrop-filter: blur(8px);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }

    h1, h2, h3, label, .stTextInput > label, .stFileUploader > label {
        color: #0f172a !important;
        font-weight: 600;
    }

    div.stButton > button {
        width: 100%;
        padding: 10px;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        background: #4f46e5;
        color: white;
        transition: 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        background: #4338ca;
    }

    textarea, .stTextInput input {
        background: rgba(255,255,255,0.9) !important;
        color: #000 !important;
        border-radius: 8px !important;
        border: 1px solid rgba(150,150,150,0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)


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