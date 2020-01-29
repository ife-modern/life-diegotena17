from src.constants import BIT_DEPTH
import pygame


class Mouse(dict):
    def __init__(self):
        super(Mouse, self).__init__({
            'x': 0,
            'y': 0,
            'position': None,
            'button': None,
            'is_pressed': False,
            'left': 1,
            'mid': 2,
            'right': 3,
            'scroll_up': 4,
            'scroll_down': 5,
            'get_pressed': pygame.mouse.get_pressed,
            'get_pos': pygame.mouse.get_pos,
            'get_rel': pygame.mouse.get_rel,
        })

    # Make dictionary keys available as attributes
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def __delattr__(self, key):
        del self[key]

    def reset(self):
        """Reset mouse object to its default state"""
        self.x = 0
        self.y = 0
        self.position = None
        self.button = None
        self.is_pressed = False

    def motion(self, event):
        """Handle mouse motion events"""
        if event.type == pygame.MOUSEMOTION:
            self.position = event.pos
            self.x, self.y = event.pos

    def button_down(self, event):
        """Handle mouse button down events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_pressed = True
            self.button = event.button
            self.start_x, self.start_y = event.pos

    def button_up(self, event):
        """Handle mouse button up events"""
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False
            self.button = event.button
            self.end_x, self.end_y = event.pos

    def hover(self, rect, offset=(0, 0)):
        if self.x and self.y:
            active_x = rect.x < self.x - offset[0] < rect.x + BIT_DEPTH
            active_y = rect.y < self.y - offset[1] < rect.y + BIT_DEPTH
            return active_x and active_y
        return False
