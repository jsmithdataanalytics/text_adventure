from responses import *
from numpy.random import choice
import re


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

        if player.mode == 'combat' and result != 'new_room':
            c = TakeHitCommand()
            c.parse()
            return c.execute()

        if result == 'invalid_command':
            return InvalidResponse()

        elif result == 'invalid_movement':
            return GoResponse('valid', 'failure', direction=direction)

        elif result == 'no_stairs':
            return Response(text='There aren\'t any stairs here.')

        elif result == 'no_inout':
            return Response(text='You can\'t go that way.')

        elif result == 'new_room':
            desc_type = 'init' if player.room.first_visit else 'short'
            player.room.first_visit = 0
            return GoResponse('valid', 'success', direction=direction, desc_type=desc_type)


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
                    items['sword'].visible = 1
                    player.room.update_desc()
                    return Response(text=player.room.text['state']['dug']['1'] + ' ' + items['sword'].init_desc)

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


class CutVinesCommand(Command):

    def execute(self):

        if player.room_name == 'vila2':

            if player.room.state['cut'] == 0:

                if 'sword' in player.inventory:
                    game_map['layout'][3][4][5] = 'wood1'
                    player.room.state['cut'] = 1
                    return Response(text=player.room.text['responses']['cut_success'])

                else:
                    return Response(text=player.room.text['responses']['nothing_to_cut_with'])

            else:
                return Response(text=player.room.text['responses']['already_cut'])

        else:
            return InvalidResponse()


class ReadCommand(Command):

    def execute(self):
        verb = self.match[1]
        subject = self.match[2].strip() if self.match[2] is not None else ''

        if subject == '':
            return Response(text=verb.title() + ' what?')

        elif subject == 'book':
            return Response(text=items['book'].text['responses']['read'])

        else:
            return InvalidResponse()


class AttackCommand(Command):
    enemy = None
    weapon = None

    valid_weapons = ['sword']

    def parse(self):
        text = self.match.string
        m = re.search(' +with( +.*)?$', text)

        if m:
            if m[1] and m[1].strip():
                self.weapon = m[1].strip()
            text = re.sub(' +with( +.*)?$', '', text)
        remainder = re.sub('^attack *', '', text)

        if remainder:
            self.enemy = remainder

    def execute(self):

        if self.enemy is None:
            return Response(text='Attack what?')

        elif self.enemy not in [enemy.type for enemy in player.room.enemies.values() if enemy.active]:
            return Response(text='There isn\'t one of those nearby.')

        elif self.weapon is None:
            return Response(text='Attack with what?')

        elif self.weapon not in player.inventory:
            return Response(text='You don\'t have one of those.')

        elif self.weapon not in self.valid_weapons:
            return Response(text='You can\'t attack with that.')

        elif self.weapon == 'sword':
            return self.sword_attack()

    def sword_attack(self):
        weapon = player.inventory[self.weapon]
        enemy = None

        for e in player.room.enemies.values():
            enemy = e

            if enemy.type == self.enemy and enemy.active:
                break
        damage = choice(weapon.damage_dist[0], p=weapon.damage_dist[1])
        text = choice(weapon.combat_text['goblin'][damage])
        more_text = enemy.lose_health(damage)
        return Response(text=text + '\n' + more_text)


class TakeHitCommand(Command):

    def execute(self):
        active_enemies = [enemy for enemy in player.room.enemies.values() if enemy.active]
        text = []

        for enemy in active_enemies:
            damage = choice(enemy.damage_dist[0], p=enemy.damage_dist[1])
            text.append(choice(enemy.attack_text[damage]))
            player.health -= damage
        return Response(text='Hardly appropriate for a combat situation!\n' + '\n'.join(text))


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

rooms['vila2'].commands.update(
    {
        'cut(?: +vines)?': CutVinesCommand
    }
)

items['shovel'].commands.update(
    {
        'dig': DigCommand
    }
)

items['book'].commands.update(
    {
        '(read|examine|inspect)( +.+)?': ReadCommand
    }
)

items['sword'].combat_commands.update(
    {
        'attack( +.*)?': AttackCommand,

    }
)
