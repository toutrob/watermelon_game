#Gere le chargement et la sauvegarde des scores élevés à partir d'un fichier texte

#Pour charger le highscore
def load_highscores():
    with open("highscores.txt", "r") as file: #ouvre le fichier en mode lecture
        highscores = [int(line.strip()) for line in file.readlines()] #lit toutes les lignes, enleve les espaces et convertit en un entier
        return sorted(highscores, reverse=True)[:5]#Tri des scores par ordre decroissant et affiche les 5 premiers

#Pour enregistrer le highscore
def save_highscores(highscores):
    with open("highscores.txt", "w") as file: #ouvre le fichier en mode ecriture
        for score in highscores:
            file.write(f"{score}\n") #chaque score est ecrit dans le fichier sur une nouvelle ligne