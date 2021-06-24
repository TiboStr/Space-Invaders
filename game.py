import pygame
import random


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
        self.player = Player(self, 2, 2, width / 350)
        self.game_loop = True
        self.enemies = []
        self.bullets = []
        # self.game()

        while self.game_loop:
            image = pygame.transform.scale(pygame.image.load("images/space.jfif"), (self.width, self.height))
            self.screen.blit(image, (0, 0))

            if 1 == random.randint(1, 60):
                self.enemies.append(Monster(self, 1, 1, self.width / 300))

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
                        Bullet(self, self.player.x + self.actor_size / 2, self.player.y, self.width / 150))

                # elif event.type == pygame.KEYDOWN:
                #     if event.key in {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}:
                #         {pygame.K_LEFT: (lambda: self.player.move_left()),
                #          pygame.K_RIGHT: (lambda: self.player.move_right()),
                #          pygame.K_UP: (lambda: self.player.move_up()),
                #          pygame.K_DOWN: (lambda: self.player.move_down())}[event.key]()

            for monster in self.enemies:
                monster.move()
                monster.draw()

            for bullet in self.bullets:
                bullet.draw()

            self.player.draw()
            pygame.display.update()
            self.clock.tick(60)


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
        # self.game.screen.blit(self.player_image, (self.x, self.y))

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

    def move(self):
        self.y -= self.speed
        if self.y <= 0 - self.height:
            self.game.bullets.remove(self)
        else:
            self.check_hits()

    def draw(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))
        self.move()

    def check_hits(self):
        for enemy in self.game.enemies:
            print(enemy.y)
            if self.y <= enemy.y + self.game.actor_size and enemy.x <= self.x <= enemy.x + self.game.actor_size:
                print("HIT")
                self.game.enemies.remove(enemy)

                # TODO find out why the bullet is sometimes not in the list
                self.game.bullets.remove(self)
                # else:
                #    print("DIT IS ZO'N MOMENT")
                #    time.sleep(130)
                break


class Monster(WorldObject):

    def __init__(self, game, x, y, speed):
        super().__init__(game, x, y, speed)
        self.monster_image = pygame.transform.scale(pygame.image.load("images/monster.png"),
                                                    (game.actor_size, game.actor_size))
        self.speed_x = speed

    def draw(self):
        super().draw(self.monster_image)

    def move(self):
        if not (0 <= self.x + self.speed <= self.game.width):
            self.speed_x *= -1
            self.y += self.speed
        self.x += self.speed_x

    # TODO testen
    def check_for_collision_with_player(self):
        if ((self.x - self.game.player.x) ** 2 + (self.y - self.game.player.y) ** 2) ** 1 / 2 < (
                self.game.actor_size ** 2 + self.game.actor_size) ** 1 / 2:
            self.game.game_loop = False
            print("GAME OVER")


if __name__ == "__main__":
    Game(1280, 720)
