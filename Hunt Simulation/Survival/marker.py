
class Marker:
    position = 0
    prevPos = 0
    age = 0
    #create a new marker with a starting position and 
    def __init__(self, position):
        self.position = []
        self.prevPos = []
        self.position.append(position)
        self.prevPos = 0
        self.age = 0
    #gets the x and y and direction
    def getY(self):
        return self.position[-1][0]
    def getX(self):
        return self.position[-1][1]
    def getPrevDirection(self):
        if self.prevPos != 0:
            x = self.position[-1][1] - self.prevPos[1]
            y = self.position[-1][0] - self.prevPos[0]
            return [y,x]
        else:
            return [0,0]
    def AgeUp(self):
        self.age += 1
    def Die(self, move):
        file = open("testfile.txt","a") 
        file.write(str(self.age))
        file.write("\n")
        file.close
    #updates the position of the marker
    def UpdatePosition(self,position):
        self.position.append(position)
        self.prevPos = self.position[-2]
    def MakeMove(self,x,y):
        self.AgeUp()
        pos = [self.getY() + y, self.getX() + x] 
        self.UpdatePosition(pos)   
    #print out the positions
    def PrintPositions(self):  
        print("Current Position: " + str(self.position))
        print("Previous Position: " + str(self.prevPos))
    