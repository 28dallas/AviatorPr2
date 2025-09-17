# Aviator-sim-research

## Overview
Aviator-sim-research is an educational, local-only crash game simulator inspired by the Aviator game. It features a provably fair mechanism using cryptographically secure RNG and SHA-256 hashing. The project includes a mock API, automated betting agents with various strategies, a backtester with performance metrics and charts, and safety features to ensure ethical use.

## Features
- Secure and provably fair crash game simulation.
- Multiple automated betting agents: Fixed-fraction, Kelly Criterion, Martingale, and ML-based.
- Backtesting framework with detailed metrics and matplotlib charts.
- SQLite persistence for game and bet data.
- Safety limits and disclaimers to prevent real betting misuse.
- Local-only, no real money or betting platform integration.

## Installation
1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- Run the FastAPI mock API:
  ```bash
  uvicorn src.api:app --reload
  ```
- Use the backtester to evaluate strategies (details to be added).

## Disclaimer
This project is for educational and research purposes only. It does not connect to any real betting platforms and should not be used for real gambling.

## License
MIT License
# AviatorPr2
