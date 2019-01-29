# File name: menublocks.py
from kivy.app import App
from functools import partial
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from dragBlockCore import DragBlock
from blocks import PlayBlock
from blocks import NumberBlock
from blocks import BuilderBlock
from blocks import SensorBlock
import json

click_sound = SoundLoader.load('sounds/touch.wav')

class BlocksTab(TabbedPanel):
    """Menu of the blocks, which tab hold blocks of the same type of command.

        Attributes:
            size (list): List with the size of the tab (witdh,height).
    """
    def __init__(self,width,height, **kwargs):
        super(BlocksTab,self).__init__(**kwargs)
        self.do_default_tab = False
        self.size = [width,height]
        self.buildTab(height - 5)
        Clock.schedule_once(partial(self.switch, self.tab_list[-1]), 0)
        self.sensor_list = [0,0]

    def switch(self, tab, *args):
        self.switch_to(tab)

    def buildTab(self,size):
        self.background_image = "images/gui_elements/tab.png"
        with open("config/blocks.json") as json_data:
            blocks_config = json.load(json_data)
            for tab in blocks_config["tabs"]:
                block_id = tab["id"][0]
                newTab = TabbedPanelItem()
                newTab.background_normal = str(tab["tab_unpress"])
                newTab.background_down = str(tab["tab_press"])
                newLayout = BoxLayout(spacing = 10)
                space = size*0.80/self.size[0]
                newLayout.size_hint = [len(tab["blocks"]) *space,1]
                for block in tab["blocks"]:
                    if '0' not in block["type"]:
                        newBlock = Block(block_id,str(block["id"]),str(block["type"]),str(block["source"]),int(size*0.80))
                        newLayout.add_widget(newBlock)
                newTab.content = newLayout
                self.add_widget(newTab)

"""
Block:
    Widget reptesent each block in the tab
"""
class Block(RelativeLayout):
    """Block inside the tabs, work as a custom buttom.
        Attributes:
            source_photo (str): path to the background image
            type (string): Which group the block is in (Audio, dunction ,sensor, etc).
            id (string): String to indeify the block.
            style (string): Indeify the behave of block if it can only be connected on side,bottom,up, etc.
            app (App): Reference to the holds the main object of the App.
            size (list): List with the size of the tab (witdh,height).
    """
    def __init__(self,type,id,style,source_image,size,**kwargs):
        super(Block,self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.blockType = type
        self.blockID = id
        self.style = style
        self.source_image = source_image
        self.size = [size,size]
        with self.canvas:
            self.rect = Rectangle(size = self.size, source = self.source_image)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            (x,y) = self.app.root.to_widget(touch.x, touch.y)
            self.draw(self.app.root, x, y,self.blockType,self.blockID,self.source_image,self.size,self.style)
            click_sound.play()
            return True
        return super(Block,self).on_touch_down(touch)

    def already_exist(self, list_widget,type,id):
        for widget in list_widget:
            if widget.id == id and widget.type == type:
                return False
        return True

    def draw(self, da, x, y,type,id,source,size,style):
        if (type == "F" and id == "0"):
            db = PlayBlock(type,id,source,size,style)
        elif (type == "F" and id == "1"):
            db = BuilderBlock(type,id,source,size,style)
        elif (type == "F" and id == "2"):
            db = NumberBlock(type,id,source,size,style)
        elif (type == 'S'):
            if self.parent.parent.parent.sensor_list[int(id)-1] == 0:
                db = SensorBlock(type,id,source,size,style)
                self.parent.parent.parent.sensor_list[int(id)-1] += 1
            else:
                return
        else:
            db = DragBlock(type,id,source,size,style)
        db.center = (x,y)
        self.app.root.add_widget(db)
