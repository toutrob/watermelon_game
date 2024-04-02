import pygame


class boules:
    def __init__(self, screen, centre):
        #self.poids = poids
        #self.type = type
        #self.sprite = sprite
        self.centre = list(centre)
        self.screen = screen

    ##def gravity(self):
        ##self.centre[1] += 0.02

    def dessin(self):
        pygame.draw.circle(self.screen, (255,0,0), self.centre, 4 )


pygame.init()

window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")
boule = boules(window, (500,500))
window.fill((255, 255, 255))

running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    window.fill((255, 255, 255))


    ##boule.gravity()
    boule.dessin()


    # Draw shapes
    ##window.fill((255, 255, 255))
    ##pygame.draw.circle(window, (255, 255, 0), (150, 200), 50)
    ##pygame.draw.rect(window, (0, 200, 0), (100, 300, 300, 200))
    ##pygame.draw.line(window, (0, 0, 100), (100, 100), (700, 500), 5)

    pygame.display.flip()
pygame.quit()

