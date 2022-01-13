import sys, random, math
import pygame, pygame_gui
import pickle as P
#Made Classes/Files
import PRPGD
import MainMenuGUI as MMGUI
from interpolator import *
#import VisualSprites as VS

#Constants
GRAVITY = -1.8
GAMESTATE = 'MAIN_MENU'
SCREENRECT = pygame.Rect(0,0,600,800)
FIRE = 5
SECONDS = 4
#define our sprite groups and add them into super constructors to initiate
all = pygame.sprite.RenderUpdates()
shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
Menu = pygame.sprite.Group()
enemyshots = pygame.sprite.Group()
playerG = pygame.sprite.Group()
Vsprites = pygame.sprite.Group()

pygame.init()
clock = pygame.time.Clock()
#custom user event with timer
SpawnNow = pygame.event.Event(pygame.USEREVENT + 1)
pygame.time.set_timer(SpawnNow,3000,5)
#Enemy Shot timer
Shoot = pygame.event.Event(pygame.USEREVENT + 2)
pygame.time.set_timer(Shoot, 500)
#Get current MS
#GUI Manager
manager = pygame_gui.UIManager((SCREENRECT.size))
#GUi element
spawn_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),text='Spawn Enemey',manager=manager)
screen = pygame.display.set_mode(SCREENRECT.size)
#Init classes
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
                                 clock.get_fps(),
                                 2,
                                 1
                                 )



        def update_interp(self):
            self.line = Interpolator(
                                     self.line.pos,
                                     self.player.rect.center,
                                     0.5,
                                     clock.get_fps(),
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
                                 2,
                                 clock.get_fps(),
                                 2,
                                 1
                                 )

    def update_interp(self):
        self.line = Interpolator(
                                 self.line.pos,
                                 self.player.rect.center,
                                 0.5,
                                 clock.get_fps(),
                                 1,
                                 0.5
                                 )
    def update(self):
        print('updating')
        if self.rect.y >= 500:
            if self.line.stop != self.player.rect.center:
                self.update_interp()
        self.rect.center = self.line.next()


class Player(pygame.sprite.Sprite):
    #Base player class that handles movement and a method for getting the objects pos(gunpos)
    speed = 5
    images = ''
    health_capacity = 100
    current_health = health_capacity

    def __init__(self):
        super().__init__(all,playerG)
        self.rpgData = PRPGD.RPGData()
        self.rpgData.Health = self.health_capacity
        self.image = self.images
        self.rect = self.image.get_rect(midbottom=(300,780))
        self.reloading = 0
        self.HealthBar = pygame_gui.elements.ui_screen_space_health_bar.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((10,780),(100,20)),
                                                                                                    manager=manager,sprite_to_monitor=Player)
        self.TotalScoreLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((450,10),(150,20)),text=('Total Score: ' + str(self.rpgData.getTotalScore())),manager=manager)

    def Move(self, direction):
        self.rect.x += (direction * self.speed)
        if self.rect.left < 0:
            self.rect.right=(600)
        elif self.rect.right > 600:
            self.rect.left=(0)


    def gunpos(self):
        pos = self.rect.midtop
        return pos

    def sethealth_capacity(self,new_hc, new_cc):
        self.health_capacity = new_hc

class Shot(pygame.sprite.Sprite):

    images = ''

    def __init__(self,pos):
        super().__init__(all,shots)
        self.image = self.images
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(0,-10)
        if self.rect.y <= 0:
            self.kill()

class EnemyShot(pygame.sprite.Sprite):

    images = ''

    def __init__(self,pos):
        super().__init__(all,enemyshots)
        self.image = self.images
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(0,10)
        if self.rect.y >= 800:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    images = ''
    startdirection = 1
    damage = 10

    def __init__(self,hp):
        super().__init__(all,enemies)
        self.image = self.images
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100,500)
        self.rect.y = 100
        self.directionX = random.choice([-1,1])
        self.directionY = 0
        self.LastDirY =  0
        self.HP = hp
        self.Fire = 5
        self.Score = 5


    def gunpos(self):
        pos = self.rect.midbottom
        return pos

    def update(self):
        if self.rect.y < 100:
            self.directionY = 1
            self.rect.move_ip(0,1 * self.directionY)
            self.directionY = 0
            self.LastDirY = self.rect.y

        elif self.directionY > 0:
            if self.rect.y < (self.LastDirY + 24):
                self.rect.move_ip(0,1*self.directionY)
            elif self.rect.y == self.LastDirY + 24:
                self.directionY = 0

        elif self.directionX > 0:
            self.rect.move_ip(1*self.directionX,0)
            if self.rect.right > 600:
                self.directionX = -1
                self.directionY = 1
                self.LastDirY = self.rect.y

        elif self.directionX < 0:
            self.rect.move_ip(1 * self.directionX,0)
            if self.rect.left < 0:
                self.directionX = 1
                self.directionY = 1
                self.LastDirY = self.rect.y

        self.rect = self.rect.clamp(SCREENRECT)

        if len(playerG.sprites()) == 0:
            self.kill()
        if self.HP <= 1:
            self.image = pygame.image.load('Images\EnemyImages\\ufo2.png')

