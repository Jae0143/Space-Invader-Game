import pygame
import random
import math
import os
import time
from pygame import mixer

# initialize the pygame
pygame.init()

# Check display
dis_info = pygame.display.Info()
screen_width, screen_height = dis_info.current_w, dis_info.current_h

# Create the screen - Width, height
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Background
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ship.png')
playerX = screen_width / 2 - 10
playerY = screen_height * 4 / 5
playerXChange = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_enemy = 6

for i in range(num_enemy):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, screen_width - 1))
    enemyY.append(random.randint(50, screen_height * 1 / 2))
    enemyXChange.append(25)
    enemyYChange.append(55)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x[i], y[i]))


# bullet (ready = you can't see the bullet, fire = bullet is moving)
bulletImg = pygame.image.load("Missile.png")
bulletX = playerX - 2
bulletY = playerY
bulletYChange = 15
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("ARCADECLASSIC.TTF", 50)
textX = 20
textY = 20

# Game over text
game_over = False
over_font = pygame.font.Font("ARCADECLASSIC.TTF", 100)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_width / 3, screen_height / 3))


def show_score(x, y):
    score = font.render("SCORE  " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16.7, y - 32))


# distance
def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distan = dist(enemyX, enemyY, bulletX, bulletY)
    if distan < 45:
        return True
    return False


# Game Loop (anything persistant)
running = True

while running:
    # set screen RGB - Red Green Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # if keystroke pressed -> check if it is right or left
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                playerXChange = -15
            if event.key == pygame.K_RIGHT:
                playerXChange = 15
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    # Checking for boundaries for spaceship
    playerX += playerXChange

    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 40:
        playerX = screen_width - 40

    # Enemy movement
    for i in range(num_enemy):
        # Game over
        distance_end = dist(enemyX[i], enemyY[i], playerX, playerY)
        if distance_end < 48:
            for j in range(num_enemy):
                # remove enemy and show game_over
                enemyY[j] = 100000000
            game_over = True
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 15
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= screen_width - 36:
            enemyXChange[i] = -15
            enemyY[i] += enemyYChange[i]
        enemy(enemyX, enemyY, i)

        # Collison
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            # Respawn enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

    # Bullet Movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    if game_over:
        game_over_text()
    player(playerX, playerY)

    show_score(textX, textY)

    # Always update game window
    pygame.display.update()
