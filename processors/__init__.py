"""Processors used with the Entity Component System"""

import esper
import numpy as np
import tcod

from params import *
from components import *
from entities import *

from items import *

class MovementProcessor(esper.Processor):
    """Move objects in a world"""

    def process(self, player):
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
                            self.world.add_component(col_ent, Collision(ent))
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

    def process(self, player):
        for ent, (recovery, health) in self.world.get_components(Recovery, Health):
            health.heal(recovery.effect)

        for ent, (poison, health) in self.world.get_components(Poison, Health):
            health.damage(poison.effect)

        for ent, stamina in self.world.get_component(Stamina):
            if stamina.current <= 0:
                self.world.add_component(ent, Velocity(x=0, y=0))


class DecayProcessor(esper.Processor):
    """Remove entities that have fully decayed"""

    def process(self, player):
        for ent, decay in self.world.get_component(Decay):
            if decay.duration > 0:
                decay.duration -= 1
                continue

            self.world.delete_entity(ent)

class CollisionProcessor(esper.Processor):
    """Apply actions for different types of object collisions"""

    def process(self, player):
        # Check for objects that have crashed into something with Health.
        for ent, (health, collision) in self.world.get_components(Health, Collision):
            self.world.remove_component(ent, Collision)

            proj = self.world.try_component(collision.hit, Projectile)
            if proj is not None:
                # Apply damage and set Projectile to disappear.
                health.damage(proj.damage)
                self.world.add_component(collision.hit, Decay())
                continue

        # Check if the player moved on top of a pile of items.
        for ent, (item, collision) in self.world.get_components(Item, Collision):
            if collision.hit != player:
                continue

            player_health = self.world.component_for_entity(player, Health)
            player_health.inventory.append(item)

            # Set Item to disappear.
            self.world.add_component(ent, Decay())


class DeathProcessor(esper.Processor):
    """Apply actions for entities whose Health reaches 0"""

    def process(self, player):
        for ent, health in self.world.get_component(Health):
            if health.current > 0 or ent == player:
                continue

            drop_pos = self.world.try_component(ent, Position)

            if drop_pos is not None:
                for item in health.inventory:
                    item.create_entities(self.world, drop_pos)

            self.world.delete_entity(ent)

class PathProcessor(esper.Processor):
    """Pathfinding"""

    def process(self, player):

        player_pos = self.world.try_component(player, Position)
        if player_pos is None:
            return

        cost = np.ones((WIDTH, WORLD_HEIGHT), dtype=np.int8, order="F") # F == xy, C == ij coordinate systems

        for ent, (collider, pos) in self.world.get_components(Collider, Position):
            if pos.overlap:
                cost.itemset((pos.x, pos.y), 2)
            else:
                cost.itemset((pos.x, pos.y), 0)

        cost.itemset((player_pos.x, player_pos.y), 1)

        for ent, (seeker, pos) in self.world.get_components(Seeker, Position):

            cost.itemset((pos.x, pos.y), 1)

            graph = tcod.path.SimpleGraph(cost=cost, cardinal=1, diagonal=0) # Allowed movement of 1 in cardinal directions, cannot move diagonal
            pf = tcod.path.Pathfinder(graph)

            pf.add_root((pos.x, pos.y))
            path = pf.path_to((player_pos.x, player_pos.y)).tolist()

            cost.itemset((pos.x, pos.y), 0)

            if len(path) < 2 or len(path) > seeker.aggro:
                continue

            x_mov = path[1][0] - path[0][0]
            y_mov = path[1][1] - path[0][1]

            self.world.add_component(ent, Velocity(x=x_mov, y=y_mov))
