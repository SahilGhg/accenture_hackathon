import ollama

def estimate_resolution_time(chat):
    prompt = f"""
Estimate how long it would take to resolve this issue.

Chat:
{chat}

Output format: <e.g., 2 days, 1 hour>
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
