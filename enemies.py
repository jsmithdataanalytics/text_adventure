from items import *
from numpy.random import choice


class Enemy:
    alive = True
    active = True
    health = 0

    def __init__(self, name, init_desc, enemy_type):
        self.name = name
        self.init_desc = init_desc
        self.type = enemy_type

    def lose_health(self, damage):
        self.health = max(self.health - damage, 0)

        if self.health == 0:
            self.active = False
            self.alive = False

            if self.name == 'wood4goblin':
                game_map['layout'][3][2][3] = 'wood5'


class Goblin(Enemy):
    health = 1

    damage_dist = [[0, 20],
                   [0.75, 0.25]]

    attack_text = {
        0: ['The goblin attacks with a knife, but misses by an inch.',
            'The goblin charges you, but you leap aside just in time.',
            'The goblin takes a swipe at you, but you block it.'],

        20: ['The goblin attacks with a knife. Ouch!',
             'The goblin charges you, knocking you to the floor.',
             'The goblin takes a swipe at you. It connects, leaving a nasty scratch.']
    }

    death_text = ['Your last attack was too much for the goblin. ' +
                  'It dies, immediately disappearing in a plume of black smoke.',
                  'The goblin dies instantly. What a pussy. Its body disappears in a plume of black smoke.']

    def lose_health(self, damage):
        super().lose_health(damage)
        return choice(self.death_text) if self.alive is False else ''


enemy_constructors = {
    'goblin': Goblin
}

game_enemies = game_map['enemies']
game_enemies = {key: enemy_constructors[value['type']](value['name'], value['init_desc'], value['type'])
                for key, value in game_enemies.items()}
