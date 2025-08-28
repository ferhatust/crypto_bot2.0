import ccxt
from bots.common.config import Config
from bots.common.risk import risk_sizing

class SniperFSM:
    def __init__(self, ex, cfg: Config):
        self.ex, self.cfg = ex, cfg
        self.state = "IDLE"
        self.entry_price = None
        self.size = 0.0

    def on_discovered(self):
        self.state = "DISCOVERED"

    def on_ready(self):
        self.state = "READY"

    def enter(self, price):
        self.entry_price = price
        self.size = 10  # örnek
        self.state = "ENTERED"

    def exit_logic(self, last):
        # örnek ladder & trailing yerine basit koşul
        if self.entry_price and last >= self.entry_price * 1.05:
            self.state = "EXITING"

if __name__ == "__main__":
    ex = ccxt.binance()
    ex.set_sandbox_mode(True)
    cfg = Config()
    fsm = SniperFSM(ex, cfg)
    print("FSM initial state:", fsm.state)
