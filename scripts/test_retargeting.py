"""
Sanity-check script: feed synthetic hand keypoints into dex_retargeting
and confirm it produces valid robot joint angles — no headset, no robot needed.
"""
import numpy as np
from pathlib import Path
from dex_retargeting.retargeting_config import RetargetingConfig

# 1. Point this at a G1 hand retargeting config yaml.
#    Look inside xr_teleoperate/teleop/robot_control/dex-retargeting/dex_retargeting/configs/
#    for one that matches the G1's end-effector (e.g. a dex3 or dex1_1 hand config).
CONFIG_PATH = Path("xr_teleoperate/teleop/robot_control/dex-retargeting/dex_retargeting/configs/teleop/<PICK_G1_HAND_CONFIG>.yml")

# 2. Some configs need a urdf/robot directory root set — check the yaml file
#    for a `urdf_dir` field; if missing, dex-retargeting looks relative to the config.
RetargetingConfig.set_default_urdf_dir(str(CONFIG_PATH.parent.parent.parent / "assets"))

def main():
    config = RetargetingConfig.load_from_file(CONFIG_PATH)
    retargeting = config.build()

    print("Joint names expected by robot model:")
    print(retargeting.joint_names)

    # 3. Fake human hand keypoints: shape depends on retargeting type
    #    (position retargeting expects an (N, 3) array of 3D joint positions,
    #    e.g. N=21 for a standard MediaPipe-style hand skeleton).
    fake_hand_keypoints = np.random.uniform(-0.1, 0.1, size=(21, 3)).astype(np.float32)

    qpos = retargeting.retarget(fake_hand_keypoints)
    print("Resulting robot joint angles:")
    print(qpos)

if __name__ == "__main__":
    main()

