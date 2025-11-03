import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv  
load_dotenv() 

def get_file_display_name(file_path: str) -> str:
    return os.path.basename(file_path).split(".")[0]

def timestamped_filename(base: str, ext: str = "txt") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}.{ext}"

def is_audio_file(filename: str) -> bool:
    audio_extensions = [".mp3", ".wav", ".m4a", ".mp4", ".webm"]
    return any(filename.lower().endswith(ext) for ext in audio_extensions)

def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# === Groq LLM Function ===
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_llm(transcript: str, prompt: str) -> str:
    full_prompt = f"""You are a helpful meeting assistant.

{prompt}

 meeting transcript:
{transcript}
"""
    print("=== DEBUG: Sending to LLM ===")
    print(full_prompt)
    print("=============================")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.choices[0].message.content.strip()
