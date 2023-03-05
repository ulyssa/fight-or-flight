#!/usr/bin/env python3
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
import tcod
import esper
import random

from components import *
from processors import *

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.
BOX_HEIGHT = int(HEIGHT * .25) # Dialogue Box is 25% of screen height
WORLD_HEIGHT = HEIGHT - BOX_HEIGHT

KEY_COMMANDS = {
    tcod.event.KeySym.UP: "move N",
    tcod.event.KeySym.DOWN: "move S",
    tcod.event.KeySym.LEFT: "move W",
    tcod.event.KeySym.RIGHT: "move E",
    tcod.event.KeySym.w: "move N",
    tcod.event.KeySym.s: "move S",
    tcod.event.KeySym.a: "move W",
    tcod.event.KeySym.d: "move E",
    tcod.event.KeySym.m: "new area"
}

FIRST_NAMES = ["BROOKDALE", "CARRIAGE", "CEDAR", "CHERRY", "EAGLE", "ELM", "EVERGREEN", "FOREST", "HIGHLAND", "HUNTER", "LAKE", "LINCOLN", "MAPLE", "OAK", "PINE", "PALM", "PRARIE", "PROVIDENCE", "SHADY", "SILVER", "SUMMER", "WILD", "WILLOW", "WINTER"]
LAST_NAMES  = ["ACRES", "CANYON", "COURTS", "COVE", "CREST", "CROSSING", "FALLS", "FARMS", "GLEN", "GROVE", "HEIGHTS", "HILLS", "KNOLL", "LAKE", "LANDING", "MEADOWS", "PARK", "PINES", "PLACE", "RIDGE", "RUN", "SPRINGS", "TRAILS", "VISTA", "WOODS"]

def generateName() -> str:
    # Returns a randomly generated two-word name as a string
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
        world = esper.World()

        # Processors
        world.add_processor(MovementProcessor(), priority=2)

        # Add player
        player = world.create_entity(
            ScreenChar('@'),
            Position(),
            Health(10, 10)
        )

        human = world.create_entity(
            ScreenChar('$'),
            Position(random.randint(0, WIDTH), random.randint(0, HEIGHT - BOX_HEIGHT)),
            Health(5, 5)
        )


        for x in range(35, 50):
            for y in range(35, 45):
                building = world.create_entity(
                    ScreenChar('%', color=[200, 200, 200]),
                    Position(x=x, y=y)
                )

        for x in range(50, 65):
            for y in range(25, 45):
                tree = world.create_entity(
                    ScreenChar('#', color=[0, 255, 0]),
                    Position(x=x, y=y)
                )

        neighborhood = generateName()

        world.process()

        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            

            #Draw and print the dialogue box
            title = " " + neighborhood + " "
            console.draw_frame(x=0, y=WORLD_HEIGHT, width=WIDTH, height=BOX_HEIGHT)
            console.print_box(x=0, y=WORLD_HEIGHT, width=WIDTH, height=1, string=title, alignment=tcod.CENTER)

            for ent, (sc, pos) in world.get_components(ScreenChar, Position):
                console.print(x=pos.x, y=pos.y, string=sc.c, fg=sc.color)

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
                        if KEY_COMMANDS[event.sym] == "move N":
                            # TODO: If Player is at X = 0, start at bottom of new neighborhood
                            world.add_component(player, Movement(y = -1))
                        elif KEY_COMMANDS[event.sym] == "move S":
                            # TODO: If Player is at Y = WORLD_HEIGHT, start at top of new neighborhood
                            world.add_component(player, Movement(y = 1))
                        elif KEY_COMMANDS[event.sym] == "move W":
                            # TODO: If Player is at X = 0, start at right of new neighborhood
                            world.add_component(player, Movement(x = -1))
                        elif KEY_COMMANDS[event.sym] == "move E":
                            # TODO: If Player is at X = WIDTH, start at left of new neighborhood
                            world.add_component(player, Movement(x = 1))
                        elif KEY_COMMANDS[event.sym] == "new area":
                            neighborhood = generateName()

                world.process()
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()

