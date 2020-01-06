import pygame
import pygame.gfxdraw
import os
from enum import Enum
import math
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon

pygame.init()

dim = 7
chess_size = (25, 25)
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
    HUMAN = 1
    AI = 2

class Chess:
    y_offset = 10
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

    def draw_circle(self, Surface, r, g, b, x, y):
        self.x = x
        self.y = y
        cir = self.circle()
        # pygame.draw.circle(Surface, (r, g, b), cir[0], cir[1], 1)
        # pygame.gfxdraw.circle(Surface, cir[0][0], cir[0][1], cir[1], (r, g, b))
        pygame.gfxdraw.filled_circle(Surface, cir[0][0], cir[0][1], cir[1], (r, g, b))
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
        elif self.type == ChessType.HUMAN:
            pygame.gfxdraw.filled_polygon(Surface, self.polygon(), (0, 0, 128))
        else:
            pygame.gfxdraw.filled_polygon(Surface, self.polygon(), (128, 0, 0))


        # collision circle
        # cir = self.circle()
        # pygame.draw.circle(Surface, (255, 0, 0), cir[0], cir[1], 1)


    def hit(self, type):
        self.type = type

class HexBoard:

    def __init__(self, game_dim):
        self.game_dim = game_dim
        self.chess_matrix = []
        self.changed = True
        self.current_player = ChessType.HUMAN
        for i in range(self.game_dim + 2):
            self.chess_matrix.append([])
            for j in range(self.game_dim + 2):
                self.chess_matrix[i].append(Chess(i, j))


    def draw_board(self, Surface):

        for row in range(self.game_dim + 2):
            col_offset = row * (chess_size[0] + Chess.x_offset)
            row_offset = row * (chess_size[1] + Chess.y_offset)
            for col in range(self.game_dim + 2):
                x_space_offset = Surface.get_width() // 2
                x_space_offset -= (row + col) * (chess_size[0] + Chess.x_offset) // 2

                x = col_offset + x_space_offset
                y = row_offset + col * (chess_size[1] + Chess.y_offset)

                # check if it is border
                if (row == 0 and col == 0) or (row == 0 and col == self.game_dim + 1) or (row == self.game_dim + 1 and col == 0) or (row == self.game_dim + 1 and row == col):
                    self.chess_matrix[row][col].draw_circle(Surface, 128, 0 ,128, x, y)
                elif row == 0 or row == self.game_dim + 1:
                    self.chess_matrix[row][col].draw_circle(Surface, 0, 0, 128, x, y)
                elif col == 0 or col == self.game_dim + 1:
                    self.chess_matrix[row][col].draw_circle(Surface, 128, 0, 0, x, y)
                else:
                    self.chess_matrix[row][col].draw(Surface, x, y)

    def flip(self):
        if self.current_player == ChessType.HUMAN:
            self.current_player = ChessType.AI
        else:
            self.current_player = ChessType.HUMAN
        self.changed = True

    def update_chess(self, row, col):
        self.chess_matrix[row][col].hit(self.current_player)
        self.flip()
        self.changed = True

    def detect_mouse_hit(self, x, y):
        for row in range(1, self.game_dim + 1):
            for col in range(1, self.game_dim + 1):
                if self.chess_matrix[row][col].type != ChessType.EMPTY:
                    continue
                if self.chess_matrix[row][col].isWithInCollisionCircle(x, y):
                    self.update_chess(row, col)

    def toMatrix(self):
        matrix = []
        for row in range(self.game_dim):
            matrix.append([])

        for row in range(1, self.game_dim + 1):
            for col in range(1, self.game_dim + 1):
                matrix[row].append(self.chess_matrix[row][col].type)

        return matrix


    def update(self): # used to update the broad
        if not self.changed:
            return

        # if self.current_player == ChessType.AI:
        #     pass  # todo: send to algorithm
        # elif:
        #     pass # todo: receive from algorithm
        # matrix = self.toMatrix()


        self.changed = False


hexboard = HexBoard(dim)

def draw_game():
    win.fill((200, 200, 200))
    hexboard.draw_board(win)
    pygame.display.update()

while run:
    clock.tick(10)
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            hexboard.detect_mouse_hit(x, y)
            print(x, y)
    # hexboard.update()
pygame.quit()