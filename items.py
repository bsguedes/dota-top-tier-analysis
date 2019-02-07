def evaluate_items(players):
    items = {i: {p['account_id']: 0 for p in players} for i, j in item_list().items()}
    for player in players:
        if player['purchase'] is None:
            return None
        for item, amount in player['purchase'].items():
            if item in items:
                items[item][player['account_id']] = amount
    return items


def item_list():
    return {
        'black_king_bar': 'Black King Bar',
        'blink': 'Blink Dagger',
        'vladmir': 'Vladmir\'s Offering',
        'radiance': 'Radiance',
        'magic_wand': 'Magic Wand',
        'magic_stick': 'Magic Stick',
        'bottle': 'Bottle',
        'ultimate_scepter': 'Aghanim\'s Scepter',
        'hand_of_midas': 'Hand of Midas',
        'rapier': 'Divine Rapier'
    }
