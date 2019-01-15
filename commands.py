from responses import *
from numpy.random import choice
import re


class Command:

    def __init__(self, game, match=None):
        self.game = game
        self.match = match

        if match:
            self.text = match.string
            self.words = self.text.split()
            self.verb = self.words[0]
            self.parsed = {}

    def parse(self):
        pass

    def execute(self):
        return InvalidResponse(self.game, 'invalid', 'failure')


class InvalidCommand(Command):

    def execute(self):
        return InvalidResponse(self.game, 'invalid', 'failure')


class GoCommand(Command):

    def parse(self):
        group = self.match.group(1).strip()
        direction = group.replace('stairs', '').replace('side', '')

        if group in ['north', 'south', 'east', 'west', 'up', 'down']:
            self.parsed['direction'] = group

        elif group in ['upstairs', 'downstairs']:

            if 'extra_directions' in self.game.player.room.state and \
                    group in self.game.player.room.state['extra_directions']:
                self.parsed['direction'] = direction

            else:
                self.parsed['direction'] = 'no_stairs'

        elif direction in ['in', 'out']:

            if 'extra_directions' in self.game.player.room.state and \
                    direction in self.game.player.room.state['extra_directions']:
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

        right_way = self.parsed['direction'] == escape_direction[self.game.player.room_name] \
            if self.game.player.mode == 'escape' else True
        result, direction = self.game.player.go(self.parsed['direction'])

        if self.game.player.mode == 'escape' and result != 'invalid_command':

            if not right_way:
                self.game.player.health = 0

                if self.game.player.room_name in ['deade', 'dead2']:
                    return Response(self.game,
                                    text='This is a dead-end. With nowhere to run, you\'re powerless to resist as the '
                                         'vines seize you and crush you!')

                elif result != 'new_room':
                    return Response(self.game, text='Wrong way! While you waste time going the wrong way, the '
                                                    'vines seize you and crush you!')

                else:
                    return Response(self.game, text='Wrong way! You\'ve run straight into the '
                                                    'vines, which promptly seize you and crush you!')

        if self.game.player.mode == 'combat' and result not in ['new_room', 'invalid_command']:
            c = TakeHitCommand(self.game)
            c.parse()
            return c.execute()

        if result == 'invalid_command':
            return InvalidResponse(self.game, )

        elif result == 'no_boots':
            return Response(self.game, text='It\'s too steep. You need to be wearing snow boots to go that way.')

        elif result == 'invalid_movement':
            return GoResponse(self.game, 'valid', 'failure', direction=direction)

        elif result == 'no_stairs':
            return Response(self.game, text='There aren\'t any stairs here.')

        elif result == 'no_inout':
            return Response(self.game, text='You can\'t go that way.')

        elif result == 'new_room':
            desc_type = 'init' if self.game.player.room.first_visit else 'short'
            self.game.player.room.first_visit = 0

            if self.game.player.room_name == 'vila2' and self.game.player.mode == 'escape':
                self.game.checkpoints['escape'] = True
                return Response(self.game,
                                text='You have escaped into the northeast part of the village. The vines have '
                                     'retreated, and the forest has returned to its usual, peaceful state. The Potion '
                                     'Master\'s apothecary is here.')

            if self.game.player.room_name == 'homeg' and "dot" in self.game.player.inventory and \
                    self.game.checkpoints['easter'] is False:
                self.game.checkpoints['easter'] = True
                return Response(self.game,
                                text='Wow! You found the invisible dot and brought it home. You are a thorough and '
                                     'dedicated player of The Vista... thank you! As a reward, I\'ve granted you a '
                                     'special power. The dot can now be used as a weapon, with guaranteed one hit KOs!'
                                     '\n\nThanks again,\nJames Smith, Creator\n\n' +
                                     self.game.player.describe_current_room(desc_type))

            return GoResponse(self.game, 'valid', 'success', direction=direction, desc_type=desc_type)


class WaitCommand(Command):

    def parse(self):
        if len(self.words) != 1:
            self.parsed = {'validity': 'invalid',
                           'outcome': 'failure'}
        else:
            self.parsed = {'validity': 'valid',
                           'outcome': 'success'}

    def execute(self):
        return WaitResponse(self.game, **self.parsed)


class LookCommand(Command):

    def execute(self):
        return LookResponse(self.game)


class InventoryCommand(Command):

    def parse(self):
        self.parsed = {'validity': 'valid',
                       'outcome': 'success'}

    def execute(self):
        return InventoryResponse(self.game, **self.parsed)


