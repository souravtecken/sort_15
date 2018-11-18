from graphics import *
import random

bgCOLOR = "WHITE"

timerWidth=30
gapWidth=5
tileWidth=70
gridSize=5

class TILE:
    def __init__(self,x=0,y=0,value=0):
        self.x=x
        self.y=y
        self.val=value


    def drawTile(self):
        r=Rectangle(Point(self.x-tileWidth//2,self.y-tileWidth//2),Point(self.x+tileWidth//2,self.y+tileWidth//2))    
        r.setFill("black")
        r.setWidth(0)
        rText=Text(Point(self.x,self.y),str(self.val))
        rText.setFill("white")
        if self.val!=0:
            r.draw(win)
            rText.draw(win)




win=GraphWin("Sort 15", tileWidth*gridSize+gapWidth*(gridSize+1),tileWidth*gridSize+gapWidth*(gridSize+1))
win.setBackground("white")


def initTileValues(tiles):
    numbers=list(range(gridSize*gridSize))
    print(numbers)
    for i in range(gridSize):
        for j in range(gridSize):
            tiles[i][j].val=random.choice(numbers)
            numbers.remove(tiles[i][j].val)
    

def drawGrid(tiles):
    for i in range(gridSize):
        for j in range(gridSize):
            tiles[i][j].drawTile()

    
# Create a 2D list of tiles, assigning the appropriate midpoints and initial ordered values.
tiles=[[TILE(gapWidth*(j+1)+j*tileWidth+tileWidth//2,gapWidth*(i+1)+i*tileWidth+tileWidth/2,i*4+j) for j in range(gridSize)] for i in range(gridSize)]

initTileValues(tiles)
drawGrid(tiles)


n=input()


