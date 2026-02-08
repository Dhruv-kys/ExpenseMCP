from fastmcp import FastMCP
import os
import sqlite3

mcp = FastMCP("Expense Tracker")

DB_PATH = "/data/expense.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool
def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    """Add a new expense to the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool
def list_expense(start_date: str, end_date: str):
    """List all expenses between two dates"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC, id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool
def summarize(start_date: str, end_date: str, category: str | None = None):
    """Summarize expenses by category within a date range"""
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

if __name__ == "__main__":
    mcp.run()