class GetCommand(Command):

    def parse(self):
        item = self.match.group(1).strip()

        if item in self.game.player.room.inventory and self.game.items[item].visible:
            self.parsed['validity'] = 'valid'
            self.parsed['item'] = item

        elif item == 'all':
            self.parsed['validity'] = 'valid'
            self.parsed['item'] = 'all'

        else:
            self.parsed = {'validity': 'invalid'}

            for key, value in self.game.player.room.item_aliases.items():

                for alias in value:

                    if re.fullmatch(alias, item):
                        self.parsed['validity'] = 'valid'
                        self.parsed['item'] = key
                        return

    def execute(self):
        if self.parsed['validity'] == 'valid':
            if self.parsed['item'] == 'all':
                n_visible = self.game.player.room.count_visible_items()

                if n_visible == 0:
                    return GetResponse(self.game, 'valid', 'failure', method='all')
                else:
                    got = self.game.player.get_all_visible_items()
                    return GetResponse(self.game, 'valid', 'success', new_items=got, method='all')
            else:
                got = self.game.player.get_items(
                    new_items={self.parsed['item']: self.game.player.room.inventory[self.parsed['item']]})
                return GetResponse(self.game, 'valid', 'success', new_items=got, method='specific')
        else:
            return GetResponse(self.game, 'invalid', 'failure', method='specific')


class DropCommand(Command):

    def parse(self):
        item = self.match.group(1).strip()

        if item in self.game.player.inventory:
            self.parsed['item'] = item

        elif item == 'all':
            self.parsed['item'] = 'all'

        else:
            self.parsed['item'] = None

            for key, value in self.game.player.item_aliases.items():

                for alias in value:

                    if re.fullmatch(alias, item):
                        self.parsed['item'] = key
                        return

    def execute(self):
        boots_message = 'You can\'t drop the snow boots because you\'re wearing them!'
        item = self.parsed['item']

        if item == 'snow boots' and self.game.player.boots:
            return Response(self.game, text=boots_message)

        elif item in self.game.player.inventory:
            self.game.player.drop_items([item])
            return Response(self.game, text='Dropped.')

        elif item == 'all':

            if self.game.player.boots:
                text = [item.name + ': dropped.' for key, item in self.game.player.inventory.items()
                        if key != 'snow boots']
                text.append(boots_message)
                self.game.player.drop_items([key for key in self.game.player.inventory.keys() if key != 'snow boots'])
                return Response(self.game, text='\n'.join(text))

            elif not self.game.player.inventory:
                return Response(self.game, text='You have nothing to drop!')

            else:
                text = [item.name + ': dropped.' for key, item in self.game.player.inventory.items()]
                self.game.player.drop_items([key for key in self.game.player.inventory.keys()])
                return Response(self.game, text='\n'.join(text))

        else:
            return Response(self.game, text='You don\'t have one of those.')


class DigCommand(Command):

    def execute(self):

        if self.game.player.room.name == 'vilb1':

            if 'shovel' in self.game.player.inventory:
                if self.game.player.room.state['dug']:
                    return Response(self.game, text=self.game.player.room.text['responses']['already_dug'])

                else:
                    self.game.player.room.state['dug'] = 1
                    self.game.items['sword'].visible = 1
                    self.game.player.room.update_desc()
                    return Response(self.game,
                                    text=self.game.player.room.text['state']['dug']['1'] + ' ' + self.game.items[
                                        'sword'].init_desc)

            else:
                return Response(self.game, text='You have nothing to dig with.')

        else:
            return Response(self.game, text='You can\'t dig here.')


class OpenChestHomeCommand(Command):

    def execute(self):

        if self.game.player.room.state['locked'] == 1:
            return Response(self.game, text=self.game.player.room.text['responses']['locked'])

        elif self.game.player.room.state['opened'] == 1:
            return Response(self.game, text=self.game.player.room.text['responses']['already_opened'])

        else:
            self.game.player.room.state['opened'] = 1
            self.game.items['ruby'].visible = 1
            self.game.player.room.update_desc()
            return Response(self.game, text='The chest is open. ' + self.game.items['ruby'].init_desc)


