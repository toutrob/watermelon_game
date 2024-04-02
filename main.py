import pygame

pygame.init()

window_size = (1200, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw shapes
    ##window.fill((255, 255, 255))
    ##pygame.draw.circle(window, (255, 255, 0), (150, 200), 50)
    ##pygame.draw.rect(window, (0, 200, 0), (100, 300, 300, 200))
    ##pygame.draw.line(window, (0, 0, 100), (100, 100), (700, 500), 5)

    pygame.display.flip()
pygame.quit()