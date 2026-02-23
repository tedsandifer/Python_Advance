"""**************************************************************************
content      -

version      -
date         -

dependency   -
how to       -
todo         -

license      -
author       Theodore Sandifer <tedsandifder@gmail.com>
**************************************************************************"""

# IMPORTS
import maya.cmds as cmds
import os

from cam_suite import cam_rig

def camera_creator():
    # creates the camera suite gui

    ui_name = 'camera_creator'

    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name)

    cam_ui_wind = cmds.window(ui_name, title = 'Camera Creator', widthHeight = (500, 300))

    cmds.columnLayout(adjustableColumn = True)

    img_path = os.path.dirname(__file__) + '/cam_ui_logo.png'
    cmds.image(image = img_path)
    
    cmds.text(label = ' ', height =  10)
    
    cmds.rowLayout(numberOfColumns = 2)
    cmds.text(label = 'Camera Name', width = 150, height =  30, align='center')
    edit_name = cmds.textField('camera_name', width = 300, height = 30)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 4)
    cmds.text(label = 'Focal Length', width = 100, height =  30, align='center')
    edit_focalLength = cmds.intField('focal_length', editable=True, value=35, width = 150, height = 30)
    cmds.text(label = 'Depth of Field', width = 100, height =  30, align='center')
    edit_dof = cmds.checkBox('depth_of_field',
                             label=' ',
                             align='center', editable=True,
                             value=False,
                             width = 150, height = 30 )
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 4)
    cmds.text(label = 'Near Clip', width = 100, height =  30, align='center')
    edit_nclip = cmds.intField('near_clip', editable=True, value=1, width = 150, height = 30)
    cmds.text(label = 'Far Clip', width = 100, height =  30, align='center')
    edit_fclip = cmds.intField('far_clip', editable=True, value=10000, width = 150, height = 30)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 1)
    cmds.button(label = 'CREATE',
                width = 500,
                align = 'center',
                command = cam_rig.build_cam_rig)
    
    
    cmds.showWindow(ui_name)