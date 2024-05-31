def load_highscores():
    with open("highscores.txt", "r") as file:
        highscores = [int(line.strip()) for line in file.readlines()]
        return sorted(highscores, reverse=True)[:5]

def save_highscores(highscores):
    with open("highscores.txt", "w") as file:
        for score in highscores:
            file.write(f"{score}\n")