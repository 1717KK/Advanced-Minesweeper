from tkinter import *
import random
from PIL import Image, ImageTk
import math
import copy


####################################
def imageShootingMonster():
    shootingMonsterImage = Image.open("monster1.gif")
    shootingMonsterPicture = shootingMonsterImage.resize((50, 50),Image.ANTIALIAS)
    shootingMonster = ImageTk.PhotoImage(shootingMonsterPicture)
    return shootingMonster
    
def imageMonster():
    monsterImage = Image.open("monster2.gif")
    monsterPicture = monsterImage.resize((50, 50),Image.ANTIALIAS)
    monster = ImageTk.PhotoImage(monsterPicture)
    return monster
    
class Monster(object):
    def __init__(self, row, col, direction):
        # A monster has a position, speed, and direction
        self.row = row
        self.col = col
        self.direction = direction
        self.image = imageMonster()
        self.cellSize = 50
        self.cx = int(self.col * self.cellSize + self.cellSize / 2)
        self.cy = int(self.row * self.cellSize + self.cellSize / 2)
        self.speed = 0.5
        print(self.row, self.col)
    
        
    # View
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image, anchor= 'center')
    
    def moveMonster(self):
        self.cx += self.speed * self.direction[0]
        self.cy += self.speed * self.direction[1]
        #print(self.cx, self.cy)
        #self.row += self.direction[0]
        #self.col += self.direction[1]
    
    # If the monster reach the edge of the wall and screen, they bounce  
    
    def reactToWall(self, wall):
        cellSize = 50
        row = wall[0]
        col = wall[1]
        x = int(col * cellSize + cellSize / 2)
        y = int(row * cellSize + cellSize / 2)
        disX = abs(self.cx - x)
        disY = abs(self.cy - y)
        if disX < cellSize:
            self.direction[0] = - self.direction[0]
        elif self.cx < 25 or self.cx > 975:
            self.direction[0] = - self.direction[0] 
        elif disY < cellSize:
            self.direction[1] = - self.direction[1]
        elif self.cy < 25 or self.cy > 475:
            self.direction[1] = - self.direction[1]

           
class ShootingMonster(Monster):
    def _init_(self, row, col, direction):
        super().__init__(self, row, col, direction)
        self.image = imageShootingMonster()
    
    def draw(self, canvas):
        super().draw(canvas)
    

    def makeBullet(self):
        offset = 35
        angle = self.direction[0] * 90  # still have some bugs.....
        x0 = self.col * self.cellSize + self.cellSize / 2
        y0 = self.row * self.cellSize + self.cellSize / 2
        x = x0 + offset*math.cos(math.radians(angle)) 
        y = y0 - offset*math.sin(math.radians(angle))
        speed = 20

        return MonsterBullet(x, y, angle, speed)


class Explorer(object):
    def __init__(self, row, col, image):
        self.row = row 
        self.col = col
        self.image = image
        self.cellSize = 50
        self.angle = 0
    
    def draw(self, canvas):
        x0 = self.col * self.cellSize + self.cellSize / 2
        y0 = self.row * self.cellSize + self.cellSize / 2
        canvas.create_image(x0, y0, image = self.image, anchor= 'center')
        
    def move(self, drow, dcol):
        if 0 <= self.row <= 11 and 0 <= self.col <= 19:
            self.row += drow
            self.col += dcol
    
    # this function is set for control direction of shooting bullets
    def rotate(self, newAngle):
        self.angle = newAngle
            
    def makeBullet(self):
        # Generates a bullet heading in the direction the ship is facing
        offset = 35
        x0 = self.col * self.cellSize + self.cellSize / 2
        y0 = self.row * self.cellSize + self.cellSize / 2
        x = x0 + offset*math.cos(math.radians(self.angle)) 
        y = y0 - offset*math.sin(math.radians(self.angle))
        speedLow, speedHigh = 20, 40

        return Bullet(x, y, self.angle, random.randint(speedLow, speedHigh))

