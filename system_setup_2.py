from subprocess import Popen, call
import sys

'''
This script will install all the required libraries to run the codes
'''

## INSTALLING ALL THE REQUIRED LIBRARIES ##

def install(package):
    call([sys.executable, '-m', 'pip', 'install', package])


package2read = open('requirements.txt', 'r')

package = package2read.read().splitlines()
for lib in package:
    install(lib)
