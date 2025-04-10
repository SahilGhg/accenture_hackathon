import ollama

def recommend_resolution(chat):
    prompt = f"""
Based on the support chat, suggest a helpful resolution in 1–2 lines.

Chat:
{chat}

Output format: Recommended Resolution - <your suggestion>
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
