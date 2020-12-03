# DSA Term Project
# Ayesha Syed

import random
import pygame
pygame.font.init() 
from pygame import mixer
import os
# ------------------------------Constants------------------------------------------------------------------

clock = pygame.time.Clock()

#-------------Total window-------------------------------- 
screen = pygame.display.set_mode((1000, 700)) 

#-------------Title---------------------------------------
pygame.display.set_caption("ULTIMATE SUDOKU") 
background = pygame.image.load("snow-background.jpg")

b1= [[7, 8, 0, 4, 0, 0, 1, 2, 0],
     [6, 0, 0, 0, 7, 5, 0, 0, 9],
     [0, 0, 0, 6, 0, 1, 0, 7, 8],
     [0, 0, 7, 0, 4, 0, 2, 6, 0],
     [0, 0, 1, 0, 5, 0, 9, 3, 0],
     [9, 0, 4, 0, 6, 0, 0, 0, 5],
     [0, 7, 0, 3, 0, 0, 0, 1, 2],
     [1, 2, 0, 0, 0, 7, 4, 0, 0],
     [0, 4, 9, 2, 0, 6, 0, 0, 7]]

b2= [[0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]]

boardlist=[b1,b2]
b= random.choice(boardlist)
    
board = [[] for i in range(len(b[0]))]
for i in range(len(b[0])):
    for j in range(len(b)):
        board[i].append(b[j][i])
# ------------------------------Functions------------------------------------------------------------------

def theme():
    # initialize
    pygame.mixer.pre_init()
    pygame.mixer.init()
    # start playing the background music
    pygame.mixer.music.load('To Build a Home - The Cinematic Orchestra.mp3')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)
    pygame.event.wait()
# theme()	
   
#--------------Intro screen-------------------------------------------------

def splashScreen():
    global game
    game = True
    screen.blit(background, (0,0))
    greet = pygame.font.SysFont("monsterret", 60).render('Welcome To Ultimate Sudoku!', True, (0,0,0))
    screen.blit(greet, [200,250])
    instructions = pygame.font.SysFont("monsterret", 30).render('Press Any Key To Enter', True, (0,0,0))
    screen.blit(instructions, [390,300])
    pygame.display.update()
	# time duration of splash screen
    # clock.tick(2)
    delay = True
    while delay:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                game = True
                delay = False
            if event.type == pygame.QUIT: 
                game = False
                delay = False


def currentPosition(): 
    for i in range(2): 
        # we use range of 2 to draw 2 horizontal and 2 vertical lines
        # line(surface, color, start_pos, end_pos, width)
        # 500/9 is size of one box
        # horizontal lines
        # xPos and yPos change as user presses key right, left, up, down
        pygame.draw.line(screen, (255, 0, 0), (xPos * (500/9)-3+30, (yPos + i)*(500/9)+30), (xPos * (500/9) + (500/9) + 3+30, (yPos + i)*(500/9)+30), 7) 
        # vertical lines
        pygame.draw.line(screen, (255, 0, 0), ( (xPos + i)* (500/9)+30, yPos * (500/9)+30 ), ((xPos + i) * (500/9)+30, yPos * (500/9) + (500/9)+30), 7) 

def gameBoard(): 
    for i in range (9): 
        for j in range (9):
            if board[i][j] != 0: 

#--------------Fill box with numbers specified----------------------------- 
                screen.blit(pygame.font.SysFont("monsterret", 35) .render(str(board[i][j]), 1, (0, 0, 0)), (i * (500/9) + 15+30, j * (500/9) + 15+30)) 


#--------------Draw horizontal and vertical lines on board-----------------
    count = 0
    a = (500/9)
    for i in range(10):
        if count % 3 == 0 and i != 0 and i != 9:
            count += 1 
            widthL = 5
        else: 
            count += 1
            widthL = 2
        pygame.draw.line(screen, (0, 0, 0), (30, i*a+30), (530, i*a+30), widthL) 
        pygame.draw.line(screen, (0, 0, 0), (i*a+30, 30), (i*a+30, 530), widthL)
    return board

#--------------Check cols, rows, and subgrids---------------------------------------------

def validSoln(board, i, j, tryValue):
    subgridI = i//3 * 3 # tells the row address of the 3X3 box as 0,1,2
    subgridJ = j//3 * 3 # tells the column address of the 3X3 box as 0,1,2
    # input number (tryValue) must not exist in same col or row
    for k in range(9): 
        col = board[i][k]
        row = board[k][j]
        if col== tryValue: 
            return False
        if row== tryValue: 
            return False
    # input number (tryValue) must not exist in same subgrid
    for i in range(subgridI, subgridI + 3): 
        for j in range (subgridJ, subgridJ + 3):
            boardLocation =  board[i][j]
            if boardLocation== tryValue: 
                return False
            else:
                return True

#--------------insert solution if valid---------------------------------------------

