import pygame
pygame.init()

board = (6*[0], 7*[0], 8*[0], 9*[0], 10*[0], 11*[0], 10*[0], 9*[0], 8*[0], 7*[0], 6*[0])
run = True

def draw_game():
    win = pygame.display.set_mode((456, 352))
    win.fill((0,0,0))
    hexboard = HexBoard()
    hexboard.draw_board(win, 28, 128)
    pygame.display.update()

class HexBoard:

    def __init__(self, red = 255, green = 248, blue = 220):
        self.r = red
        self.g = green
        self.b = blue

    def draw_board(self, Surface, off_x, off_y):
        for i, col in enumerate(board):
            col_size = len(col)
            for j, piece in enumerate(col):
                draw_hex(Surface, i*40+off_x, j*32+off_y-col_size*16+64, \
                    (self.r-14*((col_size+j)%3), self.g-45*((col_size+j)%3), self.b-49*((col_size+j)%3)))
                color = 25+i%2*195
                draw_piece(Surface, i*40+off_x, j*32+off_y-col_size*16+64, (color-20, color, color))

def draw_hex(Surface, x, y, rgb):
    pygame.draw.polygon(Surface, rgb, [(x-28,y),(x-12,y+16),(x+12,y+16),(x+28,y),(x+12,y-16),(x-12,y-16)], 0)

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