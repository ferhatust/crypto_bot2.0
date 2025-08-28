# 🧭 Kurulum ve Kullanım (crypto_bot)

## 1) Ortam
- Python 3.10+ önerilir
- `git` kurulu olmalı

## 2) Sanal Ortam ve Bağımlılıklar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 3) .env
`.env.example` dosyasını kopyalayın ve doldurun:
```bash
cp .env.example .env
```

## 4) SMA Backtest Hızlı Deneme
```bash
python bots/sma_bot.py
```

## 5) Sentiment Hızlı Deneme
```bash
python bots/sentiment_bot.py
```

## 6) GitHub’a Push
```bash
git init
git branch -M main
git add .
git commit -m "Initial commit: crypto_bot scaffold"
git remote add origin https://github.com/KULLANICI_ADIN/crypto_bot.git
git push -u origin main
```
