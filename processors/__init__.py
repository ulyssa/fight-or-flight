"""Processors used with the Entity Component System"""

import esper

from components import *

class MovementProcessor(esper.Processor):
    """Move objects in a world"""

    def process(self):
        for ent, (moving, pos) in self.world.get_components(Velocity, Position):
            rem_x = moving.x
            rem_y = moving.y

            while moving.duration > 0 and (rem_x != 0 or rem_y != 0):
                if rem_x < 0:
                    amt_x = max(rem_x, -1)
                else:
                    amt_x = min(rem_x, 1)

                if rem_y < 0:
                    amt_y = max(rem_y, -1)
                else:
                    amt_y = min(rem_y, 1)

                rem_x -= amt_x
                rem_y -= amt_y

                new_x = max(0, pos.x + amt_x)
                new_y = max(0, pos.y + amt_y)

                # Make sure we don't collide before updating position.
                collides = False

                for col_ent, (collider, col_pos) in self.world.get_components(Collider, Position):
                    if pos.z == col_pos.z and new_x == col_pos.x and new_y == col_pos.y:
                        # Stop moving on collision
                        moving.duration = 0

                        if pos.overlap or col_pos.overlap:
                            self.world.add_component(ent, Collision(col_ent))
                        else:
                            collides = True
                        break

                if collides:
                    break

                pos.x = new_x
                pos.y = new_y

            moving.duration = max(0, moving.duration - 1)

class ConditionsProcessor(esper.Processor):
    """Apply side effects of ongoing conditions"""

    def process(self):
        for ent, (recovery, health) in self.world.get_components(Recovery, Health):
            health.current = min(health.max, health.current + recovery.effect)

        for ent, (poison, health) in self.world.get_components(Poison, Health):
            health.current = max(0, health.current - poison.effect)

class DecayProcessor(esper.Processor):
    """Remove entities that have fully decayed"""

    def process(self):
        for ent, decay in self.world.get_component(Decay):
            if decay.duration > 0:
                decay.duration -= 1
                continue

            self.world.delete_entity(ent)

class CollisionProcessor(esper.Processor):
    """Apply actions for different types of object collisions"""

    def process(self):
        for ent, (proj, collision) in self.world.get_components(Projectile, Collision):
            self.world.delete_entity(ent)
            self.world.delete_entity(collision.hit)
