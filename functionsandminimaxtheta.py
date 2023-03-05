import time
import os
import sys
import pygame
import classes
import random
import csv
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

global ppW,ppB,kp,rp,bp, changeside
ppU = [[-2, -2, -2, -2], [-1, -1, -1, -1], [0, 0, 0, 0], [1, 1, 1, 1]]
ppD = [[1, 1, 1, 1], [0, 0, 0, 0], [-1, -1, -1, -1], [-2, -2, -2, -2]]
kp = [[2, 2, 2, 2], [2, 3, 3, 2], [2, 3, 3, 2], [2, 2, 2, 2]]
rp = [[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4]]
bp = [[2, 2, 2, 2], [2, 3, 3, 2], [2, 3, 3, 2], [2, 2, 2, 2]]
changeside=[1,1]
def evaluate_figures(grid, color):
    points = 0
    
    if changeside[0]==1:
        ppB = ppD
    else:
        ppB = ppU
    if changeside[1]==1:
        ppW = ppU
    else:
        ppW = ppD
    if color == 'W':
        color2 = 'B'
    else:
        color2 = 'W'

    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            if grid[i][j] == ('P', color):
                if color == 'W':
                    points = points + ppW[i][j]
                else:
                    points = points + ppB[i][j]
            if grid[i][j] == ('R', color):
                points = points + rp[i][j]
            if grid[i][j] == ('K', color):
                points = points + kp[i][j]
            if grid[i][j] == ('B', color):
                points = points + bp[i][j]
            if grid[i][j] == ('P', color2):
                if color2 == 'W':
                    points = points - ppW[i][j]
                else:
                    points = points - ppB[i][j]
            if grid[i][j] == ('R', color2):
                points = points - rp[i][j]
            if grid[i][j] == ('K', color2):
                points = points - kp[i][j]
            if grid[i][j] == ('B', color2):
                points = points - bp[i][j]
    return points


def is_winning(grid, color):

    i = 0
    j = 0
    k = 0
    l = 0
    for x in [0, 1, 2,3]:

        if grid[x][x][1] == color:
            k = k+1
            if k == 4:
                return True
        else:
            k = 0

        if grid[3-x][x][1] == color:
            l = l+1
            if l == 4:
                return True
        else:
            l = 0
        for y in [0, 1, 2,3]:

            if grid[x][y][1] == color:
                i = i+1
                if i == 4:
                    return True
            else:
                i = 0
            if grid[y][x][1] == color:
                j = j+1
                if j == 4:
                    return True
            else:
                j = 0
        i = 0
        j = 0
    return False

def row_eval_col_eval(grid, color, z):
    points = 0
    for x in range(0, 4, 1):
        k = 0
        l = 0
        for y in range(0, 4, 1):
            if z == True:
                i = x
                j = y
            else:
                i = y
                j = x
            if grid[i][j][1] == color:
                l = l+1
            elif grid[i][j][1] != color and grid[i][j][1] != "_":
                k = k+1
        if l == 2:
            points = points+8
        if l == 3:
            points = points+50
        if l == 4:
            points = 1000
        if k == 2:
            points = points - 8
        if k == 3:
            points = points - 50
        if k == 4:
            points = -1000
    return points


def diag_eval(grid, color, z):
    points = 0
    k = 0
    l = 0
    if z == 0:
        r = 1
    else:
        r = -1
    for i, j in zip([0, 1, 2, 3], [z+0*r, z+1*r, z+2*r, z+3*r]):
        if grid[i][j][1] == color:
            l = l+1
        elif grid[i][j][1] != color and grid[i][j][1] != "_":
            k = k+1
    if l == 2:
        points = points+8
    if l == 3:
        points = points+50
    if l == 4:
        points = 1000
    if k == 2:
        points = points - 8
    if k == 3:
        points = points - 50
    if k == 4:
        points = -1000
    return points


def evaluate_board(grid, color):
    points = 0
    a = row_eval_col_eval(grid, color, z=True)
    points = points+a
    a = row_eval_col_eval(grid, color, z=False)
    points = points+a
    a = diag_eval(grid, color, 3)
    points = points+a
    a = diag_eval(grid, color, 0)
    points = points+a
    a = evaluate_figures(grid, color)
    points = points+a
    return points


