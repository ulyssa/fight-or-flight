from components import *

class Item:
    character: chr
    name: str
    desc: str

    def create_entities(self, world, pos):
        ent = world.create_entity(
            ScreenChar(self.character),
            Position(x=pos.x,y=pos.y,overlap=True),
            Collider(),
        )
        world.add_component(ent, self, Item)


class Food(Item):
    def __init__(self):
        self.character = '!'
        self.name = 'Food'
        self.desc = 'It smells delicious'

class Shiny(Item):
    def __init__(self):
        self.character = '$'
        self.name = 'Bright, shiny object'
        self.desc = 'It glows brilliantly; surely someone will trade for this'
