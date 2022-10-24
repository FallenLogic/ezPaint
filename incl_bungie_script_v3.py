import bpy

swtor = True
bungie_smalldef = False
jka = False

swtor_name_list = [
    # old vertex group name - new vertex group name
    ['Root', 'ValveBiped.Bip01_Pelvis'],
    ['RootSpine', 'ValveBiped.Bip01_Pelvis'],
    ['Pelvis','ValveBiped.Bip01_Pelvis'],
    ['LowerBack','ValveBiped.Bip01_Spine'],
    ['Chest','ValveBiped.Bip01_Spine1'],
    ['Chest1','ValveBiped.Bip01_Spine2'],
    ['Chest2', 'ValveBiped.Bip01_Spine4'],
    
    ['LeftCollar', 'ValveBiped.Bip01_L_Clavicle'],

    ['lshoulder', 'ValveBiped.Bip01_L_UpperArm'],
    ['lforearm', 'ValveBiped.Bip01_L_Forearm'],
    
    ['LeftWrist', 'ValveBiped.Bip01_L_Hand'],
    ['LeftThumbFinger', 'ValveBiped.Bip01_L_Finger0'], # l-thumb
    ['LeftThumbFinger1', 'ValveBiped.Bip01_L_Finger01'],
    ['LeftThumbFinger2', 'ValveBiped.Bip01_L_Finger02'], # end l-thumb
    ['LeftIndexFinger', 'ValveBiped.Bip01_L_Finger1'], # l-index
    ['LeftIndexFinger1', 'ValveBiped.Bip01_L_Finger11'],
    ['LeftIndexFinger2', 'ValveBiped.Bip01_L_Finger12'], # end l-index
    ['LeftMiddleFinger', 'ValveBiped.Bip01_L_Finger2'], # l-hand remainder
    ['LeftMiddleFinger1', 'ValveBiped.Bip01_L_Finger21'],
    ['LeftMiddleFinger2', 'ValveBiped.Bip01_L_Finger22'],
    ['LeftRingFinger', 'ValveBiped.Bip01_L_Finger3'], 
    ['LeftRingFinger1', 'ValveBiped.Bip01_L_Finger31'],
    ['LeftRingFinger2', 'ValveBiped.Bip01_L_Finger32'],  
    ['LeftPinkFinger', 'ValveBiped.Bip01_L_Finger4'], 
    ['LeftPinkFinger1', 'ValveBiped.Bip01_L_Finger41'],
    ['LeftPinkFinger2', 'ValveBiped.Bip01_L_Finger42'], 
#   end l-hand remainder
    ['RightCollar', 'ValveBiped.Bip01_R_Clavicle'],
    
    ['rshoulder', 'ValveBiped.Bip01_R_UpperArm'],
    ['rforearm', 'ValveBiped.Bip01_R_Forearm'],

    ['RightWrist', 'ValveBiped.Bip01_R_Hand'],
    ['RightThumbFinger', 'ValveBiped.Bip01_R_Finger0'], # r-thumb
    ['RightThumbFinger1', 'ValveBiped.Bip01_R_Finger01'],
    ['RightThumbFinger2', 'ValveBiped.Bip01_R_Finger02'], # end r-thumb
    ['RightIndexFinger', 'ValveBiped.Bip01_R_Finger1'], # r-index
    ['RightIndexFinger1', 'ValveBiped.Bip01_R_Finger11'],
    ['RightIndexFinger2', 'ValveBiped.Bip01_R_Finger12'], # end r-index
    ['RightMiddleFinger', 'ValveBiped.Bip01_R_Finger2'], # r-hand remainder
    ['RightMiddleFinger1', 'ValveBiped.Bip01_R_Finger21'],
    ['RightMiddleFinger2', 'ValveBiped.Bip01_R_Finger22'],
    ['RightRingFinger', 'ValveBiped.Bip01_R_Finger3'], 
    ['RightRingFinger1', 'ValveBiped.Bip01_R_Finger31'],
    ['RightRingFinger2', 'ValveBiped.Bip01_R_Finger32'],  
    ['RightPinkFinger', 'ValveBiped.Bip01_R_Finger4'], 
    ['RightPinkFinger1', 'ValveBiped.Bip01_R_Finger41'],
    ['RightPinkFinger2', 'ValveBiped.Bip01_R_Finger42'], 

    ['Neck', 'ValveBiped.Bip01_Neck1'],
    
    ['lhip', 'ValveBiped.Bip01_L_Thigh'],
    ['LeftKnee', 'ValveBiped.Bip01_L_Calf'],
    ['LeftAnkle', 'ValveBiped.Bip01_L_Foot'],
    ['LeftToe', 'ValveBiped.Bip01_L_Toe0'],
    
    ['rhip', 'ValveBiped.Bip01_R_Thigh'],
    ['RightKnee', 'ValveBiped.Bip01_R_Calf'],
    ['RightAnkle', 'ValveBiped.Bip01_R_Foot'],
    ['RightToe', 'ValveBiped.Bip01_R_Toe0'],
    ['Skirt1', 'ValveBiped.Bip01_Pelvis'],
    ['Skirt2', 'ValveBiped.Cod'],
    ['headgroup', 'ValveBiped.Bip01_Head1'],
#    think this is leftover, test later
    ['', 'ValveBiped.Bip01_Pelvis']
]

