# RoboTwin 2.0 Public Policy Interface

This document describes the generic RoboTwin programming interface available
to heuristic policies.

It is task-independent.

It documents how to program against RoboTwin, not how to solve any particular
task.

# ============================================================
# 1. POLICY ENTRY POINT
# ============================================================

A candidate policy must define:

```python
def run_heuristic(task):
    ...
```

The `task` object represents the initialized RoboTwin environment.

Do not inspect task implementation source, success-condition source, expert
code, or hidden simulator state.


# ============================================================
# 2. ARM TAGS
# ============================================================

Valid arm identifiers are:

```python
"left"
"right"
```

Use these strings wherever an `arm_tag` argument is required.


# ============================================================
# 3. IMPORTANT ACTION CONVENTION
# ============================================================

Most RoboTwin helper methods do NOT execute immediately.

They return an action bundle containing an arm tag and a list of actions.

For example:

```python
action = task.move_by_displacement(
    "left",
    x=0.0,
    y=0.0,
    z=0.05,
)

task.move(action)
```

The numerical values above demonstrate API syntax only.

They are NOT task-specific recommendations.

In general:

```python
action_bundle = task.some_action_helper(...)
task.move(action_bundle)
```

Two arm action bundles may also be supplied to `task.move(...)` when
appropriate.


# ============================================================
# 4. MOVE
# ============================================================

Generic form:

```python
task.move(
    actions_by_arm1,
    actions_by_arm2=None,
    save_freq=-1,
)
```

Each arm argument is normally an action bundle returned by one of RoboTwin's
action helper methods.

The method executes the supplied robot actions.

It returns `False` when planning has already failed or fails during execution.

Otherwise it returns `True`.


# ============================================================
# 5. MOVE BY DISPLACEMENT
# ============================================================

Signature:

```python
task.move_by_displacement(
    arm_tag,
    x=0.0,
    y=0.0,
    z=0.0,
    quat=None,
    move_axis="world",
)
```

Arguments:

- `arm_tag`: `"left"` or `"right"`
- `x`: displacement along x
- `y`: displacement along y
- `z`: displacement along z
- `quat`: optional target quaternion
- `move_axis`: `"world"` or `"arm"`

The function returns an action bundle.

Execute it with:

```python
task.move(action_bundle)
```

When:

```python
move_axis="world"
```

the displacement is interpreted in world coordinates.


# ============================================================
# 6. MOVE TO POSE
# ============================================================

Signature:

```python
task.move_to_pose(
    arm_tag,
    target_pose,
)
```

`target_pose` may be:

- a Python list
- a NumPy array
- a `sapien.Pose`

A list or array pose follows RoboTwin's 7-value pose representation:

```text
[x, y, z, qw, qx, qy, qz]
```

The function returns an action bundle.

Execute it with:

```python
action = task.move_to_pose(
    arm_tag,
    target_pose,
)

task.move(action)
```


# ============================================================
# 7. OPEN GRIPPER
# ============================================================

Signature:

```python
task.open_gripper(
    arm_tag,
    pos=1.0,
)
```

The function returns an action bundle that commands the selected gripper
toward the requested position.

Execute it with:

```python
task.move(action_bundle)
```


# ============================================================
# 8. CLOSE GRIPPER
# ============================================================

Signature:

```python
task.close_gripper(
    arm_tag,
    pos=0.0,
)
```

The function returns an action bundle that commands the selected gripper
toward the requested position.

Execute it with:

```python
task.move(action_bundle)
```


# ============================================================
# 9. BACK TO ORIGIN
# ============================================================

Signature:

```python
task.back_to_origin(
    arm_tag,
)
```

The function returns an action bundle moving the selected arm toward its
RoboTwin original pose.

Execute it with:

```python
task.move(action_bundle)
```


# ============================================================
# 10. GET ARM POSE
# ============================================================

Generic form:

```python
task.get_arm_pose(
    arm_tag,
)
```

It returns the current end-effector pose for the selected arm.

The pose follows RoboTwin's 7-value pose representation:

```text
[x, y, z, qw, qx, qy, qz]
```


# ============================================================
# 11. GRASP ACTOR
# ============================================================

Signature:

```python
task.grasp_actor(
    actor,
    arm_tag,
    pre_grasp_dis=0.1,
    grasp_dis=0,
    gripper_pos=0.0,
    contact_point_id=None,
)
```

Arguments:

- `actor`: a permitted public RoboTwin Actor
- `arm_tag`: `"left"` or `"right"`
- `pre_grasp_dis`: pre-grasp approach distance
- `grasp_dis`: grasp displacement parameter
- `gripper_pos`: commanded closed-gripper position
- `contact_point_id`: optional contact-point index or indices

The function chooses RoboTwin grasp poses and returns an action bundle.

Execute it with:

```python
action = task.grasp_actor(
    actor,
    arm_tag,
)

task.move(action)
```

The example demonstrates API composition only.

The appropriate:

- actor
- arm
- contact point
- approach distance
- grasp distance
- orientation

are part of the heuristic-learning problem.

They are NOT specified by this interface.


# ============================================================
# 12. PLACE ACTOR
# ============================================================

Signature:

```python
task.place_actor(
    actor,
    arm_tag,
    target_pose,
    functional_point_id=None,
    pre_dis=0.1,
    dis=0.02,
    is_open=True,
    **args,
)
```

