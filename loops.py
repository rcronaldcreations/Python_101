import maya.cmds as cmds

jtlist = [['ik_shoulder_jnt', [0.0, 0.0, 0.0]], ['ik_elbow_jnt', [-1.0, 0.0, 2.0]], ['ik_wrist_jnt', [0.0, 0.0, 4.0]], ['ik_wristEnd_jnt', [0.0, 0.0, 6.0]]]

for item in jtlist:
    cmds.joint( n=item[0], p=item[1])