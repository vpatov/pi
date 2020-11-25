import pygame
from enum import Enum

class Color(Enum):
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  DARK_GREEN = (0, 80, 0)
  BLUE = (0, 0, 255)
  YELLOW = (255, 255, 0)
  PINK = (255, 105, 180)
  ORANGE = (255, 165, 0)
  DARK_BLUE = (0, 0, 139)

class DisplayMode(Enum):
  PYGAME = 'PYGAME'
  LED_PANEL = 'LED_PANEL'

class Direction(Enum):
  UP = (0,-1)
  DOWN = (0,1)
  LEFT = (-1,0)
  RIGHT = (1,0)
  
  def get_next_coor(self, direction, cell):
    return (direction.value[0] + cell[0], direction.value[1] + cell[1])

pygame.init()
display_mode = DisplayMode.PYGAME

PYGAME_WINDOW_SIZE=640
GAME_GRID_SIZE = 32
DPI = PYGAME_WINDOW_SIZE / GAME_GRID_SIZE
UPDATE_PACMAN = pygame.USEREVENT+1
REFRESH_RATE = 55

grid = [[0 for _ in range(32)] for _ in range(32)]
pacman = [(15,29)]
jail = [(12, 15), (13, 15), (14, 15), (15, 15), 
        (16, 15), (17, 15), (17, 14), (17, 13), 
        (17, 12), (16, 12), (15, 12), (14, 12), 
        (13, 12), (12, 12), (12, 13), (12, 14)]

pink_ghost = [(13, 13)]
orange_ghost = [(14, 13)]
red_ghost = [(15, 13)]
blue_ghost = [(16, 13)]

power_ups = [(1, 29), (1, 2), (30, 2), (30, 29)]


current_direction = Direction.DOWN
last_updated_direction = Direction.DOWN
is_game_over = False


windowSurface = pygame.display.set_mode((PYGAME_WINDOW_SIZE, PYGAME_WINDOW_SIZE), 0, 32)
windowSurface.fill(Color.BLACK.value)

def draw_pixel(color, x, y):
    global DPI
    pygame.draw.rect(windowSurface, color, ((x*DPI) + 4,(y*DPI) + 4, DPI - 4 ,DPI - 4))

def reset_game():
    global DPI
    windowSurface.fill(Color.BLACK.value)

    for index, jail_cell in enumerate(jail):
        jx, jy = jail_cell
        color = Color.DARK_BLUE.value
        draw_pixel(color, jx, jy)

    for index, power_up_cell in enumerate(power_ups):
        px, py = power_up_cell
        color = Color.WHITE.value
        draw_pixel(color, px, py)

    draw_pixel(Color.YELLOW.value, pacman[0][0], pacman[0][1])
    draw_pixel(Color.PINK.value, pink_ghost[0][0], pink_ghost[0][1])
    draw_pixel(Color.ORANGE.value, orange_ghost[0][0], orange_ghost[0][1])
    draw_pixel(Color.BLUE.value, blue_ghost[0][0], blue_ghost[0][1])
    draw_pixel(Color.RED.value, red_ghost[0][0], red_ghost[0][1])

    pygame.time.set_timer(UPDATE_PACMAN, REFRESH_RATE) 
    #pygame.display.update()

def draw_game():
    global DPI
    windowSurface.fill(Color.BLACK.value)

    for index, jail_cell in enumerate(jail):
        jx, jy = jail_cell
        color = Color.DARK_BLUE.value
        draw_pixel(color, jx, jy)

    for index, power_up_cell in enumerate(power_ups):
        px, py = power_up_cell
        color = Color.WHITE.value
        draw_pixel(color, px, py)

    draw_pixel(Color.YELLOW.value, pacman[0][0], pacman[0][1])
    draw_pixel(Color.PINK.value, pink_ghost[0][0], pink_ghost[0][1])
    draw_pixel(Color.ORANGE.value, orange_ghost[0][0], orange_ghost[0][1])
    draw_pixel(Color.BLUE.value, blue_ghost[0][0], blue_ghost[0][1])
    draw_pixel(Color.RED.value, red_ghost[0][0], red_ghost[0][1])

    pygame.display.update()

def update_direction(direction):
    global current_direction
    if direction == Direction.DOWN and last_updated_direction != Direction.UP:
        current_direction = Direction.DOWN
    elif direction == Direction.UP and last_updated_direction != Direction.DOWN:
        current_direction = Direction.UP
    elif direction == Direction.LEFT and last_updated_direction != Direction.RIGHT:
        current_direction = Direction.LEFT
    elif direction == Direction.RIGHT and last_updated_direction != Direction.LEFT:
        current_direction = Direction.RIGHT

def move_pacman():
    global pacman
    px, py = pacman[0]
    px += current_direction.value[0]
    py += current_direction.value[1]

    del pacman[0]
    pacman.append((px, py))

reset_game()

while True:
    for event in pygame.event.get():
        if (not is_game_over):
            if event.type == UPDATE_PACMAN:
                move_pacman()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    update_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    update_direction(Direction.RIGHT)
                elif event.key == pygame.K_DOWN:
                    update_direction(Direction.DOWN)

    draw_game()