class UnlockChestHomeCommand(Command):

    def execute(self):

        if self.game.player.room.state['locked'] == 0:
            return Response(self.game, text=self.game.player.room.text['responses']['already_unlocked'])

        elif 'key' not in self.game.player.inventory:
            return Response(self.game, text=self.game.player.room.text['responses']['no_key'])

        else:
            self.game.player.room.state['locked'] = 0
            c = OpenChestHomeCommand(self.game, self.match)
            c.parse()
            return c.execute()


class OpenChestHutCommand(Command):

    def execute(self):

        if self.game.player.room.state['frozen'] == 1:
            return Response(self.game, text='It\'s frozen shut.')

        else:
            self.game.player.room.state['open'] = 1
            self.game.items['snow boots'].visible = 1
            return Response(self.game, text=self.game.items['snow boots'].init_desc)


class CutVinesCommand(Command):

    def execute(self):

        if self.game.player.room_name == 'vila2':

            if 'sword' in self.game.player.inventory:

                if self.game.checkpoints['apoth']:

                    if self.game.player.room.state['cut'] == 0:

                        self.game.player.room.room_blocks = []
                        self.game.player.room.state['cut'] = 1
                        return Response(self.game, text=self.game.player.room.text['responses']['cut_success'])

                    else:
                        return Response(self.game, text=self.game.player.room.text['responses']['already_cut'])

                elif self.game.checkpoints['jimbo']:
                    return Response(self.game, text='Hang on, you\'re supposed to be going to see the Potion Master!')

                else:
                    return Response(self.game, text='Hang on, you\'re supposed to be going to see Jimbo!')

            else:
                return Response(self.game, text=self.game.player.room.text['responses']['nothing_to_cut_with'])

        else:
            return InvalidResponse(self.game)


class ReadCommand(Command):

    def execute(self):
        verb = self.match[1]
        subject = re.sub('^the +', '', self.match[2].strip())

        if subject == '':
            return Response(self.game, text=verb.title() + ' what?')

        elif subject == 'book':
            return Response(self.game, text=self.game.items['book'].text['responses']['read'])

        else:
            return InvalidResponse(self.game)


class AttackCommand(Command):
    verb = None
    enemy = None
    weapon = None
    valid_weapons = ['sword', 'axe']

    def parse(self):
        text = self.match.string
        self.verb = self.match[1]

        m = re.search(' +with( +.*)?$', text)

        if m:
            if m[1] and m[1].strip():
                self.weapon = m[1].strip()
            text = re.sub(' +with( +.*)?$', '', text)
        remainder = re.sub('^attack *', '', text)

        if remainder:
            self.enemy = re.sub('^the +', '', remainder.strip())

    def execute(self):

        if self.game.player.room_name == 'mouc2' and self.game.player.mode == 'combat' and self.game.enemies[
                'mouc2giant'].charge:
            c = TakeHitCommand(self.game)
            c.parse()
            return c.execute()

        if self.game.checkpoints['easter']:
            self.valid_weapons.append('dot')

        if self.verb != 'attack':
            return Response(self.game, text='The word you\'re looking for is "attack".')

        elif self.enemy is None:
            return Response(self.game, text='Attack what?')

        elif not any([re.fullmatch(enemy.type, self.enemy) for enemy in self.game.player.room.enemies.values() if
                      enemy.active]):
            return Response(self.game, text='There isn\'t one of those nearby.')

        elif self.weapon is None:
            return Response(self.game, text='Attack with what?')

        elif self.weapon not in self.game.player.inventory:

            for key, item in self.game.player.inventory.items():

                for reg in item.aliases:

                    if re.fullmatch(reg, self.weapon):
                        self.weapon = key
                        break

                if self.weapon in self.game.player.inventory:
                    break

            if self.weapon not in self.game.player.inventory:
                return Response(self.game, text='You don\'t have one of those.')

        if self.weapon not in self.valid_weapons:
            return Response(self.game, text='You can\'t attack with that.')

        else:
            weapon = self.game.player.inventory[self.weapon]
            enemy = None

            for e in self.game.player.room.enemies.values():
                enemy = e

                if re.fullmatch(enemy.type, self.enemy) and enemy.active:
                    break

            if self.weapon != 'dot':
                damage = choice(weapon.damage_dist[0], p=weapon.damage_dist[1])
                text = choice(weapon.combat_text[enemy.name][damage])

            else:
                damage = enemy.health
                text = 'One hit KO!'

            more_text = enemy.lose_health(damage)
            return Response(self.game, text=text + more_text)


