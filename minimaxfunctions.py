# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:20:32 2021

@author: John
"""

import time
import os
import sys
import classes
import random
from matplotlib import pyplot as plt
import csv
import numpy as np
import pandas as pd
global changeside
changeside=[0,1]
def evaluate_figures(grid, color):
    points = 0
    ppU=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ppD=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    if changeside[0]==1:
        ppB = ppD
    else:
        ppB = ppU
    if changeside[1]==1:
        ppW = ppU
    else:
        ppW = ppD
        
    kp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    rp = [[0, 0,0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    bp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
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
            points = points+2
        if l == 3:
            points = points+11
        if l == 4:
            points = 100
        if k == 2:
            points = points - 2
        if k == 3:
            points = points - 11
        if k == 4:
            points = -100
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
        points = points+2
    if l == 3:
        points = points+11
    if l == 4:
        points = 100
    if k == 2:
        points = points - 2
    if k == 3:
        points = points - 11
    if k == 4:
        points = -100
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

global zobrist_table 
zobrist_table = [[[random.randint(1,2**16 - 1) for i in range(8)]for j in range(4)]for k in range(4)]

P = [[("P", "B"), ("K", "B"), ("B", "B"), ("R", "B")], [
    ("P", "W"), ("K", "W"), ("B", "W"), ("R", "W")]]


grid = [[("_", "_")]*4 for n in range(4)]


grid1 = [[(350, 250), (450, 250), (550, 250), (650, 250)], [(350, 350), (450, 350), (550, 350), (650, 350)], [
    (350, 450), (450, 450), (550, 450), (650, 450)], [(350, 550), (450, 550), (550, 550), (650, 550)]]

def compute_hash(grid):
    h=0
    dictionaryzobrist={
       ('B','W'):0,
       ('P','W'):1,
       ('R','W'):2,
       ('K','W'):3,
       ('B','B'):4,
       ('P','B'):5,
       ('R','B'):6,
       ('K','B'):7
        
    }
    for i in range(0,4):
        for j in range(0,4):
            if grid[i][j]!=('_','_'):
                piece=dictionary[grid[i][j]]
                h^=zobrist_table[i][j][piece]
    return h


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
def transform_Bitboards(grid):

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
def simple_minimax(grid, depth, color,  maximazing_player,initCount):
    initCount=initCount+1
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
    if maximazing_player:
        maxing = -10000
         
    
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color, grid)
            ar[1] = not_in_board_moves('P', color, grid)
            ar[2] = not_in_board_moves('K', color, grid)
            ar[3] = not_in_board_moves('B', color, grid)
        else:
            ar = all_possible_moves(color, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:

                if i == 0:
                    y = 'R'
                   

                if i == 1:
                    y = 'P'
                   

                if i == 2:
                    y = 'K'
                   

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color)

                eval = simple_minimax(q, depth-1, color, False,initCount)

                maxing = max(maxing, eval)
                
                
        return maxing
    else:
        mining = 10000
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color2, grid)
            ar[1] = not_in_board_moves('P', color2, grid)
            ar[2] = not_in_board_moves('K', color2, grid)
            ar[3] = not_in_board_moves('B', color2, grid)
        else:
            ar = all_possible_moves(color2, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:
                if i == 0:
                    y = 'R'
                    

                if i == 1:
                    y = 'P'
                    
                if i == 2:
                    y = 'K'
                    

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
                eval = simple_minimax(q, depth - 1, color, True,initCount)
                mining = min(mining, eval)
                
               
        return mining

def simple_minimax(grid, depth, color,  maximazing_player,initCount):
    initCount=initCount+1
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
    if maximazing_player:
        maxing = -10000
         
    
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color, grid)
            ar[1] = not_in_board_moves('P', color, grid)
            ar[2] = not_in_board_moves('K', color, grid)
            ar[3] = not_in_board_moves('B', color, grid)
        else:
            ar = all_possible_moves(color, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:

                if i == 0:
                    y = 'R'
                   

                if i == 1:
                    y = 'P'
                   

                if i == 2:
                    y = 'K'
                   

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color)

                eval = simple_minimax(q, depth-1, color, False,initCount)

                maxing = max(maxing, eval)
                
                
        return maxing
    else:
        mining = 10000
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color2, grid)
            ar[1] = not_in_board_moves('P', color2, grid)
            ar[2] = not_in_board_moves('K', color2, grid)
            ar[3] = not_in_board_moves('B', color2, grid)
        else:
            ar = all_possible_moves(color2, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:
                if i == 0:
                    y = 'R'
                    

                if i == 1:
                    y = 'P'
                    
                if i == 2:
                    y = 'K'
                    

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
                eval = simple_minimax(q, depth - 1, color, True,initCount)
                mining = min(mining, eval)
                
               
        return mining
def minimax(grid, depth, color, alpha, beta, maximazing_player,initCount):
    initCount=initCount+1
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
    if maximazing_player:
        maxing = -10000
         
    
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color, grid)
            ar[1] = not_in_board_moves('P', color, grid)
            ar[2] = not_in_board_moves('K', color, grid)
            ar[3] = not_in_board_moves('B', color, grid)
        else:
            ar = all_possible_moves(color, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:

                if i == 0:
                    y = 'R'
                   

                if i == 1:
                    y = 'P'
                   

                if i == 2:
                    y = 'K'
                   

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color)

                eval = minimax(q, depth-1, color, alpha, beta, False,initCount)

                maxing = max(maxing, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return maxing
    else:
        mining = 10000
        if initCount<=6:
            ar = [0, 0, 0, 0]
            ar[0] = not_in_board_moves('R', color2, grid)
            ar[1] = not_in_board_moves('P', color2, grid)
            ar[2] = not_in_board_moves('K', color2, grid)
            ar[3] = not_in_board_moves('B', color2, grid)
        else:
            ar = all_possible_moves(color2, grid)
        s = [0, 1, 2,3]
        random.shuffle(s)
        random.shuffle(ar[0])
        random.shuffle(ar[1])
        random.shuffle(ar[2])
        random.shuffle(ar[3])
        for i in s:
            for pos_moves in ar[i]:
                if i == 0:
                    y = 'R'
                    

                if i == 1:
                    y = 'P'
                    
                if i == 2:
                    y = 'K'
                    

                if i == 3:
                    y = 'B'
                q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
                eval = minimax(q, depth - 1, color, alpha, beta, True,initCount)
                mining = min(mining, eval)
                beta = min(beta, eval)   
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return mining
def best_move_simple_minimax(grid, depth, color,initCount):
    initCount=initCount+1
    maxing = -10000
    
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', color, grid)
        ar[1] = not_in_board_moves('P', color, grid)
        ar[2] = not_in_board_moves('K', color, grid)
        ar[3] = not_in_board_moves('B', color, grid)
    else:
        ar = all_possible_moves(color, grid)
    s = [0, 1, 2, 3]
    random.shuffle(s)
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    for i in s:
        for pos_moves in ar[i]:

            if i == 0:
                y = 'R'
               
            if i == 1:
                y = 'P'
                

            if i == 2:
                y = 'K'


            if i == 3:
                y = 'B'
            q = update_grid(grid, pos_moves[0], pos_moves[1], y, color)

            eval = simple_minimax(q, depth-1, color, False, initCount)

            if eval > maxing:
                maxing = eval
                best_moves1 = pos_moves[0]
                best_moves2 = pos_moves[1]
                best_moves3 = y
           


           
            
    return best_moves1, best_moves2, best_moves3, color

def best_move(grid, depth, color, alpha, beta,initCount):
    initCount=initCount+1
    maxing = -10000
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', color, grid)
        ar[1] = not_in_board_moves('P', color, grid)
        ar[2] = not_in_board_moves('K', color, grid)
        ar[3] = not_in_board_moves('B', color, grid)
    else:
        ar = all_possible_moves(color, grid)
    s = [0, 1, 2, 3]
    random.shuffle(s)
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    for i in s:
        for pos_moves in ar[i]:

            if i == 0:
                y = 'R'
               
            if i == 1:
                y = 'P'
                

            if i == 2:
                y = 'K'


            if i == 3:
                y = 'B'
            q = update_grid(grid, pos_moves[0], pos_moves[1], y, color)

            eval = minimax(q, depth-1, color, alpha, beta, False, initCount)

            if eval > maxing:
                maxing = eval
                best_moves1 = pos_moves[0]
                best_moves2 = pos_moves[1]
                best_moves3 = y
            alpha = max(alpha, eval)


           
            if beta <= alpha:
                break
        if beta <= alpha:
            break
    return best_moves1, best_moves2, best_moves3, color


#spot = time.time()
# print((time.time()-spot))

sp = best_move(grid, 3, 'B', -10000, 10000,0)
print(sp)
al = minimax(grid, 3, 'B', -10000, 10000, True,0)

ase = evaluate_board(grid, 'B')
lvl=2
lvl2=4

notend = False
notend4 = False
notend3= False
changeside = [1,1]
i = 1
k=1
runit=[]
initCount=0

while(notend):
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
        a = best_move(grid, 4, 'B', -10000, 10000,initCount)
        k1 = (a[2], a[3])
        grid[a[0]][a[1]] = k1
        printg(grid)
        i = i+1
    if initCount<6:
        initCount=initCount+1
while(notend4):
    if (i % 2) != 0:

        a = best_move(grid, 3, 'W', -100000, 100000,initCount)
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'W'):
            notend4 = False
    else:
        a = best_move(grid, 4, 'B', -100000, 100000,initCount)
        k1 = (a[2], a[3])
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'B'):
            notend4 = False
    initCount=initCount+1
with open('test200.csv','w',newline='') as f:
    thewriter=csv.writer(f)
    while(notend3 and i!=10000 and i!=10001 and k!=250):
        print(i)
        if (i % 2) != 0 and ( lvl2!=0):
            k=k+1
            a = best_move(grid, lvl2, 'W', -10000, 10000,initCount)
            
            thewriter.writerow([a[0],a[1],a[2],a[3]])

            grid = update_grid(grid, a[0], a[1], a[2], a[3])
            youp=transform_Bitboards(grid)
            runit.append(youp)
            
            printg(youp)
            printg(grid)
            i = i+1
            if initCount<6:
                initCount=initCount+1
            if is_winning(grid, 'W'):
                initCount=1
                
                notend = True
                thewriter.writerow(['Win white'])
                grid = [[("_", "_")]*4 for n in range(4)]
                i=i+1
                k=0
            if k==250:
                initCount=1
                thewriter.writerow(['overload'])
                grid = [[("_", "_")]*4 for n in range(4)]
                i=i+1
                k=0
           
        elif (i % 2) != 0 and (lvl2==0):
            
            ar=all_possible_moves('W',grid)
            k=k+1
            i=i+1
            while q==[]:
                ins=random.choice(range(len(ar)))
                q=random.choice(ar[ins])
            if ins==0:
                kind="R"
            if ins==1:
                kind="P"
            if ins==2:
                kind="K"
            if ins==3:
                kind="B"
            thewriter.writerow([q[0],q[1],kind,'W'])
            update_grid(grid,q[0],q[1],kind,'W')
            youp=transform_Bitboards(grid)
            runit.append(youp)
            printg(youp)
            printg(grid)
            if initCount<6:
                initCount=initCount+1
            
        elif (i % 2) == 0 and (lvl==0):
            print('wow')
            i=i+1
            k=k+1
            ar=all_possible_moves('B',grid)
            ins=random.choice(range(len(ar)))
            q=random.choice(ar[ins])
            while q==[]:
                ins=random.choice(range(len(ar)))
                q=random.choice(ar[ins])
            if ins==0:
                kind="R"
            if ins==1:
                kind="P"
            if ins==2:
                kind="K"
            if ins==3:
                kind="B"
            thewriter.writerow([q[0],q[1],kind,'B'])
            update_grid(grid,q[0],q[1],kind,'B')       
            youp=transform_Bitboards(grid)
            runit.append(youp)
            printg(youp)
            printg(grid)
            if initCount<6:
                initCount=initCount+1
           
        else:
           
            a = best_move(grid, lvl, 'B', -10000, 10000,initCount)
            k1 = (a[2], a[3])
            grid = update_grid(grid, a[0], a[1], a[2], a[3])
            youp=transform_Bitboards(grid)
            runit.append(youp)
            printg(youp)
            thewriter.writerow([a[0],a[1],a[2],a[3]])
            printg(grid)
            i = i+1
            k=k+1
            if initCount<6:
                initCount=initCount+1
            if is_winning(grid, 'B'):
                initCount=1
                
                thewriter.writerow(['Win black'])
                grid = [[("_", "_")]*4 for n in range(4)]
                k=0
                notend = True

            if k==250:
                initCount=1
                thewriter.writerow(['overload'])
                grid = [[("_", "_")]*4 for n in range(4)]
                k=0

for i in range(0,len(runit),1):               
    printg(runit[i])
df=pd.read_csv('neuralattempt2.csv',dtype=str,float_precision='round_trip')
df.to_csv('roundedneuralattempt.csv',index=False)
def negamax(grid, depth, color, color2, alpha, beta,initCount):
    initCount=initCount+1
    if color == 1 and color2 == 'W':
        Col = 'B'
    elif color == -1 and color2 == 'B':
        Col = 'B'

    else:
        Col = 'W'
    if Col == 'W':
        Col2 = 'B'
    else:
        Col2 = 'W'
    if depth == 0:

        req = evaluate_board(grid, color2)
        return req * color
    if is_winning(grid, Col):
        req = evaluate_board(grid, color2)
        return req * color
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', Col2, grid)
        ar[1] = not_in_board_moves('P', Col2, grid)
        ar[2] = not_in_board_moves('K', Col2, grid)
        ar[3] = not_in_board_moves('B', Col2, grid)
    else:
        
        ar = all_possible_moves(Col2, grid)
   
    s = [0,3,2,1]
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    o = 0
    for i in s:

        for pos_moves in ar[i]:
            if pos_moves != []:
                o = o+1
            if i == 0:
                y = 'R'

            if i == 1:
                y = 'P'

            if i == 2:
                y = 'K'
            if i == 3:

                y = 'B'

            q = update_grid(grid, pos_moves[0], pos_moves[1], y, Col2)

            if o == 1:

                eval = -negamax(q, depth-1, -color, color2, -beta, -alpha,initCount)
            else:
                eval = -negamax(q, depth-1, -color, color2, -alpha-1, -alpha,initCount)
                eval1=eval
                if alpha < eval and eval < beta:
                    eval = -negamax(q, depth-1, -color, color2, -beta, -eval1,initCount)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        if alpha >= beta:
            break
    return alpha
maxdepth=4
global firstnode,winningmove
winningmove=[0,0,0,0]
firstnode=[0,0,0,0]

        

def best_move_iterative_deepening(grid, depth, color, color2, alpha, beta,initCount):
    initCount=initCount+1
    if color2 == 'W':
        Col = 'B'
    else:
        Col = 'W'
    maxing = -100000
    if initCount<=6:
        ar = [0, 0, 0, 0]
        
        ar[0] = not_in_board_moves('R', color2, grid)
        ar[1] = not_in_board_moves('P', color2, grid)
        ar[2] = not_in_board_moves('K', color2, grid)
        ar[3] = not_in_board_moves('B', color2, grid)
    else:
        ar = all_possible_moves(color2, grid)
    
    if winningmove[2]=='R':
        startingNode=0
    elif winningmove[2]=='P':
        startingNode=1
    elif winningmove[2]=='K':
        startingNode=2
    elif winningmove[2]=='B':
        startingNode=3
    
    s = [0, 3, 2,1]
    if winningmove[0]!=0:
        movesStarting=[winningmove[0],winningmove[1]]
        ar[startingNode].remove(movesStarting)
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    if winningmove[0]!=0:
        ar[startingNode].insert(0,movesStarting)
        s.remove(startingNode)
        s.insert(0,startingNode)
    o = 0
    print(ar)
    print(s)
    for i in s:
        for pos_moves in ar[i]:
            if pos_moves != []:
                o = o+1
            if i == 0:
                y = 'R'
            if i == 1:
                y = 'P'
            if i == 2:
                y = 'K'
            if i == 3:
                y = 'B'
            q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
            if is_winning(q, color2):
                return pos_moves[0], pos_moves[1], y, color2
            if o == 1:
                eval = -negamax(q, depth-1, -color, color2, -beta, -alpha,initCount)
            else:
                eval = -negamax(q, depth-1, -color, color2, -alpha-1, -alpha,initCount)
                eval1=eval
                if alpha < eval and eval < beta:
                    eval = -negamax(q, depth-1, -color, color2, -beta, -eval1,initCount)
            if eval > maxing:
                maxing = eval
                best_moves1 = pos_moves[0]
                best_moves2 = pos_moves[1]
                best_moves3 = y
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        if beta <= alpha:
            break
    return best_moves1, best_moves2, best_moves3, color2
     
    
maxDepth=7
seconds3=[]
def best_move_iterative(grid,maxDepth,color,color2,alpha,beta,initCount):
    for depth1 in range(1,maxDepth+1):
        counter=initCount
        q=grid.copy()
        if depth1==maxDepth:
            countdown1=time.time()
            
        winningmove=best_move_iterative_deepening(q,depth1,color,color2,alpha,beta,counter)
        if depth1==maxDepth:
            countdown1end=time.time()
            seconds3.append(countdown1end-countdown1)
        
        print(winningmove)
    return winningmove

def best_move2(grid, depth, color, color2, alpha, beta,initCount):
    initCount=initCount+1
    if color2 == 'W':
        Col = 'B'
    else:
        Col = 'W'
    maxing = -100000
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', color2, grid)
        ar[1] = not_in_board_moves('P', color2, grid)
        ar[2] = not_in_board_moves('K', color2, grid)
        ar[3] = not_in_board_moves('B', color2, grid)
    else:
        ar = all_possible_moves(color2, grid)
    s = [0, 3, 2,1]
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    o = 0
    for i in s:
        for pos_moves in ar[i]:
            if pos_moves != []:
                o = o+1
            if i == 0:
                y = 'R'
            if i == 1:
                y = 'P'
            if i == 2:
                y = 'K'
            if i == 3:
                y = 'B'
            q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
            if is_winning(q, color2):
                return pos_moves[0], pos_moves[1], y, color2
            if o == 1:
                eval = -negamax(q, depth-1, -color, color2, -beta, -alpha,initCount)
            else:
                eval = -negamax(q, depth-1, -color, color2, -alpha-1, -alpha,initCount)
                if alpha < eval and eval < beta:
                    eval = -negamax(q, depth-1, -color, color2, -beta, -eval,initCount)
            if eval > maxing:
                maxing = eval
                best_moves1 = pos_moves[0]
                best_moves2 = pos_moves[1]
                best_moves3 = y
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        if beta <= alpha:
            break
    return best_moves1, best_moves2, best_moves3, color2
def negamax_with_transpotition(grid, depth, color, color2, alpha, beta,initCount):
    initCount=initCount+1
    if color == 1 and color2 == 'W':
        Col = 'B'
    elif color == -1 and color2 == 'B':
        Col = 'B'

    else:
        Col = 'W'
    if Col == 'W':
        Col2 = 'B'
    else:
        Col2 = 'W'
    if depth == 0:

        req = evaluate_board(grid, color2)
        return req * color
    if is_winning(grid, Col):
        req = evaluate_board(grid, color2)
        return req * color
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', Col2, grid)
        ar[1] = not_in_board_moves('P', Col2, grid)
        ar[2] = not_in_board_moves('K', Col2, grid)
        ar[3] = not_in_board_moves('B', Col2, grid)
    else:
        
        ar = all_possible_moves(Col2, grid)
   
    s = [0,3,2,1]
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    o = 0
    for i in s:

        for pos_moves in ar[i]:
            if pos_moves != []:
                o = o+1
            if i == 0:
                y = 'R'

            if i == 1:
                y = 'P'

            if i == 2:
                y = 'K'
            if i == 3:

                y = 'B'

            q = update_grid(grid, pos_moves[0], pos_moves[1], y, Col2)

            if o == 1:

                eval = -negamax_with_transpotition(q, depth-1, -color, color2, -beta, -alpha,initCount)
            else:
                eval = -negamax_with_transpotition(q, depth-1, -color, color2, -alpha-1, -alpha,initCount)
                if alpha < eval and eval < beta:
                    eval = -negamax(q, depth-1, -color, color2, -beta, -eval,initCount)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        if alpha >= beta:
            break
    return alpha

def best_move2(grid, depth, color, color2, alpha, beta,initCount):
    initCount=initCount+1
    if color2 == 'W':
        Col = 'B'
    else:
        Col = 'W'
    maxing = -100000
    if initCount<=6:
        ar = [0, 0, 0, 0]
        ar[0] = not_in_board_moves('R', color2, grid)
        ar[1] = not_in_board_moves('P', color2, grid)
        ar[2] = not_in_board_moves('K', color2, grid)
        ar[3] = not_in_board_moves('B', color2, grid)
    else:
        
        ar = all_possible_moves(color2, grid)
    
    s = [0, 3, 2,1]
    random.shuffle(ar[0])
    random.shuffle(ar[1])
    random.shuffle(ar[2])
    random.shuffle(ar[3])
    o = 0
    for i in s:

        for pos_moves in ar[i]:
            if pos_moves != []:
                o = o+1
            if i == 0:
                y = 'R'

            if i == 1:
                y = 'P'

            if i == 2:
                y = 'K'
            if i == 3:
                
                y = 'B'

            q = update_grid(grid, pos_moves[0], pos_moves[1], y, color2)
            if is_winning(q, color2):
                return pos_moves[0], pos_moves[1], y, color2

            if o == 1:

                eval = -negamax(q, depth-1, -color, color2, -beta, -alpha,initCount)
            else:
                eval = -negamax(q, depth-1, -color, color2, -alpha-1, -alpha,initCount)
                if alpha < eval and eval < beta:
                    eval = -negamax(q, depth-1, -color, color2, -beta, -eval,initCount)
            if eval > maxing:
                maxing = eval
                best_moves1 = pos_moves[0]
                best_moves2 = pos_moves[1]
                best_moves3 = y

            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        if beta <= alpha:
            break
    return best_moves1, best_moves2, best_moves3, color2

seconds=[]
seconds2=[]
seconds3=[]
counter=0
durationstart=time.time()
notend2=False
duration=0
while(notend2 and duration<1500):
    print(duration)
    durationfinish=time.time()
    duration=durationfinish-durationstart
    counter=counter+1
    if (i % 2) == 0:
        countdown=time.time()
        #a = best_move_simple_minimax(grid, 3, 'W',initCount)
        a = best_move(grid, 5, 'W', -100000, 100000,initCount)
        #a = best_move2(grid,3,1, 'W', -100000, 100000,initCount)
        countdownend=time.time()
        seconds.append(countdownend-countdown)
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'W'):
            grid = [[("_", "_")]*4 for n in range(4)]
            
        if counter==130:
            grid = [[("_", "_")]*4 for n in range(4)]
            counter=0
    else:
        countdown=time.time()
        a=best_move_iterative(grid, 5, 1, 'B', -100000, 100000, initCount)
        #a = best_move2(grid,3,1, '', -100000, 100000,initCount)
        countdownend=time.time()
        seconds2.append(countdownend-countdown)
        k1 = (a[2], a[3])
        grid = update_grid(grid, a[0], a[1], a[2], a[3])
        printg(grid)
        i = i+1
        if is_winning(grid, 'B'):
            grid = [[("_", "_")]*4 for n in range(4)]
        if counter==130:
            grid = [[("_", "_")]*4 for n in range(4)]
            counter=0
    initCount=initCount+1
reps=np.array(range(0,len(seconds),1))
sec=np.array(seconds).sum()
sec2=np.array(seconds2).sum()
sec3=np.array(seconds3).sum()
print(sec,sec2,sec3)
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('exp', color=color)
ax1.plot(reps, seconds, color=color)
ax1.tick_params(axis='y', labelcolor=color)

 

color = 'tab:blue'
reps=np.array(range(0,len(seconds2),1))
ax1.plot(reps, seconds2, color=color)



plt.show()


