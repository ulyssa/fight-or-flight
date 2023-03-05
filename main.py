#!/usr/bin/env python3
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
import tcod
import esper

from components import *
from processors import *

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.
BOX_HEIGHT = int(HEIGHT * .25) # Dialogue Box is 25% of screen height

def move_right(world, player):
    world.add_component(player, Velocity(x = 1))
    world.process()

def move_left(world, player):
    world.add_component(player, Velocity(x = -1))
    world.process()

def move_down(world, player):
    world.add_component(player, Velocity(y = 1))
    world.process()

def move_up(world, player):
    world.add_component(player, Velocity(y = -1))
    world.process()

def fire_projectile(world, player):
    player_pos = world.component_for_entity(player, Position)

    world.create_entity(
        ScreenChar(c=">", color=(255, 0, 0)),
        Position(x=player_pos.x,y=player_pos.y,z=player_pos.z,overlap=True),
        Velocity(x=2, duration=10),
        Decay(duration=10),
        Projectile(),
        Collider()
    )

    world.process()

KEY_COMMANDS = {
    tcod.event.KeySym.UP: move_up,
    tcod.event.KeySym.DOWN: move_down,
    tcod.event.KeySym.LEFT: move_left,
    tcod.event.KeySym.RIGHT: move_right,
    tcod.event.KeySym.f: fire_projectile,
}

def main() -> None:
    """Script entry point."""
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    xpos = 0
    ypos = HEIGHT - BOX_HEIGHT - 1
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
        world.add_processor(DecayProcessor(), priority=4)
        world.add_processor(MovementProcessor(), priority=3)
        world.add_processor(CollisionProcessor(), priority=2)
        world.add_processor(ConditionsProcessor(), priority=1)

        # Add player
        player = world.create_entity(
            ScreenChar('@'),
            Position(),
            Health(10, 10),
            Collider(),
        )

        for x in range(35, 50):
            for y in range(35, 45):
                tree = world.create_entity(
                    ScreenChar('#', color=(0, 255, 0)),
                    Position(x=x, y=y),
                    Collider()
                )

        for x in range(50, 65):
            for y in range(25, 45):
                tree = world.create_entity(
                    ScreenChar('#', color=(0, 255, 0)),
                    Position(x=x, y=y),
                    Collider()
                )


        world.process()

        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            
            #Draw and print the dialogue box
            console.draw_frame(x=0, y=HEIGHT - BOX_HEIGHT, width=WIDTH, height=BOX_HEIGHT)
            console.print_box(x=0, y=HEIGHT - BOX_HEIGHT, width=WIDTH, height=1, string=" DIALOGUE BOX ", alignment=tcod.CENTER)

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
                        KEY_COMMANDS[event.sym](world, player)
                else:
                    # Skip world processing for unhandled event.
                    continue
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()

