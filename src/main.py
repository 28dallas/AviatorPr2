import argparse
import uvicorn
from .backtester import Backtester
from .agents import FixedFractionAgent, KellyCriterionAgent, MartingaleAgent, MLAgent

def run_api():
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

def run_backtest(num_rounds=100):
    agents = [
        FixedFractionAgent(1),
        KellyCriterionAgent(2),
        MartingaleAgent(3),
        MLAgent(4)
    ]
    backtester = Backtester(agents, num_rounds=num_rounds)
    backtester.run_and_report()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aviator Simulator")
    parser.add_argument("mode", choices=["api", "backtest"], help="Run mode: api or backtest")
    parser.add_argument("--rounds", type=int, default=100, help="Number of rounds for backtest")
    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "backtest":
        run_backtest(args.rounds)
