from tkinter import *
import random
from PIL import Image, ImageTk
import math
import copy
import pygame
from allClass import *
from drawToolsBar import *
from initGame import *
from algorithm import *
       
####################################
# customize these functions
####################################

def init(data):
    data.initMap = [[random.randint(1, 5) for i in range(20)]for j in range(10)]
    data.initMap[0][0] = 0 # extrance
    data.initMap[9][19] = 0 # exit
    print(data.initMap)
    data.newMap1 = None # map for blue monsters
    data.newMap2 = None # map for green monsters
    data.newMap3 = None # map for coins
    
    data.wallPos = wallPosition(data)
    data.wallCoo = wallCoordinate(data)
    data.road = roadPosition(data)
    
    # initialize level, life , clues
    initGame(data)
    data.startGame = False
    data.gameOver = False
    data.win = False
    data.rule = False
    data.isCollectCoin = False
    data.useBomb = False
    data.useMap = False
    data.isDetonateMonster = False
    data.time = 0
    
    # initialize features of explorer
    data.explorer = Explorer(0, 0, data.explorer1) # row 5, col 1
    data.position = []
    data.bullets = [] # the explorer can shoot
    
    # initialize monsters and their's movement
    data.counter = 0
    data.numMonster = 20
    data.monsters = []
    data.index = 0 # num of shooting monster
    data.monsterBullets = [[] for i in range(int(data.numMonster/2))] # shooting monsters can make bullets
    data.shootingMonsterPos = shootingMonsterPos(data)
    data.monsterPos = monsterPos(data)
    data.monsterDefeated = 0
    
    # initialize tools
    data.allCoins = 10
    data.coinPos = coinPos(data)
    
    data.clue = clue(data)
    refreshMap(data)
    
    # play music
    pygame.mixer.init() 
    pygame.mixer.music.load('Happy_Tree_Friends.mp3') 
    pygame.mixer.music.play(-1)
    
        
    

#############################################
# controller
#############################################
    

def distance(cx, cy, x, y):
    distance = ((x - cx)  ** 2 + (y - cy) ** 2) ** 0.5
    r = 20
    return distance <= r

def mousePressed(event, data):
    # start game
    pos1 = (800, 450) # start
    pos2 = (650, 463) # rule
    pos3 = (950, 550) # come back home
    posBomb = (465, 520, 635, 580) # button of using bomb
    posMap = (810, 520, 980, 580) # button of using map
    if not data.gameOver and not data.win:
        if distance(pos1[0], pos1[1], event.x, event.y):
            if solveMaze(data):
                data.startGame = True
            else:
                init(data)
        elif distance(pos2[0], pos2[1], event.x, event.y):
            data.rule = True
        elif data.rule and distance(pos3[0], pos3[1], event.x, event.y):
            data.rule = False
        elif data.startGame:
            if data.numOfBombs > 0:
                if posBomb[0] <= event.x <= posBomb[2] and \
                    posBomb[1] <= event.y <= posBomb[3]:
                    data.useBomb = not data.useBomb
            if data.numOfMaps > 0:
                if posMap[0] <= event.x <= posMap[2] and \
                    posMap[1] <= event.y <= posMap[3]:
                    data.useMap = not data.useMap
            
    # start game again
    else:
        pos4 = (305, 450, 455, 500)
        pos5 = (505, 450, 655, 500)
        if pos4[0] <= event.x <= pos4[2] and pos4[1] <= event.y <= pos4[3]:
            # enter next level
            if data.win:
                level = data.level
                numOfHearts = data.numOfHearts
                numOfCoins = data.numOfCoins
                numOfBullets = data.numOfBullets
                numOfBombs = data.numOfBombs
                numOfMaps = data.numOfMaps
                monsterDefeated = data.monsterDefeated
                init(data)
                data.level = level
                data.numOfHearts = numOfHearts
                data.numOfCoins = numOfCoins 
                data.numOfBullets = numOfBullets 
                data.numOfBombs = numOfBombs
                data.numOfMaps = numOfMaps
                if solveMaze(data):
                    data.startGame = True
                    data.numMonster += 4
                    data.level += 1
                    data.numOfHearts += 1
                    if monsterDefeated >= 5:
                        data.numOfMaps += 1
                    if monsterDefeated >= 7:
                        data.numOfBombs += 1
            # start from level 1
            if data.gameOver:
                init(data)
                data.startGame = True
        if pos5[0] <= event.x <= pos5[2] and pos5[1] <= event.y <= pos5[3]:
            if data.win or data.gameOver:
                init(data)
            

