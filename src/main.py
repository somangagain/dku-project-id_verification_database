from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, PositiveInt

app = FastAPI()

@app.get("/")
async def rootGet():
    return "Hello World!"