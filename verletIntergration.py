#Verlet Intergration Simulation
#Made by HaydenD100 
#GitHub: https://github.com/HaydenD100
#This is a vertlet intergraction particle simulation. Use the hotbar at the top too place and connect points. Using right click you can constrain points.
#You can stop and start the simulation at anytime. The simulation is set to run at 80 updates a second, Fps is displayed at the title of the window.
#v1.0.1 
#Added box coliders that the particles can interact with

import pygame
import time
import math


#Screen resoultion
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#box colider class
class Box:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

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
            
        
        for box in boxes:
            #top
            if(point.x > box.x and point.x < box.x + box.width and point.y + 9 > box.y and point.y < box.y and point.y + 9 < box.y + box.height):
                point.y = box.y - 9
                point.oldY = point.y + vy * bounce
            #bottom   
            elif(point.x > box.x and point.x < box.x + box.width and point.y - 9 < box.y + box.height and point.y > box.y + box.height and point.y  + 9 > box.y):
                point.y = box.y + box.height + 9
                point.oldY = point.y + vy * bounce
            #left   
            if(point.x + 9 > box.x and point.x + 9 < box.x + box.height and point.y < box.y + box.height and point.y > box.y):
                point.x = box.x - 9
                point.oldX = point.x + vx * bounce
            #right    
            elif(point.x - 9 < box.x + box.height and point.x > box.x + box.height and point.y < box.y + box.height and point.y > box.y):
                point.x = box.x + box.height + 9
                point.oldX = point.x + vx * bounce
            
        
        
            

 
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

def ChangeButton(state):
    place = False
    connect = False
    remove = False
    selectBox = False
    addBox = False
    
    for i in range(len(buttons)):
        if(i == state):
            continue
        buttons[i].value = False
    
    

    if(state == 1):
        place = True
    if(state == 2):
        connect = True
    if(state == 3):
        remove = True
    if(state == 4):
        selectBox = True
    if(state == 5):
        addBox = True    
    
    
    
  
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
        
    for box in boxes:
        pygame.draw.rect(screen,(255,255,255),(box.x,box.y,box.width,box.height),100)
            
    for button in buttons:
        if(button.value == True):
            pygame.draw.circle(screen,(0,255,0),(button.x,button.y),button.radius,button.radius)  
        else:
            pygame.draw.circle(screen,(255,0,0),(button.x,button.y),button.radius,button.radius)  
    if(boxCorner1 != 0 and addBox == True):
        pygame.draw.circle(screen,(00,255,0),(boxCorner1[0],boxCorner1[1]),3,3) 
    screen.blit(StopStart, (25,0))
    screen.blit(PlacePoint, (175,0))
    screen.blit(ConnectPoints,(275,0))
    screen.blit(RemovePoints,(390,0))
    #screen.blit(RightClickText,(490,0))
    screen.blit(AddBox,(504,0))
    screen.blit(SelectBox,(585,0))

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
buttons.append(Button(490,10,10,False)) #Add Box
buttons.append(Button(570,10,10,False)) #Select Box

boxes = []



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
AddBox = my_font.render('Add Box', False, (255, 255, 255))
SelectBox = my_font.render('Select Box', False, (255, 255, 255))



screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#the diffrent states 
running = True
simulate = False
place = True
connect = False
remove = False
selectBox = False
addBox = False

#for tracking fps
start_time = time.time()
FPSCounter = 0
seconds = 0

SelectedPoint1 = 0
SelectedPoint2 = 0

boxCorner1 = 0
boxCorner2 = 0




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
                
                for button in buttons:
                    if(button.CheckIfClicked(pos[0],pos[1])):
                        if(button.value == True):
                            button.value = False
                        else:
                            button.value = True
                
                if(buttons[0].CheckIfClicked(pos[0],pos[1])):
                    simulate = buttons[0].value
                if(buttons[1].CheckIfClicked(pos[0],pos[1])):
                    connect = False
                    place = True
                    addBox = False
                    selectBox = False
                    buttons[4].value = False
                    buttons[5].value = False
                    buttons[2].value = False
                    buttons[3].value = False
                    remove = False
                            
                if(buttons[2].CheckIfClicked(pos[0],pos[1])):
                            place = False 
                            connect = True
                            addBox = False
                            selectBox = False
                            buttons[4].value = False
                            buttons[5].value = False
                            buttons[1].value = False
                            buttons[3].value = False
                            
                            remove = False
                elif(buttons[3].CheckIfClicked(pos[0],pos[1])):
                            place = False
                            connect = False
                            remove = True
                            addBox = False
                            selectBox = False
                            buttons[4].value = False
                            buttons[5].value = False
                            buttons[1].value = False
                            buttons[2].value = False
                            
                elif(buttons[4].CheckIfClicked(pos[0],pos[1])):
                            place = False
                            connect = False
                            remove = False
                            selectBox = False
                            addBox = True
                            buttons[3].value = False
                            buttons[5].value = False
                            buttons[1].value = False
                            buttons[2].value = False
                elif(buttons[5].CheckIfClicked(pos[0],pos[1])):
                            place = False
                            connect = False
                            remove = False
                            addBox = False
                            selectBox = True
                            addBox = False
                            buttons[3].value = False
                            buttons[4].value = False
                            buttons[1].value = False
                            buttons[2].value = False
                
                              
                elif(event.button == 1 and place == True):
                    points.append(Point(pos[0],pos[1],pos[0] - 0.1, pos[1] - 0.1))
                
                elif(event.button == 1 and remove == True):
                    for point in points:
                            if(math.dist([point.x,point.y],[pos[0],pos[1]]) <= 9):
                                    points.remove(point)
                                    for stick in sticks:
                                        if(points.count(stick.p1) <= 0 or points.count(stick.p2) <= 0 ):
                                            sticks.remove(stick)
                                    for stick in sticks:
                                        if(points.count(stick.p1) <= 0 or points.count(stick.p2) <= 0 ):
                                            sticks.remove(stick)
                                    
                elif(event.button == 1 and connect == True):
                        for point in points:
                            if(math.dist([point.x,point.y],[pos[0],pos[1]]) <= 9):
                                if(SelectedPoint1 == 0):
                                    SelectedPoint1 = point
                                    break
                                
                                elif(SelectedPoint2 == 0 and point != SelectedPoint1):
                                    SelectedPoint2 = point
                                
                                if(SelectedPoint1 != 0 and SelectedPoint2 != 0):
                                    sticks.append(Stick(SelectedPoint1,SelectedPoint2,distance(SelectedPoint1,SelectedPoint2)))
                                    SelectedPoint1 = 0
                                    SelectedPoint2 = 0
                                    
                elif(event.button == 1 and addBox == True):
                    
                    if(boxCorner1 == 0):
                        boxCorner1 = pos
                        
                    else:
                        boxCorner2 = pos
                        width = abs(boxCorner2[0] - boxCorner1[0])
                        height = abs(boxCorner2[1] - boxCorner1[1])
                        boxes.append(Box(boxCorner1[0],boxCorner1[1],width,height))
                        boxCorner1 = 0
                        boxCorner2 = 0
                
                elif(event.button == 1 and selectBox == True):
                    for box in boxes:
                        if(pos[0] > box.x and pos[0] < box.x + box.width and pos[1] > box.y and pos[1] < box.y + box.height):
                            boxes.remove(box)
                                           
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
    
    
    
    

