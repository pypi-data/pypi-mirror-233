from typing import List, Optional

from .ctypes import Action, Config, State


def trace(actions: List[Action], config: Optional[Config] = None) -> None:
    config = config if config else Config()
    state = State(actions=actions, config=config)
    while not state.is_done():
        state.next()


__all__ = [
    "trace",
]
