from json import load


with open('map.json') as f:
    game_map = load(f)


class Item:
    def __init__(self, item_data):
        self.name = item_data['name']
        self.aliases = item_data['aliases'] if 'aliases' in item_data else []
        self.init_desc = item_data['text']['init_desc']
        self.text = item_data['text']
        self.taken = 0
        self.visible = item_data['visible']
        self.commands = {}
        self.combat_commands = {}
        self.damage_dist = [[], []]
        self.combat_text = {}


game_items = game_map['items']
game_items = {name.lower(): Item(data) for name, data in game_items.items()}

game_items['sword'].combat_text['goblin'] = {0: ['You swing your sword at the goblin, but miss.',
                                                 'You lunge at the goblin, but it leaps aside, avoiding your attack.'],
                                             20: ['Your slice attack connects, ' +
                                                  'finding its mark beneath the goblin\'s thin armour.',
                                                  'You lunge at the goblin with your sword. It\'s a hit!',
                                                  'The goblin is too slow for you, and gets caught by your attack.'],
                                             40: ['Critical hit! Your blade strikes the goblin for double damage!']}
game_items['sword'].combat_text['troll'] = {0: ['You swing your sword at the troll, but miss.',
                                                'You lunge at the troll, but it brushes off your attack like it ' +
                                                'was nothing.'],
                                            20: ['Your slice attack finds the weak spot in the troll\'s armour.',
                                                 'You lunge fiercely at the troll with your sword. Got the bastard!',
                                                 'You\'re too fast for the sluggish troll, who takes the full brunt ' +
                                                 'of your attack.'],
                                            40: ['Critical hit! Your blade strikes the troll for double damage!']}
game_items['sword'].damage_dist = [[0, 20, 40], [0.4, 0.4, 0.2]]
