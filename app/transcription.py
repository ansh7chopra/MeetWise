import os
import tempfile
import torch
import whisperx
from dotenv import load_dotenv
load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisperx.load_model("base", device, compute_type="int8")

def transcribe_audio(file, diarize=False):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(file.read())
        audio_path = tmp.name

    # Step 1: Transcribe
    result = model.transcribe(audio_path)
    segments = result["segments"]
    full_text = " ".join([seg["text"].strip() for seg in segments])

    # Step 2: Diarization (optional)
    if diarize:
        align_model = whisperx.AlignmentModel(
            language_code=result.get("language", "en"),
            device=device
        )

        segments_aligned = align_model.align(segments, audio_path)

        diarize_model = whisperx.DiarizationPipeline(
            use_auth_token=os.getenv("HF_TOKEN"),
            device=device
        )

        diarize_segments = diarize_model(audio_path)

        diarized = whisperx.align_with_diarization(segments_aligned, diarize_segments)["segments"]

        transcript = ""
        for seg in diarized:
            speaker = seg.get("speaker", "Unknown")
            text = seg.get("text", "")
            transcript += f"[{speaker}] {text.strip()}\n"
    else:
        transcript = full_text
