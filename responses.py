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
        return 'Invalid command.'


class GoResponse(Response):
    def __init__(self, validity, outcome, dead=False, direction=None):
        super().__init__(validity, outcome, dead)
        self.direction = direction

    def text_constructor(self):

        if self.outcome == 'success':
            return player.describe_current_room()

        elif self.validity == 'valid':
            return 'You can\'t go that way.'

        else:
            return 'Invalid command.'


class WaitResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':
            return 'Time passes...'

        else:
            return 'Invalid command.'


class LookResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':
            return player.describe_current_room()

        else:
            return 'Invalid command.'


class InventoryResponse(Response):

    def text_constructor(self):

        if self.validity == 'valid':

            if len(player.inventory) > 0:
                return ['Your inventory consists of:'] + [item.name for item in player.inventory.values()]

            else:
                return 'You have no items!'

        else:
            return 'Invalid command.'


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
