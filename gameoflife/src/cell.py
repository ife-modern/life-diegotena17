from src.constants import *
from src.utils import load_image_to_scale
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, game, rect):
        self.groups = (game.cells,)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dead_cell = load_image_to_scale(
            game.image_cell_path, 'dead_cell.png', BIT_DEPTH
        )
        self.live_cell = load_image_to_scale(
            game.image_cell_path, 'live_cell.png', BIT_DEPTH
        )
        self.image = self.dead_cell
        self.rect = pygame.Rect(rect)
        self.live = False
        self.neighbours = []
        self.ticks = pygame.time.get_ticks()
        self.cooldown = 200
        self.id = 0

    def select(self, now):
        if self.game.mouse.hover(self.rect, GRID_DEST) and not self.live:
            self.image = self.live_cell
            if now - self.ticks > self.cooldown and self.game.mouse.is_pressed:
                self.ticks = pygame.time.get_ticks()
                self.live = True
                self.image = self.live_cell
        if not self.game.mouse.hover(self.rect, GRID_DEST) and not self.live:
            self.image = self.dead_cell

    def deselect(self, now):
        if self.game.mouse.hover(self.rect, GRID_DEST) and self.live:
            if now - self.ticks > self.cooldown and self.game.mouse.is_pressed:
                self.ticks = pygame.time.get_ticks()
                self.live = False
                self.image = self.dead_cell

    def update(self):
        now = pygame.time.get_ticks()
        self.select(now)
        self.deselect(now)
