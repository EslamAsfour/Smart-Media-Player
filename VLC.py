import pyautogui
import os
import time
import subprocess
from tkinter import filedialog
import tkinter as tk
import pygetwindow as gw


##############################################################################
# function Name: Open_VLC
# Parameters (in): None
# Parameters (inout): None
# Parameters (out): None
# Return value: return VLC windows structure
# Description: #function to open VLC media player  and choose the file it will play
##############################################################################
def Open_VLC():
    #to get the file that the media player will play
    root=tk.Tk()
    root.withdraw()
    root.update()
    file=filedialog.askopenfile()
    root.destroy()

    #start VLC media player using cmd
    os.system('cmd /c "start vlc.exe"')
    
    #wait till the media player start
    while(1):
        if(gw.getActiveWindow().title == 'VLC media player'):
            break
    VLC=gw.getWindowsWithTitle('VLC media player')[0]
    VLC.maximize()

    #play the choosen file
    pyautogui.hotkey('ctrl', 'o')
    pyautogui.write((file.name).replace("/","\\"))
    pyautogui.press('enter')
    #change the status of the video
    toggle_Status_VLC()
    return VLC
#############################################################################



##############################################################################
# function Name: toggle_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to toggle play/pause of VLC media player 
##############################################################################
def toggle_VLC(VLC):
    if(not(gw.getActiveWindow() == VLC)):
        print("VLC is not on focus")
        return -1
    pyautogui.press('space')
    toggle_Status_VLC()
##############################################################################



##############################################################################
# function Name: VolUP_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to increase the volume of VLC by 5% 
##############################################################################
def VolUP_VLC(VLC):
    if(not(gw.getActiveWindow() == VLC)):
        print("VLC is not on focus")
        return -1
    pyautogui.hotkey('ctrl','up')
##############################################################################



##############################################################################
# function Name: VolDown_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to decrease the volume of VLC by 5% 
##############################################################################
def VolDown_VLC(VLC):
    if(not(gw.getActiveWindow() == VLC)):
        print("VLC is not on focus")
        return -1
    pyautogui.hotkey('ctrl','down')
##############################################################################



##############################################################################
# function Name: Max_VLC
# Parameters (in): VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to maximize the VLC windows  
##############################################################################    
def Max_VLC(VLC):
    VLC.maximize()
    VLC.activate()
##############################################################################



##############################################################################
# function Name: Min_VLC
# Parameters (in): VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to Minimize the VLC windows  
##############################################################################
def Min_VLC(VLC):
    VLC.minimize()
##############################################################################



##############################################################################
# function Name: toggle_Status_VLC
# Parameters (in): None
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to toggle the status parameter of VLC(True|False)
##############################################################################
def toggle_Status_VLC():
    toggle_Status_VLC.status = not(toggle_Status_VLC.status)
#status parameter of the VLC (contain the current status of the VLC)    
toggle_Status_VLC.status = False
##############################################################################



##############################################################################
# function Name: Get_Status_VLC
# Parameters (in): None
# Parameters (inout): None
# Parameters (out): None
# Return value: VLC status
# Description: #function to get the status parameter of VLC(True|False)
##############################################################################
def Get_Status_VLC():
    return toggle_Status_VLC.status
##############################################################################



##############################################################################
# function Name: Play_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to play the media on the VLC player
##############################################################################
def Play_VLC(VLC):
    if(not(gw.getActiveWindow().title == VLC.title)):
        print("VLC is not on focus")
        print(gw.getActiveWindow().title , VLC.title)
        return -1
    if(Get_Status_VLC()==True):
        return 1
    else:
        toggle_VLC(VLC)
        
        return 1 
##############################################################################



##############################################################################
# function Name: Pause_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to pause the media on the VLC player
##############################################################################
def Pause_VLC(VLC):
    if(not(gw.getActiveWindow().title == VLC.title)):
        print("VLC is not on focus")
        print(gw.getActiveWindow().title , VLC.title)
        return -1
    if(Get_Status_VLC()==False):
        return 1
    else:
        toggle_VLC(VLC)
        
        return 1 
##############################################################################



##############################################################################
# function Name: TFS_VLC
# Parameters (in):  VLC windwos structure
# Parameters (inout): None
# Parameters (out): None
# Return value: None
# Description: #function to toggle full screen in VLC player 
##############################################################################
def TFS_VLC(VLC):
    if(not(gw.getActiveWindow() == VLC)):
        print("VLC is not on focus")
        
        return -1
    pyautogui.press('f')
    