# helper function of loading image
def imageBullet():
    bulletImage = Image.open("bullet.gif")
    bulletPicture = bulletImage.resize((150, 150),Image.ANTIALIAS)
    bullet = ImageTk.PhotoImage(bulletPicture)
    return bullet           
    
class Bullet(object):
    # Model
    def __init__(self, cx, cy, angle, speed):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.angle = angle
        self.speed = speed 
        #self.image = imageBullet()
        self.num = 100
    
    # View
    def draw(self, canvas):
        image = imageBullet()
        canvas.create_image(self.cx, self.cy, image = image, anchor= 'center')

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed
        
    def collidesWithWall(self, wall):
        cellSize = 50
        row = wall[0]
        col = wall[1]
        x = int(col * cellSize + cellSize / 2)
        y = int(row * cellSize + cellSize / 2)
        disX = abs(self.cx - x)
        disY = abs(self.cy - y)
        if disX < cellSize / 2 and disY < cellSize / 2:
            return True
            
    def collide(self, other):
        cellSize = 50
        if(not isinstance(other, Monster)) : # Other must be a Monster
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            if dist < cellSize / 2:
                return True
        

    '''
    def isOffscreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        return (self.cx + self.r <= 0 or self.cx - self.r >= width) or \
               (self.cy + self.r <= 0 or self.cy - self.r >= height)
               
    '''
    
class MonsterBullet(Bullet):
    def __init__(self, cx, cy, angle, speed):
        super().__init__(self, cx, cy, angle, speed)
        self.r = 5
    
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, \
                           self.cx - self.r, self.cy - self.r, \
                           fill = "white", width = 0)
                           
    def collide(self, other):
        cellSize = 50
        if(not isinstance(other, Explorer)) : # Other must be an Explorer
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            if dist < cellSize / 2:
                return True


####################################
# customize these functions
####################################

def init(data):
    data.initMap = [[random.randint(1, 5) for i in range(20)]for j in range(10)]
    data.initMap[5][0] = 0 # extrance
    data.initMap[5][19] = 0 # exit
    data.newMap1 = None
    data.newMap2 = None
    data.wallPos= wallPosition(data)
    #print(data.wallPos)
    data.road = roadPosition(data)
    
    # initialize level, life and all tools
    initGame(data)
    data.startGame = False
    #data.isMap = False
    
    # initialize features of explorer
    data.explorer = Explorer(5, 0, data.explorer) # row 5, col 0
    data.position = []
    data.bullets = [] # the explorer can shoot
    
    # initialize monsters and their's movement
    data.counter = 0
    data.monsters = []
    data.monsterBullets = []
    data.shootingMonsterPos = shootingMonsterPos(data)
    data.monsterPos = monsterPos(data)
    #monsterMoving(data)
    
    refreshMap(data)
    

