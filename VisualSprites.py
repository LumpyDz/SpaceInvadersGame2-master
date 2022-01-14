import pygame
from interpolator import *

'''==============================
    This class handles all Visual Sprites and their respective movement.
    Sprites: |1| Vamp Sprites:
                Blue Sprites should spawn on the enemy within the area of the enemy image.They should loop outward and then toward the player,
                once they reach the player they should disappear. When they reach the player the vamp effecton life leech should apply for the amount of damage
                done to the enemy.
             |2| Coin Sprites: pictures of coins that should explode out of enemies and land somewhere +10 units away from the enemies previous image location
             |3| Explosion:
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
        if self.rect.y >= 500:
            if self.line.stop != self.player.rect.center:
                self.update_interp()
        self.rect.center = self.line.next()

class CoinSprite(pygame.sprite.Sprite):

    def __init__(self,Enemy, all, Vsprites,player):
        super().__init__(all,Vsprites)
        self.player = player
        self.enemy = Enemy
        self.Images = [pygame.image.load("Images//VisualSprites//RotatingCoin//tile000.png"),pygame.image.load("Images//VisualSprites//RotatingCoin//tile001.png"),pygame.image.load("Images//VisualSprites//RotatingCoin//tile002.png"),
                       pygame.image.load("Images//VisualSprites//RotatingCoin//tile003.png"),pygame.image.load("Images//VisualSprites//RotatingCoin//tile004.png"),pygame.image.load("Images//VisualSprites//RotatingCoin//tile005.png")]
        self.index = 0
        self.count = 0
        self.image = self.Images[self.index]  #pygame.image.load("Images//VisualSprites//dollar.png")
        self.rect = self.image.get_rect(center=(self.enemy.rect.x,self.enemy.rect.y))
        self.line = Interpolator(
                                 self.enemy.rect.center,
                                 self.player.rect.center,
                                 3,
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
        self.count += 1
        if self.count == 5:
            self.index += 1
            self.count = 0
        if self.index >= len(self.Images):
            self.index = 0
        else:
            self.image = self.Images[self.index]
            if self.rect.y >= 500:
                if self.line.stop != self.player.rect.center:
                    self.update_interp()
            self.rect.center = self.line.next()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, all, Vsprites,Enemy):
        super().__init__(all,Vsprites)
        self.enemy = Enemy
        self.Images = [pygame.image.load('Images\\Explosion2\\tile000.png'),pygame.image.load('Images\\Explosion2\\tile001.png'),pygame.image.load('Images\\Explosion2\\tile002.png'),pygame.image.load('Images\\Explosion2\\tile003.png'),pygame.image.load('Images\\Explosion2\\tile004.png'),
             pygame.image.load('Images\\Explosion2\\tile005.png'),pygame.image.load('Images\\Explosion2\\tile006.png'),pygame.image.load('Images\\Explosion2\\tile007.png'),pygame.image.load('Images\\Explosion2\\tile008.png'),pygame.image.load('Images\\Explosion2\\tile009.png'),
             pygame.image.load('Images\\Explosion2\\tile010.png'),pygame.image.load('Images\\Explosion2\\tile011.png'),pygame.image.load('Images\\Explosion2\\tile012.png'),pygame.image.load('Images\\Explosion2\\tile013.png'),pygame.image.load('Images\\Explosion2\\tile014.png'),
             pygame.image.load('Images\\Explosion2\\tile015.png'),pygame.image.load('Images\\Explosion2\\tile016.png'),pygame.image.load('Images\\Explosion2\\tile017.png'),pygame.image.load('Images\\Explosion2\\tile018.png'),pygame.image.load('Images\\Explosion2\\tile019.png'),
             pygame.image.load('Images\\Explosion2\\tile020.png'),pygame.image.load('Images\\Explosion2\\tile021.png'),pygame.image.load('Images\\Explosion2\\tile022.png'),pygame.image.load('Images\\Explosion2\\tile023.png'),pygame.image.load('Images\\Explosion2\\tile024.png')]
        self.index = 0
        self.image = self.Images[self.index]
        self.rect = self.image.get_rect(center = self.enemy.rect.center)

    def update(self):
        self.index += 1
 
        if self.index >= len(self.Images):
            self.kill()
        else:
            self.image = self.Images[self.index]