def keyPressed(event, data):
    if not data.gameOver and not data.win:
        if event.keysym == "Up":
            if data.explorer.row == 0:
                pass
            else:
                data.explorer.move(-1, 0)
                data.explorer.rotate(90)
                data.isCollectCoin = False
                data.meetMonster = False
                if isWall(data):
                    data.explorer.move(1, 0)
                    data.initMap[data.position[0]][data.position[1]] = 1
        elif event.keysym == "Down":
            if data.explorer.row == 9:
                pass
            else:
                data.explorer.move(1, 0)
                data.explorer.rotate(270)
                data.isCollectCoin = False
                data.meetMonster = False
                if isWall(data):
                    data.explorer.move(-1, 0)
                    data.initMap[data.position[0]][data.position[1]] = 1
        elif event.keysym == "Right":
            data.explorer.image = data.explorer1
            if data.explorer.col == 19:
                pass
            else:
                data.explorer.move(0, 1)
                data.explorer.rotate(0)
                data.isCollectCoin = False
                data.meetMonster = False
                if isWall(data):
                    data.explorer.move(0, -1)
                    data.initMap[data.position[0]][data.position[1]] = 1
        elif event.keysym == "Left":   
            data.explorer.image = data.explorer2
            if data.explorer.col == 0:
                pass
            else:
                data.explorer.move(0, -1)
                data.explorer.rotate(180)
                data.isCollectCoin = False
                data.meetMonster = False
                if isWall(data):
                    data.explorer.move(0, 1)
                    data.initMap[data.position[0]][data.position[1]] = 1 
        elif event.keysym == "space":
            if data.numOfBullets > 0:
                data.bullets.append(data.explorer.makeBullet())
                data.numOfBullets -= 1
        elif event.char == "c":
            row = data.position[0]
            col = data.position[1]
            if data.newMap3[row][col] == 8:
                data.numOfCoins += 1
                data.isCollectCoin = True
            else:
                pass
        elif event.keysym == "Return":
            direction = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0],\
                        [0, 1], [1, -1], [1, 0], [1, 1]]
            if data.useBomb and data.numOfBombs > 0:
                data.numOfBombs -= 1
                for d in direction:
                    newRow = data.position[0] + d[0]
                    newCol = data.position[1] + d[1]
                    if newRow <= 9 and newCol <= 19:
                        data.initMap[newRow][newCol] = -1
                data.initMap[0][0] = 0
                data.initMap[9][19] = 0
                data.useBomb = False
            if data.useMap and data.numOfMaps > 0:
                data.numOfMaps -= 1
                for d in direction:
                    newRow = data.position[0] + d[0]
                    newCol = data.position[1] + d[1]
                    if newRow <= 9 and newCol <= 19:
                        if data.newMap3[newRow][newCol] == 6 or \
                            data.newMap3[newRow][newCol] == 7:
                                data.initMap[newRow][newCol] = 10
                data.useMap = False
                    
    
def timerFired(data):
    if data.startGame:
        data.counter += 1        
        if not data.gameOver and not data.win:
            if data.counter % 10 == 0:
                data.time += 1
    
    # the explorer's bullets
    for bullet in data.bullets:
        # move bullets
        bullet.moveBullet()
    
    # the shooting monsters' bullets
    for i in range(data.index):
        for bullet in data.monsterBullets[i]:
            bullet.moveBullet()
    
    for monster in data.monsters:
        monster.reactToWall(data.wallCoo)
        monster.moveMonster()
        if isinstance(monster, ShootingMonster) and data.counter % 5 == 0:
            for i in range(data.index):
                newBullet = monster.makeBullet()
                data.monsterBullets[i].append(newBullet)
        if data.explorer.collide(monster):
            data.numOfHearts -= 1

    removeBullet(data)
    removeBulletAndMonster(data)

