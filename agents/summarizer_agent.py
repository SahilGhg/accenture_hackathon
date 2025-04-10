import ollama

def summarize_chat(chat):
    prompt = f"Summarize the following customer support chat in 2 lines:\n\n{chat}"
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
