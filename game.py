#!/usr/bin/env python

"""game.py: Initialises and runs the game."""

__author__ = "James Smith"

# from json import dumps
from items import *
from enemies import *
from rooms import *
from avatar import *
from helpers import *


def load_game(prompt):
    game_map = load_map()
    checkpoints = initialise_checkpoints()
    items = initialise_items(game_map)
    enemies = initialise_enemies(game_map, items)
    rooms = initialise_rooms(game_map, items, enemies)
    player = initialise_player(game_map, checkpoints, items, rooms)
    generic_commands = initialise_commands(items, rooms)
    _game = Game(TEXT_WIDTH, game_map, checkpoints, items, enemies, rooms, player, generic_commands)
    _game.intro(prompt)
    return _game, InvalidCommand(_game)


def initialise_game(prompt):
    print('\nLoading game...')
    return load_game(prompt)


def reinitialise_game(prompt):
    print('\nRestarting game...')
    return load_game(prompt)


def play_turn(_game, _command, text_input):
    # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
    _game.player.mode = _game.choose_mode()
    text_input = text_input.strip().lower()

    # if the user entered no text, and the previous command was
    # a valid one, interpret this as "repeat last command"
    if text_input == '' and _command.match is not None:
        text_input = _command.match.string

    _command = _game.generate_command(text_input, _game.player.mode)
    _command.parse()
    response = _command.execute()
    _game.output = _game.text_constructor(response)
    display(_game.output, before=0, after=1)
    _game.updates(_command)

    if _game.over:
        display('You are out of lives. Thy game is over.')

    elif _game.complete:
        display(_game.game_map['ending'].format(name=_game.player.name), before=0, after=1)
        display('Congratulations! You win!', before=0)
        display('Thanks for playing!\nJames Smith, Creator')

    return _game, _command


if __name__ == '__main__':
    game, command = initialise_game('Enter your name: ')

    while not game.complete and not game.quit:
        raw_input = input('>> ')
        game_input = raw_input.strip().lower()

        if game_input == 'quit':
            game.quit = True
            display('Quitting game...', before=0)
            continue

        game, command = play_turn(game, command, game_input)

        if game.over:
            game, command = reinitialise_game('Enter your name: ')

    # shortcut = game.game_map['command_history'] if 'command_history' in game.game_map else []
    # command_history = []
    #
    # while game.complete is False:
    #     # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
    #     game.player.mode = game.choose_mode()
    #     user_input = shortcut.pop(0) if shortcut else input().strip().lower()
    #     command_history.append(user_input)
    #
    #     # if the user entered no text, and the previous command was
    #     # a valid one, interpret this as "repeat last command"
    #     if user_input == '' and command.match is not None:
    #         user_input = command.match.string
    #
    #     elif user_input == 'quit':
    #         game.quit = True
    #         command_history.pop()
    #         break
    #
    #     command = game.generate_command(user_input, game.player.mode)
    #     command.parse()
    #     response = command.execute()
    #     game.output = game.text_constructor(response)
    #     display(game.output, before=0, after=1)
    #     game.updates(command)
    #
    #     if game.over:
    #         display('You are out of lives. Thy game is over.')
    #         game, command = reinitialise_game()
    #
    # if game.quit:
    #     display('Quitting game...', before=0)
    #     print(dumps(command_history))
    #
    # elif game.complete:
    #     display(game.game_map['ending'].format(name=game.player.name), before=0, after=1)
    #     display('Congratulations! You win!', before=0)
    #     display('Thanks for playing!\nJames Smith, Creator')
