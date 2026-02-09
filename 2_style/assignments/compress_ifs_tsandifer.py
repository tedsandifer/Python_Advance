"""
content = assignment
course  = Python Advanced
 
date    = 02/08/2026
email   = tedsandifer@gmail.com
"""
#Imports
import maya.cmds as mc


#Function to change the color of a curve
def set_color(ctrlList=None, color=None):

    temp_val = color
    color_val ={1:4,
                2:13,
                3:25,
                4:17,
                5:17,
                6:15,
                7:6,
                8:16,
                }

    for ctrlName in ctrlList:
        if color < 1 or color > 8:
            print("Please choose a color number between 1 and 8")
        
        else:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
            mc.setAttr(ctrlName + 'Shape.overrideColor', color_val[temp_val])
            print(f"{ctrlName} color has been set to {color_val[temp_val]}")


# EXAMPLE
set_color(['circle','circle1'], 8)