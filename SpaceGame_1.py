import pygame as pyg
import random
import math

pyg.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 7
BULLET_SPEED = 20
ENEMY_SPEED_MIN = 3
ENEMY_SPEED_MAX = 6
ENEMY_DROP = 60
POWERUP_SPEED = 8

window = pyg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pyg.display.set_caption("Extreme Space Invaders")
backgroundImg = pyg.image.load("SpaceInvaders/assets/2151625881.jpg")
resized_background = pyg.transform.scale(backgroundImg, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Player
playerImg = pyg.image.load("SpaceInvaders/assets/transparent_2024-08-11T02-23-32.png")
playerImg = pyg.transform.scale(playerImg, (60, 60))
playerX = WINDOW_WIDTH // 2 - 30
playerY = WINDOW_HEIGHT - 80
playerXchange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemy_mask = []
number_of_enemies = 12  # Change this to change number of enemies

for i in range(number_of_enemies):
    enemy_img = pyg.image.load("SpaceInvaders/assets/enemy-Photoroom.png")
    enemy_img = pyg.transform.scale(enemy_img, (50, 50))
    enemyImg.append(enemy_img)
    enemyX.append(random.randint(0, WINDOW_WIDTH - 50))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX))
    enemyYchange.append(ENEMY_DROP)
    enemy_mask.append(pyg.mask.from_surface(enemy_img))

# Bullet
bulletImg = pyg.image.load("SpaceInvaders/assets/—Pngtree—red bullet effect light effect_7150008.png")
bulletImg = pyg.transform.scale(bulletImg, (80, 80))
bulletImg = pyg.transform.rotate(bulletImg, 90)
bulletX = -80
bulletY = WINDOW_HEIGHT - 80
bulletState = "ready"
bulletXchange = 0
bulletYchange = BULLET_SPEED
bullet_mask = pyg.mask.from_surface(bulletImg)

# Power-up
powerupImg = pyg.Surface((20, 20))
powerupImg.fill((255, 255, 0))  # Yellow color
powerupX = random.randint(0, WINDOW_WIDTH - 20)
powerupY = -50
powerupYchange = POWERUP_SPEED
powerup_active = False
powerup_timer = 0

# Fonts and Colors
font = pyg.font.Font('freesansbold.ttf', 32)
text_color = (255, 255, 255)  # White color

# Game Over Font
game_over_font = pyg.font.Font('freesansbold.ttf', 64)

# Score and Lives
score_value = 0
lives = 1  # Only one life

def playerDraw(x, y):
    window.blit(playerImg, (x, y))

def enemyDraw(x, y, i):
    window.blit(enemyImg[i], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    window.blit(bulletImg, (x, y))

def isCollision(x1, y1, x2, y2, mask1, mask2):
    offset = (int(x2 - x1), int(y2 - y1))
    return mask1.overlap(mask2, offset) is not None

def show_score(x, y):
    score = font.render(f"Score: {score_value} | Lives: {lives}", True, text_color)
    window.blit(score, (x, y))

def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, text_color)
    window.blit(game_over, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50))

def show_game_over_screen():
    window.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, text_color)
    score_text = font.render(f"Your Score: {score_value}", True, text_color)
    play_again_text = font.render("Press ENTER to Play Again", True, text_color)
    
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 100))
    window.blit(score_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 +100))
    window.blit(play_again_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2  -10))

    pyg.display.update()

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_RETURN:
                    return

def reset_game():
    global score_value, lives, playerX, bulletY, bulletState, enemyX, enemyY, powerup_active, powerup_timer
    score_value = 0
    lives = 1
    playerX = WINDOW_WIDTH // 2 - 30
    bulletY = WINDOW_HEIGHT - 80
    bulletState = "ready"
    powerup_active = False
    powerup_timer = 0
    for i in range(number_of_enemies):
        enemyX[i] = random.randint(0, WINDOW_WIDTH - 50)
        enemyY[i] = random.randint(50, 150)
        enemyXchange[i] = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

clock = pyg.time.Clock()
running = True
game_over = False
last_bullet_time = 0
bullet_cooldown = 500

# ...

# ...

# ...

while running:
    clock.tick(60)  # Limit the game to 60 FPS
    window.blit(resized_background, (0, 0))

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.KEYDOWN:
            if game_over:
                if event.key == pyg.K_RETURN:
                    reset_game()
                    game_over = False
            else:
                if event.key == pyg.K_a:
                    playerXchange = -PLAYER_SPEED
                if event.key == pyg.K_d:
                    playerXchange = PLAYER_SPEED

        if event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1 and bulletState == "ready":
                current_time = pyg.time.get_ticks()
                if current_time - last_bullet_time > bullet_cooldown:
                    bulletX = playerX + playerImg.get_width() // 2 - bulletImg.get_width() // 2
                    bulletY = playerY - bulletImg.get_height()
                    fireBullet(bulletX, bulletY)
                    last_bullet_time = current_time

    keys = pyg.key.get_pressed()
    if keys[pyg.K_a]:
        playerXchange = -PLAYER_SPEED
    elif keys[pyg.K_d]:
        playerXchange = PLAYER_SPEED
    else:
        playerXchange = 0

# ...

# ...

# ...

    if not game_over:
        playerX += playerXchange
        playerX = max(0, min(playerX, WINDOW_WIDTH - 60))

        if bulletState == "fire":
            fireBullet(bulletX, bulletY)
            bulletY -= bulletYchange
            if bulletY <= 0:
                bulletY = WINDOW_HEIGHT - 80
                bulletState = "ready"

        for i in range(number_of_enemies):
            # Sinusoidal movement
            enemyX[i] += enemyXchange[i]
            enemyY[i] += math.sin(pyg.time.get_ticks() * 0.01) * 2  # Subtle up and down movement
            
            if enemyX[i] <= 0 or enemyX[i] >= WINDOW_WIDTH - 50:
                enemyXchange[i] *= -1
                enemyY[i] += enemyYchange[i]

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY, enemy_mask[i], bullet_mask):
                bulletY = WINDOW_HEIGHT - 80
                bulletState = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, WINDOW_WIDTH - 50)
                enemyY[i] = random.randint(50, 150)
                enemyXchange[i] = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)  # Randomize speed after respawn

            if isCollision(enemyX[i], enemyY[i], playerX, playerY, enemy_mask[i], pyg.mask.from_surface(playerImg)) or enemyY[i] > WINDOW_HEIGHT - 80:
                lives -= 1
                if lives <= 0:
                    game_over = True
                    show_game_over_screen()
                    break

            enemyDraw(enemyX[i], enemyY[i], i)

        # Power-up logic
        if not powerup_active:
            powerupY += powerupYchange
            window.blit(powerupImg, (powerupX, powerupY))
            if isCollision(powerupX, powerupY, playerX, playerY, pyg.mask.from_surface(powerupImg), pyg.mask.from_surface(playerImg)):
                powerup_active = True
                powerup_timer = pyg.time.get_ticks()
                bulletYchange = BULLET_SPEED * 1.5  # 1.5x bullet speed instead of 2x
            if powerupY > WINDOW_HEIGHT:
                powerupX = random.randint(0, WINDOW_WIDTH - 20)
                powerupY = -50
        else:
            if pyg.time.get_ticks() - powerup_timer > 3000:  # 3 seconds duration instead of 5
                powerup_active = False
                bulletYchange = BULLET_SPEED  # Reset bullet speed

        playerDraw(playerX, playerY)
        show_score(10, 10)

    pyg.display.update()

pyg.quit()