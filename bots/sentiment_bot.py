from transformers import pipeline

def score_text(text: str):
    nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    return nlp(text)[0]

if __name__ == "__main__":
    print(score_text("Bitcoin ETF inflows hit record levels"))
