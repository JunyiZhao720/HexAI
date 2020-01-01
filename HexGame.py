import pygame
import os
from enum import Enum

pygame.init()

game_dim = 10
chess_size = (100, 100)

board = (6 * [0], 7 * [0], 8 * [0], 9 * [0], 10 * [0], 11 * [0], 10 * [0], 9 * [0], 8 * [0], 7 * [0], 6 * [0])
run = True

chess_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'blue.png')), chess_size)

]

def draw_game():
    win = pygame.display.set_mode((456, 352))
    win.fill((0, 0, 0))
    hexboard = HexBoard()
    hexboard.draw_board(win, 28, 128)
    pygame.display.update()

class ChessType(Enum):
    EMPTY = 0
    ONE = 1
    TWO = 2

class Chess:
    row_offset = 0
    col_offset = 0

    def __init__(self, index, type = ChessType.EMPTY):
        self.index = index
        self.type = type

    def position(self):
        return self.index // game_dim, self.index % game_dim

    def draw(self, win):
        x, y = self.position()
        win.blit(chess_imgs[self.type.value], (x, y))

class HexBoard:

    def __init__(self, red=255, green=248, blue=220):
        self.r = red
        self.g = green
        self.b = blue

    def draw_board(self, win, off_x, off_y):
        # for i, col in enumerate(board):
        #     col_size = len(col)
        #     for j, piece in enumerate(col):
        #         draw_hex(Surface, i * 40 + off_x, j * 32 + off_y - col_size * 16 + 64,
        #                  (self.r - 14 * ((col_size + j) % 3), self.g - 45 * ((col_size + j) % 3),
        #                   self.b - 49 * ((col_size + j) % 3)))
        #         color = 25 + i % 2 * 195
        #         draw_piece(Surface, i * 40 + off_x, j * 32 + off_y - col_size * 16 + 64, (color - 20, color, color))
        a = Chess(0)
        a.draw(win)


def draw_hex(Surface, x, y, rgb):
    pygame.draw.polygon(Surface, rgb, [(x - 28, y), (x - 12, y + 16), (x + 12, y + 16), (x + 28, y), (x + 12, y - 16),
                                       (x - 12, y - 16)], 0)


def draw_piece(Surface, x, y, rgb):
    pygame.draw.circle(Surface, rgb, (x, y), 7)


while run:
    pygame.time.delay(1)
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
pygame.quit()