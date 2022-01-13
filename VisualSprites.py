import pygame
from interpolator import *

'''==============================
    This class handles all Visual Sprites and their respective movement.
    Sprites: |1| Vamp Sprites:
                Blue Sprites should spawn on the enemy within the area of the enemy image.They should loop outward and then toward the player,
                once they reach the player they should disappear. When they reach the player the vamp effecton life leech should apply for the amount of damage
                done to the enemy.
             |2| Coin Sprites: pictures of coins that should explode out of enemies and land somewhere +10 units away from the enemies previous image location
             |3| NextSprite:
             |4| NextSprite:
=============================='''


class VampSprite(pygame.sprite.Sprite):
    def __init__(self,Enemy,all, Vsprites,player):
        super().__init__(all,Vsprites)
        self.player = player
        self.enemy = Enemy
        self.image = pygame.image.load("Images//VisualSprites//VampSprite.png")
        self.rect = self.image.get_rect(center=(self.enemy.rect.x,self.enemy.rect.y))
        self.line = Interpolator(
                                 self.enemy.rect.center,
                                 self.player.rect.center,
                                 2,
                                 60,
                                 1,
                                 1
                                 )



    def update_interp(self):
        self.line = Interpolator(
                                    self.line.pos,
                                    self.player.rect.center,
                                    0.5,
                                    60,
                                    1,
                                    0.5
                                    )
    def update(self):
        print('updating')
        if self.rect.y >= 500:
            if self.line.stop != self.player.rect.center:
                self.update_interp()
        self.rect.center = self.line.next()

class CoinSprite(pygame.sprite.Sprite):

    def __init__(self,Enemy, all, Vsprites,player):
        super().__init__(all,Vsprites)
        self.player = player
        self.enemy = Enemy
        self.image = pygame.image.load("Images//VisualSprites//dollar.png")
        self.rect = self.image.get_rect(center=(self.enemy.rect.x,self.enemy.rect.y))
        self.line = Interpolator(
                                 self.enemy.rect.center,
                                 self.player.rect.center,
                                 4,
                                 60,
                                 2,
                                 1
                                 )

    def update_interp(self):
        self.line = Interpolator(
                                 self.line.pos,
                                 self.player.rect.center,
                                 0.5,
                                 60,
                                 1,
                                 0.5
                                 )
    def update(self):
        print('updating')
        if self.rect.y >= 500:
            if self.line.stop != self.player.rect.center:
                self.update_interp()
        self.rect.center = self.line.next()
