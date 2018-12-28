# coding=utf-8

import json
import calendar
import operator
import itertools
from time import *
from tier import TierItem
from roles import Roles
from constants import Constants


class Parser:
    def __init__(self, team_name, years, players, min_matches, min_party_size):
        self.team_name = team_name
        self.years = years
        self.players = players
        self.min_matches = min_matches
        self.min_party_size = min_party_size
        self.matches_by_party_size = []
        self.match_summary_by_player = []
        self.match_summary_by_team = []
        self.top_comebacks = []
        self.top_throws = []
        self.against_heroes = []
        self.with_heroes = []
        self.most_played_heroes = []

    def identify_heroes(self, matches, min_couple_matches=10):
        hs = open('data/heroes.json', 'r', encoding='utf-8').read()
        hs_json = json.loads(hs)
        heroes = {h['id']: h['localized_name'] for h in hs_json}
        inv_h = {h['localized_name']: h['id'] for h in hs_json}
        inv_p = {v: k for k, v in self.players.items()}
        account_ids = [v for k, v in self.players.items()]
        match_summary = {k: {'our_heroes': [], 'enemy_heroes': [], 'players': []} for k, v in matches.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids:
                    match_summary[match_id]['our_heroes'].append(p['hero_id'])
                    match_summary[match_id]['players'].append(p['account_id'])
                    match_summary[match_id]['win'] = p['win'] > 0
                    match_summary[match_id]['is_radiant'] = p['isRadiant']
                    gold_adv = [] if obj['radiant_gold_adv'] is None else obj['radiant_gold_adv']                  
                    gold_adv = gold_adv if p['isRadiant'] else -1 * gold_adv
                    obj['comeback'] = -1 * min(gold_adv + [0]) if 'comeback' not in obj else obj['comeback']
                    obj['throw'] = max(gold_adv + [0]) if 'throw' not in obj else obj['throw']
                    match_summary[match_id]['comeback_throw'] = obj['comeback'] if p['win'] > 0 else obj['throw']   
            if 'lane_role' in obj['players'][0]:
                match_summary[match_id]['roles'] = Roles.evaluate_roles(match_summary[match_id], obj['players'])
            for p in obj['players']:
                if p['isRadiant'] != match_summary[match_id]['is_radiant']:
                    match_summary[match_id]['enemy_heroes'].append(p['hero_id'])

        print('')
        list_comebacks = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] > 0}
        list_throws = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] == 0}        
        for k, v in sorted(list_comebacks.items(), key=lambda e: e[1], reverse=True)[:10]:            
            print('%s came back from %s gold disadvantage in match id %i with team: %s'
                  % (self.team_name, v, k, [x for x, y in self.players.items() if y in match_summary[k]['players']]))
        self.top_comebacks = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_comebacks.items(), key=lambda e: e[1], reverse=True)[:10]]
        for k, v in sorted(list_throws.items(), key=lambda e: e[1], reverse=True)[:10]:            
            print('%s threw a %s gold advantage in match id %i with team: %s'
                  % (self.team_name, v, k, [x for x, y in self.players.items() if y in match_summary[k]['players']]))
        self.top_throws = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_throws.items(), key=lambda e: e[1], reverse=True)[:10]]

        print('')
        wr_versus = {k: {'matches': 0, 'wins': 0} for k, v in heroes.items()}
        for mid, v in match_summary.items():
            for enemy_hero in v['enemy_heroes']:
                wr_versus[enemy_hero]['matches'] += 1
                if v['win']:
                    wr_versus[enemy_hero]['wins'] += 1
        avg = {v: 0 if wr_versus[k]['matches'] == 0 else wr_versus[k]['wins'] / wr_versus[k]['matches']
               for k, v in heroes.items()}
        s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%.2f %% %s win rate versus %s (%i matches)'
                  % (100 * v, self.team_name, k, wr_versus[inv_h[k]]['matches']))
        self.against_heroes = [
            {'id': inv_h[k], 'name': k, 'matches': wr_versus[inv_h[k]]['matches'], 'wins': wr_versus[inv_h[k]]['wins'],
             'wr': '%.2f %%' % (100 * v)} for k, v in s]

        print('')
        wr_with = {k: {'matches': 0, 'wins': 0} for k, v in heroes.items()}
        for mid, v in match_summary.items():
            for ally_hero in v['our_heroes']:
                wr_with[ally_hero]['matches'] += 1
                if v['win']:
                    wr_with[ally_hero]['wins'] += 1
        avg = {v: 0 if wr_with[k]['matches'] == 0 else wr_with[k]['wins'] / wr_with[k]['matches']
               for k, v in heroes.items()}
        s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%.2f %% %s win rate playing %s (%i matches)'
                  % (100 * v, self.team_name, k, wr_with[inv_h[k]]['matches']))
        self.with_heroes = [
            {'id': inv_h[k], 'name': k, 'matches': wr_with[inv_h[k]]['matches'], 'wins': wr_with[inv_h[k]]['wins'],
             'wr': '%.2f %%' % (100 * v)} for k, v in s]

        print('')
        matches = {h: v['matches'] for h, v in wr_with.items()}
        s = sorted(matches.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%s played %s for a total of %i matches'
                  % (self.team_name, heroes[k], v))
        self.most_played_heroes = [{'id': k, 'name': heroes[k], 'matches': v} for k, v in s]

        print('')
        player_hero_in_match = dict()
        players_heroes = {i: {h: 0 for h, n in heroes.items()} for p, i in self.players.items()}
        for mid, v in match_summary.items():
            player_hero_in_match[mid] = dict()
            for ally_hero, player in zip(v['our_heroes'], v['players']):
                player_hero_in_match[mid][player] = ally_hero
                players_heroes[player][ally_hero] += 1        
        for p, i in self.players.items():
            pl = players_heroes[self.players[p]]
            m = max(pl.items(), key=operator.itemgetter(1))
            print("%s most played hero: %s (%i of %i matches)"
                  % (p, [heroes[x] for x in ([y for y in heroes.keys() if pl[y] == m[1]])], m[1], sum(pl.values())))

        print('')
        comp_matches = dict()
        comp_wins = dict()
        for mid, v in match_summary.items():
            if 'roles' in v:
                composition = v['roles']['composition']
                if composition not in comp_matches:
                    comp_matches[composition] = 0
                    comp_wins[composition] = 0
                comp_matches[composition] += 1
                if v['win']:
                    comp_wins[composition] += 1
        avg = {k: comp_wins[k] / comp_matches[k] for k, v in comp_matches.items()}
        s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('Composition: %s win rate: %.2f %% (%i matches)' % (k, v * 100, comp_matches[k]))

        print('')
        player_positions = {y: {r: 0 for i, r in Constants.roles().items()} for x, y in self.players.items()}
        player_win_pos = {y: {r: 0 for i, r in Constants.roles().items()} for x, y in self.players.items()}
        for mid, v in match_summary.items():
            if 'roles' in v:
                positions = v['roles']['positions']
                for pid, pos in positions.items():
                    player_positions[pid][pos] += 1
                    if v['win']:
                        player_win_pos[pid][pos] += 1
        for pid, v in player_positions.items():
            pp = player_positions[pid]
            acc = sum(pp.values())
            pp = {a: '%i (%.2f %%)' % (b, 0 if acc == 0 else 100 * b / acc) for a, b in pp.items()}
            print('%s positions: %s' % (inv_p[pid], pp))

        tier_dict = dict()
        for pos_id, pos_n in Constants.roles().items():
            avg = {k: player_win_pos[v][pos_n] / player_positions[v][pos_n] for k, v in self.players.items()
                   if player_positions[v][pos_n] >= min_couple_matches}
            s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
            tier_dict[pos_n] = list()
            for k, v in s:
                tier_dict[pos_n].append(TierItem(k, v * 100, '%s: %s\'s win rate: %.2f %% (%i matches)'
                                                 % (pos_n, k, v * 100, player_positions[self.players[k]][pos_n])))

        print('')
        couples_win = {b: {x: 0 for w, x in self.players.items()} for a, b in self.players.items()}
        couples_matches = {b: {x: 0 for w, x in self.players.items()} for a, b in self.players.items()}
        for mid, v in match_summary.items():
            for p1, pid1 in self.players.items():
                for p2, pid2 in self.players.items():
                    if pid1 in v['players'] and pid2 in v['players'] and pid1 != pid2:
                        couples_matches[pid1][pid2] += 1
                        if v['win']:
                            couples_win[pid1][pid2] += 1
        couples = {
            (inv_p[x[0]], inv_p[x[1]]):
                0 if couples_matches[x[0]][x[1]] == 0 else couples_win[x[0]][x[1]] / couples_matches[x[0]][x[1]]
                for x in list(itertools.combinations(self.players.values(), 2))
        }
        s = sorted(couples.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            if couples_matches[self.players[k[0]]][self.players[k[1]]] >= min_couple_matches:
                print('%.2f %% win rate for %s (%i wins in %i matches)'
                      % (100 * v, k, couples_win[self.players[k[0]]][self.players[k[1]]],
                         couples_matches[self.players[k[0]]][self.players[k[1]]]))

        return tier_dict

    def identify_teams(self, matches):
        account_ids = [v for k, v in self.players.items()]
        match_summary = {k: {'players': [], 'win': False} for k, v in matches.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids:
                    match_summary[match_id] = {'players': match_players, 'win': p['win'] > 0}
                    break

        print('')
        win_rate = 100 * len([x for x, y in match_summary.items() if y['win']]) / len(matches)
        print('%s Win Rate: %.2f %%' % (self.team_name, win_rate))
        return win_rate

    def stat_counter(self, matches, parameter, reverse=True, has_avg=True, unit=None,
                     text=None, has_max=True, tf=None, rule=None):
        text = parameter if text is None else text

        account_ids = [v for k, v in self.players.items()]
        inv_p = {v: k for k, v in self.players.items()}
        matches_played = {k: 0 for k, v in self.players.items()}

        averages = {k: 0 for k, v in self.players.items()}
        totals = {k: 0 for k, v in self.players.items()}

        maximum_value = {v: 0 for k, v in self.players.items()}
        maximum_match = {v: 0 for k, v in self.players.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:                
                if p['account_id'] in account_ids and (parameter in p and p[parameter] is not None):
                    if not inv_p[p['account_id']] in totals:
                        totals[inv_p[p['account_id']]] = 0
                        matches_played[inv_p[p['account_id']]] = 0
                    if rule == 'kla':
                        value = (p['kills'] + p['assists']) / (p['deaths'] + 1)
                    elif rule == 'beyond_godlike':
                        value = 0 if "10" not in p[parameter] else p[parameter]["10"]
                    elif rule == 'ward_kill':
                        value = p['observer_kills'] + p['sentry_kills']
                    elif rule == 'max_hit':
                        value = p[parameter]['value']
                    elif rule == 'accumulate':
                        value = sum([v for k, v in p[parameter].items()])
                    elif parameter == 'purchase':
                        if rule == 'support_gold':
                            pch = dict()
                            costs = Constants.item_cost()
                            lst = ['ward_observer', 'ward_sentry', 'dust', 'smoke_of_deceit', 'ward_dispenser', 'gem']
                            for i in lst:
                                pch[i] = p[parameter][i] if i in p[parameter] and p[parameter][i] is not None else 0
                            obs_gold = max(pch['ward_observer'], pch['ward_dispenser']) * costs['ward_observer']
                            sen_gold = max(pch['ward_sentry'], pch['ward_dispenser']) * costs['ward_sentry']
                            value = obs_gold + sen_gold + costs['dust'] * pch['dust'] + costs['gem'] * pch['gem']
                            value = value + costs['smoke_of_deceit'] * pch['smoke_of_deceit']
                        else:
                            value = (p[parameter][rule]
                                     if rule in p[parameter] and p[parameter][rule] is not None else 0)
                            value = value / 2 if rule == 'dust' else value
                    else:
                        value = p[parameter]
                    totals[inv_p[p['account_id']]] += value
                    if value > maximum_value[p['account_id']]:
                        maximum_value[p['account_id']] = value
                        maximum_match[p['account_id']] = match_id
                    matches_played[inv_p[p['account_id']]] += 1

        for name, pid in self.players.items():
            averages[name] = totals[name]/matches_played[name] if matches_played[name] > 0 else 0

        results_avg = []
        if has_avg:
            sorted_average = sorted(averages.items(), key=lambda kv: kv[1])
            if reverse:
                sorted_average.reverse()
            for name, value in sorted_average:
                if matches_played[name] >= self.min_matches:
                    txt = '%s has %i %s in %i matches (avg %.2f %s)' \
                            % (name, totals[name], text, matches_played[name], tf(averages[name]), unit)
                    results_avg.append(TierItem(name, tf(averages[name]), txt))
            if not has_max:
                return results_avg, None

        sorted_maximum = sorted(maximum_value.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_maximum.reverse()

        results_max = []
        for pid, value in sorted_maximum:
            if matches_played[inv_p[pid]] >= self.min_matches:
                txt = '%s: %i %s (match id: %i)' % (inv_p[pid], tf(maximum_value[pid]), unit, maximum_match[pid])
                results_max.append(TierItem(inv_p[pid], tf(maximum_value[pid]), txt))

        if not has_avg:
            return None, results_max

        return results_avg, results_max

    def get_matches(self, last_days=None, ranked_only=False):
        matches = dict()
        total_matches = {n: 0 for n, pid in self.players.items()}
        for name, pid in self.players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)            
            total_matches[name] = 0
            for o in obj:
                y = gmtime(int(o['start_time'])).tm_year                
                if ((last_days is not None and (calendar.timegm(gmtime()) - int(o['start_time'])) < last_days * 86400)
                        or (last_days is None and y in self.years)
                        and (not ranked_only or o['lobby_type'] in [5, 6, 7])):
                    total_matches[name] += 1
                    if not o['match_id'] in matches:
                        matches[o['match_id']] = []
                    matches[o['match_id']].append(name)
        for i in range(0, 5):
            self.matches_by_party_size.append(len({k: v for k, v in matches.items() if len(v) == i + 1}))
            print('Matches played by party of size %i: %s' % (i + 1, self.matches_by_party_size[i]))
        
        print('')                    
        sorted_matches = sorted(total_matches.items(), key=lambda kv: kv[1])
        sorted_matches.reverse()

        for name, match_count in sorted_matches:
            matches_with_team = len([i for i, v in matches.items() if len(v) >= self.min_party_size and name in v])
            percentage_with_team = matches_with_team / match_count if match_count > 0 else 0
            self.match_summary_by_player.append(
                {
                    'player': name,
                    'matches': match_count,
                    'team_matches': matches_with_team,
                    'perc_with_team': 100 * percentage_with_team
                })
            print('%s played %i matches -- %i matches (%.2f %%) played with %s'
                  % (name, match_count, matches_with_team, 100 * percentage_with_team, self.team_name))

        self.match_summary_by_team = sorted(self.match_summary_by_player, key=lambda v: v['team_matches'], reverse=True)
        return {k: v for k, v in matches.items() if len(v) >= self.min_party_size}
