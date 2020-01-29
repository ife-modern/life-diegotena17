import pygame


class DrawText(object):

    def __init__(self, antialias=True):
        self.font = None
        self.text_surface = None
        self.text_rect = None
        self.antialias = antialias

    def set_font(self, name, size):
        self.font = pygame.font.Font(name, size)

    def render(self, text, color):
        self.text_surface = self.font.render(text, self.antialias, color)

    def set_rect(self, position, align='topleft'):
        self.text_rect = self.text_surface.get_rect(**{align: position})

    def blit(self, surface):
        surface.blit(self.text_surface, self.text_rect)
