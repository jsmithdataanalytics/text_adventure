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
        escape_direction = {'wood1': 'south',
                            'wood2': 'south',
                            'wood3': 'south',
                            'wood4': 'east',
                            'wood5': 'east',
                            'wood6': 'north',
                            'wood7': 'north',
                            'wood8': 'east',
                            'wood9': 'east',
                            'dingl': 'east'}
        right_way = self.parsed['direction'] == escape_direction[player.room_name] if player.mode == 'escape' else True
        result, direction = player.go(self.parsed['direction'])

        if player.mode == 'escape' and result != 'invalid_command':

            if not right_way:
                player.health = 0

                if player.room_name in ['deade', 'dead2']:
                    return Response(text='This is a dead-end. With nowhere to run, you\'re powerless to resist as the '
                                         'vines seize you and crush you!')

                else:
                    return Response(text='Wrong way! You\'ve run straight into the '
                                         'vines, which promptly seize you and crush you!')

        if player.mode == 'combat' and result not in ['new_room', 'invalid_command']:
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

            if player.room_name == 'vila2' and player.mode == 'escape':
                checkpoints['escape'] = True
                return Response(text='You have escaped into the northeast part of the village. The vines have '
                                'retreated, and the forest has returned to its usual, peaceful state. The Potion '
                                'Master\'s apothecary is here.')
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

    def execute(self):
        return LookResponse()


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

            for key, value in player.room.item_aliases.items():

                for alias in value:

                    if item == alias:
                        self.parsed['validity'] = 'valid'
                        self.parsed['item'] = key
                        break

    def execute(self):
        if self.parsed['validity'] == 'valid':
            if self.parsed['item'] == 'all':
                n_visible = player.room.count_visible_items()

                if n_visible == 0:
                    return GetResponse('valid', 'failure', method='all')
                else:
                    got = player.get_all_visible_items()
                    return GetResponse('valid', 'success', new_items=got, method='all')
            else:
                got = player.get_items(new_items={self.parsed['item']: player.room.inventory[self.parsed['item']]})
                return GetResponse('valid', 'success', new_items=got, method='specific')
        else:
            return GetResponse('invalid', 'failure', method='specific')


class DropCommand(Command):

    def parse(self):
        item = self.match.group(1).strip()

        if item in player.inventory:
            self.parsed['item'] = item

        elif item == 'all':
            self.parsed['item'] = 'all'

        else:
            self.parsed['item'] = None

            for key, value in player.item_aliases.items():

                for alias in value:

                    if item == alias:
                        self.parsed['item'] = key
                        break

    def execute(self):
        item = self.parsed['item']

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
            items['ruby'].visible = 1
            player.room.update_desc()
            return Response(text='The chest is open. ' + items['ruby'].init_desc)


class UnlockChestHomeCommand(Command):

    def execute(self):

        if player.room.state['locked'] == 0:
            return Response(text=player.room.text['responses']['already_unlocked'])

        elif 'key' not in player.inventory:
            return Response(text=player.room.text['responses']['no_key'])

        else:
            player.room.state['locked'] = 0
            c = OpenChestHomeCommand(self.match)
            c.parse()
            return c.execute()


class CutVinesCommand(Command):

    def execute(self):

        if player.room_name == 'vila2':

            if 'sword' in player.inventory:

                if checkpoints['apoth']:

                    if player.room.state['cut'] == 0:

                        player.room.room_blocks = []
                        player.room.state['cut'] = 1
                        return Response(text=player.room.text['responses']['cut_success'])

                    else:
                        return Response(text=player.room.text['responses']['already_cut'])

                elif checkpoints['jimbo']:
                    return Response(text='Hang on, you\'re supposed to be going to see the Potion Master!')

                else:
                    return Response(text='Hang on, you\'re supposed to be going to see Jimbo!')

            else:
                return Response(text=player.room.text['responses']['nothing_to_cut_with'])

        else:
            return InvalidResponse()


class ReadCommand(Command):

    def execute(self):
        verb = self.match[1]
        subject = re.sub('^the +', '', self.match[2].strip())

        if subject == '':
            return Response(text=verb.title() + ' what?')

        elif subject == 'book':
            return Response(text=items['book'].text['responses']['read'])

        else:
            return InvalidResponse()


