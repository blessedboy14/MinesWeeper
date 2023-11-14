import random
import pygame
import datetime
from settings import *
from tile import Tile
from tile_type import TileType
from tile_val import TileVal
from debug import debug


class Board:
    def __init__(self, width, height, mines):
        if width * height - 10 <= mines:
            raise(ValueError("A lot of mines"))
        self._width = width
        self._height = height
        self._actual_width = self._width - 1
        self._actual_height = self._height - 1
        self._mines = mines
        self._board = self._generate_board()
        self._assign_vals()
        self.is_game_ended = False
        self.is_game_over = False
        self._opened = 0
        self._sprites = {key: pygame.image.load(tile_data[key]['graphic']).convert_alpha() for key in tile_data.keys()}
        self._tile_size = next(iter(self._sprites.values())).get_rect(topleft=(0, 0))
        self._display_surface = None
        self._start_pos = pygame.math.Vector2(0, 1)
        self._count = 0
        self._start_time = pygame.time.get_ticks()
        self._font = pygame.font.Font(None, 36)
        self._flags_on_mines = 0
        self._flags = 0
        self._end_time = self._start_time
        max_milliseconds = 999
        max_time_str = "Time: 00:00:00:" + str(max_milliseconds).zfill(3)
        text_surface_width, text_surface_height = self._font.size(max_time_str)
        self.text_surface = pygame.Surface((text_surface_width, text_surface_height))

    def show_matr(self):
        for i in range(self._width):
            for j in range(self._height):
                print(self._board[i][j].get_tile_val().value, end=" ")
            print()

    def _get_mines_pos(self):
        positions = []
        while len(positions) < self._mines:
            row = random.randint(0, self._actual_width)
            col = random.randint(0, self._actual_height)
            if (row*self._actual_height)+col not in positions:
                positions.append(row*self._actual_height+col)
        return positions


    def _generate_board(self):
        # mines_pos = [random.randint(0, self._actual_width * self._actual_height + 1) for _ in range(self._mines)]
        mines_pos = self._get_mines_pos()
        board = [[Tile(TileType.CLOSED, i * TILESIZE, j * TILESIZE, TileVal.ZERO) for j in range(self._height)] for i in range(self._width) ]
        for i in range(self._width):
            for j in range(self._height):
                if (i*self._actual_height + j) in mines_pos:
                    board[i][j].make_mine()
        return board

    def _assign_vals(self):
        for i in range(self._width):
            for j in range(self._height):
                if not self._board[i][j].is_mine():
                    self._board[i][j].set_val(self._count_mines(i, j))

    def _count_mines(self, x, y):
        min_x = max(x-1, 0)
        max_x = min(x+1, self._actual_width)
        min_y = max(y-1, 0)
        max_y = min(y+1, self._actual_height)
        mines = 0
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                tile = self._board[i][j]
                if tile.is_mine():
                    mines += 1
        return mines

    def open_tile(self, x, y):
        tile = self._board[x][y]
        if tile.is_mine():
            self._board[x][y].open_tile()
            self._opened += 1
            self.is_game_over = True
            self._end_time = pygame.time.get_ticks()
        elif tile.is_zero():
            self._open_tile_recursively(x, y)
        else:
            self._board[x][y].open_tile()
            self._opened += 1

    def _open_tile_recursively(self, x, y):
        min_x = max(x-1, 0)
        max_x = min(x+1, self._actual_width)
        min_y = max(y-1, 0)
        max_y = min(y+1, self._actual_height)
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                tile = self._board[i][j]
                if tile.is_zero() and tile.is_closed():
                    self._opened += 1
                    tile.open_tile()
                    self._open_tile_recursively(i, j)
                elif tile.is_closed():
                    self._opened += 1
                    tile.open_tile()

    def update_board(self):
        if not self.is_game_ended:
            if self._flags == self._flags_on_mines and self._flags == self._mines:
                self._end_time = pygame.time.get_ticks()
                self.is_game_ended = True
            if self._opened >= (self._width*self._height) - self._mines:
                self.is_game_ended = True
                self._end_time = pygame.time.get_ticks()
        self._display_surface = pygame.display.get_surface()
        for i in range(self._width):
            for j in range(self._height):
                tile = self._board[i][j]
                x = i * TILESIZE
                y = j * TILESIZE
                self._tile_size = self._sprites['closed'].get_rect(topleft=(x, y)).topleft + self._start_pos
                if tile.is_flag():
                    self._display_surface.blit(self._sprites['flag'], self._tile_size)
                elif tile.is_open():
                    if tile.is_zero():
                        self._display_surface.blit(self._sprites['opened'], self._tile_size)
                    elif tile.is_mine():
                        self._display_surface.blit(self._sprites['mine'], self._tile_size)
                    else:
                        self._display_surface.blit(self._sprites[str(tile.get_tile_val().value)], self._tile_size)
                else:
                    self._display_surface.blit(self._sprites['closed'], self._tile_size)
        if self.is_game_over:
            debug("Game over")
        elif self.is_game_ended:
            debug("You win")
        self._update_time(True) if self.is_game_ended or self.is_game_over else self._update_time()

    def _update_time(self, is_end=False):
        end_time = self._end_time if is_end else pygame.time.get_ticks()
        elapsed_time = end_time - self._start_time
        hours = int(elapsed_time / 3600000)
        minutes = int((elapsed_time % 3600000) / 60000)
        seconds = int((elapsed_time % 60000) / 1000)
        milliseconds = elapsed_time % 1000
        hours_str = "{:02d}".format(hours)
        minutes_str = "{:02d}".format(minutes)
        seconds_str = "{:02d}".format(seconds)
        milliseconds_str = "{:03d}".format(milliseconds)
        timer_text = f"Time: {hours_str}:{minutes_str}:{seconds_str}:{milliseconds_str}"
        text_surface = self._font.render(timer_text, True, pygame.Color("black"))
        self.text_surface.fill(WATER_COLOR)
        self.text_surface.blit(text_surface, (0, 0))
        self._display_surface.blit(self.text_surface, (WIDTH/2 - self.text_surface.get_width()/2, 360))

    def process_left_click(self, mouse):
        if not self.is_game_over:
            for i in range(self._width):
                for j in range(self._height):
                    if self._board[i][j].get_rect().collidepoint(mouse):
                        self.open_tile(i, j)

    def process_right_click(self, mouse):
        if not self.is_game_over:
            for i in range(self._width):
                for j in range(self._height):
                    if self._board[i][j].get_rect().collidepoint(mouse):
                        self._put_a_flag(i, j)

    def _put_a_flag(self, x, y):
        tile = self._board[x][y]
        if tile.is_closed():
            if tile.is_flag():
                self._flags_on_mines += -1 if tile.is_mine() else 0
                tile.unput_flag()
                self._flags -= 1
            else:
                self._flags += 1
                self._flags_on_mines += 1 if tile.is_mine() else 0
                tile.put_flag()

    def write_time_to_file(self):
        if not self.is_game_over and self.is_game_ended:
            with open("leaderboard.txt", "r+") as file:
                lines = file.readlines()
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                spent = datetime.timedelta(milliseconds=self._end_time - self._start_time)
                hours, minutes, seconds, milliseconds = self._get_time_vals(spent)
                formatted_diff = "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, milliseconds)
                file.write(f"End in: {formatted_datetime}, spent time: {formatted_diff}\n")
                file.seek(0)
                lines = file.readlines()
                lines = sorted(lines, key=self._sort_file_line)
            with open("leaderboard.txt", 'w') as file:
                file.writelines(lines[:10] if len(lines) >= 10 else lines)

    def _sort_file_line(self, line):
        time_str = ":".join(line.split(':')[-3:]).strip()
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S.%f')
        return time_obj

    def _get_time_vals(self, spent):
        hours = spent.seconds // 3600
        minutes = (spent.seconds % 3600) // 60
        seconds = (spent.seconds % 3600) % 60
        milliseconds = spent.microseconds // 1000
        return hours, minutes, seconds, milliseconds
