"""**************************************************************************
content      creates a cam and rig

version      1.0.0
date         2/20/2026

author       Theodore Sandifer <tedsandifder@gmail.com>
**************************************************************************"""

import maya.cmds as cmds
import json
import os

# json file import for curve cvs---------------------------------------
# I used the json confi file to store all my curve cv data for the rig
current_folder = os.path.dirname(__file__)
json_path = f'{current_folder}\\cam_rig_verts.json'

with open(json_path) as json_file:
   cam_rig_verts = json.load(json_file)


# Create Pop ups ------------------------------------------------------
def popup_no_name():
   result = cmds.confirmDialog(title = 'HOLD UP!',
                               message = 'Looks like you forgot to enter a camera name!',
                               button = 'Whoops, my bad.',
                               defaultButton = 'Whoops, my bad.')

def popup_no_scene():
   result = cmds.confirmDialog(title = 'HOLD UP!',
                               message = 'Looks like you forgot to build the scene!',
                               button = 'Whoops, my bad.',
                               defaultButton = 'Whoops, my bad.')

# Build Cam with Rig --------------------------------------------------
def build_cam_rig(button_name):
   scene_file = cmds.ls(assemblies=True)
   cam_name = cmds.textField('camera_name', query=True, text=True)
   cam_nclip = cmds.intField('near_clip', query=True, value=True)
   cam_fclip = cmds.intField('far_clip', query=True, value=True)
   cam_focalLength = cmds.intField('focal_length', query=True, value=True)
   cam_dof = cmds.checkBox('depth_of_field', query=True, value=True)

   if cam_name == '':
      popup_no_name()

   elif 'SCENE' not in scene_file:
      popup_no_scene()

   
   else:
      cam_name = Camera(cam_name, cam_nclip, cam_fclip, cam_focalLength, cam_dof)
      cam_name.create_cam()
      create_focus_grp()
      create_cam_rig_base()
      create_cam_rig_offset()
      create_cam_rig_trans()
      create_cam_rig_pan()
      create_cam_rig_tilt()
      create_cam_rig_roll()
      create_cam_rig_shake()
      create_cam_all()

      cmds.parent(cam_name + '_focusGrp', cam_name)
      cmds.group(name = cam_name + '_connect', empty=True)
      cmds.parent(cam_name, cam_name + '_connect')
      cmds.parent(cam_name + '_connect', cam_name + '_rig_shake')
      cmds.parent(cam_name + '_rig_shake', cam_name + '_rig_roll')
      cmds.parent(cam_name + '_rig_roll', cam_name + '_rig_tilt')
      cmds.parent(cam_name + '_rig_tilt', cam_name + '_rig_pan')
      cmds.parent(cam_name + '_rig_pan', cam_name + '_rig_trans')
      cmds.parent(cam_name + '_rig_trans', cam_name + '_rig_offset')
      cmds.parent(cam_name + '_rig_offset', cam_name + '_rig_base')
      cmds.parent(cam_name + '_rig_base',cam_name + '_ALL')
      cmds.parent(cam_name + '_ALL','CAMERAS')
      cmds.select(clear=True)

   '''I decided to use the class function for my camera 
   but Im not sure if I will end up keeping it. I really struggles to 
   find a good case use for the class in my script. I think the GUI 
   will be my best use case scenario'''

class Camera():
   
   def __init__(self, cam_name, cam_nclip, cam_fclip, cam_focalLength, cam_dof):

   self.cam_name = cam_name
   self.cam_nclip = cam_nclip
   self.cam_fclip = cam_fclip
   self.cam_focalLength = cam_focalLength
   self.cam_dof = cam_dof

   def create_cam(self):
      new_cam = cmds.camera()
      new_cam_trans = new_cam[0]
      new_cam_shape = new_cam[1]

      cmds.setAttr(new_cam_shape + '.focalLength', self.cam_focalLength)
      cmds.setAttr(new_cam_shape + '.depthOfField', self.cam_dof)
      cmds.setAttr(new_cam_shape + '.nearClipPlane', self.cam_nclip)
      cmds.setAttr(new_cam_shape + '.farClipPlane', self.cam_fclip)


      cmds.rename(new_cam_shape, self.cam_name + "_Shape")
      cmds.rename(new_cam_trans, self.cam_name)

# Create Focus Group --------------------------------------------------
def create_focus_grp():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   cmds.group(name = cam_name + '_focusGrp', empty=True)

   # Create Focal Rig Shape
   rig_focal_name = cam_name + '_rig_focal'
   cmds.circle(name=rig_focal_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=8, ch=1)
   cmds.rotate(-90,0,0, rig_focal_name + '.cv[:]')
   cmds.scale(0.121,0.121,0.121, rig_focal_name + '.cv[:]')
   cmds.move(0,0,5, rig_focal_name)
   cmds.setAttr(rig_focal_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_focal_name + 'Shape.ovc',6)
   cmds.setAttr(rig_focal_name + 'Shape.lineWidth', 1.5)

   # Connect Focal Shape to Cam's Focal Distance
   cmds.parent(rig_focal_name, cam_name + '_focusGrp')
   cmds.rotate(0,180,0, cam_name + '_focusGrp')
   cmds.connectAttr(rig_focal_name + '.translateZ', cam_name + '_Shape.focusDistance',
               force=True)

   # Lock Attributes not used
   focus_lock_list = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v' ]
   focal_lock_list = ['.rx', '.ry', '.rz', '.sx', '.sy', '.sz']

   for attribute in focus_lock_list:
      cmds.setAttr(cam_name + '_focusGrp' + attribute, lock=True, keyable=False, channelBox=False)

   
   for attribute in focal_lock_list:
      cmds.setAttr(rig_focal_name + attribute, lock=True, keyable=False, channelBox=False)



