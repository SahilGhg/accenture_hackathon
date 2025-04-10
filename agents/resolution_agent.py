import ollama
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# 1. Extract keywords from chat using TF-IDF
def extract_keywords(text, top_n=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = tfidf_matrix.toarray()[0]
    feature_names = vectorizer.get_feature_names_out()
    top_indices = scores.argsort()[-top_n:][::-1]
    keywords = [feature_names[i] for i in top_indices]
    return keywords

# 2. Recommend resolution using historical DB
def recommend_resolution_from_db(chat):
    db_path = os.path.join("data", "tickets.db")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    keywords = extract_keywords(chat)

    for keyword in keywords:
        query = f"""
        SELECT Solution FROM historical_tickets
        WHERE LOWER("Issue Category") LIKE '%{keyword}%'
        ORDER BY "Date Of Resolution" DESC
        LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0], keyword  # Return Solution from DB

    conn.close()
    return None, ", ".join(keywords)

# 3. Full function with fallback to AI if no DB match
def recommend_resolution(chat):
    similar_resolution, keyword_info = recommend_resolution_from_db(chat)
    if similar_resolution:
        return f"Recommended Resolution - {similar_resolution}", "DB", keyword_info

    prompt = f"""
Based on the support chat, suggest a helpful resolution in 1–2 lines.

Chat:
{chat}

Output format: <your suggestion>
"""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    resolution_text = response["message"]["content"]

    return f"{resolution_text} (Source: AI)", "AI", []
