from items import *
from items import game_items as items
from numpy.random import choice


class Enemy:
    alive = True
    active = True
    health = 0

    def __init__(self, name, init_desc, enemy_type, blocks, inventory, death_text):
        self.name = name
        self.init_desc = init_desc
        self.type = enemy_type
        self.blocks = blocks
        self.inventory = inventory
        self.death_text = death_text

    def lose_health(self, damage):
        self.health = max(self.health - damage, 0)

        if self.health == 0:
            self.active = False
            self.alive = False

            for item in self.inventory:
                items[item].visible = 1
        return ('\n' + choice(self.death_text)) if self.alive is False else ''


class Goblin(Enemy):
    health = 1
    damage_dist = [[0, 20], [0.75, 0.25]]
    attack_text = {
        0: ['The goblin attacks with a knife, but misses by an inch.',
            'The goblin charges you, but you leap aside just in time.',
            'The goblin takes a swipe at you, but you block it.'],
        20: ['The goblin attacks with a knife. Ouch!',
             'The goblin charges you, knocking you backward.',
             'The goblin takes a swipe at you. It connects, leaving a nasty scratch.']
    }

    def __init__(self, name, init_desc, enemy_type, blocks, inventory):
        death_text = ['Your last attack was too much for the goblin. ' +
                      'It dies, immediately disappearing in a plume of black smoke.',
                      'The goblin dies instantly. What a pussy. Its body disappears in a plume of black smoke.']
        super().__init__(name, init_desc, enemy_type, blocks, inventory, death_text)


class Troll(Enemy):
    health = 140
    damage_dist = [[20, 40], [0.5, 0.5]]
    attack_text = {
        20: ['The face of the troll\'s axe knocks you backward.',
             'The troll\'s swipe leaves a nasty scratch.',
             'The troll knocks you back with the handle end of his axe. Oof!'],
        40: ['Critical hit! The troll\'s mighty left hook leaves you in a daze!',
             'Critical hit! The troll charges you, sending you flying!',
             'Critical hit! The troll\'s axe gets you dead on!']
    }

    def __init__(self, name, init_desc, enemy_type, blocks, inventory):
        death_text = ['The troll is overcome by your attack. He falls to the floor, and says:\n\n\"You fool. ' +
                      'You\'ll never defeat us! My brothers in arms will raze this land to the ground!\"\n\n' +
                      'The troll vanishes in a spectacular plume of black smoke. The ' +
                      'smoke clears to reveal a gleaming, sapphire coloured orb, and the fallen troll\'s axe.']
        super().__init__(name, init_desc, enemy_type, blocks, inventory, death_text)


class Wolf(Enemy):
    health = 60
    damage_dist = [[20, 40], [0.5, 0.5]]
    attack_text = {
        20: ['The wolf bites you, leaving you bloodied. Ouch!',
             'The wolf\'s claws leave a nasty scratch. It hurts!',
             'The wolf knocks you back with a powerful headbutt. Oof!'],
        40: ['Critical hit! The wolf\'s spiked teeth get you for double damage!',
             'Critical hit! The wolf\'s vicious slash hit its mark!']
    }

    def __init__(self, name, init_desc, enemy_type, blocks, inventory):
        death_text = ['Your attack defeats the winter wolf, which then disappears in a plume of black smoke.',
                      'The winter wolf is defeated. It emits a blood-curdling howl as it disappears in '
                      'a plume of black smoke.']
        super().__init__(name, init_desc, enemy_type, blocks, inventory, death_text)


enemy_constructors = {
    'goblin': Goblin,
    'troll': Troll,
    'wolf': Wolf
}

game_enemies = game_map['enemies']
game_enemies = {key: enemy_constructors[value['type']](
    value['name'], value['init_desc'], value['type'], value['blocks'], value['inventory'])
    for key, value in game_enemies.items()}

dt = game_enemies['moub3wolf'].death_text

for i in range(len(dt)):
    dt[i] = dt[i] + ' Left behind, in the snow, is a matchbook containing several matches.'
