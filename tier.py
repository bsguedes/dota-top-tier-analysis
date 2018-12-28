import math


class TierItem:
    def __init__(self, name, score, text):
        self.name = name
        self.score = score
        self.text = text


class Tier:
    NUMBER_OF_TIERS = 3

    def __init__(self, weight, sorted_scores, message, is_max=False):
        self.weight = weight / 4 if is_max else weight
        self.scores_array = sorted_scores
        self.player_count = len(self.scores_array)
        self.tier_size = math.ceil(self.player_count / self.NUMBER_OF_TIERS)
        self.message = message
        self.is_max = is_max
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
            if len(tiers[i-1]) == 0:
                tiers[i-1] = tiers[i]
                tiers[i] = list()
        return tiers

    def list_to_print(self):
        l = list()
        l.append('')
        l.append(self.message)
        for i in range(0, self.NUMBER_OF_TIERS):
            l.append('')
            l.append('Tier %i:' % (i + 1))
            for item in self.tiers[i]:
                l.append(item.text)
        return l

    def print(self):
        for item in self.list_to_print():
            print(item)

    def get_top_three(self):
        return self.scores_array[0:3]

    @staticmethod
    def show_results_weights(players, tier_list):
        points = {k: 0 for k, v in players.items()}
        for table in tier_list:
            level = 0
            for tier_level, tier_items in table.tiers.items():
                for ti in tier_items:
                    p = (3 - level) * table.weight
                    points[ti.name] += p if not table.is_max else p / 4
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
            for tier_level, tier_items in table.tiers.items():
                for ti in tier_items:
                    medals[ti.name][level] += 1
                level += 1
        for name, pid in players.items():
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
