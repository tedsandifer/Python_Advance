"""**************************************************************************
content      Camera Suite GUI Class

version      1.0.0
date         3/15/2026

author       Theodore Sandifer <tedsandifder@gmail.com>
**************************************************************************"""

import os
import sys
import webbrowser

from Qt import QtWidgets, QtGui, QtCore, QtCompat

from cam_suite import cam_rig_functions

import maya.cmds as cmds

#****************************************************************************
# VARIABLES
#****************************************************************************

TITLE = os.path.splitext(os.path.basename(__file__))[0]
CURRENT_PATH = os.path.dirname(__file__)
IMG_PATH = CURRENT_PATH + "/img/{}.png"
CAMERA_LIST = []
CAM_LENS_LIST = ["11", "16", "18", "21", "28", "30", "35", "40",
            "50", "60", "70", "100", "150", "200", "300"]
FSTOP_LIST = ["2", "2.8", "4", "5.6", "8", "11", "16", "22" ]

TEMP_SCENE_CAMS = "CAMERAS"
if cmds.objExists(TEMP_SCENE_CAMS):
    SCENE_CAMS = cmds.listRelatives("CAMERAS", children=True, parent=False)
    CAMERA_LIST.append(SCENE_CAMS)
else:
    pass

#****************************************************************************
# CLASS
#****************************************************************************

