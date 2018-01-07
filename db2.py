"""
Dots and Boxes Solver
Version 2:
Computer tries to complete as many boxes as possible. If no completions exist, chooses by random.

Notes:
* User goes first (so program can mathematically win)
"""

import pygame
from pygame.locals import *
import sys
from collections import namedtuple
from time import sleep
from random import choice

BOARDSIZE = 4

BLACK = (0, 0, 0)
OWNER_NONE = 0
OWNER_USER = 1
OWNER_COMPUTER = 2

Point = namedtuple('Point', ['id', 'x', 'y', 'partners'])
# Box = namedtuple("Box", ["p1", "p2", "p3", "p4", "owner"])
# initialize game engine
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 50)
BOX_USER = myfont.render('U', False, (0, 0, 0))
BOX_COMPUTER = myfont.render('C', False, (0, 0, 0))
# set screen width/height and caption
size = BOARDSIZE * 100 + 100
SURF = pygame.display.set_mode((size, size))
pygame.display.set_caption("Dots and  Boxes")
# initialize clock. used later in the loop.
clock = pygame.time.Clock()
 
# the gameboard is stored as a list of points
# points contain their number, and the number of their connections
board = []
for i in range(BOARDSIZE):
    for i2 in range(BOARDSIZE):
        # print(BOARDSIZE * i + i2)
        board.append(
            Point(BOARDSIZE * i + i2, i2 * 100 + 100, i * 100 + 100, []))
moves_done = []
boxes = [[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1,OWNER_NONE] for i in range(0,4)]
boxes.extend([[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1, OWNER_NONE] for i in range(4,8)])
boxes.extend([[i, i+1, i+BOARDSIZE, i+BOARDSIZE+1, OWNER_NONE] for i in range(8,12)])
score = [0, 0] # user, computer
# print(boxes)
def id_to_index(_id):
    for i in range(len(board)):
        if board[i].id == _id:
            return i
    return -1

