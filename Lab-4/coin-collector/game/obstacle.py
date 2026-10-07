"""
Obstacle: a static rectangular hazard inside the play area.
"""

import pygame


class Obstacle:
    def __init__(self, x, y, width, height, color=(190, 70, 70)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def get_rect(self):
        return self.rect
