from commands import *
import re
from textwrap import fill

TEXT_WIDTH = 80

game_complete = False
player_dead = False


def display(string, text_width=TEXT_WIDTH, before=1, after=0):
    paras = string.split('\n')
    string = '\n'.join([fill(para, text_width, replace_whitespace=False)
                        for para in paras])
    print('\n' * before + string + '\n' * after)


def intro():
    print('')
    print('~' * TEXT_WIDTH)
    print(game_map['opening']['title'].center(TEXT_WIDTH, ' '))
    print('~' * TEXT_WIDTH)

    for text in game_map['opening']['intro'][:5]:
        display(text)

    player.set_name(input().strip())
    display(game_map['opening']['intro'][4].format(name=player.name))

    for text in game_map['opening']['intro'][5:]:
        display(text)

    display(player.room.init_desc, after=1)
    player.room.first_visit = 0


def text_constructor(resp):
    return resp.text_constructor().format(name=player.name)


def match_command(string, command_list):

    for reg_ex in command_list:
        result = re.fullmatch(reg_ex, string)

        if result:
            return command_list[reg_ex](result)
    return InvalidCommand()


def generate_command(user_input, mode):
    room_commands = player.room.commands
    item_commands = {regex: constructor
                     for item in player.inventory.values()
                     for regex, constructor in item.commands.items()}
    command_lists = [room_commands, item_commands, generic_commands]
    command = InvalidCommand()

    if mode == 'combat':
        combat_commands = {reg: constr
                           for item in player.inventory.values()
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


def updates():
    player.room.update_blocks()
    player.room.update_item_aliases()
    player.update_item_aliases()


def choose_mode():

    if player.checkpoints['vines'] and not player.checkpoints['escape']:
        return 'escape'

    elif player.room.enemies_active():
        return 'combat'

    else:
        return 'normal'
