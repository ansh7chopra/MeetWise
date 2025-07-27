import os
import streamlit as st
# This tells Streamlit to run the UI from app/ui.py
from app import ui

if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # To suppress tokenizer warnings
    st.set_page_config(page_title="MeetWise - AI Meeting Summarizer", page_icon="🎙️")
    ui.main()

