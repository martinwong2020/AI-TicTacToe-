import pygame, sys
import numpy as np
import copy

pygame.init()

WIDTH=HEIGHT=900
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TIC TAC TOE VS AI")

def draw_lines():
    line_size=10
    pygame.draw.line(SCREEN,(101, 86, 252),(0,300),(900,300),line_size)
    pygame.draw.line(SCREEN,(101, 86, 252),(0,600),(900,600),line_size)

    pygame.draw.line(SCREEN,(101, 86, 252),(300,0),(300,900),line_size)
    pygame.draw.line(SCREEN,(101, 86, 252),(600,0),(600,900),line_size)

def draw_img(board,row,col):
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col]==1:
                pygame.draw.circle(SCREEN,(0,0,0),(int(300 * col +150),int(300*row+150)), 100,30)
            elif board[row][col]==2:
                pygame.draw.line(SCREEN,(255,255,255),(int(300*col),int(300*row+300)),(int(col*300+300),int(row*300)),20)
                # print(row,col)
                pygame.draw.line(SCREEN,(255,255,255),(int(300*col),int(300*row)),(int(col*300+300),int(row*300+300)),20)
def create_board():
    board=np.zeros((3,3))
    return board

def open_spot(board,row,col):
    return board[row][col]==0

def stuff_board(board):
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col]==0:
                return True
    return False
def win_state(board):
    for row in range(0,3):
        if board[row][0]==board[row][1]==board[row][2] and board[row][0]!=0:
            return True,"row"+str(row)
    for col in range(0,3):
        if board[0][col]==board[1][col]==board[2][col] and board[0][col]!=0:
            print("here",board)
            return True,"col"+str(col)
    if(board[0][0]==board[1][1]==board[2][2] and board[0][0]!=0):
        return True,"diagonal"
    elif(board[0][2]==board[1][1]==board[2][0] and board[2][0]!=0):
        return True,"diagonal"
    return False,"none"
def player_move(board,row,col):
    board[row][col]=1

def ai(board):
    new_board=copy.deepcopy(board)
    next_move=board
    score=-999
    for row in range(0,3):
        for col in range(0,3):
            if(board[row][col]==0):
                board[row][col]=2
                print("board",board)
                value=minmax(board,5,1)
                print(value)
                if (value>score):
                    score=value
                    next_move=copy.deepcopy(board)
                board[row][col]=0
    return next_move

def heuristic(board):
    win_way=win_state(board)[1]
    win_status=win_state(board)[0]
    if  win_way[0]=="r" and board[int(win_way[-1])][0]==2:
        # print("r",player)
        return 1
    elif win_way[0]=="r" and board[int(win_way[-1])][0]==1:
        return -1
    if win_way[0]=="c" and board[0][int(win_way[-1])]==2:
        # print("c",player)
        return 1
    elif win_way[0]=="c" and board[0][int(win_way[-1])]==1:
        return -1
    if win_way[0]=="d" and board[1][1]==2:
        # print("d",player)
        return 1
    elif win_way[0]=="d" and board[1][1]==1:
        return -1
    return 0

def minmax(board,depth,player):
    #need to add complete board
    if depth==0 or win_state(board)[0] or stuff_board(board)==False:
        # print("root",board)
        return heuristic(board)
    else:
        if player==2:
            score=-9999
            for row in range(0,3):
                for col in range(0,3):
                    if board[row][col]==0:
                        
                        board[row][col]=2
                        # print("max",board)
                        score=max(score,minmax(board,depth-1,1))
                        board[row][col]=0
            return score
        elif player==1:
            score=9999
            for row in range(0,3):
                for col in range(0,3):
                    if board[row][col]==0:
                        
                        board[row][col]=1
                        # print("min",board)
                        
                        score=min(score,minmax(board,depth-1,2))
                        board[row][col]=0
            return score


def computing_msg():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('AI Computing', True, (0,0,0))
    SCREEN.blit(text,450,450)
# board1=[[1,1,0],[2,2,0],[1,2,1]]
# print("here",ai(board1))
# print("here",minmax(board1,5,1))

FPS=60

def main():
    run=True
    SCREEN.fill((141, 116, 252))
    board=create_board()
    draw_lines()
    # print(open_spot(board,1,1))
    Win_state=False
    clock=pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN and Win_state==False:
                x_pos=event.pos[0]
                y_pos=event.pos[1]
                row=int(y_pos//300)
                col=int(x_pos//300)

                if open_spot(board,row,col):
                    player_move(board,row,col)
                    # draw_img(board,row,col)

                    board=ai(board)
                    draw_img(board,row,col)
                    Win_state=win_state(board)[0]
                    # print(minmax(board,2,"max"))
                print("up")
        pygame.display.update()

main()