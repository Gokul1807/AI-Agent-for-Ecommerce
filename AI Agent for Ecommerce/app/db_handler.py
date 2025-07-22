# app/db_handler.py

import sqlite3

DB_PATH = "ecommerce.db"

def execute_query(query: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        conn.close()
        return {"columns": columns, "rows": results}
    except Exception as e:
        conn.close()
        return {"error": str(e)}
