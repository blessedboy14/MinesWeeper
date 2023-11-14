import pygame
import sys
from board import Board
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()
        self.board = Board(9, 9, 10)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.board.process_left_click(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    self.board.process_right_click(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.board.write_time_to_file()
                        self.board = Board(9, 9, 10)
            self.screen.fill(WATER_COLOR)
            self.board.update_board()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    myGame = Game()
    myGame.run()