def initGame(data):
    data.level = 1
        
    # draw an explorer
    explorerImage = Image.open("explorer.gif")
    explorerPicture = explorerImage.resize((50, 50),Image.ANTIALIAS)
    data.explorer = ImageTk.PhotoImage(explorerPicture)
    
    # draw monster
    data.monster1 = imageShootingMonster()
    data.monster2 = imageMonster()
    
    # draw heart
    heartImage = Image.open("heart.gif")
    heartPicture = heartImage.resize((45, 45),Image.ANTIALIAS)
    data.heart = ImageTk.PhotoImage(heartPicture)
    data.numOfHearts = 3
    
    # draw coin
    coinImage = Image.open("coin.gif")
    coinPicture = coinImage.resize((70, 50),Image.ANTIALIAS)
    data.coin = ImageTk.PhotoImage(coinPicture)
    data.numOfCoins = 0
    
    # draw bomb
    bombImage = Image.open("bomb.gif")
    bombPicture = bombImage.resize((50, 50),Image.ANTIALIAS)
    data.bomb = ImageTk.PhotoImage(bombPicture)
    data.numOfBombs = 0
    
    # draw door
    doorImage = Image.open("door.gif")
    doorPicture = doorImage.resize((50, 50),Image.ANTIALIAS)
    data.door = ImageTk.PhotoImage(doorPicture)
    
    # draw roads
    roadImage2 = Image.open("road2.gif")
    roadPicture2 = roadImage2.resize((50, 50),Image.ANTIALIAS)
    data.road2 = ImageTk.PhotoImage(roadPicture2)
    
    roadImage3 = Image.open("road3.gif")
    roadPicture3 = roadImage3.resize((50, 50),Image.ANTIALIAS)
    data.road3 = ImageTk.PhotoImage(roadPicture3)
    
    roadImage4 = Image.open("road4.gif")
    roadPicture4 = roadImage4.resize((50, 50),Image.ANTIALIAS)
    data.road4 = ImageTk.PhotoImage(roadPicture4)
    
    roadImage5 = Image.open("road5.gif")
    roadPicture5 = roadImage5.resize((50, 50),Image.ANTIALIAS)
    data.road5 = ImageTk.PhotoImage(roadPicture5)  
    
    
    # draw stone
    wallImage = Image.open("wall.gif")
    wallPicture = wallImage.resize((50, 50),Image.ANTIALIAS)
    data.wall = ImageTk.PhotoImage(wallPicture)
    
    # draw bullet
    data.bullet = imageBullet()
    data.numOfBullets = 50
    
    # draw map
    mapImage = Image.open("map.gif")
    mapPicture = mapImage.resize((45, 45),Image.ANTIALIAS)
    data.oneMap = ImageTk.PhotoImage(mapPicture)
    data.numOfMaps = 0
    
# record position of Walls
def wallPosition(data): 
    rows = len(data.initMap)
    cols = len(data.initMap[0])
    cellSize = 50
    lst = []    
    for row in range(rows):
        for col in range(cols):
            cx = col * cellSize + cellSize / 2
            cy = row * cellSize + cellSize / 2
            if data.initMap[row][col] == 1:
                lst.append((row, col))
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

# add monster1(shooting blue monster)
def shootingMonsterPos(data):
    road = roadPosition(data)
    numOfMonster = 15
    data.newMap1 = copy.deepcopy(data.initMap)
    for i in range(numOfMonster):
        monsterPos = random.choice(road)
        row = monsterPos[0]
        col = monsterPos[1]
        if data.newMap1[row][col] != 6:
            data.newMap1[row][col] = 6
    return data.newMap1

# add monster2(green monster)
def monsterPos(data):
    road = roadPosition(data)
    numOfMonster = 15
    data.newMap2 = copy.deepcopy(data.newMap1)
    for i in range(numOfMonster):
        monsterPos = random.choice(road)
        row = monsterPos[0]
        col = monsterPos[1]
        if data.newMap2[row][col] != 7:
            data.newMap2[row][col] = 7
    return data.newMap2

    

#############################################

# controller

#############################################
    

def distance(cx, cy, x, y):
    distance = ((x - cx)  ** 2 + (y - cy) ** 2) ** 0.5
    r = 20
    return distance <= r

def mousePressed(event, data):
    # start game
    pos3 = (800, 450)
    if distance(pos3[0], pos3[1], event.x, event.y):
        data.startGame = True

def keyPressed(event, data):
    if event.keysym == "Up":
        data.explorer.move(-1, 0)
        data.explorer.rotate(90)
        if isWall(data):
            data.explorer.move(1, 0)
            data.initMap[data.position[0]][data.position[1]] = 1
    elif event.keysym == "Down":
        data.explorer.move(1, 0)
        data.explorer.rotate(270)
        if isWall(data):
            data.explorer.move(-1, 0)
            data.initMap[data.position[0]][data.position[1]] = 1
    elif event.keysym == "Right":
        data.explorer.move(0, 1)
        data.explorer.rotate(0)
        if isWall(data):
            data.explorer.move(0, -1)
            data.initMap[data.position[0]][data.position[1]] = 1
    elif event.keysym == "Left":
        data.explorer.move(0, -1)
        data.explorer.rotate(180)
        if isWall(data):
            data.explorer.move(0, 1)
            data.initMap[data.position[0]][data.position[1]] = 1 
    elif event.keysym == "space":
        if data.numOfBullets > 0:
            data.bullets.append(data.explorer.makeBullet())
            data.numOfBullets -= 1
 
    
