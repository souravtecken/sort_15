from graphics import *
from PIL import Image as im



# Function to resize given image based on the size of the graphics window.
# If the image is a 200*200 image, but there are 16 tiles of width 100 each, the image will be resized to a 400*400 image
def resizeImage(image,gridSize,tileWidth):
    image=image.resize((gridSize*tileWidth,gridSize*tileWidth))
    return image


# Function to divide given image into a grid based on the number of tiles and width of the tile.
# It does it by first resizing the image and then croping out required sections from the main image.
def cropImageIntoGrid(imageFileName,gridSize,tileWidth):
    image=im.open(imageFileName)
    image=resizeImage(image,gridSize,tileWidth)
    imageGrid=[[image.crop((j*tileWidth,i*tileWidth,(j+1)*tileWidth,(i+1)*tileWidth)) for j in range(gridSize)] for i in range(gridSize)]
    #
    # image.crop requires the top left point and the bottom right point.
    # top left point - (j*tileWidth,i*tileWidth) 
    # bottom right point - ((j+1)*tileWidth , (i+1)*tileWidth))
    # Where j and i correspond to column number and row number starting from 0.
    return imageGrid










