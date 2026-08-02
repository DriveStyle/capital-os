from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..schemas.portfolio import PortfolioCreate, PortfolioResponse
from ..schemas.asset import AssetCreate, AssetResponse
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(portfolio_in: PortfolioCreate, db: Session = Depends(get_db)):
    return PortfolioService.create_portfolio(db, portfolio_in)


@router.get("/user/{user_id}", response_model=List[PortfolioResponse])
def list_user_portfolios(user_id: UUID, db: Session = Depends(get_db)):
    return PortfolioService.list_portfolios_by_user(db, user_id)


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: UUID, db: Session = Depends(get_db)):
    p = PortfolioService.get_portfolio(db, portfolio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return p


@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def add_asset(asset_in: AssetCreate, db: Session = Depends(get_db)):
    p = PortfolioService.get_portfolio(db, asset_in.portfolio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return PortfolioService.add_asset(db, asset_in)


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def add_transaction(tx_in: TransactionCreate, db: Session = Depends(get_db)):
    p = PortfolioService.get_portfolio(db, tx_in.portfolio_id)
    if not p:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return PortfolioService.add_transaction(db, tx_in)
