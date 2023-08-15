import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Dino Game")
Clock = pygame.time.Clock()

track_surface = pygame.image.load("Image/Other/Track.png").convert_alpha()
dino = pygame.image.load("Image/Dino/DinoJump.png").convert_alpha()
dino_x = 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    screen.blit(track_surface, (0, 300))

    dino_x += 3
    screen.blit(dino, (dino_x, 230))

    Clock.tick(60)
    pygame.display.update()



