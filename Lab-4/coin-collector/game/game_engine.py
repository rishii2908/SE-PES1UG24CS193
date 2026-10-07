"""
GameEngine: owns the player, coins, and obstacles.

The round lasts 30 seconds. Coin collection removes collected coins so each
coin can only award points once. Obstacles use a collision latch so a single
continuous touch only costs one life.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
ROUND_DURATION = 30
COIN_TYPES = [
    ("bronze", 1, (176, 112, 64)),
    ("silver", 3, (192, 192, 192)),
    ("gold", 5, (230, 190, 60)),
]


class GameEngine:
    def __init__(self):
        self._reset_round()

    def _reset_round(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.obstacles = self._create_obstacles()
        self.score = 0
        self.lives = 3
        self._obstacle_collision_active = False
        self._round_start_ticks = pygame.time.get_ticks()
        self.remaining_time = ROUND_DURATION
        self.game_over = False

    def restart(self):
        self._reset_round()

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        _, value, color = random.choice(COIN_TYPES)
        return Coin(x=x, y=y, radius=12, value=value, color=color)

    def _create_obstacles(self):
        # All rectangles are fully inside the 700x500 play area.
        positions = [
            (100, 100, 150, 25),
            (450, 100, 150, 25),
            (100, 350, 150, 25),
            (450, 350, 150, 25),
        ]
        return [Obstacle(*position) for position in positions]

    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_r] and self.game_over:
            self.restart()
            return

        if self.game_over:
            return

        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if self.game_over:
            return

        elapsed = (pygame.time.get_ticks() - self._round_start_ticks) / 1000
        self.remaining_time = max(0, ROUND_DURATION - elapsed)
        if self.remaining_time <= 0:
            self.game_over = True
            return

        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
        self.coins = [coin for coin in self.coins if coin not in collected]

        touching_obstacle = any(
            self.player.get_rect().colliderect(obstacle.get_rect())
            for obstacle in self.obstacles
        )

        if touching_obstacle and not self._obstacle_collision_active:
            self.lives -= 1
            self._obstacle_collision_active = True
        elif not touching_obstacle:
            self._obstacle_collision_active = False

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 38))
        renderer.draw_text(surface, font, f"Time: {int(self.remaining_time):02d}", (10, 66))

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Final Score: {self.score} - Press R to Restart",
            )
