from helpers import *

command = InvalidCommand()

if __name__ == '__main__':
    game = Game()
    game.intro()

    while game.complete is False and game.over is False:
        # commands are interpreted differently depending on whether mode is "combat", "escape" or "normal"
        game.player.mode = game.choose_mode()
        user_input = input().strip().lower()

        # if the user entered no text, and the previous command was
        # a valid one, interpret this as "repeat last command"
        if user_input == '' and command.match is not None:
            user_input = command.match.string

        command = game.generate_command(user_input, game.player.mode)
        command.parse()
        response = command.execute()
        text_output = game.text_constructor(response)
        display(text_output, before=0, after=1)
        game.updates()

    if game.over:
        display('Thy game is over.')

    elif game.complete:
        display('Congratulations! You win!', before=0)
        display('Created by James Smith.')