class HammerCommand(AttackCommand):
    valid_weapons = ['hammer']
    verb = None
    enemy = None
    weapon = None

    def parse(self):
        text = self.match.string
        self.verb = self.match[1]

        m = re.search(' +with( +.*)?$', text)

        if m:
            if m[1] and m[1].strip():
                self.weapon = m[1].strip()
            text = re.sub(' +with( +.*)?$', '', text)
        remainder = re.sub('^{} *'.format(self.verb), '', text)

        if remainder:
            self.enemy = re.sub('^the +', '', remainder.strip())

    def execute(self):

        if self.enemy is None:
            return Response(self.game, text=self.verb.title() + ' what?')

        elif not (self.enemy in ['floor', 'ground'] or
                  (self.enemy in ['pedestal', 'stone'] and self.game.player.room_name == 'mouc3')):
            return Response(self.game, text='You can\'t {} that.'.format(self.verb))

        elif self.weapon is None:
            return Response(self.game, text=self.verb.title() + ' with what?')

        elif self.weapon not in self.game.player.inventory:

            for key, item in self.game.player.inventory.items():

                for reg in item.aliases:

                    if re.fullmatch(reg, self.weapon):
                        self.weapon = key
                        break

                if self.weapon in self.game.player.inventory:
                    break

            if self.weapon not in self.game.player.inventory:
                return Response(self.game, text='You don\'t have one of those.')

        if self.weapon not in self.valid_weapons:
            return Response(self.game, text='You can\'t {} with that.'.format(self.verb))

        else:
            text = 'BOOM!'

            if self.enemy in ['pedestal', 'stone'] and self.game.rooms['moub3'].state['cave'] == 0:
                text = text + ' The ground shakes as violent avalanches begin to cascade down the mountains in all ' \
                              'directions. You stand safely atop the mountains until they all finally dissipate.'
                self.game.rooms['moub3'].state['cave'] = 1
                self.game.rooms['moub3'].state['extra_directions'] = {'in': [3, 1, 8]}

            return Response(self.game, text=text)


class TakeHitCommand(Command):

    def execute(self):

        if self.game.player.room_name == 'mouc2' and self.game.player.mode == 'combat' and self.game.enemies[
                'mouc2giant'].charge:
            self.game.player.health = 0
            return Response(self.game, text=self.game.enemies['mouc2giant'].charge_attack_text)

        else:
            active_enemies = [enemy for enemy in self.game.player.room.enemies.values() if enemy.active]
            text = []

            for enemy in active_enemies:
                damage = choice(enemy.damage_dist[0], p=enemy.damage_dist[1])
                text.append(choice(enemy.attack_text[damage]))
                self.game.player.health = max(self.game.player.health - damage, 0)
            return Response(self.game, text='Hardly appropriate for a combat situation!\n' + '\n'.join(text))


class EvadeCommand(Command):

    def execute(self):
        active_enemies = [enemy for enemy in self.game.player.room.enemies.values() if enemy.active]

        if active_enemies[0].name == 'giant' and active_enemies[0].charge:
            return Response(self.game, text=choice(active_enemies[0].charge_evade_text))

        else:
            return Response(self.game, text=choice(active_enemies[0].evade_text))


class ClimbTreeCommand(Command):

    def execute(self):
        direction = self.match[1].strip() if self.match[1] is not None else None

        if self.game.player.room_name == 'dead2':

            if direction == 'down':
                return InvalidResponse(self.game)

            else:
                match = re.fullmatch('go (up)', 'go up')
                c = GoCommand(self.game, match)
                c.parse()
                return c.execute()

        elif self.game.player.room_name == 'treeh':

            if direction == 'up':
                return InvalidResponse(self.game)

            else:
                match = re.fullmatch('go (down)', 'go down')
                c = GoCommand(self.game, match)
                c.parse()
                return c.execute()

        else:
            return Response(self.game, text='You can\'t climb here.')


class GiveCommand(DropCommand):

    def execute(self):
        item = self.parsed['item']

        if self.game.player.room_name == 'apoth':

            if item in self.game.player.inventory:

                if item == 'dingleflowers':
                    self.game.player.lose_items([item])
                    self.game.player.room.short_core = self.game.player.room.text['short_core2']
                    self.game.player.room.long_core = self.game.player.room.text['long_core2']
                    self.game.checkpoints['dingleflowers'] = True
                    self.game.rooms['vilb2'].room_blocks = []
                    return Response(self.game, text=self.game.player.room.text['responses']['dingleflowers'])

                elif item == 'bottle':
                    self.game.player.lose_items([item])
                    self.game.player.room.short_core = self.game.player.room.text['short_core3']
                    self.game.player.room.long_core = self.game.player.room.text['long_core3']
                    self.game.checkpoints['water'] = True
                    self.game.rooms['vilb1'].room_blocks = []
                    return Response(self.game, text=self.game.player.room.text['responses']['water'])

                else:
                    return Response(self.game, text='Potion Master: "Hm, not really what I was looking for. '
                                                    'Perhaps you have something else for me?"')

            else:
                return Response(self.game, text='You don\'t have one of those.')

        else:
            return InvalidResponse(self.game)


