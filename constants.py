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


def rating(win, loss=None, matches=None):
    if matches is not None:
        loss = matches - win
    if win == 0:
        return 0
    wr = win / (win + loss)
    ex = 1 - math.exp(-(win + loss)/2)
    sg = 1 / (1 + math.exp(-(win-loss)))
    return 9 * wr * ex + sg
