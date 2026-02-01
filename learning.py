import json
import random
import time
from datetime import datetime

DATA_FILE = "words.json"

def load_words():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_words(words):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

def add_word(words):
    source = input("Word: ").strip()
    target = input("Translation: ").strip()
    words.append({
        "source": source,
        "target": target,
        "correct": 0,
        "wrong": 0,
        "last_review": None
    })
    save_words(words)

def choose_word(words):
    weighted = []
    for w in words:
        score = w["wrong"] - w["correct"]
        weighted.extend([w] * max(1, score + 1))
    return random.choice(weighted)

def train(words):
    if not words:
        print("No words yet 😅")
        return

    w = choose_word(words)
    print(f"\nTranslate: {w['source']}")
    answer = input("> ").strip()

    if answer.lower() == w["target"].lower():
        print("✅ Correct!")
        w["correct"] += 1
    else:
        print(f"❌ Wrong. Correct answer: {w['target']}")
        w["wrong"] += 1

    w["last_review"] = datetime.now().isoformat()
    save_words(words)
    time.sleep(1)

def show_stats(words):
    print("\n📊 Statistics:")
    for w in words:
        total = w["correct"] + w["wrong"]
        accuracy = (w["correct"] / total * 100) if total else 0
        print(f"{w['source']} → {w['target']} | {accuracy:.0f}%")

def main():
    words = load_words()

    while True:
        print("\n1. Add a word")
        print("2. Practice words")
        print("3. Statistics")
        print("4. Exit")

        choice = input("> ").strip()

        if choice == "1":
            add_word(words)
        elif choice == "2":
            train(words)
        elif choice == "3":
            show_stats(words)
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