class Spawner():
    def __init__(self, Amount):
        self.Amount = Amount
        self.SpawnEvent = pygame.event.Event(pygame.USEREVENT + 3)
        self.SpawnTimer = pygame.time.set_timer(self.SpawnEvent,5000,0)
        self.offsetCount = 0


    def SpawnBaseEnemy(self):
        self.offsetCount = 0
        for enemy in range(self.Amount):
            spawnE = Enemy(4)
            spawnE.rect.x = (((screen.get_width() - (self.Amount*32)) // 2) + (32*self.offsetCount))
            spawnE.rect.y = -10
            self.offsetCount += 1


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('Images\\BackgroundImages\Space Background.png')
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY1 = 0
        self.bgX1 = 0
        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0
        self.moving_speed = 1

    def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height


    def render(self):
        screen.blit(self.bgimage, (self.bgX1, self.bgY1))
        screen.blit(self.bgimage, (self.bgX2, self.bgY2))


def main():
    #setup main screen
    screen = pygame.display.set_mode(SCREENRECT.size)
    surface = pygame.Surface(screen.get_size())
    #initialize the screen extras
    pygame.display.set_caption('Space Invaders Test 2')
    pygame.display.set_icon(pygame.image.load('SpaceInvadersLogo.png'))

    #setup and display the background
    back_ground = Background()
    pygame.display.flip()

    #Load and prepare images
    Player.images = pygame.image.load('Images\PlayerImages\PlayerImg.png')
    Shot.images = pygame.image.load('Images\ProjectileImages\\bullet.png')
    EnemyShot.images = pygame.image.load('Images\ProjectileImages\\bomb.png')
    Enemy.images = pygame.image.load('Images\EnemyImages\\ufo.png')


    menu = MMGUI.MAINMENU(manager,Menu)
    menu.PrePlayScreen()
    #Create starting Sprites
    while menu.gamestate == 'Main Menu':
        time_delta = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu.PlayButton:
                        menu.gamestate = 'Play'
                        menu.KillPrePlayMenu()
                    if event.ui_element == menu.Quit:
                        return
                    if event.ui_element == menu.LoadGame:
                        menu.KillPrePlayMenu()
                        menu.LoadScreen()
                    if event.ui_element == menu.BackButton:
                        if menu.LoadPanel != None:
                            menu.KillLoadScreen()
                        menu.PrePlayScreen()


        back_ground.update()
        back_ground.render()
        manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    StatMenuOpen = False
    paused = False
    player = Player()
    spawner = Spawner(3)
    while menu.gamestate == 'Play':
        time_delta = clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            #User Events for retry menu
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == spawn_button:
                        Enemy(4)
                    if event.ui_element == menu.PlayAgain:
                        menu.MenuPanel.kill()
                        Player.current_health = Player.health_capacity
                        main()
                    if event.ui_element == menu.Quit:
                        return

                    elif event.ui_element == menu.ResumeButton and hasattr(menu, 'ResumeButton'):
                        paused = not paused
                        menu.KillPauseScreen()
                    #Stat Menu Button Events
                    elif event.ui_element == player.rpgData.DamageButton and player.rpgData.StatPoints >= 1:
                        player.rpgData.Damage += 1
                        player.rpgData.StatPoints -= 1
                        player.rpgData.DamageLabel.set_text('Damage Bonus: ' + str(player.rpgData.Damage))
                        player.rpgData.StatPointsLabel.set_text('Stat Points: ' + str(player.rpgData.StatPoints))

                    elif event.ui_element == player.rpgData.HealthButton and player.rpgData.StatPoints >= 1:
                        player.rpgData.Health += 1
                        player.health_capacity += 1
                        player.current_health += 1
                        player.HealthBar = pygame_gui.elements.ui_screen_space_health_bar.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((10,780),(100,20)),
                                                                                                                            manager=manager,sprite_to_monitor=player)
                        player.rpgData.StatPoints -= 1
                        player.rpgData.HealthLabel.set_text('Health Bonus: '+ str(player.rpgData.Health))
                        player.rpgData.StatPointsLabel.set_text('Stat Points: ' + str(player.rpgData.StatPoints))

                    elif event.ui_element == player.rpgData.LifeLeechButton and player.rpgData.StatPoints >= 1:
                        player.rpgData.LifeLeech += 1
                        player.rpgData.StatPoints -= 1
                        player.rpgData.LifeLeechLabel.set_text('Life Leech Bonus: ' + str(player.rpgData.LifeLeech))
                        player.rpgData.StatPointsLabel.set_text('Stat Points: ' + str(player.rpgData.StatPoints))

                    elif player.rpgData.StatPoints <= 0:
                        player.rpgData.DamageButton.disable()
                        player.rpgData.HealthButton.disable()
                        player.rpgData.LifeLeechButton.disable()

            #Global enemy fire event
            if event.type == pygame.USEREVENT + 2:
                #sprite_list = enemies.sprites()
                for enemy in enemies.sprites():
                    enemy.Fire = random.randint(0,10)
                    if enemy.Fire == FIRE:
                        EnemyShot(enemy.gunpos())

            #Spawner Event
            if event.type == pygame.USEREVENT+3 and paused == False:
                spawner.SpawnBaseEnemy()

            #Pause and Stat Menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and paused == True and StatMenuOpen == False:
                    menu.KillPauseScreen()
                    paused = not paused

                elif event.key == pygame.K_ESCAPE and paused == True and StatMenuOpen == True:
                    player.rpgData.KillStatMenu()
                    paused = False
                    StatMenuOpen = False

                elif event.key == pygame.K_ESCAPE and paused == False and StatMenuOpen == True:
                    player.rpgData.KillStatMenu()
                    menu.PauseMenu()
                    paused = not paused
                    StatMenuOpen = False

                elif event.key == pygame.K_ESCAPE and paused == False and StatMenuOpen == False:
                    menu.PauseMenu()
                    paused = True



                if event.key == pygame.K_l and StatMenuOpen == False:
                    if hasattr(menu,'PausePanel'):
                        menu.KillPauseScreen()

                    statMenu = player.rpgData.StatMenu(manager,player.rpgData)
                    if player.rpgData.StatPoints <= 0:
                        player.rpgData.DamageButton.disable()
                        player.rpgData.HealthButton.disable()
                        player.rpgData.LifeLeechButton.disable()
                    StatMenuOpen = True
                    paused = True

                elif event.key == pygame.K_l and StatMenuOpen == True:
                    player.rpgData.KillStatMenu()
                    StatMenuOpen = False
                    paused = False

                #    paused = not paused
        manager.process_events(event)
        manager.draw_ui(screen)
        manager.update(time_delta)
        player.HealthBar.redraw()
        pygame.display.update()
        if paused == True:
            continue

        else:
            #process GUI events in event loop
            manager.process_events(event)
            manager.update(time_delta)

            all.clear(screen,surface)
            all.update()


            keystate = pygame.key.get_pressed()
            direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
            player.Move(direction)
            fireing = keystate[pygame.K_SPACE]
            if not player.reloading and fireing:
                shot = Shot(player.gunpos())
            player.reloading = fireing
            #Collision detection
            #Enemy for player shots
            for enemy in pygame.sprite.groupcollide(enemies,shots,0,1).keys():
                if enemy.HP > abs((enemy.HP - player.rpgData.getDamage())):
                    #player.rpgData.XPDamage(player.rpgData.getDamage(),enemy.HP)
                    enemy.HP -= player.rpgData.getDamage()
                    #print('Level:',player.rpgData.getPlayerLevel(),'CurrentXP:',player.rpgData.getCurrentXP(),'XPNeeded:',player.rpgData.getXPNeeded())
                    if enemy.HP <= 0:
                        player.rpgData.TotalScore += enemy.Score
                        player.rpgData.XPforScore(enemy.Score)
                        #print('Level:',player.rpgData.getPlayerLevel(),'CurrentXP:',player.rpgData.getCurrentXP(),'XPNeeded:',player.rpgData.getXPNeeded())
                        enemy.kill()
                        #print("Total Score:",player.rpgData.TotalScore)
                        player.TotalScoreLabel.set_text("Total Score:" + str(player.rpgData.TotalScore))
                        coinS = CoinSprite(enemy,all,Vsprites,player)

                else:
                    player.rpgData.XPforScore(enemy.Score)
                    player.rpgData.TotalScore += enemy.Score
                    enemy.kill()
                    #print("Total Score:",player.rpgData.TotalScore)
                    player.TotalScoreLabel.set_text("Total Score:" + str(player.rpgData.TotalScore))

                if player.current_health < player.health_capacity:
                    LeechedHP = float(round((player.rpgData.LifeLeech / 100) * (abs(enemy.HP - player.rpgData.Damage)),2))
                    vampS = VampSprite(enemy,all,Vsprites,player)
                    player.current_health += round(LeechedHP, 2)
                    print(LeechedHP)
                    print(player.current_health)
                    player.HealthBar = pygame_gui.elements.ui_screen_space_health_bar.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((10,780),(100,20)),
                                                                                                                        manager=manager,sprite_to_monitor=player)
            #Player for enemy shots
            for player in pygame.sprite.groupcollide(playerG, enemyshots,0,1).keys():
                player.current_health -= Enemy.damage
                player.HealthBar = pygame_gui.elements.ui_screen_space_health_bar.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((10,780),(100,20)),
                                                                                                                    manager=manager,sprite_to_monitor=player)
                print(player.current_health)
                if player.current_health <= 0:
                    player.kill()
                    #menu.gamestate = 'Retry'
                    menu.RetryScreen()
            #VisualSprites
            for player in pygame.sprite.groupcollide(playerG, Vsprites,0,1).keys():
                print('collided')
            #Spawner
            #spawner = Spawner(10,True)

            #draw elements to screen
            back_ground.update()
            back_ground.render()
            manager.draw_ui(screen)
            dirty = all.draw(screen)
            player.HealthBar.redraw()
            pygame.display.update(dirty)
            #update entire screen again just in case
            pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