def insertSoln():
    global userInput
    if userInput != 0:             
        inputVal = pygame.font.SysFont("monsterret", 35).render(str(userInput), 1, (0, 0, 0))
        screen.blit(inputVal, (xPos * 500/9 + 45, yPos * 500/9 + 45)) 
        if validSoln(board, int(xPos), int(yPos), userInput)== True: # if input at this position is valid, it will be inserted in next step
            board[int(xPos)][int(yPos)]= userInput # input inserted
        else: 
            board[int(xPos)][int(yPos)]= 0 #  if input is not valid, position will be empty or '0'
    userInput = 0
        
 
#--------------backtracking algorithm/ game solver----------------------------------

def solverAlgo(board, i, j): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            os._exit(1)
    while board[i][j]!= 0: 
        if i < (len(board)-1): 
            i+= 1
        elif i == (len(board)-1) and j < (len(board)-1): 
            i = 0
            j+= 1
        elif i == (len(board)-1) and j == (len(board)-1): 
            return True
    pygame.event.pump()     
    for boardPos in range(1, 10): # numbers to be input must be from 1 to 9
        if validSoln(board, i, j, boardPos)== True: 
            board[i][j]= boardPos # if input is valid, it is inserted in board
            screen.blit(background, (0,0))
            solving = pygame.font.SysFont("monsterret", 50).render('Backtracking is working', True, (0,0,0))
            solving1 = pygame.font.SysFont("monsterret", 50).render('its magic...', True, (0,0,0))
            screen.blit(solving, [540,60])
            screen.blit(solving1, [540,100])
            gameBoard()
            currentPosition() 
            pygame.display.update() 
            # pygame.time.delay(20) 
            if solverAlgo(board, i, j)== True: 
                return True
            else: 
                board[i][j]= 0
            screen.blit(background, (0,0))
            solving = pygame.font.SysFont("monsterret", 50).render('Backtracking is working', True, (0,0,0))
            solving1 = pygame.font.SysFont("monsterret", 50).render('its magic...', True, (0,0,0))
            screen.blit(solving, [540,60])
            screen.blit(solving1, [540,100])
            gameBoard() 
            currentPosition()  
            pygame.display.update() 
            # pygame.time.delay(50)    
    return False

#--------------x and y positions---------------------------------------------

xPos = 0
yPos = 0

# ------------------------------Game Running------------------------------------------------------------------
# val is user input
splashScreen()
userInput = 0
boxSelected = False
while game: 
	# background color 
    screen.fill((255, 255, 255))
    screen.blit(background, (0,0))
    instructions = pygame.font.SysFont("monsterret", 37).render('Instructions:', True, (0,0,0))
    instructions1 = pygame.font.SysFont("monsterret", 37).render('Place values that do not exist in', True, (0,0,0))
    instructions2 = pygame.font.SysFont("monsterret", 37).render('the same row, column, or subgrid', True, (0,0,0))
    instructions3 = pygame.font.SysFont("monsterret", 37).render('Press "r" to reset the game', True, (0,0,0))
    instructions4 = pygame.font.SysFont("monsterret", 37).render('Press "s" to see the solution', True, (0,0,0))
    instructions5 = pygame.font.SysFont("monsterret", 37).render('Press "x" to exit', True, (0,0,0))
    instructions6 = pygame.font.SysFont("monsterret", 50).render('Have fun!', True, (0,0,0))
    screen.blit(instructions, [540,60]) 
    screen.blit(instructions1, [540,100]) 
    screen.blit(instructions2, [540,140]) 
    screen.blit(instructions3, [540,180]) 
    screen.blit(instructions4, [540,220]) 
    screen.blit(instructions5, [540,260]) 
    screen.blit(instructions6, [540,300])
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            game = False	 
        if event.type == pygame.KEYDOWN:
            boxSelected = True
            if event.key == pygame.K_LEFT:
                xPos = xPos - 1
            if event.key == pygame.K_RIGHT:
                xPos = xPos + 1
            if event.key == pygame.K_UP:
                yPos = yPos - 1
            if event.key == pygame.K_DOWN:
                yPos = yPos + 1
            if event.key == pygame.K_1: 
                userInput = 1
            if event.key == pygame.K_2: 
                userInput = 2    
            if event.key == pygame.K_3: 
                userInput = 3
            if event.key == pygame.K_4: 
                userInput = 4
            if event.key == pygame.K_5: 
                userInput = 5
            if event.key == pygame.K_6: 
                userInput = 6 
            if event.key == pygame.K_7: 
                userInput = 7
            if event.key == pygame.K_8: 
                userInput = 8
            if event.key == pygame.K_9: 
                userInput = 9 
            if event.key == pygame.K_x:
                os._exit(1) 
            if event.key == pygame.K_r:
                board = [[] for i in range(len(b[0]))]
                for i in range(len(b[0])):
                    for j in range(len(b)):
                        board[i].append(b[j][i])
                gameBoard()
            if event.key == pygame.K_s:
                board = [[] for i in range(len(b[0]))]
                for i in range(len(b[0])):
                    for j in range(len(b)):
                        board[i].append(b[j][i])
                gameBoard()
                solverAlgo(board, 0, 0)
    gameBoard() 
    
    if userInput != 0:
        insertSoln()
        
    if boxSelected:
        currentPosition() 
    pygame.display.update()  
pygame.quit()	 