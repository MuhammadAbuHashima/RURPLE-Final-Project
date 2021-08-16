import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
pygame.display.set_caption("RURPLE-Final Project")
spaces = 2
tiles = 7
tile_x = int(WIDTH / (tiles + spaces))
tile_y = int(tile_x)
initial_x = int(tile_x)
initial_y = int(tile_x)
line = 1

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AQUA = (0, 255, 255)
GREEN = (0, 128, 0)
RAT = (0, 0, 255, 255)
GRAY = (112, 128, 144)
YELLOW = (255, 222, 173)
board = []
water = []
bridge = []
move_up = False
move_down = False
move_left = False
move_right = False
mouse_died = False
water_references = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (1, 0), (1, 6), (2, 0), (2, 6), (3, 0), (3, 6), (4, 0),
    (4, 6), (5, 0), (5, 6),
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
]

frame_height = int(tiles * (tile_x + line) + 2 * line)
frame_width = frame_height
frame = pygame.Surface((frame_height, frame_width))
frame.fill(WHITE)
frame_rect = frame.get_rect()
frame_rect.x = tile_x - 2
frame_rect.y = tile_x - 2


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def board_rects():
    global initial_x, initial_y, tile_x, tile_y
    for x in range(7):
        for y in range(7):
            a_rectangle = pygame.Rect(initial_x, initial_y, tile_x, tile_y)
            if (x, y) in water_references:
                water.append(a_rectangle)
            if (x, y) == (3, 6):
                bridge.append(a_rectangle)
            else:
                board.append(a_rectangle)
            initial_x += tile_x + line
        initial_x = tile_x
        initial_y += tile_y + line


def draw_board():
    pygame.draw.rect(win, WHITE, frame_rect, 2)

    for rect in board:
        pygame.draw.rect(win, WHITE, rect)

    for rect in water:
        pygame.draw.rect(win, AQUA, rect)

    pygame.draw.rect(win, GREEN, bridge[0])



board_rects()
allowed_x = [rect.x for rect in board]
allowed_y = [rect.y for rect in board]

forbidden = [(rect.x, rect.y) for rect in water]

def create_mouse_and_cat():
    global mouse_rectangle, cat_rectangle
    cat_x = random.choice(allowed_x)
    cat_y = random.choice(allowed_y)

    mouse_x = [x for x in allowed_x if not x == cat_x]
    mouse_y = [y for y in allowed_y if not y == cat_y]
    cat_rectangle = pygame.Rect(cat_x, cat_y, tile_x, tile_y)
    mouse_rectangle = pygame.Rect(random.choice(mouse_x), random.choice(mouse_y), tile_x, tile_y)


create_mouse_and_cat()


def update_mouse():
    global move_up, move_down, move_left, move_right, mouse_died, number_of_moves
    number_of_moves = 0
    if move_up:
        mouse_rectangle.y -= tile_x + line
        number_of_moves += 1
        move_up = False
    if move_down:
        mouse_rectangle.y += tile_x + line
        number_of_moves += 1
        move_down = False
    if move_left:
        mouse_rectangle.x -= tile_x + line
        number_of_moves += 1
        move_left = False
    if move_right:
        mouse_rectangle.x += tile_x + line
        number_of_moves += 1
        move_right = False

    if (mouse_rectangle.x, mouse_rectangle.y) in forbidden:
        mouse_died = True

    if mouse_rectangle.x == cat_rectangle.x and mouse_rectangle.y == cat_rectangle.y:
        mouse_died = True

    if number_of_moves == 20:
        mouse_died = True

    if mouse_rectangle.x == bridge[0].x and mouse_rectangle.y == bridge[0].y:
        win = pygame.display.set_mode((500, 500))
        background = pygame.image.load("rat.jpg")
        win.blit(background, (0, 0))




def draw_mouse_and_cat():

    pygame.draw.rect(win, GRAY, mouse_rectangle)
    pygame.draw.rect(win, RED, cat_rectangle)

def handle_events():
    global move_up, move_down, move_right, move_left

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_down = True
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True



while True:
    win.fill(BLACK)
    handle_events()
    draw_board()

    if not mouse_died:
        update_mouse()
    else:
        create_mouse_and_cat()
        number_of_moves = 0
        mouse_died = False
    draw_mouse_and_cat()

    pygame.display.update()