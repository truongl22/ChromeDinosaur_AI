import pygame
from sys import exit

pygame.init()

# Set up screen
SCREEN = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Dino Game")
Clock = pygame.time.Clock()

# Set up images for Dinosaur
dinoJump = pygame.image.load("Image/Dino/DinoJump.png").convert_alpha()

dinoRun1 = pygame.image.load("Image/Dino/DinoRun1.png").convert_alpha()
dinoRun2 = pygame.image.load("Image/Dino/DinoRun2.png").convert_alpha()
dinoRun = [dinoRun1, dinoRun2]

dinoDuck1 = pygame.image.load("Image/Dino/DinoDuck1.png").convert_alpha()
dinoDuck2 = pygame.image.load("Image/Dino/DinoDuck2.png").convert_alpha()
dinoDuck = [dinoDuck1, dinoDuck2]

# Set up images for surface
track_surface = pygame.image.load("Image/Track/Track.png").convert_alpha()


# Set up Dino class
class Dino:
    velocity = 8.5
    x_pos = 80
    y_pos = 310
    y_duck_pos = 340

    def __init__(self, image=dinoRun[0]):
        self.image = image
        self.jump_velocity = self.velocity
        self.run = True
        self.jump = False
        self.duck = False
        self.dinoRect = image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.stepIndex = 0

    def update(self):
        if self.run:
            self.running()
        if self.jump:
            self.jumping()
        if self.duck:
            self.ducking()
        if self.stepIndex >= 10:
            self.stepIndex = 0

    def running(self):
        self.image = dinoRun[self.stepIndex // 5]
        self.dinoRect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.stepIndex += 1

    def jumping(self):
        self.image = dinoJump
        if self.jump:
            self.dinoRect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity <= -self.velocity:
            self.jump = False
            self.run = True
            self.jump_velocity = self.velocity

    def ducking(self):
        self.image = dinoDuck[self.stepIndex // 5]
        self.dinoRect = self.image.get_rect(topleft=(self.x_pos, self.y_duck_pos))
        self.stepIndex += 1

    def drawDino(self, SCREEN):
        SCREEN.blit(self.image, self.dinoRect)

# Set up main function
def main():
    dinos = [Dino()]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        SCREEN.fill((255, 255, 255))

        for dinosaur in dinos:
            dinosaur.update()
            dinosaur.drawDino(SCREEN)

        user_input = pygame.key.get_pressed()

        for i, dino in enumerate(dinos):
            if user_input[pygame.K_SPACE]:
                dino.run = False
                dino.jump = True
                dino.duck = False
            if user_input[pygame.K_DOWN]:
                dino.run = False
                dino.jump = False
                dino.duck = True
            elif not (dino.jump or user_input[pygame.K_DOWN]):
                dino.run = True
                dino.jump = False
                dino.duck = False

        Clock.tick(40)
        pygame.display.update()


main()
