# sar_generator.py

from datetime import datetime

def generate_sar(transaction_id, txn_data, risk_score, reasons):
    sar = {
        "report_id": f"SAR-{transaction_id}",
        "transaction_id": transaction_id,
        "timestamp": datetime.now().isoformat(),
        "amount": txn_data["amount"],
        "location": txn_data["location"],
        "source_account": txn_data["source_account"],
        "destination_account": txn_data["destination_account"],
        "risk_score": risk_score,
        "reasons": reasons,
        "status": "Pending Review"
    }
    return sar
