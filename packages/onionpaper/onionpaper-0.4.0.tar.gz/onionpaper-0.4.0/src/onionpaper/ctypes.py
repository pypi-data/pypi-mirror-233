from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from string import ascii_lowercase, digits
from typing import Any, Dict, List, Literal, Optional, Union

import pyautogui
import pytweening


alphanumeric_keys = [*ascii_lowercase, *digits]
mouse_buttons = ["left", "middle", "right"]
duration_range = (0.0, 10.0)

logger = logging.getLogger("onionpaper")
logger.addHandler(logging.StreamHandler())


# noinspection PyProtectedMember, PyUnresolvedReferences
def get_loglevel_value(name: str, fallback: int = 30) -> int:
    return logging._nameToLevel.get(name.upper(), fallback)


def get_tween_func(name: str):
    if hasattr(pytweening, name):
        return getattr(pytweening, name)
    return pytweening.linear


def sanitize_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("\t", "\\t")


def truncate_text(text: str, limit: int) -> str:
    return text[: min(limit, len(text))]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Config:
    loglevel: str = "warning"
    relative: bool = True
    tween: str = "linear"

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Config:
        return Config(**dikt)


class ComparisonType(StrEnum):
    IsEqualTo = "=="
    IsNotEqualTo = "!="
    GreaterThan = ">"
    GreaterThanOrIsEqualTo = ">="
    LessThan = "<"
    LessThanOrIsEqualTo = "<="


@dataclass
class Condition:
    comparison: ComparisonType = ComparisonType.IsEqualTo
    a: Any = None
    b: Any = None
    a_id: Optional[str] = None
    b_id: Optional[str] = None

    def evaluate(self, state: State) -> bool:
        left = state.store.get(self.a_id, "") if self.a_id else self.a
        right = state.store.get(self.b_id, "") if self.b_id else self.b
        if self.comparison == ComparisonType.IsEqualTo:
            e_value = left == right
        elif self.comparison == ComparisonType.IsNotEqualTo:
            e_value = left != right
        elif self.comparison == ComparisonType.GreaterThan:
            e_value = left > right
        elif self.comparison == ComparisonType.GreaterThanOrIsEqualTo:
            e_value = left >= right
        elif self.comparison == ComparisonType.LessThan:
            e_value = left < right
        elif self.comparison == ComparisonType.LessThanOrIsEqualTo:
            e_value = left <= right
        else:
            e_value = False

        logger.debug(
            "| ({}: {}) {} ({}: {}) = {}".format(
                self.a_id if self.a_id else "a",
                left,
                self.comparison,
                self.b_id if self.b_id else "b",
                right,
                e_value,
            )
        )

        return e_value

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Condition:
        return Condition(**dikt)


@dataclass
class State:
    actions: List[Action]
    config: Config
    counter: int = 0
    cycle: int = 0
    index: int = 0
    store: Dict[str, Any] = field(default_factory=lambda: {})

    def is_done(self) -> bool:
        return self.index >= len(self.actions)

    def next(self) -> None:
        action = self.actions[self.index]

        prev_index = self.index
        next_index = action.execute(state=self)

        self.counter += 1

        if self.index == len(self.actions) - 1:
            self.cycle += 1

        if next_index is None:
            self.index += 1
        else:
            self.index = next_index

        self.store["counter"] = self.counter
        self.store["cycle"] = self.cycle
        self.store["index"] = self.index
        self.store["previous_index"] = prev_index

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> State:
        return State(**dikt)


class ActionType(StrEnum):
    Click = "click"
    Configure = "configure"
    Drag = "drag"
    Hotkey = "hotkey"
    Jump = "jump"
    Move = "move"
    Press = "press"
    Stop = "stop"
    Store = "store"
    Write = "write"