# Create Cam Rig Base -----------------------------------------------------------------
def create_cam_rig_base():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_base_name = cam_name + '_rig_base'
   cmds.circle(name = rig_base_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=64, ch=1)

   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'base':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_base_name + '.' + vert_num[-1], ws=True)
      else:
         continue
   
   cmds.setAttr(rig_base_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_base_name + 'Shape.ovc',17)
   cmds.setAttr(rig_base_name + 'Shape.lineWidth', 1.5)

# Offset -------------------------------------------------------------------
def create_cam_rig_offset():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_offset_name = cam_name + '_rig_offset'
   cmds.circle(name=rig_offset_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=92, ch=1)
   
   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'offset':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_offset_name + '.' + vert_num[-1], ws=True)
      else:
         continue

   cmds.setAttr(rig_offset_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_offset_name + 'Shape.ovc',6)
   cmds.setAttr(rig_offset_name + 'Shape.lineWidth', 1.5)

# Trans -------------------------------------------------------------------
def create_cam_rig_trans():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_trans_name = cam_name + '_rig_trans'
   cmds.circle(name=rig_trans_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=60, ch=1)

   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'trans':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_trans_name + '.' + vert_num[-1], ws=True)
      else:
         continue

   cmds.setAttr(rig_trans_name +'Shape.overrideEnabled',1)
   cmds.setAttr(rig_trans_name +'Shape.ovc',13)
   cmds.setAttr(rig_trans_name + 'Shape.lineWidth', 1.5)

   trans_lock_list = ['.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']
   for attribute in trans_lock_list:
      cmds.setAttr(rig_trans_name + attribute, lock=True, keyable=False, channelBox=False)


# Tilt -------------------------------------------------------------------
def create_cam_rig_tilt():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_tilt_name = cam_name + '_rig_tilt'
   cmds.circle(name=rig_tilt_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=36, ch=1)

   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'tilt':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_tilt_name + '.' + vert_num[-1], ws=True)
      else:
         continue

   cmds.setAttr(rig_tilt_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_tilt_name + 'Shape.ovc',9)
   cmds.setAttr(rig_tilt_name + 'Shape.lineWidth', 1.5)

   tilt_lock_list = ['.tx', '.ty', '.tz', '.ry', '.rz', '.sx', '.sy', '.sz', '.v' ]
   for attribute in tilt_lock_list:
      cmds.setAttr(rig_tilt_name + attribute, lock=True, keyable=False, channelBox=False)


# Pan -------------------------------------------------------------------
def create_cam_rig_pan():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_pan_name = cam_name + '_rig_pan'
   cmds.circle(name=rig_pan_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=36, ch=1)

   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'pan':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_pan_name + '.' + vert_num[-1], ws=True)
      else:
         continue

   cmds.setAttr(rig_pan_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_pan_name + 'Shape.ovc',18)
   cmds.setAttr(rig_pan_name + 'Shape.lineWidth', 1.5)

   pan_lock_list = ['.tx', '.ty', '.tz', '.rx', '.rz', '.sx', '.sy', '.sz', '.v' ]
   for attribute in pan_lock_list:
      cmds.setAttr(rig_pan_name + attribute, lock=True, keyable=False, channelBox=False)


# Roll -------------------------------------------------------------------
def create_cam_rig_roll():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_roll_name = cam_name + '_rig_roll'
   cmds.circle(name=rig_roll_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=36, ch=1)

   for vert, pos in cam_rig_verts.items():
      vert_num = vert.split('.')

      if vert_num[0] == 'roll':
         cmds.move(float(pos[0]), float(pos[1]), float(pos[2]), rig_roll_name + '.' + vert_num[-1], ws=True)
      else:
         continue

   cmds.setAttr(rig_roll_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_roll_name + 'Shape.ovc',20)
   cmds.setAttr(rig_roll_name + 'Shape.lineWidth', 1.5)

   roll_lock_list = ['.tx', '.ty', '.tz', '.rx', '.ry', '.sx', '.sy', '.sz', '.v' ]
   for attribute in roll_lock_list:
      cmds.setAttr(rig_roll_name + attribute, lock=True, keyable=False, channelBox=False)

# Shake -----------------------------------------------------------------
def create_cam_rig_shake():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   rig_shake_name = cam_name + '_rig_shake'
   cmds.circle(name=rig_shake_name, c=(0, 0, 0), nr=(0, 1, 0), sw=360,
            r=1, d=3, ut=0, tol=0.01, s=8, ch=1)
   cmds.rotate(0,0,-90, rig_shake_name + '.cv[:]')
   cmds.scale(0.121,0.121,0.121, rig_shake_name + '.cv[:]')
   cmds.move(0,1.05,-0.224, rig_shake_name + '.cv[:]', relative=True)
   cmds.setAttr(rig_shake_name + 'Shape.overrideEnabled',1)
   cmds.setAttr(rig_shake_name + 'Shape.ovc',16)
   cmds.setAttr(rig_shake_name + 'Shape.lineWidth', 1.5)


def create_cam_all():
   cam_name = cmds.textField('camera_name', query=True, text=True)
   cam_name_all = cam_name + '_ALL'
   cmds.group(name = cam_name_all, empty=True)

   all_grp_lock_list = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v' ]
   for attribute in all_grp_lock_list:
      cmds.setAttr(cam_name_all + attribute, lock=True, keyable=False, channelBox=False)
