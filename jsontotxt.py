import json

with open("reddit_dreams.json", "r", encoding="utf-8") as f:
    dreams = json.load(f)

docs = [d['content'] for d in dreams if d['content'].strip()]
