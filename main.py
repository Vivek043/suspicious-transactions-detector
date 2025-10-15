from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/score")
async def score_transactions(payload: List[Dict]):
    df = pd.DataFrame(payload)

    # Dummy scoring logic
    df["xgb_score"] = 0.7
    df["xgb_flag"] = 1
    df["iso_flag"] = 0
    df["final_flag"] = 1
    df["reason"] = "High XGBoost score"

    df.fillna("missing", inplace=True)

    return df.to_dict(orient="records")
