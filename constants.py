import math


def item_cost():
    return {
        'ward_observer': 75,
        'ward_sentry': 100,
        'dust': 180,
        'smoke_of_deceit': 50,
        'gem': 900
    }


def fix_time(t):
    return int(int(t) - 60 * 60 * 2.7)


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


def game_mode():
    return [
        'Unknown',
        'All Pick',
        'Captains Mode',
        'Random Draft',
        'Single Draft',
        'All Random',
        'Intro',
        'Diretide',
        'Reverse Captains Mode',
        'Greeviling',
        'Tutorial',
        'Mid Only',
        'Least Played',
        'Limited Heroes',
        'Compendium Matchmaking',
        'Custom',
        'Captains Draft',
        'Balanced Draft',
        'Ability Draft',
        'Event',
        'All Random Deathmatch',
        '1v1 Mid',
        'All Draft',
        'Turbo',
        'Mutation'
    ]


def match_types():
    return {
        'normal': 'Normal Game',
        'practice': 'Practice',
        'tournament': 'Tournament',
        'tutorial': 'Tutorial',
        'bots': 'Bots',
        'ranked_team': 'Party Ranked',
        'ranked_solo': 'Solo Ranked',
        'ranked': 'Ranked',
        'mid': '1 vs. 1 Mid',
        'battle_cup': 'Battle Cup'
    }


def win_rate(wins, matches):
    return 0 if matches == 0 else 100 * wins / matches


def rating(win, loss=None, matches=None):
    if matches is not None:
        loss = matches - win
    if win == 0:
        return 0
    wr = win / (win + loss)
    ex = 1 - math.exp(-(win + loss)/2)
    ex2 = 1 - math.exp(-((win + loss)**2))
    sg = 1 / (1 + math.exp(-(win-loss)/3))
    return 7 * wr * ex + 2 * math.sqrt(sg) + ex2


def sequence(strings, maximum=None):
    if maximum is None or len(strings) <= maximum:
        return '%s and %s' % (', '.join(strings[:-1]), strings[-1]) if len(strings) > 1 else strings[0]
    else:
        return "%s, ..." % ', '.join(strings[:maximum])
