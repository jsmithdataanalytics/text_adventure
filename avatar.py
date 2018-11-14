from rooms import *
from rooms import game_rooms as rooms


levels, height, width = game_map['size']['levels'], game_map['size']['height'], game_map['size']['width']


class Avatar:
    def __init__(self):
        self.coords = game_map['spawn_point']
        self.room_name = ''
        self.room = None
        self.update_room()
        self.inventory = {item: items[item] for item in game_map['starting_inventory']}
        self.dead = False

    def update_room(self):
        self.room_name = game_map['layout'][self.coords[0]][self.coords[1]][self.coords[2]]
        self.room = rooms[self.room_name]

    def describe_current_room(self):
        self.room.update_desc()
        return self.room.text['desc']

    def get_items(self, new_items):
        self.inventory.update(new_items)
        item_list = list(new_items.keys())
        self.room.lose_items(item_list)

        for item in item_list:
            items[item].taken = 1
        return item_list

    def drop_items(self, to_drop):

        for item in to_drop:
            self.inventory.pop(item)
        self.room.gain_items(to_drop)

    def go(self, direction):
        valid_moves = {
            'north': (0, -1, 0),
            'south': (0, 1, 0),
            'east': (0, 0, 1),
            'west': (0, 0, -1),
            'up': (-1, 0, 0),
            'down': (1, 0, 0)
        }
        if direction in valid_moves:
            coord_bounds = [levels - 1, height - 1, width - 1]
            self.coords = [x + y for x, y in zip(self.coords, valid_moves[direction])]
            coord_checks = [(coord < 0 or coord > bound) for coord, bound in zip(self.coords, coord_bounds)]
            if any(coord_checks):
                self.coords = [x - y for x, y in zip(self.coords, valid_moves[direction])]
                return 'invalid_movement', direction
            else:
                self.update_room()
                return 'new_room', direction
        else:
            return 'invalid_command', direction


player = Avatar()