class DeadByVinesCommand(Command):

    def execute(self):
        self.game.player.health = 0
        return Response(self.game, text='While you waste time doing something other than running away, '
                                        'the vines seize you and crush you!')


class EnterExitCommand(Command):

    def execute(self):

        if self.match.string == 'enter':
            match = re.fullmatch('(?:go +)?(in|out)', 'go in')

        else:
            match = re.fullmatch('(?:go +)?(in|out)', 'go out')

        c = GoCommand(self.game, match)
        c.parse()
        return c.execute()


class LightMatchCommand(Command):

    def execute(self):

        if self.game.player.lit_match['status']:
            return Response(self.game, text='You are already carrying a lit match.')

        else:
            self.game.player.lit_match['status'] = 1
            self.game.player.lit_match['count'] = 4
            return Response(self.game, text='The match is burning.')


class FireplaceCommand(Command):

    def execute(self):
        item = self.match[1]
        stick_checks = [re.fullmatch(regex, item) for regex in self.game.items['sticks'].aliases]
        inv_checks = [re.fullmatch(regex, item) for itm in self.game.player.inventory for regex in
                      self.game.items[itm].aliases]

        if not any(inv_checks):
            return Response(self.game, text='You don\'t have one of those.')

        elif any(stick_checks):
            self.game.rooms['mohut'].state['firewood'] = 1
            self.game.player.lose_items(['sticks'])
            return Response(self.game, text='Done.')

        else:
            return Response(self.game, text='That doesn\'t belong in there.')


class FireCommand(Command):

    def execute(self):

        if self.game.player.room.state['firewood'] == 0:
            return Response(self.game, text='The fireplace is empty.')

        elif self.game.player.room.state['frozen'] == 0:
            return Response(self.game, text='The fire is already lit!')

        elif self.game.player.lit_match['status'] is False:
            return Response(self.game, text='You\'ll need to light a match first.')

        else:
            self.game.player.room.state['frozen'] = 0
            self.game.rooms['moub2'].state['frozen'] = 0
            self.game.player.room.state['firewood'] = 2
            self.game.checkpoints['thaw'] = True
            return Response(self.game, text='The fireplace is filled with a roaring fire. You feel the sensation '
                                            'return to your hands and feet as the room around you slowly thaws out.')


class BootsCommand(Command):

    def execute(self):
        self.game.player.boots = True
        return Response(self.game, text='You are now wearing the snow boots.')


class FillBottleCommand(Command):

    def execute(self):

        if 'bottle' not in self.game.player.inventory:
            return Response(self.game, text='You don\'t have a bottle!')

        elif self.game.player.inventory['bottle'].name != 'Empty Bottle':
            return Response(self.game, text='Your bottle is already full!')

        else:
            self.game.player.inventory['bottle'].name = 'Bottle of Alaria Spring Water'
            self.game.player.inventory['bottle'].aliases = ['((the|a) +)?bottle( +of +(alaria +)?(spring +)?water)?',
                                                            '(the +)?(alaria +)?(spring +)?water']
            return Response(self.game, text='Your bottle is now full of Alaria Spring Water.')


class PlaceOrbsCommand(Command):

    def execute(self):

        if 'sapphire' not in self.game.player.inventory or 'ruby' not in self.game.player.inventory or \
                'citrine' not in self.game.player.inventory:
            return Response(self.game, text='You don\'t have all three orbs!')

        else:
            self.game.player.room.state['orbs'] = 1
            return Response(self.game,
                            text='You step up to the alter and place the three orbs onto the pedestals. As you step '
                                 'back, the ground begins to shake and the orbs start to glow, becoming brighter and '
                                 'brighter until you have to shield your eyes. Then, with a deafening roar, a huge '
                                 'beam of white light bursts out of the altar and into the sky, vanquishing the dark '
                                 'clouds. And then, silence...')


