import pygame
import random
from sys import exit

pygame.init()

# Set up screen
game_width = 1200
game_height = 600
SCREEN = pygame.display.set_mode((game_width, game_height))
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

# Set up cactus
cactus1 = pygame.image.load("Image/Cactus/Cactus1.png").convert_alpha()
cactus2 = pygame.image.load("Image/Cactus/Cactus2.png").convert_alpha()
cactus3 = pygame.image.load("Image/Cactus/Cactus3.png").convert_alpha()
cactusArray = [cactus1, cactus2, cactus3]

# Set up Bird
bird1 = pygame.image.load("Image/Bird/Bird1.png").convert_alpha()
bird2 = pygame.image.load("Image/Bird/Bird2.png").convert_alpha()
birds = [bird1, bird2]

# Set up background
track_surface = pygame.image.load("Image/Track/Track.png").convert_alpha()
cloud = pygame.image.load("Image/Cloud/Cloud.png").convert_alpha()

# Set up font
FONT = pygame.font.Font('freesansbold.ttf', 22)


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

    def updateDino(self):
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
        self.jump_velocity = self.velocity
        self.stepIndex += 1

    def drawDino(self, SCREEN):
        SCREEN.blit(self.image, self.dinoRect)


# Set up Track class
class Track:
    def __init__(self):
        self.image = track_surface

    def createTrack(self):
        global x_track_pos, y_track_pos
        image_width = track_surface.get_width()
        SCREEN.blit(track_surface, (x_track_pos, y_track_pos))
        SCREEN.blit(track_surface, (image_width + x_track_pos, y_track_pos))
        if x_track_pos <= - image_width:
            x_track_pos = 0
        x_track_pos -= game_speed


# Set up Cloud class
class Cloud:
    cloud_width = cloud.get_width()
    x = game_width + cloud_width
    y = 42

    def __init__(self):
        self.image = cloud

    def createCloud(self):
        image_width = track_surface.get_width()
        SCREEN.blit(cloud, (self.x, self.y))
        if self.x <= - image_width:
            self.x = game_width + self.cloud_width
        self.x -= game_speed


# Set up Enemies class
class Enemies:
    def __init__(self, image, type):
        self.type = type
        self.image = image
        self.rect = self.image[self.type].get_rect()
        self.rect.x = game_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            enemies.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


# Set up Cactus class, inherit from Enemies
class Cactus(Enemies):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 315


# Set up Bird class, inherit from Enemies
class Bird(Enemies):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def removeDino(index):
    dinos.pop(index)


# Set up main function
def main():
    global game_speed, x_track_pos, y_track_pos, dinos, enemies, points
    points = 0
    game_speed = 20
    x_track_pos, y_track_pos = 0, 380
    score_pos = (950, 50)

    dinos = [Dino()]
    enemies = []
    track = Track()
    cloud = Cloud()

    def getScore():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points:  {str(points)}', True, 'Black')
        SCREEN.blit(text, score_pos)

    def handleUserInput():
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

    def createDino():
        for d in dinos:
            d.updateDino()
            d.drawDino(SCREEN)

    def createEnemies():
        if len(enemies) == 0:
            rand = random.randint(0, 10)
            if rand % 2 == 0:
                enemies.append(Cactus(cactusArray))
            if rand == 7 or rand == 5:
                enemies.append(Bird(birds))

        for e in enemies:
            e.update()
            e.draw(SCREEN)
            for i, dinosaur in enumerate(dinos):
                if dinosaur.dinoRect.colliderect(e.rect):
                    removeDino(i)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        SCREEN.fill((255, 255, 255))

        createDino()
        createEnemies()
        handleUserInput()
        getScore()
        track.createTrack()
        cloud.createCloud()

        if len(dinos) == 0:
            break
        Clock.tick(40)
        pygame.display.update()


main()
