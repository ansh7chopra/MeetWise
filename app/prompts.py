# app/prompts.py

PREDEFINED_PROMPTS = {
    "Summary": "Give a concise summary of the meeting.",
    "Action Items": "List all the action items discussed in the meeting.",
    "Key Points": "Extract the key points and decisions made in the meeting.",
    "Questions Raised": "List any questions raised during the meeting.",
    "Next Steps": "What are the next steps decided in the meeting?"
}

def get_prompt(option: str, custom_prompt: str = "") -> str:
    """
    Returns the final prompt to send to the LLM.
    If a predefined option is selected, return its prompt.
    If custom_prompt is provided, return that instead.
    """
    if custom_prompt.strip():
        return custom_prompt.strip()

    return PREDEFINED_PROMPTS.get(option, "")
