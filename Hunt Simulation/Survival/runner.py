from board import Board

b = Board(10)

for i in range(2000):
    b.MovePiece(i)
b.HeatMap()
