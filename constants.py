import math


def item_cost():
    return {
        'ward_observer': 75,
        'ward_sentry': 50,
        'dust': 90,
        'smoke_of_deceit': 50,
        'gem': 900
    }


def fix_time(t):
    return int(int(t) - 60 * 60 * 2.5)


def roles():
    return {
        1: "hard carry", 
        2: "mid", 
        3: "offlane", 
        4: "support", 
        5: "hard support"
    }


def role_list():
    return ['hard carry', 'mid', 'offlane', 'support', 'hard support']


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
    exp_factor = 1 - math.exp(-win/5)
    phat = (win + 1)/(loss + (win + 1))
    n = win + loss + 1
    z = 1.96
    plus_factor = 4.5 * (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    minus_factor = 4.5 * (phat + z*z/(2*n) + z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    rat = exp_factor + plus_factor + minus_factor
    if rat > 0:
        return rat
    else:
        if win == 0:
            return 1 - loss * (loss + 1) / 200
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


def average_rank(ranks):
    r = [float(x // 10) for x in ranks if x is not None]
    return None if len(r) == 0 else sum(r) / len(r)


def mmr_diff(a, b):
    base = 10
    increase = 50
    quotient = 400
    return 0
    # return increase * (1 - 1 / (1 + base ** (b ** 3 - a ** 3) / quotient))
