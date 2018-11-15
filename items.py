from json import load


with open('map.json') as f:
    game_map = load(f)


class Item:
    def __init__(self, item_data):
        self.name = item_data['name']
        self.init_desc = item_data['init_desc']
        self.taken = 0
        self.visible = item_data['visible']
        self.commands = {}


game_items = game_map['items']
game_items = {name.lower(): Item(data) for name, data in game_items.items()}
