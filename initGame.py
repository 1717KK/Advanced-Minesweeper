from tkinter import *
import random
from PIL import Image, ImageTk
import math
import copy
from allClass import *


def initGame(data):
    data.level = 1
    imageSize1 = (50, 50)
    imageSize2 = (45, 45)
    imageSize3 = (70, 50)
    imageSize4 = (35, 35)
        
    # draw an explorer
    explorerImage1 = Image.open("explorer.gif")
    explorerPicture1 = explorerImage1.resize(imageSize1,Image.ANTIALIAS)
    data.explorer1 = ImageTk.PhotoImage(explorerPicture1)
    
    explorerImage2 = Image.open("explorer_flip.gif")
    explorerPicture2 = explorerImage2.resize(imageSize1,Image.ANTIALIAS)
    data.explorer2 = ImageTk.PhotoImage(explorerPicture2)
    
    # draw monster
    data.monster1 = imageShootingMonster()
    data.monster2 = imageMonster()
    
    # draw heart
    heartImage = Image.open("heart.gif")
    heartPicture = heartImage.resize(imageSize2,Image.ANTIALIAS)
    data.heart = ImageTk.PhotoImage(heartPicture)
    data.numOfHearts = 5
    
    # draw coin
    coinImage = Image.open("coin.gif")
    coinPicture = coinImage.resize(imageSize3,Image.ANTIALIAS)
    data.coin = ImageTk.PhotoImage(coinPicture)
    data.numOfCoins = 0
    
    # draw bomb
    bombImage = Image.open("bomb.gif")
    bombPicture = bombImage.resize(imageSize1,Image.ANTIALIAS)
    data.bomb = ImageTk.PhotoImage(bombPicture)
    data.numOfBombs = 0
    
    # draw door
    doorImage = Image.open("door.gif")
    doorPicture = doorImage.resize(imageSize1,Image.ANTIALIAS)
    data.door = ImageTk.PhotoImage(doorPicture)
    
    # draw roads
    roadImage2 = Image.open("road2.gif")
    roadPicture2 = roadImage2.resize(imageSize1,Image.ANTIALIAS)
    data.road2 = ImageTk.PhotoImage(roadPicture2)
    
    roadImage3 = Image.open("road3.gif")
    roadPicture3 = roadImage3.resize(imageSize1,Image.ANTIALIAS)
    data.road3 = ImageTk.PhotoImage(roadPicture3)
    
    roadImage4 = Image.open("road4.gif")
    roadPicture4 = roadImage4.resize(imageSize1,Image.ANTIALIAS)
    data.road4 = ImageTk.PhotoImage(roadPicture4)
    
    roadImage5 = Image.open("road5.gif")
    roadPicture5 = roadImage5.resize(imageSize1,Image.ANTIALIAS)
    data.road5 = ImageTk.PhotoImage(roadPicture5)  
    
    
    # draw stone
    wallImage = Image.open("wall.gif")
    wallPicture = wallImage.resize(imageSize1,Image.ANTIALIAS)
    data.wall = ImageTk.PhotoImage(wallPicture)
    
    # draw bullet
    data.bullet = imageBullet()
    data.numOfBullets = 50
    
    # draw map
    mapImage = Image.open("map.gif")
    mapPicture = mapImage.resize(imageSize2,Image.ANTIALIAS)
    data.oneMap = ImageTk.PhotoImage(mapPicture)
    data.numOfMaps = 0
    
    # draw sign
    signImage = Image.open("Exclamation.gif")
    signPicture = signImage.resize(imageSize4,Image.ANTIALIAS)
    data.sign = ImageTk.PhotoImage(signPicture)
    
    
# record position of Walls
def wallPosition(data): 
    rows = len(data.initMap)
    cols = len(data.initMap[0])
    cellSize = 50
    lst = []    
    for row in range(rows):
        for col in range(cols):
            if data.initMap[row][col] == 1:
                lst.append((row, col))
    return lst

# record coordinate of Walls
def wallCoordinate(data):
    lst = []
    cellSize = 50
    for wall in data.wallPos:
        row = wall[0]
        col = wall[1]
        cx = int(col * cellSize + cellSize / 2)
        cy = int(row * cellSize + cellSize / 2)
        lst.append((cx, cy))
    return lst

# record position of roads
def roadPosition(data):
    rows = len(data.initMap)
    cols = len(data.initMap[0])
    road = []    
    for row in range(rows):
        for col in range(cols):
            if data.initMap[row][col] != 1 and data.initMap[row][col] != 0:
                road.append((row, col))
    return road

# record position of shooting blue monsters
def shootingMonsterPos(data):
    road = roadPosition(data)
    numOfMonster = int(data.numMonster/2)
    data.newMap1 = copy.deepcopy(data.initMap)
    maxRow = 9
    maxCol = 19
    label = 6
    count = 0
    while count != numOfMonster:
        monsterPos = random.choice(road)
        row = monsterPos[0]
        col = monsterPos[1]
        if row != 0 and row != maxRow and col != 0 and col != maxCol:
            if data.newMap1[row][col] != label:
                data.newMap1[row][col] = label
                count += 1
    return data.newMap1

# record position of green monsters
def monsterPos(data):
    road = roadPosition(data)
    numOfMonster = int(data.numMonster/2)
    data.newMap2 = copy.deepcopy(data.newMap1)
    maxRow = 9
    maxCol = 19
    label = 7
    count = 0
    while count != numOfMonster:
        monsterPos = random.choice(road)
        row = monsterPos[0]
        col = monsterPos[1]
        if row != 0 and row != maxRow and col != 0 and col != maxCol:
            if data.newMap2[row][col] != label:
                data.newMap2[row][col] = label
                count += 1
    return data.newMap2
    
# record position of coins
def coinPos(data):
    data.newMap3 = copy.deepcopy(data.newMap2)
    maxRow = 9
    maxCol = 19
    label = 8
    count = 0
    while count != data.allCoins:
        row = random.randint(0, maxRow)
        col = random.randint(0, maxCol)
        if row != 0 and row != maxRow and col != 0 and col != maxCol:
            if data.newMap3[row][col] != label:
                data.newMap3[row][col] = label
                count += 1
    return data.newMap3

    
