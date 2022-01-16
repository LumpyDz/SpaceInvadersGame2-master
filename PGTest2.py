import sys, random, math
import pygame
import pygame_gui
import pickle as P
#Made Classes/Files
import PRPGD
import MainMenuGUI as MMGUI
from interpolator import *
import VisualSprites as VS
import UtilityClasses as UC
#import VisualSprites as VS

#Constants
GAMESTATE = 'MAIN_MENU'
SCREENRECT = pygame.Rect(0,0,600,800)
FIRE = 5
#define our sprite groups and add them into super constructors to initiate
all = pygame.sprite.RenderUpdates()
shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
Menu = pygame.sprite.Group()
enemyshots = pygame.sprite.Group()
playerG = pygame.sprite.Group()
Vsprites = pygame.sprite.Group()
Usprites = pygame.sprite.Group()

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
screen = pygame.display.set_mode(SCREENRECT.size)

manager = pygame_gui.UIManager((SCREENRECT.size), 'MainTheme.json')
#GUi element
spawn_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),text='Spawn Enemey',manager=manager)

#Init classes

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
        self.CoinLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((450,30),(150,20)),text=('$$$: ' + str(self.rpgData.Coins)),manager=manager)

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

    #create pre play screen and init starting sprites
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

    #Main play while loop when paused
    while menu.gamestate == 'Play':
        time_delta = clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            #User Events for retry menu
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == spawn_button:
                        print('SpawnPressed')
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
                    elif event.ui_element == player.rpgData.DamageButton and hasattr(player.rpgData, 'DamageButton'):
                        if player.rpgData.StatPoints >= 1:
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

        manager.process_events(event)
        manager.draw_ui(screen)
        manager.update(time_delta)
        player.HealthBar.redraw()
        pygame.display.update()
        if paused == True:
            continue

        else:
            #Main while loop when not paused
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
                hitNumber = UC.HitNumbers(enemy,player,True,all,Usprites)
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
                        coinS = VS.CoinSprite(enemy,all,Vsprites,player)
                        explosion = VS.Explosion(all,Vsprites,enemy)
                        HitNumber = UC.HitNumbers(enemy, player, False, all, Vsprites)

                else:
                    player.rpgData.XPforScore(enemy.Score)
                    player.rpgData.TotalScore += enemy.Score
                    enemy.kill()
                    player.TotalScoreLabel.set_text("Total Score:" + str(player.rpgData.TotalScore))
                    coinS = VS.CoinSprite(enemy,all,Vsprites,player)
                    explosion = VS.Explosion(all,Vsprites,enemy)
                    hitNumber = UC.HitNumbers(enemy, player, False, all, Usprites)

                if player.current_health < player.health_capacity:
                    vampS = VS.VampSprite(enemy,all,Vsprites,player)
                   
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
            for sprite in pygame.sprite.groupcollide(Vsprites, playerG,1,0).keys():
                if type(sprite) == type(coinS):
                    player.rpgData.Coins += 1
                    player.CoinLabel.set_text('$$$:' + str(player.rpgData.Coins))
                    print('Coin')
                elif type(sprite) == type(vampS):
                    if player.current_health <player.health_capacity:
                        LeechedHP = 1
                        player.current_health += LeechedHP
                        player.HealthBar.update(time_delta)
                
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
