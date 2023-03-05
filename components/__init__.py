"""Components used with the Entity Component System"""

from dataclasses import dataclass as component

@component
class ScreenChar:
    """How an object should get printed to the screen"""
    c: chr
    color: tuple[int, int, int] = (255, 255, 255)

@component
class Collider:
    """Objects that can collide with each other"""

@component
class Movement:
    """Direction that an Entity is moving in"""
    x: int = 0
    y: int = 0
    step: int = 1
    delay: int = 0

@component
class Position:
    """Current position of an Entity on the map"""
    x: int = 0
    y: int = 0
    z: int = 0

@component
class Recovery:
    effect: int = 1

@component
class Poison:
    effect: int = 1

@component
class Health:
    current: int
    max: int
