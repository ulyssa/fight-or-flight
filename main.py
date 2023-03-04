#!/usr/bin/env python3
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
import tcod

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.

KEY_COMMANDS = {
    tcod.event.KeySym.UP: "move N",
    tcod.event.KeySym.DOWN: "move S",
    tcod.event.KeySym.LEFT: "move W",
    tcod.event.KeySym.RIGHT: "move E",
}

def main() -> None:
    """Script entry point."""
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    xpos = 0
    ypos = 0
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT, order="F")
    # Create a window based on this console and tileset.
    with tcod.context.new(  # New window for a console of size columns×rows.
        columns=console.width, rows=console.height, tileset=tileset,
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            console.print(x=xpos, y=ypos, string="Ulyssa")
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
                        if event.sym == tcod.event.KeySym.UP:
                            ypos -= 1
                            if ypos < 0:
                                ypos = 0
                        elif event.sym == tcod.event.KeySym.DOWN:
                            ypos += 1
                            if ypos >= HEIGHT:
                                ypos = HEIGHT - 1
                        elif event.sym == tcod.event.KeySym.LEFT:
                            xpos -= 1
                            if xpos < 0:
                                xpos = 0
                        elif event.sym == tcod.event.KeySym.RIGHT:
                            xpos += 1
                            if xpos >= WIDTH:
                                xpos = WIDTH - 1
                 # elif isinstance(event, tcod.event.MouseMotion(x=x, y=y, pixel_motion=pixel_motion, tile=tile, tile_motion=tile_motion)):
                 #     xpos = x
                 #     ypos = y
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()

