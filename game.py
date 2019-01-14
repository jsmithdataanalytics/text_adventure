from helpers import *
# from json import dumps

command = InvalidCommand()

if __name__ == '__main__':
    game = Game()
    game.intro()
    shortcut = game_map['command_history'] if 'command_history' in game_map else []
    command_history = []

    while game.complete is False and game.over is False:
        # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
        game.player.mode = game.choose_mode()
        user_input = shortcut.pop(0) if shortcut else input().strip().lower()
        command_history.append(user_input)

        # if the user entered no text, and the previous command was
        # a valid one, interpret this as "repeat last command"
        if user_input == '' and command.match is not None:
            user_input = command.match.string

        elif user_input == 'quit':
            game.over = True
            command_history.pop()
            break

        command = game.generate_command(user_input, game.player.mode)
        command.parse()
        response = command.execute()
        game.output = game.text_constructor(response)
        display(game.output, before=0, after=1)
        game.updates(command)

    if game.over:
        display('Thy game is over.')
        # print(dumps(command_history))

    elif game.complete:
        display(game_map['ending'].format(name=game.player.name), before=0, after=1)
        display('Congratulations! You win!', before=0)
        display('Thanks for playing!\nJames Smith, Creator')
