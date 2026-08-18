import json
from pathlib import Path

from heuristic_policies.validate_policy import validate_policy


def load_policy(path):
    path = Path(path)

    with path.open("r") as f:
        policy = json.load(f)

    validate_policy(policy)
    return policy


def select_arm(task, arm_selection):
    rule = arm_selection["type"]

    if rule == "object_x_sign":
        object_name = arm_selection["object"]

        if object_name != "bell":
            raise ValueError(f"Unsupported object: {object_name}")

        x = task.bell.get_pose().p[0]
        return "right" if x > 0 else "left"

    raise ValueError(f"Unsupported arm-selection rule: {rule}")


def execute_policy(task, policy):
    """
    Execute a validated heuristic policy on an initialized RoboTwin task.

    `task` is expected to be an initialized click_bell environment.
    """

    validate_policy(policy)

    arm_tag = select_arm(task, policy["arm_selection"])

    for stage in policy["stages"]:
        stage_type = stage["type"]

        if stage_type == "approach_actor":
            action = task.grasp_actor(
                task.bell,
                arm_tag=arm_tag,
                pre_grasp_dis=stage["pre_grasp_dis"],
                grasp_dis=stage["grasp_dis"],
                contact_point_id=stage["contact_point_id"],
            )
            task.move(action)

        elif stage_type == "move_relative":
            action = task.move_by_displacement(
                arm_tag,
                x=stage["x"],
                y=stage["y"],
                z=stage["z"],
                move_axis=stage["frame"],
            )
            task.move(action)

        elif stage_type == "check_success":
            success = task.check_success()
            print(f"check_success: {success}")

        else:
            raise ValueError(f"Unsupported stage type: {stage_type}")

    return task.check_success()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m heuristic_policies.executor POLICY.json")
        raise SystemExit(2)

    policy = load_policy(sys.argv[1])

    print("Policy loaded and validated successfully.")
    print(f"Task: {policy['task']}")
    print(f"Number of stages: {len(policy['stages'])}")
