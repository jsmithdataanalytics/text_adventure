#!/usr/bin/env python

"""avatar.py: Defines and initialises the avatar."""

__author__ = "James Smith"

from re import fullmatch


class Avatar:

    def __init__(self, game_map, checkpoints, items, rooms):
        self.game_map = game_map
        self.levels = len(game_map['layout'])
        self.height = len(game_map['layout'][0])
        self.width = len(game_map['layout'][0][0])
        self.checkpoints = checkpoints
        self.items = items
        self.rooms = rooms
        self.game_map = game_map
        self.name = ''
        self.coords = game_map['spawn_point']
        self.room_name = ''
        self.room = None
        self.update_room()
        self.inventory = {item: items[item] for item in game_map['starting_inventory']}
        self.health = 120
        self.dead = False
        self.lives = 3
        self.mode = 'normal'
        self.item_aliases = {}
        self.update_item_aliases()
        self.boots = False
        self.lit_match = {
            'status': False,
            'count': 4
        }

    def mimic(self, avatar):
        self.__dict__.update(avatar.__dict__)

    def set_name(self, name):
        self.name = name

    def update_room(self):
        self.room_name = self.game_map['layout'][self.coords[0]][self.coords[1]][self.coords[2]]
        self.room = self.rooms[self.room_name]

    def describe_current_room(self, desc_type='short'):
        self.room.update_desc()

        if desc_type == 'init':
            return self.room.init_desc

        elif desc_type == 'short':

            if self.checkpoints['vines'] and not self.checkpoints['escape'] and \
                    self.room_name not in ['deade', 'dead2']:
                return self.room.short_desc + ' Thorny vines continue to spring up just behind you, trying to stop ' \
                                              'you escaping with the Dingleflowers!'

            else:
                return self.room.short_desc

        elif desc_type == 'long':
            return self.room.long_desc

        else:
            raise ValueError('Unhandled description type')

    def get_items(self, new_items):
        self.inventory.update(new_items)
        item_list = {key: value.taken for key, value in new_items.items()}
        self.room.lose_items(item_list)

        for item in item_list:
            self.items[item].taken = 1

            if item == 'snow boots':
                self.room.state['open'] = 2
        return item_list

    def get_all_visible_items(self):
        new_items = {key: value for key, value in self.room.inventory.items() if value.visible}
        return self.get_items(new_items)

    def lose_items(self, items_to_lose):

        for item in items_to_lose:
            del self.inventory[item]

    def drop_items(self, to_drop):
        self.lose_items(to_drop)
        self.room.gain_items(to_drop)

    def go(self, direction, reference):
        valid_moves = {
            'north': (0, -1, 0),
            'south': (0, 1, 0),
            'east': (0, 0, 1),
            'west': (0, 0, -1),
            'up': (-1, 0, 0),
            'down': (1, 0, 0)
        }

        if (self.room_name == 'moub1' and direction == 'east') or \
                (self.room_name == 'mouc1' and direction == 'north'):

            if self.boots is False:
                return 'no_boots', direction

        blocked = self.room.update_blocks()

        if direction in blocked:
            return 'invalid_movement', direction

        if direction in valid_moves:
            coord_bounds = [self.levels - 1, self.height - 1, self.width - 1]
            self.coords = [x + y for x, y in zip(self.coords, valid_moves[direction])]
            coord_checks = [(coord < 0 or coord > bound) for coord, bound in zip(self.coords, coord_bounds)]

            if any(coord_checks):
                self.coords = [x - y for x, y in zip(self.coords, valid_moves[direction])]
                return 'invalid_movement', direction

            else:
                self.update_room()

                if self.room_name == 'block':
                    self.coords = [x - y for x, y in zip(self.coords, valid_moves[direction])]
                    self.update_room()
                    return 'invalid_movement', direction

                else:
                    return 'new_room', direction

        elif direction in ['in', 'out']:
            aliases = [alias.format(player_name=self.name.lower())
                       for alias in self.room.state['extra_directions']['aliases']]
            ref_checks = [fullmatch(alias, reference) for alias in aliases]

            if reference == '' or any(ref_checks):
                self.coords = self.room.state['extra_directions'][direction]
                self.update_room()

                if self.room_name == 'jimbg':
                    self.checkpoints['jimbo'] = True

                if self.room_name == 'apoth':
                    self.checkpoints['apoth'] = True
                return 'new_room', direction

            else:
                return 'invalid_command', direction

        elif direction == 'no_stairs':
            return 'no_stairs', direction

        elif direction == 'no_inout':
            return 'no_inout', direction

        elif direction == 'invalid':
            return 'invalid_command', direction

        else:
            raise (ValueError('Unhandled direction'))

    def update_item_aliases(self):
        self.item_aliases = {key: value.aliases for key, value in self.inventory.items()}


def initialise_player(game_map, checkpoints, items, rooms):
    return Avatar(game_map, checkpoints, items, rooms)
