from items import *

class Enemy:
    character: chr
    name: str
    desc: str

    health: int
    inventory: list

    def create_entities(self, world, pos):
        ent = world.create_entity(
            ScreenChar(self.character),
            Position(x=pos.x,y=pos.y,z=pos.z),
            Health(self.health, self.health, inventory=self.inventory),
            Collider(),
            Seeker(),
        )
        world.add_component(ent, self, Enemy)

class Human(Enemy):
    def __init__(self):
        self.character = 'o'
        self.name = "Human"
        self.desc = "Maybe they have food..."
        self.health = 5
        self.inventory = [Food()]
