#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SQLAlchemy ORM models for the database.
"""

from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime, 
                        create_async_engine, ForeignKey)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

from config import config

# Create an async engine instance
engine = create_async_engine(config.DATABASE_URL, echo=False)

# Create a sessionmaker for creating async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

class User(Base):
    """User model to store user information and preferences."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
    is_subscribed = Column(Boolean, default=False)
    threshold_percent = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(telegram_id=\'{self.telegram_id}\')>"

class Card(Base):
    """Card model to store unified card information across platforms."""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    renaiss_id = Column(String, unique=True, nullable=False)
    token_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    listings = relationship("Listing", back_populates="card", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Card(name=\'{self.name}\')>"

class Listing(Base):
    """Listing model to store price information from different markets."""
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    source = Column(String, nullable=False)  # e.g., 'renaiss', 'ebay'
    ask_price = Column(Float, nullable=True)
    fmv_price = Column(Float, nullable=True)
    offer_price = Column(Float, nullable=True)
    link = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    card = relationship("Card", back_populates="listings")

    def __repr__(self):
        return f"<Listing(source=\'{self.source}\', price=\'{self.ask_price}\')>"

class ArbitrageLog(Base):
    """ArbitrageLog model to record discovered arbitrage opportunities."""
    __tablename__ = "arbitrage_logs"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    profit_percent = Column(Float, nullable=False)
    profit_usd = Column(Float, nullable=False)
    type = Column(String) # e.g., 'fmv_arbitrage', 'cross_platform'
    details = Column(String) # JSON string with details
    discovered_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Initializes the database and creates tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency to get a database session."""
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()
