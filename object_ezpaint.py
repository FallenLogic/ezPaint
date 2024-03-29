# ----------------
# ezPaint Blender add-on
# Created by FallenLogic & NadaYukie
# ----------------
import bpy
import math
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import PropertyGroup

bl_info = {
    "name": "ezPaint",
    "description": "Automatically weightpaint models from a variety of games for use with the Source Engine",
    "author": "FallenLogic (original author), NadaYukie (adding support for many games)",
    "version": (0, 18),
    "blender": (2, 80, 0),
    "location": "Search Menu (Object Mode) | ezPaint",
    "warning": "Requires other addons to import and export models (see documentation)",
    "wiki_url": "https://github.com/FallenLogic/ezPaint",
    "tracker_url": "https://github.com/FallenLogic/ezPaint/issues",
    "category": "Object",
}

swtor_name_list = [
    # old vertex group name - new vertex group name
    ["Root", "ValveBiped.Bip01_Pelvis"],
    ["RootSpine", "ValveBiped.Bip01_Pelvis"],
    ["Pelvis", "ValveBiped.Bip01_Pelvis"],
    ["LowerBack", "ValveBiped.Bip01_Spine"],
    ["Chest", "ValveBiped.Bip01_Spine1"],
    ["Chest1", "ValveBiped.Bip01_Spine2"],
    ["Chest2", "ValveBiped.Bip01_Spine4"],
    ["LeftCollar", "ValveBiped.Bip01_L_Clavicle"],
    ["lshoulder", "ValveBiped.Bip01_L_UpperArm"],
    ["lforearm", "ValveBiped.Bip01_L_Forearm"],
    ["LeftWrist", "ValveBiped.Bip01_L_Hand"],
    ["LeftThumbFinger", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["LeftThumbFinger1", "ValveBiped.Bip01_L_Finger01"],
    ["LeftThumbFinger2", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["LeftIndexFinger", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["LeftIndexFinger1", "ValveBiped.Bip01_L_Finger11"],
    ["LeftIndexFinger2", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["LeftMiddleFinger", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["LeftMiddleFinger1", "ValveBiped.Bip01_L_Finger21"],
    ["LeftMiddleFinger2", "ValveBiped.Bip01_L_Finger22"],
    ["LeftRingFinger", "ValveBiped.Bip01_L_Finger3"],
    ["LeftRingFinger1", "ValveBiped.Bip01_L_Finger31"],
    ["LeftRingFinger2", "ValveBiped.Bip01_L_Finger32"],
    ["LeftPinkFinger", "ValveBiped.Bip01_L_Finger4"],
    ["LeftPinkFinger1", "ValveBiped.Bip01_L_Finger41"],
    ["LeftPinkFinger2", "ValveBiped.Bip01_L_Finger42"],
    #   end l-hand remainder
    ["RightCollar", "ValveBiped.Bip01_R_Clavicle"],
    ["rshoulder", "ValveBiped.Bip01_R_UpperArm"],
    ["rforearm", "ValveBiped.Bip01_R_Forearm"],
    ["RightWrist", "ValveBiped.Bip01_R_Hand"],
    ["RightThumbFinger", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["RightThumbFinger1", "ValveBiped.Bip01_R_Finger01"],
    ["RightThumbFinger2", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["RightIndexFinger", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["RightIndexFinger1", "ValveBiped.Bip01_R_Finger11"],
    ["RightIndexFinger2", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["RightMiddleFinger", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["RightMiddleFinger1", "ValveBiped.Bip01_R_Finger21"],
    ["RightMiddleFinger2", "ValveBiped.Bip01_R_Finger22"],
    ["RightRingFinger", "ValveBiped.Bip01_R_Finger3"],
    ["RightRingFinger1", "ValveBiped.Bip01_R_Finger31"],
    ["RightRingFinger2", "ValveBiped.Bip01_R_Finger32"],
    ["RightPinkFinger", "ValveBiped.Bip01_R_Finger4"],
    ["RightPinkFinger1", "ValveBiped.Bip01_R_Finger41"],
    ["RightPinkFinger2", "ValveBiped.Bip01_R_Finger42"],
    ["Neck", "ValveBiped.Bip01_Neck1"],
    ["lhip", "ValveBiped.Bip01_L_Thigh"],
    ["LeftKnee", "ValveBiped.Bip01_L_Calf"],
    ["LeftAnkle", "ValveBiped.Bip01_L_Foot"],
    ["LeftToe", "ValveBiped.Bip01_L_Toe0"],
    ["rhip", "ValveBiped.Bip01_R_Thigh"],
    ["RightKnee", "ValveBiped.Bip01_R_Calf"],
    ["RightAnkle", "ValveBiped.Bip01_R_Foot"],
    ["RightToe", "ValveBiped.Bip01_R_Toe0"],
    ["Skirt1", "ValveBiped.Bip01_Pelvis"],
    ["Skirt2", "ValveBiped.Cod"],
    ["headgroup", "ValveBiped.Bip01_Head1"],
    #    think this is leftover, test later
    ["", "ValveBiped.Bip01_Pelvis"],
]

jka_name_list = [
    # old name - new name
    ["pelvis", "ValveBiped.Bip01_Pelvis"],
    ["lower_lumbar", "ValveBiped.Bip01_Spine"],
    ["upper_lumbar", "ValveBiped.Bip01_Spine1"],
    ["thoracic", "ValveBiped.Bip01_Spine2"],
    #    recheck this one
    ["thoracic", "ValveBiped.Bip01_Spine4"],
    ["lclavical", "ValveBiped.Bip01_L_Clavicle"],
    ["lupper", "ValveBiped.Bip01_L_UpperArm"],
    ["lfore", "ValveBiped.Bip01_L_Forearm"],
    ["lhand", "ValveBiped.Bip01_L_Hand"],
    # JK:JA uses only two joints per digit
    ["l_d1_j1", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["l_d1_j2", "ValveBiped.Bip01_L_Finger01"],
    ["", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["l_d2_j1", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["l_d2_j2", "ValveBiped.Bip01_L_Finger11"],
    ["", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["l_d4_j1", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["l_d4_j2", "ValveBiped.Bip01_L_Finger21"],
    ["", "ValveBiped.Bip01_L_Finger22"],  # end l-hand remainder
    ["rclavical", "ValveBiped.Bip01_R_Clavicle"],
    ["rupper", "ValveBiped.Bip01_R_UpperArm"],
    ["rfore", "ValveBiped.Bip01_R_Forearm"],
    ["rhand", "ValveBiped.Bip01_R_Hand"],
    ["r_d1_j1", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["r_d1_j2", "ValveBiped.Bip01_R_Finger01"],
    ["", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["r_d2_j1", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["r_d2_j2", "ValveBiped.Bip01_R_Finger11"],
    ["", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["r_d4_j1", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["r_d4_j2", "ValveBiped.Bip01_R_Finger21"],
    ["", "ValveBiped.Bip01_R_Finger22"],  # r-hand remainder end
    ["cervical", "ValveBiped.Bip01_Neck1"],
    ["lthigh", "ValveBiped.Bip01_L_Thigh"],
    ["ltail", "ValveBiped.Bip01_L_Thigh"],
    ["ltibia", "ValveBiped.Bip01_L_Calf"],
    ["ltalus", "ValveBiped.Bip01_L_Foot"],
    #    no toes for our JKA friends!
    ["", "ValveBiped.Bip01_L_Toe0"],
    ["rthigh", "ValveBiped.Bip01_R_Thigh"],
    ["rtibia", "ValveBiped.Bip01_R_Calf"],
    ["rtalus", "ValveBiped.Bip01_R_Foot"],
    #    no toes for our JKA friends!
    ["", "ValveBiped.Bip01_R_Toe0"],
    ["Motion", "ValveBiped.Bip01_Pelvis"],
    #    misc head/facial animation bones that aren't present on ValveBiped
    ["jka_headgroup", "ValveBiped.Bip01_Head1"],
]

bungie_sm_name_list = [
    # old vertex group name - new vertex group name
    ["Pelvis", "ValveBiped.Bip01_Pelvis"],
    ["Spine_1", "ValveBiped.Bip01_Spine"],
    #    group vbp spine 1 and spine 2
    ["Spine_2", "ValveBiped.Bip01_Spine2"],
    ["Spine_3", "ValveBiped.Bip01_Spine4"],
    ["Clav.L", "ValveBiped.Bip01_L_Clavicle"],
    ["UpperArm.L", "ValveBiped.Bip01_L_UpperArm"],
    ["ForeArm.L", "ValveBiped.Bip01_L_Forearm"],
    ["bg_handlgroup", "ValveBiped.Bip01_L_Hand"],
    ["Thumb_1.L", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["Thumb_2.L", "ValveBiped.Bip01_L_Finger01"],
    ["Thumb_3.L", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["Index_1.L", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["Index_2.L", "ValveBiped.Bip01_L_Finger11"],
    ["Index_3.L", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["Middle_1.L", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["Middle_2.L", "ValveBiped.Bip01_L_Finger21"],
    ["Middle_3.L", "ValveBiped.Bip01_L_Finger22"],
    ["Ring_1.L", "ValveBiped.Bip01_L_Finger3"],
    ["Ring_2.L", "ValveBiped.Bip01_L_Finger31"],
    ["Ring_3.L", "ValveBiped.Bip01_L_Finger32"],
    ["Pinky_1.L", "ValveBiped.Bip01_L_Finger4"],
    ["Pinky_2.L", "ValveBiped.Bip01_L_Finger41"],
    ["Pinky_3.L", "ValveBiped.Bip01_L_Finger42"],
    #   end l-hand remainder
    ["Clav.R", "ValveBiped.Bip01_R_Clavicle"],
    ["UpperArm.R", "ValveBiped.Bip01_R_UpperArm"],
    ["ForeArm.R", "ValveBiped.Bip01_R_Forearm"],
    ["bg_handrgroup", "ValveBiped.Bip01_R_Hand"],
    ["Thumb_1.R", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["Thumb_2.R", "ValveBiped.Bip01_R_Finger01"],
    ["Thumb_3.R", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["Index_1.R", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["Index_2.R", "ValveBiped.Bip01_R_Finger11"],
    ["Index_3.R", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["Middle_1.R", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["Middle_2.R", "ValveBiped.Bip01_R_Finger21"],
    ["Middle_3.R", "ValveBiped.Bip01_R_Finger22"],
    ["Ring_1.R", "ValveBiped.Bip01_R_Finger3"],
    ["Ring_2.R", "ValveBiped.Bip01_R_Finger31"],
    ["Ring_3.R", "ValveBiped.Bip01_R_Finger32"],
    ["Pinky_1.R", "ValveBiped.Bip01_R_Finger4"],
    ["Pinky_2.R", "ValveBiped.Bip01_R_Finger41"],
    ["Pinky_3.R", "ValveBiped.Bip01_R_Finger42"],
    ["Neck_1", "ValveBiped.Bip01_Neck1"],
    ["Thigh.L", "ValveBiped.Bip01_L_Thigh"],
    ["Calf.L", "ValveBiped.Bip01_L_Calf"],
    ["Foot.L", "ValveBiped.Bip01_L_Foot"],
    ["Toe.L", "ValveBiped.Bip01_L_Toe0"],
    ["Thigh.R", "ValveBiped.Bip01_R_Thigh"],
    ["Calf.R", "ValveBiped.Bip01_R_Calf"],
    ["Foot.R", "ValveBiped.Bip01_R_Foot"],
    ["Toe.R", "ValveBiped.Bip01_R_Toe0"],
    ["bg_headgroup", "ValveBiped.Bip01_Head1"],
    #    think this is leftover, test later
    ["", "ValveBiped.Bip01_Pelvis"],
]

swjs_name_list = [
    ["Root", "ValveBiped.Bip01_Pelvis"],
    ["RootSpine", "ValveBiped.Bip01_Pelvis"],
    ["pelivsgroup", "ValveBiped.Bip01_Pelvis"],
    ["spineA", "ValveBiped.Bip01_Spine"],
    ["spineB", "ValveBiped.Bip01_Spine1"],
    ["spine2group", "ValveBiped.Bip01_Spine2"],
    ["neckagroup", "ValveBiped.Bip01_Spine4"],
    ["lclav", "ValveBiped.Bip01_L_Clavicle"],
    ["lshoulder", "ValveBiped.Bip01_L_UpperArm"],
    ["lforearm", "ValveBiped.Bip01_L_Forearm"],
    ["lhand", "ValveBiped.Bip01_L_Hand"],
    ["l_finThumbA", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["l_finThumbB", "ValveBiped.Bip01_L_Finger01"],
    ["l_finThumbC", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["l_finIndexA", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["l_finIndexB", "ValveBiped.Bip01_L_Finger11"],
    ["l_finIndexC", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["l_finMidA", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["l_finMidB", "ValveBiped.Bip01_L_Finger21"],
    ["l_finMidC", "ValveBiped.Bip01_L_Finger22"],
    ["l_finRingA", "ValveBiped.Bip01_L_Finger3"],
    ["l_finRingB", "ValveBiped.Bip01_L_Finger31"],
    ["l_finRingC", "ValveBiped.Bip01_L_Finger32"],
    ["l_finPinkyA", "ValveBiped.Bip01_L_Finger4"],
    ["l_finPinkyB", "ValveBiped.Bip01_L_Finger41"],
    ["l_finPinkyC", "ValveBiped.Bip01_L_Finger42"],
    #   end l-hand remainder
    ["r_clav", "ValveBiped.Bip01_R_Clavicle"],
    ["rshoulder", "ValveBiped.Bip01_R_UpperArm"],
    ["rforearm", "ValveBiped.Bip01_R_Forearm"],
    ["rhand", "ValveBiped.Bip01_R_Hand"],
    ["r_finThumbA", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["r_finThumbB", "ValveBiped.Bip01_R_Finger01"],
    ["r_finThumbC", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["r_finIndexA", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["r_finIndexB", "ValveBiped.Bip01_R_Finger11"],
    ["r_finIndexC", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["r_finMidA", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["r_finMidB", "ValveBiped.Bip01_R_Finger21"],
    ["r_finMidC", "ValveBiped.Bip01_R_Finger22"],
    ["r_finRingA", "ValveBiped.Bip01_R_Finger3"],
    ["r_finRingB", "ValveBiped.Bip01_R_Finger31"],
    ["r_finRingC", "ValveBiped.Bip01_R_Finger32"],
    ["r_finPinkyA", "ValveBiped.Bip01_R_Finger4"],
    ["r_finPinkyB", "ValveBiped.Bip01_R_Finger41"],
    ["r_finPinkyC", "ValveBiped.Bip01_R_Finger42"],
    ["neckbgroup", "ValveBiped.Bip01_Neck1"],
    ["lhip", "ValveBiped.Bip01_L_Thigh"],
    ["lcalf", "ValveBiped.Bip01_L_Calf"],
    ["l_ankle", "ValveBiped.Bip01_L_Foot"],
    ["ltoe", "ValveBiped.Bip01_L_Toe0"],
    ["rhip", "ValveBiped.Bip01_R_Thigh"],
    ["rcalf", "ValveBiped.Bip01_R_Calf"],
    ["r_ankle", "ValveBiped.Bip01_R_Foot"],
    ["rtoe", "ValveBiped.Bip01_R_Toe0"],
    ["Skirt1", "ValveBiped.Bip01_Pelvis"],
    ["Skirt2", "ValveBiped.Cod"],
    ["headgroup", "ValveBiped.Bip01_Head1"],
    #    think this is leftover, test later
    ["", "ValveBiped.Bip01_Pelvis"],
]

swbf_name_list = [
    ["Root", "ValveBiped.Bip01_Pelvis"],
    ["RootSpine", "ValveBiped.Bip01_Pelvis"],
    ["pelivsgroup", "ValveBiped.Bip01_Pelvis"],
    ["spinegroup", "ValveBiped.Bip01_Spine"],
    ["spine1group", "ValveBiped.Bip01_Spine1"],
    ["spine2group", "ValveBiped.Bip01_Spine2"],
    ["neckagroup", "ValveBiped.Bip01_Spine4"],
    ["LeftShoulder", "ValveBiped.Bip01_L_Clavicle"],
    ["lshoulder", "ValveBiped.Bip01_L_UpperArm"],
    ["lforearm", "ValveBiped.Bip01_L_Forearm"],
    ["lhand", "ValveBiped.Bip01_L_Hand"],
    ["LeftHandThumb2", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["LeftHandThumb3", "ValveBiped.Bip01_L_Finger01"],
    ["LeftHandThumb4", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["LeftHandIndex1", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["LeftHandIndex2", "ValveBiped.Bip01_L_Finger11"],
    ["lindex", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["LeftHandMiddle1", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["LeftHandMiddle2", "ValveBiped.Bip01_L_Finger21"],
    ["LeftHandMiddle3", "ValveBiped.Bip01_L_Finger22"],
    ["LeftHandRing1", "ValveBiped.Bip01_L_Finger3"],
    ["LeftHandRing2", "ValveBiped.Bip01_L_Finger31"],
    ["LeftHandRing3", "ValveBiped.Bip01_L_Finger32"],
    ["LeftHandPinky1", "ValveBiped.Bip01_L_Finger4"],
    ["LeftHandPinky2", "ValveBiped.Bip01_L_Finger41"],
    ["LeftHandPinky3", "ValveBiped.Bip01_L_Finger42"],
    #   end l-hand remainder
    ["RightShoulder", "ValveBiped.Bip01_R_Clavicle"],
    ["rshoulder", "ValveBiped.Bip01_R_UpperArm"],
    ["rforearm", "ValveBiped.Bip01_R_Forearm"],
    ["rhand", "ValveBiped.Bip01_R_Hand"],
    ["RightHandThumb2", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["RightHandThumb3", "ValveBiped.Bip01_R_Finger01"],
    ["RightHandThumb4", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["RightHandIndex1", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["RightHandIndex2", "ValveBiped.Bip01_R_Finger11"],
    ["rindex", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["RightHandMiddle1", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["RightHandMiddle2", "ValveBiped.Bip01_R_Finger21"],
    ["RightHandMiddle3", "ValveBiped.Bip01_R_Finger22"],
    ["RightHandRing1", "ValveBiped.Bip01_R_Finger3"],
    ["RightHandRing2", "ValveBiped.Bip01_R_Finger31"],
    ["RightHandRing3", "ValveBiped.Bip01_R_Finger32"],
    ["RightHandPinky1", "ValveBiped.Bip01_R_Finger4"],
    ["RightHandPinky2", "ValveBiped.Bip01_R_Finger41"],
    ["RightHandPinky3", "ValveBiped.Bip01_R_Finger42"],
    ["neckbgroup", "ValveBiped.Bip01_Neck1"],
    ["lhip", "ValveBiped.Bip01_L_Thigh"],
    ["lcalf", "ValveBiped.Bip01_L_Calf"],
    ["LeftFoot", "ValveBiped.Bip01_L_Foot"],
    ["ltoe", "ValveBiped.Bip01_L_Toe0"],
    ["rhip", "ValveBiped.Bip01_R_Thigh"],
    ["rcalf", "ValveBiped.Bip01_R_Calf"],
    ["RightFoot", "ValveBiped.Bip01_R_Foot"],
    ["rtoe", "ValveBiped.Bip01_R_Toe0"],
    ["Skirt1", "ValveBiped.Bip01_Pelvis"],
    ["Skirt2", "ValveBiped.Cod"],
    ["headgroup", "ValveBiped.Bip01_Head1"],
    #    think this is leftover, test later
    ["", "ValveBiped.Bip01_Pelvis"],
]

fortnite_name_list = [
    ["Root", "ValveBiped.Bip01_Pelvis"],
    ["RootSpine", "ValveBiped.Bip01_Pelvis"],
    ["pelivsgroup", "ValveBiped.Bip01_Pelvis"],
    ["spinegroup", "ValveBiped.Bip01_Spine"],
    ["spine 2", "ValveBiped.Bip01_Spine1"],
    ["spine2group", "ValveBiped.Bip01_Spine2"],
    ["spine4group", "ValveBiped.Bip01_Spine4"],
    ["lclavicle", "ValveBiped.Bip01_L_Clavicle"],
    ["lshoulder", "ValveBiped.Bip01_L_UpperArm"],
    ["lforearm", "ValveBiped.Bip01_L_Forearm"],
    ["lhand", "ValveBiped.Bip01_L_Hand"],
    ["arm left finger 1a", "ValveBiped.Bip01_L_Finger0"],  # l-thumb
    ["arm left finger 1b", "ValveBiped.Bip01_L_Finger01"],
    ["arm left finger 1c", "ValveBiped.Bip01_L_Finger02"],  # end l-thumb
    ["arm left finger 2a", "ValveBiped.Bip01_L_Finger1"],  # l-index
    ["arm left finger 2b", "ValveBiped.Bip01_L_Finger11"],
    ["arm left finger 2c", "ValveBiped.Bip01_L_Finger12"],  # end l-index
    ["arm left finger 3a", "ValveBiped.Bip01_L_Finger2"],  # l-hand remainder
    ["arm left finger 3b", "ValveBiped.Bip01_L_Finger21"],
    ["arm left finger 3c", "ValveBiped.Bip01_L_Finger22"],
    ["arm left finger 4a", "ValveBiped.Bip01_L_Finger3"],
    ["arm left finger 4b", "ValveBiped.Bip01_L_Finger31"],
    ["arm left finger 4c", "ValveBiped.Bip01_L_Finger32"],
    ["arm left finger 5a", "ValveBiped.Bip01_L_Finger4"],
    ["arm left finger 5b", "ValveBiped.Bip01_L_Finger41"],
    ["arm left finger 5c", "ValveBiped.Bip01_L_Finger42"],
    #   end l-hand remainder
    ["rclavicle", "ValveBiped.Bip01_R_Clavicle"],
    ["rshoulder", "ValveBiped.Bip01_R_UpperArm"],
    ["rforearm", "ValveBiped.Bip01_R_Forearm"],
    ["rhand", "ValveBiped.Bip01_R_Hand"],
    ["arm right finger 1a", "ValveBiped.Bip01_R_Finger0"],  # r-thumb
    ["arm right finger 1b", "ValveBiped.Bip01_R_Finger01"],
    ["arm right finger 1c", "ValveBiped.Bip01_R_Finger02"],  # end r-thumb
    ["arm right finger 2a", "ValveBiped.Bip01_R_Finger1"],  # r-index
    ["arm right finger 2b", "ValveBiped.Bip01_R_Finger11"],
    ["arm right finger 2c", "ValveBiped.Bip01_R_Finger12"],  # end r-index
    ["arm right finger 3a", "ValveBiped.Bip01_R_Finger2"],  # r-hand remainder
    ["arm right finger 3b", "ValveBiped.Bip01_R_Finger21"],
    ["arm right finger 3c", "ValveBiped.Bip01_R_Finger22"],
    ["arm right finger 4a", "ValveBiped.Bip01_R_Finger3"],
    ["arm right finger 4b", "ValveBiped.Bip01_R_Finger31"],
    ["arm right finger 4c", "ValveBiped.Bip01_R_Finger32"],
    ["arm right finger 5a", "ValveBiped.Bip01_R_Finger4"],
    ["arm right finger 5b", "ValveBiped.Bip01_R_Finger41"],
    ["arm right finger 5c", "ValveBiped.Bip01_R_Finger42"],
    ["neckgroup", "ValveBiped.Bip01_Neck1"],
    ["lhip", "ValveBiped.Bip01_L_Thigh"],
    ["lcalf", "ValveBiped.Bip01_L_Calf"],
    ["lankle", "ValveBiped.Bip01_L_Foot"],
    ["leg left toes", "ValveBiped.Bip01_L_Toe0"],
    ["rhip", "ValveBiped.Bip01_R_Thigh"],
    ["rcalf", "ValveBiped.Bip01_R_Calf"],
    ["rankle", "ValveBiped.Bip01_R_Foot"],
    ["leg right toes", "ValveBiped.Bip01_R_Toe0"],
    ["Skirt1", "ValveBiped.Bip01_Pelvis"],
    ["Skirt2", "ValveBiped.Cod"],
    ["headgroup", "ValveBiped.Bip01_Head1"],
    #    think this is leftover, test later
    ["", "ValveBiped.Bip01_Pelvis"],
]

SWJS_fc_bones = {
    "head",
    "head_tip",
    "head_tip_end",
    "upper_pallete_jnt",
    "lower_pallete_jnt",
    "tongue01_jnt",
    "tongue02_jnt",
    "tongue03_jnt",
    "tongue04_jnt",
    "tongue04_R_jnt",
    "tongue04_L_jnt",
    "tongue03_L_jnt",
    "tongue03_R_jnt",
    "tongue02_L_jnt",
    "tongue02_R_jnt",
    "left_eye_jnt",
    "right_eye_jnt",
    "eyeOverlay_root",
    "left_eyeOverlay1_jnt",
    "left_eyeOverlay2_jnt",
    "left_eyeOverlay4_jnt",
    "left_eyeOverlay5_jnt",
    "left_eyeOverlay6_jnt",
    "left_eyeOverlay7_jnt",
    "left_eyeOverlay8_jnt",
    "left_eyeOverlay9_jnt",
    "left_eyeOverlay10_jnt",
    "left_eyeOverlay11_jnt",
    "left_eyeOverlay12_jnt",
    "left_eyeOverlay13_jnt",
    "left_eyeOverlay14_jnt",
    "left_eyeOverlay16_jnt",
    "right_eyeOverlay1_jnt",
    "right_eyeOverlay2_jnt",
    "right_eyeOverlay3_jnt",
    "right_eyeOverlay4_jnt",
    "right_eyeOverlay5_jnt",
    "right_eyeOverlay6_jnt",
    "right_eyeOverlay7_jnt",
    "right_eyeOverlay8_jnt",
    "right_eyeOverlay9_jnt",
    "right_eyeOverlay10_jnt",
    "right_eyeOverlay11_jnt",
    "right_eyeOverlay12_jnt",
    "right_eyeOverlay13_jnt",
    "right_eyeOverlay14_jnt",
    "right_eyeOverlay15_jnt",
    "right_eyeOverlay16_jnt",
    "head_face_root",
    "midHead_024",
    "leftHead_0149",
    "leftHead_0151",
    "leftHead_0152",
    "leftHead_0177",
    "leftHead_0175",
    "leftHead_0176",
    "leftHead_0174",
    "leftHead_0204",
    "rightHead_0149",
    "rightHead_0151",
    "rightHead_0152",
    "rightHead_0177",
    "rightHead_0175",
    "rightHead_0176",
    "rightHead_0174",
    "rightHead_0204",
    "midHead_013",
    "leftHead_008",
    "leftHead_0146",
    "leftHead_081",
    "leftHead_0148",
    "leftHead_014",
    "leftHead_073",
    "leftHead_072",
    "leftHead_0206",
    "leftHead_018",
    "leftHead_099",
    "leftHead_0127",
    "leftHead_033",
    "leftHead_035",
    "leftHead_039",
    "leftHead_0142",
    "leftHead_065",
    "leftHead_047",
    "leftHead_070",
    "leftHead_071",
    "leftHead_0205",
    "leftHead_052",
    "leftHead_0142",
    "leftHead_056",
    "leftHead_061",
    "leftHead_0122",
    "leftHead_0132",
    "rightHead_008",
    "rightHead_0146",
    "rightHead_0148",
    "rightHead_014",
    "rightHead_073",
    "rightHead_072",
    "rightHead_0206",
    "rightHead_018",
    "rightHead_099",
    "rightHead_0127",
    "rightHead_033",
    "rightHead_035",
    "rightHead_039",
    "rightHead_064",
    "rightHead_065",
    "rightHead_047",
    "rightHead_070",
    "rightHead_071",
    "rightHead_0205",
    "rightHead_052",
    "rightHead_0142",
    "rightHead_056",
    "rightHead_061",
    "rightHead_0122",
    "rightHead_0132",
    "leftHead_021",
    "leftHead_0143",
    "leftHead_0144",
    "leftHead_030",
    "leftHead_0107",
    "leftHead_0165",
    "leftHead_046",
    "leftHead_0199",
    "leftHead_050",
    "leftHead_0181",
    "leftHead_0170",
    "leftHead_0178",
    "leftHead_0180",
    "rightHead_021",
    "rightHead_0143",
    "leftHead_0144",
    "rightHead_0144",
    "rightHead_030",
    "rightHead_0107",
    "rightHead_0165",
    "rightHead_046",
    "rightHead_0199",
    "rightHead_050",
    "rightHead_0181",
    "rightHead_0170",
    "rightHead_0178",
    "rightHead_0180",
    "rightHead_021",
    "rightHead_0143",
    "rightHead_0144",
    "rightHead_0107",
    "rightHead_0165",
    "rightHead_046",
    "rightHead_0199",
    "rightHead_050",
    "leftHead_022",
    "leftHead_0102",
    "rightHead_022",
    "rightHead_0102",
    "leftHead_029",
    "leftHead_0131",
    "rightHead_029",
    "rightHead_0131",
    "leftHead_005",
    "leftHead_0203",
    "leftHead_0155",
    "leftHead_0118",
    "leftHead_026",
    "leftHead_0106",
    "leftHead_0167",
    "leftHead_0164",
    "leftHead_031",
    "leftHead_0108",
    "leftHead_0166",
    "rightHead_005",
    "rightHead_0203",
    "rightHead_0155",
    "rightHead_0118",
    "rightHead_026",
    "rightHead_0106",
    "rightHead_0164",
    "rightHead_031",
    "rightHead_0108",
    "rightHead_0169",
    "rightHead_0166",
    "midHead_001",
    "midHead_003",
    "midHead_022",
    "midHead_004",
    "midHead_005",
    "midHead_0014",
    "midHead_006",
    "midHead_007",
    "midHead_008",
    "midHead_009",
    "midHead_0013",
    "midHead_010",
    "midHead_0015",
    "midHead_011",
    "midHead_012",
    "midHead_014",
    "midHead_017",
    "midHead_018",
    "midHead_019",
    "midHead_015",
    "midHead_020",
    "midHead_021",
    "leftHead_001",
    "leftHead_002",
    "leftHead_003",
    "leftHead_0010",
    "leftHead_004",
    "leftHead_0156",
    "leftHead_0193",
    "leftHead_082",
    "leftHead_006",
    "leftHead_0192",
    "leftHead_078",
    "leftHead_0189",
    "leftHead_0191",
    "leftHead_079",
    "leftHead_007",
    "leftHead_0119",
    "leftHead_009",
    "leftHead_0145",
    "leftHead_080",
    "leftHead_0147",
    "leftHead_010",
    "leftHead_0207",
    "leftHead_0208",
    "leftHead_011",
    "leftHead_0195",
    "leftHead_0194",
    "leftHead_012",
    "leftHead_013",
    "leftHead_015",
    "leftHead_074",
    "leftHead_075",
    "leftHead_016",
    "leftHead_0137",
    "leftHead_017",
    "leftHead_0109",
    "leftHead_0171",
    "leftHead_0135",
    "leftHead_059",
    "leftHead_0172",
    "leftHead_060",
    "leftHead_0136",
    "leftHead_020",
    "leftHead_086",
    "leftHead_0153",
    "leftHead_0154",
    "leftHead_023",
    "leftHead_0150",
    "leftHead_0187",
    "leftHead_0188",
    "leftHead_083",
    "leftHead_025",
    "leftHead_0209",
    "leftHead_0210",
    "leftHead_027",
    "leftHead_0134",
    "leftHead_0201",
    "leftHead_0202",
    "leftHead_0123",
    "leftHead_028",
    "leftHead_0133",
    "leftHead_057",
    "leftHead_058",
    "leftHead_032",
    "leftHead_0139",
    "leftHead_0211",
    "leftHead_0212",
    "leftHead_034",
    "leftHead_087",
    "leftHead_036",
    "leftHead_037",
    "leftHead_062",
    "leftHead_063",
    "leftHead_038",
    "leftHead_040",
    "leftHead_085",
    "leftHead_0116",
    "leftHead_0117",
    "leftHead_041",
    "leftHead_0103",
    "leftHead_0104",
    "leftHead_0163",
    "leftHead_0105",
    "leftHead_084",
    "leftHead_042",
    "leftHead_0173",
    "leftHead_0200",
    "leftHead_043",
    "leftHead_0197",
    "leftHead_0198",
    "leftHead_044",
    "leftHead_0196",
    "leftHead_045",
    "leftHead_048",
    "leftHead_069",
    "leftHead_068",
    "leftHead_049",
    "leftHead_066",
    "leftHead_067",
    "leftHead_051",
    "leftHead_0190",
    "leftHead_077",
    "leftHead_076",
    "leftHead_053",
    "leftHead_0140",
    "leftHead_054",
    "leftHead_055",
    "leftHead_0138",
    "rightHead_001",
    "rightHead_002",
    "rightHead_003",
    "rightHead_0010",
    "rightHead_004",
    "rightHead_0156",
    "rightHead_0193",
    "rightHead_082",
    "rightHead_006",
    "rightHead_0192",
    "rightHead_078",
    "rightHead_0189",
    "rightHead_0191",
    "rightHead_079",
    "rightHead_007",
    "rightHead_009",
    "rightHead_0145",
    "rightHead_080",
    "rightHead_0147",
    "rightHead_010",
    "rightHead_0207",
    "rightHead_0208",
    "rightHead_011",
    "rightHead_0195",
    "rightHead_0194",
    "rightHead_012",
    "rightHead_013",
    "rightHead_015",
    "rightHead_074",
    "rightHead_075",
    "rightHead_016",
    "rightHead_0137",
    "rightHead_017",
    "rightHead_0109",
    "rightHead_0171",
    "rightHead_0135",
    "rightHead_059",
    "rightHead_0137",
    "rightHead_0172",
    "rightHead_060",
    "rightHead_0136",
    "rightHead_020",
    "rightHead_086",
    "rightHead_0153",
    "rightHead_0154",
    "rightHead_023",
    "rightHead_0150",
    "rightHead_0187",
    "rightHead_0188",
    "rightHead_083",
    "rightHead_025",
    "rightHead_0209",
    "rightHead_0210",
    "rightHead_027",
    "rightHead_0134",
    "rightHead_0201",
    "rightHead_0202",
    "rightHead_0123",
    "rightHead_028",
    "rightHead_0133",
    "rightHead_057",
    "rightHead_058",
    "rightHead_032",
    "rightHead_0139",
    "rightHead_0211",
    "rightHead_0212",
    "rightHead_034",
    "rightHead_087",
    "rightHead_036",
    "rightHead_088",
    "rightHead_037",
    "rightHead_062",
    "rightHead_063",
    "rightHead_038",
    "rightHead_040",
    "rightHead_085",
    "rightHead_0116",
    "rightHead_0117",
    "rightHead_041",
    "rightHead_0103",
    "rightHead_0104",
    "rightHead_0163",
    "rightHead_0105",
    "rightHead_084",
    "rightHead_042",
    "rightHead_0173",
    "rightHead_0200",
    "rightHead_043",
    "rightHead_0197",
    "rightHead_0198",
    "rightHead_044",
    "rightHead_0196",
    "rightHead_045",
    "rightHead_048",
    "rightHead_069",
    "rightHead_068",
    "rightHead_049",
    "rightHead_066",
    "rightHead_067",
    "rightHead_051",
    "rightHead_0190",
    "rightHead_077",
    "rightHead_076",
    "rightHead_053",
    "rightHead_0140",
    "rightHead_054",
    "rightHead_055",
    "rightHead_0138",
    "midHead_016",
    "leftHead_064",
    "leftHead_0168",
    "rightHead_0168",
    "leftHead_0141",
    "rightHead_0141",
    "leftHead_0169",
    "rightHead_0167",
    "midHead_023",
    "leftHead_064",
    "leftHead_088",
    "rightHead_0119",
    "leftHead_0141",
    "rightHead_081",
    "left_eyeOverlay3_jnt",
    "left_eyeOverlay15_jnt",
    "leftHead_033_eyeOverlay_jnt",
    "leftHead_088_eyeOverlay_jnt",
    "leftHead_063_eyeOverlay_jnt",
    "leftHead_062_eyeOverlay_jnt",
    "leftHead_087_eyeOverlay_jnt",
    "leftHead_035_eyeOverlay_jnt",
    "leftHead_065_eyeOverlay_jnt",
    "leftHead_064_eyeOverlay_jnt",
    "leftHead_001_eyeOverlay_jnt",
    "leftHead_036_eyeOverlay_jnt",
    "leftHead_037_eyeOverlay_jnt",
    "leftHead_039_eyeOverlay_jnt",
    "leftHead_038_eyeOverlay_jnt",
    "leftHead_034_eyeOverlay_jnt",
    "leftMidhead_001_eyeOverlay_jnt",
    "rightHead_033_eyeOverlay_jnt",
    "rightHead_088_eyeOverlay_jnt",
    "rightHead_063_eyeOverlay_jnt",
    "rightHead_062_eyeOverlay_jnt",
    "rightHead_087_eyeOverlay_jnt",
    "rightHead_035_eyeOverlay_jnt",
    "rightHead_065_eyeOverlay_jnt",
    "rightHead_064_eyeOverlay_jnt",
    "rightHead_001_eyeOverlay_jnt",
    "rightHead_036_eyeOverlay_jnt",
    "rightHead_037_eyeOverlay_jnt",
    "rightHead_039_eyeOverlay_jnt",
    "rightHead_038_eyeOverlay_jnt",
    "rightHead_034_eyeOverlay_jnt",
    "rightMidhead_001_eyeOverlay_jnt",
    "head_face_root",
    "FACIAL_C_Hair1",
    "FACIAL_L_12IPV_Hair1",
    "FACIAL_R_12IPV_Hair1",
    "FACIAL_C_Hair2",
    "FACIAL_C_Hair3",
    "FACIAL_C_Hair4",
    "FACIAL_C_Hair5",
    "FACIAL_C_Hair6",
    "FACIAL_L_HairA1",
    "FACIAL_R_HairA1",
    "FACIAL_L_HairA2",
    "FACIAL_R_HairA2",
    "FACIAL_L_HairA3",
    "FACIAL_R_HairA3",
    "FACIAL_L_HairA4",
    "FACIAL_R_HairA4",
    "FACIAL_L_HairA5",
    "FACIAL_R_HairA5",
    "FACIAL_L_HairA6",
    "FACIAL_R_HairA6",
    "FACIAL_L_HairB1",
    "FACIAL_R_HairB1",
    "FACIAL_L_HairB2",
    "FACIAL_R_HairB2",
    "FACIAL_L_HairB3",
    "FACIAL_R_HairB3",
    "FACIAL_L_HairB4",
    "FACIAL_R_HairB4",
    "FACIAL_L_HairB5",
    "FACIAL_R_HairB5",
    "FACIAL_L_Temple",
    "FACIAL_R_Temple",
    "FACIAL_L_12IPV_Temple1",
    "FACIAL_R_12IPV_Temple1",
    "FACIAL_L_12IPV_Temple2",
    "FACIAL_R_12IPV_Temple2",
    "FACIAL_L_12IPV_Temple3",
    "FACIAL_R_12IPV_Temple3",
    "FACIAL_L_12IPV_Temple4",
    "FACIAL_R_12IPV_Temple4",
    "FACIAL_L_HairC1",
    "FACIAL_R_HairC1",
    "FACIAL_L_HairC2",
    "FACIAL_R_HairC2",
    "FACIAL_L_HairC3",
    "FACIAL_R_HairC3",
    "FACIAL_L_HairC4",
    "FACIAL_R_HairC4",
    "FACIAL_L_Sideburn1",
    "FACIAL_R_Sideburn1",
    "FACIAL_L_Sideburn2",
    "FACIAL_R_Sideburn2",
    "FACIAL_L_Sideburn3",
    "FACIAL_R_Sideburn3",
    "FACIAL_L_Sideburn4",
    "FACIAL_R_Sideburn4",
    "FACIAL_L_Sideburn5",
    "FACIAL_R_Sideburn5",
    "FACIAL_L_Sideburn6",
    "FACIAL_R_Sideburn6",
    "FACIAL_C_ForeheadSkin",
    "FACIAL_L_ForeheadInSkin",
    "FACIAL_R_ForeheadInSkin",
    "FACIAL_L_12IPV_ForeheadSkin1",
    "FACIAL_R_12IPV_ForeheadSkin1",
    "FACIAL_L_12IPV_ForeheadSkin2",
    "FACIAL_R_12IPV_ForeheadSkin2",
    "FACIAL_L_12IPV_ForeheadSkin3",
    "FACIAL_R_12IPV_ForeheadSkin3",
    "FACIAL_L_12IPV_ForeheadSkin4",
    "FACIAL_R_12IPV_ForeheadSkin4",
    "FACIAL_L_12IPV_ForeheadSkin5",
    "FACIAL_R_12IPV_ForeheadSkin5",
    "FACIAL_L_12IPV_ForeheadSkin6",
    "FACIAL_R_12IPV_ForeheadSkin6",
    "FACIAL_L_ForeheadMidSkin",
    "FACIAL_R_ForeheadMidSkin",
    "FACIAL_L_ForeheadOutSkin",
    "FACIAL_R_ForeheadOutSkin",
    "FACIAL_C_Skull",
    "FACIAL_C_Forehead",
    "FACIAL_C_Forehead1",
    "FACIAL_L_Forehead1",
    "FACIAL_R_Forehead1",
    "FACIAL_C_Forehead2",
    "FACIAL_L_Forehead2",
    "FACIAL_R_Forehead2",
    "FACIAL_C_Forehead3",
    "FACIAL_L_Forehead3",
    "FACIAL_R_Forehead3",
    "FACIAL_C_12IPV_Forehead1",
    "FACIAL_L_12IPV_Forehead1",
    "FACIAL_R_12IPV_Forehead1",
    "FACIAL_C_12IPV_Forehead2",
    "FACIAL_L_12IPV_Forehead2",
    "FACIAL_R_12IPV_Forehead2",
    "FACIAL_C_12IPV_Forehead3",
    "FACIAL_L_12IPV_Forehead3",
    "FACIAL_R_12IPV_Forehead3",
    "FACIAL_C_12IPV_Forehead4",
    "FACIAL_L_12IPV_Forehead4",
    "FACIAL_R_12IPV_Forehead4",
    "FACIAL_C_12IPV_Forehead5",
    "FACIAL_L_12IPV_Forehead5",
    "FACIAL_R_12IPV_Forehead5",
    "FACIAL_C_12IPV_Forehead6",
    "FACIAL_L_12IPV_Forehead6",
    "FACIAL_R_12IPV_Forehead6",
    "FACIAL_L_ForeheadIn",
    "FACIAL_L_ForeheadInA1",
    "FACIAL_L_ForeheadInA2",
    "FACIAL_L_ForeheadInA3",
    "FACIAL_L_ForeheadInB1",
    "FACIAL_L_ForeheadInB2",
    "FACIAL_L_12IPV_ForeheadIn1",
    "FACIAL_L_12IPV_ForeheadIn2",
    "FACIAL_L_12IPV_ForeheadIn3",
    "FACIAL_L_12IPV_ForeheadIn4",
    "FACIAL_L_12IPV_ForeheadIn5",
    "FACIAL_L_12IPV_ForeheadIn6",
    "FACIAL_L_12IPV_ForeheadIn7",
    "FACIAL_L_12IPV_ForeheadIn8",
    "FACIAL_L_12IPV_ForeheadIn9",
    "FACIAL_L_12IPV_ForeheadIn10",
    "FACIAL_L_12IPV_ForeheadIn11",
    "FACIAL_L_12IPV_ForeheadIn12",
    "FACIAL_L_12IPV_ForeheadIn13",
    "FACIAL_L_12IPV_ForeheadIn14",
    "FACIAL_R_ForeheadIn",
    "FACIAL_R_ForeheadInA1",
    "FACIAL_R_ForeheadInA2",
    "FACIAL_R_ForeheadInA3",
    "FACIAL_R_ForeheadInB1",
    "FACIAL_R_ForeheadInB2",
    "FACIAL_R_12IPV_ForeheadIn1",
    "FACIAL_R_12IPV_ForeheadIn2",
    "FACIAL_R_12IPV_ForeheadIn3",
    "FACIAL_R_12IPV_ForeheadIn5",
    "FACIAL_R_12IPV_ForeheadIn4",
    "FACIAL_R_12IPV_ForeheadIn6",
    "FACIAL_R_12IPV_ForeheadIn7",
    "FACIAL_R_12IPV_ForeheadIn8",
    "FACIAL_R_12IPV_ForeheadIn9",
    "FACIAL_R_12IPV_ForeheadIn10",
    "FACIAL_R_12IPV_ForeheadIn12",
    "FACIAL_R_12IPV_ForeheadIn11",
    "FACIAL_R_12IPV_ForeheadIn13",
    "FACIAL_R_12IPV_ForeheadIn14",
    "FACIAL_L_ForeheadMid",
    "FACIAL_L_ForeheadMid1",
    "FACIAL_L_ForeheadMid2",
    "FACIAL_L_12IPV_ForeheadMid15",
    "FACIAL_L_12IPV_ForeheadMid16",
    "FACIAL_L_12IPV_ForeheadMid17",
    "FACIAL_L_12IPV_ForeheadMid18",
    "FACIAL_L_12IPV_ForeheadMid19",
    "FACIAL_L_12IPV_ForeheadMid20",
    "FACIAL_L_12IPV_ForeheadMid21",
    "FACIAL_L_12IPV_ForeheadMid22",
    "FACIAL_R_ForeheadMid",
    "FACIAL_R_ForeheadMid1",
    "FACIAL_R_ForeheadMid2",
    "FACIAL_R_12IPV_ForeheadMid15",
    "FACIAL_R_12IPV_ForeheadMid16",
    "FACIAL_R_12IPV_ForeheadMid17",
    "FACIAL_R_12IPV_ForeheadMid18",
    "FACIAL_R_12IPV_ForeheadMid19",
    "FACIAL_R_12IPV_ForeheadMid20",
    "FACIAL_R_12IPV_ForeheadMid21",
    "FACIAL_R_12IPV_ForeheadMid22",
    "FACIAL_L_ForeheadOut",
    "FACIAL_L_ForeheadOutA1",
    "FACIAL_L_ForeheadOutA2",
    "FACIAL_L_ForeheadOutB1",
    "FACIAL_L_ForeheadOutB2",
    "FACIAL_L_12IPV_ForeheadOut23",
    "FACIAL_L_12IPV_ForeheadOut24",
    "FACIAL_L_12IPV_ForeheadOut25",
    "FACIAL_L_12IPV_ForeheadOut26",
    "FACIAL_L_12IPV_ForeheadOut27",
    "FACIAL_L_12IPV_ForeheadOut28",
    "FACIAL_L_12IPV_ForeheadOut29",
    "FACIAL_L_12IPV_ForeheadOut30",
    "FACIAL_L_12IPV_ForeheadOut31",
    "FACIAL_L_12IPV_ForeheadOut32",
    "FACIAL_R_ForeheadOut",
    "FACIAL_R_ForeheadOutA1",
    "FACIAL_R_ForeheadOutA2",
    "FACIAL_R_ForeheadOutB1",
    "FACIAL_R_ForeheadOutB2",
    "FACIAL_R_12IPV_ForeheadOut23",
    "FACIAL_R_12IPV_ForeheadOut24",
    "FACIAL_R_12IPV_ForeheadOut25",
    "FACIAL_R_12IPV_ForeheadOut26",
    "FACIAL_R_12IPV_ForeheadOut27",
    "FACIAL_R_12IPV_ForeheadOut28",
    "FACIAL_R_12IPV_ForeheadOut29",
    "FACIAL_R_12IPV_ForeheadOut30",
    "FACIAL_R_12IPV_ForeheadOut31",
    "FACIAL_R_12IPV_ForeheadOut32",
    "FACIAL_L_12IPV_EyesackU0",
    "FACIAL_R_12IPV_EyesackU0",
    "FACIAL_L_EyesackUpper",
    "FACIAL_L_EyesackUpper1",
    "FACIAL_L_EyesackUpper2",
    "FACIAL_L_EyesackUpper3",
    "FACIAL_R_EyesackUpper",
    "FACIAL_R_EyesackUpper1",
    "FACIAL_R_EyesackUpper2",
    "FACIAL_R_EyesackUpper3",
    "FACIAL_L_EyesackUpper4",
    "FACIAL_R_EyesackUpper4",
    "FACIAL_L_EyelidUpperFurrow",
    "FACIAL_L_EyelidUpperFurrow1",
    "FACIAL_L_EyelidUpperFurrow2",
    "FACIAL_L_EyelidUpperFurrow3",
    "FACIAL_R_EyelidUpperFurrow",
    "FACIAL_R_EyelidUpperFurrow1",
    "FACIAL_R_EyelidUpperFurrow2",
    "FACIAL_R_EyelidUpperFurrow3",
    "FACIAL_L_EyelidUpperB",
    "FACIAL_L_EyelidUpperB1",
    "FACIAL_L_EyelidUpperB2",
    "FACIAL_L_EyelidUpperB3",
    "FACIAL_R_EyelidUpperB",
    "FACIAL_R_EyelidUpperB1",
    "FACIAL_R_EyelidUpperB2",
    "FACIAL_R_EyelidUpperB3",
    "FACIAL_L_EyelidUpperA",
    "FACIAL_L_EyelidUpperA1",
    "FACIAL_L_EyelashesUpperA1",
    "FACIAL_L_EyelidUpperA2",
    "FACIAL_L_EyelashesUpperA2",
    "FACIAL_L_EyelidUpperA3",
    "FACIAL_L_EyelashesUpperA3",
    "FACIAL_R_EyelidUpperA",
    "FACIAL_R_EyelidUpperA1",
    "FACIAL_R_EyelashesUpperA1",
    "FACIAL_R_EyelidUpperA2",
    "FACIAL_R_EyelashesUpperA2",
    "FACIAL_R_EyelidUpperA3",
    "FACIAL_R_EyelashesUpperA3",
    "FACIAL_L_Eye",
    "FACIAL_L_EyeParallel",
    "FACIAL_L_Pupil",
    "FACIAL_R_Eye",
    "FACIAL_R_EyeParallel",
    "FACIAL_R_Pupil",
    "FACIAL_L_EyelidLowerA",
    "FACIAL_L_EyelidLowerA1",
    "FACIAL_L_EyelidLowerA2",
    "FACIAL_L_EyelidLowerA3",
    "FACIAL_R_EyelidLowerA",
    "FACIAL_R_EyelidLowerA1",
    "FACIAL_R_EyelidLowerA2",
    "FACIAL_R_EyelidLowerA3",
    "FACIAL_L_EyelidLowerB",
    "FACIAL_L_EyelidLowerB1",
    "FACIAL_L_EyelidLowerB2",
    "FACIAL_L_EyelidLowerB3",
    "FACIAL_R_EyelidLowerB",
    "FACIAL_R_EyelidLowerB1",
    "FACIAL_R_EyelidLowerB2",
    "FACIAL_R_EyelidLowerB3",
    "FACIAL_L_EyeCornerInner",
    "FACIAL_L_EyeCornerInner1",
    "FACIAL_L_EyeCornerInner2",
    "FACIAL_R_EyeCornerInner",
    "FACIAL_R_EyeCornerInner1",
    "FACIAL_R_EyeCornerInner2",
    "FACIAL_L_EyeCornerOuter",
    "FACIAL_L_EyeCornerOuter1",
    "FACIAL_L_EyelashesCornerOuter1",
    "FACIAL_L_EyeCornerOuter2",
    "FACIAL_R_EyeCornerOuter",
    "FACIAL_R_EyeCornerOuter1",
    "FACIAL_R_EyelashesCornerOuter1",
    "FACIAL_R_EyeCornerOuter2",
    "FACIAL_L_12IPV_EyeCornerO1",
    "FACIAL_R_12IPV_EyeCornerO1",
    "FACIAL_L_12IPV_EyeCornerO2",
    "FACIAL_R_12IPV_EyeCornerO2",
    "FACIAL_L_EyesackLower",
    "FACIAL_L_EyesackLower1",
    "FACIAL_L_EyesackLower2",
    "FACIAL_L_12IPV_EyesackL1",
    "FACIAL_L_12IPV_EyesackL2",
    "FACIAL_L_12IPV_EyesackL3",
    "FACIAL_L_12IPV_EyesackL4",
    "FACIAL_L_12IPV_EyesackL5",
    "FACIAL_L_12IPV_EyesackL6",
    "FACIAL_L_12IPV_EyesackL7",
    "FACIAL_L_12IPV_EyesackL8",
    "FACIAL_R_EyesackLower",
    "FACIAL_R_EyesackLower1",
    "FACIAL_R_EyesackLower2",
    "FACIAL_R_12IPV_EyesackL1",
    "FACIAL_R_12IPV_EyesackL2",
    "FACIAL_R_12IPV_EyesackL3",
    "FACIAL_R_12IPV_EyesackL4",
    "FACIAL_R_12IPV_EyesackL5",
    "FACIAL_R_12IPV_EyesackL6",
    "FACIAL_R_12IPV_EyesackL7",
    "FACIAL_R_12IPV_EyesackL8",
    "FACIAL_L_CheekInner",
    "FACIAL_L_CheekInner1",
    "FACIAL_L_CheekInner2",
    "FACIAL_L_CheekInner3",
    "FACIAL_L_CheekInner4",
    "FACIAL_R_CheekInner",
    "FACIAL_R_CheekInner1",
    "FACIAL_R_CheekInner2",
    "FACIAL_R_CheekInner3",
    "FACIAL_R_CheekInner4",
    "FACIAL_L_CheekOuter",
    "FACIAL_L_CheekOuter1",
    "FACIAL_L_CheekOuter2",
    "FACIAL_L_CheekOuter3",
    "FACIAL_R_CheekOuter",
    "FACIAL_R_CheekOuter1",
    "FACIAL_R_CheekOuter2",
    "FACIAL_R_CheekOuter3",
    "FACIAL_L_CheekOuter4",
    "FACIAL_R_CheekOuter4",
    "FACIAL_L_12IPV_CheekOuter1",
    "FACIAL_R_12IPV_CheekOuter1",
    "FACIAL_L_12IPV_CheekOuter2",
    "FACIAL_R_12IPV_CheekOuter2",
    "FACIAL_L_12IPV_CheekOuter3",
    "FACIAL_R_12IPV_CheekOuter3",
    "FACIAL_L_12IPV_CheekOuter4",
    "FACIAL_R_12IPV_CheekOuter4",
    "FACIAL_C_NoseBridge",
    "FACIAL_C_12IPV_NoseBridge1",
    "FACIAL_L_12IPV_NoseBridge1",
    "FACIAL_R_12IPV_NoseBridge1",
    "FACIAL_C_12IPV_NoseBridge2",
    "FACIAL_L_12IPV_NoseBridge2",
    "FACIAL_R_12IPV_NoseBridge2",
    "FACIAL_L_NoseBridge",
    "FACIAL_R_NoseBridge",
    "FACIAL_C_NoseUpper",
    "FACIAL_L_NoseUpper",
    "FACIAL_R_NoseUpper",
    "FACIAL_C_12IPV_NoseUpper1",
    "FACIAL_C_12IPV_NoseUpper2",
    "FACIAL_L_12IPV_NoseUpper1",
    "FACIAL_R_12IPV_NoseUpper1",
    "FACIAL_L_12IPV_NoseUpper2",
    "FACIAL_R_12IPV_NoseUpper2",
    "FACIAL_L_12IPV_NoseUpper3",
    "FACIAL_R_12IPV_NoseUpper3",
    "FACIAL_L_12IPV_NoseUpper4",
    "FACIAL_R_12IPV_NoseUpper4",
    "FACIAL_L_12IPV_NoseUpper5",
    "FACIAL_R_12IPV_NoseUpper5",
    "FACIAL_L_12IPV_NoseUpper6",
    "FACIAL_R_12IPV_NoseUpper6",
    "FACIAL_L_NasolabialBulge1",
    "FACIAL_R_NasolabialBulge1",
    "FACIAL_L_12IPV_NasolabialB13",
    "FACIAL_R_12IPV_NasolabialB13",
    "FACIAL_L_12IPV_NasolabialB14",
    "FACIAL_R_12IPV_NasolabialB14",
    "FACIAL_L_12IPV_NasolabialB15",
    "FACIAL_R_12IPV_NasolabialB15",
    "FACIAL_L_NasolabialBulge",
    "FACIAL_L_NasolabialBulge2",
    "FACIAL_L_NasolabialBulge3",
    "FACIAL_L_12IPV_NasolabialB1",
    "FACIAL_L_12IPV_NasolabialB2",
    "FACIAL_L_12IPV_NasolabialB3",
    "FACIAL_L_12IPV_NasolabialB4",
    "FACIAL_L_12IPV_NasolabialB5",
    "FACIAL_L_12IPV_NasolabialB6",
    "FACIAL_L_12IPV_NasolabialB7",
    "FACIAL_L_12IPV_NasolabialB8",
    "FACIAL_L_12IPV_NasolabialB9",
    "FACIAL_L_12IPV_NasolabialB10",
    "FACIAL_L_12IPV_NasolabialB11",
    "FACIAL_L_12IPV_NasolabialB12",
    "FACIAL_R_NasolabialBulge",
    "FACIAL_R_NasolabialBulge2",
    "FACIAL_R_NasolabialBulge3",
    "FACIAL_R_12IPV_NasolabialB1",
    "FACIAL_R_12IPV_NasolabialB2",
    "FACIAL_R_12IPV_NasolabialB3",
    "FACIAL_R_12IPV_NasolabialB4",
    "FACIAL_R_12IPV_NasolabialB5",
    "FACIAL_R_12IPV_NasolabialB6",
    "FACIAL_R_12IPV_NasolabialB7",
    "FACIAL_R_12IPV_NasolabialB8",
    "FACIAL_R_12IPV_NasolabialB9",
    "FACIAL_R_12IPV_NasolabialB10",
    "FACIAL_R_12IPV_NasolabialB11",
    "FACIAL_R_12IPV_NasolabialB12",
    "FACIAL_L_NasolabialFurrow",
    "FACIAL_R_NasolabialFurrow",
    "FACIAL_L_12IPV_NasolabialF1",
    "FACIAL_R_12IPV_NasolabialF1",
    "FACIAL_L_12IPV_NasolabialF2",
    "FACIAL_R_12IPV_NasolabialF2",
    "FACIAL_L_12IPV_NasolabialF3",
    "FACIAL_R_12IPV_NasolabialF3",
    "FACIAL_L_12IPV_NasolabialF4",
    "FACIAL_R_12IPV_NasolabialF4",
    "FACIAL_L_12IPV_NasolabialF5",
    "FACIAL_R_12IPV_NasolabialF5",
    "FACIAL_L_12IPV_NasolabialF6",
    "FACIAL_R_12IPV_NasolabialF6",
    "FACIAL_L_12IPV_NasolabialF7",
    "FACIAL_R_12IPV_NasolabialF7",
    "FACIAL_L_12IPV_NasolabialF8",
    "FACIAL_R_12IPV_NasolabialF8",
    "FACIAL_L_12IPV_NasolabialF9",
    "FACIAL_R_12IPV_NasolabialF9",
    "FACIAL_L_CheekLower",
    "FACIAL_L_CheekLower1",
    "FACIAL_L_CheekLower2",
    "FACIAL_L_12IPV_CheekL1",
    "FACIAL_L_12IPV_CheekL2",
    "FACIAL_L_12IPV_CheekL3",
    "FACIAL_L_12IPV_CheekL4",
    "FACIAL_R_CheekLower",
    "FACIAL_R_CheekLower1",
    "FACIAL_R_CheekLower2",
    "FACIAL_R_12IPV_CheekL1",
    "FACIAL_R_12IPV_CheekL2",
    "FACIAL_R_12IPV_CheekL3",
    "FACIAL_R_12IPV_CheekL4",
    "FACIAL_L_Ear",
    "FACIAL_L_Ear1",
    "FACIAL_L_Ear2",
    "FACIAL_L_Ear3",
    "FACIAL_L_Ear4",
    "FACIAL_R_Ear",
    "FACIAL_R_Ear1",
    "FACIAL_R_Ear2",
    "FACIAL_R_Ear3",
    "FACIAL_R_Ear4",
    "FACIAL_C_Nose",
    "FACIAL_C_NoseLower",
    "FACIAL_L_NostrilThickness3",
    "FACIAL_R_NostrilThickness3",
    "FACIAL_C_12IPV_NoseL1",
    "FACIAL_C_12IPV_NoseL2",
    "FACIAL_C_NoseTip",
    "FACIAL_C_12IPV_NoseTip1",
    "FACIAL_C_12IPV_NoseTip2",
    "FACIAL_C_12IPV_NoseTip3",
    "FACIAL_L_12IPV_NoseTip1",
    "FACIAL_R_12IPV_NoseTip1",
    "FACIAL_L_12IPV_NoseTip2",
    "FACIAL_R_12IPV_NoseTip2",
    "FACIAL_L_12IPV_NoseTip3",
    "FACIAL_R_12IPV_NoseTip3",
    "FACIAL_L_Nostril",
    "FACIAL_L_NostrilThickness1",
    "FACIAL_L_NostrilThickness2",
    "FACIAL_L_12IPV_Nostril1",
    "FACIAL_L_12IPV_Nostril2",
    "FACIAL_L_12IPV_Nostril3",
    "FACIAL_L_12IPV_Nostril4",
    "FACIAL_L_12IPV_Nostril5",
    "FACIAL_L_12IPV_Nostril6",
    "FACIAL_L_12IPV_Nostril7",
    "FACIAL_L_12IPV_Nostril8",
    "FACIAL_L_12IPV_Nostril9",
    "FACIAL_L_12IPV_Nostril10",
    "FACIAL_L_12IPV_Nostril11",
    "FACIAL_L_12IPV_Nostril12",
    "FACIAL_L_12IPV_Nostril13",
    "FACIAL_L_12IPV_Nostril14",
    "FACIAL_R_Nostril",
    "FACIAL_R_NostrilThickness1",
    "FACIAL_R_NostrilThickness2",
    "FACIAL_R_12IPV_Nostril1",
    "FACIAL_R_12IPV_Nostril2",
    "FACIAL_R_12IPV_Nostril3",
    "FACIAL_R_12IPV_Nostril4",
    "FACIAL_R_12IPV_Nostril5",
    "FACIAL_R_12IPV_Nostril6",
    "FACIAL_R_12IPV_Nostril7",
    "FACIAL_R_12IPV_Nostril8",
    "FACIAL_R_12IPV_Nostril9",
    "FACIAL_R_12IPV_Nostril10",
    "FACIAL_R_12IPV_Nostril11",
    "FACIAL_R_12IPV_Nostril12",
    "FACIAL_R_12IPV_Nostril13",
    "FACIAL_R_12IPV_Nostril14",
    "FACIAL_C_LipUpperSkin",
    "FACIAL_L_LipUpperSkin",
    "FACIAL_R_LipUpperSkin",
    "FACIAL_L_LipUpperOuterSkin",
    "FACIAL_R_LipUpperOuterSkin",
    "FACIAL_C_12IPV_LipUpperSkin1",
    "FACIAL_C_12IPV_LipUpperSkin2",
    "FACIAL_L_12IPV_LipUpperSkin",
    "FACIAL_R_12IPV_LipUpperSkin",
    "FACIAL_L_12IPV_LipUpperOuterSkin1",
    "FACIAL_R_12IPV_LipUpperOuterSkin1",
    "FACIAL_L_12IPV_LipUpperOuterSkin2",
    "FACIAL_R_12IPV_LipUpperOuterSkin2",
    "FACIAL_L_12IPV_MouthInteriorUpper1",
    "FACIAL_R_12IPV_MouthInteriorUpper1",
    "FACIAL_L_12IPV_MouthInteriorUpper2",
    "FACIAL_R_12IPV_MouthInteriorUpper2",
    "FACIAL_C_MouthUpper",
    "FACIAL_C_LipUpper",
    "FACIAL_C_LipUpper1",
    "FACIAL_C_LipUpper2",
    "FACIAL_C_LipUpper3",
    "FACIAL_L_12IPV_LipUpper1",
    "FACIAL_R_12IPV_LipUpper1",
    "FACIAL_L_12IPV_LipUpper2",
    "FACIAL_R_12IPV_LipUpper2",
    "FACIAL_L_12IPV_LipUpper3",
    "FACIAL_R_12IPV_LipUpper3",
    "FACIAL_L_12IPV_LipUpper4",
    "FACIAL_R_12IPV_LipUpper4",
    "FACIAL_L_12IPV_LipUpper5",
    "FACIAL_R_12IPV_LipUpper5",
    "FACIAL_L_LipUpper",
    "FACIAL_L_LipUpper1",
    "FACIAL_L_LipUpper2",
    "FACIAL_L_LipUpper3",
    "FACIAL_L_12IPV_LipUpper6",
    "FACIAL_L_12IPV_LipUpper7",
    "FACIAL_L_12IPV_LipUpper8",
    "FACIAL_L_12IPV_LipUpper9",
    "FACIAL_L_12IPV_LipUpper10",
    "FACIAL_L_12IPV_LipUpper11",
    "FACIAL_L_12IPV_LipUpper12",
    "FACIAL_L_12IPV_LipUpper13",
    "FACIAL_L_12IPV_LipUpper14",
    "FACIAL_L_12IPV_LipUpper15",
    "FACIAL_R_LipUpper",
    "FACIAL_R_LipUpper1",
    "FACIAL_R_LipUpper2",
    "FACIAL_R_LipUpper3",
    "FACIAL_R_12IPV_LipUpper6",
    "FACIAL_R_12IPV_LipUpper7",
    "FACIAL_R_12IPV_LipUpper8",
    "FACIAL_R_12IPV_LipUpper9",
    "FACIAL_R_12IPV_LipUpper10",
    "FACIAL_R_12IPV_LipUpper11",
    "FACIAL_R_12IPV_LipUpper12",
    "FACIAL_R_12IPV_LipUpper13",
    "FACIAL_R_12IPV_LipUpper14",
    "FACIAL_R_12IPV_LipUpper15",
    "FACIAL_L_LipUpperOuter",
    "FACIAL_L_LipUpperOuter1",
    "FACIAL_L_LipUpperOuter2",
    "FACIAL_L_LipUpperOuter3",
    "FACIAL_L_12IPV_LipUpper16",
    "FACIAL_L_12IPV_LipUpper17",
    "FACIAL_L_12IPV_LipUpper18",
    "FACIAL_L_12IPV_LipUpper19",
    "FACIAL_L_12IPV_LipUpper20",
    "FACIAL_L_12IPV_LipUpper21",
    "FACIAL_L_12IPV_LipUpper22",
    "FACIAL_L_12IPV_LipUpper23",
    "FACIAL_L_12IPV_LipUpper24",
    "FACIAL_R_LipUpperOuter",
    "FACIAL_R_LipUpperOuter1",
    "FACIAL_R_LipUpperOuter2",
    "FACIAL_R_LipUpperOuter3",
    "FACIAL_R_12IPV_LipUpper16",
    "FACIAL_R_12IPV_LipUpper17",
    "FACIAL_R_12IPV_LipUpper18",
    "FACIAL_R_12IPV_LipUpper19",
    "FACIAL_R_12IPV_LipUpper20",
    "FACIAL_R_12IPV_LipUpper21",
    "FACIAL_R_12IPV_LipUpper22",
    "FACIAL_R_12IPV_LipUpper23",
    "FACIAL_R_12IPV_LipUpper24",
    "FACIAL_L_LipCorner",
    "FACIAL_L_LipCorner1",
    "FACIAL_L_LipCorner2",
    "FACIAL_L_LipCorner3",
    "FACIAL_L_12IPV_LipCorner1",
    "FACIAL_L_12IPV_LipCorner2",
    "FACIAL_L_12IPV_LipCorner3",
    "FACIAL_R_LipCorner",
    "FACIAL_R_LipCorner1",
    "FACIAL_R_LipCorner2",
    "FACIAL_R_LipCorner3",
    "FACIAL_R_12IPV_LipCorner1",
    "FACIAL_R_12IPV_LipCorner2",
    "FACIAL_R_12IPV_LipCorner3",
    "FACIAL_L_JawBulge",
    "FACIAL_R_JawBulge",
    "FACIAL_L_JawRecess",
    "FACIAL_R_JawRecess",
    "FACIAL_L_Masseter",
    "FACIAL_R_Masseter",
    "FACIAL_C_UnderChin",
    "FACIAL_L_12IPV_UnderChin1",
    "FACIAL_R_12IPV_UnderChin1",
    "FACIAL_L_12IPV_UnderChin2",
    "FACIAL_R_12IPV_UnderChin2",
    "FACIAL_L_UnderChin",
    "FACIAL_R_UnderChin",
    "FACIAL_L_12IPV_UnderChin3",
    "FACIAL_R_12IPV_UnderChin3",
    "FACIAL_L_12IPV_UnderChin4",
    "FACIAL_R_12IPV_UnderChin4",
    "FACIAL_L_12IPV_UnderChin5",
    "FACIAL_R_12IPV_UnderChin5",
    "FACIAL_L_12IPV_UnderChin6",
    "FACIAL_R_12IPV_UnderChin6",
    "FACIAL_C_TeethUpper",
    "FACIAL_C_LowerLipRotation",
    "FACIAL_C_LipLowerSkin",
    "FACIAL_L_LipLowerSkin",
    "FACIAL_R_LipLowerSkin",
    "FACIAL_L_LipLowerOuterSkin",
    "FACIAL_R_LipLowerOuterSkin",
    "FACIAL_C_12IPV_LipLowerSkin1",
    "FACIAL_C_12IPV_LipLowerSkin2",
    "FACIAL_L_12IPV_LipLowerSkin",
    "FACIAL_R_12IPV_LipLowerSkin",
    "FACIAL_L_12IPV_LipLowerOuterSkin1",
    "FACIAL_R_12IPV_LipLowerOuterSkin1",
    "FACIAL_L_12IPV_LipLowerOuterSkin2",
    "FACIAL_R_12IPV_LipLowerOuterSkin2",
    "FACIAL_L_12IPV_LipLowerOuterSkin3",
    "FACIAL_R_12IPV_LipLowerOuterSkin3",
    "FACIAL_L_12IPV_MouthInteriorLower1",
    "FACIAL_R_12IPV_MouthInteriorLower1",
    "FACIAL_L_12IPV_MouthInteriorLower2",
    "FACIAL_R_12IPV_MouthInteriorLower2",
    "FACIAL_C_MouthLower",
    "FACIAL_C_LipLower",
    "FACIAL_C_LipLower1",
    "FACIAL_C_LipLower2",
    "FACIAL_C_LipLower3",
    "FACIAL_L_12IPV_LipLower1",
    "FACIAL_R_12IPV_LipLower1",
    "FACIAL_L_12IPV_LipLower2",
    "FACIAL_R_12IPV_LipLower2",
    "FACIAL_L_12IPV_LipLower3",
    "FACIAL_R_12IPV_LipLower3",
    "FACIAL_L_12IPV_LipLower4",
    "FACIAL_R_12IPV_LipLower4",
    "FACIAL_L_12IPV_LipLower5",
    "FACIAL_R_12IPV_LipLower5",
    "FACIAL_L_LipLower",
    "FACIAL_L_LipLower1",
    "FACIAL_L_LipLower2",
    "FACIAL_L_LipLower3",
    "FACIAL_L_12IPV_LipLower6",
    "FACIAL_L_12IPV_LipLower7",
    "FACIAL_L_12IPV_LipLower8",
    "FACIAL_L_12IPV_LipLower9",
    "FACIAL_L_12IPV_LipLower10",
    "FACIAL_L_12IPV_LipLower11",
    "FACIAL_L_12IPV_LipLower12",
    "FACIAL_L_12IPV_LipLower13",
    "FACIAL_L_12IPV_LipLower14",
    "FACIAL_L_12IPV_LipLower15",
    "FACIAL_R_LipLower",
    "FACIAL_R_LipLower1",
    "FACIAL_R_LipLower2",
    "FACIAL_R_LipLower3",
    "FACIAL_R_12IPV_LipLower6",
    "FACIAL_R_12IPV_LipLower7",
    "FACIAL_R_12IPV_LipLower8",
    "FACIAL_R_12IPV_LipLower9",
    "FACIAL_R_12IPV_LipLower10",
    "FACIAL_R_12IPV_LipLower11",
    "FACIAL_R_12IPV_LipLower12",
    "FACIAL_R_12IPV_LipLower13",
    "FACIAL_R_12IPV_LipLower14",
    "FACIAL_R_12IPV_LipLower15",
    "FACIAL_L_LipLowerOuter",
    "FACIAL_L_LipLowerOuter1",
    "FACIAL_L_LipLowerOuter2",
    "FACIAL_L_LipLowerOuter3",
    "FACIAL_L_12IPV_LipLower16",
    "FACIAL_L_12IPV_LipLower17",
    "FACIAL_L_12IPV_LipLower18",
    "FACIAL_L_12IPV_LipLower19",
    "FACIAL_L_12IPV_LipLower20",
    "FACIAL_L_12IPV_LipLower21",
    "FACIAL_L_12IPV_LipLower22",
    "FACIAL_L_12IPV_LipLower23",
    "FACIAL_L_12IPV_LipLower24",
    "FACIAL_R_LipLowerOuter",
    "FACIAL_R_LipLowerOuter1",
    "FACIAL_R_LipLowerOuter2",
    "FACIAL_R_LipLowerOuter3",
    "FACIAL_R_12IPV_LipLower16",
    "FACIAL_R_12IPV_LipLower17",
    "FACIAL_R_12IPV_LipLower18",
    "FACIAL_R_12IPV_LipLower19",
    "FACIAL_R_12IPV_LipLower20",
    "FACIAL_R_12IPV_LipLower21",
    "FACIAL_R_12IPV_LipLower22",
    "FACIAL_R_12IPV_LipLower23",
    "FACIAL_R_12IPV_LipLower24",
    "FACIAL_C_TeethLower",
    "FACIAL_C_Tongue1",
    "FACIAL_C_Tongue2",
    "FACIAL_C_TongueUpper2",
    "FACIAL_L_TongueSide2",
    "FACIAL_R_TongueSide2",
    "FACIAL_C_Tongue3",
    "FACIAL_C_TongueUpper3",
    "FACIAL_C_TongueLower3",
    "FACIAL_L_TongueSide3",
    "FACIAL_R_TongueSide3",
    "FACIAL_C_Tongue4",
    "FACIAL_C_Jaw",
    "FACIAL_C_Jawline",
    "FACIAL_L_12IPV_Jawline1",
    "FACIAL_R_12IPV_Jawline1",
    "FACIAL_L_12IPV_Jawline2",
    "FACIAL_R_12IPV_Jawline2",
    "FACIAL_L_Jawline",
    "FACIAL_L_Jawline1",
    "FACIAL_L_Jawline2",
    "FACIAL_L_12IPV_Jawline3",
    "FACIAL_L_12IPV_Jawline4",
    "FACIAL_L_12IPV_Jawline5",
    "FACIAL_L_12IPV_Jawline6",
    "FACIAL_R_Jawline",
    "FACIAL_R_Jawline1",
    "FACIAL_R_Jawline2",
    "FACIAL_R_12IPV_Jawline3",
    "FACIAL_R_12IPV_Jawline4",
    "FACIAL_R_12IPV_Jawline5",
    "FACIAL_R_12IPV_Jawline6",
    "FACIAL_L_ChinSide",
    "FACIAL_R_ChinSide",
    "FACIAL_L_12IPV_ChinS1",
    "FACIAL_R_12IPV_ChinS1",
    "FACIAL_L_12IPV_ChinS2",
    "FACIAL_R_12IPV_ChinS2",
    "FACIAL_L_12IPV_ChinS3",
    "FACIAL_R_12IPV_ChinS3",
    "FACIAL_L_12IPV_ChinS4",
    "FACIAL_R_12IPV_ChinS4",
    "FACIAL_C_Chin1",
    "FACIAL_L_Chin1",
    "FACIAL_R_Chin1",
    "FACIAL_C_Chin2",
    "FACIAL_L_Chin2",
    "FACIAL_R_Chin2",
    "FACIAL_C_Chin3",
    "FACIAL_L_Chin3",
    "FACIAL_R_Chin3",
    "FACIAL_L_12IPV_Chin1",
    "FACIAL_R_12IPV_Chin1",
    "FACIAL_L_12IPV_Chin2",
    "FACIAL_R_12IPV_Chin2",
    "FACIAL_C_12IPV_Chin3",
    "FACIAL_C_12IPV_Chin4",
    "FACIAL_L_12IPV_Chin5",
    "FACIAL_R_12IPV_Chin5",
    "FACIAL_L_12IPV_Chin6",
    "FACIAL_R_12IPV_Chin6",
    "FACIAL_L_12IPV_Chin7",
    "FACIAL_R_12IPV_Chin7",
    "FACIAL_L_12IPV_Chin8",
    "FACIAL_R_12IPV_Chin8",
    "FACIAL_L_12IPV_Chin9",
    "FACIAL_R_12IPV_Chin9",
    "FACIAL_L_12IPV_Chin10",
    "FACIAL_R_12IPV_Chin10",
    "FACIAL_L_12IPV_Chin11",
    "FACIAL_R_12IPV_Chin11",
    "FACIAL_L_12IPV_Chin12",
    "FACIAL_R_12IPV_Chin12",
    "FACIAL_L_12IPV_Chin13",
    "FACIAL_R_12IPV_Chin13",
    "FACIAL_L_12IPV_Chin14",
    "FACIAL_R_12IPV_Chin14",
    "FACIAL_C_Chin",
}

SWJS_NeckA_bones = {
    "neckA",
    "neckA_face_root",
    "midHead_0011",
    "midHead_0012",
    "leftHead_0182",
    "leftHead_0183",
    "leftHead_0185",
    "leftHead_0186",
    "rightHead_0182",
    "rightHead_0183",
    "rightHead_0185",
    "rightHead_0186",
    "neckA_face_root",
    "FACIAL_C_Neck1Root",
    "FACIAL_C_NeckB",
    "FACIAL_L_NeckB1",
    "FACIAL_R_NeckB1",
    "FACIAL_L_NeckB2",
    "FACIAL_R_NeckB2",
    "FACIAL_L_NeckB3",
    "FACIAL_R_NeckB3",
    "FACIAL_L_NeckB4",
    "FACIAL_R_NeckB4",
    "FACIAL_C_12IPV_NeckB1",
    "FACIAL_C_12IPV_NeckB2",
    "FACIAL_L_12IPV_NeckB3",
    "FACIAL_R_12IPV_NeckB3",
    "FACIAL_L_12IPV_NeckB4",
    "FACIAL_R_12IPV_NeckB4",
    "FACIAL_L_12IPV_NeckB5",
    "FACIAL_R_12IPV_NeckB5",
    "FACIAL_L_12IPV_NeckB6",
    "FACIAL_R_12IPV_NeckB6",
    "FACIAL_L_12IPV_NeckB7",
    "FACIAL_R_12IPV_NeckB7",
    "FACIAL_L_12IPV_NeckB8",
    "FACIAL_R_12IPV_NeckB8",
    "FACIAL_L_12IPV_NeckB9",
    "FACIAL_R_12IPV_NeckB9",
    "FACIAL_L_12IPV_NeckB10",
    "FACIAL_R_12IPV_NeckB10",
    "FACIAL_L_12IPV_NeckB11",
    "FACIAL_R_12IPV_NeckB11",
    "FACIAL_L_12IPV_NeckB12",
    "FACIAL_R_12IPV_NeckB12",
    "FACIAL_C_NeckBackB",
    "FACIAL_L_NeckBackB",
    "FACIAL_R_NeckBackB",
    "FACIAL_C_12IPV_NeckBackB1",
    "FACIAL_C_12IPV_NeckBackB2",
    "FACIAL_L_12IPV_NeckBackB1",
    "FACIAL_R_12IPV_NeckBackB1",
    "FACIAL_L_12IPV_NeckBackB2",
    "FACIAL_R_12IPV_NeckBackB2",
}

SWJS_NeckB_bones = {
    "neckB",
    "neckB_face_root",
    "midHead_002",
    "midHead_0010",
    "leftHead_019",
    "leftHead_0157",
    "leftHead_0158",
    "leftHead_024",
    "leftHead_0161",
    "leftHead_0159",
    "leftHead_0160",
    "leftHead_0162",
    "rightHead_019",
    "rightHead_0157",
    "rightHead_0158",
    "rightHead_024",
    "rightHead_0161",
    "rightHead_0159",
    "rightHead_0160",
    "rightHead_0162",
    "FACIAL_C_Neck2Root",
    "FACIAL_C_AdamsApple",
    "FACIAL_C_12IPV_AdamsA1",
    "FACIAL_C_12IPV_AdamsA2",
    "FACIAL_L_NeckA1",
    "FACIAL_R_NeckA1",
    "FACIAL_L_NeckA2",
    "FACIAL_R_NeckA2",
    "FACIAL_L_NeckA3",
    "FACIAL_R_NeckA3",
    "FACIAL_L_NeckA4",
    "FACIAL_R_NeckA4",
    "FACIAL_L_12IPV_NeckA1",
    "FACIAL_R_12IPV_NeckA1",
    "FACIAL_L_12IPV_NeckA2",
    "FACIAL_R_12IPV_NeckA2",
    "FACIAL_L_12IPV_NeckA3",
    "FACIAL_R_12IPV_NeckA3",
    "FACIAL_L_12IPV_NeckA4",
    "FACIAL_R_12IPV_NeckA4",
    "FACIAL_L_12IPV_NeckA5",
    "FACIAL_R_12IPV_NeckA5",
    "FACIAL_L_12IPV_NeckA6",
    "FACIAL_R_12IPV_NeckA6",
    "FACIAL_L_12IPV_NeckA7",
    "FACIAL_R_12IPV_NeckA7",
    "FACIAL_L_12IPV_NeckA8",
    "FACIAL_R_12IPV_NeckA8",
    "FACIAL_L_12IPV_NeckA9",
    "FACIAL_R_12IPV_NeckA9",
    "FACIAL_C_NeckBackA",
    "FACIAL_L_NeckBackA",
    "FACIAL_R_NeckBackA",
    "FACIAL_C_12IPV_NeckBackA1",
    "FACIAL_C_12IPV_NeckBackA2",
    "FACIAL_L_12IPV_NeckBackA1",
    "FACIAL_R_12IPV_NeckBackA1",
    "FACIAL_L_12IPV_NeckBackA2",
    "FACIAL_R_12IPV_NeckBackA2",
}

SWJS_delete_bones = {
    "blender_implicit",
    "origin",
    "propC",
    "propC_end",
    "propB",
    "propB_end",
    "propA",
    "propA_end",
    "lightsaberB",
    "lightsaberB_end",
    "lightsaber",
    "lightsaber_end",
    "blasterB",
    "blasterB_end",
    "blaster",
    "blaster_end",
    "ref_navlink",
    "ref_navlink_end",
    "camera",
    "camera_end",
    "ref",
    "ref_end",
}

SWJS_Spine2_bones = {
    "spineC",
    "backpack",
    "backpack_hoseAttach",
    "hose",
    "hose_end",
    "hose1",
    "hose1_end",
    "hose2",
    "hose2_end",
    "hose3",
    "hose3_end",
    "hose4",
    "hose4_end",
    "hose5",
    "hose5_end",
    "hose6",
    "hose6_end",
    "hose7",
    "hose7_end",
    "hose8",
    "hose8_end",
    "hose9",
    "hose9_end",
    "hose10",
    "hose10_end",
    "hose11",
    "hose11_end",
    "hose12",
    "hose12_end",
    "hose13",
    "hose13_end",
    "hose14",
    "hose14_end",
    "hose15",
    "hose15_end",
    "hose16",
    "hose16_end",
    "hose17",
    "hose17_end",
    "hose18",
    "hose18_end",
    "hose19",
    "hose19_end",
    "r_jumpTrooper_hose_minorA",
    "r_jumpTrooper_hose_minorB",
    "r_jumpTrooper_hose_minorC",
    "r_jumpTrooper_hose_minorD",
    "r_jumpTrooper_hose_minorE",
    "r_jumpTrooper_hose_minorF",
    "r_jumpTrooper_hose_minorG",
    "r_jumpTrooper_hose_minorH",
    "r_jumpTrooper_hose_minorI",
    "r_jumpTrooper_hose_minorJ",
    "r_jumpTrooper_hose_minorK",
    "r_jumpTrooper_hose_minorL",
    "r_jumpTrooper_hose_minorM",
    "r_jumpTrooper_hose_minorN",
    "r_jumpTrooper_hose_minorO",
    "r_jumpTrooper_hose_minorP",
    "r_jumpTrooper_hose_minorP_end",
    "l_jumpTrooper_hose_minorA",
    "l_jumpTrooper_hose_minorB",
    "l_jumpTrooper_hose_minorC",
    "l_jumpTrooper_hose_minorD",
    "l_jumpTrooper_hose_minorE",
    "l_jumpTrooper_hose_minorF",
    "l_jumpTrooper_hose_minorG",
    "l_jumpTrooper_hose_minorH",
    "l_jumpTrooper_hose_minorI",
    "l_jumpTrooper_hose_minorJ",
    "l_jumpTrooper_hose_minorK",
    "l_jumpTrooper_hose_minorL",
    "l_jumpTrooper_hose_minorM",
    "l_jumpTrooper_hose_minorN",
    "l_jumpTrooper_hose_minorO",
    "l_jumpTrooper_hose_minorP",
    "l_jumpTrooper_hose_minorP_end",
    "l_holsterBack_lightsaberAttach",
    "l_holsterBack_lightsaberAttach_end",
    "r_holsterBack_lightsaberAttach",
    "r_holsterBack_lightsaberAttach_end",
    "l_holsterBack_blasterAttach",
    "l_holsterBack_blasterAttach_end",
    "r_holsterBack_blasterAttach",
    "r_holsterBack_blasterAttach_end",
    "l_holsterBack_lightsaberBAttach",
    "l_holsterBack_lightsaberBAttach_end",
    "r_holsterBack_lightsaberBAttach",
    "r_holsterBack_lightsaberBAttach_end",
    "l_holsterBack_blasterBAttach",
    "l_holsterBack_blasterBAttach_end",
    "r_holsterBack_blasterBAttach",
    "r_holsterBack_blasterBAttach_end",
    "l_armpit",
    "l_armpit_end",
    "r_armpit",
    "r_armpit_end",
    "l_armor_strap_attach",
    "r_armor_strap_attach",
    "chest_armor",
}

SWJS_Pelvis_bones = {
    "belt",
    "origin",
    "hip",
    "hip_offset" "bft_m_pouch_lg_root",
    "bft_l_pouch_lg_root",
    "bft_l_pouch_lg_ft_base",
    "bft_l_pouch_lg_bk_base",
    "bft_l_pouch_lg_ft_tip",
    "bft_l_pouch_lg_ft_tip_end",
    "bft_l_pouch_lg_bk_mid",
    "holster_lightsaber",
    "holster_lightsaberAttach",
    "holster_lightsaberAttach_end",
    "holster_blaster",
    "holster_blasterAttach",
    "holster_blasterAttach_end",
    "r_magazinePouch",
    "r_magazinePouch_end",
    "r_magazinePouch_end_end",
    "l_magazinePouch",
    "l_magazinePouch_end",
    "l_magazinePouch_end_end",
    "l_magazinePouch",
    "l_magazinePouch_end",
    "l_magazinePouch_end_end",
    "holster_1",
    "holster_2",
    "holster_2_end",
}

SWJS_hand_bones_right = {
    "r_wrist",
    "r_wristEnd",
    "r_wristEnd_end",
    "r_finIndexCarpal",
    "r_finMidCarpal",
    "r_finRingCarpal",
    "r_finPinkyCarpal",
    "r_elbow_segment_3_end",
    "r_hand_blasterAttach",
    "r_hand_blasterAttach_end",
    "r_hand_lightsaberAttach",
    "r_hand_lightsaberAttach_end",
    "r_hand_blasterBAttach",
    "r_hand_blasterBAttach_end",
    "r_hand_lightsaberBAttach",
    "r_hand_lightsaberBAttach_end",
    "r_hand_propAAttach",
    "r_hand_propAAttach_end",
    "r_hand_propBAttach",
    "r_hand_propBAttach_end",
    "r_hand_propCAttach",
    "r_hand_propCAttach_end",
    "r_finThumbCEnd",
    "r_finThumbCEnd_end",
    "r_finIndexCEnd",
    "r_finMidCEnd",
    "r_finRingCEnd",
    "r_finPinkyCEnd",
}

SWJS_hand_bones_left = {
    "l_wrist",
    "l_wristEnd",
    "l_wristEnd_end",
    "l_finIndexCarpal",
    "l_finMidCarpal",
    "l_finRingCarpal",
    "l_finPinkyCarpal",
    "l_elbow_segment_3_end",
    "l_hand_blasterAttach",
    "l_hand_blasterAttach_end",
    "l_hand_lightsaberAttach",
    "l_hand_lightsaberAttach_end",
    "l_hand_blasterBAttach",
    "l_hand_blasterBAttach_end",
    "l_hand_lightsaberBAttach",
    "l_hand_lightsaberBAttach_end",
    "l_hand_propAAttach",
    "l_hand_propAAttach_end",
    "l_hand_propBAttach",
    "l_hand_propBAttach_end",
    "l_hand_propCAttach",
    "l_hand_propCAttach_end",
    "l_finThumbCEnd",
    "l_finThumbCEnd_end",
    "l_finIndexCEnd",
    "l_finMidCEnd",
    "l_finRingCEnd",
    "l_finPinkyCEnd",
}

SWJS_forearm_bones_right = {
    "r_elbow",
    "r_elbow_segment_1",
    "r_elbow_segment_1_end",
    "r_elbow_segment_2",
    "r_elbow_segment_2_end",
    "r_elbow_segment_3",
    "r_elbow_segment_3_end",
    "r_elbow_segment_4",
    "r_elbow_segment_4_end",
    "r_elbow_segment_5",
    "r_elbow_segment_5_end",
}

SWJS_forearm_bones_left = {
    "l_elbow",
    "l_elbow_segment_1",
    "l_elbow_segment_1_end",
    "l_elbow_segment_2",
    "l_elbow_segment_2_end",
    "l_elbow_segment_3",
    "l_elbow_segment_3_end",
    "l_elbow_segment_4",
    "l_elbow_segment_4_end",
    "l_elbow_segment_5",
    "l_elbow_segment_5_end",
}

SWJS_upperarm_bones_right = {
    "r_shoulder",
    "r_shldrPad",
    "r_shoulder_segment_1",
    "r_shldr_auxA_bt",
    "r_shldr_auxA_bt_end",
    "r_shoulder_segment_2",
    "r_shoulder_segment_2_end",
    "r_shoulder_segment_3",
    "r_shoulder_segment_3_end",
    "r_shoulder_segment_4",
    "r_shoulder_segment_4_end",
    "r_shoulder_segment_5",
    "r_shoulder_segment_5_end",
    "r_elbowPad",
    "r_elbowPad_end",
    "r_shldr_auxA_root_50pct",
    "r_shldr_auxA_tp",
    "r_shldr_auxA_tp_end",
    "r_shldr_auxA_ft",
    "r_shldr_auxA_ft_end",
    "r_shldr_auxA_bk",
    "r_shldr_auxA_bk_end",
}

SWJS_upperarm_bones_left = {
    "l_shoulder",
    "l_shldrPad",
    "l_shoulder_segment_1",
    "l_shldr_auxA_bt",
    "l_shldr_auxA_bt_end",
    "l_shoulder_segment_2",
    "l_shoulder_segment_2_end",
    "l_shoulder_segment_3",
    "l_shoulder_segment_3_end",
    "l_shoulder_segment_4",
    "l_shoulder_segment_4_end",
    "l_shoulder_segment_5",
    "l_shoulder_segment_5_end",
    "l_elbowPad",
    "l_elbowPad_end",
    "l_shldr_auxA_root_50pct",
    "l_shldr_auxA_tp",
    "l_shldr_auxA_tp_end",
    "l_shldr_auxA_ft",
    "l_shldr_auxA_ft_end",
    "l_shldr_auxA_bk",
    "l_shldr_auxA_bk_end",
}

SWJS_clav_bones_left = {
    "l_clav",
    "l_shoulder_armor",
}

SWJS_hip_left = {
    "l_thigh",
    "l_thigh_segment_1",
    "l_thigh_segment_1_end",
    "l_thigh_segment_2",
    "l_thigh_segment_2_end",
    "l_thigh_segment_3",
    "l_thigh_segment_3_end",
    "l_thigh_segment_4",
    "l_thigh_segment_4_end",
    "l_thigh_segment_5",
    "l_thigh_segment_5_end",
    "l_knee_helper",
    "l_skirtA_sim",
    "l_skirtB_sim",
    "l_skirtC_sim",
    "l_skirtD_sim",
    "l_skirtE_sim",
    "l_bk_skirtA_sim",
    "l_bk_skirtB_sim",
    "l_bk_skirtC_sim",
    "l_bk_skirtD_sim",
    "l_bk_skirtE_sim",
}

SWJS_hip_right = {
    "r_thigh",
    "r_thigh_segment_1",
    "r_thigh_segment_1_end",
    "r_thigh_segment_2",
    "r_thigh_segment_2_end",
    "r_thigh_segment_3",
    "r_thigh_segment_3_end",
    "r_thigh_segment_4",
    "r_thigh_segment_4_end",
    "r_thigh_segment_5",
    "r_thigh_segment_5_end",
    "r_knee_helper",
    "r_bk_skirtA_sim",
    "r_bk_skirtB_sim",
    "r_bk_skirtC_sim",
    "r_bk_skirtD_sim",
    "r_bk_skirtE_sim",
    "r_skirtA_sim",
    "r_skirtB_sim",
    "r_skirtC_sim",
    "r_skirtD_sim",
    "r_skirtE_sim",
}

SWJS_calf_left = {
    "l_knee",
    "l_knee_segment_1",
    "l_knee_segment_1_end",
    "l_knee_segment_2",
    "l_knee_segment_2_end",
    "l_knee_segment_3",
    "l_knee_segment_3_end",
    "l_knee_segment_4",
    "l_knee_segment_4_end",
    "l_knee_segment_5",
    "l_knee_segment_5_end",
}

SWJS_calf_right = {
    "r_knee",
    "r_knee_segment_1",
    "r_knee_segment_1_end",
    "r_knee_segment_2",
    "r_knee_segment_2_end",
    "r_knee_segment_3",
    "r_knee_segment_3_end",
    "r_knee_segment_4",
    "r_knee_segment_4_end",
    "r_knee_segment_5",
    "r_knee_segment_5_end",
}

SWJS_toe_left = {"l_ball", "l_toe", "l_toe_end"}

SWJS_toe_right = {"r_ball", "r_toe", "r_toe_end"}

swtor_fc_bones = {
    "fc_jaw",
    "fc_lip_left_bottom",
    "fc_lip_center_bottom",
    "fc_lip_right_bottom",
    "fc_lip_right_corner",
    "fc_lip_left_corner",
    "fc_lip_left_top",
    "fc_lip_center_top",
    "fc_lip_right_top",
    "fc_tongue",
    "fc_puffer_left",
    "fc_puffer_right",
    "fc_nose_left",
    "fc_nose_right",
    "fc_cheek_inner_right",
    "fc_cheek_inner_left",
    "fc_cheek_left",
    "fc_cheek_right",
    "fc_lid_right_bottom",
    "fc_lid_left_bottom",
    "fc_eye_left",
    "fc_eye_right",
    "fc_lid_left_top",
    "fc_lid_right_top",
    "fc_brow_left_2",
    "fc_brow_left_1",
    "fc_brow_mid",
    "fc_brow_right_1",
    "fc_brow_right_2",
    "Head",
    "Neck1",
}

swtor_forearm_bones_right = {"RightUlna", "RightElbow"}
swtor_forearm_bones_left = {"LeftUlna", "LeftElbow"}

swtor_upperarm_bones_right = {
    "RightShoulder",
    "RightShoulderTwist1",
    "RightBlendShoulder",
}
swtor_upperarm_bones_left = {
    "LeftShoulder",
    "LeftShoulderTwist1",
    "LeftBlendShoulder",
}

swtor_hip_left = {"LeftHip", "LeftHipTwist1"}
swtor_hip_right = {"RightHip", "RightHipTwist1"}

jka_humerus_l_group = {"lhumerus", "lhumerusX"}
jka_humerus_r_group = {"rhumerus", "rhumerusX"}

jka_radius_l_group = {"lradius", "lradiusX"}
jka_radius_r_group = {"rradius", "rradiusX"}

jka_thigh_l_group = {"ltail", "lfemurYZ", "lfemurX"}
jka_thigh_r_group = {"rtail", "rfemurYZ", "rfemurX"}

jka_fc_group = {
    "face",
    "cranium",
    "jaw",
    "ceyebrow",
    "lblip2",
    "leye",
    "rblip2",
    "ltlip2",
    "rtlip2",
    "reye",
}

bungie_fc_bones = {
    "Cheekbone.L",
    "UpperEyelid.L",
    "LowerEyelid.L",
    "LowerEyelid.L",
    "Nostril_.L",
    "UpperLip_4",
    "UpperLip_5",
    "NasalLobe.L",
    "Nostril_2.L",
    "Cheek.R",
    "Cheek.L",
    "Jawline_1.R",
    "Jawline_1.L",
    "Nose",
    "",
    "UnderEye.R",
    "Cheekbone.R",
    "LowerEyelid.R",
    "Nostril_1.R",
    "UpperEyelid.R",
    "UpperLip_2",
    "UpperLip_1",
    "NasalLobe.R",
    "Nostril_2.R",
    "Chin",
    "LowerLip_3",
    "LowerLip_4",
    "LowerLip_5",
    "Jawline_2.L",
    "LowerLip_2",
    "LowerLip_1",
    "Jawline_2.R",
    "Neck_2",
    "Jaw",
    "Head",
    "Tongue",
    "Brow_2.R",
    "Brow_2.L",
    "Brow_3.R",
    "Brow_3.L",
    "Brow_1.L",
    "Brow_1.R",
    "UnderEye.L",
    "UpperLip_3",
    "Jawline_.L",
}

bungie_hand_l_groups = {"Wrist_Twist_Fixup.L", "Hand.L"}
bungie_hand_r_groups = {"Wrist_Twist_Fixup.R", "Hand.R"}


swbf_fc_bones = {
    "Head",
    "HeadEnd",
    "Face",
    "Jaw",
    "LeftLowerLip",
    "LeftLowerInnerLip",
    "LowerLip",
    "LowerInnerLip",
    "RightLowerLip",
    "RightLowerInnerLip",
    "Tongue",
    "TongueTip",
    "Chin",
    "LeftLowCheek",
    "RightLowCheek",
    "LeftEye",
    "LeftIris",
    "RightEye",
    "RightIris",
    "LeftUpCheek",
    "LeftUpInnerCheek",
    "RightUpInnerCheek",
    "RightUpCheek",
    "LeftCheek",
    "RightCheek",
    "LeftMouth",
    "LeftInnerMouth",
    "LeftMiddleCrease",
    "LeftUpperLip",
    "LeftUpperInnerLip",
    "UpperLip",
    "UpperInnerLip",
    "RightUpperLip",
    "RightUpperInnerLip",
    "RightMouth",
    "RightInnerMouth",
    "RightMiddleCrease",
    "LeftUpEyelid",
    "RightUpEyelid",
    "LeftLowEyelid",
    "RightLowEyelid",
    "LeftInnerEyebrow",
    "LeftOuterEyebrow",
    "RightInnerEyebrow",
    "RightOuterEyebrow",
    "LeftNose",
    "RightNose",
    "LeftCrease",
    "RightCrease",
    "LeftLowMiddleEyebrow",
    "RightMiddleEyebrow",
    "LeftLowEyelidCrease",
    "LeftLowOuterEyebrow",
    "NoseTip",
    "RightLowOuterEyebrow",
    "LeftMiddleEyebrow",
    "RightLowMiddleEyebrow",
    "RightLowEyelidCrease",
    "LowNose",
    "Head_Phys_Base01",
    "Head_Phys_01",
    "Hair_01_Base",
    "Hair_01_Extra01",
    "Hair_01_Extra02",
    "Hair_02_Base",
    "Hair_02_Extra01",
    "Hair_02_Extra02",
    "Hair_03_Base",
    "Hair_03_Extra01",
    "Hair_03_Extra02",
    "Hair_04_Base",
    "Hair_04_Extra01",
    "Hair_04_Extra02",
    "Hair_05_Base",
    "Hair_05_Extra01",
    "Hair_05_Extra02",
    "Hair_05_Extra03",
    "Hair_06_Base",
    "Hair_06_Extra01",
    "Hair_06_Extra02",
    "Hair_06_Extra03",
    "Hair_07_Base",
    "Hair_07_Extra01",
    "Hair_07_Extra02",
    "Hair_08_Base",
    "Hair_08_Extra01",
    "Hair_08_Extra02",
    "Hair_08_Extra03",
    "FACIAL_C_FacialRoot",
    "FACIAL_LOD1_C_Forehead",
    "FACIAL_LOD1_C_Forehead_end",
    "FACIAL_LOD1_L_ForeheadIn",
    "FACIAL_LOD1_L_ForeheadIn_end",
    "FACIAL_LOD1_R_ForeheadIn",
    "FACIAL_LOD1_R_ForeheadIn_end",
    "FACIAL_LOD1_L_ForeheadMid",
    "FACIAL_LOD1_L_ForeheadMid_end",
    "FACIAL_LOD1_R_ForeheadMid",
    "FACIAL_LOD1_R_ForeheadMid_end",
    "FACIAL_LOD1_L_ForeheadOut",
    "FACIAL_LOD1_L_ForeheadOut_end",
    "FACIAL_LOD1_R_ForeheadOut",
    "FACIAL_LOD1_R_ForeheadOut_end",
    "FACIAL_LOD1_L_EyesackUpper",
    "FACIAL_LOD1_L_EyesackUpper_end",
    "FACIAL_LOD1_R_EyesackUpper",
    "FACIAL_LOD1_R_EyesackUpper_end",
    "FACIAL_LOD1_L_EyelidUpperFurrow",
    "FACIAL_LOD1_L_EyelidUpperFurrow_end",
    "FACIAL_LOD1_R_EyelidUpperFurrow",
    "FACIAL_LOD1_R_EyelidUpperFurrow_end",
    "FACIAL_LOD1_L_EyelidUpper",
    "FACIAL_LOD1_L_EyelidUpper_end",
    "FACIAL_LOD1_R_EyelidUpper",
    "FACIAL_LOD1_R_EyelidUpper_end",
    "FACIAL_LOD1_L_Eyeball",
    "FACIAL_LOD1_L_Pupil",
    "FACIAL_LOD1_L_Pupil_end",
    "FACIAL_LOD1_R_Eyeball",
    "FACIAL_LOD1_R_Pupil",
    "FACIAL_LOD1_R_Pupil_end",
    "FACIAL_LOD1_L_EyelidLower",
    "FACIAL_LOD1_L_EyelidLower_end",
    "FACIAL_LOD1_R_EyelidLower",
    "FACIAL_LOD1_R_EyelidLower_end",
    "FACIAL_LOD1_L_EyesackLower",
    "FACIAL_LOD1_L_EyesackLower_end",
    "FACIAL_LOD1_R_EyesackLower",
    "FACIAL_LOD1_R_EyesackLower_end",
    "FACIAL_LOD1_L_CheekInner",
    "FACIAL_LOD1_L_CheekInner_end",
    "FACIAL_LOD1_R_CheekInner",
    "FACIAL_LOD1_R_CheekInner_end",
    "FACIAL_LOD1_L_CheekOuter",
    "FACIAL_LOD1_L_CheekOuter_end",
    "FACIAL_LOD1_R_CheekOuter",
    "FACIAL_LOD1_R_CheekOuter_end",
    "FACIAL_LOD1_C_NoseBridge",
    "FACIAL_LOD1_C_NoseBridge_end",
    "FACIAL_LOD1_L_NasolabialBulge",
    "FACIAL_LOD1_L_NasolabialBulge_end",
    "FACIAL_LOD1_R_NasolabialBulge",
    "FACIAL_LOD1_R_NasolabialBulge_end",
    "FACIAL_LOD1_L_NasolabialFurrow",
    "FACIAL_LOD1_L_NasolabialFurrow_end",
    "FACIAL_LOD1_R_NasolabialFurrow",
    "FACIAL_LOD1_R_NasolabialFurrow_end",
    "FACIAL_LOD1_L_CheekLower",
    "FACIAL_LOD1_L_CheekLower_end",
    "FACIAL_LOD1_R_CheekLower",
    "FACIAL_LOD1_R_CheekLower_end",
    "FACIAL_LOD1_L_Ear",
    "FACIAL_LOD1_L_Ear_end",
    "FACIAL_LOD1_R_Ear",
    "FACIAL_LOD1_R_Ear_end",
    "FACIAL_LOD1_C_Nose",
    "FACIAL_LOD1_C_NoseLower",
    "FACIAL_LOD1_C_NoseLower_end",
    "FACIAL_LOD1_L_Nostril",
    "FACIAL_LOD1_L_Nostril_end",
    "FACIAL_LOD1_R_Nostril",
    "FACIAL_LOD1_R_Nostril_end",
    "FACIAL_LOD1_C_Mouth",
    "FACIAL_LOD1_C_LipUpper",
    "FACIAL_LOD1_C_LipUpperInner",
    "FACIAL_LOD1_C_LipUpperInner_end",
    "FACIAL_LOD1_L_LipUpper",
    "FACIAL_LOD1_L_LipUpperInner",
    "FACIAL_LOD1_L_LipUpperInner_end",
    "FACIAL_LOD1_R_LipUpper",
    "FACIAL_LOD1_R_LipUpperInner",
    "FACIAL_LOD1_R_LipUpperInner_end",
    "FACIAL_LOD1_L_LipUpperOuter",
    "FACIAL_LOD1_L_LipUpperOuterInner",
    "FACIAL_LOD1_L_LipUpperOuterInner_end",
    "FACIAL_LOD1_R_LipUpperOuter",
    "FACIAL_LOD1_R_LipUpperOuterInner",
    "FACIAL_LOD1_R_LipUpperOuterInner_end",
    "FACIAL_LOD1_L_LipCorner",
    "FACIAL_LOD1_L_LipCornerInner",
    "FACIAL_LOD1_L_LipCornerInner_end",
    "FACIAL_LOD1_R_LipCorner",
    "FACIAL_LOD1_R_LipCornerInner",
    "FACIAL_LOD1_R_LipCornerInner_end",
    "FACIAL_LOD1_C_LipLower",
    "FACIAL_LOD1_C_LipLowerInner",
    "FACIAL_LOD1_C_LipLowerInner_end",
    "FACIAL_LOD1_L_LipLower",
    "FACIAL_LOD1_L_LipLowerInner",
    "FACIAL_LOD1_L_LipLowerInner_end",
    "FACIAL_LOD1_R_LipLower",
    "FACIAL_LOD1_R_LipLowerInner",
    "FACIAL_LOD1_R_LipLowerInner_end",
    "FACIAL_LOD1_L_LipLowerOuter",
    "FACIAL_LOD1_L_LipLowerOuterInner",
    "FACIAL_LOD1_L_LipLowerOuterInner_end",
    "FACIAL_LOD1_R_LipLowerOuter",
    "FACIAL_LOD1_R_LipLowerOuterInner",
    "FACIAL_LOD1_R_LipLowerOuterInner_end",
    "FACIAL_LOD1_C_Jaw",
    "FACIAL_LOD1_C_Chin",
    "FACIAL_LOD1_C_Chin_end",
    "FACIAL_LOD1_L_ChinSide",
    "FACIAL_LOD1_L_ChinSide_end",
    "FACIAL_LOD1_R_ChinSide",
    "FACIAL_LOD1_R_ChinSide_end",
    "FACIAL_LOD1_C_Tongue1",
    "FACIAL_LOD1_C_Tongue2",
    "FACIAL_LOD1_C_Tongue3",
    "FACIAL_LOD1_C_Tongue4",
    "FACIAL_LOD1_C_Tongue4_end",
    "FACIAL_LOD1_L_Masseter",
    "FACIAL_LOD1_L_Masseter_end",
    "FACIAL_LOD1_R_Masseter",
    "FACIAL_LOD1_R_Masseter_end",
    "FACIAL_LOD1_C_UnderChin",
    "FACIAL_LOD1_C_UnderChin_end",
    "FACIAL_LOD1_L_UnderChin",
    "FACIAL_LOD1_L_UnderChin_end",
    "FACIAL_LOD1_R_UnderChin",
    "FACIAL_LOD1_R_UnderChin_end",
}

swbf_NeckA_bones = {
    "Neck",
    "Wep2_Root",
}

swbf_NeckB_bones = {
    "Neck1",
    "Throat",
    "HeadRoll",
    "FACIAL_C_Neck2Root",
    "FACIAL_LOD1_C_AdamsApple",
    "FACIAL_LOD1_C_AdamsApple_end",
}

swbf_delete_bones = {}

swbf_spine2_bones = {
    "Spine2",
    "Spine2_Phys",
    "Spine2_Phys_Ext_Base01",
    "Spine2_Phys_Ext_01",
    "Spine2_Phys_Ext_Base02",
    "Spine2_Phys_Ext_02",
    "Spine2_Phys_Ext_Base03",
    "Spine2_Phys_Ext_03",
    "Spine2_Phys_Ext_Base04",
    "Spine2_Phys_Ext_04",
    "Backpack_Phys_Base01",
    "Backpack_Phys_01",
    "Backpack_Phys_Ext_Base01",
    "Backpack_Phys_Ext_01",
    "Backpack_Phys_Ext_Base02",
    "Backpack_Phys_Ext_02",
    "Backpack_Phys_Ext_Base03",
    "Backpack_Phys_Ext_03",
    "Backpack_Phys_Ext_Base04",
    "Backpack_Phys_Ext_04",
    "Backpack_Phys_Weapon_Base01",
    "Backpack_Phys_Weapon_01",
    "LeftArmpit",
    "LeftDeltoidBulge",
    "RightArmpit",
    "RightDeltoidBulge",
    "Wep_Root",
    "Wep_Trigger",
    "Wep_Slide",
    "Wep_Grenade1",
    "Wep_Grenade2",
    "Wep_Mag",
    "Wep_Mag_Ammo",
    "Wep_Mag_Extra1",
    "Wep_Scope1",
    "Wep_Scope2",
    "Wep_Belt1",
    "Wep_Belt2",
    "Wep_Belt3",
    "Wep_Belt4",
    "Wep_Belt5",
    "Wep_Bipod1",
    "Wep_Bipod2",
    "Wep_Bipod3",
    "IK_Joint_LeftHand",
    "IK_Joint_RightHand",
    "Wep_Physic1",
    "Wep_Physic2",
    "Wep_Physic3",
    "Wep_Extra1",
    "Wep_Extra2",
    "Wep_Extra3",
    "Wep_Extra4",
    "Wep_Muzzle",
    "Wep_ButtStock",
    "Wep_Lag",
    "Wep_Aim",
    "NeckCollar",
}

swbf_spine1_bones = {
    "Spine1",
    "Spine1_Phys",
    "Spine1_Phys_Ext_Base01",
    "Spine1_Phys_Ext_01",
    "Spine1_Phys_Ext_Base02",
    "Spine1_Phys_Ext_02",
    "Spine1_Phys_Ext_Base03",
    "Spine1_Phys_Ext_03",
    "Spine1_Phys_Ext_Base04",
    "Spine1_Phys_Ext_04",
    "Spine_Phys",
}

swbf_spine_bones = {
    "Spine",
    "Spine_Phys",
    "Spine_Phys_Ext_Base01",
    "Spine_Phys_Ext_01",
    "Spine_Phys_Ext_Base02",
    "Spine_Phys_Ext_02",
    "Spine_Phys_Ext_Base03",
    "Spine_Phys_Ext_03",
    "Spine_Phys_Ext_Base04",
    "Spine_Phys_Ext_04",
    "Spine_Phys_Weapon_Base01",
    "Spine_Phys_Weapon_01",
}

swbf_Skirt_bones = {}

swbf_Pelvis_bones = {
    "Hips",
    "Hips_Phys",
    "Hips_Phys_Ext_Base01",
    "Hips_Phys_Ext_01",
    "Hips_Phys_Ext_Base02",
    "Hips_Phys_Ext_02",
    "Hips_Phys_Ext_Base03",
    "Hips_Phys_Ext_03",
    "Hips_Phys_Ext_Base04",
    "Hips_Phys_Ext_04",
    "Hips_Phys_Ext_Base05",
    "Hips_Phys_Ext_05",
    "Hips_Phys_Ext_Base06",
    "Hips_Phys_Ext_06",
    "LeftHipsRoll",
    "RightHipsRoll",
    "AITrajectory",
    "Trajectory",
    "TrajectoryEnd",
    "CameraBase",
    "CameraJoint",
    "Connect",
    "ConnectEnd",
    "Ground",
    "blender_implicit",
}

swbf_index_bones_right = {
    "RightHandIndex3",
    "RightHandIndex4",
}

swbf_index_bones_left = {
    "LeftHandIndex3",
    "LeftHandIndex4",
}

swbf_hand_bones_right = {
    "RightHand",
    "RightHandRing0",
    "RightHandPinky0",
    "RightHandIndex0",
    "RightHandThumb1",
    "RightHandMiddle0",
    "RightHandRing4",
    "RightHandPinky4",
    "RightHandMiddle4",
    "RightHand_Phys_Base01",
    "RightHand_Phys_01",
    "RightHandAttach",
}

swbf_hand_bones_left = {
    "LeftHand",
    "LeftHandRing0",
    "LeftHandPinky0",
    "LeftHandIndex0",
    "LeftHandThumb1",
    "LeftHandMiddle0",
    "LeftHandRing4",
    "LeftHandPinky4",
    "LeftHandMiddle4",
    "LeftHand_Phys_Base01",
    "LeftHand_Phys_01",
    "LeftHandAttach",
}

swbf_forearm_bones_right = {
    "RightForeArm",
    "RightForeArmRoll",
    "RightForeArmRoll1",
    "RightForeArmRoll2",
}

swbf_forearm_bones_left = {
    "LeftForeArm",
    "LeftForeArmRoll",
    "LeftForeArmRoll1",
    "LeftForeArmRoll2",
}

swbf_upperarm_bones_right = {
    "RightArm",
    "RightArmRoll",
    "RightArm_Phys_Base01",
    "RightArm_Phys_01",
    "RightElbowRoll",
    "RightArmRoll1",
    "RightArmBend",
}

swbf_upperarm_bones_left = {
    "LeftArm",
    "LeftArmRoll",
    "LeftArm_Phys_Base01",
    "LeftArm_Phys_01",
    "LeftElbowRoll",
    "LeftArmRoll1",
    "LeftArmBend",
}

swbf_hip_left = {
    "LeftUpLeg",
    "LeftUpLeg_Phys_Base01",
    "LeftUpLeg_Phys_01",
    "LeftKneeUp",
    "LeftUpLegRoll",
    "LeftKneeRoll",
}

swbf_hip_right = {
    "RightUpLeg",
    "RightUpLeg_Phys_Base01",
    "RightUpLeg_Phys_01",
    "RightKneeUp",
    "RightUpLegRoll",
    "RightKneeRoll",
}

swbf_calf_left = {
    "LeftLeg",
    "LeftLeg_Phys_Base01",
    "LeftLeg_Phys_01",
    "LeftKneeLow",
    "LeftKneeRoll",
}

swbf_calf_right = {
    "RightLeg",
    "RightLeg_Phys_Base01",
    "RightLeg_Phys_01",
    "RightKneeLow",
    "RightKneeRoll",
}

swbf_toe_left = {
    "LeftToeBase",
    "LeftToe",
}

swbf_toe_right = {
    "RightToeBase",
    "RightToe",
}

fortnite_fc_bones = {
    "head neck upper",
    "unusedfaceAttach",
    "head eyebrow center",
    "head eyebrow left 1",
    "head eyebrow left 2",
    "head cheek left",
    "head lip upper middle",
    "head lip upper left",
    "head lip corner left",
    "head nose bridge",
    "head eyebrow right 1",
    "head eyebrow right 2",
    "head cheek right",
    "head lip corner right",
    "head jaw",
    "head lip lower left",
    "head lip lower middle",
    "head lip lower right",
    "head teeth lower",
    "head tongue",
    "head eyeball right",
    "head eyeball left",
    "head teeth upper",
    "head lip upper right",
    "head eyelid right upper",
    "head eyelid right lower",
    "head eyelid left upper",
    "head eyelid left lower",
    "hair braid a",
    "helmet lower root",
    "head fur front left",
    "head fur front middle",
    "head fur front right",
    "head fur right a",
    "head fur right b",
    "head fur left d",
    "head fur left c",
    "head fur left b",
    "head fur left a",
    "braid front left a",
    "braid front right 1a",
    "braid front right 2a",
    "braid back left 1a",
    "braid back right a",
    "braid back left 2a",
}

fortnite_neck_bones = {
    "head neck lower",
    "head neck middle",
}

fortnite_spine4_bones = {
    "spine 5",
    "hair braid b",
    "hair braid c",
    "hair braid d",
    "hair braid e",
    "fur front right",
    "fur front left a",
    "fur front left b",
    "bandolier front middle",
    "bandolier back middle",
    "fur back top",
    "bandolier front left a",
    "bandolier front left b",
    "bandolier front left c",
    "bandolier back left a",
    "bandolier back left b",
    "bandolier back left c",
    "bandolier front right a",
    "bandolier front right b",
    "bandolier front right c",
    "bandolier back right a",
    "bandolier back right b",
    "bandolier back right c",
    "braid front left b",
    "braid front left c",
    "braid front left d",
    "braid front right 1b",
    "braid front right 1c",
    "braid front right 1d",
    "braid front right 2b",
    "braid front right 2c",
    "braid front right 2d",
    "braid back left 1b",
    "braid back left 1c",
    "braid back left 1d",
    "braid back right b",
    "braid back right c",
    "braid back right d",
    "braid back left 2b",
    "braid back left 2c",
    "braid back left 2d",
    "braid back left 2e",
}

fortnite_spine2_bones = {
    "spine 3",
    "spine 4",
    "fur front middle a",
    "fur front middle b",
    "fur back middle a",
    "fur back middle b",
    "fur front middle c",
    "fur front middle d",
}

fortnite_spine_bones = {
    "spine 1",
}

fortnite_Pelvis_bones = {
    "root ground",
    "root hips",
    "pelvis",
    "belt feather 1a",
    "belt feather 1b",
    "belt feather 1c",
    "belt feather 1d",
    "belt feather 1e",
    "belt feather 2a",
    "belt feather 2b",
    "belt feather 2c",
    "belt feather 2d",
    "belt feather 2e",
    "belt pouch",
    "belt buckle",
    "fur thigh left d",
    "fur thigh left c",
    "fur thigh left b",
    "fur thigh left g",
    "fur thigh left a",
    "pouch root",
}

fortnite_hand_bones_right = {
    "arm right wrist",
    "arm right metacarpal 1",
    "arm right metacarpal 2",
    "arm right metacarpal 4",
    "arm right metacarpal 3",
    "fur wrist right d",
}

fortnite_hand_bones_left = {
    "arm left wrist",
    "arm left metacarpal 1",
    "arm left metacarpal 2",
    "arm left metacarpal 4",
    "arm left metacarpal 3",
    "fur wrist left f",
}

fortnite_forearm_bones_right = {
    "arm right elbow",
    "arm right wrist twist",
    "arm right elbow twist",
    "fur wrist right a",
    "fur wrist right b",
    "fur wrist right c",
    "fur wrist right e",
    "fur elbow right c",
    "fur elbow right a",
    "fur elbow right b",
}

fortnite_forearm_bones_left = {
    "arm left elbow",
    "arm left wrist twist",
    "arm left elbow twist",
    "fur wrist left c",
    "fur wrist left b",
    "fur wrist left a",
    "fur wrist left d",
    "fur wrist left e",
    "fur elbow left d",
    "arm left elbow back adj",
    "fur elbow left b",
    "fur elbow left c",
    "fur elbow left a",
}

fortnite_upperarm_bones_right = {
    "arm right shoulder 2",
    "arm right shoulder twist 1",
    "arm right shoulder twist 2",
    "arm right deltoid adj",
    "arm right shoulder pad",
    "fur shoulder right a",
    "arm right elbow front adj",
    "arm right elbow back adj",
    "fur shoulder right b",
}

fortnite_upperarm_bones_left = {
    "arm left shoulder 2",
    "arm left shoulder twist 1",
    "arm left shoulder twist 2",
    "arm left deltoid adj",
    "arm left shoulder pad",
    "fur shoulder left a",
    "arm left elbow front adj",
    "fur shoulder left b",
}

fortnite_clavicle_bones_right = {
    "arm right shoulder 1",
    "arm right pectoral adj",
}

fortnite_clavicle_bones_left = {
    "arm left pectoral adj",
    "arm left shoulder 1",
}

fortnite_hip_left = {
    "leg left thigh",
    "leg left thigh twist",
    "jacket front left a",
    "jacket front left b",
    "jacket front left c",
    "jacket back left 1a",
    "jacket back left 1b",
    "jacket back left 1c",
    "jacket back left 2a",
    "jacket back left 2b",
    "jacket back left 2c",
    "jacket left a",
    "jacket left b",
    "jacket left c",
    "leg left butt adj",
    "leg left thigh front adj",
    "fur thigh left f",
    "fur thigh left e",
    "fur thigh left h",
    "fur thigh left i",
    "fur thigh left k",
    "fur thigh left j",
    "leg left knee back adj",
    "leg left knee front adj",
    "fur knee left a",
}

fortnite_hip_right = {
    "leg right thigh",
    "leg right thigh twist",
    "jacket front right a",
    "jacket front right b",
    "jacket front right c",
    "jacket back right 2a",
    "jacket back right 2b",
    "jacket back right 2c",
    "jacket back right 1a",
    "jacket back right 1b",
    "jacket back right 1c",
    "jacket right a",
    "jacket right b",
    "jacket right c",
    "holster root",
    "leg right butt adj",
    "leg right thigh front adj",
    "fur thigh right b",
    "fur thigh right a",
    "fur thigh right f",
    "fur thigh right c",
    "fur thigh right d",
    "fur thigh right e",
    "leg right knee back adj",
    "leg right knee front adj",
    "fur knee right a",
}

fortnite_calf_left = {
    "leg left knee",
    "leg left ankle twist",
    "fur knee left e",
    "leg left knee twist",
    "fur knee left c",
    "fur knee left b",
    "fur knee left d",
}

fortnite_calf_right = {
    "leg right knee",
    "leg right ankle twist",
    "fur knee right d",
    "fur knee right e",
    "leg right knee twist",
    "fur knee right b",
    "fur knee right c",
}

fortnite_ankle_left = {
    "leg left ankle",
    "fur ankle left a",
    "fur ankle left b",
    "fur ankle left d",
    "fur ankle left c",
}

fortnite_ankle_right = {
    "leg right ankle",
    "fur ankle right c",
    "fur ankle right b",
    "fur ankle right d",
    "fur ankle right a",
}


class EZPAINT_OT_ReweightModel(bpy.types.Operator):
    bl_idname = "object.ezpaint_reweight"
    bl_label = "ezPaint | Automatic Weightpaint"
    bl_description = "Automatically convert model weights to be used in the Source Engine"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        selected_game = bpy.context.scene.ezpaint_opts.game_type

        act_obj = context.active_object
        v_groups = act_obj.vertex_groups

        def merge_groups(group_input, final_name, act_obj):

            group_lookup = {g.index: g.name for g in v_groups}
            group_candidates = {n for n in group_lookup.values() if n in group_input}

            # test whether all candidates are components of group_lookup
            if all(n in group_lookup.values() for n in group_candidates):
                pass

            # general tests
            if (
                    len(group_candidates)
                    and act_obj.type == "MESH"
                    and bpy.context.mode == "OBJECT"
            ):

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
                    if vertex_weights[key] > 1.0:
                        vertex_weights[key] = 1.0
                # if (vertex_weights[key] < 0.3): vertex_weights[key] = 0.0
                # create new vertex group
                vgroup = act_obj.vertex_groups.new(name=final_name)

                # combine values into the group
                for key, value in vertex_weights.items():
                    vgroup.add([key], value, "REPLACE")  # options are 'ADD','SUBTRACT', 'REPLACE'

                # cleans up duplicates, adapted from https://blender.stackexchange.com/questions/134587/
                vgs = [vg for vg in act_obj.vertex_groups if vg.name in group_input]
                while vgs:
                    act_obj.vertex_groups.remove(vgs.pop())

        def swtor_fixups(act_obj):
            # Scaling factors may not be completely accurate
            act_obj.scale = (330, 330, 330)

            prefix = act_obj.name[:3]
            prefixes = ("bms", "bmf", "bmn", "bma", "bfn", "bfs")

            has_swtor_skels = bpy.context.scene.ezpaint_opts.has_swtor_skels
            if has_swtor_skels:
                if prefix in prefixes:
                    skeleton = act_obj.modifiers.new(name="Armature", type="ARMATURE")
                    skelobj = bpy.data.objects[
                        "bfb_armature"
                    ]  # This is because the armature cannot be null post modifier application. It gets replaced immediately (unless bfb is the correct prefix)
                    armature_name = prefix + "_armature"
                    skelobj = bpy.data.objects[armature_name]
                    skeleton.object = skelobj
                    skelobj.hide_set(False)

            merge_groups(swtor_fc_bones, "headgroup", act_obj)

            merge_groups(swtor_forearm_bones_right, "rforearm", act_obj)
            merge_groups(swtor_forearm_bones_left, "lforearm", act_obj)

            merge_groups(swtor_upperarm_bones_left, "lshoulder", act_obj)
            merge_groups(swtor_upperarm_bones_right, "rshoulder", act_obj)

            merge_groups(swtor_hip_left, "lhip", act_obj)
            merge_groups(swtor_hip_right, "rhip", act_obj)

            fix_swtor_matnames = bpy.context.scene.ezpaint_opts.fix_swtor_matnames

            if fix_swtor_matnames:
                # This prevents duplicate material names, which Source does not support
                # It also guesses material names based on mesh names,
                # since sometimes single mesh objects in SW:TOR have matching material names.
                # Only enable this if you know what you are doing.
                if act_obj.active_material.name == "default":
                    new_mat = act_obj.active_material.copy()
                    act_obj.active_material = new_mat
                    new_mat.name = act_obj.name + "_v01"

        def jka_fixups(act_obj):
            act_obj.scale = (11, 11, 11)

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
                new_mat.name = new_mat.name[15:-8]  # Slices the file extension off

        def bungie_smalldef_fixups(act_obj):
            act_obj.scale = (38, 38, 38)
            # Bungie group merges
            merge_groups(bungie_fc_bones, "bg_headgroup", act_obj)
            merge_groups(bungie_hand_l_groups, "bg_handlgroup", act_obj)
            merge_groups(bungie_hand_r_groups, "bg_handrgroup", act_obj)

        def swjs_fixups_helper(act_obj):
            merge_groups(SWJS_fc_bones, "headgroup", act_obj)
            
            merge_groups(SWJS_NeckA_bones, "neckagroup", act_obj)
            
            merge_groups(SWJS_NeckB_bones, "neckbgroup", act_obj)
            
            merge_groups(SWJS_Pelvis_bones, "pelivsgroup", act_obj)
            
            merge_groups(SWJS_Spine2_bones, "spine2group", act_obj)
            
            merge_groups(SWJS_hand_bones_right, "rhand", act_obj)
            merge_groups(SWJS_hand_bones_left, "lhand", act_obj)
            
            merge_groups(SWJS_forearm_bones_right, "rforearm", act_obj)
            merge_groups(SWJS_forearm_bones_left, "lforearm", act_obj)
            
            merge_groups(SWJS_upperarm_bones_left, "lshoulder", act_obj)
            merge_groups(SWJS_upperarm_bones_right, "rshoulder", act_obj)
            
            merge_groups(SWJS_clav_bones_left, "lclav", act_obj)
            
            merge_groups(SWJS_hip_left, "lhip", act_obj)
            merge_groups(SWJS_hip_right, "rhip", act_obj)
            
            merge_groups(SWJS_calf_left, "lcalf", act_obj)
            merge_groups(SWJS_calf_right, "rcalf", act_obj)
            
            merge_groups(SWJS_toe_left, "ltoe", act_obj)
            merge_groups(SWJS_toe_right, "rtoe", act_obj)


        def swjs_fixups(act_obj):
            # TODO: rewrite this to make more sense
            fbx_mode = bpy.context.scene.ezpaint_opts.fbx_mode
            if fbx_mode:
                # Used only for models from common SWJS FBX archives
                act_obj.scale = (0.38, 0.38, 0.38)
                act_obj.rotation_euler[0] = math.radians(
                    -0)  # If you ask me why this works I have no idea this shit fucked
                swjs_fixups_helper(act_obj)

            else:
                # Only use with direct rips from umodel!
                act_obj.scale = (38.5, 38.5, 38.5)
                # Only use with direct rips from umodel!
                swjs_fixups_helper(act_obj)

        def swbf_fixups(act_obj):

            # Only use with fbx models from common archives of SWBF models

            act_obj.scale = (40.5, 40.5, 40.5)

            act_obj.rotation_euler[0] = math.radians(90)

            # Only use with FBX models from common archives of SWBF models

            merge_groups(swbf_fc_bones, "headgroup", act_obj)

            merge_groups(swbf_NeckA_bones, "neckagroup", act_obj)

            merge_groups(swbf_NeckB_bones, "neckbgroup", act_obj)

            merge_groups(swbf_Pelvis_bones, "pelivsgroup", act_obj)

            merge_groups(swbf_spine2_bones, "spine2group", act_obj)

            merge_groups(swbf_spine1_bones, "spine1group", act_obj)

            merge_groups(swbf_spine_bones, "spinegroup", act_obj)

            merge_groups(swbf_index_bones_right, "rindex", act_obj)
            merge_groups(swbf_index_bones_left, "lindex", act_obj)

            merge_groups(swbf_hand_bones_right, "rhand", act_obj)
            merge_groups(swbf_hand_bones_left, "lhand", act_obj)

            merge_groups(swbf_forearm_bones_right, "rforearm", act_obj)
            merge_groups(swbf_forearm_bones_left, "lforearm", act_obj)

            merge_groups(swbf_upperarm_bones_left, "lshoulder", act_obj)
            merge_groups(swbf_upperarm_bones_right, "rshoulder", act_obj)

            merge_groups(swbf_hip_left, "lhip", act_obj)
            merge_groups(swbf_hip_right, "rhip", act_obj)

            merge_groups(swbf_calf_left, "lcalf", act_obj)
            merge_groups(swbf_calf_right, "rcalf", act_obj)

            merge_groups(swbf_toe_left, "ltoe", act_obj)
            merge_groups(swbf_toe_right, "rtoe", act_obj)
        
        def fortnite_fixups_helper(act_obj):
        
            merge_groups(fortnite_fc_bones, "headgroup", act_obj)
            
            merge_groups(fortnite_neck_bones, "neckgroup", act_obj)
            
            merge_groups(fortnite_spine4_bones, "spine4group", act_obj)
            
            merge_groups(fortnite_spine2_bones, "spine2group", act_obj)
            
            merge_groups(fortnite_spine_bones, "spinegroup", act_obj)
            
            merge_groups(fortnite_Pelvis_bones, "pelivsgroup", act_obj)
            
            merge_groups(fortnite_hand_bones_right, "rhand", act_obj)
            merge_groups(fortnite_hand_bones_left, "lhand", act_obj)
            
            merge_groups(fortnite_forearm_bones_right, "rforearm", act_obj)
            merge_groups(fortnite_forearm_bones_left, "lforearm", act_obj)
            
            merge_groups(fortnite_upperarm_bones_left, "lshoulder", act_obj)
            merge_groups(fortnite_upperarm_bones_right, "rshoulder", act_obj)
            
            merge_groups(fortnite_clavicle_bones_left, "lclavicle", act_obj)
            merge_groups(fortnite_clavicle_bones_right, "rclavicle", act_obj)
            
            merge_groups(fortnite_hip_left, "lhip", act_obj)
            merge_groups(fortnite_hip_right, "rhip", act_obj)
            
            merge_groups(fortnite_calf_left, "lcalf", act_obj)
            merge_groups(fortnite_calf_right, "rcalf", act_obj)
            
            merge_groups(fortnite_ankle_left, "lankle", act_obj)
            merge_groups(fortnite_ankle_right, "rankle", act_obj)
        
        def fortnite_fixups(act_obj):

            fortnite_female_armature = bpy.context.scene.ezpaint_opts.fortnite_female_armature

            if fortnite_female_armature:
                act_obj.scale = (44, 44, 44) # Female Fornite Models use a different armature compared to males requiring different scaling
                fortnite_fixups_helper(act_obj)
            else:
                act_obj.scale = (42.5, 42.5, 42.5) # Female Fornite Models use a different armature compared to males requiring different scaling
                fortnite_fixups_helper(act_obj)
                

        def reweight(v_groups, name_list):
            for n in name_list:
                if n[0] in v_groups:
                    v_groups[n[0]].name = n[1]

        def custom_fixups(act_obj):
            input_file = bpy.path.abspath(
                bpy.context.scene.ezpaint_opts.custom_v_filepath
            )
            groups_to_merge = []
            temp_group = []

            vertex_groups_replacement_list = []

            in_merge_area = False
            in_vertex_area = False

            with open(input_file, "r") as fin:
                lines = fin.readlines()
                scale = float(lines[0])
                for i in range(len(lines)):
                    line = lines[i]
                    if line.startswith("{"):
                        in_merge_area = True
                    if line.startswith("}"):
                        temp_group.append(line.strip())
                        temp_group.append(lines[i + 1])
                        in_merge_area = False
                    if in_merge_area:
                        temp_group.append(line[:-1])  # Removes newline
                    else:
                        groups_to_merge.append(temp_group)
                        temp_group = []
                    if line.startswith("["):
                        in_vertex_area = True
                    if line.startswith("]"):
                        in_vertex_area = False
                    if in_vertex_area:
                        if "[" not in line and "]" not in line:
                            line = line.strip()
                            vertex_groups_replacement_list.append(line.split(":"))

            print(scale)
            print(vertex_groups_replacement_list)

            raw_group = []
            for g in groups_to_merge:
                if len(g):
                    final_name = g[-1].strip()  # last element (minus newline)
                    for k in g:
                        if "{" not in k and "}" not in k and final_name not in k:
                            raw_group.append(k.strip())
                    print(raw_group)
                    merge_groups(raw_group, final_name, act_obj)
                    print(final_name)
                raw_group = []

            act_obj.scale = (scale, scale, scale)
            reweight(v_groups, vertex_groups_replacement_list)

        if selected_game == "SWTOR":
            print("SW:TOR MODE")
            swtor_fixups(act_obj)
            reweight(v_groups, swtor_name_list)
        if selected_game == "DEST2":
            print("DESTINY 2 MODE")
            bungie_smalldef_fixups(act_obj)
            # TODO: add checks for other bungie skeleton sizes
            reweight(v_groups, bungie_sm_name_list)
        if selected_game == "JKA":
            print("JEDI KNIGHT MODE")
            jka_fixups(act_obj)
            reweight(v_groups, jka_name_list)
        if selected_game == "SWJS":
            print("JEDI SERIES MODE")
            swjs_fixups(act_obj)
            reweight(v_groups, swjs_name_list)
        if selected_game == "BFII":
            print("BATTLEFRONT MODE")
            swbf_fixups(act_obj)
            reweight(v_groups, swbf_name_list)
        if selected_game == "FORTNITE":
            print("FORTNITE MODE")
            fortnite_fixups(act_obj)
            reweight(v_groups, fortnite_name_list)
        if selected_game == "CUSTOM":
            print("CUSTOM MODE")
            custom_fixups(act_obj)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        layout.separator()
        col = layout.column()
        col.label(text="INFO:", icon="ERROR")
        col.label(text="  Processing can take several seconds!")
        col.label(text="  ONLY the active object will be processed.")
        col.label(text="  Results may vary if games have unique skeletons.")


class EZPAINT_Settings(PropertyGroup):
    games = [
        ("SWTOR", "SW:TOR", "Star Wars: The Old Republic"),
        ("JKA", "JK:JA/II", "Jedi Knight Series (Academy & II)"),
        ("SWJS", "SW:JS/JFO", "Star Wars: Jedi Series (Survivor & Fallen Order)"),
        ("BFII", "BF/II", "Star Wars Battlefront & Battlefront II"),
        ("DEST2", "Destiny 2", "Destiny 2 - Only supports small characters for now"),
        (
            "FORTNITE",
            "Fortnite Battle Royale",
            "Fortnite - Only limited support for characters due to most models having unique bones",
        ),
        (
            "CUSTOM",
            "Use Custom Settings",
            "Load custom vertex groups and fixups from a file",
        ),
    ]

    fbx_mode: BoolProperty(
        name="FBX Mode (Only use for SW:JFO/SW:JS FBX meshes)",
        description="Only use when using FBX model from online archives. Leave unchecked if model is directly from umodel",
        default=False,
    )

    fortnite_female_armature: BoolProperty(
        name="Female Armature (Only use for female Fortnite meshes)",
        description="Only use when using a female model from fortnite. Leave unchecked if model is male",
        default=False,
    )

    has_swtor_skels: BoolProperty(
        name="Scene has SW:TOR skeletons",
        description="Scene contains the proportioned skeletons to parent the repainted mesh to",
        default=False,
    )

    fix_swtor_matnames: BoolProperty(
        name='Fix "default" materials & duplicates (SW:TOR)',
        description='ezPaint should attempt to fix material names that are duplicates or "default" (ONLY for SW:TOR)',
        default=False,
    )

    game_type: EnumProperty(
        items=games,
        name="Game",
        description="Game that the imported mesh is from",
        default="SWTOR",
    )

    custom_v_filepath: StringProperty(
        name="Custom Vertex Groups",
        subtype="FILE_PATH",
        description="File that defines a custom vertex group mapping",
    )


class EZPAINT_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ezp_opts = scene.ezpaint_opts
        col = layout.column()
        col.prop(ezp_opts, "fbx_mode")
        col.prop(ezp_opts, "fortnite_female_armature")
        col.prop(ezp_opts, "has_swtor_skels")
        col.prop(ezp_opts, "fix_swtor_matnames")
        col.prop(ezp_opts, "game_type")
        col.prop(ezp_opts, "custom_v_filepath")


class EZP_PT_options_panel(bpy.types.Panel):
    bl_label = "ezPaint Options"
    bl_idname = "VIEW3D_PT_ezp_settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ezPaint"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ezp_opts = scene.ezpaint_opts

        layout.operator(EZPAINT_OT_ReweightModel.bl_idname, icon="MESH_DATA")
        layout.separator()

        layout.prop(ezp_opts, "fbx_mode")
        layout.prop(ezp_opts, "fortnite_female_armature")
        layout.prop(ezp_opts, "has_swtor_skels")
        layout.prop(ezp_opts, "fix_swtor_matnames")
        layout.prop(ezp_opts, "game_type")
        layout.prop(ezp_opts, "custom_v_filepath")


classes = (
    EZPAINT_Settings,
    EZPAINT_AddonPreferences,
    EZPAINT_OT_ReweightModel,
    EZP_PT_options_panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.ezpaint_opts = PointerProperty(type=EZPAINT_Settings)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.ezpaint_opts


# allows running add-on from builtin text editor
if __name__ == "__main__":
    register()
