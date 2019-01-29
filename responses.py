#!/usr/bin/env python

"""responses.py: Defines the response objects that a command can return."""

__author__ = "James Smith"


class Response:
    def __init__(self, game, validity='valid', outcome='success', dead=False, text='', checkpoint=False):
        self.game = game
        self.validity = validity
        self.outcome = outcome
        self.dead = dead
        self.text = text
        self.checkpoint = checkpoint

    def text_constructor(self):
        return self.text


class InvalidResponse(Response):

    def text_constructor(self):
        return 'You can\'t do that.'


class GoResponse(Response):
    def __init__(self, game, validity, outcome, dead=False, direction=None, desc_type='short'):
        super().__init__(game, validity, outcome, dead)
        self.direction = direction
        self.desc_type = desc_type

    def text_constructor(self):

        if self.outcome == 'success':
            text = self.game.player.describe_current_room(desc_type=self.desc_type)

            if (self.game.player.room_name == 'mouc1' and self.direction == 'east') or \
                    (self.game.player.room_name == 'mouc2' and self.direction == 'north'):
                return 'With the snow boots on, you\'re able to scramble up the steep hill...\n\n' + text

            elif (self.game.player.room_name == 'mouc1' and self.direction == 'south') or \
                    (self.game.player.room_name == 'moub1' and self.direction == 'west'):
                return 'With the snow boots on, you\'re able to safely descend the steep hill...\n\n' + text

            else:
                return text

        elif self.validity == 'valid':
            if self.game.player.room_name == 'vilb2' and self.direction == 'east':
                return 'That path leads into the Gygax Mountains. You have somewhere else that you\'re ' \
                       'supposed to be going!'

            elif self.game.player.room_name == 'vilb1' and self.direction == 'south':
                return 'That path leads to Floonyloon Shrine. You have somewhere else that you\'re ' \
                       'supposed to be going!'

            elif self.game.player.room_name == 'vila2' and self.direction == 'in':
                return 'You\'re supposed to be going to see Jimbo!'

            else:
                return 'You can\'t go that way.'

        else:
            return 'You can\'t do that.'


class WaitResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':
            return 'Time passes...'

        else:
            return 'You can\'t do that.'


class LookResponse(Response):

    def text_constructor(self):
        return self.game.player.describe_current_room(desc_type='long')


class InventoryResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':

            if len(self.game.player.inventory) > 0:
                return '\n'.join(['Your inventory consists of:'] +
                                 [item.name for item in self.game.player.inventory.values()])

            else:
                return 'You have no items!'

        else:
            return 'You can\'t do that.'


class GetResponse(Response):
    def __init__(self, game, validity, outcome, method, dead=False, new_items=None):
        super().__init__(game, validity, outcome, dead)
        self.new_items = new_items
        self.method = method

    def text_constructor(self):

        if self.validity == 'valid':

            if self.outcome == 'success':

                if self.method == 'all':
                    to_return = '\n'.join([self.game.items[item].name + ': taken.' for item in self.new_items])

                elif self.method == 'specific':
                    to_return = 'Taken.'

                else:
                    raise ValueError('Unexpected get method')

                if 'dingleflowers' in self.new_items and self.new_items['dingleflowers'] == 0:
                    self.game.checkpoints['vines'] = True
                    return to_return + '\n\nAs soon as you take the Dingleflowers, thorny vines spring up from the ' \
                                       'earth and attempt to grab you. Time to leave! Escape to the village without ' \
                                       'taking a wrong turn!'

                else:
                    return to_return

            else:
                return 'There are no items here.'

        else:
            return 'There isn\'t one of those nearby.'
