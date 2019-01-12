from enemies import *
from enemies import game_enemies as enemies
from collections import OrderedDict


class Room:
    def __init__(self, room_data):
        self.name = room_data['name']
        self.text = room_data['text']
        self.init_core = self.text['init_core']
        self.short_core = self.text['short_core'] if 'short_core' in self.text else self.text['init_core']
        self.long_core = self.text['long_core'] if 'long_core' in self.text else self.text['init_core']
        self.init_desc = ''
        self.short_desc = ''
        self.long_desc = ''
        self.inventory = {item: items[item] for item in room_data['items']}
        self.enemies = {e: enemies[e] for e in room_data['enemies']} if 'enemies' in room_data else {}
        self.state = room_data['state']
        self.commands = {}
        self.first_visit = 1
        self.room_blocks = room_data['blocks'] if 'blocks' in room_data else []
        self.enemy_blocks = []
        self.blocks = []
        self.item_aliases = {}
        self.update_item_aliases()
        self.update_blocks()
        self.update_desc()

    def lose_items(self, items_to_lose):

        for item in items_to_lose:
            del self.inventory[item]

    def gain_items(self, items_to_gain):
        self.inventory.update({item: items[item] for item in items_to_gain})

    def count_visible_items(self):
        count = 0

        for item in self.inventory.values():

            if item.visible:
                count += 1
        return count

    def update_desc(self):
        text_components = [[self.init_core], [self.short_core], [self.long_core]]
        descs = []

        for core in text_components:

            for x, y in self.state.items():

                if 'state' in self.text and x in self.text['state']:
                    string = self.text['state'][x][str(y)]

                    if string:
                        core.append(string)

            for key, value in self.inventory.items():

                if value.taken:
                    item_name = value.name.lower()

                    if item_name[-1] == 's':
                        verb, determiner = 'are', 'some'

                    elif item_name[0] in 'aeiou':
                        verb, determiner = 'is', 'an'

                    else:
                        verb, determiner = 'is', 'a'
                    core.append('\nThere {} {} {} here.'.format(verb, determiner, item_name))

                elif value.visible:
                    core.append(value.init_desc)

            for value in self.enemies.values():
                if value.active:
                    core.append(value.init_desc)

            descs.append(' '.join(core))
        self.init_desc, self.short_desc, self.long_desc = descs[0], descs[1], descs[2]

    def enemies_active(self):

        for enemy in self.enemies.values():

            if enemy.active:
                return True
        return False

    def update_blocks(self):
        self.enemy_blocks = [block for enemy in self.enemies.values() if enemy.active for block in enemy.blocks]
        self.blocks = list(set(self.room_blocks + self.enemy_blocks))
        return self.blocks

    def update_item_aliases(self):
        self.item_aliases = {key: value.aliases for key, value in self.inventory.items()}


game_rooms = game_map['rooms']
game_rooms = {name.lower(): Room(data) for name, data in game_rooms.items()}

game_rooms['mohut'].state = OrderedDict([
    ("frozen", 1),
    ("firewood", 0),
    ("open", 0),
    ("extra_directions", {"out": [3, 4, 8]})
])
