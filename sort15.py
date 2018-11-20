import image
from graphics import *
import random

bgCOLOR = "WHITE"

timerWidth=30
gapWidth=10
tileWidth=100
gridSize=4
animationSpeed=20
imageFileName="image.gif"
# imageGrid stores image objects created in the image.py file
imageGrid=image.cropImageIntoGrid(imageFileName,gridSize,tileWidth)


class TILE:
    def __init__(self,x=0,y=0,value=0,img=0):
        self.x=x
        self.y=y    
        self.val=value
        self.img=img


    def drawTile(self):
        r=Rectangle(Point(self.x-tileWidth//2,self.y-tileWidth//2),Point(self.x+tileWidth//2,self.y+tileWidth//2))    
        r.setFill("black")
        r.setWidth(0)
        rText=Text(Point(self.x,self.y),str(self.val))
        rText.setFill("white")
        img=Image(Point(self.x,self.y),self.img)
        if self.val!=0:
            r.draw(win)
            rText.draw(win)
            img.draw(win)




win=GraphWin("Sort 15", tileWidth*gridSize+gapWidth*(gridSize+1),tileWidth*gridSize+gapWidth*(gridSize+1),autoflush=False)
win.setBackground("white")


def initTileValues(tiles):
    numbers=list(range(gridSize*gridSize))
    print(numbers)
    for i in range(gridSize):
        for j in range(gridSize):
            tiles[i][j].val=random.choice(numbers)
            numbers.remove(tiles[i][j].val)

            tileValue=tiles[i][j].val         #tileValue used to hold the value of the tile for some operations
            if tileValue==0:                  # Attempting to map the values of the tiles to the corresponding section of the image
                tileValue=gridSize*gridSize-1 # grid. Number 1 corresponds to the image piece in the first row first, column, so on.
            else:                             # The tile with value 0 must get the bottom right most piece of the picture. (Because it's not displayed) 
                tileValue-=1                  
            ii=tileValue//gridSize           # Based on tileValue, I assign the tile it's corresponding image section.
            jj=tileValue%gridSize            # This's done by determining the row and column number.
            tiles[i][j].img=imageGrid[ii][jj] 
# For example, in a 4*4 grid:
# Value 1 will be in the first row first column, value 4 will be in the 1st row 4th column.
# Value 5 will be in the second row, first column, so on...
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
                    update(200)
        else:
            while not tiles[i][lTile[2]-1].x==lTile[0].x:
                speed=animationSpeed
                if(lTile[0].x - tiles[i][lTile[2]-1].x<animationSpeed):
                    speed=lTile[0].x-tiles[i][lTile[2]+-1].x
                for j in range(fTile[2],lTile[2]):
                    r=Rectangle(Point(tiles[i][j].x-tileWidth/2,tiles[i][j].y-tileWidth/2),Point(tiles[i][j].x+tileWidth/2,tiles[i][j].y+tileWidth/2))
                    r.setFill("white")
                    r.setWidth(0)
                    r.draw(win)
                    tiles[i][j].x+=speed
                    tiles[i][j].drawTile()
                    update(200)
    else:
        j=fTile[2]
        if fTile[1]>lTile[1]:
            while not tiles[lTile[1]+1][j].y==lTile[0].y:
                speed=animationSpeed
                if(tiles[lTile[1]+1][j].y-lTile[0].y<animationSpeed):
                    speed=tiles[lTile[1]+1][j].y-lTile[0].y
                for i in range(lTile[1]+1,fTile[1]+1):
                    r=Rectangle(Point(tiles[i][j].x-tileWidth/2,tiles[i][j].y-tileWidth/2),Point(tiles[i][j].x+tileWidth/2,tiles[i][j].y+tileWidth/2))
                    r.setFill("white")
                    r.setWidth(0)
                    r.draw(win)
                    tiles[i][j].y-=speed
                    tiles[i][j].drawTile()
                    update(200)
        else:
            while not tiles[lTile[1]-1][j].y==lTile[0].y:
                speed=animationSpeed
                if(lTile[0].y-tiles[lTile[1]-1][j].y<animationSpeed):
                    speed=lTile[0].y-tiles[lTile[1]-1][j].y
                for i in range(fTile[1],lTile[1]):
                    r=Rectangle(Point(tiles[i][j].x-tileWidth/2,tiles[i][j].y-tileWidth/2),Point(tiles[i][j].x+tileWidth/2,tiles[i][j].y+tileWidth/2))
                    r.setFill("white")
                    r.setWidth(0)
                    r.draw(win)
                    tiles[i][j].y+=speed
                    tiles[i][j].drawTile()
                    update(200)
        
    lTile[0].x,lTile[0].y=firstTileCoordinates


def sortTilesInGrid(tiles):
    # Sort each row according to their x-coordinates
    for i in range(gridSize):   
        gridRow=list(tiles[i])
        gridRow=sorted(tiles[i],key=lambda tile:tile.x)
        tiles[i]=gridRow        

    # Sort each columns according to their y-coordinates
    for j in range(gridSize):
        gridColumn=[]
        for i in range(gridSize):
            gridColumn.append(tiles[i][j])
        gridColumn=sorted(gridColumn,key=lambda tile:tile.y)

        for i in range(gridSize):
            tiles[i][j]=gridColumn[i]

def checkCompletion(tiles):
    for i in range(gridSize):
        for j in range(gridSize):
            # If the tile value doesn't correspond to the numeric order and the tile being checked is not the last tile.
            if(tiles[i][j].val!=gridSize*i+j+1 and not i+j==(gridSize-1)*2):
                return False
    return True

def checkSolvability(tiles):
    n=numberOfInversions(tiles)
    zeroPosition=0
    for i in range(len(tiles)):
        numbersInRow=list(map(lambda tile:tile.val,tiles[i]))
        if 0 in numbersInRow:
            zeroPosition=gridSize-i # The zero position is checked from bottom row, row 1 being the last row
            break

    if gridSize%2: # if grid size is odd
        if not n%2: # if number of inversions is even
            return True # Solvable
    else:   # if grid size is even
        if not zeroPosition%2: # if zero is in an even row
            if n%2: # if number of inversions is odd
                return True # Solvable
        else: # if zero is in an odd row
            if not n%2: # if number of inversions is even
                return True # Solvable
    return False # if all above are false, the given state is not solvable
    

def play(tiles):
    while not checkCompletion(tiles):
        mouseClick=win.getMouse()
        tileClicked=checkIfTileClicked(tiles,mouseClick)
        tileCanMove=False
        if tileClicked:
            tileCanMove=checkTilesMove(tiles,tileClicked)
        if tileCanMove:
            moveTiles(tiles,tileClicked,tileCanMove)
            sortTilesInGrid(tiles)

       

def numberOfInversions(tiles):      
    gridNumbers=list()
    for i in range(gridSize):
        for j in range(gridSize):
            if(tiles[i][j].val):
                gridNumbers.append(tiles[i][j].val)
    n=0 # Number of inversions
    for i in range(len(gridNumbers)):
        for j in range(i+1,len(gridNumbers)):
            if gridNumbers[i]>gridNumbers[j]:
                n+=1

    return n # n is the variable holding number of inversions

    

        
def main():        
    # Create a 2D list of tiles, assigning the appropriate midpoints and initial ordered values.
    tiles=[[TILE(gapWidth*(j+1)+j*tileWidth+tileWidth//2,gapWidth*(i+1)+i*tileWidth+tileWidth/2,i*4+j) for j in range(gridSize)] for i in range(gridSize)]
    initTileValues(tiles)
    while not checkSolvability(tiles):
        initTileValues(tiles)
    drawGrid(tiles)
    play(tiles)
    


main()


