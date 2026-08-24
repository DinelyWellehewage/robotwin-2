"""
Public policy interface for black-box RoboTwin heuristic learning.

This module belongs to the experiment infrastructure.

It may inspect the initialized task internally in order to expose a small,
task-independent public actor interface to candidate policies.

Candidate policies must not perform this introspection themselves.
"""

from __future__ import annotations

from typing import Any

from envs.utils.actor_utils import Actor


def discover_public_actors(task: Any) -> tuple[Actor, ...]:
    """
    Return RoboTwin Actor wrappers stored directly on an initialized task.

    Only Actor instances are exposed. Raw SAPIEN entities, simulator
    infrastructure, robot internals, and arbitrary private task state are not
    included.

    Discovery is performed by trusted experiment infrastructure so candidate
    policies do not need to know task-specific Python attribute names.
    """

    actors: list[Actor] = []
    seen: set[int] = set()

    for value in vars(task).values():
        if not isinstance(value, Actor):
            continue

        identity = id(value)

        if identity in seen:
            continue

        seen.add(identity)
        actors.append(value)

    return tuple(actors)


def install_public_interface(task: Any) -> None:
    """
    Install the generic actor accessor available to candidate policies.

    After installation, policies may call:

        task.get_public_actors()

    The accessor returns a tuple of RoboTwin Actor objects.

    The candidate is not given task attribute names or access to the discovery
    mechanism.
    """

    actors = discover_public_actors(task)

    def get_public_actors() -> tuple[Actor, ...]:
        return actors

    task.get_public_actors = get_public_actors
