import pygame
from random import randint
pygame.init()

SCORE = 0
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 750
CUBE_WIDTH = 30
RANGE_X = range(12)
RANGE_Y = range(22)
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Creates pygame window

#Definining Tetris Colors
RED = (237, 47, 33)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAMSCICLE = (255, 157, 0)
BLUE = (0, 140, 255)
TURQUIOSE = (79, 255, 255)
LIGHT_GREEN = (114, 240, 72)
PURPLE = (176, 114, 242)
YELLOW = (239, 247, 79)
colors = [RED, CREAMSCICLE, BLUE,TURQUIOSE,LIGHT_GREEN, PURPLE, YELLOW]

run = True
tetris_name = pygame.image.load('tetris.png')
next_move = []

class Block(): #Class that defines the Block objects of the grid ; https://docs.python.org/3/tutorial/classes.html; Gave basic information of how to use a class and it's attributes
    def __init__(self, value, color):
        self.value = value
        self.color = color

#coordinates/Grid
GRID = [[Block(0, BLACK) for n in RANGE_X] for n in RANGE_Y] #Creates a grid 12x22 dimensions ; https://www.youtube.com/watch?v=5d1CfnYT-KM ; Adapted for our purposes with Block object

#The shape functions all define and initiate the current shape in play
def L_shape(x, y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y + 1][x] = Block(1, rand_color)
    GRID[y + 2][x] = Block(1, rand_color)
    GRID[y + 2][x + 1] = Block(1, rand_color)
    return [x, x, x, x + 1], [y, y+1, y+2, y+2]

def stick_shape(x,y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y+1][x] = Block(1, rand_color)
    GRID[y+2][x] = Block(1, rand_color)
    GRID[y+3][x] = Block(1, rand_color)
    return [x,x,x,x], [y, y+1, y+2, y+3]

def line_shape(x, y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y][x+1] = Block(1, rand_color)
    GRID[y][x+2] = Block(1, rand_color)
    GRID[y][x+3] = Block(1, rand_color)
    return [x, x+1, x+2, x+3],[y, y, y, y]

def Rstep_shape(x,y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y][x+1] = Block(1, rand_color)
    GRID[y+1][x+1] = Block(1, rand_color)
    GRID[y+1][x+2] = Block(1, rand_color)
    return [x, x+1, x+1, x+2],[y,y,y+1,y+1]

def Lcorner_shape(x,y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y+1][x] = Block(1, rand_color)
    GRID[y+1][x+1] = Block(1, rand_color)
    GRID[y+1][x+2] = Block(1, rand_color)
    return [x,x,x+1,x+2],[y,y+1,y+1,y+1]

def Rcorner_shape(x,y):
    GRID[y][x] = Block(1, rand_color)
    GRID[y+1][x] = Block(1, rand_color)
    GRID[y+2][x] = Block(1, rand_color)
    GRID[y+2][x-1] = Block(1, rand_color)
    return [x,x,x,x-1],[y,y+1,y+2,y+2]

def square_shape(x, y): 
    GRID[y][x] = Block(1, rand_color)
    GRID[y][x + 1] = Block(1, rand_color)
    GRID[y + 1][x] = Block(1, rand_color) 
    GRID[y + 1][x + 1] = Block(1, rand_color)
    return [x, x+1, x, x+1],[y, y, y + 1, y+1]

#List of all shape functions
shapes = [square_shape, Rstep_shape, L_shape, stick_shape, Rcorner_shape, Lcorner_shape, line_shape,]

def pick_randcolor(): #Picks random color from colors list
    return colors[randint(0, len(colors) - 1)]

def rand_start_position(): #Chooses a random start position for the current shape in play to start on the top line of the grid
    return randint(2,8)

def check_full_row(grid): #Returns the row at which every block on the grid has a value of 2, and is "filled"
    counter = 0
    for r in RANGE_Y:
        counter = 0
        for c in RANGE_X:
            if(grid[r][c].value == 2):
                counter += 1
        if(counter == 12):
            return r
    return False

def check_gameover(grid): #Returns true if any block's value on the top row of the grid equals 2 
    dummy = False
    for block in grid[0]:
        if(block.value == 2):
            dummy = True    
    return dummy

def clear_row(grid, score): #Clears a filled row on the grid and moves all other block's values and colors down, and increments score
    if(check_full_row(grid)):
        row = check_full_row(grid)
        while (row > -1): 
            for c in RANGE_X:
                if(row == 0):
                    grid[row][c].color = BLACK
                    grid[row][c].value = 0
                else:
                    grid[row][c].color = grid[row - 1][c].color
                    grid[row][c].value = grid[row-1][c].value
            row -= 1
        score += 100
    return score
                
def move_keys(keys): #Takes in a list of key values and calls the according 'move' function that corresponds with the key pressed
    if keys[pygame.K_LEFT]: #https://www.youtube.com/watch?v=2-DNswzCkqk ; This video gave the basic idea of how to input keyboard controls in pygame ; Adapted for Tetris purposes
        move_block_left(GRID, current_shape_x, current_shape_y)
    if keys[pygame.K_RIGHT]:
        move_block_right(GRID, current_shape_x, current_shape_y)
    if keys[pygame.K_DOWN]:
        move_block_down(GRID, current_shape_x, current_shape_y)

