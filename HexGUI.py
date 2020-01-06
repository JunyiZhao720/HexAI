import pygame
import pygame.gfxdraw
import os
from enum import Enum
import math
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon

pygame.init()

dim = 7
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

    def __init__(self, row, col, type = ChessType.EMPTY):
        self.type = type
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.changed = True


    def polygon(self):
        a = (int(self.x + chess_size[0]/2), self.y)
        b = (self.x + chess_size[0], int(self.y + math.sqrt(3)/6 * chess_size[0]))
        c = (self.x + chess_size[0], int(self.y + math.sqrt(3)/2 * chess_size[0]))
        d = (int(self.x + chess_size[0]/2), int(self.y + 2 * math.sqrt(3)/3 * chess_size[0]))
        e = (self.x, int(self.y + math.sqrt(3)/2 * chess_size[0]))
        f = (self.x, int(self.y + math.sqrt(3)/6 * chess_size[0]))

        return [a, b, c, d, e, f]

    def circle(self):
        p = (int(0.5 * chess_size[0] + self.x), int(math.sqrt(3)/3 * chess_size[0] + self.y))
        r = int(math.sqrt(3)/3 * chess_size[0])

        return [p, r]  # original point, radius

    def isWithInCollisionCircle(self, x, y):
        circle = self.circle()
        d = math.sqrt((circle[0][0] - x)**2 + (circle[0][1] - y)**2)
        return d <= circle[1]


    def draw(self, Surface, x, y):

        # row = self.row
        # col = self.col
        # total_lines = 2 * game_dim - 1
        #
        # x_space_offset = (game_dim // 2) * (Chess.x_offset + chess_size[0]) + (chess_size[0] + Chess.x_offset) // 2
        # if row <= game_dim - 1:
        #     x_space_offset -= row * ((chess_size[0] + Chess.x_offset) // 2)
        # else:
        #     x_space_offset -= (total_lines - row - 1) * ((chess_size[0] + Chess.x_offset) // 2)
        #
        # x_space_offset += Surface.get_width() // 3
        # y_space_offset = Chess.y_offset + chess_size[1]
        # y = y_space_offset + row * (Chess.y_offset + chess_size[1])
        # x = x_space_offset + col * (Chess.x_offset + chess_size[0])

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


        # collision circle
        cir = self.circle()
        pygame.draw.circle(Surface, (255, 0, 0), cir[0], cir[1], 1)


    def hit(self, type):
        self.type = type

class HexBoard:

    def __init__(self, game_dim):
        self.game_dim = game_dim
        self.chess_matrix = []
        self.changed = True
        for i in range(self.game_dim):
            self.chess_matrix.append([])
            for j in range(self.game_dim):
                self.chess_matrix[i].append(Chess(i, j))


    def draw_board(self, Surface):

        for row in range(self.game_dim):
            col_offset = row * (chess_size[0] + Chess.x_offset)
            row_offset = row * (chess_size[1] + Chess.y_offset)
            for col in range(self.game_dim):
                x_space_offset = Surface.get_width() // 2
                # x_space_offset -= row * (chess_size[0] + Chess.x_offset) // 2

                x = col_offset + x_space_offset
                y = row_offset + col * (chess_size[1] + Chess.y_offset)
                self.chess_matrix[row][col].draw(Surface, x, y)


        # border
        # for chess in self.chess_matrix:
        #     row, col = chess.position()
        #     if col == 0:
        #         x = chess.x - (Chess.x_offset + chess_size[0])
        #         y = chess.y
        #         if row < game_dim - 1:
        #             Surface.blit(border_imgs[ChessType.ONE.value], (x, y))
        #         if row > game_dim - 1:
        #             Surface.blit(border_imgs[ChessType.TWO.value], (x, y))

    def change(self, chess):
        chess.hit(ChessType.ONE)
        self.changed = True

    def detect_mouse_hit(self, x, y):
        for chess in self.chess_matrix:
            if chess.isWithInCollisionCircle(x, y):
                self.change(chess)

    # def list_to_matrix(self):
    #     matrix = []
    #     for i in range(game_dim):
    #         matrix.append([])
    #
    #     # first row
    #     matrix[0].append(0)
    #     for offset in range(1, game_dim):
    #         matrix[0].append(matrix[0][offset-1] + offset)
    #
    #     # generate dimension list
    #     dimension_list = []
    #     for i in range(1, game_dim + 1):
    #         dimension_list.append(i)
    #     for i in range(game_dim, 0, -1):
    #         dimension_list.append(i)
    #
    #     print(dimension_list)
    #     # set remaining elements
    #
    #
    # def matrix_to_list(self, matrix):
    #     # matrix to r_c
    #     r_c = []
    #     for i in range(2 * game_dim - 1):
    #         r_c.append([])
    #
    #     for row in range(game_dim):
    #         for col in range(game_dim):
    #             r_c[col]

        # r_c to index
        # count = 0
        # for row in rc:
        #     for type in row:
        #         self.chess_matrix[count] = type
        #         count += 1

    # def update(self): # used to update the algorithm class
    #     if not self.changed:
    #         return
    #
    #     # self.algorithm.update()
    #     print(self.list_to_matrix())
    #
    #     self.changed = False


hexboard = HexBoard(dim)

def draw_game():
    win.fill((200, 200, 200))
    hexboard.draw_board(win)
    pygame.display.update()

while run:
    clock.tick(1)
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # hexboard.detect_mouse_hit(x, y)
            print(x, y)
    # hexboard.update()
pygame.quit()