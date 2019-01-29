#!/usr/bin/env python

"""helpers.py: Definition of Game class and general helper functions."""

__author__ = "James Smith"

from commands import *
from re import fullmatch
from textwrap import fill
from copy import deepcopy
from random import randint

TEXT_WIDTH = 4 * 20


class Game:

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

    def updates(self, command):
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
                    text = 'You are in the Potion Master\'s apothecary, and have just given her the Dingleflowers.\n\n'
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
            snapshot = deepcopy(self)
            self.snapshot = snapshot

        if self.enemies['mouc2giant'].active:

            if not isinstance(command, InvalidCommand) and not isinstance(command, CommandsCommand):
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

            if name != '':
                break
            display('You need to provide a name!', before=0, after=1)

        self.player.set_name(name)
        display(self.game_map['opening']['intro'][4].format(name=self.player.name))

        for text in self.game_map['opening']['intro'][5:]:
            display(text)

        display(self.player.room.init_desc, after=1)
        self.player.room.first_visit = 0

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
                '((example +)?commands?|hints?|examples?)': CommandsCommand})

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

                elif mode == 'escape' and not (isinstance(command, GoCommand) or isinstance(command, CommandsCommand)):
                    return DeadByVinesCommand(self, command.match)

                else:
                    return command

        return command

    def restore(self, lives):

        for key in self.__dict__:

            if key != 'snapshot':
                self.__dict__[key] = self.snapshot.__dict__[key]
        self.old_checkpoints = None
        self.player.lives = lives


def display(string, text_width=TEXT_WIDTH, before=1, after=0):
    paras = string.split('\n')
    string = '\n'.join([fill(para, text_width, replace_whitespace=False)
                        for para in paras])
    print('\n' * before + string + '\n' * after)


def match_command(game, string, command_list):
    for reg_ex in command_list:
        result = fullmatch(reg_ex, string)

        if result:
            return command_list[reg_ex](game=game, match=result)
    return InvalidCommand(game)
