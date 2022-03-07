import pygame
import os  # to find path for import of images, sound etc
from pygame import mixer
import sys
pygame.font.init()
pygame.mixer.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # creat a window with the chosen width and heigth
pygame.display.set_caption("Just poop on it!")

ICON = pygame.image.load(resource_path("poop.png"))
pygame.display.set_icon(ICON)

BLACK = (0, 0, 0)
BROWN = (95, 40, 0)
OLIVE = (48, 37, 0)

# Soundtrack
mixer.music.load(resource_path("marccut.mp3"))
mixer.music.play(-1)

# BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
BORDER = pygame.Surface((10, 500))
BORDER.set_colorkey(BLACK)  # make the border invisible
BORDER.fill((0, 0, 0))

BULLET_HIT_SOUND = pygame.mixer.Sound(resource_path("445109__breviceps__mud-splat.wav"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(resource_path("fartcut.mp3"))

HEALTH_FONT = pygame.font.SysFont("Arial", 16)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5  # Velocity
BULLET_VEL = 7
MAX_BULLETS = 3

PLAYER_1 = pygame.image.load(resource_path("output-onlinepngtools.png"))
PLAYER_2 = pygame.image.load(resource_path("output-onlinepngtools (1).png"))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 90

P_1_HIT = pygame.USEREVENT + 1  # Creating new events
P_2_HIT = pygame.USEREVENT + 2

BACKGROUND = pygame.image.load(resource_path("BACKTEST2.png"))


def draw_window(P_1, P_2, P_1_bullets, P_2_bullets, P_1_health, P_2_health):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(BORDER, (445, 0))
    # pygame.draw.rect(WIN, BLACK, BORDER)

    P_1_health_text = HEALTH_FONT.render(": " + str(P_1_health), 1, (0, 0, 0))
    P_2_health_text = HEALTH_FONT.render(str(P_2_health) + " :", 1, (0, 0, 0))
    WIN.blit(P_2_health_text, (WIDTH - P_2_health_text.get_width() - 28, 8))
    WIN.blit(P_1_health_text, (28, 8))

    WIN.blit(PLAYER_1, (P_1.x, P_1.y))
    WIN.blit(PLAYER_2, (P_2.x, P_2.y))

    for bullet in P_1_bullets:
        pygame.draw.rect(WIN, BROWN, bullet)

    for bullet in P_2_bullets:
        pygame.draw.rect(WIN, OLIVE, bullet)

    pygame.display.update()  # necessary to update what is seen on the window


def P_1_handle_movements(keys_pressed, P_1):
    if keys_pressed[pygame.K_q] and P_1.x - VEL > 0:  # LEFT (avoiding going off the screen on the left
        P_1.x -= VEL
    if keys_pressed[pygame.K_d] and P_1.x + VEL < 410:  # RIGHT
        P_1.x += VEL
    if keys_pressed[pygame.K_z] and P_1.y - VEL > 0:  # UP
        P_1.y -= VEL
    if keys_pressed[pygame.K_s] and P_1.y + VEL < 410:  # DOWN
        P_1.y += VEL


def P_2_handle_movements(keys_pressed, P_2):
    if keys_pressed[pygame.K_LEFT] and P_2.x - VEL > 450:  # LEFT
        P_2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and P_2.x + VEL < 860:  # RIGHT
        P_2.x += VEL
    if keys_pressed[pygame.K_UP] and P_2.y - VEL > 0:  # UP
        P_2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and P_2.y + VEL < 410:  # DOWN
        P_2.y += VEL


def handle_bullets(P_1_bullets, P_2_bullets, P_1, P_2):  # check bullets collision
    for bullet in P_1_bullets:
        bullet.x += BULLET_VEL
        if P_2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(P_2_HIT))
            P_1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            P_1_bullets.remove(bullet)

    for bullet in P_2_bullets:
        bullet.x -= BULLET_VEL
        if P_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(P_1_HIT))
            P_2_bullets.remove(bullet)
        elif bullet.x < 0:
            P_2_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (76, 48, 5))
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, 150 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(7000)  # Winning text will be showed for 5s before restarting the game


def main():
    P_1 = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)  # to draw rectangles where the players are going to be
    P_2 = pygame.Rect(800, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    P_1_bullets = []
    P_2_bullets = []

    P_2_health = 10
    P_1_health = 10

    clock = pygame.time.Clock()  # FPS related
    run = True
    while run:
        clock.tick(
            FPS)  # it will make sure we run this while loop 60 times per seconds, for the game to be formated to one speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(
                        P_1_bullets) < MAX_BULLETS:  
                    bullet = pygame.Rect(P_1.x + P_1.width, P_1.y + P_1.height // 2 - 2, 10, 5)
                    P_1_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_0 and len(
                        P_2_bullets) < MAX_BULLETS:  
                    bullet = pygame.Rect(P_2.x, P_2.y + P_2.height // 2 - 2, 10, 5)
                    P_2_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == P_2_HIT:
                P_2_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == P_1_HIT:
                P_1_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if P_2_health <= 0:
            P_2_health_text = HEALTH_FONT.render(str(P_2_health) + " :", 1, (0, 0, 0))
            WIN.blit(P_2_health_text, (WIDTH - P_2_health_text.get_width() - 28, 8))
            winner_text = "Pooper 1 Wins!"
        if P_1_health <= 0:
            P_1_health_text = HEALTH_FONT.render(": 0", 1, (0, 0, 0))
            WIN.blit(P_1_health_text, (28, 8))
            winner_text = "Pooper 2 Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break  # Someone won

        keys_pressed = pygame.key.get_pressed()  # to press multiple keys at a time
        P_1_handle_movements(keys_pressed, P_1)
        P_2_handle_movements(keys_pressed, P_2)

        handle_bullets(P_1_bullets, P_2_bullets, P_1, P_2)

        draw_window(P_1, P_2, P_1_bullets, P_2_bullets, P_1_health, P_2_health)

    main()


if __name__ == "__main__": 
    main()
