from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=1000.0)  # Starting balance for simulation
    created_at = Column(DateTime, default=datetime.utcnow)

    bets = relationship("Bet", back_populates="user")

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    seed = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    crash_multiplier = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bets = relationship("Bet", back_populates="game")

class Bet(Base):
    __tablename__ = 'bets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    amount = Column(Float, nullable=False)
    cash_out_multiplier = Column(Float, nullable=True)  # None if not cashed out
    payout = Column(Float, nullable=True)  # Calculated payout
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bets")
    game = relationship("Game", back_populates="bets")
