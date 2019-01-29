"""
Blocks.py:
Collection of classes for each blocks used in GUI, all commun behaves are defined
in dragBlockCore.py. To add new type of blocks change this file.
"""
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from wifi import my_socket
from dragBlockCore import DragBlock
from random import randrange,shuffle
from kivy.app import App

play_sound_fail = SoundLoader.load('sounds/start_fail.wav')
play_sound_succes = SoundLoader.load('sounds/start_succes.wav')

class NumberBlock(DragBlock):
    """Block that works as number for blocks that can hold numbers.

        Attributes:
            counter (int): Current number in the block.
            plusButton (Button): Button to add the current number.
            minusButton (Button): Button to decrease the current number.
    """
    def __init__(self,type,id,source_photo,size,style,**kwargs):
        super(NumberBlock, self).__init__(type,id,source_photo,size,style,**kwargs)
        self.counter = 1
        self.space_a = Widget()
        self.space_a.size_hint = [0.35,1]
        self.space_b = Widget()
        self.space_b.size_hint = [0.50,1]
        self.plusButton = Button()
        self.plusButton.background_normal = 'images/functions/plus.png'
        self.plusButton.background_down   = 'images/functions/plus_press.png'
        self.plusButton.bind(on_press = self.add)
        self.plusButton.size_hint =  [1,0.30]
        self.plusButton.pos_hint = {'top':0.60}
        self.minusButton = Button()
        self.minusButton.background_normal = 'images/functions/minus.png'
        self.minusButton.background_down   = 'images/functions/minus_press.png'
        self.minusButton.bind(on_press = self.minus)
        self.minusButton.size_hint = [1,0.30]
        self.minusButton.pos_hint = {'top':0.60}
        self.blockLayout = BoxLayout(spacing = 1, orientation = 'horizontal')
        self.value = Label(text = str(self.counter),font_size='30sp')
        self.value.size_hint = [1,1]
        self.value.pos_hint = {'top':0.95}
        self.value.color = [0.80,1,0,1]
        self.blockLayout.add_widget(self.space_a)
        self.blockLayout.add_widget(self.minusButton)
        self.blockLayout.add_widget(self.value)
        self.blockLayout.add_widget(self.plusButton)
        self.blockLayout.add_widget(self.space_b)
        self.add_widget(self.blockLayout)

    def add(self,instance):
        self.counter = self.counter + 1
        if self.counter > 10:
            self.counter = 1
        self.value.text = str(self.counter)

    def minus(self,instance):
        self.counter = self.counter - 1
        if self.counter < 1:
            self.counter = 10
        self.value.text = str(self.counter)

class BuilderBlock(DragBlock):
    """Block to create InstanceBlock.

        Attributes:
            childBoxes (list): List of current brocks connected.
            buildButton (Button): Button to create a InstanceBlock.
            minusButton (Button): Button to decrease the current number.
    """
    def __init__(self,type,id,source_photo,size,style,**kwargs):
        super(BuilderBlock, self).__init__(type,id,source_photo,size,style,**kwargs)
        #List to store all created instances
        self.childBoxes = []
        #Add button in the center
        self.blockColor = [randrange(0,50,1)/255, randrange(0,255,25)/255, randrange(0,255,50)/255]
        shuffle(self.blockColor)
        with self.canvas:
            Color(self.blockColor[0],self.blockColor[1],self.blockColor[2],1)
            Rectangle(pos=(self.size[0]*0.25,self.size[1]*0.25),size_hint=(0.5, 0.5))
        self.buildButton = Button()
        self.buildButton.background_normal = 'images/functions/build_button.png'
        self.buildButton.background_down   = 'images/functions/build_button_press.png'
        self.buildButton.bind(on_press = self.build_command) #Command to send datagram to robot
        self.add_widget(self.buildButton)
        self.buildButton.size_hint = [0.5,0.5]
        self.buildButton.pos_hint = {'top':0.72, 'right':0.74}

    #Create an Instance block
    def build_command(self,instance):
        (x,y) = self.pos
        db = InstanceBlock("F","3","images/functions/macro_ins_brick.png",self.size,"0lr",self.blockColor,self)
        db.center = (x,y)
        self.childBoxes.append(db)
        self.app.root.add_widget(db)

    #Can't conencted with any InstanceBlocks (No recursive lists...)
    def on_touch_up(self, touch):
        super(BuilderBlock, self).on_touch_up(touch)
        right = self.right_block
        while right is not None:
            if right.type == "F" and right.id == "3":
                self.right_block.unbind()
                self.right_block.x += self.size[0]*0.5
                self.right_block.left_block = None
                self.right_block = None
                break
            right = right.right_block
        block = self
        self.command = ''
        while block is not None:
            if block.bottom_block is not None:
                block.command = block.type + str(block.id) + str(block.bottom_block.value.text)
            self.command += block.command
            block = block.right_block
        return

    #Erase need to also delete isntances blocks
    def eraseBlocks(self):
        for block in self.childBoxes:
            if block.left_block is not None:
                block.left_block.right_block = None
                block.left_block.unbind()
                block.left_block = None
            if block.right_block is not None:
                block.right_block.left_block = None
                block.right_block.unbind()
                block.right_block = None
            self.app.root.remove_widget(block)
        super(BuilderBlock, self).eraseBlocks()

