from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__),"expense.db")
mcp = FastMCP("Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                  CREATE TABLE IF NOT EXISTS expenses(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      amount REAL NOT NULL,
                      category TEXT NOT NULL,
                      subcategory TEXT DEFAULT '',
                      note TEXT DEFAULT '',
                  )
             """)
        
init_db()

@mcp.tool
def add_expense(date,amount,category,subcategory="",note=""):
    '''Add new expense to the databse'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES (?,?,?,?,?)",
            (date,amount,category,subcategory,note)
        )
        return {'status':"ok","id":cur.lastrowid}
    
@mcp.tool
def list_expense(start_date,end_date):
    with sqlite3.connect(DB_PATH) as c:
        '''List all expense entries from the databse'''
        cur=c.execute("""
                      SELECT id,date,amount,category,subcategory,note FROM expense ORDER BY id ASC
                      """,
                      (start_date,end_date)
                      )
        cols=[d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]
    
if __name__ == "__main__":
    mcp.run()