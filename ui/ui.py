import maya.cmds as cmds
import importlib as ib

print('UI')

def rigarm(*args):
    print('Rig_Arm_Is_Cool')
    import rig.rig_arm as rig_arm
    # ib.reload(rig_arm)

mymenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rigarm)


