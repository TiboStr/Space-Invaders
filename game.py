import pygame

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("  Space Invaders")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
game_loop = True

player_image = pygame.transform.scale(pygame.image.load("images/player.png"), (int(width/20), int(width/20)))
player_x = width / 2
player_y = height * 0.85


def player():
    screen.blit(player_image, (player_x, player_y))


while game_loop:

    image = pygame.transform.scale(pygame.image.load("images/space.jfif"), (width, height))
    screen.blit(image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    player()
    pygame.display.update()


class Game:
    screen = None
    enemies = []

    def __init__(self, width, height):
        self.width = width
        self.height = height


print("hello world")
g = Game(2, 4)