jka_name_list = [
    # old name - new name
    ['pelvis','ValveBiped.Bip01_Pelvis'],
    ['lower_lumbar','ValveBiped.Bip01_Spine'],
    ['upper_lumbar','ValveBiped.Bip01_Spine1'],
    ['thoracic','ValveBiped.Bip01_Spine2'],
#    recheck this one
    ['thoracic', 'ValveBiped.Bip01_Spine4'],
    ['lclavical', 'ValveBiped.Bip01_L_Clavicle'],
    ['lupper', 'ValveBiped.Bip01_L_UpperArm'],
    ['lfore', 'ValveBiped.Bip01_L_Forearm'],
    ['lhand', 'ValveBiped.Bip01_L_Hand'],
    # JK:JA uses only two joints per digit  
    ['l_d1_j1', 'ValveBiped.Bip01_L_Finger0'], # l-thumb
    ['l_d1_j2', 'ValveBiped.Bip01_L_Finger01'],
    ['', 'ValveBiped.Bip01_L_Finger02'], # end l-thumb
    ['l_d2_j1', 'ValveBiped.Bip01_L_Finger1'], # l-index
    ['l_d2_j2', 'ValveBiped.Bip01_L_Finger11'],
    ['', 'ValveBiped.Bip01_L_Finger12'], # end l-index
    ['l_d4_j1', 'ValveBiped.Bip01_L_Finger2'], # l-hand remainder
    ['l_d4_j2', 'ValveBiped.Bip01_L_Finger21'],
    ['', 'ValveBiped.Bip01_L_Finger22'], # end l-hand remainder
    ['rclavical', 'ValveBiped.Bip01_R_Clavicle'],
    ['rupper', 'ValveBiped.Bip01_R_UpperArm'],
    ['rfore', 'ValveBiped.Bip01_R_Forearm'],
    ['rhand', 'ValveBiped.Bip01_R_Hand'],
    ['r_d1_j1', 'ValveBiped.Bip01_R_Finger0'], # r-thumb
    ['r_d1_j2', 'ValveBiped.Bip01_R_Finger01'],
    ['', 'ValveBiped.Bip01_R_Finger02'], # end r-thumb
    ['r_d2_j1', 'ValveBiped.Bip01_R_Finger1'], # r-index
    ['r_d2_j2', 'ValveBiped.Bip01_R_Finger11'],
    ['', 'ValveBiped.Bip01_R_Finger12'], # end r-index
    ['r_d4_j1', 'ValveBiped.Bip01_R_Finger2'], # r-hand remainder
    ['r_d4_j2', 'ValveBiped.Bip01_R_Finger21'],
    ['', 'ValveBiped.Bip01_R_Finger22'], # r-hand remainder end
    ['cervical', 'ValveBiped.Bip01_Neck1'],
    ['lthigh', 'ValveBiped.Bip01_L_Thigh'],
    ['ltail', 'ValveBiped.Bip01_L_Thigh'],
    ['ltibia', 'ValveBiped.Bip01_L_Calf'],
    ['ltalus', 'ValveBiped.Bip01_L_Foot'],
#    no toes for our JKA friends!
    ['', 'ValveBiped.Bip01_L_Toe0'],
    ['rthigh', 'ValveBiped.Bip01_R_Thigh'],
    ['rtibia', 'ValveBiped.Bip01_R_Calf'],
    ['rtalus', 'ValveBiped.Bip01_R_Foot'],
#    no toes for our JKA friends!
    ['', 'ValveBiped.Bip01_R_Toe0'],
    ['Motion', 'ValveBiped.Bip01_Pelvis'],
#    misc head/facial animation bones that aren't present on ValveBiped
    ['jka_headgroup', 'ValveBiped.Bip01_Head1']
]

