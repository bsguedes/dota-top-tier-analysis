import random
RARE_CHANCE = 3.3 / 4
COMMON_CHANCE = (100 - RARE_CHANCE * 4) / 10
SIMULATIONS = 50000

RELICS = {
    10: RARE_CHANCE,
    11: RARE_CHANCE,
    12: RARE_CHANCE,
    13: RARE_CHANCE,
    0: COMMON_CHANCE,
    1: COMMON_CHANCE,
    2: COMMON_CHANCE,
    3: COMMON_CHANCE,
    4: COMMON_CHANCE,
    5: COMMON_CHANCE,
    6: COMMON_CHANCE,
    7: COMMON_CHANCE,
    8: COMMON_CHANCE,
    9: COMMON_CHANCE
}


def weighted_random_choice(choices):
    _max = sum(choices.values())
    pick = random.uniform(0, _max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key


def criteria(rs, commons, rares):
    c = rs[:10]
    r = rs[10:]
    return sum([1 for x in c if x]) >= commons and sum([1 for x in r if x]) >= rares


for j in range(9, 11):
    for k in range(0, 5):
        total_rolls = 0
        total_cost = 0
        for i in range(SIMULATIONS):
            relics = [False for _ in range(14)]
            rolls = 0
            spent = 0
            while not criteria(relics, j, k):
                rolls += 1
                spent += 800
                choice = weighted_random_choice(RELICS)
                if relics[choice] and choice < 10:
                    spent -= 400
                elif relics[choice]:
                    spent -= 5000
                relics[choice] = True
            spent += sum([5000 for x in relics[:10] if not x]) + sum([10000 for x in relics[10:] if not x])
            total_rolls += rolls
            total_cost += spent
        print(j, k, total_rolls / SIMULATIONS, total_cost / SIMULATIONS)
