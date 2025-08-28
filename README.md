# 🚀 crypto_bot

## 🎯 Amaç
Kripto ve hisse piyasalarında **yeni fırsatları** yakalamak için;
- Yeni listelemeler
- AI destekli analiz
- Haber & sentiment
- Otomatik al-sat botları

tek bir depoda toplanır. Bu repo hem **öğrenme** hem de **prototip** amaçlıdır.

---

# 🌐 Platform Özellikleri

## Çekirdek Özellikler (MVP)
### 🆕 Yeni Listelemeler
- Çoklu borsa entegrasyonu ile **yaklaşan/yeni listelenen** coinler.
- T₀ sonrası 1-5-15 dk grafikleri, hacim ve spread göstergeleri.
- Sinyal kartları: “Likidite OK / Spread OK / Trade akışı OK”.

### 🤖 AI Destekli Analiz
- SMA, EMA, RSI, MACD, ATR.
- Basit ML tahminleri + güven skoru.
- **Risk derecelendirme**: Düşük/Orta/Yüksek.

### 📰 Haber Merkezi
- Kripto & hisse için birleşik akış.
- **AI özet** (2-3 cümle) + **sentiment etiketi**.
- Coin/symbol bazlı haber geçmişi + fiyat reaksiyonu.

---

## İleri Özellikler
- Alım-satım botu (SMA, RSI, Haber+Trend, Listeleme Sniper)
- Risk modülü (SL/TP/Trailing, kill-switch, günlük limit)
- Testnet → Gerçek akışı
- Staking paneli
- Strategy marketplace, webhook/API, A/B parametre testi

---

## Basit Sayfa Yapısı (öneri)
```
/ (Landing)
/features
/listings
/analysis
/news
/bots
/staking
/docs
```

---

# 🤖 Trade Bot Planları (Detaylı)

Bu bölüm, bot planları ve örnek **kod iskeletlerini** içerir. Kodlar **öğrenme/prototip** amaçlıdır.

## 1) Basit SMA Botu (MVP Başlangıç)
**Strateji:** SMA50>SMA200 → Long, tersi → Flat/Sat  
**Risk:** SL %1.5, TP %3, Günlük limit −2R

**Backtest — Örnek Kod**
```python
import ccxt, pandas as pd

ex = ccxt.binance(); ex.set_sandbox_mode(True)
ohlcv = ex.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=600)

df = pd.DataFrame(ohlcv, columns=["ts","o","h","l","c","v"])
df["sma50"] = df["c"].rolling(50).mean()
df["sma200"] = df["c"].rolling(200).mean()
df = df.dropna()

df["signal"] = (df["sma50"] > df["sma200"]).astype(int)
df["ret"] = pd.Series(df["c"]).pct_change().fillna(0)
df["pos"] = df["signal"].shift(1).fillna(0)
fee = 0.001
turnover = (df["pos"] - df["pos"].shift(1)).abs().fillna(0)
df["strat"] = df["pos"]*df["ret"] - turnover*fee

equity = (1+df["strat"]).cumprod()
print("Cumulative:", equity.iloc[-1])
```

**Testnet Emir — Örnek Kod**
```python
import ccxt, os
from dotenv import load_dotenv
load_dotenv()

ex = ccxt.binance({
  "apiKey": os.getenv("API_KEY"),
  "secret": os.getenv("API_SECRET"),
  "enableRateLimit": True
})
ex.set_sandbox_mode(True)

symbol, amount = "BTC/USDT", 0.001
print(ex.create_order(symbol, "market", "buy", amount))
```

---

## 2) Haber & Sentiment Botu
**Veri:** Haber API + FinBERT  
**Filtre:** Pozitif+Trend↑ → Long, Negatif+Trend↓ → Short, aksi → Flat

**Sentiment — Örnek Kod**
```python
from transformers import pipeline
nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")
text = "Bitcoin ETF inflows hit record levels"
print(nlp(text))  # [{'label': 'positive', 'score': 0.95}]
```

**Sinyal Birleştirme — Örnek Kod**
```python
def trend_up(df):  # df: ohlcv DataFrame
    return df["c"].iloc[-1] > df["c"].rolling(100).mean().iloc[-1]

def signal_from_news(sent_label, sent_score, up):
    if sent_label == "positive" and sent_score > 0.8 and up:
        return "LONG"
    if sent_label == "negative" and sent_score > 0.8 and not up:
        return "SHORT"
    return "FLAT"
```

---

## 3) Listeleme Sniper Bot
**Hedef:** Yeni listelenen coinlerde ilk spike’tan hızlı kâr.  
**Kurallar:** IOC/FOK limit buy (slip ≤%2–3), Ladder TP (+5%, +10%), Trailing stop (zirveden −%3), ≤90 sn zaman limiti.  
**Filtre:** Spread <0.8%, Depth >200k USDT, ≥3 trade/3 sn.

**FSM**
```
IDLE → DISCOVERED → READY → ENTERED → EXITING → DONE/ABORT
```

**IOC Emir — Örnek Kod**
```python
import ccxt
ex = ccxt.binance({ "apiKey": "...", "secret": "...", "enableRateLimit": True })
ex.set_sandbox_mode(True)

symbol, price_cap, qty = "NEW/USDT", 1.05, 10
order = ex.create_order(symbol, "limit", "buy", qty, price_cap, {"timeInForce": "IOC"})
print(order)
```

**Basit Exit — Örnek Kod**
```python
def ladder_take_profit(avg_entry, last, size):
    tp1, tp2 = avg_entry*1.05, avg_entry*1.10
    t = []
    if last >= tp1: t.append(("sell", size*0.5, last))
    if last >= tp2: t.append(("sell", size*0.3, last))
    return t
```

---

## 4) Ortak Mimari
```
[MarketData] → [Strategy Engine] → [Risk Manager] → [Execution]
                                ↘ [Logging / Monitoring / Alerts] ↙
```

**Config — Örnek**
```python
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
```

**Risk — Örnek**
```python
def risk_sizing(equity, r, price, lot=0.0001):
    raw = max(0.0, (equity*r)/max(price,1e-9))
    steps = int(raw/lot)
    return steps*lot
```

**Kill-Switch — Örnek**
```python
def kill_switch(day_R, threshold_R=-2.0):
    return day_R <= threshold_R
```

---

## 5) Yol Haritası (Botlar)
- MVP: SMA Botu → backtest + testnet  
- AI: Sentiment filtresi → backtest + canlı test  
- Hız: Listeleme Sniper → WS + slip kontrol + exit disiplini  
- Prod: Log/alert, dashboard, parametre yönetimi, çoklu borsa  

---

## ⚠️ Uyarı
Kodlar **öğrenme/prototip** içindir. Canlıya geçmeden önce **testnet** ve **risk kontrolleri** şarttır. Yatırım tavsiyesi değildir.
