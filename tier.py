import math


class TierItem:
    def __init__(self, name, score, text, number=None, scores_per_role=None, totals_per_role=None):
        self.name = name
        self.score = score
        self.text = text
        self.score_per_role = scores_per_role
        self.totals_per_role = totals_per_role
        self.number = float(score) if number is None else number

    def __repr__(self):
        return str(self.score_per_role)


class Tier:
    NUMBER_OF_TIERS = 3

    def __init__(self, weight, sorted_scores, message, reverse=True, is_max=False):
        self.weight = weight / 4 if is_max else weight
        self.scores_array = sorted_scores
        self.player_count = len(self.scores_array)
        self.unique_elements = len(set([x.score for x in self.scores_array]))
        self.tier_size = math.ceil(self.unique_elements / self.NUMBER_OF_TIERS)
        self.message = message
        self.is_max = is_max
        self.reverse = reverse
        self.tiers = self.get_tiers()

    def players_sorted_by_role(self, role):
        ordered = sorted([[t.name, float(t.score_per_role[role])] for t in
                   sorted([v for v in self.scores_array if v.score_per_role[role] is not None],
                          key=lambda e: e.score_per_role[role], reverse=self.reverse)],
                         key=lambda x: x[1], reverse=self.reverse)
        return ordered

    def get_tiers(self):
        tiers = dict()
        grouped_values = self.group(
            list(set([x.number if x.number is not None else x.score for x in self.scores_array])))
        for i in range(0, self.NUMBER_OF_TIERS):
            tiers[i] = list()
            for tier_item in self.scores_array:
                if tier_item.number is not None and tier_item.number in grouped_values[i] or tier_item.score in \
                        grouped_values[i]:
                    tiers[i].append(tier_item)
        return tiers

    def group(self, unique_values):
        tiers = {i: [] for i in range(self.NUMBER_OF_TIERS)}
        unique_values = sorted(unique_values, reverse=self.reverse)
        divs = [len(unique_values)/self.NUMBER_OF_TIERS, len(unique_values)*2/self.NUMBER_OF_TIERS]
        for j in range(len(unique_values)):
            if j < divs[0]:
                tiers[0].append(unique_values[j])
            elif j < divs[1]:
                tiers[1].append(unique_values[j])
            else:
                tiers[2].append(unique_values[j])
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
