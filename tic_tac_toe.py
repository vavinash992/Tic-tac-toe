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
    
    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
    
    def empt_sqr(self,row,column):
        return self.squares[row][column]==0

class Game:
    def __init__(self):
        self.showlines()
        self.player=1
        self.board=Board()
    
    def showlines(self):
        #horizontal
        pygame.draw.line(screen,linecolor,(sq_size,0),(sq_size,HEIGHT),line_width)
        pygame.draw.line(screen,linecolor,(WIDTH-sq_size,0),(WIDTH-sq_size,HEIGHT),line_width)
        
        #vertical
        pygame.draw.line(screen,linecolor,(0,sq_size),(WIDTH,sq_size),line_width)
        pygame.draw.line(screen,linecolor,(0,HEIGHT-sq_size),(WIDTH,HEIGHT-sq_size),line_width)
        
    def next_turn(self):
        self.player=self.player%2 + 1

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
                    print(board.squares)
                    game.next_turn()
        pygame.display.update()
main()