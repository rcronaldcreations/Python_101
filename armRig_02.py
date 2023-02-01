import maya.cmds as cmds

shoulder_pos = [-7.0, 0.0, 4.0]
elbow_pos = [0.0, 0.0, 0.0]
wrist_pos = [6.0, 0.0, 4.0]
wrist_end_pos = [10.0, 0.0, 4.0]

# # Create empty dictionary for all the arm joints
# arm_jnts = {}

# # Append the joints into the dictionary
# arm_jnts['ik_jnts'] = [['ik_shoulder_jnt', shoulder_pos], ['ik_elbow_jnt', elbow_pos], ['ik_wrist_jnt', wrist_pos], ['ik_wristEnd_jnt', wrist_end_pos]]
# arm_jnts['fk_jnts'] = [['fk_shoulder_jnt', shoulder_pos], ['fk_elbow_jnt', elbow_pos], ['fk_wrist_jnt', wrist_pos], ['fk_wristEnd_jnt', wrist_end_pos]]
# arm_jnts['rig_jnts'] = [['rig_shoulder_jnt', shoulder_pos], ['rig_elbow_jnt', elbow_pos], ['rig_wrist_jnt', wrist_pos], ['rig_wristEnd_jnt', wrist_end_pos]]

# # Loop through the dictionary, and then loop through each value of the dictionary (that's the different joints)
# for key, value in arm_jnts.items():
#     for i in range(len(arm_jnts[key])):
#         cmds.joint( n=value[i][0], p=value[i][1])
#     if len(value) >= len(arm_jnts[key]): 
#         cmds.select(cl=1, sym=1)

### function implementation
ik_jnt_list = [['ik_shoulder_jnt', shoulder_pos], ['ik_elbow_jnt', elbow_pos], ['ik_wrist_jnt', wrist_pos], ['ik_wristEnd_jnt', wrist_end_pos]]
fk_jnt_list = [['fk_shoulder_jnt', shoulder_pos], ['fk_elbow_jnt', elbow_pos], ['fk_wrist_jnt', wrist_pos], ['fk_wristEnd_jnt', wrist_end_pos]]

def createJoints(jntinfo):
    for item in jntinfo:
        cmds.joint( n=item[0], p=item[1])

createJoints(ik_jnt_list)
cmds.select(cl=1, sym=1)
createJoints(fk_jnt_list)
cmds.select(cl=1, sym=1)


# Create IK handle

cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)

# Create IK Control

# Get ws position of joints
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)

# Get ws position of wrist, elbow and shoulder fk joints
fk_wrist_pos = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
fk_elbow_pos = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
fk_shoulder_pos = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)


# Create an empty group
cmds.group(em=True, name='grp_ctrl_ikWrist')

# Create circle control object
cmds.circle( n='ctrl_ikWrist', nr=(0, 0, 1), c=(0, 0, 0) )

# Parent the control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

# Move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=wrist_pos, ws=True)

# Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

# Create Pole vector for IK and group it
cmds.spaceLocator(n='elbow_pv', p=(0, 0, 0))
cmds.group(em=True, name='grp_elbow_pv')
cmds.parent('elbow_pv','grp_elbow_pv')

# Pole vector constraint to ik elbow ...

# translate it to the ik elbow
cmds.xform('grp_elbow_pv', t=elbow_pos, ws=True)

fk_ctrls = {}

# Append the grps and ctrls into the dictionary
fk_ctrls['arm'] = [['grp_ctrl_fkShoulder', 'ctrl_fkShoulder', shoulder_pos], ['grp_ctrl_fkElbow', 'ctrl_fkElbow', elbow_pos], ['grp_ctrl_fkWrist', 'ctrl_fkWrist', wrist_pos]]
fk_jnts = ['fk_shoulder_jnt', 'fk_elbow_jnt', 'fk_wrist_jnt']
# Loop through the dictionary, and then loop through each value of the dictionary (that's the different joints)
for key, value in fk_ctrls.items():
    for i in range(len(fk_ctrls[key])):
        # print(fk_jnts[i])

        grp = cmds.group(em=True, name=value[i][0])
        ctrl = cmds.circle(n=value[i][1], nr=(0, 0, 1), c=(0, 0, 0))
        pos = value[i][2]
        cmds.parent(ctrl, grp)
        cmds.xform(grp, t=pos, ws=True)
        cmds.parentConstraint(ctrl, fk_jnts[i], mo=1)

    # if len(value) >= len(arm_jnts[key]): 
    #     cmds.select(cl=1, sym=1)

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








