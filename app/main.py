from fastapi import FastAPI
from pydantic import BaseModel
from app.model import score_transaction

app = FastAPI()

class Transaction(BaseModel):
    amount: float
    timestamp: str
    location: str
    source_account: str
    destination_account: str

@app.post("/score")
def score(tx: Transaction):
    result = score_transaction(tx.dict())
    return {"risk_score": result}
