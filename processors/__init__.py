"""Processors used with the Entity Component System"""

import esper

from components import *

class MovementProcessor(esper.Processor):
    """Move objects in a world"""

    def process(self):
        for ent, (moving, pos) in self.world.get_components(Movement, Position):
            if moving.x == 0 and moving.y == 0:
                self.world.remove_component(ent, Movement)
                continue

            if moving.delay != 0:
                moving.delay -= 1
                continue

            if moving.x < 0:
                amt_x = max(moving.x, -moving.step)
            else:
                amt_x = min(moving.x, moving.step)

            if moving.y < 0:
                amt_y = max(moving.y, -moving.step)
            else:
                amt_y = min(moving.y, moving.step)

            moving.x -= amt_x
            moving.y -= amt_y

            new_x = max(0, pos.x + amt_x)
            new_y = max(0, pos.y + amt_y)

            # Make sure we don't collide before updating position.
            collides = False

            for col_ent, (collider, col_pos) in self.world.get_components(Collider, Position):
                if pos.z == col_pos.z and new_x == col_pos.x and new_y == col_pos.y:
                    collides = True
                    break

            if collides:
                continue

            pos.x = new_x
            pos.y = new_y

class ConditionsProcessor(esper.Processor):
    def process(self):
        for ent, (recovery, health) in self.world.get_components(Recovery, Health):
            health.current = min(health.max, health.current + recovery.effect)

        for ent, (poison, health) in self.world.get_components(Poison, Health):
            health.current = max(0, health.current - poison.effect)
