# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 05:35:58 2021

@author: Tushar Anand
"""

import pygame,sys,random

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,path,xpos,ypos):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load('spaceship_charged.png')
        self.image = self.uncharged
        self.rect = self.image.get_rect(center = (xpos,ypos))
        self.shield_surface = pygame.image.load('shield.png')
        self.health = 5
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.constraints()
        self.display()
    
    
    def constraints(self):
        if self.rect.topright[0] >= 1280 and self.rect.topright[1]<=0:
            self.rect.topright = (1280,0)
        elif self.rect.topleft[0] <= 0 and self.rect.topleft[1] <=0:
            self.rect.topleft = (0,0)
        elif self.rect.bottomright[0] >= 1280 and self.rect.bottomright[1] >720:
            self.rect.bottomright = (1280,720)
        elif self.rect.bottomleft[0] <=0 and self.rect.bottomleft[1] > 720:
            self.rect.bottomleft = (0,720)
        elif self.rect.right >= 1280:
            self.rect.right = 1280
        elif self.rect.left <= 0:
           self.rect.left = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 720:
            self.rect.bottom = 720
       
    def display(self):
        for i in range(0,self.health):
            screen.blit(self.shield_surface,(10+40*i,10))
            
    def get_damage(self,damage):
        self.health -=damage
    
    def charge(self):
        self.image = self.charged
    def uncharge(self):
        self.image = self.uncharged
        
     

class Meteor(pygame.sprite.Sprite):
    def __init__(self,path,xpos,ypos,xspeed,yspeed):
        super().__init__()
        self.image= pygame.image.load(path)
        self.rect = self.image.get_rect(center= (xpos,ypos))
        self.xspeed = xspeed
        self.yspeed = yspeed
    def update(self):
        self.rect.centerx += self.xspeed
        self.rect.centery += self.yspeed
        if self.rect.centery>750:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self,path,pos,speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= -20:
            self.kill()



        
def main_game():
    global laser_active
    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteor_group.draw(screen)
    laser_group.update()
    spaceship_group.update()
    meteor_group.update()
    
    if pygame.sprite.spritecollide(spaceship_group.sprite,meteor_group,True):
        spaceship_group.sprite.get_damage(1)
    for i in laser_group:
        
        pygame.sprite.spritecollide(i,meteor_group,True)
       

    
    if pygame.time.get_ticks() - laser_time >= 500:
        laser_active= True
        spaceship_group.sprite.charge()
        
    return 1

def game_over():
    space_bg(0)
    font_surface = font_text.render('GAME OVER',True,(255,255,255)) 
    font_rect = font_surface.get_rect(center = (640,300))
    screen.blit(font_surface,font_rect)
    
    score_surface = font_text.render(f'SCORE : {score}',True,(255,255,255)) 
    score_rect = score_surface.get_rect(center = (640,360))
    screen.blit(score_surface,score_rect)
    
    hscore_surface = font_text.render(f'HIGHSCORE : {hs}',True,(255,255,255)) 
    hscore_rect = hscore_surface.get_rect(center = (640,390))
    screen.blit(hscore_surface,hscore_rect)

def space_bg(bg_ypos):
    screen.blit(bg,(0,bg_ypos))   
    screen.blit(bg,(0,bg_ypos-720))   
    
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
score = 0
hs=0
laser_time = 0 
laser_active = True

#font 
font_text = pygame.font.Font('btseps2.ttf',40)

#spaceship
spaceship= SpaceShip('spaceship.png',640,600)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

#meteor group
meteor_group= pygame.sprite.Group()
meteor_event = pygame.USEREVENT
pygame.time.set_timer(meteor_event,300)

#laser group
laser_group = pygame.sprite.Group()

#background
bg= pygame.image.load('back.png').convert()
bg_ypos = 0

#music
music1 = pygame.mixer.music.load('space laser.mp3')
pygame.mixer.music.set_volume(0.01)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            laser_active= False
            laser = Laser('Laser.png',spaceship.rect.center,12)
            laser_group.add(laser)
            laser_time = pygame.time.get_ticks()
            spaceship_group.sprite.uncharge()
            pygame.mixer.music.play()
            
        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health<=0:
            score = 0
            spaceship_group.sprite.health = 5
            meteor_group.empty()
        if event.type == meteor_event:
            meteor_path = random.choice(('Meteor1.png','Meteor2.png','Meteor3.png'))
            xpos= random.randrange(0,1280)
            ypos = random.randrange(-500,-50)
            xspeed= random.randrange(-2,2)
            yspeed = random.randrange(6,8)
            meteor=Meteor(meteor_path,xpos,ypos,xspeed,yspeed)
            meteor_group.add(meteor)
    bg_ypos+=1
    space_bg(bg_ypos)
    if bg_ypos > 720:
        bg_ypos = 0
    
    
    if spaceship_group.sprite.health > 0:
        score +=main_game()
        if score>hs:
            hs=score
    else:
        game_over()
         
        
    pygame.display.update()
    clock.tick(120)
            