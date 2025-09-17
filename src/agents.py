import random
from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression
import numpy as np

class BaseAgent(ABC):
    def __init__(self, user_id, initial_balance=1000.0):
        self.user_id = user_id
        self.balance = initial_balance
        self.bets = []

    @abstractmethod
    def decide_bet(self, game_hash):
        """Decide bet amount and cash out multiplier."""
        pass

    def update_balance(self, payout):
        self.balance += payout
        self.bets.append(payout)

class FixedFractionAgent(BaseAgent):
    def __init__(self, user_id, fraction=0.01, cash_out=2.0):
        super().__init__(user_id)
        self.fraction = fraction  # Fraction of balance to bet
        self.cash_out = cash_out  # Target multiplier

    def decide_bet(self, game_hash):
        bet_amount = self.balance * self.fraction
        return bet_amount, self.cash_out

class KellyCriterionAgent(BaseAgent):
    def __init__(self, user_id, win_prob=0.5, odds=2.0):
        super().__init__(user_id)
        self.win_prob = win_prob
        self.odds = odds

    def decide_bet(self, game_hash):
        kelly_fraction = (self.odds * self.win_prob - 1) / (self.odds - 1)
        bet_amount = self.balance * kelly_fraction
        return bet_amount, self.odds

class MartingaleAgent(BaseAgent):
    def __init__(self, user_id, base_bet=10.0, cash_out=2.0):
        super().__init__(user_id)
        self.base_bet = base_bet
        self.cash_out = cash_out
        self.last_bet = base_bet

    def decide_bet(self, game_hash):
        bet_amount = self.last_bet
        # Double after loss, reset after win
        # For simplicity, assume we track wins/losses
        # In real use, would need to know previous outcome
        return bet_amount, self.cash_out

    def update_balance(self, payout):
        super().update_balance(payout)
        if payout > 0:
            self.last_bet = self.base_bet
        else:
            self.last_bet *= 2

class MLAgent(BaseAgent):
    def __init__(self, user_id, cash_out=2.0):
        super().__init__(user_id)
        self.cash_out = cash_out
        self.model = LinearRegression()
        self.history = []  # List of (bet_amount, outcome)

    def decide_bet(self, game_hash):
        if len(self.history) < 10:
            bet_amount = self.balance * 0.01  # Default
        else:
            # Simple ML: predict based on past
            X = np.array([h[0] for h in self.history]).reshape(-1, 1)
            y = np.array([h[1] for h in self.history])
            self.model.fit(X, y)
            predicted_outcome = self.model.predict([[self.balance * 0.01]])[0]
            bet_amount = self.balance * 0.01 * (1 + predicted_outcome)
        return bet_amount, self.cash_out

    def update_balance(self, payout):
        super().update_balance(payout)
        # Assume outcome is 1 if win, 0 if loss
        outcome = 1 if payout > 0 else 0
        self.history.append((self.balance * 0.01, outcome))
