import pymunk

class Physic:

    def __init__(self):
        self.space = pymunk.Space() #création d'un espace de gravité
        self.space.gravity = (0, -1000) #set-up des variables de cette espace (-1000 de gravité)
        self.space.damping = 1 #rétention des objets dans l'espace