@dataclass
class Action:
    type: ActionType = ActionType.Move
    x: float = 0.0
    y: float = 0.0
    duration: float = 0.0
    button: str = "left"
    key: str = "return"
    index: Optional[int] = None
    condition: Optional[Union[dict, Condition]] = None
    randomize: Optional[str] = None
    text: Optional[str] = None
    id: Optional[str] = None
    value: Any = None

    loglevel: Optional[str] = None
    relative: Optional[bool] = None
    tween: Optional[str] = None

    def execute(self, state: State) -> Optional[int]:
        loglevel = self.loglevel if self.loglevel else state.config.loglevel
        relative = self.relative if self.relative is not None else state.config.relative
        tween = self.tween if self.tween else state.config.tween

        self.randomize_parts(relative=relative, state=state)

        self.set_loglevel(loglevel=loglevel)

        result = None

        if self.type == ActionType.Click:
            result = self.execute_click()
        if self.type == ActionType.Configure:
            result = self.execute_configure(state=state)
        elif self.type == ActionType.Drag:
            result = self.execute_drag(relative=relative, tween=tween)
        elif self.type == ActionType.Hotkey:
            result = self.execute_hotkey()
        elif self.type == ActionType.Jump:
            result = self.execute_jump(state=state)
        elif self.type == ActionType.Move:
            result = self.execute_move(relative=relative, tween=tween)
        elif self.type == ActionType.Press:
            result = self.execute_press()
        elif self.type == ActionType.Stop:
            result = self.execute_stop()
        elif self.type == ActionType.Store:
            result = self.execute_store(state=state)
        elif self.type == ActionType.Write:
            result = self.execute_write()

        return result

    def execute_click(self) -> Optional[int]:
        pyautogui.mouseDown(button=self.button)
        logger.debug(f"| mouseDown(button={self.button})")
        time.sleep(self.duration)
        pyautogui.mouseUp(button=self.button)
        logger.debug(f"| mouseUp(button={self.button})")
        logger.info("* click")
        return None

    def execute_configure(self, state: State) -> Optional[int]:
        if self.loglevel:
            state.config.loglevel = self.loglevel
            logger.debug(f"| loglevel = {self.loglevel}")
        if self.relative is not None:
            state.config.relative = self.relative
            logger.debug(f"| relative = {self.relative}")
        if self.tween:
            state.config.tween = self.tween
            logger.debug(f"| tween = {self.tween}")
        logger.info("* configure")
        return None

    def execute_drag(self, relative: bool, tween: str) -> Optional[int]:
        if relative:
            pyautogui.dragRel(
                xOffset=self.x,
                yOffset=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
                button=self.button,
            )
            logger.debug(
                "| dragRel("
                f"xOffset={self.x}, "
                f"yOffset={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween}, "
                f"button={self.button})"
            )
        else:
            pyautogui.dragTo(
                x=self.x,
                y=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
                button=self.button,
            )
            logger.debug(
                "| dragTo("
                f"x={self.x}, "
                f"y={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween}, "
                f"button={self.button})"
            )
        logger.info("* drag")
        return None

    def execute_hotkey(self) -> Optional[int]:
        hotkeys = [hk.strip() for hk in self.key.split("+")]
        interval: float = self.duration / len(hotkeys)
        logger.debug(f"| hotkey({', '.join(hotkeys)}, interval={interval})")
        pyautogui.hotkey(*hotkeys, interval=interval)
        logger.info("* hotkey")
        return None

    def execute_jump(self, state: State) -> Optional[int]:
        if self.condition and isinstance(self.condition, Condition):
            e_value = self.condition.evaluate(state=state)
            if not e_value:
                logger.info("* jump (skipped)")
                return None
        logger.debug(f"| jump({self.index})")
        logger.info("* jump")
        return self.index

    def execute_move(self, relative: bool, tween: str) -> Optional[int]:
        if relative:
            pyautogui.moveRel(
                xOffset=self.x,
                yOffset=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
            )
            logger.debug(
                "| moveRel("
                f"xOffset={self.x}, "
                f"yOffset={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween})"
            )
        else:
            pyautogui.moveTo(
                x=self.x,
                y=self.y,
                duration=self.duration,
                tween=get_tween_func(tween),
            )
            logger.debug(
                "| moveTo("
                f"x={self.x}, "
                f"y={self.y}, "
                f"duration={self.duration}, "
                f"tween={tween})"
            )
        logger.info("* move")
        return None

    def execute_press(self) -> Optional[int]:
        pyautogui.keyDown(key=self.key)
        logger.debug(f"| keyDown(key={self.key})")
        time.sleep(self.duration)
        pyautogui.keyUp(key=self.key)
        logger.debug(f"| keyUp(key={self.key})")
        logger.info("* press")
        return None

    def execute_store(self, state: State) -> Optional[int]:
        identifier = self.id if self.id else ""
        logger.debug(f"| store({identifier}={self.value})")
        state.store[identifier] = self.value
        logger.info("* store")
        return None

    def execute_stop(self) -> Optional[int]:
        logger.debug(f"| stop({self.duration})")
        time.sleep(self.duration)
        logger.debug(f"| resume()")
        logger.info("* stop")
        return None

    def execute_write(self) -> Optional[int]:
        interval: float = self.duration / len(self.text)
        logger.debug(
            f"| write('{truncate_text(sanitize_text(self.text), limit=25)}...', interval={interval})"
        )
        pyautogui.write(message=self.text, interval=interval)
        logger.info("* write")
        return None

    def randomize_parts(self, relative: bool, state: State) -> None:
        if self.randomize:
            randomize_parts = self.randomize.split(",")
            for part in randomize_parts:
                part = part.strip()
                if part == "x":
                    self.x = self.random_coord("x", relative=relative)
                    logger.debug(f"| x = random(<{self.x}>)")
                elif part == "y":
                    self.y = self.random_coord("y", relative=relative)
                    logger.debug(f"| y = random(<{self.y}>)")
                elif part == "duration":
                    self.duration = random.uniform(*duration_range)
                    logger.debug(f"| duration = random(<{self.duration}>)")
                elif part == "button":
                    self.button = random.choice(mouse_buttons)
                    logger.debug(f"| button = random(<{self.button}>)")
                elif part == "key":
                    self.key = random.choice(alphanumeric_keys)
                    logger.debug(f"| key = random(<{self.key}>)")
                elif part == "index":
                    self.index = random.randint(0, len(state.actions) - 1)
                    logger.debug(f"| index = random(<{self.index}>)")

    # noinspection PyMethodMayBeStatic
    def set_loglevel(self, loglevel: str) -> None:
        logger.setLevel(get_loglevel_value(loglevel))

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Action:
        action = Action(**dikt)
        if action.condition and isinstance(action.condition, dict):
            action.condition = Condition.create_from_dict(action.condition)
        return action

    # noinspection PyShadowingBuiltins
    @staticmethod
    def random_coord(
        axis: Literal["x", "y"] = "x",
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        range: float = 100.0,
        relative: bool = True,
    ) -> float:
        if relative:
            if minimum is None and maximum is None:
                minimum = -range * 0.5
                maximum = range * 0.5
            if minimum is None:
                minimum = maximum - range
            if maximum is None:
                maximum = minimum + range
            return random.uniform(minimum, maximum)
        else:
            if minimum is None:
                minimum = 0
            if maximum is None:
                size = pyautogui.size()
                maximum = size[0] if axis == "x" else size[1]
            return random.uniform(minimum, maximum)


__all__ = [
    "Action",
    "ActionType",
    "Config",
    "State",
    "logger",
]
