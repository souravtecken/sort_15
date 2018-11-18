from graphics import *
import random

bgCOLOR = "WHITE"

timerWidth=30
gapWidth=5
tileWidth=70
gridSize=5
animationSpeed=5

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




def checkIfTileClicked(tiles,mouseClick):
    for i in range(gridSize):
        for j in range(gridSize):
            if mouseClick.x>tiles[i][j].x-tileWidth/2 and mouseClick.y<tiles[i][j].y+tileWidth/2:
                if mouseClick.x<tiles[i][j].x+tileWidth/2 and mouseClick.y>tiles[i][j].y-tileWidth/2:
                    return tiles[i][j],i,j
    return False

def checkTilesMove(tiles,tile):
    for i in range(0,tile[1]):
        j=tile[2]
        if tiles[i][j].val==0:
            return tiles[i][j],i,j
    for i in range(tile[1]+1,gridSize):
        j=tile[2]
        if tiles[i][j].val==0:
            return tiles[i][j],i,j
    for j in range(0,tile[2]):
        i=tile[1]
        if tiles[i][j].val==0:
            return tiles[i][j],i,j
    for j in range(tile[2]+1,gridSize):
        i=tile[1]
        if tiles[i][j].val==0:
            return tiles[i][j],i,j
    return False

def moveTiles(tiles,fTile,lTile):
    firstTileCoordinates=fTile[0].x,fTile[0].y
    if fTile[1]==lTile[1]:
        i=fTile[1]
        if fTile[2]>lTile[2]:
            while not tiles[i][lTile[2]+1].x==lTile[0].x:
                speed=animationSpeed
                if(tiles[i][lTile[2]+1].x-lTile[0].x<animationSpeed):
                    speed=tiles[i][lTile[2]+1].x-lTile[0].x
                for j in range(lTile[2]+1,fTile[2]+1):
                    r=Rectangle(Point(tiles[i][j].x-tileWidth/2,tiles[i][j].y-tileWidth/2),Point(tiles[i][j].x+tileWidth/2,tiles[i][j].y+tileWidth/2))
                    r.setFill("white")
                    r.setWidth(0)
                    r.draw(win)
                    tiles[i][j].x-=speed
                    tiles[i][j].drawTile()
        
    
    
    
    
    lTile[0].x,lTile[0].y=firstTileCoordinates






    if fTile[2]==lTile[2]:
        pass

def sortTilesInGrid(tiles):
    # Sort each row according to their x-coordinates
    for i in range(gridSize):   
        gridRow=list(tiles[i])
        gridRow=sorted(tiles[i],key=lambda tile:tile.x)
        tiles[i]=gridRow        

    # Sort each columns according to their y-coordinates
    

def play(tiles):
    while True:
        mouseClick=win.getMouse()
        tileClicked=checkIfTileClicked(tiles,mouseClick)
        tileCanMove=False
        if tileClicked:
            tileCanMove=checkTilesMove(tiles,tileClicked)
        if tileCanMove:
            moveTiles(tiles,tileClicked,tileCanMove)
            sortTilesInGrid(tiles)

        
            
        
        


    
# Create a 2D list of tiles, assigning the appropriate midpoints and initial ordered values.
tiles=[[TILE(gapWidth*(j+1)+j*tileWidth+tileWidth//2,gapWidth*(i+1)+i*tileWidth+tileWidth/2,i*4+j) for j in range(gridSize)] for i in range(gridSize)]

initTileValues(tiles)
drawGrid(tiles)
play(tiles)






n=input()


