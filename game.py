from commands import *
import re
from textwrap import fill

TEXT_WIDTH = 80

game_complete = False
player_dead = False


def text_constructor(resp):

    if player_dead is True:
        return 'You have died.'

    elif game_complete is True:
        return 'Congratulations! You win!'

    else:
        return resp.text_constructor()


def match_command(text, command_list):

    for reg_ex in command_list:
        result = re.fullmatch(reg_ex, text)

        if result:
            return command_list[reg_ex](result), result
    return InvalidCommand(), None


def display(paras, text_width=TEXT_WIDTH, before=1, after=0, between=2):
    if isinstance(paras, str):
        paras = [paras]
    text = ('\n' * between).join([fill(para, text_width) for para in paras])
    print('\n' * before + text + '\n' * after)


print('\n' + '~' * TEXT_WIDTH + '\n' + game_map['opening']['title'].center(TEXT_WIDTH, ' ') + '\n' + '~' * TEXT_WIDTH)
display(game_map['opening']['intro'][:4])
player.set_name(input().strip())
display(game_map['opening']['intro'][4].format(player.name))
display(game_map['opening']['intro'][5:])
display(player.room.text['desc'])
command = InvalidCommand()


while game_complete is False and player_dead is False:
    user_input = input().strip().lower()

    if user_input == '' and command.match is not None:
        user_input = command.match.string

    command, match = match_command(user_input, player.room.commands)

    for item in player.inventory.values():

        if not match:
            command, match = match_command(user_input, item.commands)

        else:
            break

    if not match:
        command, match = match_command(user_input, generic_commands)

    command.parse()
    response = command.execute()

    if 'diamond' in player.inventory:
        game_complete = True

    if player.dead is True:
        player_dead = True

    text_output = text_constructor(response)
    display(text_output, between=1)

if player_dead:
    display('Thy game is over.')
elif game_complete:
    display('Created by James Smith.')
