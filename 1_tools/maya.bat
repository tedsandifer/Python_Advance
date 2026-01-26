::
@echo off

::PATH
set "SCRIPT_PATH=C:/Users/tedsa/Documents/python_work/maya_scripts/"
set "PYTHONPATH=%SCRIPT_PATH%;%PYTHONPATH%"

::PLUGIN
set "MAYA_PLUG_IN_PATH=%SCRIPT_PATH%plugins;%MAYA_PLUG_IN_PATH%"

::SHELF
set "MAYA_SHELF_PATH=%SCRIPT_PATH%shelf;%MAYA_SHELF_PATH%"

::SPLASHSCREEN
set "XBMLANGPATH=%SCRIPT_PATH%img;%XBMLANGPATH%"

::DISABLE REPORT
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"

::Start Maya
start "" "C:/Program Files/Autodesk/Maya2026/bin/maya.exe"

exit