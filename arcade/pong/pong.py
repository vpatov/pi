import pygame, sys
from pygame.locals import *
from enum import Enum
from digits import digit_grids
import random

class Color(Enum):
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  DARK_GREEN = (0, 80, 0)
  BLUE = (0, 0, 255)

class DisplayMode(Enum):
  PYGAME = 'PYGAME'
  LED_PANEL = 'LED_PANEL'

## used only for the paddle
class Direction(Enum):
  UP = (0,-1)
  DOWN = (0,1)
  LEFT = (-1,0)
  RIGHT = (1,0)

  def get_next_coor(direction, cell):
    return (direction.value[0] + cell[0], direction.value[1] + cell[1])

pygame.init()
display_mode = DisplayMode.PYGAME

PYGAME_WINDOW_SIZE=640
GAME_GRID_SIZE = 32
DPI = PYGAME_WINDOW_SIZE / GAME_GRID_SIZE
UPDATE_PADDLE = pygame.USEREVENT+1
REFRESH_RATE = 55

grid = [[0 for _ in range(32)] for __ in range(32)]
PADDLE = [(2,2), (2,3), (2,4)]

is_game_over = False


windowSurface = pygame.display.set_mode((PYGAME_WINDOW_SIZE, PYGAME_WINDOW_SIZE), 0, 32)
windowSurface.fill(Color.BLACK.value)

def draw_pixel(color, x, y):
  global DPI
  pygame.draw.rect(windowSurface, color, ((x*DPI) + 4,(y*DPI) + 4, DPI - 4 ,DPI - 4))

# run the game loop
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
        



