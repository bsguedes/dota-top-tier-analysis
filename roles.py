import operator
from constants import roles


class Roles:
    @staticmethod
    def got_first_blood(players, our_players):
        for player in players:
            if 'firstblood_claimed' not in player:
                return None
            if player['firstblood_claimed'] == 1 and player['account_id'] in our_players:
                return True
        return False

    @staticmethod
    def first_bounties(players, our_players):
        runes = 0
        for player in players:
            if player['runes_log'] is None:
                return None
            if player['account_id'] in our_players:
                runes += sum([1 for r in player['runes_log'] if r['key'] == 5 and r['time'] < 300])
        return runes

    @staticmethod
    def evaluate_roles(match_summary, team_players):
        our_players = match_summary['players']
        result_roles = [-1] * 5
        team_players = team_players[0:5] if match_summary['is_radiant'] else team_players[5:10]
        for i in range(5):
            if team_players[i]['account_id'] not in our_players:
                team_players[i]['account_id'] = i

        roamers = [x['account_id'] for x in team_players if x['lane_role'] == 4 or x['is_roaming']]
        mid_players = [x['account_id'] for x in team_players if x['lane_role'] == 2 and x['account_id'] not in roamers]
        safe_players = [x['account_id'] for x in team_players if x['lane_role'] == 1 and x['account_id'] not in roamers]
        off_players = [x['account_id'] for x in team_players if x['lane_role'] == 3 and x['account_id'] not in roamers]
        if len(roamers) == 0:
            composition = '%i-%i-%i' % (len(safe_players), len(mid_players), len(off_players))
        else:
            composition = '%i-%i-%i (%i roaming)' % (len(safe_players), len(mid_players),
                                                     len(off_players), len(roamers))

        partners = [sorted(safe_players), sorted(mid_players), sorted(off_players)]

        if len(mid_players) == 1:
            result_roles[1] = mid_players[0]
            mid_players.remove(result_roles[1])
        elif len(mid_players) > 1:
            result_roles[1] = Roles.max_gpm(mid_players, team_players)
            mid_players.remove(result_roles[1])

        rest_of_players = safe_players + mid_players + off_players + roamers

        hc_points = {p: 0 for p in rest_of_players}
        targets = [p for p in team_players if result_roles[1] != p['account_id']]
        params = ['last_hits', 'hero_damage', 'kills', 'total_gold']
        weights = [2, 1, 0, 4]
        for player in targets:
            pid = player['account_id']
            if pid in safe_players:
                hc_points[pid] += 108
            for param, w in zip(params, weights):
                if player[param] == max(targets, key=lambda e: e[param])[param]:
                    hc_points[pid] += 100 + w
        ordered = sorted(hc_points.items(), key=lambda k: -k[1])
        result_roles[0] = ordered[0][0]
        hc_lane = 1 if result_roles[0] in safe_players else 3

        if hc_lane == 1:
            off_candidates = roamers if len(off_players) == 0 else off_players
        else:
            off_candidates = roamers if len(safe_players) == 0 else safe_players
        if len(off_candidates) == 0:
            off_candidates = [x for x in rest_of_players if x != result_roles[0]]
        off_points = {p: 0 for p in off_candidates}
        targets = [p for p in team_players if p['account_id'] in off_candidates]
        params = ['last_hits', 'hero_damage', 'kills', 'total_gold']
        weights = [4, 1, 0, 2]
        min_t = min(10, len(targets[0]['lh_t']))
        max_lh_t = max(targets, key=lambda e: e['lh_t'][min_t])['lh_t'][min_t]
        for player in targets:
            pid = player['account_id']
            if player['lh_t'][min_t] == max_lh_t:
                off_points[pid] += 108
            for param, w in zip(params, weights):
                if player[param] == max(targets, key=lambda e: e[param])[param]:
                    off_points[pid] += 100 + w
        ordered = sorted(off_points.items(), key=lambda k: -k[1])
        result_roles[2] = ordered[0][0]

        remaining = [p for p in rest_of_players if p not in result_roles]
        hs_points = {p: 0 for p in remaining}
        targets = [p for p in team_players if p['account_id'] in remaining]
        params = ['last_hits', 'sen_placed', 'obs_placed', 'total_gold']
        order = [-1, 1, 1, -1]
        weights = [0, 1, 2, 4]

        for player in targets:
            pid = player['account_id']
            if player['lane_role'] == hc_lane:
                hs_points[pid] += 208
            for param, w, o in zip(params, weights, order):
                if player[param] == max(targets, key=lambda e: o * e[param])[param]:
                    hs_points[pid] += 100 + w
        ordered = sorted(hs_points.items(), key=lambda k: -k[1])
        result_roles[4] = ordered[0][0]
        result_roles[3] = ordered[1][0]

        positions = {x: roles()[result_roles.index(x)+1] for x in result_roles if x > 9}
        return {'composition': composition, 'positions': positions, 'partners': [p for p in partners if len(p) >= 2]}

    @staticmethod
    def max_gpm(players, team_players):
        gpm_list = {k['account_id']: k['gold_per_min'] for k in team_players if k['account_id'] in players}
        m = max(gpm_list.items(), key=operator.itemgetter(1))
        return m[0]

    @staticmethod
    def max_wards(players, team_players):
        wards_list = {k['account_id']: (-k['obs_placed'] - k['sen_placed'], -k['gold_per_min']) for k in team_players if
                      k['account_id'] in players}
        m = max(wards_list.items(), key=operator.itemgetter(1))
        return m[0]
