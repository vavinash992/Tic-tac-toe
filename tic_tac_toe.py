import sys    #to exit the program
import pygame
from constants import *
import numpy as np
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
    
    def final_State(self):
        '''
        returns 0,if there is no win yet
        returns 1,if player 1 wins
        returns 2,if player 2 wins
        '''
        #vertical wins
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col] !=0:
                return self.squares[0][col]

        #horizontal wins
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2] !=0:
                return self.squares[row][0]
        
        #descending line wins
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2] !=0:
            return self.squares[0][0]
        
        #ascending line wins
        if self.squares[0][2]==self.squares[1][1]==self.squares[2][0] !=0:
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

class Game:
    def __init__(self):
        self.showlines()
        self.player=1           # 1-crosses 2-circles
        self.board=Board()
        self.gamemode='pvp' 
        self.running=True
    
    def showlines(self):
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
            
        

def main():
    game=Game()
    board=game.board
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//sq_size
                col=pos[0]//sq_size
                if board.empt_sqr(row,col):
                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
        pygame.display.update()
main()