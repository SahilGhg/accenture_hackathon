import ollama

def route_ticket(chat):
    prompt = f"""
Which team should handle this issue?

Options: Technical Support, Billing, Account Management

Chat:
{chat}

Output format: <team name>
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
