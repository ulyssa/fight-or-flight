"""Functions for creating new entities"""

from components import *

def makeBuilding(world, x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            building = world.create_entity(
                ScreenChar('%', color=(200, 200, 200)),
                Position(x=i, y=j),
                Collider()
            )

def make_player(world):
    player = world.create_entity(
        ScreenChar('@'),
        Position(),
        Health(10, 10),
        Stamina(15, 15),
        Velocity(),
        Collider(),
    )

    return player

def make_pile(world, pos, inventory):
    for item in inventory:
        item.create_entities(world, pos)
