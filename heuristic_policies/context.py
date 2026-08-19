from pathlib import Path


class HeuristicContext:
    """
    Restricted interface exposed to heuristic policies.

    The underlying RoboTwin task is kept private.

    If debug_dir is provided, the context automatically saves a head-camera
    image after each policy action. This is only for debugging/visualization;
    the policy itself has no camera or filesystem access.
    """

    def __init__(self, task, debug_dir=None):
        self._task = task
        self._debug_dir = Path(debug_dir) if debug_dir else None
        self._debug_step = 0

        if self._debug_dir is not None:
            self._debug_dir.mkdir(parents=True, exist_ok=True)

    def snapshot(self, label):
        """
        Save the current head-camera image for debugging.
        """
        if self._debug_dir is None:
            return

        path = self._debug_dir / (
            f"{self._debug_step:02d}_{label}.png"
        )

        self._task.save_camera_rgb(
            str(path),
            camera_name="head_camera",
        )

        print(f"Saved debug image: {path}")
        self._debug_step += 1

    def select_arm(self, actor):
        """
        Select an arm based on the actor's x-position.
        """
        if actor != "bell":
            raise ValueError(f"Unsupported actor: {actor}")

        x = self._task.bell.get_pose().p[0]
        arm = "right" if x > 0 else "left"

        print(f"Selected arm: {arm}")
        return arm

    def approach_actor(
        self,
        actor,
        arm,
        pre_grasp_dis,
        grasp_dis,
        contact_point_id=0,
    ):
        """
        Approach an actor using RoboTwin's grasp_actor() primitive.
        """
        if actor != "bell":
            raise ValueError(f"Unsupported actor: {actor}")

        action = self._task.grasp_actor(
            self._task.bell,
            arm_tag=arm,
            pre_grasp_dis=pre_grasp_dis,
            grasp_dis=grasp_dis,
            contact_point_id=contact_point_id,
        )

        self._task.move(action)
        self.snapshot("after_approach")

    def move_relative(
        self,
        arm,
        x=0.0,
        y=0.0,
        z=0.0,
        frame="world",
    ):
        """
        Move the selected end effector by a relative displacement.
        """
        action = self._task.move_by_displacement(
            arm,
            x=x,
            y=y,
            z=z,
            move_axis=frame,
        )

        self._task.move(action)

        if z < 0:
            label = "after_downward_move"
        elif z > 0:
            label = "after_upward_move"
        else:
            label = "after_relative_move"

        self.snapshot(label)

    def check_success(self):
        """
        Call RoboTwin's original fixed task-success evaluator.
        """
        success = self._task.check_success()
        print(f"Policy check_success: {success}")
        return success
