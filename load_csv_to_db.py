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
