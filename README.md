# Indian Algo Trading Bot

A modular, extensible Python framework for algorithmic trading and backtesting on Indian equities.

## Key Features
- **Modular architecture:**
  - `data/` — Data fetching utilities (e.g., Yahoo Finance)
  - `strategies/` — Plug-and-play trading strategies
  - `backtest/` — Vectorized, event-driven backtesting engine
  - `utils/` — Visualization and helper tools
- **Momentum strategy** with moving average crossovers (default)
- **Configurable stop-loss and take-profit**
- **Clear CLI for rapid experimentation**

## Quick Start
```bash
pip install -r requirements.txt
python main.py --symbol INFY --period 3mo --stop 0.02 --target 0.04
```

## Project Structure
```
indian-algo-trading-bot/
├── main.py
├── data/
├── strategies/
├── backtest/
├── utils/
└── requirements.txt
```

## Extend & Customize
- Add new strategies in `strategies/`
- Integrate broker APIs in `broker/` (future)
- Write tests in `tests/`

---
*Built for rapid research, robust analytics, and real-world trading.*
