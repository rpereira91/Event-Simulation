import random
# import numpy as np
# import matplotlib.pyplot as plt
from datetime import datetime


class Board:
    direction = [0,0],[0,1],[1,0],[1,1],[0,-1],[-1,0],[-1,-1],[1,-1],[-1,1]
    #this is for a random starting position, it's currently commented out
    #position = [random.randint(0,6),random.randint(0,6)]
    #standard starting position 
    position = [7,0]
    board = 0
    boardSize = 0
    def __init__(self, bs):
        #creates a blank board
        self.board = [[0 for i in range(bs)] for j in range(bs)]
        #set the board size
        self.boardSize = bs
        #draw the board
        self.UpdateBoard()
        random.seed(datetime.now())
    #randomly makes a move in a valid direction
    def MakeRandomMove(self):
        #create x and y to be larger than the board so it's not a valid move
        y = self.boardSize + 1
        x = self.boardSize + 1
        #keep making new moves till a valid move is made
        while (self.ValidMove(x,y) != True):
            cm = random.randint(0,8)
            y = self.position[0]+self.direction[cm][0]
            x = self.position[1]+self.direction[cm][1]
        #make the move
        self.position[0] = y
        self.position[1] = x
        self.UpdateBoard()
    #checks to see if the x,y passed to the method is a valid move
    def ValidMove(self,x,y):
        if x >= self.boardSize or y >= self.boardSize:
            return False
        if x < 0 or y < 0:
            return False
        return True
    # Prints out the board
    def PrintBoard(self):
        for i in range(self.boardSize):
            print (self.board[i])
        print (" ")
        #heat map code, might not run on lab computers since it needs dependencies installed, commented out for now. 
        # npArray = np.array(self.board)
        # plt.imshow(npArray)
        # plt.show()
     # Updates the board with the current position of the marker 
    def UpdateBoard(self):
        self.board[self.position[0]][self.position[1]] += 1
        


