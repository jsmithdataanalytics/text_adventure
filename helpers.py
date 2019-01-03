from commands import *
import re
from textwrap import fill

TEXT_WIDTH = 80


class Game:

    def __init__(self):
        self.complete = False
        self.over = False
        self.player = player
        self.rooms = rooms
        self.enemies = enemies
        self.items = items
        self.checkpoints = checkpoints

    def updates(self):
        self.player.room.update_blocks()
        self.player.room.update_item_aliases()
        self.player.update_item_aliases()

        if self.player.room_name == 'mount':
            self.complete = True

        if self.player.health <= 0:
            self.player.lives -= 1
            display('You have died.', before=0)

            if self.player.lives > 0:
                display('Reverting to last checkpoint...', after=1)
                self.player.health = 120
                self.player.dead = False
                display(self.text_constructor(LookResponse()), before=0, after=1)

            else:
                self.over = True

    def intro(self):
        print('')
        print('~' * TEXT_WIDTH)
        print(game_map['opening']['title'].center(TEXT_WIDTH, ' '))
        print('~' * TEXT_WIDTH)

        for text in game_map['opening']['intro'][:5]:
            display(text)

        self.player.set_name(input().strip())
        display(game_map['opening']['intro'][4].format(name=self.player.name))

        for text in game_map['opening']['intro'][5:]:
            display(text)

        display(self.player.room.init_desc, after=1)
        self.player.room.first_visit = 0

    def choose_mode(self):

        if self.player.checkpoints['vines'] and not self.player.checkpoints['escape']:
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
        command_lists = [room_commands, item_commands, generic_commands]
        command = InvalidCommand()

        if mode == 'combat':
            combat_commands = {reg: constr
                               for item in self.player.inventory.values()
                               for reg, constr in item.combat_commands.items()}
            combat_commands.update(
                {'(?:go +)?(north|south|east|west|up|down|upstairs|downstairs|in|out|inside|outside)': GoCommand}
            )
            command = match_command(user_input, combat_commands)

            if not isinstance(command, InvalidCommand):
                return command

        for command_list in command_lists:
            command = match_command(user_input, command_list)

            if not isinstance(command, InvalidCommand):

                if mode == 'combat':
                    return TakeHitCommand(command.match)

                elif mode == 'escape' and not isinstance(command, GoCommand):
                    return DeadByVinesCommand(command.match)

                else:
                    return command

        return command


def display(string, text_width=TEXT_WIDTH, before=1, after=0):
    paras = string.split('\n')
    string = '\n'.join([fill(para, text_width, replace_whitespace=False)
                        for para in paras])
    print('\n' * before + string + '\n' * after)


def match_command(string, command_list):

    for reg_ex in command_list:
        result = re.fullmatch(reg_ex, string)

        if result:
            return command_list[reg_ex](result)
    return InvalidCommand()
