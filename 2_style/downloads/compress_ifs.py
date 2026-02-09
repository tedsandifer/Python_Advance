"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com
"""

from maya import mel as mc



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
        if color == False:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
      
        elif color > 8:
            print("Please choose a color number between 1 and 8")
        
        else:
            mc.setAttr(ctrlName + 'Shape.overrideColor', color_val[temp_val])

        '''else:
            if color == 1:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 4)
            elif color == 2:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 13)
            elif color == 3:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 25)
            elif color == 4:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 17)
            elif color == 5:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 17)
            elif color == 6:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 15)
            elif color == 7:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 6)
            elif color == 8:
                mc.setAttr(ctrlName + 'Shape.overrideColor', 16)
      '''


# EXAMPLE
set_color(['circle','circle1'], 9)