# if bullet collides with wall, it will be removed
def removeBullet(data):
    for bullet in data.bullets:
        for wall in data.wallPos:
            if bullet.collidesWithWall(wall):
                data.bullets.remove(bullet) 
    
    for i in range(data.index):          
        for bullet in data.monsterBullets[i]:
            for wall in data.wallPos:
                if bullet.collidesWithWall(wall):
                    data.monsterBullets[i].remove(bullet)
                
# if bullet collides with the explorer or monster, it will be removed
def removeBulletAndMonster(data):
    for bullet in data.bullets:
        for monster in data.monsters:
            if bullet.collide(monster):
                data.bullets.remove(bullet)
                data.monsters.remove(monster)
                data.monsterDefeated += 1
    
    for i in range(data.index):
        for bullet in data.monsterBullets[i]:
            if bullet.collide(data.explorer):
                data.monsterBullets[i].remove(bullet)
                data.numOfHearts -= 1
                if data.numOfHearts <= 0:
                    data.gameOver = True
    


####################################
# move the explorer and monsters
####################################

# the explorer cannot move if a wall is in front of him        
def isWall(data):
    row = data.explorer.row
    col = data.explorer.col
    data.position = [row, col]
    if data.initMap[row][col] == 1:
        return True 
             

###################################
# start the game!!!
###################################

def gameStarted(data, canvas):
    # name of game
    pos1 = (725, 350)
    canvas.create_text(pos1[0], pos1[1], text = "MINESWEEPER", fill = "white", \
                        font = ('Helvetica', '30'))
    pos2 = (650, 450)
    pos3 = (800, 450)
    r1 = 20
    # game rules
    canvas.create_oval(pos2[0] - r1, pos2[1] - r1, pos2[0] + r1, pos2[1] + r1,\
                        outline = "white", width = 2)
    pos4 = (640, 447)
    pos5 = (650, 437)
    pos6 = (660, 447)
    pos7 = (650, 457)
    pos8 = (650, 463)
    r2 = 1.5
    canvas.create_line(pos4[0], pos4[1], pos5[0], pos5[1], \
                        fill = "white", width = 2)
    canvas.create_line(pos5[0], pos5[1], pos6[0], pos6[1], \
                        fill = "white", width = 2)
    canvas.create_line(pos6[0], pos6[1], pos7[0], pos7[1], \
                        fill = "white", width = 2)
    canvas.create_oval(pos8[0] - r2, pos8[1] - r2, pos8[0] + r2, pos8[1] + r2, \
                        fill = "white", width = 0)
    # button of starting game
    pos9 = (792, 440)
    pos10 = (812, 450)
    pos11 = (792, 460)
    canvas.create_polygon(pos9[0], pos9[1], pos10[0], pos10[1], \
                          pos11[0], pos11[1], fill = "white")
    canvas.create_oval(pos3[0] - r1, pos3[1] - r1, pos3[0] + r1, pos3[1] + r1, \
                       outline = "white", width = 2)
    

#############################################
# draw explorer, walls and roads
#############################################

