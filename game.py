#!/usr/bin/env python

"""main.py: Definition of Game class."""

__author__ = "James Smith"

from collections import OrderedDict
from copy import deepcopy
from json import dumps, loads
from random import randint
from time import time
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
import crypto
from commands import *


class Game:
    encryption_key = crypto.key
    cipher_suite = Fernet(encryption_key)

    def __init__(self, text_width, game_map, checkpoints, items, enemies, rooms, player, generic_commands):
        self.text_width = text_width
        self.complete = False
        self.over = False
        self.quit = False
        self.game_map = game_map
        self.checkpoints = checkpoints
        self.old_checkpoints = deepcopy(checkpoints)
        self.items = items
        self.enemies = enemies
        self.rooms = rooms
        self.player = player
        self.generic_commands = generic_commands
        self.output = None
        self.last_checkpoint = None
        self.snapshot = None
        self.start = time()
        self.filename = None
        self.time = self.start - self.start

    def updates(self, command, response):
        self.player.room.update_blocks()
        self.player.room.update_item_aliases()
        self.player.update_item_aliases()

        if self.rooms['shrin'].state['orbs'] == 1:
            self.complete = True
            return

        if self.player.health <= 0:
            self.player.lives -= 1
            display('You have died.', before=0)

            if self.player.lives > 0:

                if self.player.lives == 1:
                    display('You have {} life left. Reverting to the last checkpoint...'.format(
                        self.player.lives), after=1)

                else:
                    display('You have {} lives left. Reverting to the last checkpoint...'.format(
                        self.player.lives), after=1)
                self.restore(self.player.lives)
                self.player.health = 60

                if self.last_checkpoint == 'vines':
                    text = 'You are at the end of the forest trail, in the process of taking the Dingleflowers.\n\n'
                    output = self.output.split('\n')[-1]
                    display(text + output, before=0, after=1)

                elif self.last_checkpoint == 'dingleflowers':
                    text = 'You are in the Potion Master\'s teepee, and have just given her the Dingleflowers.\n\n'
                    display(text + self.output, before=0, after=1)

                elif self.last_checkpoint in ['easter', 'thaw']:
                    display(self.player.describe_current_room('long'), before=0, after=1)

                else:
                    display(self.output, before=0, after=1)

            else:
                self.over = True
                return

        if self.checkpoints != self.old_checkpoints:

            if self.old_checkpoints is not None:

                for checkpoint in self.checkpoints:

                    if self.checkpoints[checkpoint] != self.old_checkpoints[checkpoint]:
                        self.last_checkpoint = checkpoint
                        break

            self.old_checkpoints = deepcopy(self.checkpoints)
            self.snapshot = None
            self.snapshot = deepcopy(self)

        if not isinstance(command, InvalidCommand) and \
                not isinstance(command, CommandsCommand) and \
                not isinstance(command, SaveCommand) and \
                not (isinstance(command, AttackCommand) and response.validity == 'invalid'):

            if self.enemies['mouc2giant'].active:

                previous = self.enemies['mouc2giant'].charge
                self.enemies['mouc2giant'].charge = False

                if self.player.mode == 'combat' and self.player.room_name == 'mouc2' and not previous:

                    if randint(0, 1):
                        self.enemies['mouc2giant'].charge = True
                        display(self.enemies['mouc2giant'].charge_text, before=0, after=1)

            if self.player.lit_match['status']:
                self.player.lit_match['count'] -= 1

                if self.player.lit_match['count'] == 0:
                    self.player.lit_match['status'] = False
                    display('Your match has gone out.', before=0, after=1)

    def intro(self, prompt):
        print('')
        print('~' * TEXT_WIDTH)
        print(self.game_map['opening']['title'].center(TEXT_WIDTH, ' '))
        print('~' * TEXT_WIDTH)

        for text in self.game_map['opening']['intro'][:4]:
            display(text)
        display('', before=0, after=0)

        while True:
            name = input(prompt).strip()

            if name == '':
                display('You need to provide a name!', before=0, after=1)

            elif len(name) > self.text_width - len(prompt):
                display('Nobody\'s name is that long.', before=0, after=1)

            else:
                break

        self.player.set_name(name)
        display(self.game_map['opening']['intro'][4].format(name=self.player.name))

        for text in self.game_map['opening']['intro'][5:]:
            display(text)

        display(self.player.room.init_desc, after=1)
        self.player.room.first_visit = 0

    def ending_sequence(self):
        play_time = round((time() - self.start) + self.time)
        hours = play_time // 3600
        minutes = (play_time - hours * 3600) // 60
        seconds = play_time - hours * 3600 - minutes * 60

        if play_time <= 60 * 20:
            completion_message = self.game_map['message'][0]

        elif play_time <= 60 * 45:
            completion_message = self.game_map['message'][1]

        else:
            completion_message = self.game_map['message'][2]

        display(self.game_map['ending'].format(name=self.player.name), before=0)
        display('Congratulations! You win!')
        display('Play time: {}h : {}m : {}s'.format(hours, minutes, seconds))
        display(completion_message, before=0)
        display('Thanks for playing!')
        self.roll_credits()
        input("Press Enter to quit...")

    def roll_credits(self):
        credits_dict = self.game_map['credits']

        for role, names in credits_dict.items():
            display(role.ljust(20) + names[0])

            if names[1:]:
                display('\n'.join([(' ' * 20) + name for name in names[1:]]), before=0)

        display('', before=0)

    def choose_mode(self):

        if self.checkpoints['vines'] and not self.checkpoints['escape']:
            return 'escape'

        elif self.player.room.enemies_active():
            return 'combat'

        else:
            return 'normal'

    def text_constructor(self, resp):
        return resp.text_constructor().format(name=self.player.name)

    def generate_command(self, user_input, mode):
        room_commands = self.player.room.commands
        item_commands = {regex: constructor
                         for item in self.player.inventory.values()
                         for regex, constructor in item.commands.items()}
        command_lists = [room_commands, item_commands, self.generic_commands]
        command = InvalidCommand(self)

        if mode == 'combat':
            combat_commands = {reg: constr
                               for item in self.player.inventory.values()
                               for reg, constr in item.combat_commands.items()}
            combat_commands.update({
                go_regex: GoCommand,
                '(dodge|evade|avoid)(( +the)? +attack)?': EvadeCommand,
                '(attack|hit|strike|stab|kill)( +.*)?': AttackCommand,
                '((example +)?commands?|hints?|examples?)': CommandsCommand,
                'save( *file| +to +file| +((the|my) +)?game| +(my +)?progress)?': SaveCommand})

            if self.player.room_name == 'mouc2':
                combat_commands.update(
                    {'(get|jump|move|leap) +out +of +(the +)?way': EvadeCommand,
                     '(dodge|evade|avoid)(( +the)? +hammer)?': EvadeCommand,
                     '(dodge|evade|avoid) +it': EvadeCommand,
                     '(jump|move|leap) +aside': EvadeCommand,
                     'climb +(?:(up|down) +)?(?:the +)?(?:hill|incline|slope|mountain)': ClimbHill,
                     'go +(up|down) +(?:the +)?(?:hill|incline|slope|mountain)': ClimbHill,
                     '(?:(?:go|climb) +)?(up|down)hill': ClimbHill,
                     '(?:(?:go|climb) +)?(north|south|east|west|up|down)': ClimbHill,
                     'climb': ClimbHill
                     })
            command = match_command(self, user_input, combat_commands)

            if not isinstance(command, InvalidCommand):
                return command

        for command_list in command_lists:
            command = match_command(self, user_input, command_list)

            if not isinstance(command, InvalidCommand):

                if mode == 'combat':
                    return TakeHitCommand(self, command.match)

                elif mode == 'escape' and not (isinstance(command, GoCommand) or
                                               isinstance(command, CommandsCommand) or
                                               isinstance(command, SaveCommand)):
                    return DeadByVinesCommand(self, command.match)

                else:
                    return command

        return command

    def restore(self, lives):

        for key in self.__dict__:

            if key not in ['snapshot', 'filename']:
                self.__dict__[key] = self.snapshot.__dict__[key]
        self.old_checkpoints = None
        self.player.lives = lives

    @staticmethod
    def default(obj):

        if isinstance(obj, type) and obj.__dict__['__module__'] == 'commands':
            return obj.__name__

        return obj.__dict__

    def save(self):
        now = time()
        self.time = (now - self.start) + self.time
        self.start = now
        game = deepcopy(self)
        game.game_map = None

        for enemy in game.enemies.values():
            enemy.items = None

        for room in game.rooms.values():
            room.items = None
            tmp_enemies = []

            for enemy in room.enemies:
                tmp_enemies.append(enemy)

            room.enemies = tmp_enemies

        game.player.game_map = None
        game.player.checkpoints = None
        game.player.items = None
        game.player.room = None
        game.player.rooms = None
        tmp_inventory = []

        for item in game.player.inventory:
            tmp_inventory.append(item)

        game.player.inventory = tmp_inventory
        game.snapshot = None

        with open('{}.vista'.format(self.filename), 'wb') as f:
            plain_text = bytes(dumps(game, default=self.default), 'UTF-8')
            cipher_text = self.cipher_suite.encrypt(plain_text)
            f.write(cipher_text)

    def load(self, filename):

        with open('{}.vista'.format(filename), 'rb') as f:
            cipher_text = f.read()

            try:
                plain_text = self.cipher_suite.decrypt(cipher_text)

            except (InvalidToken, InvalidSignature):
                return 0

            savefile = loads(plain_text.decode(encoding='UTF-8'))

        self.start = time()
        self.time = savefile['time']
        self.filename = filename
        self.old_checkpoints = savefile['old_checkpoints']
        self.output = savefile['output']
        self.last_checkpoint = None

        for key in self.checkpoints:
            self.checkpoints[key] = savefile['checkpoints'][key]

        for key, item in self.items.items():

            for attr in ['taken', 'visible']:
                item.__setattr__(attr, savefile['items'][key][attr])

        for key, enemy in self.enemies.items():

            for attr in ['health', 'alive', 'active', 'charge', 'inventory']:
                enemy.__setattr__(attr, savefile['enemies'][key][attr])

        for key, room in self.rooms.items():

            for attr in ['init_core', 'short_core', 'long_core', 'init_desc', 'short_desc',
                         'long_desc', 'first_visit', 'room_blocks', 'enemy_blocks', 'blocks', 'item_aliases']:
                room.__setattr__(attr, savefile['rooms'][key][attr])

            room.inventory = OrderedDict([(item, self.items[item]) for item in savefile['rooms'][key]['inventory']])
            room.state = OrderedDict([(var, savefile['rooms'][key]['state'][var]) for var in room.state_order])

        for attr in ['name', 'coords', 'health', 'dead', 'lives', 'mode', 'item_aliases', 'boots', 'lit_match']:
            self.player.__setattr__(attr, savefile['player'][attr])

        self.player.update_room()
        self.player.inventory = {item: self.items[item] for item in self.player.item_aliases}

        self.snapshot = None
        self.snapshot = deepcopy(self)

        return 1
