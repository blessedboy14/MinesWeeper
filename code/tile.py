import pygame.display
from settings import *
from tile_type import TileType
from tile_val import TileVal


class Tile(pygame.sprite.Sprite):
    def __init__(self, tType, x, y, val):
        super().__init__()
        self._tile_type = tType
        self._x_pos = x
        self._y_pos = y
        self.rect = pygame.rect.Rect(self._x_pos, self._y_pos, TILESIZE, TILESIZE)
        self._val = val
        self.hitbox = self.rect.inflate(INFLATE_VAL, INFLATE_VAL)

    def open_tile(self):
        self._tile_type = TileType.OPEN

    def is_open(self):
        return self._tile_type == TileType.OPEN

    def get_tile_val(self):
        return self._val

    def is_flag(self):
        return self._tile_type == TileType.FLAG

    def put_flag(self):
        self._tile_type = TileType.FLAG

    def unput_flag(self):
        self._tile_type = TileType.CLOSED

    def make_flag(self):
        self._tile_type = TileType.FLAG

    def make_mine(self):
        self._val = TileVal.MINE

    def is_mine(self):
        return self._val == TileVal.MINE

    def is_closed(self):
        return not self._tile_type == TileType.OPEN

    def set_val(self, num):
        self._val = TileVal(num)

    def is_zero(self):
        return self._val == TileVal.ZERO

    def set_rect(self, rect):
        self.rect = rect
        self.hitbox = self.rect.inflate(-2, -2)

    def get_rect(self):
        return self.hitbox