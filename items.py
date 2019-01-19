#!/usr/bin/env python

"""items.py: Defines and initialises the game's items."""

__author__ = "James Smith"

# from json import load


class Item:
    def __init__(self, item_data):
        self.name = item_data['name']
        self.aliases = item_data['aliases'] if 'aliases' in item_data else []
        self.init_desc = item_data['text']['init_desc']
        self.text = item_data['text']
        self.taken = 0
        self.visible = item_data['visible']
        self.commands = {}
        self.combat_commands = {}
        self.damage_dist = [[], []]
        self.combat_text = {}


# def load_map():
#     with open('map.json') as f:
#         game_map = load(f)
#     return game_map


def initialise_checkpoints():
    return {'jimbo': False,
            'apoth': False,
            'vines': False,
            'escape': False,
            'dingleflowers': False,
            'easter': False,
            'thaw': False,
            'water': False}


def initialise_items(game_map):
    game_items = game_map['items']
    game_items = {name.lower(): Item(data) for name, data in game_items.items()}

    game_items['sword'].combat_text['goblin'] = {0: ['You swing your sword at the goblin, but miss.',
                                                     'You lunge at the goblin, but it leaps aside, avoiding your '
                                                     'attack.'],
                                                 20: ['Your slice attack connects, ' +
                                                      'finding its mark beneath the goblin\'s thin armour.',
                                                      'You lunge at the goblin with your sword. It\'s a hit!',
                                                      'The goblin is too slow for you, and gets caught by your '
                                                      'attack.'],
                                                 40: ['Critical hit! Your blade strikes the goblin for double damage!']}
    game_items['sword'].combat_text['troll'] = {0: ['You swing your sword at the troll, but miss.',
                                                    'You lunge at the troll, but it brushes off your attack like it ' +
                                                    'was nothing.'],
                                                20: ['Your slice attack finds the weak spot in the troll\'s armour.',
                                                     'You lunge fiercely at the troll with your sword. Got the '
                                                     'bastard!',
                                                     'You\'re too fast for the sluggish troll, who takes the full '
                                                     'brunt of your attack.'],
                                                40: ['Critical hit! Your blade strikes the troll for double damage!']}
    game_items['sword'].combat_text['wolf'] = {0: ['You swing your sword at the wolf, but miss.',
                                                   'You lunge at the wolf, but it leaps aside.'],
                                               20: ['Your slice attack makes contact. Take that!',
                                                    'You lunge fiercely at the wolf with your sword. Got the bastard!',
                                                    'Your speed catches the wolf off guard. It takes the full brunt ' +
                                                    'of your attack!'],
                                               40: ['Critical hit! Your blade strikes the wolf for double damage!']}
    game_items['sword'].combat_text['giant'] = {0: ['You swing your sword at the frost giant, but miss.',
                                                    'You lunge at the giant, but it leaps aside.'],
                                                20: ['Your slice attack makes contact. Take that!',
                                                     'You lunge fiercely at the frost giant with your sword. '
                                                     'Got the bastard!',
                                                     'Your speed catches the giant off guard. It takes the full '
                                                     'brunt of your attack!'],
                                                40: ['Critical hit! Your blade strikes the frost giant for double '
                                                     'damage!']}
    game_items['sword'].damage_dist = [[0, 20, 40], [0.4, 0.4, 0.2]]
    game_items['axe'].combat_text['wolf'] = {0: ['You swing your axe at the wolf, but miss.',
                                                 'You lunge at the wolf with your axe, but it leaps aside.'],
                                             30: ['Your axe attack makes contact. Take that!',
                                                  'You swing your axe at the wolf. Got the bastard!',
                                                  'Your speed catches the wolf off guard. It takes the full brunt ' +
                                                  'of your attack!'],
                                             60: ['Critical hit! Your axe strikes the wolf for double damage!']}
    game_items['axe'].combat_text['giant'] = {0: ['You swing your axe at the frost giant, but miss.',
                                                  'You lunge at the frost giant with your axe, but it leaps aside.'],
                                              30: ['Your axe attack makes contact. Take that!',
                                                   'You swing your axe at the frost giant. Got the bastard!',
                                                   'Your speed catches the giant off guard. It takes the full brunt ' +
                                                   'of your attack!'],
                                              60: ['Critical hit! Your axe strikes the frost giant for double damage!']}
    game_items['axe'].damage_dist = [[0, 30, 60], [0.4, 0.4, 0.2]]
    return game_items
