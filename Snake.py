# Snake Game Version 2023-11-06_1945
# Developer: Hristian Carabulea
# YT Course: https://www.youtube.com/watch?v=XKHEtdqhLK8
# How to play sound files in python: https://projects.raspberrypi.org/en/projects/generic-python-playing-sound-files
# Sound files from https://soundbible.com/

from tkinter import *
import random

import pygame ### add sound capabilities
pygame.init()

# constants do not exist in Python
GAME_WIDTH = 700
GAME_HEIGHT = 400

SPEED = 200 # the lower the number, the faster the game

SPACE_SIZE = 25 # make the board bigger or smaller
BODY_PARTS  = 3 # make the snake longer or shorter at starting point
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

### the sounds to play at certain events

EAT_SOUND = pygame.mixer.Sound("Sounds/eat.wav")
GAME_OVER = pygame.mixer.Sound("Sounds/gameOver.wav")
GROW_BY_ONE = pygame.mixer.Sound("Sounds/grow.wav")

class Snake:
  def __init__(self): # this is a constructor
    self.body_size = BODY_PARTS
    self.coordinates = []
    self.squares =[]

    for i in range(0, BODY_PARTS):
      self.coordinates.append([0,0])
      

    for x, y in self.coordinates:
      square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
      self.squares.append(square)
  

class Food:
  def __init__(self): # this is a constructor. Number of places formula results in 14: 700 / 50 = 14

  # need to use // for division to return an integer. Otherwise getting error
    x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
    y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

    self.coordinates = [x, y]

    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

##########################
def next_turn(snake, food):
  x, y = snake.coordinates[0]

  if direction == "up":
    y -= SPACE_SIZE
  elif direction == "down":
    y += SPACE_SIZE
  elif direction == "left":
    x -= SPACE_SIZE
  elif direction == "right":
    x += SPACE_SIZE

  snake.coordinates.insert(0, (x, y))

  square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

  snake.squares.insert(0, square)

  if (x == food.coordinates[0] and y == food.coordinates[1]):
    global score
    score += 1
    label.config(text="Score:{}".format(score)) ### ERROR ###
    canvas.delete( "food")
    food = Food()
    EAT_SOUND.play()

  else: # only delete last body part if we did not eat a food object
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1]) #delete the tail of the snake as it moves
    del snake.squares[-1]

  if check_collisions(snake):
    game_over()

  else:
    window1.after(SPEED, next_turn, snake, food)
    GROW_BY_ONE.play()



####################################
def change_direction(new_direction):
  global direction

  if new_direction == 'left':
    if direction != 'right':
      direction = new_direction
  elif new_direction == 'right':
    if direction != 'left':
      direction = new_direction
  elif new_direction == 'up':
    if direction != 'down':
      direction = new_direction
  elif new_direction == 'down':
    if direction != 'up':
      direction = new_direction




####################################
def check_collisions(snake): 
  x, y = snake.coordinates[0] # unpack snake

  if x < 0 or x >= GAME_WIDTH:
    #print("GAME OVER")
    
    return True

  elif y < 0 or y >= GAME_HEIGHT:
    #print("GAME OVER")
    #GAME_OVER.play()
    return True

  for body_part in snake.coordinates[1:]:
    if x == body_part[0] and y == body_part[1]:
      #print("GAME OVER")
      #GAME_OVER.play()
      return True
    
  return False
    
####################################    
def game_over():

  GAME_OVER.play() # play sound for game over notification
  canvas.delete(ALL)
  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                     font=('consolas', 30), text="GAME OVER", fill="red", tag="gameover")


################### MAIN #######################    

window1 = Tk() # create a window 

window1.title("Snake Game")
window1.resizable(False,False)

score = 0
direction = 'down'

label = Label(window1, text="Score:{}".format(score), font=('consolas',30))
label.pack()

canvas = Canvas(window1, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window1.update()

window1_width = window1.winfo_width()
window1_height = window1.winfo_height()
screen_width = window1.winfo_screenwidth()
screen_height = window1.winfo_screenheight()

x =int((screen_width/2) - (window1_width/2))    # only integers can be passed to window.geometry below
y =int((screen_height/2) - (window1_height/2))  # only integers can be passed to window.geometry below

window1.geometry(f"{window1_width}x{window1_height}+{x}+{y}")

window1.bind('<Left>', lambda event: change_direction('left'))
window1.bind('<Right>', lambda event: change_direction('right'))
window1.bind('<Up>', lambda event: change_direction('up'))
window1.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)


window1.mainloop() # first must instantiate(create) window with: windowName = Tk()