def drawMap(data, canvas):
    cellSize = 50
    cols = 20
    rows = 10
    for col in range(cols):
        for row in range(rows):
            x0 = col * cellSize + cellSize / 2
            y0 = row * cellSize + cellSize / 2
            cx = int(x0)
            cy = int(y0)
            positionOfRoad = (cx, cy)
            if data.initMap[row][col] == 0: 
                canvas.create_image(x0, y0, image = data.door, anchor= 'center')
            elif data.initMap[row][col] == 1:
                canvas.create_image(x0, y0, image = data.wall, anchor= 'center')
            elif data.initMap[row][col] == 2:
                canvas.create_image(x0, y0, image = data.road2, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 3:
                canvas.create_image(x0, y0, image = data.road3, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 4:
                canvas.create_image(x0, y0, image = data.road4, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 5:
                canvas.create_image(x0, y0, image = data.road5, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 6:
                # shooting blue monster
                canvas.create_image(x0, y0, image = data.monster1, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 7:
                # non-shooting green monster
                canvas.create_image(x0, y0, image = data.monster2, \
                                    anchor= 'center')
            elif data.initMap[row][col] == 8:
                # coin
                canvas.create_image(x0, y0, image = data.coin, anchor= 'center')
            elif data.initMap[row][col] == 9:
                # clue
                canvas.create_text(x0, y0, text = str(data.clue[(row, col)]), \
                                    fill = "white", font = ('Helvetica', '20'),\
                                     anchor= 'center')
            elif data.initMap[row][col] == 10:
                # coin
                canvas.create_image(x0, y0, image = data.sign, anchor= 'center')

                    
def refreshMap(data):
    if data.position != []:
        row = data.position[0]
        col = data.position[1]
        # walls and doors cannot be opened
        if data.initMap[row][col] != 1 and data.initMap[row][col] != 0:
            data.initMap[row][col] = -1 
            direction = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
            if data.newMap3[row][col] == 6: # map of shooting blue monster
                data.isDetonateMonster = True
                data.monsters.append(ShootingMonster(row, col, direction))
                data.index += 1
                if data.isDetonateMonster:
                    data.numOfHearts -= 1
                data.newMap3[row][col] = -1
                data.isDetonateMonster = False
            elif data.newMap3[row][col] == 7: # map of green monster
                data.isDetonateMonster = True
                data.monsters.append(Monster(row, col, direction))
                if data.isDetonateMonster:
                    data.numOfHearts -= 1
                data.newMap3[row][col] = -1
                data.isDetonateMonster = False
            elif data.newMap3[row][col] == 8: # map of coin
                if data.isCollectCoin == False:
                    data.initMap[row][col] = 8
                else:
                    data.initMap[row][col] = -1
                    data.newMap3[row][col] = -1
            elif (row, col) in data.clue: # map of clue
                data.initMap[row][col] = 9
        if row == 9 and col == 19:
            data.win = True

def cleanMap(canvas, data):
    row = data.position[0]
    col = data.position[1]
    cellSize = 50
    cx = col * cellSize + cellSize/2
    cy = row * cellSize + cellSize/2
    size = 75
    x0 = cx - size
    y0 = cy - size
    x1 = cx + size
    y1 = cy + size
    y2 = cy + size/2 - 15
    if row  < 9:
        canvas.create_rectangle(x0, y0, x1, y1, outline = "white", width = 3)
    else:
        canvas.create_rectangle(x0, y0, x1, y2, outline = "white", width = 3)
            
def rule(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, \
                            fill = "black")
    canvas.create_text(850, 35, text = "Game Rules", fill = "white", \
                        font = ('Helvetica', '30')) 
    rules = "Goals:\n- Collect coins(Press 'c') as much as possible and "+\
            "escape the maze in the shortest time\n\nHeart: \n"+\
            "- The explorer will have 3 hearts at the beginning of"+\
            " game.\n"+\
            "- The explorer will get one more heart while entering"+\
            " the next level.\n"+\
            "- The explorer will lose 1 heart while detonating"+\
            " monsters or being shooted by monsters.\n\n"+\
            "Bomb:\n"+"- The explorer will have 1 bomb at the"+\
            " beginning of game.\n"+\
            "- Bomb can be used for cleaning 9 grid around the"+\
            " explorer. Hidden monsters and coins will be cleaned\n"+\
            "  as well.\n"+\
            "- If the explorer defeats more than 7 monsters, he will"+\
            " get one more bomb while entering the next level.\n"+\
            "- Click on 'Bomb' and press 'Enter' to use it.\n\n"+\
            "Bullet:\n"+\
            "- The explorer will have 50 bullets at the beginning of"+\
            " game.\n"+\
            "- The explorer presses 'Space' to shoot monsters.\n"+\
            "- Consumed Bullets won't come back.\n\n"+\
            "Map:\n- The explorer won't have map at the beginning of"+\
            " game.\n"+\
            "- If the explorer defeats more than 5 monsters, he will"+\
            " get one more map while entering the next level.\n"+\
            "- Map can be used for checking if there are any monsters"+\
            " hidden under the 8 nearby grids.\n"+\
            "- Click on 'Map' and press 'Enter' to use it."
    canvas.create_text(500, 300, text = rules, fill = "white", \
                        font = ('Garamond', '15'))     
    r = 20
    canvas.create_oval(950 - r, 550 - r, 950 + r, 550 + r, \
                        outline = "white", width = 2)  
    canvas.create_line(940, 550, 960, 540, fill = "white", width = 2) 
    canvas.create_line(940, 550, 960, 560, fill = "white", width = 2) 
    
def drawInfo(canvas, data):
    canvas.create_text(400, 300, \
                        text = " Time: \n Coin gathered: \n" + \
                        " Monster defeated: \n Level reached:", \
                        fill = "white", font = ('Garamond', '20'))
    canvas.create_text(650, 300, text = str(data.time) + "\n" + \
                        str(data.numOfCoins) + "\n" + \
                        str(data.monsterDefeated) + "\n" \
                        + str(data.level), fill = "white", \
                        font = ('Garamond', '20'))
    canvas.create_rectangle(305, 450, 455, 500, outline = "white", \
                            width = 1)
    canvas.create_rectangle(505, 450, 655, 500, outline = "white", \
                            width = 1)
    canvas.create_text(580, 475, text = "Home", fill = "white", \
                        font = ('Helvetica', '15'))
    
def redrawAll(canvas, data):
    if not data.startGame:
        gameStarted(data, canvas) 
        if data.rule:
            rule(canvas, data)
    else:
        if data.gameOver:
            canvas.create_rectangle(0, 0, data.width, data.height, \
                                    fill = "black")            
            canvas.create_text(300, 100, text = "Better Luck Next Time", \
                               fill = "white", font = ('Helvetica', '30'))                                           
            drawInfo(canvas, data)
            canvas.create_text(380, 475, text = "New Game", fill = "white", \
                                font = ('Helvetica', '15'))
        elif data.win:
            canvas.create_rectangle(0, 0, data.width, data.height, \
                                    fill = "black")            
            canvas.create_text(300, 100, text = "Congratulation", \
                               fill = "white", font = ('Helvetica', '30'))                                           
            drawInfo(canvas, data)
            canvas.create_text(380, 475, text = "Next Level", fill = "white", \
                                font = ('Helvetica', '15'))
        else:
            drawMap(data, canvas)
            drawToolsBar(data, canvas)
            refreshMap(data)
            for bullet in data.bullets:
                bullet.draw(canvas)
                if bullet.isOffScreen(1000, 500):
                    data.bullets.remove(bullet)
            for monster in data.monsters:
                monster.draw(canvas)
            for i in range(data.index):
                for bullet in data.monsterBullets[i]:
                    bullet.draw(canvas)
                    if bullet.isOffScreen(1000, 500):
                        data.monsterBullets[i].remove(bullet)
            data.explorer.draw(canvas)
            if data.useBomb and data.position != []:
                cleanMap(canvas, data)
            if data.useMap and data.position != []:
                cleanMap(canvas, data)
            
            
        


####################################
# use the run function as-is
# most of the below codes are cited from 15-112 website
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='#1b335e', width=0) 
        
        # update the picture to canvas
        canvas.create_image(0, 0, image=data.background, anchor= 'nw')
        if data.startGame:
            canvas.create_image(0, 0, image=data.background1, anchor= 'nw')            
        
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    
    # create background
    pilImage = Image.open("start_game.gif")
    picture = pilImage.resize((data.width, data.height),Image.ANTIALIAS)
    data.background = ImageTk.PhotoImage(picture)
    
    pilImage1 = Image.open("background1.gif")
    picture1 = pilImage1.resize((data.width, data.height-100),Image.ANTIALIAS)
    data.background1 = ImageTk.PhotoImage(picture1)

    canvas.pack(padx=0, pady=0)
    
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    pygame.mixer.music.stop()
    print("bye!")

run(1000, 600)
