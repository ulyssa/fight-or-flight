"""Components used with the Entity Component System"""

from dataclasses import dataclass as component

class ScreenChar:
    def __init__(self, c, color = [255, 255, 255]):
        self.c = c
        self.color = color

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
class Health:
    current: int
    max: int
