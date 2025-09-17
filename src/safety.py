import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SafetyManager:
    def __init__(self, max_bet_fraction=0.1, max_daily_loss=500.0):
        self.max_bet_fraction = max_bet_fraction  # Max bet as fraction of balance
        self.max_daily_loss = max_daily_loss
        self.daily_loss = 0.0

    def check_bet(self, user_balance, bet_amount):
        if bet_amount > user_balance * self.max_bet_fraction:
            logger.warning(f"Bet {bet_amount} exceeds max fraction for balance {user_balance}")
            return False
        if self.daily_loss + bet_amount > self.max_daily_loss:
            logger.warning(f"Bet would exceed daily loss limit")
            return False
        return True

    def log_bet(self, user_id, bet_amount, outcome):
        logger.info(f"User {user_id} bet {bet_amount}, outcome: {outcome}")
        if outcome < 0:
            self.daily_loss += abs(outcome)

    def reset_daily_loss(self):
        self.daily_loss = 0.0
        logger.info("Daily loss reset")

    @staticmethod
    def print_disclaimer():
        print("""
        DISCLAIMER:
        This is an educational simulation only.
        Do not use for real gambling.
        No real money is involved.
        Results are for research purposes.
        """)

# Global instance
safety_manager = SafetyManager()
safety_manager.print_disclaimer()
