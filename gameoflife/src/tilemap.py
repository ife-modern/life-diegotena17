from pygame import Surface
from pytmx.util_pygame import load_pygame
from pytmx.pytmx import TiledTileLayer


class TiledMap(object):
    def __init__(self, filename):
        self.tmxdata = load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        width = x * self.tmxdata.tilewidth
                        height = y * self.tmxdata.tileheight
                        surface.blit(tile, (width, height))

    def make_map(self):
        surface = Surface((self.width, self.height))
        self.render(surface)
        return surface
