import os
import base64
from groq import Groq

def transcribe_audio(audio_file, diarize=False):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Read file
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    response = client.audio.transcriptions.create(
        file=(audio_file.name, audio_bytes),
        model="whisper-large-v3",
        response_format="text"
    )

    transcript = response.strip()

    if not transcript or transcript.lower() == "none":
        return "Could not generate transcription. Try a longer or clearer audio."

    return transcript
