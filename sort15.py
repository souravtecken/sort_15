# By Chirag Srinivas, Mihir Patil and Sourav Raveendran

# Standard Libraries
import random
import datetime
import os
# Third Party Libraries
from graphics import *
from PIL import Image as im
# User defined 
import image


# -----------------Global Variables-------------------------

bgCOLOR = "white"
gapWidth=1
tileWidth=100
gridSize=4
animationSpeed=20
imageFileName="image.jpg"
imageWidth=(tileWidth*gridSize+gapWidth*(gridSize+1))*0.5 # Half of the puzzle width - Size of image being show on the right
screenWidth=(tileWidth*gridSize+gapWidth*(gridSize+1))*3/2 # 1.5 times the puzzle width 
screenHeight=tileWidth*gridSize+gapWidth*(gridSize+1)

# ----------------------------------------------------------




class TILE:
    def __init__(self,x=0,y=0,value=0,img=0):
        self.x=x
        self.y=y    
        self.val=value
        self.img=img


    def drawTile(self):
        if self.val!=0:
            r=Rectangle(Point(self.x-tileWidth//2,self.y-tileWidth//2),Point(self.x+tileWidth//2,self.y+tileWidth//2))    
            r.setFill("black")
            r.setWidth(0)
            rText=Text(Point(self.x,self.y),str(self.val))
            rText.setFill("white")
            r.draw(win)
            rText.draw(win)
            if imageFileName:
                img=Image(Point(self.x,self.y),self.img)
                img.draw(win)
            


# The graphic window - Height and width set according to tile width, gap width and number of tiles.
win=GraphWin("Sort 15", (tileWidth*gridSize+gapWidth*(gridSize+1))*3/2,tileWidth*gridSize+gapWidth*(gridSize+1),autoflush=False)
win.setBackground("white")


    


# Function to assign random number values to the tiles, and to assign corresponding image piece to that tile.
def initTileValues(tiles):
    global imageFileName
    numbers=list(range(gridSize*gridSize))
    if not os.path.isfile(imageFileName):
        imageFileName=""

    # imageGrid stores image objects created in the image.py file
    if imageFileName:
        imageGrid=image.cropImageIntoGrid(imageFileName,gridSize,tileWidth)

    for i in range(gridSize):
        for j in range(gridSize):
            tiles[i][j].val=random.choice(numbers)
            numbers.remove(tiles[i][j].val)
            if imageFileName:
                tileValue=tiles[i][j].val         #tileValue used to hold the value of the tile for some operations
                if tileValue==0:                  # Attempting to map the values of the tiles to the corresponding section of the image
                    tileValue=gridSize*gridSize-1 # grid. Number 1 corresponds to the image piece in the first row first, column, so on.
                else:                             # The tile with value 0 must get the bottom right most piece of the picture. (Because it's not displayed) 
                    tileValue-=1                  
                ii=tileValue//gridSize           # Based on tileValue, I assign the tile its corresponding image section.
                jj=tileValue%gridSize            # This's done by determining the row and column number.
                tiles[i][j].img=imageGrid[ii][jj] 
# For example, in a 4*4 grid:
# Value 1 will be in the first row first column, value 4 will be in the 1st row 4th column.
# Value 5 will be in the second row, first column, so on...

#Function to draw the entire grid of tiles.
def drawGrid(tiles):
    r=Rectangle(Point(0,0),Point(screenHeight,screenWidth))
    r.setFill(bgCOLOR)
    r.draw(win)
    for i in range(gridSize):
        for j in range(gridSize):
            tiles[i][j].drawTile()

# Function to return number of inversions
# Inversion - The total number of cases where a tile has a greater value than a tile on it's right, when all tiles in the grid are
# laid down in a straight line.
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



#Checks if the given tile state is solvable, not all combinations are solvable.
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


# Function to draw the image on the right.
def createSideBar():
    if imageFileName:
        img=im.open(imageFileName)
        
        img=img.resize((int(imageWidth),int(imageWidth)))
        winImage=Image(Point(screenWidth-imageWidth/2,screenHeight-imageWidth/2),img)
        winImage.draw(win)

# Function that displays the timer on the right.
def updateTimer(timeStart):
    timeNow=datetime.datetime.now()
    timeDif=timeNow-timeStart
    minutes,seconds=divmod(timeDif.seconds,60)
    timeString=str(minutes)+":"+str(seconds)
    r=Rectangle(Point(screenWidth-imageWidth,0),Point(screenWidth,imageWidth))
    r.setFill(bgCOLOR)
    r.draw(win)
    timerText=Text(Point(screenWidth-imageWidth/2,imageWidth/2),timeString)
    timerText.setSize(35)
    timerText.draw(win)





# Function checks if the mouse click was on a tile.
# Parameters - THe tile grid, and coordinates of mouseclick.
# Returns tuple(tile that was clicked, row number, column number); False if no tile was clicked.
def checkIfTileClicked(tiles,mouseClick):
    for i in range(gridSize):
        for j in range(gridSize):
            if mouseClick.x>tiles[i][j].x-tileWidth/2 and mouseClick.y<tiles[i][j].y+tileWidth/2:
                if mouseClick.x<tiles[i][j].x+tileWidth/2 and mouseClick.y>tiles[i][j].y-tileWidth/2:
                    return tiles[i][j],i,j
    return False



# Function checks if the clicked tile can move either horizontally or vertically
# Parameters - The tile grid, tuple(tile that was clicked, row number, column number)
# Returns - The tuple(zero tile, row number, column number); False if tile can't move
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




# Function to move all tiles that can move
# Parameters - The tile grid, tuple(Tile that was clicked, row number, column number), tuple(zero tile, row number, column number)
# The set of tiles move towards the zero tile, The zero tile obtains coordinates of the tile that was clicked after movement's over.
def moveTiles(tiles,fTile,lTile):
    firstTileCoordinates=fTile[0].x,fTile[0].y  # The coordinates of the tile that was clicked.
    if fTile[1]==lTile[1]: # Checks if the clicked tile and zero tile are on the same row, if yes - horizontal movement.
        i=fTile[1] # Since it's horizontal movement, the row number is common - Stored in 'i' for easy usage.
        if fTile[2]>lTile[2]: # Checks if clicked tile is to the right of zero tile, if yes - left movement
            while not tiles[i][lTile[2]+1].x==lTile[0].x: # The movement is carried out till the tile next to the zero tile gets the same x coordinate as the zero tile.
                speed=animationSpeed
                if(tiles[i][lTile[2]+1].x-lTile[0].x<animationSpeed):
                    # If the distance to be moved is less than speed, I make the tiles move only by that distance, else tile will cross destination
                    speed=tiles[i][lTile[2]+1].x-lTile[0].x
                for j in range(lTile[2]+1,fTile[2]+1): # Selects all tiles that need to be moved. These tiles lie in [fTile,lTile)
                    r=Rectangle(Point(tiles[i][j].x-tileWidth/2,tiles[i][j].y-tileWidth/2),Point(tiles[i][j].x+tileWidth/2,tiles[i][j].y+tileWidth/2))
                    r.setFill("white")
                    r.setWidth(0)
                    r.draw(win)
                    tiles[i][j].x-=speed
                    tiles[i][j].drawTile()
                    update(200)
        else: # Clicked tile is to the left of zero tile, movement is to the right.
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
    else: # Else, the clicked tile and zero tile are in the same column - vertical movement
        j=fTile[2] # The column number is common this time
        if fTile[1]>lTile[1]: # Checks if clicked tile is below zero tile, if yes - Movement up
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
        else: # Else, clicked tile is above zero tile, movement down
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



# Function to sort the tiles in the 2D array according to their coordinates which have changed because of movement.
def sortTilesInGrid(tiles):
    # Sort each row according to their x-coordinates
    for i in range(gridSize):   
        gridRow=list(tiles[i])
        gridRow=sorted(tiles[i],key=lambda tile:tile.x)
        tiles[i]=gridRow        

    # Sort each column according to their y-coordinates
    for j in range(gridSize):
        gridColumn=[]
        for i in range(gridSize):
            gridColumn.append(tiles[i][j])
        gridColumn=sorted(gridColumn,key=lambda tile:tile.y)

        for i in range(gridSize):
            tiles[i][j]=gridColumn[i]


# Checks if all the tiles in the grid are in order, if yes - The game is complete
def checkCompletion(tiles):
    for i in range(gridSize):
        for j in range(gridSize):
            # If the tile value doesn't correspond to the numeric order and the tile being checked is not the last tile.
            if(tiles[i][j].val!=gridSize*i+j+1 and not i+j==(gridSize-1)*2):
                return False
    return True



    

def play():
    # Create a 2D list of tiles, assigning the appropriate midpoints and initial ordered values.
    tiles=[[TILE(gapWidth*(j+1)+j*tileWidth+tileWidth//2,gapWidth*(i+1)+i*tileWidth+tileWidth/2,i*gridSize+j) for j in range(gridSize)] for i in range(gridSize)]
    initTileValues(tiles)
    while not checkSolvability(tiles):
        initTileValues(tiles)
    drawGrid(tiles)
    createSideBar()
    
    timeStart=0
    timeEnd=0
    numberOfClicks=0
    
    while not checkCompletion(tiles):
        mouseClick=win.checkMouse()
        tileClicked=False
        if mouseClick:
            tileClicked=checkIfTileClicked(tiles,mouseClick)
        tileCanMove=False
        if tileClicked:
            numberOfClicks+=1
            if numberOfClicks==1:
                timeStart=datetime.datetime.now()
            tileCanMove=checkTilesMove(tiles,tileClicked)
        if tileCanMove:
            moveTiles(tiles,tileClicked,tileCanMove)
            sortTilesInGrid(tiles)
        if timeStart:
            updateTimer(timeStart)
    timeEnd=datetime.datetime.now()
    return win.getKey()

       
    

        
def main():
    while not play()=="Escape":
        pass

main()


