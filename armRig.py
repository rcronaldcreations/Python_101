import maya.cmds as cmds


# Create IK Joints

cmds.joint( n='ik_shoulder_jnt', p=[-7, 0, 4])
cmds.joint( n='ik_elbow_jnt', p=[0, 0, 0])
cmds.joint( n='ik_wrist_jnt', p=[6, 0, 4])
cmds.joint( n='ik_wristEnd_jnt', p=[10, 0, 4])
cmds.select(d=True)

ik_jnts = jtlist = [['ik_shoulder_jnt', [-7.0, 0.0, 4.0]], ['ik_elbow_jnt', [0.0, 0.0, 0.0]], ['ik_wrist_jnt', [6.0, 0.0, 4.0]], ['ik_wristEnd_jnt', [10.0, 0.0, 4.0]]] 


# Create FK Joints

cmds.joint( n='fk_shoulder_jnt', p=[-7, 0, 4])
cmds.joint( n='fk_elbow_jnt', p=[0, 0, 0])
cmds.joint( n='fk_wrist_jnt', p=[6, 0, 4])
cmds.joint( n='fk_wristEnd_jnt', p=[10, 0, 4])
cmds.select(d=True)

# Create rig Joints

cmds.joint( n='rig_shoulder_jnt', p=[-7, 0, 4])
cmds.joint( n='rig_elbow_jnt', p=[0, 0, 0])
cmds.joint( n='rig_wrist_jnt', p=[6, 0, 4])
cmds.joint( n='rig_wristEnd_jnt', p=[10, 0, 4])
cmds.select(d=True)

# Create IK Rig
# Create IK handle

cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)


# Create IK Control

# Get ws position of joints
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)

# Get ws position of wrist, elbow and shoulder fk joints
wrist_pos = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
elbow_pos = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
shoulder_pos = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)


# Create an empty group
cmds.group(em=True, name='grp_ctrl_ikWrist')

# Create circle control object
cmds.circle( n='ctrl_ikWrist', nr=(0, 0, 1), c=(0, 0, 0) )

# Parent the control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

# Move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)

# Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

# Create Pole vector for IK and group it
cmds.spaceLocator(n='elbow_pv', p=(0, 0, 0))
cmds.group(em=True, name='grp_elbow_pv')
cmds.parent('elbow_pv','grp_elbow_pv')

# Pole vector constraint to ik elbow ...

# translate it to the ik elbow
cmds.xform('grp_elbow_pv', t=elbow_pos, ws=True)


# Create FK Rig

# Get ws position of wrist, elbow and shoulder fk joints
wrist_pos = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
elbow_pos = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
shoulder_pos = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)

# Create an empty groups for each
cmds.group(em=True, name='grp_ctrl_fkWrist')
cmds.group(em=True, name='grp_ctrl_fkElbow')
cmds.group(em=True, name='grp_ctrl_fkShoulder')

# Create circle control objects for each
cmds.circle( n='ctrl_fkWrist', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.circle( n='ctrl_fkElbow', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.circle( n='ctrl_fkShoulder', nr=(0, 0, 1), c=(0, 0, 0) )

# Parent the controls to the groups
cmds.parent('ctrl_fkWrist', 'grp_ctrl_fkWrist')
cmds.parent('ctrl_fkElbow', 'grp_ctrl_fkElbow')
cmds.parent('ctrl_fkShoulder', 'grp_ctrl_fkShoulder')

# Then transform the groups to their corresponding jnts.
cmds.xform('grp_ctrl_fkWrist', t=wrist_pos, ws=True)
cmds.xform('grp_ctrl_fkElbow', t=elbow_pos, ws=True)
cmds.xform('grp_ctrl_fkShoulder', t=shoulder_pos, ws=True)

# Parent contrain the joints to corresponding ctrls
cmds.parentConstraint('ctrl_fkWrist', 'fk_wrist_jnt', mo=1)
cmds.parentConstraint('ctrl_fkElbow', 'fk_elbow_jnt', mo=1)
cmds.parentConstraint('ctrl_fkShoulder', 'fk_shoulder_jnt', mo=1)

# Parent the fk joint heirarchy
cmds.parent('grp_ctrl_fkElbow', 'ctrl_fkShoulder')
cmds.parent('grp_ctrl_fkWrist', 'ctrl_fkElbow')


# Blend IK and FK to Rig joints

# Create Color Blend nodes

cmds.createNode('blendColors', n='shoulder_rotate_blend')
cmds.createNode('blendColors', n='shoulder_translate_blend')

cmds.createNode('blendColors', n='elbow_rotate_blend')
cmds.createNode('blendColors', n='elbow_translate_blend')

cmds.createNode('blendColors', n='wrist_rotate_blend')
cmds.createNode('blendColors', n='wrist_translate_blend')

# Connect rotations

cmds.connectAttr('ik_shoulder_jnt.rotate', 'shoulder_rotate_blend.color1', f=1)
cmds.connectAttr('fk_shoulder_jnt.rotate', 'shoulder_rotate_blend.color2', f=1)
cmds.connectAttr('shoulder_rotate_blend.output', 'rig_shoulder_jnt.rotate', f=1)

cmds.connectAttr('ik_elbow_jnt.rotate', 'elbow_rotate_blend.color1', f=1)
cmds.connectAttr('fk_elbow_jnt.rotate', 'elbow_rotate_blend.color2', f=1)
cmds.connectAttr('elbow_rotate_blend.output', 'rig_elbow_jnt.rotate', f=1)

cmds.connectAttr('ik_wrist_jnt.rotate', 'wrist_rotate_blend.color1', f=1)
cmds.connectAttr('fk_wrist_jnt.rotate', 'wrist_rotate_blend.color2', f=1)
cmds.connectAttr('wrist_rotate_blend.output', 'rig_wrist_jnt.rotate', f=1)

# Connect translations

cmds.connectAttr('ik_shoulder_jnt.translate', 'shoulder_translate_blend.color1', f=1)
cmds.connectAttr('fk_shoulder_jnt.translate', 'shoulder_translate_blend.color2', f=1)
cmds.connectAttr('shoulder_translate_blend.output', 'rig_shoulder_jnt.translate', f=1)

cmds.connectAttr('ik_elbow_jnt.translate', 'elbow_translate_blend.color1', f=1)
cmds.connectAttr('fk_elbow_jnt.translate', 'elbow_translate_blend.color2', f=1)
cmds.connectAttr('elbow_translate_blend.output', 'rig_elbow_jnt.translate', f=1)

cmds.connectAttr('ik_wrist_jnt.translate', 'wrist_translate_blend.color1', f=1)
cmds.connectAttr('fk_wrist_jnt.translate', 'wrist_translate_blend.color2', f=1)
cmds.connectAttr('wrist_translate_blend.output', 'rig_wrist_jnt.translate', f=1)









