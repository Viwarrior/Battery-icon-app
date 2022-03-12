# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:15:25 2022

@author: user
"""
# Import the required libraries
from pystray import MenuItem as item
from pystray import Icon
from PIL import Image, ImageDraw, ImageFont
from psutil import sensors_battery
from time import sleep


# functions

#to update image of icon
def update_image(icon, msg, plug):   
    
    #defualts
    icon_color = "white"
    low_color =  "#fc2b35"
    plug_color = "#55e645"
    
    #color logic
    if(msg<30):
        icon_color = low_color
    if(plug):
        icon_color = plug_color
    
    #int to str
    msg = str(msg)
    
    #100
    if msg == "100":
        msg = "CC"
    
    #create the icon
    title_font = ImageFont.truetype('wide.ttf', 470)
    W, H = (700,700)
    im = Image.new("RGBA",(W,H),"#101010")
    draw = ImageDraw.Draw(im)
    w, h = draw.textsize(msg, font=title_font)
    draw.text(((W-w)/2,40), msg, fill=icon_color,font = title_font)
    
    #save image
    im.save("icon_image.png", "PNG")
    
    #update icon
    icon.icon = Image.open("icon_image.png")

#to stop entire program
def quit_window(icon, item):

    #stop the running icon
    icon.stop()

# change ui periodically
def change_ui(icon):
    icon.visible = True
    
    old_msg = -1
    old_plug = 8
    while(True):
        
        #battery stats
        battery_obj = sensors_battery()
        plug = battery_obj.power_plugged
        msg = battery_obj.percent
        
        if msg != old_msg  or plug != old_plug:    
            #update the image
            update_image(icon, msg,plug)
        
        #update old_msg
        old_msg = msg
        
        #update plug
        old_plug = plug
        
        
        #do it each second
        sleep(2)
    
#classes
class Icon_class():
    def __init__(self):
        #open image
        self.image = Image.open("icon_image.png")
        
        #create option menu to quit systray icon
        self.menu=(item('Quit', quit_window),)
        
        #create icon
        self.icon=Icon("name", self.image, "Battery notifier", self.menu)
        
    def run_icon(self):
        #run icon
        self.icon.run_detached(setup = change_ui)

#main
if __name__ == "__main__":
    #create icon object
    battery_icon = Icon_class()
    
    #run icon
    battery_icon.run_icon()