bungie_sm_name_list = [
    # old vertex group name - new vertex group name
    ['Pelvis','ValveBiped.Bip01_Pelvis'],
    ['Spine_1','ValveBiped.Bip01_Spine'],
#    group vbp spine 1 and spine 2
    ['Spine_2','ValveBiped.Bip01_Spine2'],
    ['Spine_3', 'ValveBiped.Bip01_Spine4'],
    
    ['Clav.L', 'ValveBiped.Bip01_L_Clavicle'],

    ['UpperArm.L', 'ValveBiped.Bip01_L_UpperArm'],
    ['ForeArm.L', 'ValveBiped.Bip01_L_Forearm'],
    
    ['bg_handlgroup', 'ValveBiped.Bip01_L_Hand'],
    
    ['Thumb_1.L', 'ValveBiped.Bip01_L_Finger0'], # l-thumb
    ['Thumb_2.L', 'ValveBiped.Bip01_L_Finger01'],
    ['Thumb_3.L', 'ValveBiped.Bip01_L_Finger02'], # end l-thumb
    ['Index_1.L', 'ValveBiped.Bip01_L_Finger1'], # l-index
    ['Index_2.L', 'ValveBiped.Bip01_L_Finger11'],
    ['Index_3.L', 'ValveBiped.Bip01_L_Finger12'], # end l-index
    ['Middle_1.L', 'ValveBiped.Bip01_L_Finger2'], # l-hand remainder
    ['Middle_2.L', 'ValveBiped.Bip01_L_Finger21'],
    ['Middle_3.L', 'ValveBiped.Bip01_L_Finger22'],
    ['Ring_1.L', 'ValveBiped.Bip01_L_Finger3'], 
    ['Ring_2.L', 'ValveBiped.Bip01_L_Finger31'],
    ['Ring_3.L', 'ValveBiped.Bip01_L_Finger32'],  
    ['Pinky_1.L', 'ValveBiped.Bip01_L_Finger4'], 
    ['Pinky_2.L', 'ValveBiped.Bip01_L_Finger41'],
    ['Pinky_3.L', 'ValveBiped.Bip01_L_Finger42'], 
#   end l-hand remainder
    ['Clav.R', 'ValveBiped.Bip01_R_Clavicle'],
    
    ['UpperArm.R', 'ValveBiped.Bip01_R_UpperArm'],
    ['ForeArm.R', 'ValveBiped.Bip01_R_Forearm'],

    ['bg_handrgroup', 'ValveBiped.Bip01_R_Hand'],
    
    ['Thumb_1.R', 'ValveBiped.Bip01_R_Finger0'], # r-thumb
    ['Thumb_2.R', 'ValveBiped.Bip01_R_Finger01'],
    ['Thumb_3.R', 'ValveBiped.Bip01_R_Finger02'], # end r-thumb
    ['Index_1.R', 'ValveBiped.Bip01_R_Finger1'], # r-index
    ['Index_2.R', 'ValveBiped.Bip01_R_Finger11'],
    ['Index_3.R', 'ValveBiped.Bip01_R_Finger12'], # end r-index
    ['Middle_1.R', 'ValveBiped.Bip01_R_Finger2'], # r-hand remainder
    ['Middle_2.R', 'ValveBiped.Bip01_R_Finger21'],
    ['Middle_3.R', 'ValveBiped.Bip01_R_Finger22'],
    ['Ring_1.R', 'ValveBiped.Bip01_R_Finger3'], 
    ['Ring_2.R', 'ValveBiped.Bip01_R_Finger31'],
    ['Ring_3.R', 'ValveBiped.Bip01_R_Finger32'],  
    ['Pinky_1.R', 'ValveBiped.Bip01_R_Finger4'], 
    ['Pinky_2.R', 'ValveBiped.Bip01_R_Finger41'],
    ['Pinky_3.R', 'ValveBiped.Bip01_R_Finger42'], 

    ['Neck_1', 'ValveBiped.Bip01_Neck1'],
    
    ['Thigh.L', 'ValveBiped.Bip01_L_Thigh'],
    ['Calf.L', 'ValveBiped.Bip01_L_Calf'],
    ['Foot.L', 'ValveBiped.Bip01_L_Foot'],
    ['Toe.L', 'ValveBiped.Bip01_L_Toe0'],
    
    ['Thigh.R', 'ValveBiped.Bip01_R_Thigh'],
    ['Calf.R', 'ValveBiped.Bip01_R_Calf'],
    ['Foot.R', 'ValveBiped.Bip01_R_Foot'],
    ['Toe.R', 'ValveBiped.Bip01_R_Toe0'],
    
    ['bg_headgroup', 'ValveBiped.Bip01_Head1'],
#    think this is leftover, test later
    ['', 'ValveBiped.Bip01_Pelvis']
]

