from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.portfolio import Portfolio
from ..models.asset import Asset
from ..models.transaction import Transaction
from ..schemas.portfolio import PortfolioCreate, PortfolioUpdate
from ..schemas.asset import AssetCreate
from ..schemas.transaction import TransactionCreate


class PortfolioService:
    @staticmethod
    def create_portfolio(db: Session, portfolio_in: PortfolioCreate) -> Portfolio:
        portfolio = Portfolio(
            name=portfolio_in.name,
            description=portfolio_in.description,
            owner_id=portfolio_in.owner_id,
            total_value=Decimal("0.00"),
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        return portfolio

    @staticmethod
    def get_portfolio(db: Session, portfolio_id: UUID) -> Optional[Portfolio]:
        return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    @staticmethod
    def list_portfolios_by_user(db: Session, user_id: UUID) -> List[Portfolio]:
        return db.query(Portfolio).filter(Portfolio.owner_id == user_id).all()

    @staticmethod
    def add_asset(db: Session, asset_in: AssetCreate) -> Asset:
        asset = Asset(
            symbol=asset_in.symbol,
            asset_type=asset_in.asset_type,
            quantity=asset_in.quantity,
            cost_basis=asset_in.cost_basis,
            current_value=asset_in.current_value,
            notes=asset_in.notes,
            portfolio_id=asset_in.portfolio_id,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        PortfolioService.recalculate_total_value(db, asset_in.portfolio_id)
        return asset

    @staticmethod
    def add_transaction(db: Session, tx_in: TransactionCreate) -> Transaction:
        tx = Transaction(
            transaction_type=tx_in.transaction_type,
            amount=tx_in.amount,
            currency=tx_in.currency,
            description=tx_in.description,
            portfolio_id=tx_in.portfolio_id,
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx

    @staticmethod
    def recalculate_total_value(db: Session, portfolio_id: UUID) -> Decimal:
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            return Decimal("0.00")
        assets = db.query(Asset).filter(Asset.portfolio_id == portfolio_id).all()
        total = sum((a.current_value for a in assets if a.current_value is not None), Decimal("0.00"))
        portfolio.total_value = total
        db.commit()
        db.refresh(portfolio)
        return total
