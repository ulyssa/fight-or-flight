#!/usr/bin/env python3
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
from enum import Enum

import tcod
import esper
import random
import numpy as np

from components import *
from entities import *
from processors import *

from enemies import *
from items import *

class InfoBox(Enum):
    NONE = 0
    HELP = 1
    EQUIP = 2

def move_right(game):
    """Move your character right"""
    level = game.current_level()
    level.world.add_component(level.player, Velocity(x = 1))
    level.tick()

def move_left(game):
    """Move your character left"""
    level = game.current_level()
    level.world.add_component(level.player, Velocity(x = -1))
    level.tick()

def move_down(game):
    """Move your character down"""
    level = game.current_level()
    level.world.add_component(level.player, Velocity(y = 1))
    level.tick()

def move_up(game):
    """Move your character up"""
    level = game.current_level()
    level.world.add_component(level.player, Velocity(y = -1))
    level.tick()

def fire_up(game):
    """Fire a projectile up"""
    level = game.current_level()
    player_pos = level.world.component_for_entity(level.player, Position)

    player_stamina = level.world.component_for_entity(level.player, Stamina)

    if player_stamina.current > 0:
        level.world.create_entity(
            ScreenChar(c="*", color=(255, 0, 0)),
            Position(x=player_pos.x,y=player_pos.y,z=player_pos.z,overlap=True),
            Velocity(x=0, y=-1, duration=10), 
            Decay(duration=10),
            Projectile(damage=1),
            Collider()
        )

        # How do we call exert on player each time they fire?

    level.tick()

def fire_down(game):
    """Fire a projectile down"""
    level = game.current_level()
    player_pos = level.world.component_for_entity(level.player, Position)

    player_stamina = level.world.component_for_entity(level.player, Stamina)

    if player_stamina.current > 0: 
        level.world.create_entity(
            ScreenChar(c="*", color=(255, 0, 0)),
            Position(x=player_pos.x,y=player_pos.y,z=player_pos.z,overlap=True),
            Velocity(x=0, y=1, duration=10), 
            Decay(duration=10),
            Projectile(damage=1),
            Collider()
        )

    level.tick()

def fire_left(game):
    """Fire a projectile to the left"""
    level = game.current_level()
    player_pos = level.world.component_for_entity(level.player, Position)

    player_stamina = level.world.component_for_entity(level.player, Stamina)

    if player_stamina.current > 0:
        level.world.create_entity(
            ScreenChar(c="*", color=(255, 0, 0)),
            Position(x=player_pos.x,y=player_pos.y,z=player_pos.z,overlap=True),
            Velocity(x=-1, y=0, duration=10), 
            Decay(duration=10),
            Projectile(damage=1),
            Collider()
        )

    level.tick()

def fire_right(game):
    """Fire a projectile to the right"""
    level = game.current_level()
    player_pos = level.world.component_for_entity(level.player, Position)

    player_stamina = level.world.component_for_entity(level.player, Stamina)

    if player_stamina.current > 0:
        level.world.create_entity(
            ScreenChar(c="*", color=(255, 0, 0)),
            Position(x=player_pos.x,y=player_pos.y,z=player_pos.z,overlap=True),
            Velocity(x=1, y=0, duration=10), 
            Decay(duration=10),
            Projectile(damage=1),
            Collider()
        )

    level.tick()

def recharge(game):
    """Increase stamina to fire ESP"""
    level = game.current_level()

    # how to call rest() against Stamina?

    level.tick()

def show_help(game):
    """Toggle showing this help menu"""
    if game.info == InfoBox.HELP:
        game.info = InfoBox.NONE
    else:
        game.info = InfoBox.HELP

class Level:
    def __init__(self):
        self.world = esper.World()

        # Processors
        self.world.add_processor(DecayProcessor(), priority=5)
        self.world.add_processor(PathProcessor(), priority=4)
        self.world.add_processor(MovementProcessor(), priority=3)
        self.world.add_processor(CollisionProcessor(), priority=2)
        self.world.add_processor(ConditionsProcessor(), priority=1)
        self.world.add_processor(DeathProcessor(), priority=0)

        # Add player
        self.player = make_player(self.world)

        # Generate name for this neighborhood.
        self.neighborhood = generateName()

        makeBuilding(self.world, 22, 20, 5, 5)
        makeBuilding(self.world, 30, 10, 5, 5)

        for x in range(50, 65):
            for y in range(25, 45):
                tree = self.world.create_entity(
                    ScreenChar('#', color=(0, 255, 0)),
                    Position(x=x, y=y),
                    Collider() # TODO: Resolve how to have people (missiles too?) but not player collide with trees
                )

        human_pos = Position(random.randint(0, WIDTH), random.randint(0, HEIGHT - BOX_HEIGHT))
        human = Human()
        human.create_entities(self.world, human_pos)

    def tick(self):
        self.world.process(self.player)

