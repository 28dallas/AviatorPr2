from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Game, Bet
from .simulator import AviatorSimulator
import os

DATABASE_URL = "sqlite:///./data/aviator.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Aviator Simulator API", description="Mock API for Aviator crash game simulation")

# Create tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aviator Simulator API"}

@app.post("/user/create")
def create_user(username: str):
    db = SessionLocal()
    try:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"user_id": user.id, "username": user.username, "balance": user.balance}
    finally:
        db.close()

@app.post("/game/start")
def start_game():
    db = SessionLocal()
    try:
        sim = AviatorSimulator()
        game = Game(seed=sim.seed, hash=sim.hash, crash_multiplier=sim.generate_crash_multiplier())
        db.add(game)
        db.commit()
        db.refresh(game)
        return {"game_id": game.id, "hash": game.hash}
    finally:
        db.close()

@app.post("/bet")
def place_bet(user_id: int, game_id: int, amount: float):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        # Assume bet is placed before crash
        bet = Bet(user_id=user_id, game_id=game_id, amount=amount)
        db.add(bet)
        user.balance -= amount
        db.commit()
        db.refresh(bet)
        return {"bet_id": bet.id, "amount": bet.amount}
    finally:
        db.close()

@app.post("/game/crash/{game_id}")
def crash_game(game_id: int):
    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        bets = db.query(Bet).filter(Bet.game_id == game_id).all()
        for bet in bets:
            if bet.cash_out_multiplier is None:  # Not cashed out, lost
                bet.payout = 0.0
            else:
                bet.payout = bet.amount * bet.cash_out_multiplier
                bet.user.balance += bet.payout
        db.commit()
        return {"crash_multiplier": game.crash_multiplier, "bets_processed": len(bets)}
    finally:
        db.close()

@app.post("/bet/cashout/{bet_id}")
def cash_out_bet(bet_id: int, multiplier: float):
    db = SessionLocal()
    try:
        bet = db.query(Bet).filter(Bet.id == bet_id).first()
        if not bet:
            raise HTTPException(status_code=404, detail="Bet not found")
        game = bet.game
        if multiplier > game.crash_multiplier:
            raise HTTPException(status_code=400, detail="Cannot cash out after crash")
        bet.cash_out_multiplier = multiplier
        bet.payout = bet.amount * multiplier
        bet.user.balance += bet.payout
        db.commit()
        return {"payout": bet.payout}
    finally:
        db.close()

@app.get("/user/{user_id}/balance")
def get_balance(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"balance": user.balance}
    finally:
        db.close()
