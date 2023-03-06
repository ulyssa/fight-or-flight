"""Components used with the Entity Component System"""

from dataclasses import dataclass as component, field

@component
class ScreenChar:
    """How an object should get printed to the screen"""
    def __init__(self, c, color = (255, 255, 255)):
        self.c = c
        self.color = color

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
    damage: int = 0

@component
class Recovery:
    effect: int = 1

@component
class Poison:
    effect: int = 1

@component
class Seeker:
    """Seeker"""
    aggro: int = 10

@component
class Health:
    current: int
    max: int
    inventory: list = field(default_factory=list)

    def damage(self, amt):
        self.current = max(0, self.current - amt)

    def heal(self, amt):
        self.current = min(self.max, self.current + amt)

@component
class Stamina:
    current: int
    max: int

    def exert(self, amt):
        self.current = max(0, self.current - amt)

    def rest(self, amt): 
        self.current = min(self.max, self.current + amt)

        # TODO: Insert a time for how long a rest takes?
