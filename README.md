# sort_15
A python implementation of the popular grid sorting game.

To run:
1. Install tkinter:
```
sudo apt-get install python3-tk
```
2. Install Pillow (PIL Fork)
```
pip install Pillow
```
3. Use the graphics.py file within the repository. 
4. Run sort15.py


The graphics.py used is a slightly modified version of the standard graphics library:
[graphics.py](http://mcsp.wartburg.edu/zelle/python/graphics.py)

Changes made to the Image class to accept an image as a PIL Image object rather than the file name.
------------------------------------------------------------------------------------------------------

To customize:
Global variables in sort15.py
1. gapWidth : Border size
2. tileWidth : Width of the tile
3. gridSize : Number of tiles per row/column
4. imageFileName : Name of image with extension being used. Image must be in the same directory as the program.
