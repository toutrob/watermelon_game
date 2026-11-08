import os

HIGHSCORE_FILE = "highscores.txt"

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return [0, 0, 0, 0, 0]
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
            highscores = [int(line.strip()) for line in file if line.strip().isdigit()]
            highscores = sorted(highscores, reverse=True)[:5]
            while len(highscores) < 5:
                highscores.append(0)
            return highscores
    except Exception:
        return [0, 0, 0, 0, 0]

def save_highscores(highscores):
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
            for score in sorted(highscores, reverse=True)[:5]:
                file.write(f"{score}\n")
    except Exception as e:
        print(f"Erreur sauvegarde highscores : {e}")