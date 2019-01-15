#!/usr/bin/env python

"""game.py: Initialises and runs the game."""

__author__ = "James Smith"

# from json import dumps
from items import *
from enemies import *
from rooms import *
from avatar import *
from helpers import *


def load_game():
    game_map = load_map()
    checkpoints = initialise_checkpoints()
    items = initialise_items(game_map)
    enemies = initialise_enemies(game_map, items)
    rooms = initialise_rooms(game_map, items, enemies)
    player = initialise_player(game_map, checkpoints, items, rooms)
    generic_commands = initialise_commands(items, rooms)
    _game = Game(TEXT_WIDTH, game_map, checkpoints, items, enemies, rooms, player, generic_commands)
    _game.intro()
    return _game, InvalidCommand(_game)


def initialise_game():
    print('\nLoading game...')
    return load_game()


def reinitialise_game():
    print('\nRestarting game...')
    return load_game()


if __name__ == '__main__':
    game, command = initialise_game()
    shortcut = game.game_map['command_history'] if 'command_history' in game.game_map else []
    command_history = []

    while game.complete is False:
        # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
        game.player.mode = game.choose_mode()
        user_input = shortcut.pop(0) if shortcut else input().strip().lower()
        command_history.append(user_input)

        # if the user entered no text, and the previous command was
        # a valid one, interpret this as "repeat last command"
        if user_input == '' and command.match is not None:
            user_input = command.match.string

        elif user_input == 'quit':
            game.quit = True
            command_history.pop()
            break

        command = game.generate_command(user_input, game.player.mode)
        command.parse()
        response = command.execute()
        game.output = game.text_constructor(response)
        display(game.output, before=0, after=1)
        game.updates(command)

        if game.over:
            display('You are out of lives. Thy game is over.')
            game, command = reinitialise_game()

    if game.quit:
        display('Quitting game...', before=0)
        # print(dumps(command_history))

    elif game.complete:
        display(game.game_map['ending'].format(name=game.player.name), before=0, after=1)
        display('Congratulations! You win!', before=0)
        display('Thanks for playing!\nJames Smith, Creator')