def initialise_commands(items, rooms):
    generic_commands = {
        '(?:go +)?(north|south|east|west|up|down|upstairs|downstairs|in|out|inside|outside)': GoCommand,
        'wait': WaitCommand,
        'look(?: +a?round)?': LookCommand,
        '(?:(?:check|inspect|examine) +)?(?:items|inventory)': InventoryCommand,
        '(?:get|take|grab|pick +up) +(.+)': GetCommand,
        'pick +(.+) +up': GetCommand,
        '(?:drop|leave|put +down) +(.+)': DropCommand,
        'put +(.+) +(?:down|on +(?:the +)?floor|on +(?:the +)?ground)': DropCommand,
        'dig(?: +(?:a +)?hole)?(?: +with +(?:the +)?(?:shovel|spade))?': DigCommand,
        'climb( +(?:up|down))?(?: +(?:the +)?tree)?': ClimbTreeCommand,
        'enter|exit': EnterExitCommand
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

    rooms['mohut'].commands.update(
        {
            '(?:unlock|open)(?: +(?:the +)?chest)?': OpenChestHutCommand
        }
    )

    rooms['vila2'].commands.update(
        {
            '(?:cut|slice|clear|sever)'
            '(?: +(?:the +)?(?:vines|thicket))?(?: +with +(?:the +)?(?:sword))?': CutVinesCommand
        }
    )

    rooms['apoth'].commands.update(
        {
            '(?:give +her|show +her) +(.+)': GiveCommand,
            '(?:give|present|show|hand +over) +(.+?)(?: +to +(?:her|(?:the +)?(?:potion +)?master))?': GiveCommand
        }
    )

    rooms['mohut'].commands.update(
        {
            '(?:put|place) +(.+) +(?:in(?:(?:to|side))? +(?:the +)?fireplace)': FireplaceCommand
        }
    )

    rooms['mohut'].commands.update(
        {
            '(?:light|ignite) +(?:(?:the|a) +)?fire': FireCommand,
            '(?:light|ignite) +(?:the +)?fire(?:wood|place)': FireCommand,
            'start +(?:(?:the|a) +)?fire': FireCommand,
            '(?:light|ignite|burn) +(?:the +)?(?:fire)?wood': FireCommand
        }
    )

    rooms['cave1'].commands.update(
        {
            'fill +(up +)?((the( +empty)?|a(n? +empty)?) +)?bottle'
            '( +with +((the|some( +of +the)?) +)?(alaria +)?(spring +)?water)?': FillBottleCommand,
            'get +((the|some( +of +the)?) +)?(alaria +)?(spring +)?water': FillBottleCommand
        }
    )

    rooms['shrin'].commands.update(
        {
            '(put|place|set) +((the|all|all +of +the|the +three|all +three( +of +the)?) +)?orbs? +(on(to)?|upon) +'
            '(((the|an?) +)?(stone +)?(altar|pedestals?)|'
            '((the|all|all +of +the|the +three|all +three( +of +the)?) +)?(stone +)?pedestals?)': PlaceOrbsCommand,
            '(put|place|set) +(((the|an?) +)?((red|blue|yellow|sapphire|ruby|citrine) +)?|(one|each)( +of +the)? +)?'
            'orbs? +(on(to)?|upon) +((the|an?|(one|each)( +of +the)?) +)?(stone +)?(altar|pedestals?)': PlaceOrbsCommand
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
            '(attack|hit|strike|stab)( +.*)?': AttackCommand
        }
    )

    items['axe'].combat_commands.update(
        {
            '(attack|hit|strike)( +.*)?': AttackCommand
        }
    )

    items['dot'].combat_commands.update(
        {
            '(attack|hit|strike|kill)( +.*)?': AttackCommand
        }
    )

    items['matchbook'].commands.update(
        {
            '(?:light|strike|ignite|burn) +(?:a +)?match': LightMatchCommand
        }
    )
    items['snow boots'].commands.update(
        {
            '(?:wear|equip|put +on|strap +on|don) +(the +)?(snow *)?boots': BootsCommand,
            'put +(the +)?(snow *)?boots +on': BootsCommand,
            'change +into +(the +)?(snow *)?boots': BootsCommand,
            '(change|swap|switch) +(boots|shoes)': BootsCommand
        }
    )
    items['hammer'].commands.update(
        {
            '(hit|strike|pound|smash|hammer)( +.*)?': HammerCommand
        }
    )
    return generic_commands
