import pygame
import sys
import numpy as np

#game constants
screenSize = 900
tileSize = 20
backgroundColor = (0, 0, 0) # black
cellColor = (250, 250, 250) # white
pygame.init()
screen = pygame.display.set_mode((600, 630))
pygame.display.set_caption('Convay\'s Game Of Life') # window title
clock = pygame.time.Clock()
grid = np.random.choice(a=[0, 1], size=(35, 25)) # a matrix of zeroes and random ones with a size
fps = 10
count = 0 # number of movements made

# conditions of the game
def life(x, y, grid):
    neighbours = np.sum(grid[x - 1: x + 2, y - 1: y + 2]) - grid[x, y]
    if grid[x, y] == 1 and not 2 <= neighbours <= 3: # a living cell (1) and has no 2 or 3 neighbors = dies
        return 0
    elif neighbours == 3: # if a cell has three neighbors live
        return 1
    return grid[x, y]


# game commands
paused=True
while paused:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # if we press escape the game closes
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:  # if we press r the game restart
                grid = np.random.choice(a=[0, 1], size=(26, 26 ))
                count = 0
            elif event.key == pygame.K_p: # if we press p we pause the game
                grid = np.random.choice(a=[0, 1], size=(0, 0))
            elif event.key == pygame.K_SPACE:  # if we press space the game start
                grid= np.random.choice(a=[0, 1], size=(26, 26))
                count = 0

    # Back ground color
    screen.fill(backgroundColor)

    # add text within the game, pressing a button on the keyboard will have function in the game
    text1 ="Game of Life"
    text2 = "Press the R  button to restart"
    text3 = "Press the ESCAPE button to close the game"
    text4 = "Press the SPACE button to start"
    text5 = "Press the P  button to pause"
    text6 = "count= " + str(count)    #show number of repetitions on the screen
    fuente = pygame.font.Font(None, 30)   #font of the game
    mensaje1= fuente.render(text1, 1, (250, 250, 250))
    screen.blit(mensaje1,(20,510))
    mensaje2= fuente.render(text4,1,(250,250,250))
    screen.blit(mensaje2, (20, 540))
    mensaje3 = fuente.render(text3, 1, (250, 250, 250))
    screen.blit(mensaje3, (20, 560))
    mensaje4 = fuente.render(text5, 1, (250, 250, 250))
    screen.blit(mensaje4, (20, 580))
    mensaje5 = fuente.render(text2, 1, (250, 250, 250))
    screen.blit(mensaje5, (20, 600))
    mensaje6 = fuente.render(text6, 1, (250, 250, 250))
    screen.blit(mensaje6, (400, 510))


# what makes the game work and add new cells
    newgrid = np.copy(grid)
    for (x, y), value in np.ndenumerate(grid):
        newgrid[x, y] = life(x, y, grid)
        if newgrid[x, y] == 1:
            pygame.draw.rect(screen, cellColor, (tileSize * (x - 1), tileSize * (y - 1), tileSize, tileSize), 0)
    grid = newgrid
    count += 1

    pygame.display.update()
    msElapsed = clock.tick(fps)