from src.constants import *
from src.utils import load_image_to_scale
import pygame


class Widget(pygame.sprite.Sprite):
    def __init__(self, game, live_image, dead_image, rect, label):
        self.groups = (game.widgets,)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.live_image = live_image
        self.dead_image = dead_image
        self.image = dead_image
        self.rect = pygame.Rect(rect)
        self.label = label
        self.live = False
        self.active = False
        self.ticks = pygame.time.get_ticks()
        self.cooldown = 200

    def select(self, now):
        if self.game.mouse.hover(self.rect, GUI_DEST) and not self.live:
            self.image = self.live_image
            self.active = True
            if now - self.ticks > self.cooldown and self.game.mouse.is_pressed:
                self.ticks = pygame.time.get_ticks()
                self.live = True
                self.active = False
                self.image = self.live_image
        if not self.game.mouse.hover(self.rect, GUI_DEST) and not self.live:
            self.active = False
            self.image = self.dead_image

    def deselect(self, now):
        if self.game.mouse.hover(self.rect, GUI_DEST) and self.live:
            if now - self.ticks > self.cooldown and self.game.mouse.is_pressed:
                self.ticks = pygame.time.get_ticks()
                self.live = False
                self.image = self.dead_image
                if self.label == 'play':
                    self.game.evolving = False

    def update(self):
        now = pygame.time.get_ticks()
        self.select(now)
        self.deselect(now)


class WidgetAction(object):
    def __init__(self, game):
        self.game = game
        self.widgets = game.widgets
        self.ticks = pygame.time.get_ticks()
        self.cooldown = 1000

    def draw_context(self):
        for widget in self.widgets:
            if widget.active:
                x, y = widget.rect.midbottom
                y += 5  # add padding in pixels
                self.game.draw_text.set_font(self.game.font_name, FONT_SIZE)
                self.game.draw_text.render(widget.label, self.game.color.white)
                self.game.draw_text.set_rect((x, y), 'center')
                self.game.draw_text.blit(self.game.screen_gui)

    def kill(self, widget):
        now = pygame.time.get_ticks()
        if now - self.ticks > self.cooldown:
            self.ticks = pygame.time.get_ticks()
            widget.active = False
            widget.live = False

    # there's an expected bug here where the event keys
    # don't match up with the mouse/widget based events
    def event(self, label):
        for widget in self.widgets:
            if widget.label == label:
                widget.live = not widget.live
                if widget.image == widget.dead_image:
                    widget.image = widget.live_image
                else:
                    widget.image = widget.dead_image

    def update(self):
        for widget in self.widgets:
            if widget.live:
                if widget.label == 'play':
                    self.game.evolving = not self.game.evolving
                elif widget.label == 'reset':
                    self.kill(widget)
                    self.game.running = False
                    self.game.evolving = False
                elif widget.label == 'open':
                    self.kill(widget)
                elif widget.label == 'save':
                    self.kill(widget)


class Gui(object):
    def __init__(self, game):
        self.game = game
        self.play_dead = load_image_to_scale(game.image_gui_path, 'play-outline.png', 32)
        self.play_live = load_image_to_scale(game.image_gui_path, 'play-full.png', 32)
        self.save_dead = load_image_to_scale(game.image_gui_path, 'save-text.png', 32)
        self.save_live = load_image_to_scale(game.image_gui_path, 'save-block.png', 32)
        self.open_dead = load_image_to_scale(game.image_gui_path, 'open-basic.png', 32)
        self.open_live = load_image_to_scale(game.image_gui_path, 'open-arrow.png', 32)
        self.reset_dead = load_image_to_scale(game.image_gui_path, 'box-lid.png', 32)
        self.reset_live = load_image_to_scale(game.image_gui_path, 'box-full.png', 32)

    def load_widgets(self):
        center = GUI_WIDTH / 2
        play_rect = pygame.Rect(center - (32 * 4) + 10 + 32, 15, 32, 32)
        #save_rect = pygame.Rect(center - (32 * 3) + 20 + 32, 15, 32, 32)
        #open_rect = pygame.Rect(center - (32 * 2) + 30 + 32, 15, 32, 32)
        reset_rect = pygame.Rect(center - (32 * 1) + 40 + 32, 15, 32, 32)
        Widget(self.game, self.play_live, self.play_dead, play_rect, 'play')
        #Widget(self.game, self.save_live, self.save_dead, save_rect, 'save')
        #Widget(self.game, self.open_live, self.open_dead, open_rect, 'open')
        Widget(self.game, self.reset_live, self.reset_dead, reset_rect, 'reset')

