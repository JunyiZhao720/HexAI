import pygame
import os
from enum import Enum

pygame.init()

game_dim = 10
chess_size = (50, 50)
clock = pygame.time.Clock()

board = (6 * [0], 7 * [0], 8 * [0], 9 * [0], 10 * [0], 11 * [0], 10 * [0], 9 * [0], 8 * [0], 7 * [0], 6 * [0])
run = True

chess_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'blue.png')), chess_size)

]

def draw_game():
    win = pygame.display.set_mode((1920, 1080))
    win.fill((0, 0, 0))
    hexboard.draw_board(win, 28, 128)
    pygame.display.update()

class ChessType(Enum):
    EMPTY = 0
    ONE = 1
    TWO = 2

class Chess:
    y_offset = 10
    x_offset = 10
    start_offset = 0

    def __init__(self, index, type = ChessType.EMPTY):
        self.index = index
        self.type = type
        self.x = 0
        self.y = 0

    def position(self):
        remaining = self.index

        offset = 1
        row = 0
        while(remaining >= offset and offset >= 0):
            remaining -= offset
            row += 1
            if row <= game_dim - 2:
                offset += 1
            else:
                offset -= 1

        return row, remaining

    def draw(self, Surface):
        row, col = self.position()
        print(row, col)
        y = row * (Chess.y_offset + chess_size[1])
        x = col * (Chess.x_offset + chess_size[0])
        # if row % 2 == 0:  # starts from 0
        #     row_even_lines = row
        #     left_offset = game_dim // 2 - row

        # # Set up x
        # if y%2 == 0:                        # start from middle
        #     mid_col = col_num // 2
        #     if x > mid_col:                     # right side
        #         x = (mid_width + chess_size[0] // 2 + Chess.x_offset) + (x - mid_col) * (chess_size[0] + Chess.x_offset)
        #     elif x < mid_col:                 # left
        #         x = (mid_width - chess_size[0] // 2 - Chess.x_offset) - (mid_col - x) * (chess_size[0] + Chess.x_offset)
        #     else:                           # mid
        #         x = mid_width - chess_size[0] // 2
        #
        # else:                               # start from besides
        #     mid_col = col_num // 2
        #     if x >= mid_col:                 # right side
        #         x = mid_width + (x - mid_col) * (chess_size[0] + Chess.x_offset)
        #     else:   # left side
        #         x = mid_width - (x - mid_col) * (chess_size[0] + Chess.x_offset)
        #
        # # Set Up y
        #     y = y * (chess_size[1] + Chess.y_offset)


        Surface.blit(chess_imgs[self.type.value], (x, y))

class HexBoard:

    def __init__(self, red=255, green=248, blue=220):
        self.r = red
        self.g = green
        self.b = blue
        self.chess_list = []



    def draw_board(self, Surface, off_x, off_y):

        num = 81
        for i in range(num):
            self.chess_list.append(Chess(i))
        for i in range(num):
            self.chess_list[i].draw(Surface)


def draw_hex(Surface, x, y, rgb):
    pygame.draw.polygon(Surface, rgb, [(x - 28, y), (x - 12, y + 16), (x + 12, y + 16), (x + 28, y), (x + 12, y - 16),
                                       (x - 12, y - 16)], 0)


def draw_piece(Surface, x, y, rgb):
    pygame.draw.circle(Surface, rgb, (x, y), 7)


hexboard = HexBoard()

while run:
    clock.tick(10)
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
pygame.quit()