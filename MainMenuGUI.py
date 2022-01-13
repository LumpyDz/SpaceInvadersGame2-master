import pygame_gui, pygame

class MAINMENU(pygame.sprite.Sprite):
    def __init__(self,manager,Menu):
        super().__init__(Menu)
        self.manager = manager
        self.gamestate = "Main Menu"
        self.PlayAgain = None
        #self.Quit = None
        self.BackButton = None
        self.ResumeButton = None
        #self.MenuPanel = None

    def RetryScreen(self):
        self.MenuPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=self.manager)
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((90,0),(200,50)),text='You Died! Play Again?',manager=self.manager,container = self.MenuPanel)
        self.PlayAgain = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((150,150),(100,50)), text='Play Again?', manager=self.manager, container=self.MenuPanel)
        self.Quit = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((150,200),(100,50)), text='Quit', manager=self.manager, container=self.MenuPanel)

    def PrePlayScreen(self):
        self.PrePlayPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=self.manager)
        self.PlayButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.PrePlayPanel.rect.x,50), (200, 50)),text='New Game',manager=self.manager,container=self.PrePlayPanel)
        self.InfoButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.PrePlayPanel.rect.x, 100), (200, 50)),text='Info',manager=self.manager,container=self.PrePlayPanel)
        self.Quit = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((self.PrePlayPanel.rect.x,200),(200,50)), text='Quit', manager=self.manager, container=self.PrePlayPanel)
        self.LoadGame = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((self.PrePlayPanel.rect.x,150),(200,50)), text='Load Game', manager=self.manager, container=self.PrePlayPanel)

    def LoadScreen(self):
        self.LoadPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=self.manager)
        self.BackButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100,350), (200, 50)),text='Back',manager=self.manager,container=self.LoadPanel)

    def PauseMenu(self):
        self.PausePanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=self.manager)
        self.Quit = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((self.PausePanel.rect.x,200),(200,50)), text='Quit', manager=self.manager, container=self.PausePanel)
        self.ResumeButton = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((self.PausePanel.rect.x,150),(200,50)), text='Resume', manager=self.manager, container=self.PausePanel)

    #KillScreens

    def KillLoadScreen(self):
        self.LoadPanel.kill()
        self.BackButton.kill()

    def KillPrePlayMenu(self):
        self.PlayButton.kill()
        self.InfoButton.kill()
        self.Quit.kill()
        self.LoadGame.kill()
        self.PrePlayPanel.kill()

    def KillPauseScreen(self):
        self.PausePanel.kill()
        self.Quit.kill()
        self.ResumeButton.kill()
