import math
import numpy as np


class TierItem:
    def __init__(self, name, score, text, number=None):
        self.name = name
        self.score = score
        self.text = text
        self.number = float(score) if number is None else number


class Tier:
    NUMBER_OF_TIERS = 3

    def __init__(self, weight, sorted_scores, message, reverse=True, is_max=False):
        self.weight = weight / 4 if is_max else weight
        self.scores_array = sorted_scores
        self.player_count = len(self.scores_array)
        self.tier_size = math.ceil(self.player_count / self.NUMBER_OF_TIERS)
        self.message = message
        self.is_max = is_max
        self.reverse = reverse
        self.tiers = self.get_tiers()

    def get_tiers(self):
        tiers = dict()
        count = 0
        for i in range(0, self.NUMBER_OF_TIERS):
            tiers[i] = list()
            for j in range(count, min(int((i + 1) * self.tier_size), self.player_count)):
                tiers[i].append(self.scores_array[j])
                count += 1
            if i < self.NUMBER_OF_TIERS - 1:
                while count < len(self.scores_array) and len(tiers[i]) > 0 \
                        and self.scores_array[count].score == tiers[i][-1].score:
                    tiers[i].append(self.scores_array[count])
                    count += 1
        for i in range(1, self.NUMBER_OF_TIERS):
            if len(tiers[i - 1]) == 0:
                tiers[i - 1] = tiers[i]
                tiers[i] = list()
        return tiers

    def list_to_print(self):
        lst = list()
        lst.append('')
        lst.append(self.message)
        for i in range(self.NUMBER_OF_TIERS):
            lst.append('')
            lst.append('Tier %i:' % (i + 1))
            if i in self.tiers:
                for item in self.tiers[i]:
                    lst.append(item.text)
        return lst

    def print(self):
        for item in self.list_to_print():
            print(item)

    def get_top_three(self):
        return self.scores_array[0:min(3, len(self.scores_array))]

    @staticmethod
    def show_results_weights(players, tier_list):
        points = {k: 0 for k, v in players.items()}
        for table in tier_list:
            level = 0
            for _, tier_items in table.tiers.items():
                for ti in tier_items:
                    p = (3 - level) * table.weight
                    points[ti.name] += p
                level += 1

        print('')
        s = sorted(points.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%s;%i' % (k, v))
        return s

    @staticmethod
    def show_results(players, tier_list):
        medals = {k: [0, 0, 0] for k, v in players.items()}
        for table in tier_list:
            level = 0
            for _, tier_items in table.tiers.items():
                for ti in tier_items:
                    medals[ti.name][level] += 1
                level += 1
        for name, _ in players.items():
            medals[name] = (medals[name][0], medals[name][1], medals[name][2])

        print('')
        s = sorted(medals.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%s;%i;%i;%i' % (k, v[0], v[1], v[2]))
        return s


class T:
    @staticmethod
    def percentage(number):
        return number * 100

    @staticmethod
    def sec_to_min(number):
        return int(100 * number / 60) / 100
