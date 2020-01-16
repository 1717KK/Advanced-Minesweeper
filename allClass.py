from tkinter import *
import random
from PIL import Image, ImageTk
import math
import copy


#############################################
# loading images
#############################################

def imageShootingMonster():
    imageSize = (50, 50)
    shootingMonsterImage = Image.open("monster1.gif")
    shootingMonsterPic = shootingMonsterImage.resize(imageSize, Image.ANTIALIAS)
    shootingMonster = ImageTk.PhotoImage(shootingMonsterPic)
    return shootingMonster
    
def imageMonster():
    imageSize = (50, 50)
    monsterImage = Image.open("monster2.gif")
    monsterPicture = monsterImage.resize(imageSize,Image.ANTIALIAS)
    monster = ImageTk.PhotoImage(monsterPicture)
    return monster
    
def imageBullet():
    imageSize = (150, 150)
    bulletImage = Image.open("bullet.gif")
    bulletPicture = bulletImage.resize(imageSize,Image.ANTIALIAS)
    bullet = ImageTk.PhotoImage(bulletPicture)
    return bullet  

##############################################
# Monster
##############################################
    
class Monster(object):
    def __init__(self, row, col, direction):
        # A monster has a position, speed, and direction
        self.row = row
        self.col = col
        self.direction = direction
        self.image = None
        self.cellSize = 50
        self.cx = self.col * self.cellSize + self.cellSize / 2
        self.cy = self.row * self.cellSize + self.cellSize / 2
        self.speed = 5
    
        
    # View
    def draw(self, canvas):
        self.image = imageMonster()
        canvas.create_image(self.cx, self.cy, image = self.image, \
                            anchor= 'center')
    
    def moveMonster(self):
        self.cx += self.speed * self.direction[0]
        self.cy += self.speed * self.direction[1]
       
    
    # If the monster reach the edge of the wall and screen, they bounce  
    def reactToWall(self, wall):
        cellSize = 50
        
        maxX = 1000
        maxY = 500
        if self.cx - cellSize / 2 <= 0 or self.cx + cellSize / 2 >= maxX:
            self.direction[0] = - self.direction[0]  
        elif self.cy - cellSize / 2 <= 0 or self.cy + cellSize / 2 >= maxY:
            self.direction[1] = - self.direction[1]
            
        for w in wall:
            if (abs(w[0] - self.cx) < cellSize and \
                abs(w[1] - self.cy) < cellSize):
                self.direction[0] = - self.direction[0]
                self.direction[1] = - self.direction[1]


           
class ShootingMonster(Monster):
    def _init_(self, row, col, direction):
        super().__init__(self, row, col, direction)

    def draw(self, canvas):
        self.image = imageShootingMonster()
        canvas.create_image(self.cx, self.cy, image = self.image, \
                            anchor= 'center')
    
    def makeBullet(self):
        if self.direction == [1, 0]:
            angle = 0
        elif self.direction == [-1, 0]:
            angle = 180
        elif self.direction == [0, -1]:
            angle = 90
        elif self.direction == [0, 1]:
            angle = 270
        speed = 20
        
        return MonsterBullet(self.cx, self.cy, angle, speed)

##############################################
# Explorer
##############################################
    
class Explorer(object):
    def __init__(self, row, col, image):
        self.row = row 
        self.col = col
        self.image = image
        self.cellSize = 50
        self.angle = 0
        self.cx = 0
        self.cy = 0
        
    
    def draw(self, canvas):
        x0 = self.col * self.cellSize + self.cellSize / 2
        y0 = self.row * self.cellSize + self.cellSize / 2
        self.cx = x0
        self.cy = y0
        canvas.create_image(x0, y0, image = self.image, anchor= 'center')
        
    def move(self, drow, dcol):
        maxRow = 10
        maxCol = 19
        if 0 <= self.row <= maxRow and 0 <= self.col <= maxCol:
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
            
    def collide(self, other):
        if(not isinstance(other, Monster)) : # Other must be a Monster
            return False
        else:
            if other.cx == self.cx and other.cy == self.cy:
                return True


##############################################
# Bullet
##############################################
    
        
class Bullet(object):
    # Model
    def __init__(self, cx, cy, angle, speed):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.angle = angle
        self.speed = speed 
        self.image = imageBullet()
        self.num = 100
    
    # View
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image = self.image, \
                            anchor= 'center')

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
        

    def isOffScreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        if (self.cx <= 0 or self.cx >= width) or \
            (self.cy <= 0 or self.cy >= height):
            return True
               
    
class MonsterBullet(Bullet):
    def __init__(self, cx, cy, angle, speed):
        super().__init__(cx, cy, angle, speed)
    
    def draw(self, canvas):
        r = 3
        canvas.create_oval(self.cx - r, self.cy - r, \
                           self.cx + r, self.cy + r, \
                           fill = "white", width = 0)
                           
    def collide(self, other):
        cellSize = 50
        if(not isinstance(other, Explorer)) : # Other must be an Explorer
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            if dist < cellSize / 2:
                return True
                
    def isOffScreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        r = 3
        if (self.cx + r <= 0 or self.cx - r >= width) or\
           (self.cy + r <= 0 or self.cy - r >= height - 20):
               return True