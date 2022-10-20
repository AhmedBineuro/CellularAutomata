import pygame
import random
pygame.init()
SCREEN_W = 1000
SCREEN_H = 800
STEP_TIME = 5
GROW = 100
GCOLUMN = 100

tick = 60
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
cellSize = 5
cellsInRow = int(SCREEN_W/cellSize)
cellsInColumn = int(SCREEN_H/cellSize)
clock = pygame.time.Clock()
clock.tick(tick)
cellGrid = []
pause = True
stepTime = STEP_TIME
###CELL CLASS###


class cell:
    def __init__(self, cS, x, y):
        self.cellSize = cS
        self.x = x
        self.y = y
        self.occupied = False
        self.switch = False
        self.update = False

    def draw(self):
        c = (255, 255, 255)
        if (self.occupied):
            c = (140, 120, 40)
        if pause:
            pygame.draw.rect(screen, c, pygame.Rect(
                self.x-self.cellSize/2, self.y-self.cellSize/2, self.cellSize, self.cellSize), 0, int(cellSize))
        else:
            pygame.draw.rect(screen, c, pygame.Rect(
                self.x-self.cellSize/2, self.y-self.cellSize/2, self.cellSize, self.cellSize))

    def clickResolve(self, x, y):
        xCondition = (x >= (self.x-cellSize/2)) and (x <= (self.x+cellSize/2))
        yCondition = (y >= (self.y-cellSize/2)) and (y <= (self.y+cellSize/2))
        if xCondition and yCondition:
            self.occupied = not self.occupied


class grid:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.grid = []
        for i in range(row):
            temp = []
            for j in range(col):
                x = (SCREEN_W*2/3)-(cellSize*self.col/2) + (cellSize*j)
                y = (SCREEN_H/2)-(cellSize*self.row/2) + (cellSize*i)
                temp.append(cell(cellSize, x, y))

            self.grid.append(temp.copy())

    def draw(self):
        for i in range(self.row):
            for j in range(self.col):
                self.grid[i][j].draw()

    def checkClick(self, x, y):
        for i in range(self.row):
            for j in range(self.col):
                self.grid[i][j].clickResolve(x, y)

    def clear(self):
        for i in range(self.row):
            for j in range(self.col):
                self.grid[i][j].occupied = False
                self.grid[i][j].update = False

    def doStep(self):
        for i in range(self.row):
            for j in range(self.col):
                count = 0
                # Check Left
                if j > 0:
                    if self.grid[i][j-1].occupied:
                        count += 1
                # Check Right
                if j < self.col-1:
                    if self.grid[i][j+1].occupied:
                        count += 1
                # Check Up
                if i > 0:
                    if self.grid[i-1][j].occupied:
                        count += 1
                    # Check Up Left
                    if j > 0:
                        if self.grid[i-1][j-1].occupied:
                            count += 1
                    # Check Up Right
                    if j < self.col-1:
                        if self.grid[i-1][j+1].occupied:
                            count += 1
                # Check Down
                if i < self.row-1:
                    if self.grid[i+1][j].occupied:
                        count += 1
                    # Check Down Left
                    if j > 0:
                        if self.grid[i+1][j-1].occupied:
                            count += 1
                    # Check Down Right
                    if j < self.col-1:
                        if self.grid[i+1][j+1].occupied:
                            count += 1
                # Oringinal Connway GOL
                if (self.grid[i][j].occupied and (count < 2 or count > 3)) or ((not self.grid[i][j].occupied) and count == 3):
                    self.grid[i][j].update = True

                # Slime mold
                # if (not self.grid[i][j].occupied) and (count >= 2 and count <= 4):
                #     if random.random() <= 0.7:
                #         self.grid[i][j].update = True
                # elif (self.grid[i][j].occupied and (count < 2 or count > 4)):
                #     self.grid[i][j].update = True

    def updateCells(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.grid[i][j].update:
                    self.grid[i][j].occupied = not self.grid[i][j].occupied
                    self.grid[i][j].update = False


g = grid(GCOLUMN, GROW)


################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            g.checkClick(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_c:
                g.clear()
    if not pause:
        if stepTime == 0:
            g.doStep()
            g.updateCells()
            stepTime = STEP_TIME
        else:
            stepTime -= 1
    screen.fill((0, 0, 0, 0.2))
    g.draw()
    clock.tick(tick)
    pygame.display.update()
