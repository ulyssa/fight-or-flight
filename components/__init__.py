"""Components used with the Entity Component System"""

from dataclasses import dataclass as component

@component
class ScreenChar:
    """How an object should get printed to the screen"""
    c: chr
    color: tuple[int, int, int] = (255, 255, 255)

@component
class Collision:
    """Objects that have hit each other, such as projectiles and an enemy"""
    hit: int

@component
class Collider:
    """Objects that can collide with each other"""

@component
class Decay:
    """Entities that disappear after some number of turns"""
    duration: int = 0

@component
class Velocity:
    """Direction that an Entity is moving in"""
    x: int = 0
    y: int = 0
    duration: int = 1

@component
class Position:
    """Current position of an Entity on the map"""
    x: int = 0
    y: int = 0
    z: int = 0
    overlap: bool = False

@component
class Projectile:
    """Weapon of class destruction"""

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
