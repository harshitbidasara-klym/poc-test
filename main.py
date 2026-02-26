from fastapi import FastAPI, Request
import psycopg2
import os

app = FastAPI()

DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_NAME=os.getenv("DB_NAME")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

@app.get("/hello")
def hello():
    return {"message": "hello world"}

@app.get("/users")
def users():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        cur.close()
        return {"data": rows}
    finally:
        conn.close() # CRITICAL: Close the connection so it doesn't leak!

@app.get("/xss")
async def xss(q:str):
    return {"response": q}
