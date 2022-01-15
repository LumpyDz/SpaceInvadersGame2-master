import pygame_gui, pygame
from pygame_gui.core.ui_element import ObjectID

class RPGData():
    def __init__(self):
        self.PlayerLevel = 0
        self.CurrentXP = 0
        self.XPNeeded = 5
        self.Coins = 0
        self.Stage = 0
        self.World = 0
        self.TotalScore = 0
        self.Lives = 0
        self.Health = 0
        #States
        self.Damage = 2
        self.LifeLeech = 2
        self.StatPoints = 10
        self.DamageButton = None
        self.HealthButton = None
        self.LifeLeechButton = None

    #Utility Functions
    def XPforScore(self, score):
        self.setCurrentXP(self.getCurrentXP() + score)
        if self.CurrentXP >= self.XPNeeded:
            self.setPlayerLevel(1)
            self.setCurrentXP(0)
            self.setXPNeeded(5)
            self.setStatPoints(1)

    def LifeLeechForDamage(self, damage, EnemyHP):
        if damage > EnemyHP:
            self.Health


    def StatMenu(self,manager,RPGData):
        self.manager = manager
        self.PlayerData = RPGData
        #Main Panel
        self.StatPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=self.manager)
        #Buttons
        self.DamageButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120,120),(140,50)),text='Damage + 1',manager=self.manager,starting_height=1,object_id='#DamageButton')
        self.HealthButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120,200),(140,50)),text='Health + 1',manager=self.manager,starting_height=1)
        self.LifeLeechButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120,280),(140,50)),text='Life Leech + 1',manager=self.manager,starting_height=1)
        #stat Labels
        self.DamageLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((300,120),(150,50)),text='Damage Bonus: ' + str(self.PlayerData.Damage),manager=self.manager)
        self.HealthLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((300,200),(175,50)),text='Health Bonus: ' + str(self.PlayerData.Health),manager=self.manager)
        self.LifeLeechLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((300,280),(175,50)),text='Life Leech Bonus: ' + str(self.PlayerData.LifeLeech),manager=self.manager)
        self.StatPointsLabel = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((200,380),(200,50)),text='Stat Points : ' + str(self.PlayerData.StatPoints),manager=self.manager)

    def KillStatMenu(self):
        self.StatPanel.kill()
        self.DamageButton.kill()
        self.HealthButton.kill()
        self.LifeLeechButton.kill()
        self.DamageLabel.kill()
        self.HealthLabel.kill()
        self.LifeLeechLabel.kill()
        self.StatPointsLabel.kill()
    #Getters
    def getPlayerLevel(self):
        return int(self.PlayerLevel)
    def getCurrentXP(self):
        return int(self.CurrentXP)
    def getXPNeeded(self):
        return int(self.XPNeeded)
    def getStage(self):
        return int(self.Stage)
    def getWorld(self):
        return int(self.World)
    def getTotalScore(self):
        return int(self.TotalScore)
    def getLives(self):
        return int(self.Lives)
    def getDamage(self):
        return int(self.Damage)
    def getDefense(self):
        return int(self.Defense)
    def getStatPoints(self):
        return int(self.StatPoints)
    #Setters
    def setPlayerLevel(self, newLevel):
        self.PlayerLevel += newLevel
    def setCurrentXP(self,amount):
        self.CurrentXP = amount
    def setXPNeeded(self, XP):
        self.XPNeeded += XP
    def setStage(self,newstage):
        self.Stage = newstage
    def setWorld(self,world):
        self.World  = World
    def setTotalStore(self, amount):
        self.TotalScore += amount
    def setLives(self, amount):
        self.lives += amount
    def setDamage(self,amount):
        self.Damage += amount
    def setDefense(self,amount):
        self.Defense += amount
    def setStatPoints(self,amount):
        self.StatPoints += amount
