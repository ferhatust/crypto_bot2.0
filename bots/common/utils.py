import os
import ccxt
from dotenv import load_dotenv

def init_exchange(testnet: bool = True):
    load_dotenv()
    ex = ccxt.binance({
        "apiKey": os.getenv("API_KEY"),
        "secret": os.getenv("API_SECRET"),
        "enableRateLimit": True,
    })
    ex.set_sandbox_mode(testnet)
    return ex