class AttackCommand(Command):
    verb = None
    enemy = None
    weapon = None
    valid_weapons = ['sword']

    def parse(self):
        text = self.match.string
        self.verb = self.match[1]

        m = re.search(' +with( +.*)?$', text)

        if m:
            if m[1] and m[1].strip():
                self.weapon = re.sub('^the +', '', m[1].strip())
            text = re.sub(' +with( +.*)?$', '', text)
        remainder = re.sub('^attack *', '', text)

        if remainder:
            self.enemy = re.sub('^the +', '', remainder.strip())

    def execute(self):

        if self.verb != 'attack':
            return Response(text='The word you\'re looking for is "attack".')

        elif self.enemy is None:
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
        text = choice(weapon.combat_text[self.enemy][damage])
        more_text = enemy.lose_health(damage)
        return Response(text=text + more_text)


class TakeHitCommand(Command):

    def execute(self):
        active_enemies = [enemy for enemy in player.room.enemies.values() if enemy.active]
        text = []

        for enemy in active_enemies:
            damage = choice(enemy.damage_dist[0], p=enemy.damage_dist[1])
            text.append(choice(enemy.attack_text[damage]))
            player.health = max(player.health - damage, 0)
        return Response(text='Hardly appropriate for a combat situation!\n' + '\n'.join(text))


class ClimbTreeCommand(Command):

    def execute(self):
        direction = self.match[1].strip() if self.match[1] is not None else None

        if player.room_name == 'dead2':

            if direction == 'down':
                return InvalidResponse()

            else:
                match = re.fullmatch('go (up)', 'go up')
                c = GoCommand(match)
                c.parse()
                return c.execute()

        elif player.room_name == 'treeh':

            if direction == 'up':
                return InvalidResponse()

            else:
                match = re.fullmatch('go (down)', 'go down')
                c = GoCommand(match)
                c.parse()
                return c.execute()

        else:
            return Response(text='You can\'t climb here.')


class GiveCommand(DropCommand):

    def execute(self):
        item = self.parsed['item']

        if player.room_name == 'apoth':

            if item in player.inventory:

                if item == 'dingleflowers':
                    player.lose_items([item])
                    player.room.short_core = player.room.text['short_core2']
                    player.room.long_core = player.room.text['long_core2']
                    checkpoints['dingleflowers'] = True
                    rooms['vilb2'].room_blocks = []
                    return Response(text=player.room.text['responses']['dingleflowers'])

                else:
                    return Response(text='Potion Master: "Hm, not really what I was looking for. '
                                         'Perhaps you have something else for me?"')

            else:
                return Response(text='You don\'t have one of those.')

        else:
            return InvalidResponse()


class DeadByVinesCommand(Command):

    def execute(self):
        player.health = 0
        return Response(text='While you waste time doing something other than running away, '
                             'the vines seize you and crush you!')


generic_commands = {
    '(?:go +)?(north|south|east|west|up|down|upstairs|downstairs|in|out|inside|outside)': GoCommand,
    'wait': WaitCommand,
    'look(?: +a?round)?': LookCommand,
    '(?:(?:check|inspect|examine) +)?(?:items|inventory)': InventoryCommand,
    '(?:get|take|grab|pick +up) +(.+)': GetCommand,
    '(?:drop|leave|put +down) +(.+)': DropCommand,
    'put +(.+) +(?:down|on +floor|on +ground)': DropCommand,
    'dig(?: +(?:a +)?hole)?(?: +with +(?:the +)?(?:shovel|spade))?': DigCommand,
    'climb( +(?:up|down))?(?: +(?:the +)?tree)?': ClimbTreeCommand,
}

rooms['vilb1'].commands.update(
    {
        'dig(?: +(?:a +)?hole)?(?: +with +(?:the +)?(?:shovel|spade))?': DigCommand,
        'dig +up +(?:the +)?sword': DigCommand
    }
)

rooms['home1'].commands.update(
    {
        '(?:unlock|open)(?: +(?:the +)?chest(?: +with +(?:the +)?key)?)?': UnlockChestHomeCommand,
        'insert +(?:the +)?key(?: +into +(?:the +)?(?:chest|lock))?': UnlockChestHomeCommand
    }
)

rooms['vila2'].commands.update(
    {
        '(?:cut|slice|clear|sever)(?: +(?:the +)?(?:vines|thicket))?(?: +with +(?:the +)?(?:sword))?': CutVinesCommand
    }
)

rooms['apoth'].commands.update(
    {
        '(?:give|present|show|hand +over) +(.+)': GiveCommand
    }
)

items['shovel'].commands.update(
    {
        'dig(?: +(?:a +)?hole)?(?: +with +(?:the +)?(?:shovel|spade))?': DigCommand
    }
)

items['book'].commands.update(
    {
        '(read|examine|inspect|open)( +(?:the +)?book)': ReadCommand
    }
)

items['sword'].combat_commands.update(
    {
        '(attack|hit|stab)( +.*)?': AttackCommand,
        '(swing) +(?:the +)?sword.*': AttackCommand
    }
)
