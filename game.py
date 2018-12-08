from helpers import *

game_complete = False
player_dead = False
command = InvalidCommand()


if __name__ == '__main__':

    intro()

    while game_complete is False and player_dead is False:
        player.mode = 'combat' if player.room.enemies_active() else 'normal'
        user_input = input().strip().lower()

        # if the user entered no text, and the previous command was
        # a valid one, interpret this as "repeat last command"
        if user_input == '' and command.match is not None:
            user_input = command.match.string

        command = generate_command(user_input, player.mode)

        command.parse()
        response = command.execute()

        if player.room_name == 'dingl':
            game_complete = True

        if player.health <= 0:
            player_dead = True

        text_output = text_constructor(response)
        display(text_output, before=0, after=1)

    if player_dead:
        display('You have died.', before=0)
        display('Thy game is over.')

    elif game_complete:
        display('Congratulations! You win!', before=0)
        display('Created by James Smith.')
