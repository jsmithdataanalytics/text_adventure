#!/usr/bin/env python

"""main.py: Initialises and runs the game."""

__author__ = "James Smith"

import os
from avatar import *
from enemies import *
from game import *
from items import *
from map import *
from rooms import *


def load_game(prompt, filename=None):
    checkpoints = initialise_checkpoints()
    items = initialise_items(game_map)
    enemies = initialise_enemies(game_map, items)
    rooms = initialise_rooms(game_map, items, enemies)
    player = initialise_player(game_map, checkpoints, items, rooms)
    generic_commands = initialise_commands(items, rooms)
    _game = Game(TEXT_WIDTH, game_map, checkpoints, items, enemies, rooms, player, generic_commands)

    if filename:
        _game.load(filename)
        display(_game.player.describe_current_room('long').format(name=_game.player.name), after=1)

    else:
        _game.intro(prompt)

    return _game, InvalidCommand(_game)


def initialise_game(prompt):

    to_load = None
    savefiles = [filename[:-6] for filename in os.listdir('.') if filename[-6:] == '.vista']

    if savefiles:
        options = ['"{}"'.format(filename) for filename in savefiles]
        display('\n'.join(['Available save files:'] + options), before=1, after=1)

        while True:
            to_load = input('Specify a save file to load, or hit Enter to start from the beginning: ').lower()

            if to_load in savefiles or not to_load:
                break

            else:
                display('That\'s not one of the options.', before=0, after=1)

    print('\nLoading game...')
    return load_game(prompt, to_load)


def reinitialise_game(prompt, filename):
    print('\nRestarting game...')
    _game, _command = load_game(prompt)
    _game.filename = filename
    return _game, _command


def play_turn(_game, _command, text_input):
    # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
    _game.player.mode = _game.choose_mode()
    text_input = text_input.strip().lower()

    # if the user entered no text, and the previous command was a valid one, interpret this as "repeat last command"
    if text_input == '' and _command.match is not None:
        text_input = _command.match.string

    _command = _game.generate_command(text_input, _game.player.mode)
    _command.parse()
    response = _command.execute()
    _game.output = _game.text_constructor(response)
    display(_game.output, before=0, after=1)
    _game.updates(_command, response)

    if _game.over:
        display('You are out of lives. Thy game is over.')

    elif _game.complete:
        _game.ending_sequence()

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
            game, command = reinitialise_game('Enter your name: ', game.filename)
