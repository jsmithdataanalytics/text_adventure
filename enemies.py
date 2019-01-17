#!/usr/bin/env python

"""enemies.py: Defines and initialises the game's enemies."""

__author__ = "James Smith"

from numpy.random import choice


class Enemy:

    def __init__(self, enemy_data, items):
        self.health = 1
        self.items = items
        self.alive = True
        self.active = True
        self.name = enemy_data['name']
        self.init_desc = enemy_data['init_desc']
        self.type = enemy_data['type']
        self.blocks = enemy_data['blocks']
        self.inventory = enemy_data['inventory']
        self.charge = False
        self.death_text = enemy_data['death_text']
        self.evade_text = ['You leap back and avoid the {name}\'s attack.',
                           'You jump aside, narrowly avoiding the {name}\'s attack.']

        for ix, text in enumerate(self.evade_text):
            self.evade_text[ix] = text.format(name=self.name)

    def lose_health(self, damage):
        self.health = max(self.health - damage, 0)

        if self.health == 0:
            self.active = False
            self.alive = False

            for item in self.inventory:
                self.items[item].visible = 1
        return ('\n\n' + choice(self.death_text)) if self.alive is False else ''


class Goblin(Enemy):
    damage_dist = [[0, 20], [0.75, 0.25]]
    attack_text = {
        0: ['The goblin attacks with a knife, but misses by an inch.',
            'The goblin charges you, but you leap aside just in time.',
            'The goblin takes a swipe at you, but you block it.'],
        20: ['The goblin attacks with a knife. Ouch!',
             'The goblin charges you, knocking you backward.',
             'The goblin takes a swipe at you. It connects, leaving a nasty scratch.']
    }


class Troll(Enemy):
    damage_dist = [[20, 40], [0.5, 0.5]]
    attack_text = {
        20: ['The face of the troll\'s axe knocks you backward.',
             'The troll\'s swipe leaves a nasty scratch.',
             'The troll knocks you back with the handle end of its axe. Oof!'],
        40: ['Critical hit! The troll\'s mighty left hook leaves you in a daze!',
             'Critical hit! The troll charges you, sending you flying!',
             'Critical hit! The troll\'s axe gets you dead on!']
    }

    def __init__(self, enemy_data, items):
        super().__init__(enemy_data, items)
        self.health = 140


class Wolf(Enemy):
    damage_dist = [[20, 40], [0.5, 0.5]]
    attack_text = {
        20: ['The wolf bites you, leaving you bloodied. Ouch!',
             'The wolf\'s claws leave a nasty scratch. It hurts!',
             'The wolf knocks you back with a powerful headbutt. Oof!'],
        40: ['Critical hit! The wolf\'s spiked teeth get you for double damage!',
             'Critical hit! The wolf\'s vicious slash hit its mark!']
    }

    def __init__(self, enemy_data, items):
        super().__init__(enemy_data, items)
        self.health = 60


class Giant(Enemy):
    damage_dist = [[40, 80], [0.7, 0.3]]
    attack_text = {
        40: ['The frost giant kicks you backward. Oof!',
             'The frost giant\'s punch connects. Ouch!',
             'The giant knocks you back with the handle end of its hammer. Oof!'],
        80: ['Critical hit! The frost giant\'s mighty left hook leaves you in a daze!',
             'Critical hit! The frost giant charges you, sending you flying!',
             'Critical hit! The giant\'s hammer gets you dead on!']
    }
    charge_prob = 0.5
    charge_text = 'The frost giant lifts its might hammer over its head...'
    charge_evade_text = ['You jump back just in time, as the frost giant\'s mighty hammer comes crashing down, '
                         'leaving a small crater where you once stood.',
                         'You leap aside, just barely avoiding the frost giant\'s devastating hammer attack.']
    charge_attack_text = 'While you get started with that instead of worrying about the frost giant\'s attack, the ' \
                         'hammer comes crashing down on you!'

    def __init__(self, enemy_data, items):
        super().__init__(enemy_data, items)
        self.health = 200


def initialise_enemies(game_map, items):
    enemy_constructors = {
        'goblin': Goblin,
        'troll': Troll,
        'wolf': Wolf,
        'giant': Giant
    }

    game_enemies = game_map['enemies']
    game_enemies = {key: enemy_constructors[value['name']](value, items) for key, value in game_enemies.items()}

    dt = game_enemies['moub3wolf'].death_text

    for i in range(len(dt)):
        dt[i] = dt[i] + ' Left behind, in the snow, is a matchbook containing several matches.'
    return game_enemies
