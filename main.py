#!/usr/bin/env python3
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
import tcod

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.
BOX_HEIGHT = int(HEIGHT * .25) # Dialogue Box is 25% of screen height


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
        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            
            console.draw_rect(x=35, y=35, width=15, height=10, ch=0x23, fg=[0, 255, 0])
            console.draw_rect(x=50, y=25, width=15, height=20, ch=0x23, fg=[0, 255, 0]) # 0x23 = #


            #Draw and print the dialogue box
            console.draw_frame(x=0, y=HEIGHT - BOX_HEIGHT, width=WIDTH, height=BOX_HEIGHT)
            console.print_box(x=0, y=HEIGHT - BOX_HEIGHT, width=WIDTH, height=1, string=" DIALOGUE BOX ", alignment=tcod.CENTER)
            console.print(x=xpos, y=ypos, string="@", fg=[255, 255, 255])


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
                            if ypos >= HEIGHT - BOX_HEIGHT:
                                ypos = HEIGHT - BOX_HEIGHT - 1
                        elif event.sym == tcod.event.KeySym.LEFT:
                            xpos -= 1
                            if xpos < 0:
                                xpos = 0
                        elif event.sym == tcod.event.KeySym.RIGHT:
                            # TODO: If string is more than 1 char, stop string from running out of screen
                            xpos += 1
                            if xpos >= WIDTH:
                                xpos = WIDTH - 1
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()

