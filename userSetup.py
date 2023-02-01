# import os
# import sys
# import pymel.core as pm

# print ('In User Setup')

# pm.evalDeferred('import startup')

import os
import sys
import maya.cmds as cmds

print('In User Setup')

sys.path.append('/Users/rickyric/Documents/GitHub/Python_101')
cmds.evalDeferred('import startup')