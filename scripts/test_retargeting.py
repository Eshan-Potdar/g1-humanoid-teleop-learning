"""
Sanity-check script: feed synthetic hand keypoints into dex_retargeting
using the REAL Unitree G1 (Dex3 hand) config, and confirm it produces
valid robot joint angles — no headset, no robot needed.

Loading pattern verified against xr_teleoperate's actual
teleop/robot_control/hand_retargeting.py source code.
"""
import yaml
import numpy as np
from pathlib import Path
from dex_retargeting.retargeting_config import RetargetingConfig

# Path to the repo's assets folder (URDF + meshes live here)
ASSETS_DIR = Path("xr_teleoperate/assets")
CONFIG_PATH = ASSETS_DIR / "unitree_hand" / "unitree_dex3.yml"

RetargetingConfig.set_default_urdf_dir(str(ASSETS_DIR))

def build_hand(cfg_dict):
    return RetargetingConfig.from_dict(cfg_dict).build()

def main():
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)

    left_hand = build_hand(cfg["left"])
    right_hand = build_hand(cfg["right"])

    print("Left hand joint names:", left_hand.joint_names)
    print("Right hand joint names:", right_hand.joint_names)

    fake_hand_keypoints = np.random.uniform(-0.1, 0.1, size=(21, 3)).astype(np.float32)

    left_qpos = left_hand.retarget(fake_hand_keypoints)
    right_qpos = right_hand.retarget(fake_hand_keypoints)

    print("\nLeft hand resulting joint angles:")
    print(left_qpos)
    print("\nRight hand resulting joint angles:")
    print(right_qpos)

if __name__ == "__main__":
    main()
