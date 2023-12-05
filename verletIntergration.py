#Verlet Intergration Simulation
#Made by HaydenD100 
#GitHub: https://github.com/HaydenD100
#This is a vertlet intergraction particle simulation. Use the hotbar at the top too place and connect points. Using right click you can constrain points.
#You can stop and start the simulation at anytime. The simulation is set to run at 80 updates a second, Fps is displayed at the title of the window.

import pygame
import time
import math


#Screen resoultion
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


#Ui Button with function for checking if the button has been clicked by seeing if the mouse button is within the radius of the button
class Button:
    def __init__(self,x,y,radius,StartingValue):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = StartingValue
    
    def CheckIfClicked(self,x,y):
        if(math.dist([x,y],[self.x,self.y]) <= self.radius):
            return True
        else:
            return False

#point class which stores current x and y value and precious x and y value. Velocity is calculated by subtracting old position form new position
class Point:
    
    def __init__(self,PosX,PosY,pX,pY):
        self.moveAble = True
        self.x = PosX
        self.y = PosY
        self.oldX = pX
        self.oldY = pY

#Stick class stores the two points its connect by and the lenght between them
class Stick:
    def __init__(self,p1,p2,lenght):
        self.p1 = p1
        self.p2 = p2
        self.lenght = lenght
     
#updates all the points and applies Gravity bounce if the point has hit the sides or bottom of the screen and friction   
def UpdatePoints():
    for point in points:
        if(point.moveAble == False):
            continue
        
        vx = (point.x - point.oldX) * friction
        vy = (point.y - point.oldY) * friction
        
        point.oldX = point.x
        point.oldY = point.y
        
        point.x += vx
        point.y += vy
        point.y += gravity
        
        

#Constrains any points that need too be contrainted by setting new postion of a point too the old postion as well as making sure points dont go outside the screen
def ConstrainPoints():
    for point in points:
        if(point.moveAble == False):
            point.x = point.oldX
            point.y = point.oldY
            continue
        
        vx = (point.x - point.oldX) * friction
        vy = (point.y - point.oldY) * friction
        
        
        #checks if the points are outside the screen boundary
        if(point.x > SCREEN_WIDTH):
            point.x = SCREEN_WIDTH
            point.oldX = point.x + vx * bounce
            
        elif(point.x < 0):
            point.x = 0
            point.oldX = point.x + vx * bounce
            
        if(point.y > SCREEN_HEIGHT):
            point.y = SCREEN_HEIGHT
            point.oldY = point.y + vy * bounce
            
        elif(point.y < 0):
            point.y = 0
            point.oldY = point.y + vy * bounce
 
#This function takes a list of stick objects and loops through them updating all the sticks and their connected points           
def UpdateSticks():
    for stick in sticks:
        dx = stick.p2.x - stick.p1.x
        dy = stick.p2.y - stick.p1.y
        distance = math.sqrt(dx * dx + dy * dy)
        diffrence = stick.lenght - distance
        precent = diffrence / distance / 2
        offSetX = dx * precent
        offSetY = dy * precent
        
        stick.p1.x -= offSetX
        stick.p1.y -= offSetY
        
        stick.p2.x += offSetX
        stick.p2.y +=offSetY
            
#returns the distance between two points
def distance(point1, point2): 
    return math.dist([point1.x,point1.y],[point2.x,point2.y])
  
#This function renders the sticks,the points and the ui elements
def Draw():
    screen.fill((0, 0, 0))
    
    for point in points:
        if(point.moveAble == False):
            pygame.draw.circle(screen,(255,0,0),(point.x,point.y),9,9)  
        elif(point == SelectedPoint1 or point == SelectedPoint2):
            pygame.draw.circle(screen,(0,255,0),(point.x,point.y),9,9)  
        else:
            pygame.draw.circle(screen,(255,255,255),(point.x,point.y),9,9)  
    for stick in sticks:
        pygame.draw.line(screen,(255,255,255),(stick.p1.x,stick.p1.y),(stick.p2.x,stick.p2.y),2)
            
    for button in buttons:
        if(button.value == True):
            pygame.draw.circle(screen,(0,255,0),(button.x,button.y),button.radius,button.radius)  
        else:
            pygame.draw.circle(screen,(255,0,0),(button.x,button.y),button.radius,button.radius)  
        
    screen.blit(StopStart, (25,0))
    screen.blit(PlacePoint, (175,0))
    screen.blit(ConnectPoints,(275,0))
    screen.blit(RemovePoints,(390,0))
    screen.blit(RightClickText,(490,0))

    pygame.display.update()

