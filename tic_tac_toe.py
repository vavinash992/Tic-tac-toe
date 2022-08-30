from copy import copy
import sys    #to exit the program
import pygame
from constants import *
import numpy as np
import random
import copy

#pygame 
pygame.init()
screen=pygame.display.set_mode( (WIDTH,HEIGHT) )
pygame.display.set_caption('TIC TAC TOE')
screen.fill(bgcolor)

class Board:
    def __init__(self):
        self.squares=np.zeros((rows,cols))
        self.empt_sqrs=self.squares
        self.marked_sqrs=0
    
    def final_State(self,show=False):
        '''
        returns 0,if there is no win yet
        returns 1,if player 1 wins
        returns 2,if player 2 wins
        '''
        #vertical wins
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col] !=0:
                if show:
                    color=CIRC_COLOR if self.squares[0][col]==2 else CROSS_COLOR
                    iPos=(col*sq_size+sq_size//2,20)
                    fPos=(col*sq_size+sq_size//2,HEIGHT-20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                return self.squares[0][col]

        #horizontal wins
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2] !=0:
                if show:
                    color=CIRC_COLOR if self.squares[row][1]==2 else CROSS_COLOR
                    iPos=(20,row*sq_size+sq_size//2)
                    fPos=(WIDTH-20,row*sq_size+sq_size//2)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                return self.squares[row][0]
        
        #descending line wins
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2] !=0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[0][0]
        
        #ascending line wins
        if self.squares[0][2]==self.squares[1][1]==self.squares[2][0] !=0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        return 0
        
        
    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs+=1
    
    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in range(rows):
            for col in range(cols):
                if self.empt_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def empt_sqr(self,row,column):
        return self.squares[row][column]==0
    
    def isfull(self):
        return self.marked_sqrs==9
    
    def isempty(self):
        return self.marked_sqrs==0

class AI:
    
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)
    
    def minmax(self,board,maximizing):
        terminal_case=board.final_State()
        if terminal_case==1:
            return 1,None
        if terminal_case==2:
            return -1,None
        if board.isfull():
            return 0,None
        
        if maximizing:
            max_eval=-100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for (row,col) in empty_sqrs:
                temp=copy.deepcopy(board)
                temp.mark_sqr(row,col,1)
                eval=self.minmax(temp,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)
            return max_eval,best_move
        
        elif not maximizing:
            min_eval=sys.maxsize
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for (row,col) in empty_sqrs:
                temp=copy.deepcopy(board)
                temp.mark_sqr(row,col,self.player)
                eval=self.minmax(temp,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
                    
            return min_eval,best_move
    
    def eval(self,mainboard):
        if self.level==0:
            #random move
            eval='random'
            move=self.rnd(mainboard)
        else:
            #min max move
            eval,move=self.minmax(mainboard,False)
        
        print(f'AI move: {move} \n AI eval: {eval}')
        return move
        
    
    
    
class Game:
    def __init__(self):
        self.showlines()
        self.player=1           # 1-crosses 2-circles
        self.board=Board()
        self.gamemode='ai' 
        self.running=True
        self.ai=AI()
    
    def showlines(self):
        screen.fill(bgcolor)
        #horizontal
        pygame.draw.line(screen,linecolor,(sq_size,0),(sq_size,HEIGHT),line_width)
        pygame.draw.line(screen,linecolor,(WIDTH-sq_size,0),(WIDTH-sq_size,HEIGHT),line_width)
        
        #vertical
        pygame.draw.line(screen,linecolor,(0,sq_size),(WIDTH,sq_size),line_width)
        pygame.draw.line(screen,linecolor,(0,HEIGHT-sq_size),(WIDTH,HEIGHT-sq_size),line_width)
        
    def next_turn(self):
        self.player=self.player%2 + 1
    
    def draw_fig(self,row,col):
        if self.player==1:      
            #desc line      
            start_desc = (col * sq_size + OFFSET, row * sq_size + OFFSET)
            end_desc = (col * sq_size + sq_size - OFFSET, row * sq_size + sq_size - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, cross_width)
            # asc line
            start_asc = (col * sq_size + OFFSET, row * sq_size + sq_size - OFFSET)
            end_asc = (col * sq_size + sq_size - OFFSET, row * sq_size + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, cross_width)
            
        elif self.player==2:
            centre=(col*sq_size+sq_size//2,row*sq_size+sq_size//2)
            pygame.draw.circle(screen,CIRC_COLOR,centre,RADIUS,CIRC_WIDTH)
            
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def reset(self):
        self.__init__()
    
    def isover(self):
        return self.board.final_State(show=True) != 0 or self.board.isfull()
          
        

def main():
    game=Game()
    ai=AI()
    board=game.board
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1 
                    
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//sq_size
                col=pos[0]//sq_size
                if board.empt_sqr(row,col) and game.running: 

                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
                    if game.isover():
                        game.running = False
        
        if game.gamemode=='ai'and game.player==ai.player and game.running:
            pygame.display.update()
            row,col=ai.eval(board)
            board.mark_sqr(row,col,ai.player)
            game.draw_fig(row,col)
            game.next_turn()
            
            if game.isover():
                game.running = False
            
            
            
            
        pygame.display.update()
main()
