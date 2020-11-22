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

  def gradient(start, end, percentage):
    sr, sg, sb = start.value
    er, eg, eb = end.value
    nr = sr + int((er - sr) * percentage)
    ng = sg + int((eg - sg) * percentage)
    nb = sb + int((eb - sb) * percentage)
    return (nr,ng,nb)


class DisplayMode(Enum):
  PYGAME = 'PYGAME'
  LED_PANEL = 'LED_PANEL'

class Direction(Enum):
  UP = (0,-1)
  DOWN = (0,1)
  LEFT = (-1,0)
  RIGHT = (1,0)

  def get_next_coor(direction, cell):
    return (direction.value[0] + cell[0], direction.value[1] + cell[1])


pygame.init()
display_mode = DisplayMode.PYGAME
## TODO set display_mode according to if led panel is available
## TODO separate game logic, draw logic, and pygame/led into separate files

PYGAME_WINDOW_SIZE=640
GAME_GRID_SIZE = 32
DPI = PYGAME_WINDOW_SIZE / GAME_GRID_SIZE
UPDATE_SNAKE = pygame.USEREVENT+1
REFRESH_RATE = 50

grid = [[0 for _ in range(32)] for __ in range(32)]
snake = [(14,16), (15,16), (16,16)]
food = [(20,16)]
current_direction = Direction.DOWN
last_updated_direction = Direction.DOWN
is_game_over = False


windowSurface = pygame.display.set_mode((PYGAME_WINDOW_SIZE, PYGAME_WINDOW_SIZE), 0, 32)
windowSurface.fill(Color.BLACK.value)

def draw_pixel(color, x, y):
  global DPI
  pygame.draw.rect(windowSurface, color, ((x*DPI) + 4,(y*DPI) + 4, DPI - 4 ,DPI - 4))

def draw_game():
  global DPI
  windowSurface.fill(Color.BLACK.value)
  snake_len = len(snake)
  for index, snake_cell in enumerate(snake) :
    sx,sy = snake_cell
    color = Color.gradient(Color.DARK_GREEN, Color.GREEN, index / snake_len)
    draw_pixel(color, sx, sy)
  shx,shy = snake[-1]
  draw_pixel(Color.GREEN.value, shx, shy)
  for food_cell in food:
    fx, fy = food_cell
    draw_pixel(Color.RED.value, fx,fy)
  pygame.display.update()

# TODO once API for RGB led panel is known, update this method
def serialize_grid():
  for index, snake_cell in enumerate(snake):
    sx, sy = snake_cell
    grid[sx][sy] = 1
  for food_cell in food:
    fx, fy = food_cell
    grid[fx][fy] = 2
  
SCORE_OFFSET = (2,2)
# DIGIT GRID SIZE 
dgsx, dgsy = (6,4)

def draw_game_over():
  snake_len = len(snake)
  for index, ch in enumerate(str(snake_len)):
    digit_grid = digit_grids[int(ch)]
    offx, offy = (index * dgsx) + SCORE_OFFSET[0], SCORE_OFFSET[1]
    for y, row in enumerate(digit_grid):
      for x, cell in enumerate(row):
        if (cell > 0):
          draw_pixel(Color.BLUE.value, x + offx, y + offy)

  pygame.display.update()


def reset_game():
  global grid, snake, food, current_direction, last_updated_direction, is_game_over
  is_game_over = False
  grid = [[0 for _ in range(32)] for __ in range(32)]
  snake = [(14,16), (15,16), (16,16)]
  food = [(20,16)]
  current_direction = Direction.DOWN
  last_updated_direction = Direction.DOWN
  pygame.time.set_timer(UPDATE_SNAKE, REFRESH_RATE) 


def eat_food():
  global food
  while(True):
    new_food = random.randint(0,GAME_GRID_SIZE-1),random.randint(0,GAME_GRID_SIZE-1)
    if new_food not in snake:
      break
  food.append(new_food)
  del food[0]

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
  
def update_snake():
  global snake, last_updated_direction, is_game_over
  snake_head = snake[-1]
  i, j = Direction.get_next_coor(current_direction, snake_head)

  ## allow wrap-around
  if (i >= GAME_GRID_SIZE):
    i = 0
  elif (i < 0):
    i = GAME_GRID_SIZE - 1
  if (j >= GAME_GRID_SIZE):
    j = 0
  elif (j < 0):
    j = GAME_GRID_SIZE - 1

  if ((i,j) != snake[-2] and (i,j) in snake):
    is_game_over = True

  else:
    snake.append((i,j))
    if ((i,j) in food):
      eat_food()
    else:
      del snake[0]
    last_updated_direction = current_direction
  
reset_game()

# run the game loop
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
        
    if (not is_game_over):
      if event.type == UPDATE_SNAKE:
        update_snake()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          update_direction(Direction.LEFT)
        if event.key == pygame.K_RIGHT:
          update_direction(Direction.RIGHT)
        if event.key == pygame.K_DOWN:
          update_direction(Direction.DOWN)
        if event.key == pygame.K_UP:
          update_direction(Direction.UP)

  if (is_game_over):
    draw_game_over()
    pygame.time.set_timer(UPDATE_SNAKE, 0)     
    pygame.event.clear()
    while (True):
      next_event = pygame.event.wait()
      if next_event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if next_event.type == pygame.KEYDOWN and next_event.key == pygame.K_SPACE:
        reset_game()
        break
  else:
    draw_game()


    