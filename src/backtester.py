import matplotlib.pyplot as plt
from .simulator import AviatorSimulator
from .agents import FixedFractionAgent, KellyCriterionAgent, MartingaleAgent, MLAgent
import random

class Backtester:
    def __init__(self, agents, num_rounds=100):
        self.agents = agents
        self.num_rounds = num_rounds
        self.results = {agent.__class__.__name__: [] for agent in agents}

    def run_simulation(self):
        for round_num in range(self.num_rounds):
            sim = AviatorSimulator()
            crash_mult = sim.generate_crash_multiplier()
            for agent in self.agents:
                bet_amount, target_mult = agent.decide_bet(sim.hash)
                if bet_amount > agent.balance:
                    bet_amount = agent.balance
                if bet_amount <= 0:
                    payout = 0
                else:
                    # Simulate cash out: random between 1.0 and crash_mult
                    cash_out_mult = random.uniform(1.0, crash_mult)
                    if cash_out_mult <= target_mult:
                        payout = bet_amount * cash_out_mult - bet_amount
                    else:
                        payout = -bet_amount
                agent.update_balance(payout)
                self.results[agent.__class__.__name__].append(agent.balance)

    def calculate_metrics(self, balances):
        initial = balances[0]
        final = balances[-1]
        total_return = (final - initial) / initial
        peak = max(balances)
        trough = min(balances)
        max_drawdown = (peak - trough) / peak
        # Simple Sharpe: assume risk-free 0, std of returns
        returns = [balances[i] / balances[i-1] - 1 for i in range(1, len(balances))]
        sharpe = sum(returns) / len(returns) / (sum(r**2 for r in returns)/len(returns))**0.5 if returns else 0
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'final_balance': final
        }

    def plot_results(self):
        for name, balances in self.results.items():
            plt.plot(balances, label=name)
        plt.xlabel('Rounds')
        plt.ylabel('Balance')
        plt.title('Agent Performance Over Time')
        plt.legend()
        plt.show()

    def run_and_report(self):
        self.run_simulation()
        for name, balances in self.results.items():
            metrics = self.calculate_metrics(balances)
            print(f"{name}: {metrics}")
        self.plot_results()

if __name__ == "__main__":
    agents = [
        FixedFractionAgent(1),
        KellyCriterionAgent(2),
        MartingaleAgent(3),
        MLAgent(4)
    ]
    backtester = Backtester(agents, num_rounds=50)
    backtester.run_and_report()
