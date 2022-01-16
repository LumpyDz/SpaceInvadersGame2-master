import pygame, pygame_gui
from interpolator import *

pygame.font.init()
number_font = pygame.font.SysFont( None, 32 )

class HitNumbers(pygame.sprite.Sprite):

    def __init__(self,enemy, player, crit,all,Usprites):
        super().__init__(all,Usprites)
        self.enemy = enemy
        self.player = player
        self.Crit = crit #Not implemented
        self.image = number_font.render( str(self.player.rpgData.Damage), True, 'WHITE' )
        self.rect = self.image.get_rect(center=self.enemy.rect.center)
        self.yStart = self.enemy.rect.y
        self.xStart = self.enemy.rect.x
        self.speed = 1,-(3*1.8)
        self.line = Interpolator(
                            self.enemy.rect.center,
                            (self.rect.x+50,self.rect.y-50),
                            1,
                            60,
                            2,
                            0.1
                            )
        
        

    def update(self):
        if self.line.next() != None:
            self.rect.center = self.line.pos
        if self.rect.y >= self.yStart+50:
            self.kill()