def choose_randshape(shapes): #Chooses a random shape function from the shapes list
    return shapes[randint(0, len(shapes)-1)]


def update_xylists(grid, x_list, y_list): #Updates the x and y lists that contain the current shape's coordinates
    x_list.clear()
    y_list.clear()

    for r in RANGE_Y:
        for c in RANGE_X:
            if(grid[r][c].value == 1):
                x_list.append(c)
                y_list.append(r)

def move_block_down(grid, x_list, y_list): #Moves the current shape in play down
    next_position_2 = False
    i = len(x_list) - 1

    if(x_list):
        max_coord_y = max(y_list)
        
    while i > -1:
        for a in range(len(x_list)): #Checks if next block's value in shape's path is filled
            if(y_list[a] == max_coord_y):
                if ((max_coord_y == 21) or grid[max_coord_y+1][x_list[a]].value == 2):
                    next_position_2 = True
        
        if(y_list[i] == 21 or next_position_2):
            for i in range(len(x_list)):
                grid[y_list[i]][x_list[i]].value = 2
                next_move.append(1)
            return None
        else:
            if(grid[y_list[i]][x_list[i]].value == 1):
                grid[y_list[i]+1][x_list[i]] = Block(grid[y_list[i]][x_list[i]].value, grid[y_list[i]][x_list[i]].color)
                grid[y_list[i]][x_list[i]] = Block(0, BLACK)
        next_position_2 = False
        i -= 1
        update_xylists(grid, x_list, y_list)

def move_block_right(grid, x_list, y_list): #Moves the current shape in play right
    i = len(x_list) - 1
    while i > -1:
        if(x_list[i] == 11):
            return None
        else:
            if(grid[y_list[i]][x_list[i]].value == 1):
                grid[y_list[i]][x_list[i] + 1] = Block(grid[y_list[i]][x_list[i]].value, grid[y_list[i]][x_list[i]].color)
                grid[y_list[i]][x_list[i]] = Block(0, BLACK)
        i -= 1
        update_xylists(grid, x_list,y_list)

def move_block_left(grid, x_list, y_list): #Moves the current shape in play left
    i = 0
    while i < (len(x_list)):
        if(x_list[i] == 0):
            return None
        else:
            if(grid[y_list[i]][x_list[i]].value == 1):
                grid[y_list[i]][x_list[i] - 1] = Block(grid[y_list[i]][x_list[i]].value, grid[y_list[i]][x_list[i]].color)
                grid[y_list[i]][x_list[i]] = Block(0, BLACK)
        i += 1
        update_xylists(grid, x_list,y_list)

def draw_grid(): # Draws the grid's colors and white outlines
    grid_y = 50 #https://www.youtube.com/watch?v=5d1CfnYT-KM ; Adapted for pygame and Tetris purposes ; Gave basic idea of how to translate grid values to graphics
    for row in RANGE_Y:
        grid_x = 19
        for column in RANGE_X:
            pygame.draw.rect(window, GRID[row][column].color, (grid_x, grid_y, CUBE_WIDTH, CUBE_WIDTH)) 
            pygame.draw.rect(window, WHITE, (grid_x , grid_y, CUBE_WIDTH + 1, CUBE_WIDTH + 1), 1) #Draws white grid(rectangles with white border)
            grid_x += CUBE_WIDTH
        grid_y += CUBE_WIDTH

def redraw_gamewindow(): #https://www.pygame.org/docs/ ; Gave documentation on how to initiate game window/ extra graphics
    score_font = pygame.font.SysFont("Courier New", 20).render("Your Score: " + str(SCORE), False, (WHITE))#Creates text object 'score' to display ; https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame; Adapted for Tetris purposes
    window.fill(BLACK)#Fills whole screen black
    window.blit(tetris_name, (SCREEN_WIDTH/2 - 100,-25)) #Draws tetris logo
    window.blit(score_font, (4,30))#Displays score
    draw_grid()

rand_color = pick_randcolor()
current_shape_x, current_shape_y = choose_randshape(shapes)(rand_start_position(),0)

while run: #Main run loop
    if(check_gameover(GRID)):
        run = False
    pygame.time.delay(300)
    for event in pygame.event.get(): #https://www.youtube.com/watch?v=2-DNswzCkqk ; This video gave basic fundamentals of pygame and how to stop the program when the red 'x' was pressed
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed() #https://www.youtube.com/watch?v=2-DNswzCkqk ; This video gave the basic idea of how to input keyboard controls in pygame
    move_keys(keys) 
    move_block_down(GRID, current_shape_x,current_shape_y)
    redraw_gamewindow()
    pygame.display.update() #https://www.pygame.org/docs/ ; Updates the display
    SCORE = clear_row(GRID, SCORE)
    if(next_move):
        rand_color = pick_randcolor()
        current_shape_x, current_shape_y = choose_randshape(shapes)(rand_start_position(),0)
        next_move.clear()

pygame.quit()