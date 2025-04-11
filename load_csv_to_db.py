import pandas as pd
import sqlite3
import os

# Load CSV
csv_path = os.path.join("data", "Historical_ticket_data.csv")
df = pd.read_csv(csv_path)

# Connect to (new) DB
db_path = os.path.join("data", "tickets.db")
conn = sqlite3.connect(db_path)

# Store DataFrame to SQL
df.to_sql("historical_tickets", conn, if_exists="replace", index=False)

conn.close()
print("✅ New tickets.db created with historical_tickets table")

import sqlite3

conn = sqlite3.connect("data/tickets.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT,
    rating INTEGER,
    comments TEXT
)
""")

conn.commit()
conn.close()
print("✅ Feedback table created.")
