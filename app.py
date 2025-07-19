from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from data.fetcher import fetch_stock_data
from strategies.momentum import apply_momentum_strategy
from backtest.core import backtest

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to your GitHub Pages domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/backtest")
def run_backtest(
    symbol: str = Query(..., description="Stock symbol"),
    period: str = Query("3mo", description="Data period"),
    stop: float = Query(0.02, description="Stop loss (e.g. 0.02 for 2%)"),
    target: float = Query(0.04, description="Take profit (e.g. 0.04 for 4%)"),
):
    df = fetch_stock_data(symbol, period=period)
    strat_df = apply_momentum_strategy(df)
    final_value, return_pct, trade_log = backtest(strat_df, symbol, stop_loss_pct=stop, take_profit_pct=target)
    return {
        "symbol": symbol,
        "final_value": final_value,
        "return_pct": return_pct,
        "trades": trade_log,
    }

# AWS Lambda handler using Mangum
from mangum import Mangum
handler = Mangum(app)
