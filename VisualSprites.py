import pygame
import PGTest2 as PG2

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
NEW_MS = PG2.NEW_MS

class VampSprites(pygame.sprite.Sprite):
    def __init__(self,EnemyX,EnemyY, all, Vsprites,player):
        super().__init__(all,Vsprites)
        self.speedX = (0.5**2)
        self.speedY = 1
        self.player = player
        self.enemyX = EnemyX
        self.enemyY = EnemyY
        self.image = pygame.image.load("Images//VisualSprites//VampSprite.png")
        self.rect = self.image.get_rect(center=(self.enemyX,self.enemyY))
        print('Spawned')

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.rect.move_ip(self.speedX,self.speedY)
        elif self.rect.x > self.player.rect.x:
            self.rect.move_ip(-self.speedX,self.speedY)
        else:
            self.rect.move_ip(self.speedX,self.speedY)
        self.speedX += 0.1
        self.speedY += 0.1

class CoinSprite(pygame.sprite.Sprite):
    def __init__(self,EnemyX,EnemyY, all, Vsprites,player):

        super().__init__(all,Vsprites)
        self.player = player
        self.enemyX = EnemyX
        self.enemyY = EnemyY
        self.image = pygame.image.load("Images//VisualSprites//dollar.png")
        self.rect = self.image.get_rect(center=(self.enemyX,self.enemyY))
        print('Spawned')

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.rect.move_ip(1,2)
        elif self.rect.x > self.player.rect.x:
            self.rect.move_ip(-1,2)
        else:
            self.rect.move_ip(0,2)