act_obj = bpy.context.active_object
v_groups = act_obj.vertex_groups

def merge_groups(group_input, final_name, act_obj):
    

    group_lookup = {g.index: g.name for g in v_groups}
    group_candidates = {n for n in group_lookup.values() if n in group_input}

    # test whether all candidates are components of group_lookup
    if all(n in group_lookup.values() for n in group_candidates):
        pass

    # general tests
    if (len(group_candidates) and act_obj.type == 'MESH' and
        bpy.context.mode == 'OBJECT'):
        
        # iterate through the vertices and sum the weights per group
        vertex_weights = {}
        for vert in act_obj.data.vertices:
            if len(vert.groups):  
                for item in vert.groups:
                    vg = act_obj.vertex_groups[item.group]
                    if vg.name in group_candidates:
                        if vert.index in vertex_weights:    
                            vertex_weights[vert.index] += vg.weight(vert.index)
                        else:
                            vertex_weights[vert.index] = vg.weight(vert.index)
        # clamp/slice values above 1.0
        for key in vertex_weights.keys():
            if (vertex_weights[key] > 1.0): vertex_weights[key] = 1.0
#            if (vertex_weights[key] < 0.3): vertex_weights[key] = 0.0
        # create new vertex group
        vgroup = act_obj.vertex_groups.new(name=final_name) 
            
        # add the values to the group                       
        for key, value in vertex_weights.items():
            vgroup.add([key], value ,'REPLACE') #'ADD','SUBTRACT', 'REPLACE'

#       cleans up duplicates, adapted from https://blender.stackexchange.com/questions/134587/
        vgs = [vg for vg in act_obj.vertex_groups if vg.name in group_input]
        while(vgs):
            act_obj.vertex_groups.remove(vgs.pop())

def swtor_fixups(act_obj):
#    act_obj.scale=(330,330,330)
    
#    act_obj.parent = bms_armature
    skeleton = act_obj.modifiers.new(name="Armature", type='ARMATURE')
    skelobj = bpy.data.objects["bfb_armature"]
    
    if(act_obj.name[:3] == "bms"):
        skelobj = bpy.data.objects["bms_armature"]
    if(act_obj.name[:3] == "bmf"):
        skelobj = bpy.data.objects["bmf_armature"]
    if(act_obj.name[:3] == "bmn"):
        skelobj = bpy.data.objects["bmn_armature"]
    if(act_obj.name[:3] == "bma"):
        skelobj = bpy.data.objects["bma_armature"]
    if(act_obj.name[:3] == "bfn"):
        skelobj = bpy.data.objects["bfn_armature"]
    if(act_obj.name[:3] == "bfs"):
        skelobj = bpy.data.objects["bfs_armature"]
    
    skeleton.object = skelobj
    skelobj.hide_set(False)
    
    swtor_fc_bones = {'fc_jaw',
    'fc_lip_left_bottom',
    'fc_lip_center_bottom',
    'fc_lip_right_bottom',
    'fc_lip_right_corner',
    'fc_lip_left_corner',
    'fc_lip_left_top',
    'fc_lip_center_top',
    'fc_lip_right_top',
    'fc_tongue',
    'fc_puffer_left',
    'fc_puffer_right',
    'fc_nose_left',
    'fc_nose_right', 
    'fc_cheek_inner_right',
    'fc_cheek_inner_left',
    'fc_cheek_left', 
    'fc_cheek_right',
    'fc_lid_right_bottom',
    'fc_lid_left_bottom',
    'fc_eye_left',
    'fc_eye_right',
    'fc_lid_left_top',
    'fc_lid_right_top',
    'fc_brow_left_2',
    'fc_brow_left_1',
    'fc_brow_mid',
    'fc_brow_right_1',
    'fc_brow_right_2',
    'Head',
    'Neck1'}

    swtor_forearm_bones_right = {'RightUlna', 'RightElbow'}
    swtor_forearm_bones_left = {'LeftUlna', 'LeftElbow'}

    swtor_upperarm_bones_right = {'RightShoulder', 'RightShoulderTwist1', 'RightBlendShoulder'}
    swtor_upperarm_bones_left = {'LeftShoulder', 'LeftShoulderTwist1', 'LeftBlendShoulder'}

    swtor_hip_left = {'LeftHip','LeftHipTwist1'}
    swtor_hip_right = {'RightHip','RightHipTwist1'}

    merge_groups(swtor_fc_bones, "headgroup", act_obj)

    merge_groups(swtor_forearm_bones_right, "rforearm", act_obj)
    merge_groups(swtor_forearm_bones_left, "lforearm", act_obj)

    merge_groups(swtor_upperarm_bones_left, "lshoulder", act_obj)
    merge_groups(swtor_upperarm_bones_right, "rshoulder", act_obj)

    merge_groups(swtor_hip_left, "lhip", act_obj)
    merge_groups(swtor_hip_right, "rhip", act_obj)
    # this prevents duplicate material names, which Source does not support
    if(act_obj.active_material.name == "default"):
        new_mat = act_obj.active_material.copy()
        act_obj.active_material = new_mat
        new_mat.name = act_obj.name + "_v01"


