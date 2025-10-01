from fastapi import FastAPI
from app.model import score_transaction

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.post("/score")
def score(data: dict):
    result = score_transaction(data)
    return {"risk_score": result}