#points list
points = []

#sticks list
sticks = []

#buttons lists
buttons = []
buttons.append(Button(10,10,10,False))
buttons.append(Button(160,10,10,True))
buttons.append(Button(260,10,10,False))
buttons.append(Button(375,10,10,False))



#forces
bounce = 0.9
gravity = 0.1
friction = 0.999
    

pygame.init()   
pygame.font.init()
pygame.display.init()

#Text
my_font = pygame.font.SysFont('Arial', 15)
StopStart = my_font.render('Start/Stop Simulation', False, (255, 255, 255))
PlacePoint = my_font.render('Place Point', False, (255, 255, 255))
ConnectPoints = my_font.render('Connect Points', False, (255, 255, 255))
RemovePoints = my_font.render('Remove Points', False, (255, 255, 255))
RightClickText = my_font.render('Right Click On Point To Constrain Point', False, (255, 255, 255))



screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#the diffrent states 
running = True
simulate = False
place = True
connect = False
remove = False

#for tracking fps
start_time = time.time()
FPSCounter = 0
seconds = 0

SelectedPoint1 = 0
SelectedPoint2 = 0




LastTIme = time.time()

#this sets the fps the simulation will try too run at
FPS = 80


while running:
    currentTime = time.time()
    if(currentTime <= LastTIme + 1/80):
        continue
    LastTIme = currentTime
    

    
        
    
    #used for debuggin and FPS checking
    FPSCounter = FPSCounter + 1
    current_time = time.time()
    if current_time - start_time >= seconds:
        seconds = seconds +1
        pygame.display.set_caption("FPS:" + str(FPSCounter))
        FPSCounter = 0
        
    
        
    #Diffrent input events
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if(buttons[2].CheckIfClicked(pos[0],pos[1])):
                            place = False 
                            connect = True
                            buttons[1].value = False
                            buttons[3].value = False
                            remove = False
                if(buttons[3].CheckIfClicked(pos[0],pos[1])):
                            place = False
                            connect = False
                            remove = True
                            buttons[1].value = False
                            buttons[2].value = False
                              
                if(event.button == 1 and place == True):
                    points.append(Point(pos[0],pos[1],pos[0] - 0.1, pos[1] - 0.1))
                
                if(event.button == 1 and remove == True):
                    for point in points:
                            if(math.dist([point.x,point.y],[pos[0],pos[1]]) <= 9):
                                    points.remove(point)
                                    for stick in sticks:
                                        if(stick.p1 == point or stick.p2 == point):
                                            sticks.remove(stick)
                                    
                if(event.button == 1 and connect == True):
                        for point in points:
                            if(math.dist([point.x,point.y],[pos[0],pos[1]]) <= 9):
                                if(SelectedPoint1 == 0):
                                    SelectedPoint1 = point
                                elif(SelectedPoint2 == 0 and point != SelectedPoint1):
                                    SelectedPoint2 = point
                                
                                if(SelectedPoint1 != 0 and SelectedPoint2 != 0):
                                    sticks.append(Stick(SelectedPoint1,SelectedPoint2,distance(SelectedPoint1,SelectedPoint2)))
                                    SelectedPoint1 = 0
                                    SelectedPoint2 = 0
                                    
                                
                                    
                                    
                                    
                for button in buttons:
                    if(button.CheckIfClicked(pos[0],pos[1])):
                        if(button.value == True):
                            button.value = False
                        else:
                            button.value = True
                            
                        if(button == buttons[0]):
                            simulate = button.value
                        if(button == buttons[1]):
                            place = True
                            buttons[2].value = False
                            buttons[3].value = False
                            remove = False

                        
  
                        
                    
                if(event.button == 3):
                    for point in points:
                        if(math.dist([point.x,point.y],[pos[0],pos[1]]) <= 7):
                            if(point.moveAble == False):
                                point.moveAble = True
                            else:
                                point.moveAble = False
                                
                
                
                            
                            
    #will only updates the points/sticks if simulate is true        
    if(simulate):                       
        UpdatePoints()
        for i in range(5):
            UpdateSticks()  
            ConstrainPoints()   
     
    
    Draw()
    
    
    
    