def jka_fixups(act_obj):
    act_obj.scale=(11,11,11)
    jka_humerus_l_group = {"lhumerus", "lhumerusX"}
    jka_humerus_r_group = {"rhumerus", "rhumerusX"}

    jka_radius_l_group = {"lradius", "lradiusX"}
    jka_radius_r_group = {"rradius", "rradiusX"}
    
    jka_thigh_l_group = {"ltail", "lfemurYZ", "lfemurX"}
    jka_thigh_r_group = {"rtail", "rfemurYZ", "rfemurX"}
    
    jka_fc_group = {"face","cranium","jaw","ceyebrow","lblip2","leye","rblip2","ltlip2","rtlip2","reye"}
    
    merge_groups(jka_humerus_l_group, "lupper", act_obj)
    merge_groups(jka_humerus_r_group, "rupper", act_obj)
    merge_groups(jka_radius_l_group, "lfore", act_obj)
    merge_groups(jka_radius_r_group, "rfore", act_obj)
    merge_groups(jka_thigh_l_group, "lthigh", act_obj)
    merge_groups(jka_thigh_r_group, "rthigh", act_obj)
    merge_groups(jka_fc_group, "jka_headgroup", act_obj)
    
    for m in act_obj.material_slots:
        new_mat = m.material.copy()
        m.material = new_mat
        new_mat.name = new_mat.name[15:-8]

    
def bungie_smalldef_fixups(act_obj):
    act_obj.scale=(38,38,38)
    # Bungie group merges
    bungie_fc_bones = {'Cheekbone.L',
    'UpperEyelid.L', 'LowerEyelid.L', 'LowerEyelid.L', 'Nostril_.L', 'UpperLip_4', 'UpperLip_5', 'NasalLobe.L',
    'Nostril_2.L', 'Cheek.R', 'Cheek.L', 'Jawline_1.R', 'Jawline_1.L', 'Nose', '', 'UnderEye.R', 'Cheekbone.R','LowerEyelid.R',
    'Nostril_1.R', 'UpperEyelid.R', 'UpperLip_2', 'UpperLip_1', 'NasalLobe.R', 'Nostril_2.R', 'Chin', 'LowerLip_3',
    'LowerLip_4', 'LowerLip_5', 'Jawline_2.L', 'LowerLip_2', 'LowerLip_1', 'Jawline_2.R', 'Neck_2', 'Jaw', 'Head', 
    'Tongue', 'Brow_2.R', 'Brow_2.L', 'Brow_3.R', 'Brow_3.L', 'Brow_1.L', 'Brow_1.R', 'UnderEye.L', 'UpperLip_3', 'Jawline_.L'}

    bungie_hand_l_groups = {'Wrist_Twist_Fixup.L', 'Hand.L'}
    bungie_hand_r_groups = {'Wrist_Twist_Fixup.R', 'Hand.R'}


    merge_groups(bungie_fc_bones, "bg_headgroup", act_obj)
    merge_groups(bungie_hand_l_groups, "bg_handlgroup", act_obj)
    merge_groups(bungie_hand_r_groups, "bg_handrgroup", act_obj)

def reweight(v_groups, name_list):
    for n in name_list:
            if n[0] in v_groups:
                v_groups[n[0]].name = n[1]

if swtor == True:
    swtor_fixups(act_obj)
    reweight(v_groups, swtor_name_list)
elif jka == True:
    jka_fixups(act_obj)
    reweight(v_groups, jka_name_list)
elif bungie_smalldef == True:
    bungie_smalldef_fixups(act_obj)
    reweight(v_groups, bungie_name_list)