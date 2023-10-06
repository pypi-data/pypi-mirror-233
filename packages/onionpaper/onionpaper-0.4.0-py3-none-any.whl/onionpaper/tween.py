import math
from typing import Callable

TweenFunction = Callable[[float], float]


def ease_in_cubic(n: float) -> float:
    return n * n * n


def ease_out_cubic(n: float) -> float:
    return 1.0 - math.pow(1 - n, 3)


def ease_in_out_cubic(n: float) -> float:
    if n < 0.5:
        return 4.0 * n * n * n
    else:
        return 1.0 - math.pow(-2.0 * n + 2.0, 3.0) / 2.0


def ease_in_sine(n: float) -> float:
    return 1.0 - math.cos((n * math.pi) / 2.0)


def ease_out_sine(n: float) -> float:
    return math.sin((n * math.pi) / 2.0)


def ease_in_out_sine(n: float) -> float:
    return -(math.cos(math.pi * n) - 1.0) / 2.0


def linear(n: float) -> float:
    return n


tween_functions = {
    "ease_in_cubic": ease_in_out_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_in_sine": ease_in_sine,
    "ease_out_sine": ease_out_sine,
    "ease_in_out_sine": ease_in_out_sine,
    "linear": linear,
}


def get_tween_function(tween_function: str) -> TweenFunction:
    return tween_functions.get(tween_function, linear)


__all__ = [
    "TweenFunction",
    "ease_in_cubic",
    "ease_out_cubic",
    "ease_in_out_cubic",
    "ease_in_sine",
    "ease_out_sine",
    "ease_in_out_sine",
    "linear",
    "tween_functions",
    "get_tween_function",
]
