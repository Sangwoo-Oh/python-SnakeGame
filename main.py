import pygame
import random # for random arrangement of food position

# Initialize Pygame
pygame.init() # initialize all modules of pygame (display, fonts, clock)

# Define colors as triple tuples in RGB format

YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)

# Set up game window
# set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
# What is Surface object? A. pygame object for representing images
# set_mode function will create a "display surface". Pygame does not support multiple display surfaces.
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('Simple Snake Game') # set window title

# Game variables
snake_block = 20 # size of snake block
snake_speed = 10 # how fast the snake moves
clock = pygame.time.Clock() # to control the speed of the game

# # Fonts
font_style = pygame.font.SysFont("impact", 25)
score_font = pygame.font.SysFont("impact", 25)

# Score function
def draw_score(score):
    # render(text, antialias, color, background=None) -> Surface: draw text on a new surface
    surface = score_font.render("Your Score: " + str(score), True, YELLOW)
    dis.blit(surface, (5,5))

# Snake function (The body of the snake is represented by a list of coordinates (queue data structure))
def draw_snake(snake_block, snake_List):
    for idx, coord in enumerate(snake_List):
        # draw is a pygame module for drawing shapes
        if idx == len(snake_List) - 1:
            pygame.draw.rect(dis, RED, (coord[0], coord[1], snake_block, snake_block))
        else:
            pygame.draw.rect(dis, BLACK, (coord[0], coord[1], snake_block, snake_block))
        

# Message function
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, (dis_width / 6, dis_height / 2))

# Main game loop
def gameLoop():
    is_run = True # True while the game is running
    is_game_over = False # True when the game is over

    # Snake starting position
    x = dis_width / 2 
    y = dis_height / 2 

    # Snake movement
    x_change = 0
    y_change = 0

    # Snake body
    snake_List = []
    Length_of_snake = 1

    # Food position
    # generate number with 20 step to align with the snake grid
    foodx = random.randrange(0, dis_width - snake_block + 1, 20)
    foody = random.randrange(0, dis_height - snake_block + 1, 20)

    while is_run:
        # Game over screen
        while is_game_over:
            dis.fill(GRAY)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            draw_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False
                    is_game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        is_run = False
                        is_game_over = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = snake_block

        # Check boundaries
        if x >= dis_width or x < 0 or y >= dis_height or y < 0:
            is_game_over = True

        # Update position
        x += x_change
        y += y_change
        dis.fill(GRAY)

        # Draw food
        pygame.draw.rect(dis, GREEN, [foodx, foody, snake_block, snake_block])

        # Update snake
        snake_Head = (x, y)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0] # remove the first element of the list -> delete the last of tail of the snake
        
        # Check collision with itself
        for coord in snake_List[:-1]:
            if coord == snake_Head:
                is_game_over = True

        draw_snake(snake_block, snake_List)
        draw_score(Length_of_snake - 1)

        pygame.display.update()

        # Check food collision with snake
        if x == foodx and y == foody:
            foodx = random.randrange(0, dis_width - snake_block + 1, 20)
            foody = random.randrange(0, dis_height - snake_block + 1, 20)
            print(foodx, foody)
            Length_of_snake += 1

            # increase the speed of the snake as the snake eats more food
            global snake_speed
            snake_speed += 1

        # setting the fps of the game
        clock.tick(snake_speed)

# Start game
gameLoop()
