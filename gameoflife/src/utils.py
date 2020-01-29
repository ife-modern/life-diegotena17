import pygame
import os


def load_image_to_scale(path, filename, bitdepth):
    return pygame.transform.scale(
        pygame.image.load(
            os.path.join(path, filename)
        ).convert_alpha(),
        (bitdepth, bitdepth)
    )
