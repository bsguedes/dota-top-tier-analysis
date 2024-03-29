# coding=utf-8

import statistics
import json
import calendar
import operator
import itertools
import items
import time
from time import gmtime
from tier import TierItem
from roles import Roles
from constants import *
from datetime import timedelta, date
from fantasy_data import FantasyData
import csv


def daterange(start_date, end_date):
    for n in range(0, int((end_date - start_date).days) + 1, 7):
        yield start_date + timedelta(n)


class Parser:
    def __init__(self, team_name, years, month, players, min_matches, min_party_size, min_matches_with_hero):
        self.team_name = team_name
        self.years = years
        self.month = month
        self.players = players
        self.heroes = {}
        self.inv_p = {v: k for k, v in self.players.items()}
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
        self.top_fast_wins = []
        self.top_fast_losses = []
        self.longest_matches = []
        self.against_heroes = []
        self.with_heroes = []
        self.most_played_heroes = []
        self.compositions = []
        self.win_rate_by_hour = {}
        self.win_rate_by_weekday = {}
        self.win_rate_length_hist = [{
            'duration': s,
            'wins': 0,
            'losses': 0
        } for s in ['20-', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65+']]
        self.win_rate_by_month = {}
        self.player_roles = {}
        self.player_heroes = {}
        self.player_wins_by_hero = {}
        self.player_pairs = {}
        self.player_couples = []
        self.trios = []
        self.five_player_compositions = []
        self.hero_statistics = []
        self.player_heroes_in_match = {}
        self.player_descriptor = []
        self.factions = {}
        self.match_types = []
        self.match_skill = []
        self.min_matches_with_hero = min_matches_with_hero
        self.rivals = []
        self.lane_partners = []
        self.hero_lane_partners = []
        self.hero_player_couples = []
        self.hero_spammers = []
        self.gold_variance = [[] for _ in range(180)]
        self.xp_variance = [[] for _ in range(180)]

    @staticmethod
    def load_matches(unique_matches):
        matches = list()
        for match_id, player_list in unique_matches.items():
            if int(match_id) - match_id == 0:
                with open('matches/%i.json' % match_id, 'r', encoding='utf-8') as f:
                    content = Parser.clear_content(json.loads(f.read()))
                    if all(p['hero_id'] is not None and p['hero_id'] > 0 for p in content['players']):
                        matches.append({'id': match_id, 'content': content, 'date': fix_time(content['start_time'])})
            else:
                with open('matches/%i.json' % int(match_id), 'r', encoding='utf-8') as f:
                    content = Parser.clear_content(json.loads(f.read()))
                    if all(p['hero_id'] is not None and p['hero_id'] > 0 for p in content['players']):
                        team_is_radiant = player_list[0][1]
                        for player in content['players']:
                            if (not player['isRadiant'] and team_is_radiant) or \
                                    (not team_is_radiant and player['isRadiant']):
                                player['account_id'] *= 10
                        matches.append({'id': match_id, 'content': content, 'date': fix_time(content['start_time'])})
        return sorted(matches, key=lambda e: e['date'])

    @staticmethod
    def clear_content(content):
        content['chat'] = None
        content['cosmetics'] = None
        content['draft_timings'] = None
        content['objectives'] = None
        content['picks_bans'] = None
        content['all_word_counts'] = None
        content['my_word_counts'] = None
        content['replay_url'] = None
        for player in content['players']:
            player['ability_targets'] = None
            player['ability_upgrades_arr'] = None
            player['ability_uses'] = None
            player['actions'] = None
            player['benchmarks'] = None
            player['buyback_log'] = None
            player['connection_log'] = None
            player['damage'] = None
            player['damage_inflictor'] = None
            player['damage_inflictor_received'] = None
            player['damage_targets'] = None
            player['gold_reasons'] = None
            player['hero_hits'] = None
            player['killed'] = None
            player['killed_by'] = None
            player['kills_log'] = None
            player['lane_pos'] = None
            player['max_hero_hit'] = None
            player['cosmetics'] = None
            player['permanent_buffs'] = None
            player['xp_reasons'] = None
            player['objectives'] = None
            player['first_purchase_time'] = None
            player['item_win'] = None
            player['item_usage'] = None
            player['teamfights'] = None
            player['times'] = None
            player['sen_left_log'] = None
            player['sen_log'] = None
            player['sen'] = None
            player['obs_left_log'] = None
            player['obs_log'] = None
            player['obs'] = None
        return content

    def bounties(self):
        lst = list()
        for i in range(5):
            r = dict()
            r['counts'] = i
            r['matches'] = len([1 for x, y in self.match_summary.items() if y['first_bounties'] == i])
            r['wins'] = len([1 for x, y in self.match_summary.items() if y['first_bounties'] == i and y['win']])
            r['losses'] = r['matches'] - r['wins']
            r['wr'] = win_rate(r['wins'], matches=r['matches'])
            lst.append(r)
        return lst

    def heroes_role_for_player(self, player_id):
        role_summary = {r: [] for _, r in roles().items()}
        for hero_desc in self.hero_statistics:
            for player_desc in hero_desc['played_by']:
                if player_desc['id'] == player_id:
                    for role, role_desc in player_desc['roles'].items():
                        if role_desc['matches'] >= self.min_matches_with_hero:
                            role_summary[role].append({
                                'hero_name': hero_desc['name'],
                                'hero_id': hero_desc['id'],
                                'details': role_desc
                            })
        for role, data in role_summary.items():
            role_summary[role] = sorted(data, key=lambda e: -e['details']['rating'])
        return role_summary

    def first_blood_win_rate(self):
        first_bloods = len([1 for x, y in self.match_summary.items() if y['first_blood']])
        matches = len([1 for x, y in self.match_summary.items() if y['first_blood'] is not None])
        win_fb = len([1 for x, y in self.match_summary.items() if y['first_blood'] and y['win']])
        win_nfb = len([1 for x, y in self.match_summary.items() if not y['first_blood'] and y['win']])
        return {
            'first_blood_rate': win_rate(first_bloods, matches),
            'first_bloods': first_bloods,
            'matches': matches,
            'wr_if_first_blood': win_rate(win_fb, first_bloods),
            'wr_if_not_first_blood': win_rate(win_nfb, matches - first_bloods),
            'wins_if_first_blood': win_fb,
            'wins_if_no_first_blood': win_nfb
        }

    def evaluate_best_team_by_hero_player(self, min_matches, is_best):
        role_dict = {}
        result_dict = {}
        inv_p = {v: k for k, v in self.players.items()}
        for _, r in roles().items():
            role_dict[r] = list()
            for hero in self.hero_statistics:
                for p in hero['played_by']:
                    if p['roles'][r]['matches'] >= min_matches:
                        role_dict[r].append({'player': p['id'], 'hero': hero['id'], 'data': p['roles'][r]})
        fact = -1 if is_best else 1
        for _, r in roles().items():
            s = sorted(role_dict[r], key=lambda e: (fact * e['data']['rating'], fact * e['data']['matches']))
            result_dict[r] = list()
            for i in range(min(5, len(s))):
                m = s[i]
                if m['data']['rating'] > 0 or not is_best:
                    result_dict[r].append({'hero_id': m['hero'], 'hero_name': self.heroes[m['hero']],
                                           'rating': m['data']['rating'],
                                           'player_id': m['player'], 'player_name': inv_p[m['player']], 'role': r})
        return result_dict

    def evaluate_best_team_by_player(self, min_matches, is_best):
        role_dict = {}
        result_dict = {}
        for _, r in roles().items():
            role_dict[r] = list()
        for pid, role_desc in self.player_roles.items():
            for r in role_desc:
                rtg = r['rating']
                if (rtg > 0 or not is_best) and r['matches'] >= min_matches:
                    role_dict[r['role']].append({'player_id': pid, 'rating': rtg, 'matches': r['matches']})
        fact = -1 if is_best else 1
        for _, r in roles().items():
            s = sorted(role_dict[r], key=lambda e: (fact * e['rating'], fact * e['matches']))
            result_dict[r] = list()
            for i in range(min(5, len(s))):
                m = s[i]
                result_dict[r].append({'player_id': m['player_id'], 'player_name': self.inv_p[m['player_id']],
                                       'rating': m['rating'],
                                       'role': r})
        return result_dict

    def evaluate_best_team_by_hero(self, min_matches, is_best):
        role_dict = {}
        result_dict = {}
        for _, r in roles().items():
            role_dict[r] = list()
        for hero in self.hero_statistics:
            for r in hero['roles']:
                rtg = rating(r['wins'], matches=r['matches'])
                if (rtg > 0 or not is_best) and r['matches'] >= min_matches:
                    role_dict[r['role']].append({'hero': hero['id'], 'rating': rtg, 'matches': r['matches']})
        fact = -1 if is_best else 1
        for _, r in roles().items():
            s = sorted(role_dict[r], key=lambda e: (fact * e['rating'], fact * e['matches']))
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
                if summary['items'] is not None:
                    s = sum([k['count'] for p, k in summary['items'][item].items()])
                    if s not in counts:
                        counts[s] = {'wins': 0, 'matches': 0, 'wr': 0.0}
                    counts[s]['matches'] += 1
                    if summary['win']:
                        counts[s]['wins'] += 1
            min_count = min(counts.keys())
            max_count = max(counts.keys())
            for i in range(min_count, max_count + 1):
                if i not in counts:
                    counts[i] = {'wins': 0, 'matches': 0, 'wr': 0.0}
                else:
                    counts[i]['wr'] = win_rate(counts[i]['wins'], counts[i]['matches'])
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

    def identify_heroes(self, rep, matches, forced_replacements, min_couple_matches=10):
        matches = {o['id']: o['content'] for o in matches}
        hs = open('data/heroes.json', 'r', encoding='utf-8').read()
        hs_json = json.loads(hs)
        self.heroes = {h['id']: h['localized_name'] for h in hs_json}
        inv_h = {h['localized_name']: h['id'] for h in hs_json}
        inv_p = {v: k for k, v in self.players.items()}
        account_ids = [v for k, v in self.players.items()]
        mmr_var = {}
        rivals_names = {}
        replacements = {}
        lane_players = {}
        lane_heroes = {}
        if rep is not None:
            for k, v_l in rep.items():
                for v in v_l:
                    replacements[v] = k
        match_summary = {k: {'our_heroes': [],
                             'enemy_heroes': [],
                             'rivals': [],
                             'our_team_heroes': [],
                             'players': [],
                             'our_ranks': [],
                             'enemy_ranks': [],
                             'match_id': v['match_id'],
                             'player_desc': {}} for k, v in matches.items()}
        self.win_rate_by_hour = {str(i): {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in range(24)}
        self.win_rate_by_weekday = {i: {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in calendar.day_abbr}
        self.win_rate_by_month = {i: {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in calendar.month_abbr[1:]}

        start_dt = date(2015, 1, 4)
        end_dt = date(2020, 12, 31)
        file = []
        line = []
        for dt in daterange(start_dt, end_dt):
            line.append(str(dt))
        file.append(line)
        chart_csv = {}
        for name, v in self.players.items():
            chart_csv[v] = {dt: 0 for dt in line}

        for match_id, obj in matches.items():
            if any(p['hero_id'] == 0 for p in obj['players']):
                continue
            team_fight_index = -1
            for p in obj['players']:
                team_fight_index += 1
                if p['account_id'] in replacements:
                    if match_id in forced_replacements:
                        if p['account_id'] in forced_replacements[match_id]:
                            p['account_id'] = self.players[forced_replacements[match_id][p['account_id']]]
                    if p['account_id'] in replacements:
                        if not self.players[replacements[p['account_id']]] in [e['account_id'] for e in obj['players']]:
                            p['account_id'] = self.players[replacements[p['account_id']]]
                        else:
                            p['account_id'] += 1
                if p['account_id'] in account_ids:
                    match_summary[match_id]['lobby_type'] = lobby_type()[obj['lobby_type']]
                    match_summary[match_id]['skill'] = obj['skill']
                    match_summary[match_id]['game_mode'] = game_mode()[obj['game_mode']]
                    match_summary[match_id]['our_heroes'].append(p['hero_id'])
                    match_summary[match_id]['players'].append(p['account_id'])
                    if 'rank_tier' in p and p['rank_tier'] is not None:
                        match_summary[match_id]['our_ranks'].append(p['rank_tier'])
                    apm = p['actions_per_min'] if 'actions_per_min' in p else 0
                    runes = p['runes'] if 'runes' in p else []
                    if 'teamfights' not in obj or obj['teamfights'] is None \
                            or len(obj['teamfights']) == 0 or len(obj['players']) != 10:
                        p['tf_max_damage'] = 0
                        p['tf_max_healing'] = 0
                    else:
                        p['tf_max_damage'] = max(
                            [tf['players'][team_fight_index]['damage'] for tf in obj['teamfights']])
                        p['tf_max_healing'] = max(
                            [tf['players'][team_fight_index]['healing'] for tf in obj['teamfights']])
                    match_summary[match_id]['player_desc'][p['account_id']] = {'hero': self.heroes[p['hero_id']],
                                                                               'total_gold': p['total_gold'],
                                                                               'kills': p['kills'],
                                                                               'deaths': p['deaths'],
                                                                               'runes': runes,
                                                                               'apm': apm}
                    match_summary[match_id]['win'] = p['win'] > 0

                    if obj['lobby_type'] in [5, 6, 7]:
                        if p['account_id'] not in mmr_var:
                            mmr_var[p['account_id']] = 0
                        mmr_var[p['account_id']] += 20 if match_summary[match_id]['win'] else -20

                    match_summary[match_id]['start_time'] = obj['start_time']
                    match_summary[match_id]['is_radiant'] = p['isRadiant']
                    gold_adv = [] if obj['radiant_gold_adv'] is None else obj['radiant_gold_adv']
                    gold_adv = gold_adv if p['isRadiant'] else -1 * gold_adv
                    obj['comeback'] = -1 * min(gold_adv + [0]) if 'comeback' not in obj else obj['comeback']
                    obj['throw'] = max(gold_adv + [0]) if 'throw' not in obj else obj['throw']
                    match_summary[match_id]['comeback_throw'] = obj['comeback'] if p['win'] > 0 else obj['throw']
                    match_summary[match_id]['our_gold_lead'] = []
                    match_summary[match_id]['party_size'] = len([x for x, y in self.players.items()
                                                                 if y in match_summary[match_id]['players']])
                    gold_radiant = [p['gold_t'] for p in obj['players'][0:5]]
                    gold_dire = [p['gold_t'] for p in obj['players'][5:]]
                    if not any(g is None for g in gold_radiant):
                        if match_summary[match_id]['is_radiant']:
                            our_gold = [sum(x) for x in zip(*gold_radiant)]
                            their_gold = [sum(x) for x in zip(*gold_dire)]
                        else:
                            our_gold = [sum(x) for x in zip(*gold_dire)]
                            their_gold = [sum(x) for x in zip(*gold_radiant)]
                        gold_idx = 0
                        for our, their in zip(our_gold, their_gold):
                            self.gold_variance[gold_idx].append(our / their - 1 if their != 0 else 0)
                            gold_idx += 1
                    xp_radiant = [p['xp_t'] for p in obj['players'][0:5]]
                    xp_dire = [p['xp_t'] for p in obj['players'][5:]]
                    if not any(g is None for g in xp_radiant):
                        if match_summary[match_id]['is_radiant']:
                            our_xp = [sum(x) for x in zip(*xp_radiant)]
                            their_xp = [sum(x) for x in zip(*xp_dire)]
                        else:
                            our_xp = [sum(x) for x in zip(*xp_dire)]
                            their_xp = [sum(x) for x in zip(*xp_radiant)]
                        xp_idx = 0
                        for our, their in zip(our_xp, their_xp):
                            self.xp_variance[xp_idx].append(our / their - 1 if their != 0 else 0)
                            xp_idx += 1

            if 'lane_role' in obj['players'][0]:
                match_summary[match_id]['roles'] = Roles.evaluate_roles(match_summary[match_id],
                                                                        [x for x in obj['players'] if 'lane_role' in x])
                for lane in match_summary[match_id]['roles']['partners']:
                    if all(p in account_ids for p in lane):
                        lane_string = ', '.join([inv_p[p] for p in lane])
                        if lane_string not in lane_players:
                            lane_players[lane_string] = {'lane': lane_string, 'matches': 0, 'wins': 0,
                                                         'rating': 0, 'losses': 0, 'wr': 0}
                        lane_players[lane_string]['matches'] += 1
                        if match_summary[match_id]['win']:
                            lane_players[lane_string]['wins'] += 1
                        else:
                            lane_players[lane_string]['losses'] += 1
            match_summary[match_id]['has_abandon'] = sum([o['abandons'] for o in obj['players']]) > 0
            match_summary[match_id]['duration'] = obj['duration']
            duration_index = min(len(self.win_rate_length_hist) - 1, max(0, int((obj['duration'] / 60) / 5) - 4))
            if match_summary[match_id]['win']:
                self.win_rate_length_hist[duration_index]['wins'] += 1
            else:
                self.win_rate_length_hist[duration_index]['losses'] += 1
            match_summary[match_id]['items'] = items.evaluate_items([x for x in obj['players'] if
                                                                     x['account_id'] in account_ids])
            match_summary[match_id]['barracks'] = obj[
                'barracks_status_radiant' if match_summary[match_id]['is_radiant'] else 'barracks_status_dire']
            match_summary[match_id]['towers'] = obj[
                'tower_status_radiant' if match_summary[match_id]['is_radiant'] else 'tower_status_dire']
            match_summary[match_id]['first_blood'] = Roles.got_first_blood(obj['players'],
                                                                           match_summary[match_id]['players'])
            match_summary[match_id]['first_bounties'] = Roles.first_bounties(obj['players'],
                                                                             match_summary[match_id]['players'])
            match_summary[match_id]['multi_kills'] = {}
            for p in match_summary[match_id]['players']:
                po = [o for o in obj['players'] if o['account_id'] == p][0]
                match_summary[match_id]['multi_kills'][p] = po['multi_kills'] if 'multi_kills' in po and po[
                    'multi_kills'] is not None else {}
            tm = gmtime(int(fix_time(obj['start_time'])))
            c_month = calendar.month_abbr[tm.tm_mon]
            c_weekday = calendar.day_abbr[tm.tm_wday]
            c_hour = str(tm.tm_hour)
            dt = date(tm.tm_year, tm.tm_mon, tm.tm_mday)
            for threshold_date in line:
                if threshold_date > str(dt):
                    for player in match_summary[match_id]['players']:
                        chart_csv[player][threshold_date] += 1
                    break
            self.win_rate_by_hour[c_hour]['matches'] += 1
            self.win_rate_by_weekday[c_weekday]['matches'] += 1
            self.win_rate_by_month[c_month]['matches'] += 1
            if match_summary[match_id]['win']:
                self.win_rate_by_hour[c_hour]['wins'] += 1
                self.win_rate_by_weekday[c_weekday]['wins'] += 1
                self.win_rate_by_month[c_month]['wins'] += 1
            else:
                self.win_rate_by_hour[c_hour]['losses'] += 1
                self.win_rate_by_weekday[c_weekday]['losses'] += 1
                self.win_rate_by_month[c_month]['losses'] += 1
            for p in [x for x in obj['players'] if x['hero_id'] is not None]:
                if p['isRadiant'] != match_summary[match_id]['is_radiant']:
                    match_summary[match_id]['enemy_heroes'].append(p['hero_id'])
                    if p['account_id'] is not None:
                        match_summary[match_id]['rivals'].append(p['account_id'])
                        if 'rank_tier' in p and p['rank_tier'] is not None:
                            match_summary[match_id]['enemy_ranks'].append(p['rank_tier'])
                        if p['account_id'] not in rivals_names:
                            rivals_names[p['account_id']] = []
                        if 'personaname' in p:
                            rivals_names[p['account_id']].append(p['personaname'])
                else:
                    match_summary[match_id]['our_team_heroes'].append(self.heroes[p['hero_id']])
        for wd, o in self.win_rate_by_weekday.items():
            self.win_rate_by_weekday[wd]['wr'] = win_rate(o['wins'], o['matches'])
        for wd, o in self.win_rate_by_month.items():
            self.win_rate_by_month[wd]['wr'] = win_rate(o['wins'], o['matches'])
        for wd, o in self.win_rate_by_hour.items():
            self.win_rate_by_hour[wd]['wr'] = win_rate(o['wins'], o['matches'])
        for skill in range(1, 4):
            m = [y for x, y in match_summary.items() if 'skill' in y and y['skill'] == skill]
            games = len(m)
            wins = len([x for x in m if x['win']])
            if games > 0:
                self.match_skill.append({
                    'skill': [None, 'Normal Skill', 'High Skill', 'Very High Skill'][skill],
                    'wins': wins,
                    'matches': games,
                    'wr': win_rate(wins, games),
                })
        for lobby, game in list(itertools.product(lobby_type(), game_mode())):
            m = [y for x, y in match_summary.items() if 'lobby_type' in y and y['lobby_type'] == lobby
                 and y['game_mode'] == game]
            games = len(m)
            wins = len([x for x in m if x['win']])
            if games > 0:
                self.match_types.append({
                    'lobby_type': '%s %s' % (match_types()[lobby], game),
                    'wins': wins,
                    'matches': games,
                    'wr': win_rate(wins, games),
                })
        self.match_summary = match_summary

        self.gold_variance = [sum(x) / len(x) if len(x) > 0 else 0 for x in self.gold_variance]
        while self.gold_variance[-1] == 0:
            self.gold_variance.pop(-1)

        self.xp_variance = [sum(x) / len(x) if len(x) > 0 else 0 for x in self.xp_variance]
        while self.xp_variance[-1] == 0:
            self.xp_variance.pop(-1)

        csv_file = [['Name', 'Image'] + line]
        for player, values in chart_csv.items():
            player_line = [inv_p[player], player]
            total = 0
            for _, count in values.items():
                total += count
                player_line.append(total)
            csv_file.append(player_line)
        print(csv_file)

        for lane, data in lane_players.items():
            data['rating'] = rating(data['wins'], data['losses'])
            data['wr'] = win_rate(data['wins'], data['matches'])
        self.lane_partners = sorted([v for _, v in lane_players.items() if v['matches'] >= self.min_matches / 2],
                                    key=lambda e: (-e['rating'], e['losses']))

        with open('chart.csv', mode='w') as file:
            employee_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_file:
                employee_writer.writerow(row)

        r_wins = sum([1 for mid, data in self.match_summary.items() if data['is_radiant'] and data['win']])
        r_matches = sum([1 for mid, data in self.match_summary.items() if data['is_radiant']])
        d_wins = sum([1 for mid, data in self.match_summary.items() if not data['is_radiant'] and data['win']])
        d_matches = sum([1 for mid, data in self.match_summary.items() if not data['is_radiant']])
        self.factions = {
            'r_wr': win_rate(r_wins, r_matches),
            'r_win': r_wins,
            'r_loss': r_matches - r_wins,
            'd_wr': win_rate(d_wins, d_matches),
            'd_win': d_wins,
            'd_loss': d_matches - d_wins,
        }

        print('')
        self.win_rate = win_rate(len([x for x, y in match_summary.items() if y['win']]), len(matches))
        print('%s Win Rate: %.2f %%' % (self.team_name, self.win_rate))

        list_comebacks = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] > 0
                          and v['party_size'] >= self.min_party_size}
        list_throws = {m: v['comeback_throw'] for m, v in match_summary.items() if v['win'] == 0
                       and v['party_size'] >= self.min_party_size}
        list_longest = {m: (v['duration'], v['win']) for m, v in match_summary.items()
                        if v['party_size'] >= self.min_party_size}
        list_fast_wins = {m: v['duration'] for m, v in match_summary.items() if v['win'] > 0 and not v['has_abandon']
                          and v['party_size'] >= self.min_party_size}
        list_fast_loss = {m: v['duration'] for m, v in match_summary.items() if v['win'] == 0 and not v['has_abandon']
                          and v['party_size'] >= self.min_party_size}
        self.top_comebacks = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_comebacks.items(), key=lambda e: e[1], reverse=True)[:15]]
        self.top_throws = [
            {'match': m, 'gold': g,
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_throws.items(), key=lambda e: e[1], reverse=True)[:15]]
        self.top_fast_wins = [
            {'match': m, 'time': (g // 60, g % 60),
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_fast_wins.items(), key=lambda e: e[1])[:15]]
        self.top_fast_losses = [
            {'match': m, 'time': (g // 60, g % 60),
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_fast_loss.items(), key=lambda e: e[1])[:15]]
        self.longest_matches = [
            {'match': m, 'time': (g[0] // 60, g[0] % 60), 'win': 'yes' if g[1] else 'no',
             'players': ', '.join([x for x, y in self.players.items() if y in match_summary[m]['players']])}
            for m, g in sorted(list_longest.items(), key=lambda e: e[1][0], reverse=True)[:15]]

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

        rivals = {}
        for mid, v in match_summary.items():
            if len(v['rivals']) > 0:
                for rival in v['rivals']:
                    if rival not in rivals:
                        rival_set = set(rivals_names[rival])
                        if len(rival_set) > 0:
                            rivals[rival] = {'id': rival, 'matches': 0, 'wins': 0, 'wr': 0,
                                             'name': max(rival_set, key=rivals_names[rival].count)}
                            rivals[rival]['matches'] += 1
                            if v['win']:
                                rivals[rival]['wins'] += 1
        for _, v in rivals.items():
            v['wr'] = win_rate(v['wins'], v['matches'])
        self.rivals = sorted([v for _, v in rivals.items() if v['matches'] > 1],
                             key=lambda e: (-e['matches'], -e['wins']))

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

                for partner in v['roles']['partners']:
                    if len(partner) == 2 and all(pid in inv_p for pid in partner):
                        heroes = sorted([player_hero_in_match[mid][pid] for pid in partner])
                        hero_lane_string = ', '.join([str(h) for h in heroes])
                        if hero_lane_string not in lane_heroes:
                            lane_heroes[hero_lane_string] = {
                                'hero_ids': heroes,
                                'hero_names': [self.heroes[h] for h in heroes],
                                'matches': 0,
                                'wins': 0,
                                'rating': 0,
                                'losses': 0,
                                'wr': 0
                            }
                        lane_heroes[hero_lane_string]['matches'] += 1
                        if match_summary[mid]['win']:
                            lane_heroes[hero_lane_string]['wins'] += 1
                        else:
                            lane_heroes[hero_lane_string]['losses'] += 1

        for heroes, data in lane_heroes.items():
            data['rating'] = rating(data['wins'], data['losses'])
            data['wr'] = win_rate(data['wins'], data['matches'])
        self.hero_lane_partners = sorted([v for _, v in lane_heroes.items()
                                          if v['matches'] >= self.min_matches_with_hero],
                                         key=lambda e: (-e['rating'], e['losses']))

        for pid, v in player_positions.items():
            pp = player_positions[pid]
            ppp = {a: '%i (%.2f %%)' % (
                b, win_rate(player_win_pos[pid][a], player_positions[pid][a]))
                   for a, b in pp.items()}
            print('%s positions: %s' % (inv_p[pid], ppp))
            self.player_roles[pid] = [
                {'role': a, 'matches': b, 'rating': rating(player_win_pos[pid][a], matches=b),
                 'wr': win_rate(player_win_pos[pid][a], player_positions[pid][a])}
                for a, b in player_positions[pid].items()]
        self.hero_statistics = sorted([{
            'name': hero_name,
            'id': inv_h[hero_name],
            'matches': wr_with[inv_h[hero_name]]['matches'],
            'roles': [{'role': r, 'matches': v['matches'], 'wins': v['wins'],
                       'wr': win_rate(v['wins'], v['matches'])} for r, v in
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
                                  'wr': win_rate(phd[pid][inv_h[hero_name]]['wins'],
                                                 phd[pid][inv_h[hero_name]]['matches'])}
                                 for p_name, pid in self.players.items() if phd[pid][inv_h[hero_name]]['matches'] > 0],
                                key=lambda z: (z['rating'], z['wins']), reverse=True)
        } for hero_name, value in ss], key=lambda l: l['name'])

        self.hero_player_couples = sorted([
            {
                'player_name': player['name'],
                'hero_name': hero['name'],
                'hero_id': hero['id'],
                'player_id': self.players[player['name']],
                'wins': player['wins'],
                'losses': player['matches'] - player['wins'],
                'rating': player['rating'],
                'wr': player['wr'],
                'matches': player['matches']
            } for hero in self.hero_statistics for player in hero['played_by']
            if player['matches'] >= self.min_matches_with_hero
        ], key=lambda e: -e['rating'])

        self.hero_spammers = sorted(self.hero_player_couples, key=lambda e: (-e['matches'], -e['rating']))

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
        trios = {}
        for match_id, v in match_summary.items():
            our_players = v['players']
            for comb in itertools.combinations(our_players, 3):
                c = ', '.join([inv_p[i] for i in sorted(comb)])
                if c not in trios:
                    trios[c] = {'matches': 0, 'wins': 0, 'wr': 0, 'rating': 0, 'players': c}
                trios[c]['matches'] += 1
                if v['win']:
                    trios[c]['wins'] += 1
        for x, y in trios.items():
            y['rating'] = rating(y['wins'], matches=y['matches'])
            y['wr'] = win_rate(y['wins'], matches=y['matches'])
        self.trios = sorted([y for _, y in trios.items() if y['matches'] >= min_couple_matches],
                            key=lambda e: (e['rating'], -e['matches']), reverse=True)

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
        self.player_couples = sorted(self.player_couples, key=lambda e: (e['rating'], -e['matches']), reverse=True)

        starting_mmr = 2000
        mmrs = {pid: starting_mmr for _, pid in self.players.items()}
        sorted_summaries = [match_summary[x] for x in sorted([m for m, _ in match_summary.items()])]
        for summary in sorted_summaries:
            our_rank = average_rank(summary['our_ranks'])
            enemy_rank = average_rank(summary['enemy_ranks'])
            if our_rank is not None and enemy_rank is not None:
                diff = mmr_diff(our_rank, enemy_rank) * 1 if summary['win'] else -1
                for player in summary['players']:
                    mmrs[player] += diff

        self.player_descriptor = [
            {
                'name': player_name,
                'id': pid,
                'roles': self.player_roles[pid],
                'heroes': self.player_wins_by_hero[pid],
                'top_heroes': self.calculate_top_heroes(pid),
                'pairings': self.player_pairs[pid],
                'matches': sum([w['matches'] for h, w in self.player_wins_by_hero[pid].items()]),
                'streaks': self.calculate_streaks(pid),
                'months': self.calculate_months(pid),
                'mmr': int(mmrs[pid]),
                'mmr_var': mmr_var[pid] if pid in mmr_var else "-",
                'radiant_wr': win_rate(
                    len([1 for _, d in match_summary.items() if pid in d['players'] and d['win'] and d['is_radiant']]),
                    len([1 for _, d in match_summary.items() if pid in d['players'] and d['is_radiant']])),
                'dire_wr': win_rate(len(
                    [1 for _, d in match_summary.items() if
                     pid in d['players'] and d['win'] and not d['is_radiant']]), len(
                    [1 for _, d in match_summary.items() if pid in d['players'] and not d['is_radiant']])),
                'wins': sum([w['wins'] for h, w in self.player_wins_by_hero[pid].items()]),
                'team_wins': len([1 for l, v in match_summary.items() if v['win']]),
                'team_matches': len([1 for l, v in match_summary.items()]),
                'rating': rating(sum([w['wins'] for h, w in self.player_wins_by_hero[pid].items()]),
                                 matches=sum([w['matches'] for h, w in self.player_wins_by_hero[pid].items()])),
                'versatility': self.versatility([w['matches'] for h, w in self.player_wins_by_hero[pid].items()])
            } for player_name, pid in self.players.items()]
        return tier_dict

    def stat_counter(self, matches, parameter, reverse=True, has_avg=True, unit=None, max_fmt=None, avg_fmt=None,
                     text=None, has_max=True, tf=None, rule=None, minimize=False):
        matches = {o['id']: o['content'] for o in matches}
        text = parameter if text is None else text

        account_ids = [v for k, v in self.players.items()]
        inv_p = {v: k for k, v in self.players.items()}
        matches_played = {k: 0 for k, v in self.players.items()}

        averages = {k: 0 for k, v in self.players.items()}
        totals = {k: 0 for k, v in self.players.items()}
        totals_per_role = {k: {r: 0 for r in role_list()} for k, _ in self.players.items()}
        matches_per_role = {k: {r: 0 for r in role_list()} for k, _ in self.players.items()}
        average_per_role = {k: {r: None for r in role_list()} for k, _ in self.players.items()}

        maximum_value = {v: 9999999999 for k, v in self.players.items()} \
            if not reverse and minimize else {v: 0 for k, v in self.players.items()}
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
                    elif rule == 'max_streak':
                        value = max([int(k) for k, v in p[parameter].items()]) if len(p[parameter]) > 0 else 0
                    elif parameter == 'multi_kills' or parameter == 'actions' or parameter == 'item_uses':
                        value = 0 if rule not in p[parameter] else p[parameter][rule]
                    elif rule == 'ward_kill':
                        value = p['observer_kills'] + p['sentry_kills']
                    elif rule == 'max_hit':
                        value = p[parameter]['value']
                    elif rule == 'accumulate':
                        value = sum([v for k, v in p[parameter].items()])
                    elif rule == 'bool':
                        value = 1 if p[parameter] else 0
                    elif rule == 'deaths_per_15min':
                        s = p['deaths']
                        fifteen_minutes = p['duration'] / 60 / 15
                        value = 1 if s / fifteen_minutes < 1 else 0
                    elif rule == 'time_kill_assist':
                        s = p['kills'] + p['assists']
                        value = 0 if s == 0 else p['duration'] / s
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
                        elif rule == 'utility_items':
                            amount = 0
                            lst = ['blink', 'spirit_vessel', 'crimson_guard', 'vladmir', 'ultimate_scepter',
                                   'shivas_guard', 'assault', 'guardian_greaves', 'solar_crest', 'lotus_orb',
                                   'helm_of_the_overlord', 'heavens_halberd', 'pipe']
                            for i in lst:
                                if i in p[parameter] and p[parameter][i] is not None:
                                    amount += 1
                            value = amount
                        elif rule == 'support_items':
                            amount = 0
                            lst = ['holy_locket', 'spirit_vessel', 'blink', 'glimmer_cape',
                                   'ultimate_scepter', 'force_staff', 'guardian_greaves', 'aether_lens']
                            for i in lst:
                                if i in p[parameter] and p[parameter][i] is not None:
                                    amount += 1
                            value = amount
                        else:
                            value = (p[parameter][rule]
                                     if rule in p[parameter] and p[parameter][rule] is not None else 0)
                            value = value / 2 if rule == 'dust' else value
                    else:
                        value = p[parameter]
                    totals[inv_p[p['account_id']]] += value
                    if 'roles' in self.match_summary[match_id]:
                        accs = [v for v, _ in self.match_summary[match_id]['roles']['positions'].items()]
                        if p['account_id'] in accs:
                            role = next(v for k, v in self.match_summary[match_id]['roles']['positions'].items()
                                        if k == p['account_id'])
                            totals_per_role[inv_p[p['account_id']]][role] += value
                            matches_per_role[inv_p[p['account_id']]][role] += 1
                    if not reverse and minimize:
                        if value < maximum_value[p['account_id']] and value != 0:
                            maximum_value[p['account_id']] = value
                            maximum_match[p['account_id']] = match_id
                    else:
                        if value > maximum_value[p['account_id']]:
                            maximum_value[p['account_id']] = value
                            maximum_match[p['account_id']] = match_id
                    matches_played[inv_p[p['account_id']]] += 1

        for name, pid in self.players.items():
            averages[name] = totals[name] / matches_played[name] if matches_played[name] > 0 else 0
            for role in role_list():
                average_per_role[name][role] = totals_per_role[name][role] / \
                                               matches_per_role[name][role] if \
                    matches_per_role[name][role] > self.min_matches_with_hero else None

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
                    results_avg.append(TierItem(name, vl, txt, tf(averages[name]),
                                                average_per_role[name], totals_per_role[name]))
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
                txt = '%s: %s %s as %s (match id: #%i#)' % (inv_p[pid], v, unit, hero, maximum_match[pid])
                results_max.append(TierItem(inv_p[pid], tf(maximum_value[pid]), txt))

        if not has_avg:
            return None, results_max

        return results_avg, results_max

    def get_matches(self, replacement, excluded, month=None, last_days=None, ranked_only=False):
        matches = dict()
        total_matches = {n: 0 for n, pid in self.players.items()}
        for name, _ in self.players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)
            total_matches[name] = 0
            for o in obj:
                m = gmtime(int(fix_time(o['start_time']))).tm_mon
                y = gmtime(int(fix_time(o['start_time']))).tm_year
                if ((last_days is not None
                     and (calendar.timegm(gmtime()) - fix_time(int(o['start_time']))) < last_days * 86400)
                        or (last_days is None and month is not None and y in self.years and m == month)
                        or (last_days is None and month is None and y in self.years)
                        and (not ranked_only or o['lobby_type'] in [5, 6, 7])):
                    total_matches[name] += 1
                    if not o['match_id'] in matches and not o['match_id'] in excluded:
                        matches[o['match_id']] = []
                    if not o['match_id'] in excluded:
                        matches[o['match_id']].append((name, o['player_slot'] < 100))
        if replacement is not None:
            for name, pid_array in replacement.items():
                i = 0
                for _ in pid_array:
                    i += 1
                    content = open('players/%s_matches_%i.json' % (name, i), 'r').read()
                    obj = json.loads(content)
                    if name not in total_matches:
                        total_matches[name] = 0
                    for o in obj:
                        m = gmtime(fix_time(int(o['start_time']))).tm_mon
                        y = gmtime(fix_time(int(o['start_time']))).tm_year
                        if ((last_days is not None
                             and (calendar.timegm(gmtime()) - fix_time(int(o['start_time']))) < last_days * 86400)
                                or (last_days is None and month is not None and y in self.years and m == month)
                                or (last_days is None and month is None and y in self.years)
                                and (not ranked_only or o['lobby_type'] in [5, 6, 7])):
                            total_matches[name] += 1
                            if not o['match_id'] in matches and not o['match_id'] in excluded:
                                matches[o['match_id']] = []
                            if not o['match_id'] in excluded:
                                matches[o['match_id']].append((name, o['player_slot'] < 100))

        duplicates = []
        split_matches = {}
        for match_id, players_list in matches.items():
            if len(players_list) > 5:
                radiant_team = [p for p in players_list if p[1]]
                dire_team = [p for p in players_list if not p[1]]
                if len(radiant_team) >= 2 and len(dire_team) >= 2:
                    split_matches[match_id + 0.1] = radiant_team
                    split_matches[match_id + 0.2] = dire_team
                    duplicates.append(match_id)
            else:
                if len(players_list) > len(set(x[0] for x in players_list)):
                    duplicates.append(match_id)
        for match in duplicates:
            matches.pop(match)
        for match_id, players_list in split_matches.items():
            matches[match_id] = players_list

        for i in range(5):
            self.matches_by_party_size.append(len({k: v for k, v in matches.items() if len(v) == i + 1}))
            print('Matches played by party of size %i: %s' % (i + 1, self.matches_by_party_size[i]))

        print('')
        sorted_matches = sorted(total_matches.items(), key=lambda kv: kv[1])
        sorted_matches.reverse()

        for name, match_count in sorted_matches:
            with_team = len([i for i, v in matches.items() if len(v) >= 2 and name in [x[0] for x in v]])
            with_party = len(
                [i for i, v in matches.items() if len(v) >= self.min_party_size and name in [x[0] for x in v]])
            percentage_with_team = with_team / match_count if match_count > 0 else 0
            self.match_summary_by_player.append(
                {
                    'player': name,
                    'matches': match_count,
                    'team_matches': with_team,
                    'perc_with_team': 100 * percentage_with_team,
                    'matches_party': with_party
                })
            print('%s played %i matches -- %i matches (%.2f %%) played with %s'
                  % (name, match_count, with_team, 100 * percentage_with_team, self.team_name))

        self.match_summary_by_team = sorted(self.match_summary_by_player, key=lambda v: v['team_matches'], reverse=True)
        return {k: v for k, v in matches.items() if
                self.min_party_size == 1 and len(v) == 1 or len(v) >= self.min_party_size}

    def best_team(self, players):
        print('')
        print('Best team analysis:')
        print('Players: ', sequence(players))
        start = time.time()
        players = [self.players[i] for i in players]
        inv_r = {v: k for k, v in roles().items()}
        player_hero_role_scores = {}
        for hid, _ in self.heroes.items():
            y = [x for x in self.hero_statistics if x['id'] == hid]
            if len(y) > 0:
                played_by = y[0]['played_by']
                for pid in players:
                    z = [x for x in played_by if x['id'] == pid]
                    if len(z) > 0:
                        player_hero = z[0]['roles']
                        for el in self.player_roles[pid]:
                            if player_hero[el['role']]['matches'] >= self.min_matches_with_hero:
                                player_hero_role_scores[(inv_r[el['role']], pid, hid)] = el['rating'] * \
                                                                                         player_hero[el['role']][
                                                                                             'rating']
                            else:
                                player_hero_role_scores[(inv_r[el['role']], pid, hid)] = 0
        print("Rating time %.2f seconds." % (time.time() - start))
        start = time.time()
        print("List of scores: ", len(player_hero_role_scores))
        player_hero_role_scores = {k: v for k, v in player_hero_role_scores.items() if v > 30}
        print("List of scores after filter: ", len(player_hero_role_scores))
        history = {}
        for p in players:
            for i, r in roles().items():
                history[(p, i)] = []
                for hid, _ in self.heroes.items():
                    c = (i, p, hid)
                    if c in player_hero_role_scores:
                        history[(p, i)].append((hid, player_hero_role_scores[c]))
        print("History time %.2f seconds." % (time.time() - start))
        start = time.time()
        combinations = []
        total_combinations = 0
        for composition in list(itertools.permutations(players, 5)):
            team = [[{
                'player': composition[role_index - 1],
                'role': role_index,
                'hero': hero
            } for hero in history[(composition[role_index - 1], role_index)]] for role_index, role in roles().items()]
            if any([len(member) == 0 for member in team]):
                continue
            for combination in itertools.product(*team):
                total_combinations += 1
                heroes = list(set([x['hero'][0] for x in combination]))
                if len(heroes) == 5:
                    s = sum([player['hero'][1] for player in combination]) / 5
                    if s > 40:
                        d = []
                        for player in combination:
                            r = player['role']
                            h = player['hero'][0]
                            p = player['player']
                            d.append((r, h, p))
                        combinations.append((s, d))
        print("Permutation time %.2f seconds." % (time.time() - start))
        print('Number of filtered combinations: %s' % len(combinations))
        print('Number of combinations: %s' % total_combinations)
        combinations.sort(reverse=True)
        heroes_resulted = [[x[1] for x in combinations[0][1]]]
        resulted = [combinations[0]]
        for i in range(len(combinations)):
            heroes = [x[1] for x in combinations[i][1]]
            append = True
            for j in range(len(resulted)):
                if len(set(heroes_resulted[j]) & set(heroes)) > 3:
                    append = False
                    break
            if append:
                resulted.append(combinations[i])
                heroes_resulted.append(heroes)
                if len(resulted) > 10:
                    break
        return resulted

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
                       self.player_descriptor if len(p['streaks']) > 0 and p['matches'] >= self.min_matches],
                      key=lambda e: e.score, reverse=True)

    def fantasy_value_tiers(self, fantasy_data):
        players = {}
        for item in fantasy_data:
            player_name = item['name']
            if player_name not in players:
                players[player_name] = 0
            players[player_name] += item['current_value']
        return sorted([TierItem(name, v, '%s fantasy cards are worth %d ƒ on PnKasino' % (name, v)) for
                       name, v in players.items()], key=lambda e: e.score, reverse=True)

    def coins_worth(self, fantasy_scores):
        player_names = [k for k, _ in self.players.items()]
        player_scores = {}
        for item in fantasy_scores:
            player_name = item['real_name']
            if player_name in player_names:
                player_scores[player_name] = item['worth']
        return sorted([TierItem(name, v, '%s\'s net worth on PnKasino is %d ₭' % (name, v)) for
                       name, v in player_scores.items()], key=lambda e: e.score, reverse=True)

    def achievements(self, fantasy_scores):
        player_names = [k for k, _ in self.players.items()]
        player_scores = {}
        for item in fantasy_scores:
            player_name = item['real_name']
            if player_name in player_names:
                player_scores[player_name] = item['achievements']
        return sorted([TierItem(name, v, '%s\'s hero pool size on PnKasino is %d heroes' % (name, v)) for
                       name, v in player_scores.items()], key=lambda e: e.score, reverse=True)

    def fantasy_worth(self, fantasy_scores):
        player_names = [k for k, _ in self.players.items()]
        player_scores = {}
        for item in fantasy_scores:
            player_name = item['real_name']
            if player_name in player_names:
                player_scores[player_name] = item['fcoins']
        return sorted([TierItem(name, v, '%s\'s net worth on PnKasino is %d ƒ' % (name, v)) for
                       name, v in player_scores.items()], key=lambda e: e.score, reverse=True)

    def discord(self, ids, data, avg=False):
        inv_id = {v: k for k, v in ids.items()}
        player_ids = [k for k, _ in inv_id.items()]
        entries = {}
        for item in data['results']:
            pid = int(item['player_id'])
            if pid in player_ids:
                if pid not in entries:
                    entries[pid] = 0
                year, month = map(lambda e: int(e), item['month_year'].split('-'))
                if year in self.years and (self.month is None or self.month == month):
                    entries[pid] += item['duration']
        valid_ids = [pid for name, pid in self.players.items() if name in [i for i, _ in ids.items()]]
        inv_p = {v: k for k, v in self.players.items()}
        if avg:
            durations = {v: 0 for k, v in self.players.items()}
            for mid, data in self.match_summary.items():
                for p in data['players']:
                    if p in valid_ids:
                        durations[p] += data['duration']
            return sorted([TierItem(inv_p[pid], entries[ids[inv_p[pid]]] / 10 / d,
                                    '%s spoke during %.2f %% of his time in matches' % (inv_p[pid],
                                                                                        entries[ids[inv_p[
                                                                                            pid]]] / 10 / d))
                           for pid, d in durations.items() if d > 0 and ids[inv_p[pid]] in entries],
                          key=lambda e: e.score)
        else:
            return sorted([TierItem(inv_id[pid], d / 60000,
                                    '%s spoke %d:%02d minutes on Discord' % (inv_id[pid],
                                                                             (d / 1000) // 60,
                                                                             (d / 1000) % 60)) for
                           pid, d in entries.items()],
                          key=lambda e: e.score, reverse=True)

    def loss_streak(self):
        return sorted([TierItem(p['name'], abs(min(0, min(p['streaks']))),
                                '%s worst loss streak: %s matches' % (p['name'], abs(min(0, min(p['streaks']))))) for p
                       in self.player_descriptor if len(p['streaks']) > 0 and p['matches'] >= self.min_matches],
                      key=lambda e: e.score)

    def mmr_change(self):
        mmr_list = []
        for player in self.player_descriptor:
            if player['mmr_var'] != '-':
                mmr_list.append({
                    'name': player['name'],
                    'mmr': player['mmr_var']
                })
        return sorted(mmr_list, key=lambda e: -e['mmr'])

    def versatility(self, values):
        ver_factor = 20
        count = len([x for x in values if x > 0])
        h_sum = sum([x for x in values if x > 0])
        if count == 0 or h_sum < self.min_matches / ver_factor:
            return 0
        matches_factor = 1 - math.exp(-(count - 1) / ver_factor)
        mean = statistics.mean(values)
        norm = statistics.stdev(values) / mean
        variance_factor = math.exp(-norm / 2)
        return math.sqrt(matches_factor * variance_factor)

    def calculate_top_heroes(self, pid):
        hero_ids = []
        for hero in self.hero_statistics:
            valid = [h for h in hero['played_by'] if h['matches'] >= self.min_matches_with_hero]
            if len(valid) > 0:
                max_rating = max(valid, key=lambda x: x['rating'])['rating']
                if max_rating > 0:
                    e = [h for h in hero['played_by'] if h['id'] == pid]
                    if len(e) == 1 and e[0]['rating'] == max_rating and e[0]['matches'] >= self.min_matches_with_hero:
                        hero_ids.append(hero['id'])
        return hero_ids

    def calculate_months(self, pid):
        matches = self.match_summary
        win_rate_by_month = {i: {'wins': 0, 'losses': 0, 'matches': 0, 'wr': 0} for i in calendar.month_abbr[1:]}
        for mid, data in matches.items():
            if pid in data['players']:
                c_month = calendar.month_abbr[gmtime(int(fix_time(data['start_time']))).tm_mon]
                win_rate_by_month[c_month]['matches'] += 1
                if data['win']:
                    win_rate_by_month[c_month]['wins'] += 1
                else:
                    win_rate_by_month[c_month]['losses'] += 1
        for i in calendar.month_abbr[1:]:
            win_rate_by_month[i]['wr'] = win_rate(win_rate_by_month[i]['wins'], win_rate_by_month[i]['matches'])
        return win_rate_by_month

    def role_summary(self):
        return [
            {
                'match_id': match_id,
                'players': [
                    {
                        'player_id': pid,
                        'position': position,
                        'hero_id': self.player_heroes_in_match[match_id][pid]
                    } for pid, position in match_data['roles']['positions'].items()],
                'win': match_data['win'],
                'duration': match_data['duration'],
                'lane': match_data['roles']['composition']
            } for match_id, match_data in self.match_summary.items() if 'roles' in match_data]

    def calculate_fantasy_score(self, fantasy_values, fantasy_scores, fantasy_data):
        inv_r = {v: k for k, v in roles().items()}
        for player_data in fantasy_scores:
            for position, data in player_data['team'].items():
                pos = position.replace('_', ' ')
                if data['card'] in fantasy_values and pos in fantasy_values[data['card']]:
                    data['points'] = fantasy_data.get_score_for_player(pos, data['card'])
                    if player_data['silver'] == inv_r[pos]:
                        p = roles()[player_data['silver']]
                        name = data['card']
                        ps = fantasy_values[name]['silver'][p] if p in fantasy_values[name]['silver'] else 0
                        data['points'] += ps
                    if player_data['gold'] == inv_r[pos]:
                        p = roles()[player_data['gold']]
                        name = data['card']
                        ps = fantasy_values[name]['gold'][p] if p in fantasy_values[name]['gold'] else 0
                        pss = fantasy_values[name]['silver'][p] if p in fantasy_values[name]['silver'] else 0
                        data['points'] += ps + pss
                else:
                    data['points'] = 0
            player_data['total_score'] = sum(t['points'] for p, t in player_data['team'].items())
            player_data['earnings'] = int(player_data['total_score'] ** 3) // 150 * 10
            player_data['bonus'] = 0
        ranking = sorted(fantasy_scores, key=lambda e: (-e['total_score'], e['cost']))
        bonus = [5000, 3000, 1500]
        for i in range(min(3, len(ranking))):
            ranking[i]['bonus'] = bonus[i]

        print('Monthly rewards')
        print(str({'rewards': [
            {
                'name': p['name'],
                'earnings': p['earnings'],
                'bonus': p['bonus']
            } for p in fantasy_scores]}).replace("'", "\""))
        return ranking

    def fantasy(self, tiers):
        tier_fantasy = {
            'Zé': {},
            'Chaos': {},
            'Nuvah': {},
            'Baco': {},
            'Scrider': {},
            'kkz': {},
            'tchepo': {},
            'Lotus': {},
            'Alidio': {},
            'Chuvisco': {},
            'Older': {},
            'Cristian': {},
            'Pringles': {},
            'Kiddy': {},
            'Xupito': {},
            'JohnMirolho': {},
            'tiago': {},
            'Roshan': {}
        }
        tier_silver = {player: {} for player, _ in tier_fantasy.items()}
        tier_gold = {player: {} for player, _ in tier_fantasy.items()}
        fantasy_roles = ['hard carry', 'mid', 'offlane', 'support', 'hard support']
        fantasy_categories = ['hard carry', 'mid', 'offlane', 'support', 'hard support', 'xp_per_min', 'gold_per_min',
                              'stuns', 'hero_healing', 'damage_taken', 'tower_damage', 'kills', 'assists', 'obs_placed',
                              'hero_damage', 'last_hits', 'stuns', 'observer_kills', 'multi_kills', 'kill_streaks',
                              'courier_kills', 'creeps_stacked', 'deaths', 'camps_stacked', 'purchase']
        silver = ['tower_damage', 'kills', 'damage_taken', 'stuns', 'observer_kills']
        silver_weights = [0.000005, 0.00625, 0.0000025, 0.001, 0.008]
        gold = ['deaths', 'hero_damage', 'purchase', 'assists', 'camps_stacked']
        gold_weights = [0.33333333, 0.000002, 0.08333333, 0.00666667, 0.0666667]

        for player, _ in tier_fantasy.items():
            tier_fantasy[player] = {category: {} for category in fantasy_categories}
            tier_silver[player] = {category: {} for category in silver}
            tier_gold[player] = {category: {} for category in gold}

        fantasy_weights = {
            'hard carry': [5, 0, 0, 0, 0],
            'mid': [0, 5, 0, 0, 0],
            'offlane': [0, 0, 5, 0, 0],
            'support': [0, 0, 0, 5, 0],
            'hard support': [0, 0, 0, 0, 5],
            'xp_per_min': [2, 3, 2, 1, 1],
            'gold_per_min': [4, 3, 2, 1, 1],
            'stuns': [1, 1, 3, 4, 2],
            'hero_healing': [0, 0, 1, 2, 4],
            'damage_taken': [1, 1, 3, 2, 1],
            'hero_damage': [3, 2, 1, 0, 0],
            'tower_damage': [3, 2, 2, 1, 1],
            'kills': [3, 4, 2, 2, 1],
            'assists': [1, 2, 2, 3, 4],
            'obs_placed': [1, 1, 1, 3, 4]
        }

        fantasy_properties = {
            'hard carry': {'header': 'win rate', 'unit': '%', 'multiplier': 1, 'decimal': 1},
            'mid': {'header': 'win rate', 'unit': '%', 'multiplier': 1, 'decimal': 1},
            'offlane': {'header': 'win rate', 'unit': '%', 'multiplier': 1, 'decimal': 1},
            'support': {'header': 'win rate', 'unit': '%', 'multiplier': 1, 'decimal': 1},
            'hard support': {'header': 'win rate', 'unit': '%', 'multiplier': 1, 'decimal': 1},
            'xp_per_min': {'header': 'xpm', 'unit': '', 'multiplier': 1, 'decimal': 0},
            'gold_per_min': {'header': 'gpm', 'unit': '', 'multiplier': 1, 'decimal': 0},
            'stuns': {'header': 'stuns', 'unit': 's', 'multiplier': 1, 'decimal': 1},
            'hero_healing': {'header': 'healing', 'unit': 'k', 'multiplier': 1000, 'decimal': 1},
            'damage_taken': {'header': 'dmg taken', 'unit': 'k', 'multiplier': 1000, 'decimal': 1},
            'hero_damage': {'header': 'hero dmg', 'unit': 'k', 'multiplier': 1000, 'decimal': 1},
            'tower_damage': {'header': 'tower dmg', 'unit': 'k', 'multiplier': 1000, 'decimal': 1},
            'kills': {'header': 'kills', 'unit': '', 'multiplier': 1, 'decimal': 1},
            'assists': {'header': 'assists', 'unit': '', 'multiplier': 1, 'decimal': 1},
            'obs_placed': {'header': 'wards', 'unit': '', 'multiplier': 1, 'decimal': 1},
            'deaths': {'header': '<1death /15min', 'unit': '', 'multiplier': 1, 'decimal': 0},
            'purchase': {'header': 'utility items', 'unit': '', 'multiplier': 1, 'decimal': 0},
            'camps_stacked': {'header': 'camps stacked', 'unit': '', 'multiplier': 1, 'decimal': 0},
            'observer_kills': {'header': 'wards destroyed', 'unit': '', 'multiplier': 1, 'decimal': 0},
        }

        fantasy_count = {category: {role: 0 for role in fantasy_roles} for category in fantasy_categories}
        fantasy_players = [player for player, _ in tier_fantasy.items()]
        fantasy_data = FantasyData()
        for role in fantasy_roles:
            fantasy_data.add_role(role)

        for t in tiers:
            category = t[1].parameter
            tier = t[0]
            if category in silver and not tier.is_max:
                for role in fantasy_roles:
                    for tier_item in tier.scores_array:
                        if tier_item.name in fantasy_players:
                            tier_silver[tier_item.name][category][role] = tier_item.totals_per_role[role]
            if category in gold and not tier.is_max:
                for role in fantasy_roles:
                    for tier_item in tier.scores_array:
                        if tier_item.name in fantasy_players:
                            if role not in tier_gold[tier_item.name][category]:
                                tier_gold[tier_item.name][category][role] = 0
                            if t[1].parameter == 'deaths':
                                if t[1].rule == 'deaths_per_15min':
                                    tier_gold[tier_item.name][category][role] += tier_item.totals_per_role[role]
                            elif t[1].parameter == 'purchase':
                                if t[1].rule == 'utility_items':
                                    tier_gold[tier_item.name][category][role] += tier_item.totals_per_role[role]
                            else:
                                tier_gold[tier_item.name][category][role] += tier_item.totals_per_role[role]
            if category in fantasy_categories and not tier.is_max:
                if category in fantasy_roles:
                    i = 0
                    fantasy_data.add_category(category, category)
                    fantasy_data.add_category_properties(category, category, max(fantasy_weights[category]),
                                                         fantasy_properties[category])
                    last_score = None
                    for tier_item in tier.scores_array:
                        if tier_item.name in fantasy_players:
                            desc = next(p for p in self.player_descriptor if p['name'] == tier_item.name)
                            role_desc = next(r for r in desc['roles'] if r['role'] == category)
                            if role_desc['matches'] <= self.min_matches_with_hero:
                                continue
                            if tier_item.score == last_score:
                                i -= 1
                            tier_fantasy[tier_item.name][category][category] = i
                            fantasy_data.add_player_to_role(category, category, tier_item.name)
                            fantasy_data.add_player_value(category, category, tier_item.name, tier_item.score)
                            fantasy_data.add_player_matches(category, category, tier_item.name, role_desc['matches'])
                            last_score = tier_item.score
                            i += 1
                    fantasy_count[category][category] = i
                else:
                    if category in fantasy_weights:
                        idx_role = 0
                        for role, weight in zip(fantasy_roles, fantasy_weights[category]):
                            if weight > 0:
                                fantasy_data.add_category(role, category)
                                fantasy_data.add_category_properties(role, category,
                                                                     fantasy_weights[category][idx_role],
                                                                     fantasy_properties[category])
                            idx_role += 1
                        for role in fantasy_roles:
                            i = 0
                            last_score = None
                            for name, score in tier.players_sorted_by_role(role):
                                if name in fantasy_players and category in fantasy_data.roles[role]:
                                    desc = next(p for p in self.player_descriptor if p['name'] == name)
                                    role_desc = next(r for r in desc['roles'] if r['role'] == role)
                                    if role_desc['matches'] <= self.min_matches_with_hero:
                                        continue
                                    if score == last_score:
                                        i -= 1
                                    tier_fantasy[name][category][role] = i
                                    fantasy_data.add_player_to_role(role, category, name)
                                    fantasy_data.add_player_value(role, category, name, score)
                                    last_score = score
                                    i += 1
                            fantasy_count[category][role] = i

        BASE = 100
        POND = 4 if len(self.years) == 1 else 3
        ADJUST = 1

        for idx_role in range(5):
            for category in fantasy_categories:
                for player, data in tier_fantasy.items():
                    if "value_%s" % idx_role not in data:
                        data["value_%s" % idx_role] = 0
                    if category in data and category in fantasy_weights and category in fantasy_data.roles[
                        fantasy_roles[idx_role]]:
                        role_name = fantasy_roles[idx_role]
                        w = (1 + fantasy_weights[category][idx_role] * POND / 100.0)
                        b = fantasy_weights[category][idx_role] * BASE
                        if role_name in data[category] and player in fantasy_data.roles[role_name][category]['players']:
                            points = b * w ** (fantasy_count[category][role_name] / 2 - data[category][role_name])
                            fantasy_data.add_player_fantasy_score(role_name, category, player, (points / 500.0))
                            fantasy_data.add_player_relative_position(role_name, category, player,
                                                                      data[category][role_name])
                            data["value_%s" % idx_role] += points

        fantasy_data.clean_up()

        fantasy_values = {}

        for player, d in tier_fantasy.items():
            player_scores = {}
            for r in fantasy_roles:
                player_scores[r] = fantasy_data.get_score_for_player(r, player)
            fantasy_values[player] = {role: int(score * 50) * ADJUST * 10 for role, score in player_scores.items()}
            for role, _ in fantasy_values[player].items():
                desc = next(p for p in self.player_descriptor if p['name'] == player)
                role_desc = next(r for r in desc['roles'] if r['role'] == role)
                if role_desc['matches'] <= self.min_matches_with_hero:
                    fantasy_values[player][role] = 0

        print('Updated Fantasy Values')
        print(str(fantasy_values).replace("'", "\""))
        print('')

        if len(self.years) > 1:
            print('Add as new player')
            for player, data in fantasy_values.items():
                print(str({'player': player, 'roles': data}).replace("'", "\""))
            print('')

        for i in range(5):
            fantasy_data.add_category(fantasy_roles[i], 'silver')
            fantasy_data.add_category_properties(fantasy_roles[i], 'silver', silver_weights[i],
                                                 {
                                                     'header': fantasy_properties[silver[i]]['header'],
                                                     'unit': fantasy_properties[silver[i]]['unit'],
                                                     'multiplier': fantasy_properties[silver[i]]['multiplier'],
                                                     'decimal': 0
                                                 })
            fantasy_data.add_category(fantasy_roles[i], 'gold')
            fantasy_data.add_category_properties(fantasy_roles[i], 'gold', gold_weights[i],
                                                 {
                                                     'header': fantasy_properties[gold[i]]['header'],
                                                     'unit': fantasy_properties[gold[i]]['unit'],
                                                     'multiplier': fantasy_properties[gold[i]]['multiplier'],
                                                     'decimal': 0
                                                 })

        for player, data in fantasy_values.items():
            data['silver'] = {}
            data['gold'] = {}
            for i in range(5):
                if fantasy_roles[i] in tier_silver[player][silver[i]]:
                    data['silver'][fantasy_roles[i]] = tier_silver[player][silver[i]][fantasy_roles[i]] * \
                                                       silver_weights[i]
                    if fantasy_data.player_in_role(fantasy_roles[i], player):
                        fantasy_data.add_player_to_role(fantasy_roles[i], 'silver', player)
                        fantasy_data.add_player_fantasy_score(fantasy_roles[i], 'silver', player,
                                                              data['silver'][fantasy_roles[i]])
                        fantasy_data.add_player_value(fantasy_roles[i], 'silver', player,
                                                      tier_silver[player][silver[i]][fantasy_roles[i]])

                if fantasy_roles[i] in tier_gold[player][gold[i]]:
                    data['gold'][fantasy_roles[i]] = tier_gold[player][gold[i]][fantasy_roles[i]] * gold_weights[i]
                    if fantasy_data.player_in_role(fantasy_roles[i], player):
                        fantasy_data.add_player_to_role(fantasy_roles[i], 'gold', player)
                        fantasy_data.add_player_fantasy_score(fantasy_roles[i], 'gold', player,
                                                              data['gold'][fantasy_roles[i]])
                        fantasy_data.add_player_value(fantasy_roles[i], 'gold', player,
                                                      tier_gold[player][gold[i]][fantasy_roles[i]])

        return fantasy_values, fantasy_data

    def calculate_streaks(self, pid):
        matches = self.match_summary
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
