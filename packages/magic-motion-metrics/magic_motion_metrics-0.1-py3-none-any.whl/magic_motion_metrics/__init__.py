import json

def load_metric(kind = "foot_distance", **kwargs):
    if kind == "foot_distance":
        from magic_motion_metrics.foot_distance.FootDistance import FOOTDISTANCE
        return FOOTDISTANCE(**kwargs)
    elif kind == "hip_to_right_shoulder_dist":
        from magic_motion_metrics.hip_to_right_shoulder.HipToRightShoulder import HipToRightShoulder
        return HipToRightShoulder(**kwargs)
    elif kind == "hip_to_left_shoulder_dist":
        from magic_motion_metrics.hip_to_left_shoulder.HipToLeftShoulder import HipToLeftShoulder
        return HipToLeftShoulder(**kwargs)
    elif kind == "foot_arc_right":
        from magic_motion_metrics.right_foot_arc.RightFootArc import RightFootArc
        return RightFootArc(**kwargs)
    elif kind == "foot_arc_left":
        from magic_motion_metrics.left_foot_arc.LeftFootArc import LeftFootArc 
        return LeftFootArc(**kwargs)
    elif kind == "trunk_tilt_angle":
        from magic_motion_metrics.trunk_tilt_angle.TrunkTiltAngle import TrunkTiltAngle
        return TrunkTiltAngle(**kwargs)
    elif kind == "right_hip_shoulder_sepration_angle":
        from magic_motion_metrics.right_hip_shoulder_sepration_angle.RightHipShoulderSeprationAngle import RightHipShoulderSeprationAngle
        return RightHipShoulderSeprationAngle(**kwargs)
    elif kind == "left_hip_shoulder_sepration_angle":
        from magic_motion_metrics.left_hip_shoulder_sepration_angle.LeftHipShoulderSeprationAngle import LeftHipShoulderSeprationAngle
        return LeftHipShoulderSeprationAngle(**kwargs)
    elif kind == "right_fore_arm_angle":
        from magic_motion_metrics.right_fore_arm_angle.RightForearmAngle import RightForearmAngle
        return RightForearmAngle(**kwargs)
    elif kind == "left_fore_arm_angle":
        from magic_motion_metrics.left_fore_arm_angle.LeftForearmAngle import LeftForearmAngle
        return LeftForearmAngle(**kwargs)
    

def default_config():
    config = {
        "Metrics":{
            "foot_distance": {
                "name": "Foot Distance"
            },
            "hip_to_right_shoulder_dist": {
                "name": "Hip To Right Shoulder"
            },
            "hip_to_left_shoulder_dist": {
                "name": "Hip To Left Shoulder"
            },
            "foot_arc_right": {
                "name": "Foot Arc Right"
            },
            "foot_arc_left": {
                "name": "Foot Arc Left"
            },
            "trunk_tilt_angle": {
                "name": "Trunk Tilt Angle"
            },
            "right_hip_shoulder_sepration_angle": {
                "name": "Right Hip Shoulder Sepration Angle"
            },
            "left_hip_shoulder_sepration_angle": {
                "name": "Left Hip Shoulder Sepration Angle"
            },
            "right_fore_arm_angle": {
                "name": "Right Fore Arm Angle"
            },
            "left_fore_arm_angle": {
                "name": "Left Fore Arm Angle"
            }
        }
    }
    return config

def get_metrics():
    # with open('config/config.json') as json_file:
    #     config = json.load(json_file)
    return default_config()