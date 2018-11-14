from commands import *
import re


game_complete = False
player_dead = False


def text_constructor(resp):

    if player_dead is True:
        return 'You have died.'

    elif game_complete is True:
        return 'Congratulations! You win!'

    else:
        return resp.text_constructor()


print(player.room.text['desc'])

while game_complete is False and player_dead is False:
    user_input = input().strip().lower()
    match = None
    command = InvalidCommand()

    for regex in player.room.commands:
        match = re.fullmatch(regex, user_input)

        if match:
            command = player.room.commands[regex](match)
            break

    if match is None:

        for regex in command_constructors:
            match = re.fullmatch(regex, user_input)

            if match:
                command = command_constructors[regex](match)
                break

    command.parse()
    response = command.execute()

    if player.room_name == 'crater' and 'sword' in player.inventory:
        game_complete = True

    if player.dead is True:
        player_dead = True

    text_output = text_constructor(response)
    print(text_output)

if player_dead:
    print('Thy game is over.')
elif game_complete:
    print('Created by James Smith.')
