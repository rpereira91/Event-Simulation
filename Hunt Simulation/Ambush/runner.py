#import statement
from board import Board
#create an 8x8 board
b = Board(8)
#run it over the number of iterations 
x = input("How many cycles do you want to run the simulation for? ")
for i in range(0,int(x)):
    b.MakeRandomMove()
#display the board    
b.PrintBoard()