def not_in_board_moves(kind, color, grid):
    k = 0

    for i in range(0, 4, 1):
        for j in range(0, 4, 1):
            if grid[i][j] == (kind, color):
                k = 1
    if k == 0:
        moves = []

        for i in range(0, 4, 1):
            for j in range(0, 4, 1):
                if grid[i][j] == ('_', '_'):
                    moves.append([i, j])
        return moves
    else:
        moves = []
        return moves


P = [[("P", "B"), ("K", "B"), ("B", "B"), ("R", "B")], [
    ("P", "W"), ("K", "W"), ("B", "W"), ("R", "W")]]
grid = [[("_", "_")]*4 for n in range(4)]


grid1 = [[(350, 250), (450, 250), (550, 250), (650, 250)], [(350, 350), (450, 350), (550, 350), (650, 350)], [
    (350, 450), (450, 450), (550, 450), (650, 450)], [(350, 550), (450, 550), (550, 550), (650, 550)]]


def printg(grid):
    print('                 ')
    for i in range(0, 4, 1):
        print(grid[i])


def get_pawn_pos(grid, kind, color):
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            if grid[i][j] == (kind, color):
                return i, j


def all_possible_moves(color, grid):
    global changeside
    a = [0, 0, 0, 0]
    a[0] = not_in_board_moves('R', color, grid)
    a[1] = not_in_board_moves('P', color, grid)
    a[2] = not_in_board_moves('K', color, grid)
    a[3] = not_in_board_moves('B', color, grid)
    if a[0] == []:
        c, b = get_pawn_pos(grid, 'R', color)
        a[0] = classes.rook(c, b, color).valid_moves(grid)
    if a[1] == []:
        
        c, b = get_pawn_pos(grid, 'P', color)
        changeside=classes.pawn(c,b,color,changeside).change_sides(grid)
        a[1] = classes.pawn(c, b, color,changeside).valid_moves(grid)
    if a[2] == []:
        c, b = get_pawn_pos(grid, 'K', color)
        a[2] = classes.knight(c, b, color).valid_moves(grid)
    if a[3] == []:
        c, b = get_pawn_pos(grid, 'B', color)
        a[3] = classes.bishop(c, b, color).valid_moves(grid)
    return a

    return a


winning = 'yes'

while winning == 'no':
    if l == 'B':
        l = 'W'
    else:
        l = 'B'
    x, y, z = input("x,y,kind ").split()
    grid[x, y] = (kind, l)
    winning = input('say if over')


def update_grid(grid, x, y, kind, color):

    q = [[1] * 4 for n in range(4)]
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            q[i][j] = grid[i][j]
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            if q[i][j] == (kind, color):
                q[i][j] = ('_', '_')
    q[x][y] = (kind, color)

    return q
def transform_bitboards(grid):

    bitboard1 = [[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]]
    for i in [0,1,2,3]:
        for j in [0,1,2,3]:
            if grid[i][j]==('R','W'):
                bitboard1[i][j][0]=1
            if grid[i][j]==('B','W'):
                bitboard1[i][j][1]=1
            if grid[i][j]==('K','W'):
                bitboard1[i][j][2]=1
            if grid[i][j]==('P','W'):
                bitboard1[i][j][3]=1
            if grid[i][j]==('R','B'):
                bitboard1[i][j][4]=1
            if grid[i][j]==('B','B'):
                bitboard1[i][j][5]=1
            if grid[i][j]==('K','B'):
                bitboard1[i][j][6]=1
            if grid[i][j]==('P','B'):
                bitboard1[i][j][7]=1
            
    return bitboard1


