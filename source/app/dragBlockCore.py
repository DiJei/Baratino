from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader
from kivy.app import App

click_sound = SoundLoader.load('sounds/touch.wav')
erase_sound = SoundLoader.load('sounds/erase.wav')
connect_sound = SoundLoader.load('sounds/connect.wav')

class DragBlock(RelativeLayout):
    """Define the behave of a common dragging block.

        Attributes:
            selected (Boolean): Boolean that check if the brick is been dragged.
            left_block (Block): Reference to the block connected on the left.
            right_block (Right): Reference to the block connected on the right.
            up_block (Up): Reference to the block connected on the up.
            bottom_block (Bottom): Reference to the block connected on the bottom.
            type (string): Which group the block is in (Audio, dunction ,sensor, etc).
            id (string): String to indeify the block.
            style (string): Indeify the behave of block if it can only be connected on side,bottom,up, etc.
            command (string): String tha represent the command that it holds.
            app (App): Reference to the holds the main object of the App.
    """
    def __init__(self,type,id,source_photo,size,style,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        #Keep pointer to connected block
        self.left_block   = None
        self.right_block  = None
        self.up_block     = None
        self.bottom_block = None
        self.id = id
        self.type = type
        self.size = size
        self.style = style
        self.app = App.get_running_app()
        if "u" in self.style:
            self.command = type + str(id) + "1"
        else:
            self.command = type + str(id)
        with self.canvas:
            Color(1,1,1)
            self.rect = Rectangle(source=source_photo, pos=self.pos, size=self.size)
    #Block is pressed, disconect with any left block
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.left_block is not None:
                self.left_block.right_block = None
                self.left_block.unbind()
                self.left_block = None
            if self.up_block is not None:
                self.up_block.command = self.up_block.type + str(self.up_block.id) + "1"
                self.up_block.bottom_block = None
                self.up_block.unbind()
            self.up_block = None
            self.left_block = None
            self.selected = True
            click_sound.play()
        return RelativeLayout.on_touch_down(self, touch)
    #Block is been dragged
    def on_touch_move(self, touch):
        if self.selected:
            self.center = (touch.x,touch.y)
            return True
        return RelativeLayout.on_touch_move(self, touch)
    #Press release check if there is any block to connect
    def on_touch_up(self, touch):
        if self.selected:
            self.selected = False
            if self.parent.children[-1].collide_point(touch.x, touch.y):
                self.eraseBlocks()
                return True
            last = self
            while(last.right_block != None):
                last = last.right_block
            list_blocks = self.app.root.children[:-1]
            list_blocks.remove(self)
            for block in list_blocks:
                if self.collide_widget(block):
                    if self.checkLeft(block,touch) and "l" in self.style and "r" in block.style:
                        if block.right_block is None:
                            self.left_block = block
                            block.right_block = self
                            self.pos = self.left_block.x + self.left_block.width*0.80, self.left_block.y
                            block.bind(pos = self.updatePosHorizotnal)
                            connect_sound.play()
                    elif self.checkRight(None,block,touch) and "r" in self.style and "l" in block.style:
                        if block.left_block is None:
                            self.right_block = block
                            block.left_block = self
                            self.pos = block.x - block.width*0.80, block.y
                            self.bind(pos = block.updatePosHorizotnal)
                            connect_sound.play()
                    elif "u" in self.style + block.style and "b" in self.style + block.style:
                        if "u" in self.style and self.checkBottom(block,touch):
                            if block.up_block is None:
                                self.bottom_block = block
                                block.up_block = self
                                self.bind(pos = block.updatePosVertical)
                                block.pos = block.x, self.y - block.height
                                connect_sound.play()
                        elif "b" in self.style and self.checkUp(block,touch):
                            if block.up_block is None:
                                self.up_block = block
                                block.bottom_block = self
                                block.bind(pos = self.updatePosVertical)
                                self.pos = self.up_block.x, block.y - self.height*0.60
                                connect_sound.play()
                if last.collide_widget(block) and "r" in last.style and "l" in block.style:
                    if last.checkRight(last,block,touch):
                        if block.left_block is None:
                            last.right_block = block
                            block.left_block = last
                            last.pos = block.x - block.width*0.80, block.y
                            temp = last.left_block
                            while(temp != None):
                                temp.pos = temp.right_block.x - temp.right_block.width*0.80, temp.right_block.y
                                temp = temp.left_block
                            last.bind(pos = last.right_block.updatePosHorizotnal)
                            connect_sound.play()
        return RelativeLayout.on_touch_up(self, touch)

    #See if there is a block to connect on the left
    def checkLeft(self,block,touch):
        if self.x > block.x + (block.width/2) and self.x < block.x  + block.width and self.y >= block.y*0.95 and self.y <= block.y + block.height:
            return True
        return False
    #See if there is a block to connect on the Right
    def checkRight(self,another,block,touch):
        if another is None:
            if self.x + self.width > block.x  and self.x + self.width < block.x + (block.width/2) and self.y >= block.y*0.95  and self.y <= block.y + block.height:
                return True
            return False
        else:
            if another.x + another.width > block.x  and another.x + another.width < block.x + (block.width/2) and another.y >= block.y*0.95  and another.y <= block.y + block.height:
                return True
            return False
    #See if there is a block to connect on the Bottom
    def checkBottom(self,block,touch):
        if self.y <= block.y + block.height and self.y  > block.y + block.height/2 and  self.x >= block.x and self.x <= block.x + (block.width/2):
            return True
        return False
    #See if there is a block to connect on the Bottom
    def checkUp(self,block,touch):
        if self.y + self.height >= block.y and self.y + self.height  < block.y + block.height/2 and  self.x >= block.x and self.x <= block.x + (block.width/2):
            return True
        return False
    #Used to update position of connected block
    def updatePosHorizotnal(self, *args):
        if self.left_block:
            self.pos = self.left_block.x + self.left_block.width*0.80, self.left_block.y
    def updatePosVertical(self, *args):
        if self.up_block:
            self.pos = self.up_block.x, self.up_block.y - self.height*0.60
    #Delete all chain blocks
    def eraseBlocks(self):
        temp = None
        end = self
        while(end.right_block != None):
            end = end.right_block
        while(end != self):
            temp = end
            end = temp.left_block
            if temp.bottom_block is not None:
                self.app.root.remove_widget(temp.bottom_block)
            self.app.root.remove_widget(temp)

        if self.bottom_block:
            self.app.root.remove_widget(self.bottom_block)
        self.app.root.remove_widget(self)
        erase_sound.play()
