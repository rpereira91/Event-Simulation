import random
from marker import Marker
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class Board:
    direction = [0,0],[0,1],[1,0],[1,1],[0,-1],[-1,0],[-1,-1],[1,-1],[-1,1]
    board = 0
    boardSize = 0
    markers = 0
    b = 0.8
    g = 0.6
    danger = 0
    def __init__(self, bs):
        self.board = [[0 for i in range(bs)] for j in range(bs)]
        self.markers = []
        self.danger = []
        #create two markers that will spawn randomly 
        self.markers.append(Marker([random.randint(0,bs-1),random.randint(0,bs-1)]))
        self.markers.append(Marker([random.randint(0,bs-1),random.randint(0,bs-1)]))
        self.boardSize = bs
        self.UpdateBoard(0)
        print ("Starting Board")
        self.PrintBoard()
        self.AddDanger(10)
        random.seed(datetime.now())
        
    def AddDanger(self,danger):
        for i in range (danger):
            self.danger.append(Marker([random.randint(0,9),random.randint(0,9)]))
    #checks to see if the x,y passed to the method is a valid move
    def ValidMove(self,x,y):
        if x >= self.boardSize or y >= self.boardSize:
            return False
        if x < 0 or y < 0:
            return False
        return True
    #moves the piece based on the calculations
    def MovePiece(self,move):
        tempMarkers = self.markers[:]
        for m in tempMarkers:
            validMoves = []
            for d in self.direction:
                y = m.getY() + d[0]
                x = m.getX() + d[1]
                if self.ValidMove(x,y):
                    validMoves.append(d)
            #get the last direction the piece moved
            mrkPD = m.getPrevDirection()
            itrMoves = validMoves[:]
            for vm in itrMoves:
                y = m.getY() + vm[0]
                x = m.getX() + vm[1]
                # #if the piece didn't move before, increase the chances of it moving there
                if vm[1] != 0 and vm[0] != 0:
                    if self.board[y][x] == 1:
                        validMoves.append(vm)
                #if the piece has moved before 
                #if the current move is in the direction of a previous move, add that move to the list
                if mrkPD[0] == vm[0] and mrkPD[1] == vm[1]:
                    validMoves.append(vm)
            #if the piece has not moved in the past it is also likely to stand still for the next move                
            if mrkPD[0] == 0 and mrkPD[1] == 0 and m.prevPos != 0:
                validMoves.append([0,0])
            dir = validMoves[random.randint(0,len(validMoves) - 1)]
            m.MakeMove(dir[1],dir[0])
        self.UpdateBoard(move)
        #self.PrintBoard()
        #updates the visual of the board
    def UpdateBoard(self,move):
        self.board = [[0 for i in range(self.boardSize)] for j in range(self.boardSize)]
        for marker in self.markers:
            self.board[marker.getY()][marker.getX()] += 1
        self.CheckMate(move)
    #sees if it needs to create an offspring
    def CheckMate(self,move):
        #number of markers to be created or killed
        createCount = 0
        deathCount = 0
        #iterate through the board
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] >= 2:
                    #if a marker can be created, and it beats the odds of b, create a marker
                    if self.board[i][j] == 2:
                        if random.random() > self.b:
                            createCount += 1
                    #if there are more than 4 marker on the square kill a marker
                    elif self.board[i][j] >= 4:
                        if random.random() > self.g:
                            deathCount += 1
                #if there's danger there kill a marker
                if(self.ContainsDanger(j,i) and self.board[i][j] >= 1):
                    deathCount+=self.board[i][j]
        #create and delete the needed number of users
        for i in range(createCount):
            self.markers.append(Marker([random.randint(0,self.boardSize-1),random.randint(0,self.boardSize-1)]))
        for i in range(deathCount):
            self.markers[-1].Die(move)
            del self.markers[-1]
    #prints board
    def PrintBoard(self):
        for i in range(self.boardSize):
            print (self.board[i])
        print (" ")
    #heat map
    def HeatMap(self):
        npArray = np.array(self.board)
        print(len(self.markers))
        plt.imshow(npArray)
        plt.show()
    #sees if there's danger on the passed spot
    def ContainsDanger(self,y,x):
        for m in self.danger:
            if(m.getX() == x and m.getY() == y):
                if(self.board[y][x] > 0):
                    return True
        return False       
        