class Game:
    def __init__(self):
        self.level = Level()
        self.info = InfoBox.NONE

    def current_level(self):
        return self.level

    def current_world(self):
        return self.current_level().world

    def draw(self, console):
        console.clear()

        #Draw and print the dialogue box
        title = " " + self.current_level().neighborhood + " "
        console.draw_frame(x=0, y=WORLD_HEIGHT, width=WIDTH, height=BOX_HEIGHT)
        console.print_box(x=0, y=WORLD_HEIGHT, width=WIDTH, height=1, string=title, alignment=tcod.CENTER)

        # Render entities to their positions.
        for ent, (sc, pos) in self.current_world().get_components(ScreenChar, Position):
            console.print(x=pos.x, y=pos.y, string=sc.c, fg=sc.color)

        if self.info == InfoBox.HELP:
            x = 50
            y = 0

            console.draw_frame(x=x, y=y, width=30,height=40)
            console.print_box(x=x, y=y, width=30, height=1, string="Help Menu", alignment=tcod.CENTER)

            x += 1

            for char in CHAR_COMMANDS:
                y += 1
                console.print(x=x, y=y, string=f"{char} - {CHAR_COMMANDS[char].__doc__}")


KEY_COMMANDS = {
    tcod.event.KeySym.UP: move_up,
    tcod.event.KeySym.DOWN: move_down,
    tcod.event.KeySym.LEFT: move_left,
    tcod.event.KeySym.RIGHT: move_right,
}

CHAR_COMMANDS = {
    'w': fire_up,
    's': fire_down,
    'a': fire_left,
    'd': fire_right,
    'r': recharge,
    '?': show_help,
}

FIRST_NAMES = ["BROOKDALE", "CARRIAGE", "CEDAR", "CHERRY", "EAGLE", "ELM", "EVERGREEN", "FOREST", "HIGHLAND", "HUNTER", "LAKE", "LINCOLN", "MAPLE", "OAK", "PINE", "PALM", "PRARIE", "PROVIDENCE", "SHADY", "SILVER", "SUMMER", "WILD", "WILLOW", "WINTER"]
LAST_NAMES  = ["ACRES", "CANYON", "COURTS", "COVE", "CREST", "CROSSING", "FALLS", "FARMS", "GLEN", "GROVE", "HEIGHTS", "HILLS", "KNOLL", "LAKE", "LANDING", "MEADOWS", "PARK", "PINES", "PLACE", "RIDGE", "RUN", "SPRINGS", "TRAILS", "VISTA", "WOODS"]

def generateName() -> str:
    """Returns a randomly generated two-word name as a string"""
    first = FIRST_NAMES[random.randint(0, len(FIRST_NAMES) - 1)]
    last = LAST_NAMES[random.randint(0, len(LAST_NAMES) - 1)]
    return first + " " + last


def main() -> None:
    """Script entry point."""

    xpos = 0
    ypos = WORLD_HEIGHT - 1

    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT, order="F")
    # Create a window based on this console and tileset.
    with tcod.context.new(  # New window for a console of size columns×rows.
        columns=console.width, rows=console.height, tileset=tileset,
    ) as context:
        game = Game()

        game.current_level().tick()

        while True:  # Main loop, runs until SystemExit is raised.
            game.draw(console)
            context.present(console)  # Show the console.
            # This event loop will wait until at least one event is processed before exiting.
            # For a non-blocking event loop replace `tcod.event.wait` with `tcod.event.get`.
            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                print(event)  # Print event names and attributes.
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym in KEY_COMMANDS:
                        print(f"Command: {KEY_COMMANDS[event.sym]}")
                        KEY_COMMANDS[event.sym](game)
                    else:
                        print(f"Unprocessed keypress: {event.sym}")
                elif isinstance(event, tcod.event.TextInput):
                    if event.text == 'm': # Just generates new neighborhood name for now
                        game.current_level().neighborhood = generateName()
                    elif event.text in CHAR_COMMANDS:
                        print(f"Command: {CHAR_COMMANDS[event.text]}")
                        CHAR_COMMANDS[event.text](game)
                        # TODO: REDUCE STAMINA BY 1 HERE?
                    else:
                        print(f"Unprocessed keypress: {event.text}")
                else:
                    # Skip world processing for unhandled event.
                    continue

        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()

