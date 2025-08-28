from dataclasses import dataclass

@dataclass
class Config:
    symbol: str = "BTC/USDT"
    slip_cap: float = 0.025
    max_spread: float = 0.008
    min_depth_usd: float = 200_000
    time_cut_sec: int = 90
    trailing_drop: float = 0.03
    risk_per_trade: float = 0.01
