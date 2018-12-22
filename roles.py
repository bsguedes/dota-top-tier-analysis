import operator
from constants import Constants


class Roles:
    @staticmethod
    def evaluate_roles(match_summary, team_players):
        our_players = match_summary['players']
        result_roles = [-1] * 5
        team_players = team_players[0:5] if match_summary['is_radiant'] else team_players[5:10]
        for i in range(0, 5):
            if team_players[i]['account_id'] not in our_players:
                team_players[i]['account_id'] = i

        roamers = [x['account_id'] for x in team_players if x['lane_role'] == 4 or x['is_roaming']]
        mid_players = [x['account_id'] for x in team_players if x['lane_role'] == 2 and x['account_id'] not in roamers]
        safe_players = [x['account_id'] for x in team_players if x['lane_role'] == 1 and x['account_id'] not in roamers]
        off_players = [x['account_id'] for x in team_players if x['lane_role'] == 3 and x['account_id'] not in roamers]
        composition = '%i-%i-%i' % (len(safe_players), len(mid_players), len(off_players))

        if len(mid_players) == 1:
            result_roles[1] = mid_players[0]
            mid_players.remove(result_roles[1])
        elif len(mid_players) > 1:
            result_roles[1] = Roles.max_gpm(mid_players, team_players)
            mid_players.remove(result_roles[1])

        if len(safe_players) > len(off_players):
            result_roles[0] = Roles.max_gpm(safe_players, team_players)
            safe_players.remove(result_roles[0])
            if len(off_players) > 0:
                result_roles[2] = Roles.max_gpm(off_players, team_players)
                off_players.remove(result_roles[2])
        elif len(off_players) > len(safe_players):
            result_roles[0] = Roles.max_gpm(off_players, team_players)
            off_players.remove(result_roles[0])
            if len(safe_players) > 0:
                result_roles[2] = Roles.max_gpm(safe_players, team_players)
                safe_players.remove(result_roles[2])
        else:
            result_roles[0] = Roles.max_gpm(safe_players, team_players)
            if result_roles[0] in safe_players:
                safe_players.remove(result_roles[0])
                result_roles[2] = Roles.max_gpm(off_players, team_players)
                off_players.remove(result_roles[2])
            else:
                off_players.remove(result_roles[0])
                result_roles[2] = Roles.max_gpm(safe_players, team_players)
                safe_players.remove(result_roles[2])

        rest_of_players = safe_players + mid_players + off_players + roamers
        pos = 0
        while -1 in result_roles:
            if result_roles[pos] == -1:
                result_roles[pos] = Roles.max_gpm(rest_of_players, team_players)
                rest_of_players.remove(result_roles[pos])
            pos += 1

        positions = {x: Constants.roles()[result_roles.index(x)+1] for x in result_roles if x > 9}
        return {'composition': composition, 'positions': positions}

    @staticmethod
    def max_gpm(players, team_players):
        gpm_list = {k['account_id']: k['gold_per_min'] for k in team_players if k['account_id'] in players}
        m = max(gpm_list.items(), key=operator.itemgetter(1))
        return m[0]