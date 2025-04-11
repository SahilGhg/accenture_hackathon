# agents/predict_category_agent.py

import ollama

def predict_category(chat):
    prompt = f"""
Based on the following support chat, predict the issue category.

Available Categories:
- Software Installation Failure
- Network Connectivity Issue
- Device Compatibility Error
- Account Synchronization Bug
- Payment Gateway Integration Failure

Chat:
{chat}

Output format: <one of the categories>
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]
