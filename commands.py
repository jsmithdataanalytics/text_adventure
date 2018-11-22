from responses import *


class Command:

    def __init__(self, match=None):
        self.match = match

        if match:
            self.text = match.string
            self.words = self.text.split()
            self.verb = self.words[0]
            self.parsed = {}

    def parse(self):
        pass

    def execute(self):
        return InvalidResponse('invalid', 'failure')


class InvalidCommand(Command):

    def execute(self):
        return InvalidResponse('invalid', 'failure')


class GoCommand(Command):

    def parse(self):
        group = self.match.group(1).strip()
        direction = group.replace('stairs', '').replace('side', '')

        if group in ['north', 'south', 'east', 'west', 'up', 'down']:
            self.parsed['direction'] = group

        elif group in ['upstairs', 'downstairs']:

            if 'extra_directions' in player.room.state and group in player.room.state['extra_directions']:
                self.parsed['direction'] = direction

            else:
                self.parsed['direction'] = 'no_stairs'

        elif direction in ['in', 'out']:

            if 'extra_directions' in player.room.state and direction in player.room.state['extra_directions']:
                self.parsed['direction'] = direction

            else:
                self.parsed['direction'] = 'no_inout'

        else:
            self.parsed['direction'] = 'invalid'

    def execute(self):
        result, direction = player.go(self.parsed['direction'])
        if result == 'invalid_command':
            return GoResponse('invalid', 'failure')
        elif result == 'invalid_movement':
            return GoResponse('valid', 'failure', direction=direction)
        elif result == 'no_stairs':
            return Response(text='There aren\'t any stairs here.')
        elif result == 'no_inout':
            return Response(text='You can\'t go that way.')
        elif result == 'new_room':
            return GoResponse('valid', 'success', direction=direction)


class WaitCommand(Command):

    def parse(self):
        if len(self.words) != 1:
            self.parsed = {'validity': 'invalid',
                           'outcome': 'failure'}
        else:
            self.parsed = {'validity': 'valid',
                           'outcome': 'success'}

    def execute(self):
        return WaitResponse(**self.parsed)


class LookCommand(Command):

    def parse(self):
        if self.text == 'look' or self.text == 'look around':
            self.parsed = {'validity': 'valid',
                           'outcome': 'success'}

        else:
            self.parsed = {'validity': 'invalid',
                           'outcome': 'failure'}

    def execute(self):
        return LookResponse(**self.parsed)


class InventoryCommand(Command):

    def parse(self):
        self.parsed = {'validity': 'valid',
                       'outcome': 'success'}

    def execute(self):
        return InventoryResponse(**self.parsed)


class GetCommand(Command):

    def parse(self):
        item = self.match.group(1).strip()

        if item in player.room.inventory and items[item].visible:
            self.parsed['validity'] = 'valid'
            self.parsed['item'] = item
        elif item == 'all':
            self.parsed['validity'] = 'valid'
            self.parsed['item'] = 'all'
        else:
            self.parsed = {'validity': 'invalid'}

    def execute(self):
        if self.parsed['validity'] == 'valid':
            if self.parsed['item'] == 'all':
                n_visible = player.room.count_visible_items()

                if n_visible == 0:
                    return GetResponse('valid', 'failure', method='all')
                else:
                    item_list = player.get_all_visible_items()
                    return GetResponse('valid', 'success', new_items=item_list, method='all')
            else:
                player.get_items(new_items={self.parsed['item']: player.room.inventory[self.parsed['item']]})
                return GetResponse('valid', 'success', new_items=[self.parsed['item']], method='specific')
        else:
            return GetResponse('invalid', 'failure', method='specific')


class DropCommand(Command):

    def execute(self):
        item = self.match.group(1).strip()

        if item in player.inventory:
            player.drop_items([item])
            return Response(text='Dropped.')

        elif item == 'all':
            to_return = Response(text='\n'.join([item.name + ': dropped.' for item in player.inventory.values()]))
            player.drop_items(list(player.inventory.keys()))
            return to_return

        else:
            return Response(text='You don\'t have one of those.')


class DigCommand(Command):

    def execute(self):

        if player.room.name == 'vilb1':

            if 'shovel' in player.inventory:
                if player.room.state['dug']:
                    return Response(text=player.room.text['responses']['already_dug'])

                else:
                    player.room.state['dug'] = 1
                    items['diamond'].visible = 1
                    player.room.update_desc()
                    return Response(text=player.room.text['state']['dug']['1'] + ' ' + items['diamond'].init_desc)

            else:
                return Response(text='You have nothing to dig with.')

        else:
            return Response(text='You can\'t dig here.')


class OpenChestHomeCommand(Command):

    def execute(self):

        if player.room.state['locked'] == 1:
            return Response(text=player.room.text['responses']['locked'])

        elif player.room.state['opened'] == 1:
            return Response(text=player.room.text['responses']['already_opened'])

        else:
            player.room.state['opened'] = 1
            items['shield'].visible = 1
            player.room.update_desc()
            return Response(text='Done. ' + items['shield'].init_desc)


class UnlockChestHomeCommand(Command):

    def execute(self):

        if player.room.state['locked'] == 0:
            return Response(text=player.room.text['responses']['already_unlocked'])

        elif 'key' not in player.inventory:
            return Response(text=player.room.text['responses']['no_key'])

        else:
            player.room.state['locked'] = 0
            player.room.update_desc()
            return Response(text=player.room.text['responses']['unlocked'])


generic_commands = {
    '(?:go +)?(north|south|east|west|up|down|upstairs|downstairs|in|out|inside|outside)': GoCommand,
    'wait': WaitCommand,
    'look(?: +around)?': LookCommand,
    '(?:(?:check|inspect|examine) +)?(?:items|inventory)': InventoryCommand,
    '(?:get|take) +(.+)': GetCommand,
    '(?:drop|put +down) +(.+)': DropCommand,
    'dig': DigCommand
}

rooms['vilb1'].commands.update(
    {
        'dig': DigCommand
    }
)

rooms['home1'].commands.update(
    {
        'open(?: +chest)?': OpenChestHomeCommand,
        'unlock(?: +chest)?': UnlockChestHomeCommand
    }
)

items['shovel'].commands.update(
    {
        'dig': DigCommand
    }
)
