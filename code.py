# coding=utf-8

import statistics
import json
import calendar
import operator
import itertools
import items
from time import gmtime
from tier import TierItem
from roles import Roles
from constants import *


class Parser:
    def __init__(self, team_name, years, players, min_matches, min_party_size):
        self.team_name = team_name
        self.years = years
        self.players = players
        self.heroes = {}
        self.win_rate = 0
        self.min_matches = min_matches
        self.min_party_size = min_party_size
        self.full_party_matches = 2
        self.matches_by_party_size = []
        self.match_summary = {}
        self.match_summary_by_player = []
        self.match_summary_by_team = []
        self.top_comebacks = []
        self.top_throws = []
        self.against_heroes = []
        self.with_heroes = []
        self.most_played_heroes = []
        self.compositions = []
        self.win_rate_by_weekday = {}
        self.win_rate_by_month = {}
        self.player_roles = {}
        self.player_heroes = {}
        self.player_wins_by_hero = {}
        self.player_pairs = {}
        self.player_couples = []
        self.five_player_compositions = []
        self.hero_statistics = []
        self.player_heroes_in_match = {}
        self.player_descriptor = []
        self.factions = {}

    @staticmethod
    def load_matches(unique_matches):
        matches = list()
        for match_id, _ in unique_matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            content = json.loads(content)
            matches.append({'id': match_id, 'content': content, 'date': content['start_time']})
        return sorted(matches, key=lambda e: e['date'])

    def evaluate_best_team_by_hero_player(self, min_matches):
        role_dict = {}
        result_dict = {}
        inv_p = {v: k for k, v in self.players.items()}
        for _, r in roles().items():
            role_dict[r] = list()
            for hero in self.hero_statistics:
                for p in hero['played_by']:
                    if p['roles'][r]['matches'] >= min_matches:
                        role_dict[r].append({'player': p['id'], 'hero': hero['id'], 'data': p['roles'][r]})
        for _, r in roles().items():
            s = sorted(role_dict[r], key=lambda e: e['data']['rating'], reverse=True)
            result_dict[r] = list()
            for i in range(min(5, len(s))):
                m = s[i]
                result_dict[r].append({'hero_id': m['hero'], 'hero_name': self.heroes[m['hero']],
                                       'rating': m['data']['rating'],
                                       'player_id': m['player'], 'player_name': inv_p[m['player']], 'role': r})
        return result_dict

    def evaluate_best_team_by_hero(self, min_matches):
        role_dict = {}
        result_dict = {}
        for _, r in roles().items():
            role_dict[r] = list()
        for hero in self.hero_statistics:
            for r in hero['roles']:
                rtg = rating(r['wins'], matches=r['matches'])
                if rtg > 0 and r['matches'] >= min_matches:
                    role_dict[r['role']].append({'hero': hero['id'], 'rating': rtg})
        for _, r in roles().items():
            s = sorted(role_dict[r], key=lambda e: e['rating'], reverse=True)
            result_dict[r] = list()
            for i in range(min(5, len(s))):
                m = s[i]
                result_dict[r].append({'hero_id': m['hero'], 'hero_name': self.heroes[m['hero']], 'rating': m['rating'],
                                       'role': r})
        return result_dict

    def generate_item_statistics(self):
        ret = []
        for item, name in items.item_list().items():
            counts = dict()
            for match_id, summary in self.match_summary.items():
                s = sum([k for p, k in summary['items'][item].items()])
                if s not in counts:
                    counts[s] = {'wins': 0, 'matches': 0, 'wr': 0.0}
                counts[s]['matches'] += 1
                if summary['win']:
                    counts[s]['wins'] += 1
            min_count = min(counts.keys())
            max_count = max(counts.keys())
            for i in range(min_count, max_count+1):
                if i not in counts:
                    counts[i] = {'wins': 0, 'matches': 0, 'wr': 0.0}
                else:
                    counts[i]['wr'] = 100 * counts[i]['wins'] / counts[i]['matches']
            ss = sorted(counts.items(), key=lambda e: e[0])
            ret.append({
                'item_name': name,
                'item_internal_name': item,
                'counts': [i[0] for i in ss],
                'wins': [i[1]['wins'] for i in ss],
                'matches': [i[1]['matches'] for i in ss],
                'losses': [i[1]['matches'] - i[1]['wins'] for i in ss],
                'wr': [i[1]['wr'] for i in ss]
            })
        return ret

    def identify_heroes(self, rep, matches, min_couple_matches=10):
        matches = {o['id']: o['content'] for o in matches}
        hs = open('data/heroes.json', 'r', encoding='utf-8').read()
        hs_json = json.loads(hs)
        self.heroes = {h['id']: h['localized_name'] for h in hs_json}
        inv_h = {h['localized_name']: h['id'] for h in hs_json}
        inv_p = {v: k for k, v in self.players.items()}
        account_ids = [v for k, v in self.players.items()]
        replacements = {v: k for k, v in rep.items()} if rep is not None else {}
        match_summary = {k: {'our_heroes': [],
                             'enemy_heroes': [],
                             'our_team_heroes': [],
                             'players': [],
                             'player_desc': {}} for k, v in matches.items()}
        self.win_rate_by_weekday = {i: {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in calendar.day_abbr}
        self.win_rate_by_month = {i: {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in calendar.month_abbr[1:]}
        for match_id, obj in matches.items():
            for p in obj['players']:
                if p['account_id'] in replacements:
                    p['account_id'] = self.players[replacements[p['account_id']]]
                if p['account_id'] in account_ids:
                    match_summary[match_id]['lobby_type'] = lobby_type()[obj['lobby_type']]
                    match_summary[match_id]['our_heroes'].append(p['hero_id'])
                    match_summary[match_id]['players'].append(p['account_id'])
                    match_summary[match_id]['player_desc'][p['account_id']] = {'hero': self.heroes[p['hero_id']],
                                                                               'total_gold': p['total_gold']}
                    match_summary[match_id]['win'] = p['win'] > 0
                    match_summary[match_id]['is_radiant'] = p['isRadiant']
                    gold_adv = [] if obj['radiant_gold_adv'] is None else obj['radiant_gold_adv']                  
                    gold_adv = gold_adv if p['isRadiant'] else -1 * gold_adv
                    obj['comeback'] = -1 * min(gold_adv + [0]) if 'comeback' not in obj else obj['comeback']
                    obj['throw'] = max(gold_adv + [0]) if 'throw' not in obj else obj['throw']
                    match_summary[match_id]['comeback_throw'] = obj['comeback'] if p['win'] > 0 else obj['throw']   
            if 'lane_role' in obj['players'][0]:
                match_summary[match_id]['roles'] = Roles.evaluate_roles(match_summary[match_id], obj['players'])
            match_summary[match_id]['items'] = items.evaluate_items([x for x in obj['players'] if
                                                                    x['account_id'] in account_ids])
            match_summary[match_id]['barracks'] = obj[
                'barracks_status_radiant' if match_summary[match_id]['is_radiant'] else 'barracks_status_dire']
            c_month = calendar.month_abbr[gmtime(int(obj['start_time'])).tm_mon]
            c_weekday = calendar.day_abbr[gmtime(int(obj['start_time'])).tm_wday]
            self.win_rate_by_weekday[c_weekday]['matches'] += 1
            self.win_rate_by_month[c_month]['matches'] += 1
            if match_summary[match_id]['win']:
                self.win_rate_by_weekday[c_weekday]['wins'] += 1
                self.win_rate_by_month[c_month]['wins'] += 1
            else:
                self.win_rate_by_weekday[c_weekday]['losses'] += 1
                self.win_rate_by_month[c_month]['losses'] += 1
            for p in obj['players']:
                if p['isRadiant'] != match_summary[match_id]['is_radiant']:
                    match_summary[match_id]['enemy_heroes'].append(p['hero_id'])
                else:
                    match_summary[match_id]['our_team_heroes'].append(self.heroes[p['hero_id']])
        for wd, o in self.win_rate_by_weekday.items():
            self.win_rate_by_weekday[wd]['wr'] = 100 * o['wins'] / o['matches'] if o['matches'] > 0 else 0
        for wd, o in self.win_rate_by_month.items():
            self.win_rate_by_month[wd]['wr'] = 100 * o['wins'] / o['matches'] if o['matches'] > 0 else 0
        self.match_summary = match_summary

        r_wins = sum([1 for mid, data in self.match_summary.items() if data['is_radiant'] and data['win']])
        r_matches = sum([1 for mid, data in self.match_summary.items() if data['is_radiant']])
        d_wins = sum([1 for mid, data in self.match_summary.items() if not data['is_radiant'] and data['win']])
        d_matches = sum([1 for mid, data in self.match_summary.items() if not data['is_radiant']])
        self.factions = {
            'r_wr': 100 * r_wins / r_matches,
            'r_win': r_wins,
            'r_loss': r_matches - r_wins,
            'd_wr': 100 * d_wins / d_matches,
            'd_win': d_wins,
            'd_loss': d_matches - d_wins,
        }

        print('')
        self.win_rate = 100 * len([x for x, y in match_summary.items() if y['win']]) / len(matches)
        print('%s Win Rate: %.2f %%' % (self.team_name, self.win_rate))

        list_comebacks = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] > 0}
        list_throws = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] == 0}
        self.top_comebacks = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_comebacks.items(), key=lambda e: e[1], reverse=True)[:10]]
        self.top_throws = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_throws.items(), key=lambda e: e[1], reverse=True)[:10]]

        wr_versus = {k: {'matches': 0, 'wins': 0} for k, v in self.heroes.items()}
        for mid, v in match_summary.items():
            for enemy_hero in v['enemy_heroes']:
                wr_versus[enemy_hero]['matches'] += 1
                if v['win']:
                    wr_versus[enemy_hero]['wins'] += 1
        avg = {v: 0 if wr_versus[k]['matches'] == 0 else wr_versus[k]['wins'] / wr_versus[k]['matches']
               for k, v in self.heroes.items()}
        s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        self.against_heroes = sorted([
            {'id': inv_h[k], 'name': k, 'matches': wr_versus[inv_h[k]]['matches'], 'wins': wr_versus[inv_h[k]]['wins'],
             'wr': 100 * v, 'rating': rating(wr_versus[inv_h[k]]['wins'], matches=wr_versus[inv_h[k]]['matches'])} for
            k, v in s], key=lambda z: (-z['rating'], -z['wr'], -z['wins'], z['matches']))

        wr_with = {k: {'matches': 0, 'wins': 0} for k, v in self.heroes.items()}
        for mid, v in match_summary.items():
            for ally_hero in v['our_heroes']:
                wr_with[ally_hero]['matches'] += 1
                if v['win']:
                    wr_with[ally_hero]['wins'] += 1
        avg = {v: 0 if wr_with[k]['matches'] == 0 else wr_with[k]['wins'] / wr_with[k]['matches']
               for k, v in self.heroes.items()}
        ss = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        self.with_heroes = sorted([
            {'id': inv_h[k], 'name': k, 'matches': wr_with[inv_h[k]]['matches'], 'wins': wr_with[inv_h[k]]['wins'],
             'wr': 100 * v, 'rating': rating(wr_with[inv_h[k]]['wins'], matches=wr_with[inv_h[k]]['matches'])} for k, v
            in ss], key=lambda z: (-z['rating'], -z['wr'], -z['wins'], z['matches']))

        matches = {h: v['matches'] for h, v in wr_with.items()}
        s = sorted(matches.items(), key=lambda e: e[1], reverse=True)
        self.most_played_heroes = [{'id': k, 'name': self.heroes[k], 'matches': v} for k, v in s]

        print('')
        player_hero_in_match = dict()
        players_heroes = {i: {h: 0 for h, n in self.heroes.items()} for p, i in self.players.items()}
        phd = {i: {h: {'wins': 0,
                       'matches': 0,
                       'wins_against': 0,
                       'matches_against': 0} for h, n in self.heroes.items()} for p, i in self.players.items()}
        for mid, v in match_summary.items():
            player_hero_in_match[mid] = dict()
            for ally_hero, player in zip(v['our_heroes'], v['players']):
                player_hero_in_match[mid][player] = ally_hero
                players_heroes[player][ally_hero] += 1
                phd[player][ally_hero]['matches'] += 1
                if v['win']:
                    phd[player][ally_hero]['wins'] += 1
            for player in v['players']:
                for enemy_hero in v['enemy_heroes']:
                    phd[player][enemy_hero]['matches_against'] += 1
                    if v['win']:
                        phd[player][enemy_hero]['wins_against'] += 1
        for p, _ in self.players.items():
            pl = players_heroes[self.players[p]]
            m = max(pl.items(), key=operator.itemgetter(1))
            print("%s most played hero: %s (%i of %i matches)"
                  % (p, [self.heroes[x] for x in ([y for y in self.heroes.keys() if pl[y] == m[1]])], m[1],
                     sum(pl.values())))
        self.player_heroes_in_match = player_hero_in_match
        self.player_heroes = players_heroes
        for pid, v in phd.items():
            for hid, s in v.items():
                phd[pid][hid]['rating'] = rating(phd[pid][hid]['wins'], matches=phd[pid][hid]['matches'])
                phd[pid][hid]['inv_rating'] = rating(phd[pid][hid]['matches_against'] - phd[pid][hid]['wins_against'],
                                                     matches=phd[pid][hid]['matches_against'])
        self.player_wins_by_hero = phd

        print('')
        five_player = dict()
        for mid, v in match_summary.items():
            if len(v['players']) == 5:
                comp_sum = sum(v['players'])
                if comp_sum not in five_player:
                    five_player[comp_sum] = {
                        'players': ', '.join([inv_p[i] for i in v['players']]),
                        'wins': 0,
                        'matches': 0
                    }
                five_player[comp_sum]['matches'] += 1
                if v['win']:
                    five_player[comp_sum]['wins'] += 1
        while True:
            avg = [{'key': k, 'wr': v['wins'] / v['matches'], 'matches': v['matches']} for k, v in five_player.items()
                   if
                   v['matches'] >= self.full_party_matches]
            if len(avg) <= 17:
                break
            else:
                self.full_party_matches += 1
        s = sorted(avg, key=lambda e: (e['wr'], e['matches']), reverse=True)
        for k in s:
            five_player[k['key']]['wr'] = k['wr'] * 100
            self.five_player_compositions.append(five_player[k['key']])
            print('5-player team: %s win rate: %.2f %% (%i matches)' % (
                   five_player[k['key']]['players'], k['wr'] * 100, k['matches']))

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
        self.compositions = [{'comp': k, 'matches': comp_matches[k], 'wins': comp_wins[k], 'wr': v * 100} for k, v in s]
        self.compositions = sorted(self.compositions, key=lambda e: e['matches'], reverse=True)

        print('')
        player_positions = {y: {r: 0 for i, r in roles().items()} for x, y in self.players.items()}
        player_win_pos = {y: {r: 0 for i, r in roles().items()} for x, y in self.players.items()}
        hero_positions = {k: {p: {'wins': 0, 'matches': 0} for i, p in roles().items()} for k, v in
                          self.heroes.items()}
        player_hero_position = {r: {(a, b): {'wins': 0, 'matches': 0}
                                for _, a in self.players.items() for b, _ in self.heroes.items()
                                    } for _, r in roles().items()}
        for mid, v in match_summary.items():
            if 'roles' in v:
                positions = v['roles']['positions']
                for pid, pos in positions.items():
                    player_positions[pid][pos] += 1
                    hero_positions[player_hero_in_match[mid][pid]][pos]['matches'] += 1
                    player_hero_position[pos][(pid, player_hero_in_match[mid][pid])]['matches'] += 1
                    if v['win']:
                        hero_positions[player_hero_in_match[mid][pid]][pos]['wins'] += 1
                        player_hero_position[pos][(pid, player_hero_in_match[mid][pid])]['wins'] += 1
                        player_win_pos[pid][pos] += 1
        for pid, v in player_positions.items():
            pp = player_positions[pid]
            ppp = {a: '%i (%.2f %%)' % (
                   b, 0 if player_positions[pid][a] == 0 else 100 * player_win_pos[pid][a] / player_positions[pid][a])
                   for a, b in pp.items()}
            print('%s positions: %s' % (inv_p[pid], ppp))
            self.player_roles[pid] = [
                {'role': a, 'matches': b,
                 'wr': 0 if player_positions[pid][a] == 0 else 100 * player_win_pos[pid][a] / player_positions[pid][a]}
                for a, b in player_positions[pid].items()]
        self.hero_statistics = sorted([{
            'name': hero_name,
            'id': inv_h[hero_name],
            'matches': wr_with[inv_h[hero_name]]['matches'],
            'roles': [{'role': r, 'matches': v['matches'], 'wins': v['wins'],
                       'wr': 0 if v['matches'] == 0 else 100 * v['wins'] / v['matches']} for r, v in
                      hero_positions[inv_h[hero_name]].items()],
            'played_by': sorted([{'name': p_name, 'id': pid, 'matches': phd[pid][inv_h[hero_name]]['matches'],
                                  'wins': phd[pid][inv_h[hero_name]]['wins'],
                                  'roles': {r: {'wins': player_hero_position[r][(pid, inv_h[hero_name])]['wins'],
                                                'matches': player_hero_position[r][(pid, inv_h[hero_name])]['matches'],
                                                'rating': rating(
                                                    player_hero_position[r][(pid, inv_h[hero_name])]['wins'],
                                                    matches=player_hero_position[r][(pid, inv_h[hero_name])][
                                                        'matches'])} for _, r in roles().items()},
                                  'rating': rating(phd[pid][inv_h[hero_name]]['wins'],
                                                   matches=phd[pid][inv_h[hero_name]]['matches']),
                                  'wr': (100 * phd[pid][inv_h[hero_name]]['wins'] / phd[pid][inv_h[hero_name]][
                                      'matches'] if phd[pid][inv_h[hero_name]]['matches'] > 0 else 0)}
                                 for p_name, pid in self.players.items() if phd[pid][inv_h[hero_name]]['matches'] > 0],
                                key=lambda z: (z['rating'], z['wins']), reverse=True)
        } for hero_name, value in ss], key=lambda l: l['name'])

        tier_dict = dict()
        for _, pos_n in roles().items():
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
            for _, pid1 in self.players.items():
                for _, pid2 in self.players.items():
                    if pid1 in v['players'] and pid2 in v['players'] and pid1 != pid2:
                        couples_matches[pid1][pid2] += 1
                        if v['win']:
                            couples_win[pid1][pid2] += 1
        couples = {
            (inv_p[x[0]], inv_p[x[1]]):
                0 if couples_matches[x[0]][x[1]] == 0 else couples_win[x[0]][x[1]] / couples_matches[x[0]][x[1]]
                for x in list(itertools.combinations(self.players.values(), 2))
        }
        for _, pid in self.players.items():
            self.player_pairs[pid] = []
        s = sorted(couples.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            if couples_matches[self.players[k[0]]][self.players[k[1]]] >= min_couple_matches:
                self.player_pairs[self.players[k[0]]].append(
                    {'name': k[1], 'wins': couples_win[self.players[k[0]]][self.players[k[1]]], 'wr': 100 * v,
                     'matches': couples_matches[self.players[k[0]]][self.players[k[1]]]})
                self.player_pairs[self.players[k[1]]].append(
                    {'name': k[0], 'wins': couples_win[self.players[k[0]]][self.players[k[1]]], 'wr': 100 * v,
                     'matches': couples_matches[self.players[k[0]]][self.players[k[1]]]})
                self.player_couples.append({'p1': self.players[k[0]], 'p2': self.players[k[1]], 'wr': 100 * v,
                                            'rating': rating(couples_win[self.players[k[0]]][self.players[k[1]]],
                                                             matches=couples_matches[self.players[k[0]]][
                                                                 self.players[k[1]]]),
                                            'wins': couples_win[self.players[k[0]]][self.players[k[1]]],
                                            'matches': couples_matches[self.players[k[0]]][self.players[k[1]]]})

        self.player_couples = sorted(self.player_couples, key=lambda e: e['rating'], reverse=True)

        self.player_descriptor = [
            {
                'name': player_name,
                'id': pid,
                'roles': self.player_roles[pid],
                'heroes': self.player_wins_by_hero[pid],
                'pairings': self.player_pairs[pid],
                'matches': sum([w['matches'] for h, w in self.player_wins_by_hero[pid].items()]),
                'streaks': Parser.calculate_streaks(pid, match_summary),
                'radiant_wr': 0 if len(
                    [1 for _, d in match_summary.items() if
                     pid in d['players'] and d['is_radiant']]) == 0 else 100 * len(
                    [1 for _, d in match_summary.items() if
                     pid in d['players'] and d['win'] and d['is_radiant']]) / len(
                    [1 for _, d in match_summary.items() if pid in d['players'] and d['is_radiant']]),
                'dire_wr': 0 if len([1 for _, d in match_summary.items() if
                                     pid in d['players'] and not d['is_radiant']]) == 0 else 100 * len(
                    [1 for _, d in match_summary.items() if
                     pid in d['players'] and d['win'] and not d['is_radiant']]) / len(
                    [1 for _, d in match_summary.items() if pid in d['players'] and not d['is_radiant']]),
                'wins': sum([w['wins'] for h, w in self.player_wins_by_hero[pid].items()]),
                'rating': rating(sum([w['wins'] for h, w in self.player_wins_by_hero[pid].items()]),
                                 matches=sum([w['matches'] for h, w in self.player_wins_by_hero[pid].items()])),
                'versatility': self.versatility([w['matches'] for h, w in self.player_wins_by_hero[pid].items()])
            } for player_name, pid in self.players.items()]
        return tier_dict

    def stat_counter(self, matches, parameter, reverse=True, has_avg=True, unit=None, max_fmt=None, avg_fmt=None,
                     text=None, has_max=True, tf=None, rule=None):
        matches = {o['id']: o['content'] for o in matches}
        text = parameter if text is None else text

        account_ids = [v for k, v in self.players.items()]
        inv_p = {v: k for k, v in self.players.items()}
        matches_played = {k: 0 for k, v in self.players.items()}

        averages = {k: 0 for k, v in self.players.items()}
        totals = {k: 0 for k, v in self.players.items()}

        maximum_value = {v: 0 for k, v in self.players.items()}
        maximum_match = {v: 0 for k, v in self.players.items()}

        for match_id, obj in matches.items():
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
                    elif rule == 'bool':
                        value = 1 if p[parameter] else 0
                    elif parameter == 'purchase':
                        if rule == 'support_gold':
                            pch = dict()
                            costs = item_cost()
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
                    vl = avg_fmt % tf(averages[name])
                    avg_block = ('(avg %s %s)' % (vl, unit)) if len(unit) > 0 else ('(avg %s)' % vl)
                    txt = '%s has %i %s in %i matches %s' % (name, totals[name], text, matches_played[name], avg_block)
                    results_avg.append(TierItem(name, vl, txt))
            if not has_max:
                return results_avg, None

        sorted_maximum = sorted(maximum_value.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_maximum.reverse()

        results_max = []
        for pid, value in sorted_maximum:
            if matches_played[inv_p[pid]] >= self.min_matches and maximum_match[pid] > 0:
                v = max_fmt % tf(maximum_value[pid])
                hero = self.heroes[self.player_heroes_in_match[maximum_match[pid]][pid]]
                txt = '%s: %s %s as %s (match id: %i)' % (inv_p[pid], v, unit, hero, maximum_match[pid])
                results_max.append(TierItem(inv_p[pid], tf(maximum_value[pid]), txt))

        if not has_avg:
            return None, results_max

        return results_avg, results_max

    def get_matches(self, replacement, month=None, last_days=None, ranked_only=False):
        matches = dict()
        total_matches = {n: 0 for n, pid in self.players.items()}
        for name, _ in self.players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)            
            total_matches[name] = 0
            for o in obj:
                m = gmtime(int(o['start_time'])).tm_mon
                y = gmtime(int(o['start_time'])).tm_year                
                if ((last_days is not None and (calendar.timegm(gmtime()) - int(o['start_time'])) < last_days * 86400)
                        or (last_days is None and month is not None and y in self.years and m == month)
                        or (last_days is None and month is None and y in self.years)
                        and (not ranked_only or o['lobby_type'] in [5, 6, 7])):
                    total_matches[name] += 1
                    if not o['match_id'] in matches:
                        matches[o['match_id']] = []
                    matches[o['match_id']].append(name)
        if replacement is not None:
            for name, _ in replacement.items():
                content = open('players/%s_matches_r.json' % name, 'r').read()
                obj = json.loads(content)
                if name not in total_matches:
                    total_matches[name] = 0
                for o in obj:
                    m = gmtime(int(o['start_time'])).tm_mon
                    y = gmtime(int(o['start_time'])).tm_year
                    if ((last_days is not None
                            and (calendar.timegm(gmtime()) - int(o['start_time'])) < last_days * 86400)
                            or (last_days is None and month is not None and y in self.years and m == month)
                            or (last_days is None and month is None and y in self.years)
                            and (not ranked_only or o['lobby_type'] in [5, 6, 7])):
                        total_matches[name] += 1
                        if not o['match_id'] in matches:
                            matches[o['match_id']] = []
                        matches[o['match_id']].append(name)
        for i in range(5):
            self.matches_by_party_size.append(len({k: v for k, v in matches.items() if len(v) == i + 1}))
            print('Matches played by party of size %i: %s' % (i + 1, self.matches_by_party_size[i]))
        
        print('')                    
        sorted_matches = sorted(total_matches.items(), key=lambda kv: kv[1])
        sorted_matches.reverse()

        for name, match_count in sorted_matches:
            matches_with_team = len([i for i, v in matches.items() if len(v) >= 2 and name in v])
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

    def player_versatility(self):
        inv_p = {v: k for k, v in self.players.items()}
        versatility_dict = dict()
        for pid, hero_dict in self.player_heroes.items():
            versatility = self.versatility([y for x, y in hero_dict.items()])
            if versatility > 0:
                versatility_dict[inv_p[pid]] = versatility
        s = sorted(versatility_dict.items(), key=lambda e: e[1], reverse=True)
        return [TierItem(k, v, '%s versatility: %.3f' % (k, v)) for k, v in s]

    def win_streak(self):
        return sorted([TierItem(p['name'], max(0, max(p['streaks'])),
                                '%s best win streak: %s matches' % (p['name'], max(0, max(p['streaks'])))) for p in
                       self.player_descriptor if len(p['streaks']) > 0 and p['matches'] > self.min_matches],
                      key=lambda e: e.score, reverse=True)

    def loss_streak(self):
        return sorted([TierItem(p['name'], abs(min(0, min(p['streaks']))),
                                '%s worst loss streak: %s matches' % (p['name'], abs(min(0, min(p['streaks']))))) for p
                       in self.player_descriptor if len(p['streaks']) > 0 and p['matches'] > self.min_matches],
                      key=lambda e: e.score)

    def versatility(self, values):
        count = len([x for x in values if x > 0])
        h_sum = sum([x for x in values if x > 0])
        if count == 0 or h_sum < self.min_matches:
            return 0
        matches_factor = 1 - math.exp(-(count - 1) / 20)
        mean = statistics.mean(values)
        norm = statistics.stdev(values) / mean
        variance_factor = math.exp(-norm / 2)
        return math.sqrt(matches_factor * variance_factor)

    @staticmethod
    def calculate_streaks(pid, matches):
        streaks = list()
        streak = 0
        for mid, data in matches.items():
            if pid in data['players']:
                if streak == 0:
                    streak += 1 if data['win'] else -1
                elif streak > 0:
                    if data['win']:
                        streak += 1
                    else:
                        streaks.append(streak)
                        streak = -1
                elif streak < 0:
                    if data['win']:
                        streaks.append(streak)
                        streak = 1
                    else:
                        streak -= 1
        if streak != 0:
            streaks.append(streak)
        return streaks
