from tkinter import *
import random
from PIL import Image, ImageTk
import math
import copy

####################################    
# draw tools bar
####################################

def drawToolsBar(data, canvas):
    
    # draw levels
    cx1 = 55
    cy1 = 530
    cx2 = 55
    cy2 = 570
    canvas.create_text(cx1, cy1, text = "LEVEL", fill = "white", \
                        font = ('Helvetica', '20'))
    canvas.create_text(cx2, cy2, text = str(data.level), fill = "white", \
                        font = ('Helvetica', '25'))
    
    # draw tools bar
    cellSize = 172
    numOfCellSize = 5
    for col in range(numOfCellSize):
        x0 = 120 + col * cellSize
        y0 = 520
        x1 = x0 + cellSize
        y1 = 580
        canvas.create_rectangle(x0, y0, x1, y1, outline = "white", width = 2)
    
    # draw heart
    drawHeart(data, canvas)
    
    # draw tools
    drawTools(data, canvas)
    
def drawHeart(data, canvas):
    
    # draw heart
    x0 = 180
    y0 = 550
    canvas.create_image(x0, y0, image = data.heart, anchor= 'center')
    
    # num of hearts
    x1 = 235
    y1 = 550
    canvas.create_text(x1, y1, text = str(data.numOfHearts), fill = "white", \
                        width = 2, font = ('Helvetica', '20'))
    

def drawTools(data, canvas):
    
    # draw coin
    x0 = 345
    y0 = 550
    canvas.create_image(x0, y0, image = data.coin, anchor= 'center')
    
    # num of coins
    x1 = 412
    y1 = 550
    canvas.create_text(x1, y1, text = str(data.numOfCoins), fill = "white", \
                        width = 2, font = ('Helvetica', '20'))                        
    
    # draw bomb
    x2 = 515
    y2 = 550
    canvas.create_image(x2, y2, image = data.bomb, anchor= 'center')
    
    # num of bombs
    x3 = 579
    y3 = 550
    canvas.create_text(x3, y3, text = str(data.numOfBombs), fill = "white", \
                        width = 2, font = ('Helvetica', '20'))
                        
    # draw bullet
    x4 = 685
    y4 = 558
    canvas.create_image(x4, y4, image = data.bullet, anchor= 'center')
    
    # num of bullets
    x5 = 750
    y5 = 550
    canvas.create_text(x5, y5, text = str(data.numOfBullets), fill = "white", \
                        font = ('Helvetica', '20'))
                        
    # draw map
    x6 = 865
    y6 = 548
    canvas.create_image(x6, y6, image = data.oneMap, anchor= 'center')
    
    # num of maps
    x7 = 930
    y7 = 550
    canvas.create_text(x7, y7, text = str(data.numOfMaps), fill = "white", \
                        font = ('Helvetica', '20'))  