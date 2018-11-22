from items import *
from items import game_items as items


class Room:
    def __init__(self, room_data):
        self.name = room_data['name']
        self.text = {'desc': room_data['text']['init_desc']}
        self.text.update(room_data['text'])
        self.inventory = {item: items[item] for item in room_data['items']}
        self.state = room_data['state']
        self.commands = {}
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
        text_components = [self.text['init_desc']]

        for x, y in self.state.items():

            if 'state' in self.text and x in self.text['state']:
                text_components.append(self.text['state'][x][str(y)])

        for key, value in self.inventory.items():

            if value.taken:
                item_name = value.name.lower()
                determiner = 'an' if item_name[0] in 'aeiou' else 'a'
                text_components.append('\nThere is {} {} here.'.format(determiner, item_name))

            elif value.visible:
                text_components.append(value.init_desc)
        self.text['desc'] = ' '.join(text_components)


game_rooms = game_map['rooms']
game_rooms = {name.lower(): Room(data) for name, data in game_rooms.items()}
