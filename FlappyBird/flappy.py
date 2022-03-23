
from os import kill
from sys import flags
import pygame
import time
import random
from pygame import fastevent


from pygame.transform import scale

pygame.init()


display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)



gameDisplay = pygame.display.set_mode((display_width,display_height))
bg = pygame.image.load('flappybg.png').convert_alpha()
bg = pygame.transform.scale(bg, (display_width, display_height))
pygame.display.set_caption('flappy')
clock = pygame.time.Clock()

def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center = rect.center)
    return rot_image, rot_rect

class pipe (pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.scale = 0.35
        self.gap = -1 * 800

        self.flag = False
        self.speed = 150/60
        self.x = display_width + 50
        rand = random.randrange(370-110,371+110) # random height
        self.y = display_height/2 + rand
        self.a = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.a, 0, self.scale)
        self.rect = self.image.get_rect(center = (self.x, self.y))

        # UPPER PIPE
        self.upper_pipe = pipeUP()
        self.upper_pipe.rect.y = self.rect.y + self.gap
    
    def move(self):
        self.rect.x -= self.speed # move lower pipe left
        self.upper_pipe.rect.x -= self.speed # move upper pipe left
        if (self.rect.x < -100):
            self.upper_pipe.kill()
            self.kill()
        

            
        
        
class pipeUP (pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.scale = 0.35
        self.speed = 100/60
        self.x = display_width + 50
        self.y = display_height/2 + 320
        self.a = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.a, 180, self.scale)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask  = pygame.mask.from_surface( self.image )
    
    # def check(self):
    #     if (self.rect.x < -100):
    #         self.kill()
    

        
        
class Box(pygame.sprite.Sprite): #sprite for the floor
    
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((display_width,1))
        self.rect = self.image.get_rect(center = (display_width/2, 0))
        self.image.fill(black)
        

class Flappy(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.gravity = 1
        self.scale = 0.15
        self.flag = True
        self.angle = 0
        self.rot = -.3 * 0
        self.speed = 0
        self.x = 100
        self.y = display_height/2
        self.a = pygame.image.load('flappy.png').convert_alpha()
        # self.image = pygame.transform.scale(a, (scale, scale))
        self.image = pygame.transform.rotozoom(self.a, self.angle, self.scale)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask  = pygame.mask.from_surface( self.image )
        
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.speed = -12
            
            
    def apply_gravity(self):
        self.speed += self.gravity
        self.rect.y += self.speed
        self.angle += self.rot
        self.image, self.rect = rot_center(self.image, self.rect, self.angle)

        # self.image = pygame.transform.rotozoom(self.a, self.angle, self.scale)

        
    def update(self):
        self.apply_gravity()
        self.player_input()
        # self.angle += 3.3
        
    
        

def start_screen():
    gameDisplay.blit(bg,(0,0))
    birdy = Flappy()
    player = pygame.sprite.GroupSingle()
    player.add(birdy)
    birdy.rect.y = display_height/2
    player.draw(gameDisplay)
    pygame.display.update()
    loop = True
    while loop:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e or event.key == pygame.K_UP:
                    # loop = False
                    return
    
    
def game_loop():
    
    score = 0
    pixelfont = pygame.font.Font('Pixeltype.ttf', 75)
        
    
    # HAPPENS ONCE
    bird = Flappy()

    player = pygame.sprite.GroupSingle()
    pipes = pygame.sprite.Group()
    
    boxup = Box()
    boxdown = Box()
    boxdown.rect.y = display_height
    pipes.add(boxup)
    pipes.add(boxdown)
    

    pipe_list = []
    
    
    
    player.add(bird)
    player.draw(gameDisplay)

    pipes.draw(gameDisplay)
    pipe_timer = 0
    while True:

        pipe_timer += 1
        if pipe_timer % 90 == 0: # add pipe every second
            pipe_list.append(pipe())
            pipes.add(pipe_list[-1])
            pipes.add(pipe_list[-1].upper_pipe)
            if pipe_timer > 360: # remove pipes per second after 6 seconds
                pipe_list.pop(0)
        for pipess in pipe_list:
            pipess.move()
            if not pipess.flag and pipess.rect.x < 100:
                pipess.flag = True
                score += 1
            
        
        if (pygame.sprite.spritecollide(bird, pipes, False, collided=pygame.sprite.collide_mask)):
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        bird.update()
        
        # if -60<bird.rect.y<display_height-60:
        #     bird.update()
        # else: return
        
        # pipe1.move()
        # new_pipe.move()
        # pipe1.upper_pipe.check()
        
        score_surface = pixelfont.render(str(score), False, white)
        gameDisplay.blit(bg,(0,0))
        player.draw(gameDisplay)
        pipes.draw(gameDisplay)
        
        gameDisplay.blit(score_surface, (display_width/2, 50))

        pygame.display.update()
        clock.tick(60)

# runtime
while True:
    start_screen()
    game_loop()
pygame.quit()
quit()