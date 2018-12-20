import math


class TierItem:
    def __init__(self, name, score, text):
        self.name = name
        self.score = score
        self.text = text
        self.tier = 0

    def set_tier(self, tier):
        self.tier = tier


class Tier:
    NUMBER_OF_TIERS = 3

    def __init__(self, sorted_scores, message):
        self.scores_array = sorted_scores
        self.player_count = len(self.scores_array)
        self.tier_size = math.ceil(self.player_count / self.NUMBER_OF_TIERS)
        self.message = message
        self.tiers = self.get_tiers()

    def get_tiers(self):
        tiers = dict()
        count = 0
        for i in range(0, self.NUMBER_OF_TIERS):
            tiers[i] = list()
            for j in range(count, min(int((i + 1) * self.tier_size), self.player_count)):
                tiers[i].append(self.scores_array[j])
                self.scores_array[j].set_tier(i+1)
                count += 1
            if i < self.NUMBER_OF_TIERS - 1:
                while self.scores_array[count].score == tiers[i][-1].score:
                    tiers[i].append(self.scores_array[count])
                    self.scores_array[count].set_tier(i + 1)
                    count += 1
        return tiers

    def print(self):
        print('')
        print(self.message.upper())
        for i in range(0, self.NUMBER_OF_TIERS):
            print('')
            print('Tier %i:' % (i + 1))
            for item in self.tiers[i]:
                print(item.text)

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
