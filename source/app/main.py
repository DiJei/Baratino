from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from tabMenu import BlocksTab



''' Setting screen for desktop - don't needed for Mobile '''
#-------------------------------------------------------#

import pygame
pygame.init()
infoObject = pygame.display.Info()
h = str(infoObject.current_h)
w = str(infoObject.current_w)
pygame.quit()
#-------------------------------------------------------#
from kivy.config import Config
Config.set('graphics', 'width', w)
Config.set('graphics', 'height', h)
Config.set('graphics', 'resizable', '1')
Config.set('input','mouse','mouse,disable_multitouch')
#-------------------------------------------------------#


from kivy.core.window import Window


class GuiScreen(Widget):
    """Widget that will hold all other widget of the Appself.

    Args:
        none.

    Attributes:
        source_photo (str): path to the background image
        size (list): define the size of widget (width, height)
        tabBlocks (BlocksTab): custom widget object that holds the tab of the App.
    """
    def __init__(self, **kwargs):
        super(GuiScreen,self).__init__(**kwargs)
        self.source_photo = "images/gui_elements/blueprint.png"
        self.size = [Window.width,Window.height]
        with self.canvas:
            self.rect = Rectangle(source=self.source_photo, pos=[0,0], size=self.size)
        self.tabBlocks = BlocksTab(self.size[0],int(self.size[1]/4))
        self.tabBlocks.pos = [0,0]
        self.add_widget(self.tabBlocks)


class BaratinoApp(App):
    def build(self):
        return GuiScreen()

if __name__ == '__main__':
    BaratinoApp().run()