class CamSuite:

    def __init__(self):
        path_ui = CURRENT_PATH + "/" + TITLE +".ui"
        self.wgSave = QtCompat.loadUi(path_ui)


        #Window Icon
        self.wgSave.setWindowIcon(QtGui.QPixmap(IMG_PATH.format("cam_shelf_logo")))

        #NEW CAM TEXT LABEL
        self.wgSave.ledNewCamName.setPlaceholderText("Enter Camera Name Here")

        #Button Images
        self.wgSave.btn_offset_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_offset_img")))
        self.wgSave.btn_base_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_base_img")))
        self.wgSave.btn_trans_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_trans_img")))
        self.wgSave.btn_pan_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_pan_img")))
        self.wgSave.btn_tilt_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_tilt_img")))
        self.wgSave.btn_roll_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_roll_img")))
        self.wgSave.btn_shake_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_Shake_img")))
        self.wgSave.btn_cam_img.setIcon(QtGui.QPixmap(IMG_PATH.format("cam_rig_camera_img")))

        #True/ False Button image swap
        self.wgSave.btn_frustum_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_off_img")))
        self.wgSave.btn_dof_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_off_img")))


        #SIGNALS BTNS
        self.wgSave.btnNewCam.clicked.connect(self.create_new_cam)
        self.wgSave.btn_base.clicked.connect(lambda: self.select_rig("_rig_base"))
        self.wgSave.btn_base_img.clicked.connect(lambda: self.select_rig("_rig_base"))
        self.wgSave.btn_offset.clicked.connect(lambda: self.select_rig("_rig_offset"))
        self.wgSave.btn_offset_img.clicked.connect(lambda: self.select_rig("_rig_offset"))
        self.wgSave.btn_trans.clicked.connect(lambda: self.select_rig("_rig_trans"))
        self.wgSave.btn_trans_img.clicked.connect(lambda: self.select_rig("_rig_trans"))
        self.wgSave.btn_pan.clicked.connect(lambda: self.select_rig("_rig_pan"))
        self.wgSave.btn_pan_img.clicked.connect(lambda: self.select_rig("_rig_pan"))
        self.wgSave.btn_tilt.clicked.connect(lambda: self.select_rig("_rig_tilt"))
        self.wgSave.btn_tilt_img.clicked.connect(lambda: self.select_rig("_rig_tilt"))
        self.wgSave.btn_roll.clicked.connect(lambda: self.select_rig("_rig_roll"))
        self.wgSave.btn_roll_img.clicked.connect(lambda: self.select_rig("_rig_roll"))
        self.wgSave.btn_shake.clicked.connect(lambda: self.select_rig("_rig_shake"))
        self.wgSave.btn_shake_img.clicked.connect(lambda: self.select_rig("_rig_shake"))
        self.wgSave.btn_cam_img.clicked.connect(lambda: self.select_rig("_Cam"))
        self.wgSave.btn_frustum_img.toggled.connect(self.switch_frustum)
        self.wgSave.btn_dof_img.toggled.connect(self.switch_dof)
        self.wgSave.cbxFocalLength.activated.connect(self.select_focal_length)
        self.wgSave.cbxFStop.activated.connect(self.select_fstop)
        self.wgSave.ledNewCamName.returnPressed.connect(self.create_new_cam)

        #CAM SLIDERS
        self.wgSave.sldPan.valueChanged.connect(lambda value: self.slider_update(value, "_rig_pan.ry", "sldPan"))
        self.wgSave.sldTilt.valueChanged.connect(lambda value: self.slider_update(value, "_rig_tilt.rx", "sldTilt"))
        self.wgSave.sldRoll.valueChanged.connect(lambda value: self.slider_update(value, "_rig_roll.rz", "sldRoll"))
        self.wgSave.sldPan.sliderReleased.connect(lambda: self.slider_reset("sldPan"))
        
        #SIGNALS COMBOBOX
        self.wgSave.cbxSceneCams.addItems(CAMERA_LIST)
        self.wgSave.cbxFocalLength.addItems(CAM_LENS_LIST)
        self.wgSave.cbxFStop.addItems(FSTOP_LIST)

        #LINE EDITS
        self.wgSave.ledPan.editingFinished.connect(lambda: self.update_from_ui("_rig_pan.ry", "ledPan"))
        self.wgSave.ledTilt.editingFinished.connect(lambda: self.update_from_ui("_rig_tilt.rx", "ledTilt"))
        self.wgSave.ledRoll.editingFinished.connect(lambda: self.update_from_ui("_rig_roll.rz", "ledRoll"))
        self.wgSave.ledNearClip.editingFinished.connect(lambda: self.update_from_ui("_Cam.nearClipPlane", "ledNearClip"))
        self.wgSave.ledFarClip.editingFinished.connect(lambda: self.update_from_ui("_Cam.farClipPlane", "ledFarClip"))
        self.wgSave.ledFocusDis.editingFinished.connect(lambda: self.update_from_ui("_rig_focal.tz", "ledFocusDis"))
        self.wgSave.ledFocusRegionScale.editingFinished.connect(lambda: self.update_from_ui("_Cam.focusRegionScale", "ledFocusRegionScale"))



        #SHOW GUI
        self.wgSave.show()

        self.link_attr_to_gui("_rig_pan.ry", "ledPan")
        self.link_attr_to_gui("_rig_tilt.rx", "ledTilt")
        self.link_attr_to_gui("_rig_roll.rz", "ledRoll")

    def link_attr_to_gui(self, rig_attr, led_name):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        if cbx_cam_select:
            self.job_id = cmds.scriptJob(
                attributeChange=[cbx_cam_select + rig_attr, lambda: self.update_from_maya(rig_attr, led_name)])
        else:
            pass

    #FUNCTIONS
    def create_new_cam(self):
        cam_name = self.wgSave.ledNewCamName.text()
        cam_rig_functions.build_cam_rig(cam_name)
        CAMERA_LIST.append(cam_name)
        self.wgSave.cbxSceneCams.addItems(CAMERA_LIST)
        self.wgSave.ledNewCamName.clear()
        self.link_attr_to_gui("_rig_pan.ry", "ledPan")
        self.link_attr_to_gui("_rig_tilt.rx", "ledTilt")
        self.link_attr_to_gui("_rig_roll.rz", "ledRoll")
        self.link_attr_to_gui("_Cam.nearClipPlane", "ledNearClip")
        self.link_attr_to_gui("_Cam.farClipPlane", "ledFarClip")
        self.link_attr_to_gui("_rig_focal.tz", "ledFocusDis")
        self.link_attr_to_gui("_Cam.focusRegionScale", "ledFocusRegionScale")





    def select_rig(self, rig_name):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        cmds.select(cbx_cam_select + rig_name)

    def select_focal_length(self):
        lens_select = self.wgSave.cbxFocalLength.currentText()
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        cmds.setAttr(cbx_cam_select + "_Cam.focalLength", int(lens_select))

    def select_fstop(self):
        current_fstop = self.wgSave.cbxFStop.currentText()
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        cmds.setAttr(cbx_cam_select + "_Cam.fStop", float(current_fstop))

    def switch_frustum(self, is_checked):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        if is_checked:
            cmds.setAttr(cbx_cam_select + "_Cam.displayCameraFrustum", True)
            self.wgSave.btn_frustum_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_on_img")))
        else:
            cmds.setAttr(cbx_cam_select + "_Cam.displayCameraFrustum", False)
            self.wgSave.btn_frustum_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_off_img")))

    def switch_dof(self, is_checked):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        if is_checked:
            cmds.setAttr(cbx_cam_select + "_Cam.depthOfField", True)
            cmds.setAttr(cbx_cam_select + "_focusGrp.v", 1)
            self.wgSave.btn_dof_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_on_img")))
        else:
            cmds.setAttr(cbx_cam_select + "_Cam.depthOfField", False)
            cmds.setAttr(cbx_cam_select + "_focusGrp.v", 0)
            self.wgSave.btn_dof_img.setIcon(QtGui.QPixmap(IMG_PATH.format("btn_switch_off_img")))


    #SLIDER FUNCTIONS

    def slider_update(self, value, rig_name, slider_name):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        current_val = cmds.getAttr(cbx_cam_select + rig_name)
        cmds.setAttr(cbx_cam_select + rig_name, value + current_val)

    def slider_reset(self, slider_name):
        current_slider = getattr(self.wgSave, slider_name)
        time.sleep(.5)
        current_slider.blockSignals(True)
        current_slider.setValue(0)
        current_slider.blockSignals(False)

    #MAYA TO UI UPDATE
    def update_from_ui(self, rig_attr,led_name):
        target_widget = getattr(self.wgSave, led_name)
        ui_val = target_widget.text()
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        cmds.setAttr(cbx_cam_select + rig_attr, float(ui_val))
            

    def update_from_maya(self, rig_attr, led_name):
        cbx_cam_select = self.wgSave.cbxSceneCams.currentText()
        maya_val = cmds.getAttr(cbx_cam_select + rig_attr)
        target_widget = getattr(self.wgSave, led_name)
        target_widget.setText(str(maya_val))


        


#****************************************************************************
# START UI
#****************************************************************************

def show_cam_suite_gui():
    global cam_suite
    cam_suite = CamSuite()
    
