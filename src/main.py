from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, PositiveInt

from mysql.connector import Error
from lib.database.db import create_connection, select_query, execute_query, close_connection

app = FastAPI()

class Sample(BaseModel):
    id: PositiveInt
    url: str
    data: str

@app.get("/")
async def rootGet():
    return "Welcome"

@app.get("/sample")
async def sampleGet():
    try:
        connection = create_connection()
        res = select_query(connection, "SELECT * FROM sample")
        close_connection(connection)
        
        if res is not None: return [o for o in res] 
        else: return []
    except Error as e:
        print(f"main sampleGet Error: {e}")