class InstanceBlock(DragBlock):
    """Block that holds a predefined group of commands.

        Attributes:
            father (DragBlock): Reference to the BuilderBlock.
    """
    def __init__(self,type,id,source_photo,size,style,color,father,**kwargs):
        super(InstanceBlock, self).__init__(type,id,source_photo,size,style,**kwargs)
        myColor = Color(color[0],color[1],color[2])
        self.canvas.add(myColor)
        with self.canvas:
            Rectangle(pos=(self.size[0]*0.25,self.size[1]*0.25),size_hint=(0.5, 0.5))
        self.father = father

    #Can't conencted with any BuilderBlock (No recursive lists...)
    def on_touch_up(self, touch):
        super(InstanceBlock, self).on_touch_up(touch)
        left = self
        while left.left_block is not None:
            left = left.left_block
        if left.type == "F" and left.id == "1":
            left.right_block.left_block = None
            left.right_block.unbind()
            left.right_block.x += self.size[0]*0.5
            left.right_block = None
            return
    #Return command on BuilderBlock
    def get_list(self):
        return self.father.command

class PlayBlock(DragBlock):
    """Block that send the current command to the robot by UDP server.

        Attributes:
            playButton (Button): BUtton to send the command.
    """
    def __init__(self,type,id,source_photo,size,style,**kwargs):
        super(PlayBlock, self).__init__(type,id,source_photo,size,style,**kwargs)
        #Add button in the center
        self.playButton = Button() #PLaceHolder for now
        self.playButton.background_normal = 'images/functions/play_button.png'
        self.playButton.background_down   = 'images/functions/play_button_press.png'
        self.playButton.bind(on_press = self.build_command) #Command to send datagram to robot
        self.add_widget(self.playButton)
        self.playButton.size_hint = [0.6, 0.6]
        self.playButton.pos_hint = {'top':0.80, 'right':0.80}

    #Check the list of block and build a full list of commands
    def build_command(self,instance):
        #First Build the command
        self.command = ''
        temp = self.right_block
        while temp is not None:
            if temp.bottom_block is not None:
                temp.command = temp.type + str(temp.id) + str(temp.bottom_block.value.text)
                self.command += temp.command
            elif temp.type == "F" and temp.id == "3":
                self.command += temp.get_list()
            else:
                self.command += temp.command
            temp = temp.right_block
        #Once build we can send to Robot
        self.sendCommands(self.command)
        #send command

    def sendCommands(self, msg):
        my_socket.connect()

        if my_socket.send_data(msg):
            play_sound_succes.play()
        else:
            play_sound_fail.play()

class SensorBlock(DragBlock):
    """Block hold the command to be executed if the sensor is activated.
    """
    def __init__(self,type,id,source_photo,size,style,**kwargs):
        super(SensorBlock, self).__init__(type,id,source_photo,size,style,**kwargs)
        self.command = ''

    def on_touch_up(self, touch):
        super(SensorBlock, self).on_touch_up(touch)
        command = ''
        command =  self.type + self.id
        temp = self.right_block
        while temp is not None:
            if temp.bottom_block is not None:
                temp.command = temp.type + str(temp.id) + str(temp.bottom_block.value.text)
                command += temp.command
            elif temp.type == "F" and temp.id == "3":
                command += temp.get_list()
            else:
                command += temp.command
            temp = temp.right_block
        if command != self.command :
            self.command = command
            self.sendCommands(self.command)

    def sendCommands(self, msg):
        my_socket.connect()
        my_socket.send_data(msg)


    #Delete all chain blocks and unlock for create another sensor block
    def eraseBlocks(self):
        super(SensorBlock, self).eraseBlocks()
        self.app.root.children[-1].sensor_list[int(self.id)-1] = 0
