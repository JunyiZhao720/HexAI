import pygame
import pygame.gfxdraw
import os
from enum import Enum
import math

pygame.init()

game_dim = 7
chess_size = (50, 50)
clock = pygame.time.Clock()
win = pygame.display.set_mode((1440, 920))

run = True

chess_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'empty.png')), chess_size),
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'blue.png')), chess_size),
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'red.png')), chess_size)
]

border_imgs = [
    None,
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'blue-border.png')), chess_size),
    pygame.transform.scale(pygame.image.load(os.path.join('img', 'red-border.png')), chess_size)
]

class ChessType(Enum):
    EMPTY = 0
    ONE = 1
    TWO = 2

class Chess:
    y_offset = 5
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
            if row <= game_dim - 1:
                offset += 1
            else:
                offset -= 1

        return row, remaining           # row, col

    def polygon(self):
        a = (int(self.x + chess_size[0]/2), self.y)
        b = (self.x + chess_size[0], int(self.y + math.sqrt(3)/6 * chess_size[0]))
        c = (self.x + chess_size[0], int(self.y + math.sqrt(3)/2 * chess_size[0]))
        d = (int(self.x + chess_size[0]/2), int(self.y + 2 * math.sqrt(3)/3 * chess_size[0]))
        e = (self.x, int(self.y + math.sqrt(3)/2 * chess_size[0]))
        f = (self.x, int(self.y + math.sqrt(3)/6 * chess_size[0]))

        return [a, b, c, d, e, f]

    def draw(self, Surface):
        row, col = self.position()
        total_lines = 2 * game_dim - 1

        x_space_offset = (game_dim // 2) * (Chess.x_offset + chess_size[0]) + (chess_size[0] + Chess.x_offset) // 2
        if row <= game_dim - 1:
            x_space_offset -= row * ((chess_size[0] + Chess.x_offset) // 2)
        else:
            x_space_offset -= (total_lines - row - 1) * ((chess_size[0] + Chess.x_offset) // 2)

        x_space_offset += Surface.get_width() // 3
        y_space_offset = Chess.y_offset + chess_size[1]
        y = y_space_offset + row * (Chess.y_offset + chess_size[1])
        x = x_space_offset + col * (Chess.x_offset + chess_size[0])

        self.x = x
        self.y = y

        # Surface.blit(chess_imgs[self.type.value], (x, y))
        # pygame.draw.polygon(Surface, (0, 0, 0), self.polygon(), 5)
        if self.type == ChessType.EMPTY:
            pygame.gfxdraw.aapolygon(Surface, self.polygon(), (0, 0, 0))
        elif self.type == ChessType.ONE:
            pygame.gfxdraw.filled_polygon(Surface, self.polygon(), (0, 0, 64))
        else:
            pygame.gfxdraw.filled_polygon(Surface, self.polygon(), (64, 0, 0))
class HexBoard:

    def __init__(self, red=255, green=248, blue=220):
        self.r = red
        self.g = green
        self.b = blue
        self.chess_list = []


    def draw_boder(self, Surface):
        for chess in self.chess_list:
            row, col = chess.position()
            if col == 0:
                x = chess.x - (Chess.x_offset + chess_size[0])
                y = chess.y
                if row < game_dim - 1:
                    Surface.blit(border_imgs[ChessType.ONE.value], (x, y))
                if row > game_dim - 1:
                    Surface.blit(border_imgs[ChessType.TWO.value], (x, y))

    def draw_board(self, Surface):

        num = game_dim ** 2
        for i in range(num):
            self.chess_list.append(Chess(i))
        self.chess_list[3].type = ChessType.ONE
        self.chess_list[8].type = ChessType.TWO

        for i in range(num):
            self.chess_list[i].draw(Surface)

        self.draw_boder(Surface)


hexboard = HexBoard()

def draw_game():
    win.fill((128, 128, 128))
    hexboard.draw_board(win)
    pygame.display.update()


while run:
    clock.tick(1)
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
pygame.quit()