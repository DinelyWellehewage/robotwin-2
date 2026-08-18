import json
import math
import sys
from pathlib import Path


ALLOWED_STAGE_TYPES = {
    "approach_actor",
    "move_relative",
    "check_success",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_number(value, name):
    require(isinstance(value, (int, float)) and not isinstance(value, bool),
            f"{name} must be a number")
    require(math.isfinite(value), f"{name} must be finite")


def validate_policy(policy):
    require(isinstance(policy, dict), "Policy must be a JSON object")

    require(policy.get("version") == 1, "version must be 1")
    require(policy.get("task") == "click_bell", "task must be click_bell")

    arm_selection = policy.get("arm_selection")
    require(isinstance(arm_selection, dict), "arm_selection must be an object")
    require(
        arm_selection.get("type") == "object_x_sign",
        "arm_selection.type must be object_x_sign",
    )
    require(
        arm_selection.get("object") == "bell",
        "arm_selection.object must be bell",
    )

    stages = policy.get("stages")
    require(isinstance(stages, list), "stages must be a list")
    require(1 <= len(stages) <= 10, "stages must contain between 1 and 10 entries")

    for i, stage in enumerate(stages):
        require(isinstance(stage, dict), f"stage {i} must be an object")

        stage_type = stage.get("type")
        require(
            stage_type in ALLOWED_STAGE_TYPES,
            f"stage {i}: unsupported type {stage_type!r}",
        )

        if stage_type == "approach_actor":
            require(stage.get("actor") == "bell",
                    f"stage {i}: actor must be bell")

            pre_grasp_dis = stage.get("pre_grasp_dis")
            grasp_dis = stage.get("grasp_dis")

            finite_number(pre_grasp_dis, f"stage {i}.pre_grasp_dis")
            finite_number(grasp_dis, f"stage {i}.grasp_dis")

            require(
                0.02 <= pre_grasp_dis <= 0.20,
                f"stage {i}: pre_grasp_dis must be in [0.02, 0.20]",
            )
            require(
                0.02 <= grasp_dis <= 0.20,
                f"stage {i}: grasp_dis must be in [0.02, 0.20]",
            )

            require(
                stage.get("contact_point_id") == 0,
                f"stage {i}: contact_point_id must be 0",
            )

        elif stage_type == "move_relative":
            require(
                stage.get("frame") == "world",
                f"stage {i}: frame must be world",
            )

            for axis in ("x", "y", "z"):
                value = stage.get(axis)
                finite_number(value, f"stage {i}.{axis}")
                require(
                    -0.15 <= value <= 0.15,
                    f"stage {i}: {axis} must be in [-0.15, 0.15]",
                )

        elif stage_type == "check_success":
            require(
                set(stage.keys()) == {"type"},
                f"stage {i}: check_success takes no extra parameters",
            )

    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_policy.py POLICY.json")
        sys.exit(2)

    path = Path(sys.argv[1])

    with path.open("r") as f:
        policy = json.load(f)

    try:
        validate_policy(policy)
    except ValueError as exc:
        print(f"INVALID: {exc}")
        sys.exit(1)

    print("VALID")


if __name__ == "__main__":
    main()
