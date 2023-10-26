import pygame
from logic import Game
import numpy as np

pygame.init()
pygame.display.set_caption('Batteshlip') #Name of the game
clock = pygame.time.Clock() #Setting fotograms per second

#Global variables
SQ_SIZE = 25 #Size of the squares
H_MARGIN = 200 #Horizontal margin of the screen
V_MARGIN = 100 #Vertical margin of the screen
WIDTH = 1000 #Width of the screen
HEIGHT = 700 #Height of the screen
SCREEN_SIZE = (WIDTH, HEIGHT) #Size of the screen
SCREEN = pygame.display.set_mode(SCREEN_SIZE) #Setting the screen

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (40, 50, 60)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (50, 200, 100)

#Draw the grids (10 x 10 squares on each grid)
def grid_make(left = 40, top = 40):
    for i in range(10):
        for j in range(10):
            x = left + (i * ((WIDTH - H_MARGIN)//20)) #Coord. x of the square
            y = top + (j * ((HEIGHT - V_MARGIN)//20)) #Coord. y of the square
            square = pygame.Rect(x, y, (WIDTH - H_MARGIN)//20, (HEIGHT - V_MARGIN)//20) #Square, made of coordinates and size (width, height)
            pygame.draw.rect(SCREEN, WHITE, square, width=3) #Draw the square (1 of 100)

#Draw the ships
def draw_ships(player, left = 40, top = 40): #Player is an object of the class Player, ecach player has 10 ships
    for ship in player.ships:
        for i, j in ship: #i is the row, j is the column of each ship
            pygame.draw.rect(SCREEN, GREEN, (5 + left + (i * ((WIDTH - H_MARGIN)//20)), \
                                    5 + top + (j * ((HEIGHT - V_MARGIN)//20)),\
                                        (WIDTH - H_MARGIN)//20 -10, (HEIGHT - V_MARGIN)//20 - 10), border_radius= 20) #Draw the ship
            pygame.draw.rect(SCREEN, BLACK, (left + (i * ((WIDTH - H_MARGIN)//20)), \
                                    top + (j * ((HEIGHT - V_MARGIN)//20)),\
                                        (WIDTH - H_MARGIN)//20, (HEIGHT - V_MARGIN)//20), width=1) #Draw the square of the ship

#Draw shots that hit the ships
def draw_removed_positions(game_shots, left, top):
    for i, j in game_shots:
        # Draw a different color or indicator for removed positions
        pygame.draw.rect(SCREEN, RED, (5 + left + (i * ((WIDTH - H_MARGIN)//20)), \
                                    5 + top + (j * ((HEIGHT - V_MARGIN)//20)),\
                                        (WIDTH - H_MARGIN)//20 -10, (HEIGHT - V_MARGIN)//20 - 10))
        
#Draw shots that missed the ships
def draw_shots(game_shots, left, top):
    for i, j in game_shots:
        # Draw a different color or indicator for removed positions
        pygame.draw.rect(SCREEN, BLUE, (5 + left + (i * ((WIDTH - H_MARGIN)//20)), \
                                    5 + top + (j * ((HEIGHT - V_MARGIN)//20)),\
                                        (WIDTH - H_MARGIN)//20 -10, (HEIGHT - V_MARGIN)//20 - 10))

#Loop of the game
animating = True
pausing = False
Game_battleship = Game() #Create an object of the class Game

#Grids
SCREEN.fill(GREY)
grid_make() #Create the grid where player 1 shots
grid_make(WIDTH//2 + 60, 40) #Create the grid of player 2


grid_make(40, HEIGHT//2 + 25) #Create the grid of player 1
grid_make(WIDTH//2 + 60, HEIGHT//2 + 25)#Create the grid where player 2 shots

#Ships
draw_ships(Game_battleship.player_1, 40, HEIGHT//2 + 25)
draw_ships(Game_battleship.player_2, WIDTH//2 + 60, 40)

#Main loop
while animating:
    for event in pygame.event.get():

        #Out of the game
        if event.type == pygame.QUIT:
            animating = False
        
        #Press a key
        if event.type == pygame.KEYDOWN:

            #ESC to quit
            if event.key == pygame.K_ESCAPE:
                animating = False
            
            #Space to pause
            if event.key == pygame.K_SPACE:

                if pausing == True:
                    pausing = False
                
                elif pausing == False:
                    pausing = True

            
        #Playing the game
        if not pausing:
            message = Game_battleship.make_move(np.random.randint(10), np.random.randint(10)) #Play game
            draw_removed_positions(game_shots = Game_battleship.player_1_removed_positions, left = 40, top = 40)
            draw_removed_positions(game_shots = Game_battleship.player_2_removed_positions, left = WIDTH//2 + 60, top = HEIGHT//2 + 25)
            draw_shots(game_shots = Game_battleship.player_1_shots, left = 40, top = 40)
            draw_shots(game_shots = Game_battleship.player_2_shots, left = WIDTH//2 + 60, top = HEIGHT//2 + 25)
            

            pygame.display.flip()
            clock.tick(50)

            

            

