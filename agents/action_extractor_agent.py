import ollama

def extract_action(chat):
    prompt = f"""
Read the support conversation and extract the main action taken or needed.

Chat:
{chat}

Output format: <action here>
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
