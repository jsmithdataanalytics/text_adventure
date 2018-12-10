from avatar import *


class Response:
    def __init__(self, validity='valid', outcome='success', dead=False, text=''):
        self.validity = validity
        self.outcome = outcome
        self.dead = dead
        self.text = text

    def text_constructor(self):
        return self.text


class InvalidResponse(Response):

    def text_constructor(self):
        return 'You can\'t do that.'


class GoResponse(Response):
    def __init__(self, validity, outcome, dead=False, direction=None, desc_type='short'):
        super().__init__(validity, outcome, dead)
        self.direction = direction
        self.desc_type = desc_type

    def text_constructor(self):

        if self.outcome == 'success':
            return player.describe_current_room(desc_type=self.desc_type)

        elif self.validity == 'valid':
            if player.room_name == 'vilb2' and self.direction == 'east':
                return 'That path leads into the Gygax Mountains. Don\'t you have somewhere else that you\'re ' \
                       'supposed to be going?'

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

        if self.validity == 'valid':
            return player.describe_current_room(desc_type='long')

        else:
            return 'You can\'t do that.'


class InventoryResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':

            if len(player.inventory) > 0:
                return '\n'.join(['Your inventory consists of:'] + [item.name for item in player.inventory.values()])

            else:
                return 'You have no items!'

        else:
            return 'You can\'t do that.'


class GetResponse(Response):
    def __init__(self, validity, outcome, method, dead=False, new_items=None):
        super().__init__(validity, outcome, dead)
        self.new_items = new_items
        self.method = method

    def text_constructor(self):

        if self.validity == 'valid':

            if self.outcome == 'success':

                if len(self.new_items) > 1:
                    return '\n'.join([items[item].name + ': taken.' for item in self.new_items])

                elif self.method == 'all':
                    return items[self.new_items[0]].name + ': taken.'

                elif self.method == 'specific':
                    return 'Taken.'

            else:
                return 'There are no items here.'

        else:
            return 'There isn\'t one of those nearby.'
