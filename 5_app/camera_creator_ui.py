"""**************************************************************************
content     -Creates the Camera UI that sets the desired attributes 
            and builds the rig camera on completion.

version     -1.0.1
date        -2/8/2026

dependency  -cam_rig
how to      -create_cam_ui()
todo        -

license     -
author      -Theodore Sandifer <tedsandifder@gmail.com>
**************************************************************************"""

#Imports
import maya.cmds as cmds
import os

from cam_suite import cam_rig


#**********************************************************************
#Camera Creator function that builds the UI
def create_cam_ui():
    
    ui_name = 'camera_creator'

    #Checks to see if the UI exist, if it does, current ui is deleted and rebuilt.
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name)

    cam_ui_wind = cmds.window(ui_name, 
                              title = 'Camera Creator', 
                              widthHeight = (500, 300),
                              )

    #Main layout established
    cmds.columnLayout(adjustableColumn = True)
    
    
    #Banner Image for UI
    img_path = os.path.dirname(__file__) + '/cam_ui_logo.png'
    cmds.image(image = img_path)
    
    #Blank line inserted for aesthetics
    cmds.text(label = ' ', height =  10)
    
    #Camera name input textfield
    cmds.rowLayout(numberOfColumns = 2)
    cmds.text(label = 'Camera Name',
              width = 150, height =  30,
              align = 'center',
              )
    edit_name = cmds.textField('camera_name',
                               width = 300, height = 30,
                               )
    cmds.setParent('..')

    #Camera attributes - focal length, depth of field
    cmds.rowLayout(numberOfColumns = 4)
    cmds.text(label = 'Focal Length',
              width = 100, height =  30,
              align = 'center',
              )
    edit_focalLength = cmds.intField('focal_length',
                                     editable = True,
                                     value = 35,
                                     width = 150, height = 30,
                                     )
    cmds.text(label = 'Depth of Field',
              width = 100, height =  30,
              align = 'center',
              )
    edit_dof = cmds.checkBox('depth_of_field',
                             label = ' ',
                             align = 'center',
                             editable = True,
                             value = False,
                             width = 150, height = 30,
                             )
    cmds.setParent('..')
    
    #Camera attributes - near and far clipping
    cmds.rowLayout(numberOfColumns = 4)
    cmds.text(label = 'Near Clip',
              width = 100, height =  30,
              align = 'center',
              )
    edit_nclip = cmds.intField('near_clip',
                               editable = True,
                               value = 1,
                               width = 150, height = 30,
                               )
    cmds.text(label = 'Far Clip',
              width = 100, height =  30,
              align ='center',
              )
    edit_fclip = cmds.intField('far_clip',
                               editable = True,
                               value = 10000,
                               width = 150, height = 30,
                               )
    cmds.setParent('..')
    
    #Create camera button
    cmds.rowLayout(numberOfColumns = 1)
    cmds.button(label = 'CREATE',
                width = 500,
                align = 'center',
                command = cam_rig.build_cam_rig)
    
    
    cmds.showWindow(ui_name)