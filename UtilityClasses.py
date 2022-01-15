import pygame, pygame_gui, thorpy

class HitNumbers():

    def __init__(self,enemy, player, crit,all,Vsprites):
        #super().__init__(all,Vsprites)
        self.enemy = enemy
        self.player = player
        self.Crit = crit #Not implemented
        #self.Images = [pygame.image.load('Images//UtilitySprites//HitEffectFont//0.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//1.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//2.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//3.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//4.png'),
        #               pygame.image.load('Images//UtilitySprites//HitEffectFont//5.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//6.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//7.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//8.png'),pygame.image.load('Images//UtilitySprites//HitEffectFont//9.png')
        #]
        #self.Damage = str(player.rpgData.Damage)
        #self.image = []
        #self.rect = []
        #for i,number in enumerate(self.Damage):
        #    self.image.append(self.Images[int(number)])
        #    self.rect.append(self.image[i].get_rect(center = self.enemy.rect.center))

        #self.rect = self.image.get_rect(center=self.enemy.rect.center)
        self.text = thorpy.make_text(str(self.player.rpgData.Damage))

    def update(self):
        print('Updating')



