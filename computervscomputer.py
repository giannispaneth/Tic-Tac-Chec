# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:52:36 2023

@author: John
"""


import time
import pygame
from pygame.locals import *
import sys
import os
import minimaxfunctions
from minimaxfunctions import all_possible_moves
from minimaxfunctions import best_move2
import classes
from classes import bishop,pawn,knight,rook
BLACK = (0,0,0)
BLUE = (222,222,222)
BLUE = (222,222,222)
selection=0
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 30)
gameDisplay= pygame.display.set_mode((1000,1000))
pygame.display.set_caption('tic tac chec')
running=True
gameDisplay.fill(BLUE)
imageDimensions=[0,0,0,0,0,0,0,0]
image=[0,0,0,0,0,0,0,0]
buttonDown=2
initialcount=0
image[0] = pygame.image.load('C:/Users/John\Desktop/bishopB2.png')
image[1] = pygame.image.load('C:/Users/John\Desktop/pawnB2.png')
image[2] = pygame.image.load('C:/Users/John\Desktop/rookB2.png')
image[3] = pygame.image.load('C:/Users/John\Desktop/KnightB2.png')
image[4] = pygame.image.load('C:/Users/John\Desktop/bishopW2.png')
image[5] = pygame.image.load('C:/Users/John\Desktop/pawnW2.png')
image[6] = pygame.image.load('C:/Users/John\Desktop/rookW2.png')
image[7] = pygame.image.load('C:/Users/John\Desktop/KnightW2.png')
imageDimensions[0]=image[0].get_rect()
imageDimensions[1]=image[1].get_rect()
imageDimensions[2]=image[2].get_rect()
imageDimensions[3]=image[3].get_rect()
imageDimensions[4]=image[4].get_rect()
imageDimensions[5]=image[5].get_rect()
imageDimensions[6]=image[6].get_rect()
imageDimensions[7]=image[7].get_rect()

choseBlack = myFont.render('    Black', False, (255, 0, 0))
chosewhite= myFont.render('   White', False, (0, 0, 0))
finalWinner= myFont.render('Computer Wins', False, (0, 0, 0))
blackBoxChose=pygame.Rect(200,400,200,100)
whiteBoxChose=pygame.Rect(600,400,200,100)


winnerboxchose=pygame.Rect(400,400,400,200)
imageDimensions[0].x=324
imageDimensions[0].y=124
imageDimensions[1].x=424
imageDimensions[1].y=124
imageDimensions[2].x=524
imageDimensions[2].y=124
imageDimensions[3].x=624
imageDimensions[3].y=124
imageDimensions[4].x=324
imageDimensions[4].y=624
imageDimensions[5].x=424
imageDimensions[5].y=624
imageDimensions[6].x=524
imageDimensions[6].y=624
imageDimensions[7].x=624
imageDimensions[7].y=624
finalSpotx=[324,424,524,624,324,424,524,624]
finalSpoty=[124,124,124,124,624,624,624,624]
x=[324,424,524,624,324,424,524,624]
y=[224,224,224,224,224,224,224,224]
w=[350,450,550,650,359,450,550,650]
z=[250,250,250,250,250,250,250,250]
t=[350,450,550,650,350,4250,550,650]
u=0
r=5
l=1
o=[150,150,150,150,650,650,650,650]
piecesOnBoard=[0,0,0,0,0,0,0,0]
max1=[10000,10000,10000,10000,10000,10000,10000,10000]
outOfBoardx={
    0:324,
    1:424,
    2:524,
    3:624,
    4:324,
    5:424,
    6:524,
    7:624

}
outOfBoardy={
    0:124,
    1:124,
    2:124,
    3:124,
    4:624,
    5:624,
    6:624,
    7:624
}
def move_pieces(mouse1,mouse2):
    global k,r,image
    gameDisplay.blit(image[k],(mouse1,mouse2))
def board_winner():
    pygame.draw.rect(gameDisplay,(255,255,0),(300,700,400,200))
def board_before_choice():
   
    pygame.draw.rect(gameDisplay,(255,255,0),(200,400,200,100))
    pygame.draw.rect(gameDisplay,(255,255,0),(600,400,200,100))
levelWhite=[]
levelBlack=[]
for i in range(1,5):
    levelWhite.append(pygame.Rect(800,60*i,100,50))
    levelBlack.append(pygame.Rect(900,60*i,100,50))
def board_after_choice():
    global levelB,levelW
    for i in range(1, 5):
        for j in range(1, 5):
            pygame.draw.rect(gameDisplay, [((i + j) % 2) * 255, ((i + j) % 2) * 255, ((i + j) % 2) * 255],
                             (100 * i + 200, 100 * j + 100, 100, 100))
    pygame.draw.rect(gameDisplay,[127,127,127],(800,0,90,50))
    pygame.draw.rect(gameDisplay,[127,127,127],(900,0,90,50))
    difficultyWhite = myFont.render('Level ', False, (0, 0,0))
    difficultyBlack = myFont.render('Level ', False, (255, 255,255))
    gameDisplay.blit(difficultyWhite,(910,5))
    gameDisplay.blit(difficultyBlack,(810,5))
    for i in range(1,5):
        
        difficultyBlack = myFont.render(str(i), False, (127, 127,127))
        difficultyWhite = myFont.render(str(i), False, (127, 127,127))
        if i==levelW:
            pygame.draw.rect(gameDisplay,[100,255,100],(800,60*i,100,50))
        else:
            pygame.draw.rect(gameDisplay,[255,255,255],(800,60*i,100,50))
        gameDisplay.blit(difficultyBlack,(845,60*i+5))
        if i==levelB:
            pygame.draw.rect(gameDisplay,[100,255,100],(900,60*i,100,50))
        else:
            pygame.draw.rect(gameDisplay,[0,0,0],(900,60*i,100,50))
        
        gameDisplay.blit(difficultyWhite,(945,60*i+5))
def transform_from_matrix():
    global imageDimensions, counter, selectedPiece, grid,image,gameDisplay,finalSpotx,finalSpoty,t,o,piecesOnBoard,moves
    dictionx={
       0:324,
       1:424,
       2:524,
       3:624
    }
    dictiony={
       0:224,
       1:324,
       2:424,
       3:524
    }
    diction3={
       ('B','B'):0,
       ('P','B'):1,
       ('R','B'):2,
       ('K','B'):3,
       ('B','W'):4,
       ('P','W'):5,
       ('R','W'):6,
       ('K','W'):7
    }
    diction4={
       0:3,
       1:1,
       2:0,
       3:2,
       4:3,
       5:1,
       6:0,
       7:2
    }
    outOfBoardx={
        0:324,
        1:424,
        2:524,
        3:624,
        4:324,
        5:424,
        6:524,
        7:624
    }
    outOfBoardy={
        0:124,
        1:124,
        2:124,
        3:124,
        4:624,
        5:624,
        6:624,
        7:624
    }
    visualMovement=diction3[moves[2],moves[3]]
    lastY=dictiony[moves[0]]
    lastX=dictionx[moves[1]]
    firstX=imageDimensions[visualMovement].x
    firstY=imageDimensions[visualMovement].y
    for i in range(0,8):
        piecesOnBoard[i]=0
    for i in [0,1,2,3]:
        for j in [0,1,2,3]:
            if grid[i][j]!=('_','_') :
                    k1=diction3[grid[i][j]]
                    piecesOnBoard[k1]=1
                    imageDimensions[k1].centerx=dictionx[j]+26
                    imageDimensions[k1].centery=dictiony[i]+26
                    
                    t[k1]=imageDimensions[k1].x
                    o[k1]=imageDimensions[k1].y
                    finalSpotx[k1]=imageDimensions[k1].x
                    finalSpoty[k1]=imageDimensions[k1].y
                    gameDisplay.blit(image[k1],(dictionx[j],dictiony[i]))
    for k1 in range(0,8):
        if piecesOnBoard[k1]==0:
            imageDimensions[k1].centerx=outOfBoardx[k1]+26
            imageDimensions[k1].centery=outOfBoardy[k1]+26
            t[k1]=imageDimensions[k1].x
            o[k1]=imageDimensions[k1].y
            finalSpotx[k1]=imageDimensions[k1].x
            finalSpoty[k1]=imageDimensions[k1].y
            gameDisplay.blit(image[k1],(outOfBoardx[k1],outOfBoardy[k1]))
    x1=firstX
    y1=firstY
    for i in range(0,300):
        x1+=(lastX-firstX)/300
        y1+=(lastY-firstY)/300
        gameDisplay.fill(BLUE)
        board_after_choice()
        gameDisplay.blit(image[visualMovement],(x1,y1))
        for k1 in range(0,8):
            if k1!=visualMovement:
                gameDisplay.blit(image[k1],(finalSpotx[k1],finalSpoty[k1]))
                
        pygame.display.update()
        
                
def transform_from_visual(x,y,k):
    global imageDimensions,selectedPiece,grid,choice,turn1
    dictionx={
        324:0,
        424:1,
        524:2,
        624:3
    }
    dictiony={
        224:0,
        324:1,
        424:2,
        524:3
    }
    kind_and_color={
        0:'B',
        1:'P',
        2:'R',
        3:'K',
        4:'B',
        5:'P',
        6:'R',
        7:'K'
    }
    diction4={
        0:3,
        1:1,
        2:0,
        3:2,
        4:3,
        5:1,
        6:0,
        7:2
    }
    am1=[0,0,0,0]
    am2=[0,0,0,0]
    grid = [[("_", "_")]*4 for n in range(4)]
    for i in [350, 450, 550, 650]:
        for j in [250, 350, 450, 550]:
            for k2 in [0,1,2,3,4,5,6,7]:
                if imageDimensions[k2].centerx==i and imageDimensions[k2].centery==j and k2<4:
                    
                    grid[dictiony[j-26]][dictionx[i-26]]=(kind_and_color[k2],'B')
                elif imageDimensions[k2].centerx==i and imageDimensions[k2].centery==j:
                    
                    grid[dictiony[j-26]][dictionx[i-26]]=(kind_and_color[k2],'W')
    
   
    
    if k<4 and selectedPiece!=9:
        if turn1<=6:
            am1[0]=minimaxfunctions.not_in_board_moves('R','B',grid)
            am1[1]=minimaxfunctions.not_in_board_moves('P','B',grid)
            am1[2]=minimaxfunctions.not_in_board_moves('K','B',grid)
            am1[3]=minimaxfunctions.not_in_board_moves('B','B',grid)
        else:
            am1=all_possible_moves('B',grid)  
        
        for a in am1[diction4[k]]:
            if dictiony[y-26]==a[0] and dictionx[x-26]==a[1] :
                for i in range(0,4):
                    for j in range(0,4):
                        
                        if kind_and_color[k]==grid[i][j][0] and grid[i][j][1]=='B':
                            grid[i][j]=('_','_')
                            break
                        
                        
        
                grid[dictiony[y-26]][dictionx[x-26]]=(kind_and_color[k],'B')
                print('yes')
                minimaxfunctions.printg(grid)
            
        
                return True
    elif k>=4 and k<8 and selectedPiece!=9:
        if turn1<=6:
            am2[0]=minimaxfunctions.not_in_board_moves('R','W',grid)
            am2[1]=minimaxfunctions.not_in_board_moves('P','W',grid)
            am2[2]=minimaxfunctions.not_in_board_moves('K','W',grid)
            am2[3]=minimaxfunctions.not_in_board_moves('B','W',grid)
        else:
            am2=all_possible_moves('W',grid)  
        for a in am2[diction4[k]]:
            if dictiony[y-26]==a[0] and dictionx[x-26]==a[1] :
                for i in range(0,4):
                    for j in range(0,4):
                        if kind_and_color[k]==grid[i][j][0] and grid[i][j][1]=='W':
                            grid[i][j]=('_','_')
                            break
                grid[dictiony[y-26]][dictionx[x-26]]=(kind_and_color[k],'W')
                print('yes')
                minimaxfunctions.printg(grid)
            
        
                return True  
    
    return False  



levelW=2
levelB=2
computer='NC'
turn1=1
turn=0      
selection=0
selectedPiece=9
buttonDown=2
choice='NC'
grid = [[("_", "_")]*4 for n in range(4)]
deadTime=True
while running:
    if minimaxfunctions.is_winning(grid, 'W'):
        winner='white wins'
        selection=1
        finalWinner= myFont.render('     White Wins', False, (0, 0, 0))
    if minimaxfunctions.is_winning(grid, 'B'):
        winner='black wins'
        finalWinner= myFont.render('     Black Wins', False, (0, 0, 0))
        selection=1
    if selection==1:
        board_winner()
        gameDisplay.blit(finalWinner,(400,770))
        
    pygame.display.update()
  
    if selection==1:
        pygame.time.wait(3000)
        deadTime=True
        
        selection=0
        
        turn1=1
        grid = [[("_", "_")]*4 for n in range(4)]
        imageDimensions[0].x=324
        imageDimensions[0].y=124
        imageDimensions[1].x=424
        imageDimensions[1].y=124
        imageDimensions[2].x=524
        imageDimensions[2].y=124
        imageDimensions[3].x=624
        imageDimensions[3].y=124
        imageDimensions[4].x=324
        imageDimensions[4].y=624
        imageDimensions[5].x=424
        imageDimensions[5].y=624
        imageDimensions[6].x=524
        imageDimensions[6].y=624
        imageDimensions[7].x=624
        imageDimensions[7].y=624
        finalSpotx=[324,424,524,624,324,424,524,624]
        finalSpoty=[124,124,124,124,624,624,624,624]
        x=[324,424,524,624,324,424,524,624]
        y=[224,224,224,224,224,224,224,224]
        w=[350,450,550,650,359,450,550,650]
        z=[250,250,250,250,250,250,250,250]
        t=[350,450,550,650,350,4250,550,650]
        o=[150,150,150,150,650,650,650,650]
        piecesOnBoard=[0,0,0,0,0,0,0,0]
        max1=[10000,10000,10000,10000,10000,10000,10000,10000]
    
    if selection==0 and deadTime:    
        gameDisplay.fill(BLUE)
        board_after_choice()
        deadTime=False
                
    POSITION = pygame.mouse.get_pos()
    if  buttonDown==1 and selection==0:
        for i in range(1,5):
            if levelBlack[i-1].collidepoint(POSITION):
                levelB=i
                print(levelB)
            if levelWhite[i-1].collidepoint(POSITION):
                levelW=i
                print(levelW)
       
        
        
        
   
       
            
    if  selection==0 :
        for k in range(0,8):
            move_pieces(finalSpotx[k],finalSpoty[k])
        pygame.display.update()
        if turn1 %2==1:
            computer='W'
            level=levelW
        else:
            computer='B'
            level=levelB
        moves=minimaxfunctions.best_move(grid,level,computer,-10000,10000,turn1)
        
        grid=minimaxfunctions.update_grid(grid, moves[0], moves[1], moves[2], moves[3])
       
        transform_from_matrix()
        print(levelB)
        print(levelW)
        turn1+=1
        
        deadTime=False
        for k in range(0,8):
            move_pieces(finalSpotx[k],finalSpoty[k])
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:    #Remember to use: from pygame.locals import *
            buttonDown=1
        if event.type == MOUSEBUTTONUP:    
            buttonDown=0
        if event.type == pygame.QUIT:
            
            running = False
            pygame.quit()

            sys.exit()

        
    