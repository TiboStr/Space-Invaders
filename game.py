import math
import random

import pygame


class Game:

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption("  Space Invaders")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()

        self.actor_size = int(width / 20)
        self.actor_base_speed = width / 300
        self.player = Player(self, self.width / 2, self.height * 0.85, self.actor_base_speed)

        self.generator = Generator(self)

        self.game_loop = True
        self.enemies = []
        self.bullets = []

    def game(self):
        while self.game_loop:
            image = pygame.transform.scale(pygame.image.load("images/space.jfif"), (self.width, self.height))
            self.screen.blit(image, (0, 0))

            self.generator.generate_enemies()

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RIGHT]:
                self.player.move_right()
            elif pressed_keys[pygame.K_LEFT]:
                self.player.move_left()
            elif pressed_keys[pygame.K_UP]:
                self.player.move_up()
            elif pressed_keys[pygame.K_DOWN]:
                self.player.move_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_loop = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bullets.append(
                        Bullet(self, self.player.x + self.actor_size / 2, self.player.y, self.actor_base_speed * 6))

            for enemy in self.enemies:
                enemy.act()
            for bullet in self.bullets:
                bullet.act()

            self.player.draw()
            pygame.display.update()
            self.clock.tick(60)


class Generator:
    def __init__(self, game):
        self.game = game
        self.rate = 10

    def generate_enemies(self):
        number = random.randint(1, int(self.rate))
        if number % 11 == number % 6 == 0:
            self.game.enemies.append(AlienEasy(self.game))
        if number % 23 == number % 9 == 0:
            self.game.enemies.append(AlienMedium(self.game))
        if number > 100 and number % 17 == number % 5 == 0:
            self.game.enemies.append(AlienHard(self.game))
        print(number)
        self.rate += 0.25


class WorldObject:
    def __init__(self, game, x, y, speed):
        self.game = game
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, img):
        self.game.screen.blit(img, (self.x, self.y))


class Player(WorldObject):

    def __init__(self, game, x, y, speed):
        super().__init__(game, x, y, speed)
        self.player_image = pygame.transform.scale(pygame.image.load("images/player.png"),
                                                   (game.actor_size, game.actor_size))

    def draw(self):
        super().draw(self.player_image)

    def move_left(self):
        self.x -= self.speed if self.x - self.speed >= 0 else self.x

    def move_right(self):
        self.x = self.x + self.speed if self.x + self.speed <= self.game.width - self.game.actor_size else self.x

    def move_down(self):
        self.y = self.y + self.speed if self.y + self.speed <= self.game.height - self.game.actor_size else self.y

    def move_up(self):
        self.y -= self.speed if self.y - self.speed >= 0 else self.y


class Bullet(WorldObject):

    def __init__(self, game, x, y, speed):
        super().__init__(game, x, y, speed)
        self.width = 1
        self.height = self.game.actor_size / 4

    def act(self):
        self.move()
        if self in self.game.bullets:
            self.draw()
            self.check_hits()

    def move(self):
        self.y -= self.speed
        if self.y <= 0 - self.height:
            self.game.bullets.remove(self)

    def draw(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))

    def check_hits(self):
        for enemy in self.game.enemies:
            if self.y <= enemy.y + self.game.actor_size and enemy.x <= self.x <= enemy.x + self.game.actor_size:
                print("HIT")
                enemy.lives -= 1
                if enemy.lives == 0:
                    self.game.enemies.remove(enemy)
                self.game.bullets.remove(self)
                break


class Alien(WorldObject):

    def __init__(self, game, x, y, speed, lives):
        super().__init__(game, x, y, speed)
        self.speed_x = speed
        self.lives = lives

    def move(self):
        if not (0 <= self.x + self.speed <= self.game.width):
            self.speed_x *= -1
            self.y += self.speed
        self.x += self.speed_x

    def check_for_collision_with_player(self):
        if math.sqrt((self.x - self.game.player.x) ** 2 + (self.y - self.game.player.y) ** 2) < \
                math.sqrt(self.game.actor_size ** 2 + self.game.actor_size):

            self.game.game_loop = False
            print("GAME OVER")


class AlienHard(Alien):
    images = [pygame.image.load(f"images/alienHARD_{i}.png") for i in range(1, 11)]

    def __init__(self, game):
        super().__init__(game, random.randint(0, game.width), random.randint(0, math.ceil(game.height * 0.05)),
                         game.actor_base_speed * random.randint(1, 3), 10)

    def act(self):
        self.move()
        self.draw()
        self.check_for_collision_with_player()

    def get_image(self):
        return pygame.transform.scale(self.images[self.lives - 1],
                                      (self.game.actor_size, self.game.actor_size))

    def draw(self):
        super().draw(self.get_image())


class AlienMedium(Alien):
    images = [pygame.image.load(f"images/alienMEDIUM_{i}.png") for i in range(1, 7)]

    def __init__(self, game):
        super().__init__(game, random.randint(0, game.width), random.randint(0, math.ceil(game.height * 0.05)),
                         game.actor_base_speed * random.randint(1, 2), 6)

    def act(self):
        self.move()
        self.draw()
        self.check_for_collision_with_player()

    def get_image(self):
        return pygame.transform.scale(self.images[self.lives - 1],
                                      (self.game.actor_size, self.game.actor_size))

    def draw(self):
        super().draw(self.get_image())


class AlienEasy(Alien):
    images = [pygame.image.load(f"images/alienEASY_{i}.png") for i in range(1, 4)]

    def __init__(self, game):
        super().__init__(game, random.randint(0, game.width), random.randint(0, math.ceil(game.height * 0.05)),
                         game.actor_base_speed * random.randint(1, 2), 3)

    def act(self):
        self.move()
        self.draw()
        self.check_for_collision_with_player()

    def get_image(self):
        return pygame.transform.scale(self.images[self.lives - 1],
                                      (self.game.actor_size, self.game.actor_size))

    def draw(self):
        super().draw(self.get_image())


if __name__ == "__main__":
    g = Game(1280, 720)
    g.game()
