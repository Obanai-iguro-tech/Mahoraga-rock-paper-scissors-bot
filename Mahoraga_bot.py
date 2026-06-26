import random
import json
import os
from collections import defaultdict

DATA_FILE = "rps_data.json"

BEATS = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
LOSES_TO = {v: k for k, v in BEATS.items()}
CHOICES = list(BEATS.keys())


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"history": [], "score": {"you": 0, "bot": 0, "ties": 0}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def predict_next(history, depth=3):
    if len(history) < depth:
        return random.choice(CHOICES)


    pattern = tuple(history[-depth:])
    counts = defaultdict(int)

    for i in range(len(history) - depth):
        if tuple(history[i:i+depth]) == pattern:
            counts[history[i+depth]] += 1

    if not counts:

        freq = defaultdict(int)
        for move in history:
            freq[move] += 1
        predicted = max(freq, key=freq.get)
        return BEATS[predicted]

    predicted = max(counts, key=counts.get)
 
    return BEATS[predicted]


def get_result(player, bot):
    if player == bot:
        return "ties"
    if BEATS[player] == bot:
        return "bot"
    return "you"


def display_score(score):
    print(f"\n  You {score['you']}  |  Bot {score['bot']}  |  Ties {score['ties']}")


def display_result(player, bot, result):
    symbols = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
    print(f"\n  You: {symbols[player]} {player:<10} Bot: {symbols[bot]} {bot}")
    if result == "ties":
        print("  → Tie!")
    elif result == "you":
        print(f"  → You win! {player} beats {bot}")
    else:
        print(f"  → Bot wins! {bot} beats {player}")


def main():
    data = load_data()
    history = data["history"]
    score = data["score"]

    print("    Rock  Paper  Scissors     ")
    print("        with my bot       ")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
    print("\n  Commands: r/rock  p/paper  s/scissors  q/quit  reset")

    aliases = {"r": "rock", "p": "paper", "s": "scissors"}

    while True:
        display_score(score)
        raw = input("\n  Your move: ").strip().lower()

        if raw == "q" or raw == "quit":
            save_data({"history": history, "score": score})
            print("\n  See you next time.\n")
            break

        if raw == "reset":
            score = {"you": 0, "bot": 0, "ties": 0}
            history = []
            print("  Stats reset.")
            continue

        player = aliases.get(raw, raw)
        if player not in CHOICES:
            print("  Type r, p, or s.")
            continue

        bot = predict_next(history)
        result = get_result(player, bot)
        score[result] += 1
        history.append(player)

        display_result(player, bot, result)


        if len(history) == 10:
            print("\n  (mahoraga has enough data to start adapting — watch out)")

        save_data({"history": history, "score": score})


if __name__ == "__main__":
    main()
