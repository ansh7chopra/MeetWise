import streamlit as st
from app.transcription import transcribe_audio
from app.utils import query_llm

def main():
    st.set_page_config(page_title="MeetWise - AI Meeting Assistant")
    st.title("🎙️ MeetWise - AI Meeting Summarizer")

    audio_file = st.file_uploader("Upload your meeting audio file", type=["mp3", "wav", "m4a"])

    # Diarization toggle
    diarize = st.checkbox("Enable Speaker Diarization (Experimental)", value=False)

    preset_prompts = {
        "📝 Get Summary": "Summarize this meeting.",
        "📌 Key Points": "Extract key discussion points from the meeting.",
        "✅ Action Items": "List action items discussed in this meeting.",
    }

    selected_prompt = ""

    if audio_file:
        st.success("Audio file uploaded!")

        st.subheader("Select a prompt or enter your own:")
        col1, col2, col3 = st.columns(3)
        if col1.button("📝 Get Summary"):
            selected_prompt = preset_prompts["📝 Get Summary"]
        if col2.button("📌 Key Points"):
            selected_prompt = preset_prompts["📌 Key Points"]
        if col3.button("✅ Action Items"):
            selected_prompt = preset_prompts["✅ Action Items"]

        custom_prompt = st.text_input("Or enter a custom prompt:")
        if custom_prompt:
            selected_prompt = custom_prompt

        if selected_prompt:
            with st.spinner("Transcribing audio..."):
                transcript = transcribe_audio(audio_file, diarize=diarize)

            with st.spinner("Generating response from LLM..."):
                response = query_llm(transcript, selected_prompt)

            st.subheader("🗒️ Transcript")
            st.text_area("Transcription", value=transcript, height=300)

            st.subheader("🤖 LLM Response")
            st.text_area("Result", value=response, height=300)

# streamlit run run.py