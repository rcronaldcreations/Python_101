import maya.cmds as cmds

shoulder_pos = [-7.0, 0.0, 4.0]
elbow_pos = [0.0, 0.0, 0.0]
wrist_pos = [6.0, 0.0, 4.0]
wrist_end_pos = [10.0, 0.0, 4.0]

### function implementation
ik_jnt_list = [['ik_shoulder_jnt', shoulder_pos], ['ik_elbow_jnt', elbow_pos], ['ik_wrist_jnt', wrist_pos], ['ik_wrist_end_jnt', wrist_end_pos]]
fk_jnt_list = [['fk_shoulder_jnt', shoulder_pos], ['fk_elbow_jnt', elbow_pos], ['fk_wrist_jnt', wrist_pos], ['fk_wrist_end_jnt', wrist_end_pos]]
rig_jnt_list = [['rig_shoulder_jnt', shoulder_pos], ['rig_elbow_jnt', elbow_pos], ['rig_wrist_jnt', wrist_pos], ['rig_wrist_end_jnt', wrist_end_pos]]

def createJoints(jntinfo):
    for item in jntinfo:
        cmds.joint( n=item[0], p=item[1])

# Create IK joints
createJoints(ik_jnt_list)
cmds.select(cl=1, sym=1)
# Create FK joints
createJoints(fk_jnt_list)
cmds.select(cl=1, sym=1)
# Create Rig joints
createJoints(rig_jnt_list)
cmds.select(cl=1, sym=1)

# Create IK handle

def createIkArmCtrl(name, first_jnt, mid_jnt, last_jnt, ik_name, pv_name):
    print('ik_done')

    cmds.ikHandle( n=name, sj=first_jnt, ee=last_jnt, sol='ikRPsolver', p=2, w=1)

    # Create IK Control

    # Get ws position of wrist and elbow ik joints
    ik_wrist_pos = cmds.xform(last_jnt, q=True, t=True, ws=True)
    ik_elbow_pos = cmds.xform(mid_jnt, q=True, t=True, ws=True)
    # Create an empty group
    cmds.group(em=True, name='grp_ctrl_{}'.format(ik_name))
    # Create circle control object
    cmds.circle( n='ctrl_{}'.format(ik_name), nr=(0, 0, 1), c=(0, 0, 0) )
    # Parent the control to the group
    cmds.parent('ctrl_{}'.format(ik_name), 'grp_ctrl_{}'.format(ik_name))
    # Move the group to the joint
    cmds.xform('grp_ctrl_{}'.format(ik_name), t=ik_wrist_pos, ws=True)
    # Parent ikh to ctrl
    cmds.parent(name, 'ctrl_{}'.format(ik_name))
    # Create Pole vector for IK and group it
    cmds.spaceLocator(n=pv_name, p=(0, 0, 0))
    cmds.group(em=True, name='grp_{}'.format(pv_name))
    cmds.parent(pv_name,'grp_{}'.format(pv_name))
    # translate it to the ik elbow
    cmds.xform('grp_elbow_pv', t=ik_elbow_pos, ws=True)


createIkArmCtrl('ikh_arm', 'ik_shoulder_jnt', 'ik_elbow_jnt', 'ik_wrist_jnt', 'ik_wrist', 'elbow_pv')


def createFkArmCtrl(shoulder_name, elbow_name, wrist_name):
    fk_ctrls = {}

    # Append the grps and ctrls into the dictionary
    fk_ctrls['arm'] = [['grp_ctrl_{}'.format(shoulder_name), 'ctrl_{}'.format(shoulder_name), shoulder_pos], ['grp_ctrl_{}'.format(elbow_name), 'ctrl_{}'.format(elbow_name), elbow_pos], ['grp_ctrl_{}'.format(wrist_name), 'ctrl_{}'.format(wrist_name), wrist_pos]]
    fk_jnts = ['{}_jnt'.format(shoulder_name), '{}_jnt'.format(elbow_name), '{}_jnt'.format(wrist_name)]
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
    cmds.parent('grp_ctrl_{}'.format(elbow_name), 'ctrl_{}'.format(shoulder_name))
    cmds.parent('grp_ctrl_{}'.format(wrist_name), 'ctrl_{}'.format(elbow_name))

createFkArmCtrl('fk_shoulder', 'fk_elbow', 'fk_wrist')
