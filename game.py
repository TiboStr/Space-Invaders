import pygame

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("  Space Invaders")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
game_loop = True

actor_size = int(width / 20)

player_image = pygame.transform.scale(pygame.image.load("images/player.png"), (actor_size, actor_size))
player_x = width / 2
player_y = height * 0.85

player_speed = width / 350


def player(x, y):
    screen.blit(player_image, (x, y))


player_x_change = 0
player_y_change = 0

while game_loop:

    image = pygame.transform.scale(pygame.image.load("images/space.jfif"), (width, height))
    screen.blit(image, (0, 0))
    player(player_x, player_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        elif event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                player_x_change = {pygame.K_LEFT: -player_speed, pygame.K_RIGHT: player_speed}.get(event.key)

            elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                player_y_change = {pygame.K_UP: -player_speed, pygame.K_DOWN: player_speed}.get(event.key)

        elif event.type == pygame.KEYUP and event.key in {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}:
            player_x_change, player_y_change = 0, 0

    if 0 <= player_x + player_x_change <= width - actor_size and 0 <= player_y + player_y_change <= height - actor_size:
        player_x += player_x_change
        player_y += player_y_change
        player(player_x, player_y)

    pygame.display.update()


class Game:
    screen = None
    enemies = []

    def __init__(self, width, height):
        self.width = width
        self.height = height


print("hello world")
g = Game(2, 4)
