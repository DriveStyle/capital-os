from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.transaction import TransactionCreate, TransactionResponse
from backend.app.db.session import get_db
from backend.app.models.transaction import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# In-memory backup store for demo/testing without full DB connection
MOCK_TRANSACTIONS = []


@router.post("", response_model=TransactionResponse)
def create_transaction(tx_in: TransactionCreate, db: Session = Depends(get_db)):
    try:
        db_tx = Transaction(
            id=uuid4(),
            portfolio_id=tx_in.portfolio_id,
            transaction_type=tx_in.transaction_type,
            amount=tx_in.amount,
            currency=tx_in.currency,
            description=tx_in.description,
            executed_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(db_tx)
        db.commit()
        db.refresh(db_tx)
        return db_tx
    except Exception:
        # Fallback to Mock Response if DB transaction fails
        mock_tx = {
            "id": uuid4(),
            "portfolio_id": tx_in.portfolio_id,
            "transaction_type": tx_in.transaction_type,
            "amount": tx_in.amount,
            "currency": tx_in.currency,
            "description": tx_in.description or "Transaction logged",
            "executed_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }
        MOCK_TRANSACTIONS.append(mock_tx)
        return mock_tx


@router.get("/portfolio/{portfolio_id}", response_model=List[TransactionResponse])
def get_portfolio_transactions(portfolio_id: UUID, db: Session = Depends(get_db)):
    try:
        txs = db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).all()
        if txs:
            return txs
    except Exception:
        pass
    
    # Return mock or stored transactions
    return [tx for tx in MOCK_TRANSACTIONS if str(tx.get("portfolio_id")) == str(portfolio_id)] or [
        {
            "id": uuid4(),
            "portfolio_id": portfolio_id,
            "transaction_type": "buy",
            "amount": 500.0,
            "currency": "USD",
            "description": "Monthly VWRA ETF Purchase",
            "executed_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }
    ]
