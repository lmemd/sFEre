from subprocess import Popen, call
import sys

# THE FOLLOWING CODE HAS ONLY BEEN TESTED IN VISUAL STUDIO CODE ON WINDOWS COMPUTERS

'''
This script will download and install Python 3.9.13 to your computer
If that version of python is already installed, it will update it if necessary
It will also download and install Microsoft Visual Studio 2022 BuildTools
'''

'''
!!! SO FAR THE SCRIPT ONLY WORKS FOR COMPUTERS RUNNING WINDOWS !!!
'''


## INSTALLING (OR UPDATING) THE PYTHON 3.9.13 ##
#FOR WINDOWS
p = Popen("python3_9_13_download.bat")
stdout, stderr = p.communicate()


## INSTALLING C++ TOOL ##

vsc = Popen("MicrosoftVisualC.bat")
stdout, stderr = vsc.communicate()


'''
To continue with the setup you need to select python version 3.9.13 as an instpreter 
(CTRL+SHIFT+P --> Python: Select Interpreter --> Python 3.9.13) and then run system_setup_2.py
'''

# CREATING A VIRTUAL PYTHON ENVIRONMENT USING PYTHON 3.9.13