def timerFired(data):
    data.counter += 1
    '''
    print(data.monster1)
    for monster in data.monsterPos1:
        monster.moveMonster()
    '''
        
    for bullet in data.bullets:
        # move bullets
        bullet.moveBullet()
    
    for monster in data.monsters:
        for wall in data.wallPos:
            monster.moveMonster()
            data.monsterBullets.append(monster.makeBullet())
            monster.reactToWall(wall)
            #pass
        
    #generateMonster(data)
    removeBullet(data)
    removeBulletAndMonster(data)

def removeBullet(data):
    for bullet in data.bullets:
        for wall in data.wallPos:
            if bullet.collidesWithWall(wall):
                data.bullets.remove(bullet)  

def removeBulletAndMonster(data):
    for bullet in data.bullets:
        for monster in data.monsters:
            if bullet.collide(monster):
                data.bullets.remove(bullet)
                data.monsters.remove(monster)
    
    for bullet in data.monsterBullets:
        if bullet.collide(Explorer):
            data.monsterBullets.remove(bullet)
            data.numOfHearts -= 1

         

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
    

####################################    

# draw tools bar

####################################

def drawToolsBar(data, canvas):
    
    # draw levels
    cx1 = 55
    cy1 = 530
    cx2 = 55
    cy2 = 570
    canvas.create_text(cx1, cy1, text = "LEVEL", fill = "white", font = ('Helvetica', '20'))
    canvas.create_text(cx2, cy2, text = str(data.level), fill = "white", font = ('Helvetica', '25'))
    
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

##########################

# draw explorer, walls and roads

##########################

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
                canvas.create_image(x0, y0, image = data.road2, anchor= 'center')
            elif data.initMap[row][col] == 3:
                canvas.create_image(x0, y0, image = data.road3, anchor= 'center')
            elif data.initMap[row][col] == 4:
                canvas.create_image(x0, y0, image = data.road4, anchor= 'center')
            elif data.initMap[row][col] == 5:
                canvas.create_image(x0, y0, image = data.road5, anchor= 'center')
            elif data.initMap[row][col] == 6:
                # shooting blue monster
                canvas.create_image(x0, y0, image = data.monster1, anchor= 'center')
            elif data.initMap[row][col] == 7:
                # non-shooting green monster
                canvas.create_image(x0, y0, image = data.monster2, anchor= 'center')

                    
def refreshMap(data):
    if data.position != []:
        row = data.position[0]
        col = data.position[1]
        # walls and doors cannot be opened
        if data.initMap[row][col] != 1 and data.initMap[row][col] != 0:
            data.initMap[row][col] = -1 
            direction = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
            if data.newMap1[row][col] == 6: # map of shooting blue monster
                data.monsters.append(ShootingMonster(row, col, direction))
                data.newMap1[row][col] = -1
            elif data.newMap2[row][col] == 7: # map of green monster
                data.monsters.append(Monster(row, col, direction))
                data.newMap2[row][col] = -1
    
    
def redrawAll(canvas, data):
    if not data.startGame:
        gameStarted(data, canvas)            
    else:
        drawMap(data, canvas)
        drawToolsBar(data, canvas)
        refreshMap(data)
        for bullet in data.bullets:
            bullet.draw(canvas)
        for monster in data.monsters:
            monster.draw(canvas)
        data.explorer.draw(canvas)
        


####################################
# use the run function as-is
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
    print("bye!")

run(1000, 600)