# print(board)
def disp_board():
    for point in board:
        pygame.draw.circle(SURF, (point.id * 10,) * 3, (point.x, point.y), 5, 0)
        for partner_id in point.partners:
            partner = board[id_to_index(partner_id)]
            pygame.draw.line(SURF, BLACK, (point.x, point.y), (partner.x, partner.y))
            # print(partner)
    for box in boxes:
        x1 = board[id_to_index(box[0])].x
        y1 = board[id_to_index(box[0])].y
        if box[4] == OWNER_USER:
            text_width, text_height = myfont.size("U")
            SURF.blit(BOX_USER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
        elif box[4] == OWNER_COMPUTER:
            text_width, text_height = myfont.size("C")
            SURF.blit(BOX_COMPUTER, (x1 + 50 - text_width / 2, y1 + 50 - text_height / 2))
        
def is_connection(id1, id2):
    if (id1, id2) in moves_done:
        return True
    if (id2, id1) in moves_done:
        return True
    return False

def is_valid(id1, id2):
    if is_connection(id1, id2):
        return False
    p1 = board[id_to_index(id1)]
    p2 = board[id_to_index(id2)]
    if (p1.x == p2.x + 100 or p1.x == p2.x - 100) and p1.y == p2.y:
        return True
    if p1.x == p2.x and (p1.y == p2.y + 100 or p1.y == p2.y - 100):
        return True
    return False
    # return ((id1, id2) not in moves_done and (id2, id1) not in moves_done) and (id2 == id1 + 1 or id2 == id1 - 1 or id2 == id1 + BOARDSIZE or id2 == id1 - BOARDSIZE)

def move(is_user, id1, id2):
    # connects id1 and id2
    # depends on somebody else to check if move is valid
    board[id_to_index(id1)].partners.append(id2)
    board[id_to_index(id2)].partners.append(id1)
    moves_done.append((id1, id2))
    return check_move_made_box(is_user, id1, id2)

def possible_moves():
    possible = []
    for a in range(1, len(board)):
        for b in list(range(1, len(board))):
            if b == a:
                continue
            if not is_valid(a, b):
                continue
            possible.append((a, b))
    return possible

def get_best_move_v1(possible):
    # take random from possible moves
    return choice(possible)

def get_best_move(possible):
    # check if there are any possible boxes
    for p_move in possible:
        if move_makes_box(*p_move):
            # this move can make a box - take it!
            return p_move
    # ok, so there weren't any box making moves
    # now lets just take a random move
    return choice(possible)

def decide_and_move():
    # randomly pick a valid move
    possible = possible_moves()
    my_choice = get_best_move(possible)
    # print(my_choice)
    is_box = move(False, my_choice[0],my_choice[1])
    
    if is_box:
        score[1] += 1
        SURF.fill((255, 255, 255))
        disp_board()
        pygame.display.update()
        decide_and_move()

def check_complete():
    possible = possible_moves()
    if len(possible) == 0:
        # game is finished!
        print("Game over")
        if score[0] > score[1]:
            print("You won! Score:{} to {}".format(score[0],score[1]))
        elif score[1] > score[0]:
            print("Computer won :( Score:{} to {}".format(score[0],score[1]))
        else:
            print("Tie game. Score:{} to {}".format(score[0],score[1]))
        pygame.quit()
        sys.exit()

def move_makes_box(id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    for i, box in enumerate(boxes):
        temp = list(box[:-1])
        # print(temp)
        if id1 not in temp or id2 not in temp:
            continue
        # temp = list(box[:])
        temp.remove(id1)
        temp.remove(id2)
        # print(temp)
        if is_connection(temp[0],temp[1]):
            if (is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or (is_connection(id1, temp[1]) and is_connection(id2, temp[0])):
                is_box = True
            
    return is_box
def check_move_made_box(is_user, id1, id2):
    is_box = False
    # check if the connection just make from id1 to id2 made a box
    # print(boxes)
    for i, box in enumerate(boxes):
        temp = list(box[:-1])
        if id1 not in temp or id2 not in temp:
            continue
        # temp = list(box[:-1])
        temp.remove(id1)
        temp.remove(id2)
        #if is_user:
        #    print(temp)
        if is_connection(temp[0],temp[1]) and ((is_connection(id1, temp[0]) and is_connection(id2, temp[1])) or
                                (is_connection(id1, temp[1]) and is_connection(id2, temp[0]))):
            # yup, we just made a box
            if is_user:
                score[0] += 1
                boxes[i][4] = OWNER_USER
                # hack to set owner of box
                # boxes[i] = boxes[i]._replace(owner=OWNER_USER)
                # boxes[i].owner = OWNER_USER
            else:
                score[1] + 1
                boxes[i][4] = OWNER_COMPUTER
                # boxes[i] = boxes[i]._replace(owner=OWNER_COMPUTER)
                # boxes[i].owner = OWNER_COMPUTER
            is_box = True
            
    return is_box

def user_move():
    try:
        p1, p2 = map(int,input("What move do you want to make?").split(","))
    except ValueError:
        print("Invalid move.")
        user_move()
    else:
        if is_connection(p1, p2):
            print("Sorry, this move is already taken.")
            user_move()
        elif not is_valid(p1, p2):
            print("Invalid move.")
            user_move()
        else:
            is_box = move(True, p1, p2)
            check_complete()
        
            if is_box:
                print("You scored! Have another turn.")
                score[0] += 1
                SURF.fill((255, 255, 255))
                disp_board()
                pygame.display.update()
                user_move()

SURF.fill((255, 255, 255))
disp_board()
pygame.display.update()

# Loop until the user clicks close button
while True:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # write game logic here
 
    # clear the screen before drawing
    SURF.fill((255, 255, 255))

    # print(id_to_index(p1))
    # move(p1, p2) # board[id_to_index(p1)].partners.append(p2)
    user_move()
    disp_board()
    # display what’s drawn
    pygame.display.update()

    sleep(0.5)

    decide_and_move()
    check_complete()
    SURF.fill((255, 255, 255))
    disp_board()
    pygame.display.update()
    # sleep(1.5)
    # run at 20 fps
    # clock.tick(20)