def minimax(grid, depth, color, alpha, beta, maximazingPlayer):
    if depth == 0:
        req = evaluate_board(grid, color)
        return req
        print()
    if color == 'W':
        color2 = 'B'
    else:
        color2 = 'W'
    if is_winning(grid, color):
        req = evaluate_board(grid, color)
        return req
    if is_winning(grid, color2):
        req = evaluate_board(grid, color)

        return req
    if maximazingPlayer:
        maxing = -10000
        ar = all_possible_moves(color, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for posmoves in ar[i]:
                if i == 0:
                    y = 'R'
                if i == 1:
                    y = 'P'
                if i == 2:
                    y = 'K'
                if i == 3:
                    y = 'B'
                q = update_grid(grid, posmoves[0], posmoves[1], y, color)
                eval = minimax(q, depth-1, color, alpha, beta, False)
                maxing = max(maxing, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return maxing
    else:
        mining = 10000
        ar = all_possible_moves(color2, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for posmoves in ar[i]:
                if i == 0:
                    y = 'R'
                if i == 1:
                    y = 'P'
                if i == 2:
                    y = 'K'
                if i == 3:
                    y = 'B'
                q = update_grid(grid, posmoves[0], posmoves[1], y, color2)
                eval = minimax(q, depth - 1, color, alpha, beta, True)
                mining = min(mining, eval)
                beta = min(beta, eval)   
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return mining


def best_move(grid, depth, color, alpha, beta):

    maxing = -10000
    ar = all_possible_moves(color, grid)
    s = [0, 1, 2, 3]
    random.shuffle(s)
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    for i in s:
        for posmoves in ar[i]:

            if i == 0:
                y = 'R'
               
            if i == 1:
                y = 'P'
                

            if i == 2:
                y = 'K'


            if i == 3:
                y = 'B'
            q = update_grid(grid, posmoves[0], posmoves[1], y, color)

            eval = minimax(q, depth-1, color, alpha, beta, False)

            if eval > maxing:
                maxing = eval
                best_moves1 = posmoves[0]
                best_moves2 = posmoves[1]
                best_moves3 = y
            alpha = max(alpha, eval)


           
            if beta <= alpha:
                break
        if beta <= alpha:
            break
    return best_moves1, best_moves2, best_moves3, color


#spot = time.time()
# print((time.time()-spot))

sp = best_move(grid, 3, 'B', -10000, 10000)
print(sp)
al = minimax(grid, 3, 'B', -10000, 10000, True)

ase = evaluate_board(grid, 'B')
lvl=0
lvl2=3

notEnd = False
notEnd4 = False
notEnd3= True
i = 1
k=1
runit=[]
while(notEnd):
    if (i % 2) != 0:
        a = [0, 0, 0, 0]
        a = input("enter valid move").split()
        print(a)
        a[0] = int(a[0])
        a[1] = int(a[1])
        print(a)
        k2 = (a[2], a[3])
        grid[a[0]][a[1]] = k2
        printg(grid)
        i = i+1
    else:
        a = best_move(grid, 4, 'B', -10000, 10000)
        k1 = (a[2], a[3])
        grid[a[0]][a[1]] = k1
        printg(grid)
        i = i+1
while(notEnd4):
    if (i % 2) != 0:

        a = best_move(grid, 2, 'W', -100000, 100000)
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'W'):
            notEnd4 = False
    else:
        a = best_move(grid, 2, 'B', -100000, 100000)
        k1 = (a[2], a[3])
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'B'):
            notEnd4 = False
pieceValues=[0,0,0,0,0,0,0,0,0,0,0,0,0]


for j in range(0,13,1):
    pieceValues[j]=random.randrange(-10, 10,1)
winIndex=0
with open('mycsv3.csv','w',newline='') as f:
    theWriter=csv.writer(f)
    while(i!=1000001 and i!=1000002 ):
        print(i)
        if (i % 2) != 0 :
            k=k+1
            ppU = [[pieceValues[1], pieceValues[0], pieceValues[0], pieceValues[1]],
                   [pieceValues[11], pieceValues[12], pieceValues[12], pieceValues[11]],
                   [pieceValues[11],pieceValues[12], pieceValues[12],pieceValues[11]],
                   [pieceValues[1], pieceValues[0], pieceValues[0], pieceValues[1]]]
            ppD = [[pieceValues[1], pieceValues[0], pieceValues[0], pieceValues[1]],
                   [pieceValues[11], pieceValues[12], pieceValues[12], pieceValues[11]],
                   [pieceValues[11],pieceValues[12], pieceValues[12],pieceValues[11]], 
                   [pieceValues[1], pieceValues[0], pieceValues[0], pieceValues[1]]]
            kp = [[pieceValues[4], pieceValues[5], pieceValues[5], pieceValues[4]],
                  [pieceValues[5], pieceValues[6], pieceValues[6], pieceValues[5]],
                  [pieceValues[5], pieceValues[6], pieceValues[6], pieceValues[5]],
                  [pieceValues[4], pieceValues[5], pieceValues[5], pieceValues[4]]]
            rp = [[pieceValues[2], pieceValues[3], pieceValues[3], pieceValues[2]],
                  [pieceValues[3], pieceValues[7], pieceValues[7],pieceValues[3]],
                  [pieceValues[3],pieceValues[7] , pieceValues[7], pieceValues[3]],
                  [pieceValues[2], pieceValues[3], pieceValues[3], pieceValues[2]]]
            bp = [[pieceValues[8],pieceValues[9],pieceValues[9], pieceValues[8]],
                  [pieceValues[9], pieceValues[10], pieceValues[10], pieceValues[9]],
                  [pieceValues[9],pieceValues[10],pieceValues[10], pieceValues[9]],
                  [pieceValues[8], pieceValues[9], pieceValues[9], pieceValues[8]]]
            a = best_move(grid, 3, 'W', -10000, 10000)
            grid = update_grid(grid, a[0], a[1], a[2], a[3])
            i = i+1
            if is_winning(grid, 'W'):
                winIndex=winIndex+1
                notEnd = True
                theWriter.writerow([pieceValues[0],pieceValues[1],pieceValues[2], pieceValues[3],
                                    pieceValues[4],pieceValues[5],pieceValues[6], pieceValues[7],
                                    pieceValues[8],pieceValues[9],pieceValues[10],pieceValues[11],
                                    pieceValues[12],'Win white'])
                grid = [[("_", "_")]*4 for n in range(4)]
                if winIndex%20==0:
                    for j in range(0,13,1):
                        pieceValues[j]=random.randrange(-10, 10,1)
                    winIndex=0
                i=i+1
                k=0
            if k==50:
                winIndex=winIndex+1
                theWriter.writerow([pieceValues[0],pieceValues[1],pieceValues[2], pieceValues[3],
                                    pieceValues[4],pieceValues[5],pieceValues[6], pieceValues[7],
                                    pieceValues[8],pieceValues[9],pieceValues[10],pieceValues[11],
                                    pieceValues[12],'overload'])
                if winIndex%20==0:
                    for j in range(0,13,1):
                        pieceValues[j]=random.randrange(-10, 10,1)
                    
                    winIndex=0
                grid = [[("_", "_")]*4 for n in range(4)]
                i=i+1
                k=0
        else:
            ppU = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            ppD = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            kp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            rp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            bp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            a = best_move(grid, 3, 'B', -10000, 10000)
            k1 = (a[2], a[3])
            grid = update_grid(grid, a[0], a[1], a[2], a[3])
            i = i+1
            k=k+1
            if is_winning(grid, 'B'):
                winIndex=winIndex+1
                if winIndex%20==0:
                    for j in range(0,13,1):
                        pieceValues[j]=random.randrange(-10, 10,1)
                    winIndex=0
                theWriter.writerow([pieceValues[0],pieceValues[1],pieceValues[2], pieceValues[3],
                                    pieceValues[4],pieceValues[5],pieceValues[6], pieceValues[7],
                                    pieceValues[8],pieceValues[9],pieceValues[10],pieceValues[11],
                                    pieceValues[12],'Win black'])
                grid = [[("_", "_")]*4 for n in range(4)]
                k=0
                notEnd = True
            if k==50:
                winIndex=winIndex+1
                theWriter.writerow([pieceValues[0],pieceValues[1],pieceValues[2], pieceValues[3],
                                    pieceValues[4],pieceValues[5],pieceValues[6], pieceValues[7],
                                    pieceValues[8],pieceValues[9],pieceValues[10],pieceValues[11],
                                    pieceValues[12],'overload'])
                if winIndex%20==0:
                    for j in range(0,13,1):
                        pieceValues[j]=random.randrange(-10, 10,1)
                grid = [[("_", "_")]*4 for n in range(4)]
                k=0
for i in range(0,len(runit),1):               
    printg(runit[i])
df=pd.read_csv('mycsv3.csv',dtype=str,float_precision='round_trip')
df.to_csv('testpiecevalues2.csv',index=False)