The function generates placement actions for a permitted public actor.

It returns an action bundle.

Execute it with:

```python
action = task.place_actor(
    actor,
    arm_tag,
    target_pose,
)

task.move(action)
```

The appropriate target, placement geometry, arm, orientation, and parameters
must be discovered through the heuristic-learning process.


# ============================================================
# 13. PUBLIC ACTOR INTERFACE
# ============================================================

Policies may use Actor objects explicitly exposed through the experiment's
public actor view.

A public RoboTwin Actor supports:

```python
actor.get_name()
actor.get_pose()
```

`actor.get_name()` returns the normal actor name.

`actor.get_pose()` returns a `sapien.Pose` representing the actor's current
world pose.


## Contact points

Where available:

```python
actor.get_contact_point(
    idx,
    ret="list",
)
```

A policy may also iterate through available contact points:

```python
for idx, point in actor.iter_contact_points(
    ret="list",
):
    ...
```


## Functional points

Where available:

```python
actor.get_functional_point(
    idx,
    ret="list",
)
```


## Target points

Where available:

```python
actor.get_target_point(
    idx,
    ret="list",
)
```


## Orientation point

Where available:

```python
actor.get_orientation_point(
    ret="list",
)
```


## Point return representations

Supported `ret` values are:

```text
"list"
"matrix"
"pose"
```

When:

```python
ret="list"
```

the point is represented as a world-frame 7-value pose:

```text
[x, y, z, qw, qx, qy, qz]
```

A particular point may be unavailable for a particular actor.

Policies must handle that possibility rather than assuming every actor has
every type of annotated point.


# ============================================================
# 14. PUBLIC ACTOR DISCOVERY
# ============================================================

The experiment infrastructure provides a task-independent public actor view.

This view exists so policies do not need to know private Python attribute
names used inside individual RoboTwin task implementations.

Policies must use the documented public actor view to discover available
actors.

Policies must NOT:

- inspect `task.__dict__`
- call `vars(task)` to discover private fields
- enumerate private task attributes
- guess private task attribute names
- use `dir(task)` for task-internal discovery
- use Python introspection to reveal task internals
- inspect task source code
- inspect `load_actors()` implementations
- inspect `check_success()` implementations
- inspect expert `play_once()` implementations

The public actor view may expose normal observable actor names and public
geometry.

It must not expose task implementation details, hidden success information,
or expert strategy.

The public actor accessor is `task.get_public_actors()`.

It returns a tuple of permitted RoboTwin Actor objects.

Generic usage:

    actors = task.get_public_actors()

    for actor in actors:
        name = actor.get_name()
        pose = actor.get_pose()

The ordering and names of actors must not be interpreted as hidden task
implementation information. Policies must reason from public observations
and the supplied task description.

The discovery mechanism itself is evaluator infrastructure and is not
available to the candidate policy.


# ============================================================
# 15. SCENE ACCESS
# ============================================================

Raw scene enumeration is not the primary actor-discovery mechanism for
heuristic policies.

Policies should use the experiment's public actor view instead of attempting
to reconstruct task implementation structure from low-level simulator
entities.

Infrastructure objects, robot internals, and other simulator entities are not
automatically task-relevant actors.


# ============================================================
# 16. PLANNING FAILURES
# ============================================================

RoboTwin motion primitives may fail to find a valid motion plan.

Policies must not assume every requested pose, displacement, grasp, or
placement is reachable.

The return value of motion execution may be used to detect planning failure
where supported.

Evaluation feedback determines whether the resulting task execution
ultimately succeeds.


# ============================================================
# 17. WHAT THE POLICY MUST DISCOVER
# ============================================================

The following information is intentionally NOT supplied by this interface:

- which actor should be manipulated
- which actor is a target
- which arm should be used
- whether an object should be grasped
- whether an object should be pressed
- whether an object should be moved
- approach direction
- interaction direction
- displacement magnitude
- target offset
- target orientation
- contact-point choice
- functional-point choice
- target-point choice
- motion sequence
- recovery strategy
- task-specific thresholds
- task-specific geometric constants

These are part of the heuristic-learning problem.

They must be discovered through permitted interaction and evaluator feedback.


# ============================================================
# 18. BLACK-BOX INFORMATION BOUNDARY
# ============================================================

The policy may use:

```text
generic RoboTwin API knowledge
the supplied natural-language task description
the experiment public actor view
public actor poses
public annotated actor points
robot proprioception
planning success/failure
evaluation success/failure
policies generated during THIS search
history and feedback from THIS search
```

The policy may NOT use:

```text
selected task source code
private task Python attributes
load_actors() implementation
check_success() implementation
play_once() expert code
existing expert policies
previous experimental solutions
hidden simulator state
held-out evaluation results
external implementations
published task solutions
internet resources
```


# ============================================================
# 19. PURPOSE OF THIS INTERFACE
# ============================================================

The purpose of this document is to separate:

```text
knowing how to program RoboTwin
```

from:

```text
knowing how to solve the selected RoboTwin task
```

Generic API syntax and semantics are programming-interface knowledge.

Task strategy, geometry, object selection, interaction sequence, and success
conditions remain unknown and must be learned.

Measured RoboTwin episodes should therefore test heuristic learning rather
than Python API reverse engineering.
