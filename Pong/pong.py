from math import sqrt
import pygame
import random
import time

from pygame import draw
from pygame.display import update


pygame.init()

display_width = 1000
display_height = 600
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

ball_radius = 15
netvel = 10

width = 10
height = 100

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pong')
    
def drawball(x,y):
    pygame.draw.circle(gameDisplay, red,(x,y), ball_radius)
    
def drawleft(x,y):
    pygame.draw.rect(gameDisplay, white,(x,y,width, height))
    
def drawright(x,y):
    pygame.draw.rect(gameDisplay, white,(x,y,width, height))
    
def pause_loop():
    pass

# puts a text at x,y on surface
def texter(text, font, x,y, surface, size):
    font0 = pygame.font.Font(font, size)
    surf = pygame.font.Font.render(font0, text, True, white)
    a = surf.get_rect(center = (x,y))
    # surface.blit(surf,surf.get_rect())
    surface.blit(surf,a)
    
    

def gameloop():
    
    killgame = False 
    
    ttf = 'freesansbold.ttf'
    
    lpoint = 0
    rpoint = 0
    
    ballx = display_width/2
    bally = display_height/2
    
    speed = 0
    speedr = 0
    
    xvel = 0
    yvel = 0
    
    lefty=400
    righty=400
    
    
    # initial drawings
    
    gameDisplay.fill(black)
    drawball(400,400)
    drawleft(0,height)
    drawright(display_width-width,height)
    
    
    pygame.display.update()
    
    def pythag(a,c):
        return sqrt(c*c-a*a)
    
    
        


    while (not killgame):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    xvel = 3*(-1+2*random.randint(0,1))
                    yvel = random.randint(-7,7)
                    
                if event.key == pygame.K_w:
                    speed = -5
                if event.key == pygame.K_s:
                    speed = 5
                if event.key == pygame.K_UP:
                    speedr = -5
                if event.key == pygame.K_DOWN:
                    speedr = 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    speed = 0
                if event.key == pygame.K_s:
                    speed = 0
                if event.key == pygame.K_UP:
                    speedr= 0
                if event.key == pygame.K_DOWN:
                    speedr = 0
        if ballx<=width+ball_radius and lefty+ball_radius<=bally<=lefty+height-ball_radius:
            xvel*=-1.0
        if ballx>=display_width-ball_radius and righty+ball_radius<=bally<=righty+height-ball_radius:
            xvel*=-1.0
            
        if bally<=0+ball_radius or bally >= display_height-ball_radius:
            yvel*= -1.0
            
        if ballx>display_width:
            # time.sleep(2)
            lpoint+=1
            ballx = display_width/2
            bally = display_height/2
            xvel = 0
            yvel = 0
            
        if ballx<0:
            # time.sleep(2)
            rpoint+=1
            ballx = display_width/2
            bally = display_height/2
            xvel = 0
            yvel = 0
        
            
                        
            
                    
                
                    
                
        ballx += xvel
        bally += yvel
        lefty += speed
        righty += speedr
        
        gameDisplay.fill(black)
        drawleft(0,lefty)
        drawright(display_width-width,righty)
        drawball(ballx,bally)
        
        texter(str(rpoint), ttf, 510,580, gameDisplay, 20)
        texter(str(lpoint), ttf, 490,580, gameDisplay, 20)

        pygame.display.update()
        clock.tick(60)
             
    
gameloop()
pygame.quit()
quit()

                
    
