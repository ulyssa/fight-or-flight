"""Processors used with the Entity Component System"""

import esper

from components import *

class MovementProcessor(esper.Processor):
    def process(self):
        for ent, (moving, pos) in self.world.get_components(Movement, Position):
            if moving.delay != 0:
                moving.delay -= 1
                continue

            if moving.x > 0:
                amt = min(moving.x, moving.step)
                moving.x -= amt
                pos.x += amt
            elif moving.x < 0:
                amt = max(moving.x, -moving.step)
                moving.x -= amt
                pos.x += amt

            if moving.y > 0:
                amt = min(moving.y, moving.step)
                moving.y -= amt
                pos.y += amt
            elif moving.y < 0:
                amt = max(moving.y, -moving.step)
                moving.y -= amt
                pos.y += amt
