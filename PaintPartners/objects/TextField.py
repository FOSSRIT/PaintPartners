import pygame
from pygame.locals import *

class TextField(pygame.sprite.Sprite):
    def __init__(self,pos,maxChars,fontSize,buttonName,font,password=False):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.selected = False
        self.blink = False
        self.password = password
        self.timer = 0
        self.name = buttonName

        self.text_color = (0,0,0)

        self.maxChars = maxChars
        self.message = ""
        temp_message = ""
        for i in range(maxChars):
            temp_message += "X"
        
        self.font = font
        self.text = self.font.render(self.message, 1,self.text_color)
        self.rect = pygame.Rect(0,0,self.font.size(temp_message)[0]+6,self.font.size(temp_message)[1]+8)
        self.rect_border = pygame.Rect(0,0,self.font.size(temp_message)[0]+8,self.font.size(temp_message)[1]+10)

        self.nametext = self.font.render(self.name, 1,self.text_color)
        self.rect_name = pygame.Rect(0,0,self.font.size(self.name)[0],self.font.size(self.name)[1])
        
        self.rect.center = (pos[0]+ self.font.size(self.name)[0]/2,pos[1])
        self.rect_border.center = (pos[0] + self.font.size(self.name)[0]/2,pos[1])
        self.rect_name.center = (pos[0] - self.font.size(temp_message)[0]/2 - 6,pos[1])
    
    def is_mouse_over(self,mousePos):
        if mousePos[0] < self.rect.x or mousePos[0] > self.rect.x + self.rect.w or mousePos[1] < self.rect.y or mousePos[1] > self.rect.y + self.rect.h:
            return False
        return True

    def update_message(self,message):
        if ord(message) != 8 and ord(message) != 13:#not backspace key or enter key
            if len(self.message) < self.maxChars:
                self.message += message
                if self.password == False:
                    self.text = self.font.render(self.message, 1,self.text_color)
                else:
                    message = ""
                    for i in self.message:
                        message += "*"
                    self.text = self.font.render(message, 1,self.text_color)
        elif ord(message) == 8:#backspace key
            if len(self.message) > 0:
                self.message = self.message[:-1]
                if self.password == False:
                    self.text = self.font.render(self.message, 1,self.text_color)
                else:
                    message = ""
                    for i in self.message:
                        message += "*"
                    self.text = self.font.render(message, 1,self.text_color)
        elif ord(message) == 13:#enter key
            self.blink = False
            self.timer = 0
            self.selected = False

    def update(self,events,mousePos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.is_mouse_over(mousePos) == True:
                        self.selected = True
                    else:
                        self.selected = False
            elif event.type == pygame.KEYDOWN:
                try:
                    if self.selected == True:
                        self.update_message(str(chr(event.key)))
                except:
                    pass
        if self.selected == True:
            self.timer += 1
            if self.timer > 20:
                self.timer = 0
                self.blink = not self.blink

    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.rect_border)
        if self.selected == True:
            pygame.draw.rect(screen,(225,225,225),self.rect)
            if self.blink == True:
                rectNew = pygame.Rect(self.rect.x+self.font.size(self.message)[0] + 8,self.rect.y+4,8,self.rect.h-9)
                pygame.draw.rect(screen,(0,0,0),rectNew)
        else:
            pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.nametext, self.rect_name)
        screen.blit(self.text, self.rect)