import math


def item_cost():
    return {
        'ward_observer': 75,
        'ward_sentry': 100,
        'dust': 180,
        'smoke_of_deceit': 50,
        'gem': 900
    }


def roles():
    return {
        1: "hard carry", 
        2: "mid", 
        3: "offlane", 
        4: "support", 
        5: "hard support"
    }


def lobby_type():
    return [
        'normal',
        'practice',
        'tournament',
        'tutorial',
        'bots',
        'ranked_team',
        'ranked_solo',
        'ranked',
        'mid',
        'battle_cup'
    ]


def rating(win, loss=None, matches=None):
    if matches is not None:
        loss = matches - win
    if win == 0:
        return 0
    wr = win / (win + loss)
    ex = 1 - math.exp(-(win + loss)/2)
    sg = 1 / (1 + math.exp(-(win-loss)/3))
    return 3 * wr * ex + 7 * sg


def sequence(strings, maximum=None):
    if maximum is None or len(strings) <= 5:
        return '%s and %s' % (', '.join(strings[:-1]), strings[-1]) if len(strings) > 1 else strings[0]
    else:
        return "%s, ..." % ', '.join(strings[:5])
