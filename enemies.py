from items import *
from items import game_items as items
from numpy.random import choice


class Enemy:
    alive = True
    active = True
    health = 0
    death_text = []

    def __init__(self, name, init_desc, enemy_type, blocks):
        self.name = name
        self.init_desc = init_desc
        self.type = enemy_type
        self.blocks = blocks

    def lose_health(self, damage):
        self.health = max(self.health - damage, 0)

        if self.health == 0:
            self.active = False
            self.alive = False
        return ('\n' + choice(self.death_text)) if self.alive is False else ''


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


class Troll(Enemy):
    health = 100

    damage_dist = [[20, 40],
                   [0.5, 0.5]]

    attack_text = {
        20: ['The face of the troll\'s axe knocks you off your feet.',
             'The troll\'s swipe leaves a nasty scratch.',
             'The troll knocks you back with the handle end of his axe. Oof!'],

        40: ['Critical hit! The troll\'s mighty left hook leaves you in a daze!',
             'Critical hit! The troll charges you, sending you flying!',
             'Critical hit! The troll\'s axe gets you dead on!']
    }

    death_text = ['Finally, the troll is overcome by your relentless barrage of attacks. ' +
                  'He falls to the floor, and says:\n\n\"You fool. You\'ll never defeat us! My brothers in arms ' +
                  'will raze this land to the ground!\"\n\nThe troll vanishes in a spectacular plume of black smoke.' +
                  ' The smoke clears to reveal a gleaming, sapphire coloured orb, and the fallen troll\'s axe.']

    def lose_health(self, damage):
        self.health = max(self.health - damage, 0)

        if self.health == 0:
            self.active = False
            self.alive = False
            items['axe'].visible = 1
            items['sapphire'].visible = 1
        return ('\n' + choice(self.death_text)) if self.alive is False else ''


enemy_constructors = {
    'goblin': Goblin,
    'troll': Troll
}

game_enemies = game_map['enemies']
game_enemies = {key: enemy_constructors[value['type']](
    value['name'], value['init_desc'], value['type'], value['blocks']) for key, value in game_enemies.items()}
