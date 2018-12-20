# coding=utf-8

import requests
import os.path
import json
import math
import calendar
from time import *
from tier import TierItem


class Parser:
    @staticmethod
    def identify_heroes(players, matches):
        hs = open('data/heroes.json', 'r', encoding='utf-8').read()
        hs_json = json.loads(hs)
        heroes = {h['id']: h['localized_name'] for h in hs_json}
        inv_h = {h['localized_name']: h['id'] for h in hs_json}
        account_ids = [v for k, v in players.items()]
        match_summary = {k: {'pnk_heroes': [], 'enemy_heroes': [], 'players': []} for k, v in matches.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids:
                    match_summary[match_id]['pnk_heroes'].append(p['hero_id'])                    
                    match_summary[match_id]['players'].append(p['account_id'])
                    match_summary[match_id]['win'] = p['win'] > 0
                    match_summary[match_id]['is_radiant'] = p['isRadiant']        
            for p in obj['players']:
                if p['isRadiant'] != match_summary[match_id]['is_radiant']:
                    match_summary[match_id]['enemy_heroes'].append(p['hero_id'])
        win_rate_versus_heroes = {k: {'matches': 0, 'wins': 0} for k, v in heroes.items()}
        for mid, v in match_summary.items():
            for enemy_hero in v['enemy_heroes']:
                win_rate_versus_heroes[enemy_hero]['matches'] += 1
                if v['win']:
                    win_rate_versus_heroes[enemy_hero]['wins'] += 1
        avg = {v: win_rate_versus_heroes[k]['wins'] / win_rate_versus_heroes[k]['matches'] for k, v in heroes.items()}
        s = sorted(avg.items(), key=lambda e: e[1], reverse=True)
        for k, v in s:
            print('%.2f %% PnK win rate versus %s (%i matches)'
                  % (100 * v, k, win_rate_versus_heroes[inv_h[k]]['matches']))

    @staticmethod
    def identify_teams(players, matches):
        account_ids = [v for k, v in players.items()]
        match_summary = {k: {'players': [], 'win': False} for k, v in matches.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids:
                    match_summary[match_id] = {'players': match_players, 'win': p['win'] > 0}
                    break

        print('')
        print('PnK Win Rate: %.2f %%' % (100 * len([x for x, y in match_summary.items() if y['win']]) / len(matches)))

    @staticmethod
    def pnk_counters(players, matches, parameter, reverse=True, min_matches=10,
                     text=None, accumulate=False, has_max=True):
        text = parameter if text is None else text

        account_ids = [v for k, v in players.items()]
        inv_p = {v: k for k, v in players.items()}
        matches_played = {k: 0 for k, v in players.items()}

        averages = {k: 0 for k, v in players.items()}
        totals = {k: 0 for k, v in players.items()}

        maximum_value = {v: 0 for k, v in players.items()}
        maximum_match = {v: 0 for k, v in players.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids and parameter in p and p[parameter] is not None:
                    if not inv_p[p['account_id']] in totals:
                        totals[inv_p[p['account_id']]] = 0
                        matches_played[inv_p[p['account_id']]] = 0
                    if accumulate:
                        value = sum([v for k, v in p[parameter].items()])
                    else:
                        value = p[parameter]
                    totals[inv_p[p['account_id']]] += value
                    if value > maximum_value[p['account_id']]:
                        maximum_value[p['account_id']] = value
                        maximum_match[p['account_id']] = match_id
                    matches_played[inv_p[p['account_id']]] += 1

        for name, pid in players.items():
            averages[name] = totals[name]/matches_played[name] if matches_played[name] > 0 else 0

        sorted_average = sorted(averages.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_average.reverse()

        results_avg = []
        for name, value in sorted_average:
            if matches_played[name] > min_matches:
                txt = '%s has %i %s in %i matches (avg %.2f)' \
                        % (name, totals[name], text, matches_played[name], averages[name])
                results_avg.append(TierItem(name, averages[name], txt))

        if not has_max:
            return results_avg, None

        sorted_maximum = sorted(maximum_value.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_maximum.reverse()

        results_max = []
        for pid, value in sorted_maximum:
            if matches_played[inv_p[pid]] > min_matches:
                txt = '%s: %i %s (match id: %i)' \
                       % (inv_p[pid], maximum_value[pid], text, maximum_match[pid])
                results_max.append(TierItem(inv_p[pid], maximum_value[pid], txt))

        return results_avg, results_max

    @staticmethod
    def get_matches_for_year(year, players, min_party_size=2, last_days=0):
        matches = dict()
        total_matches = {n: 0 for n, pid in players.items()}
        for name, pid in players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)            
            total_matches[name] = 0
            for o in obj:
                y = gmtime(int(o['start_time'])).tm_year                
                if (last_days > 0 and (calendar.timegm(gmtime()) - int(o['start_time'])) < last_days * 86400) \
                        or (last_days == 0 and y == year):
                    total_matches[name] += 1
                    if not o['match_id'] in matches:
                        matches[o['match_id']] = []
                    matches[o['match_id']].append(name)
        for i in range(0, 5):
            print('Matches played by party of size %i: %s'
                  % (i+1, len({k: v for k, v in matches.items() if len(v) == i+1})))
        
        print('')                    
        sorted_matches = sorted(total_matches.items(), key=lambda kv: kv[1])
        sorted_matches.reverse()
        
        for name, match_count in sorted_matches:
            matches_with_pnk = len([i for i, v in matches.items() if len(v) >= min_party_size and name in v])
            percentage_with_pnk = matches_with_pnk / match_count if match_count > 0 else 0
            print('%s played %i matches -- %i matches (%.2f %%) played with PnK' 
                  % (name, match_count, matches_with_pnk, 100 * percentage_with_pnk))

        return {k: v for k, v in matches.items() if len(v) >= min_party_size}


class Category:
    def __init__(self, param, text=None, reverse=True, has_max=True):
        self.parameter = param
        self.text = text
        self.reverse = reverse
        self.has_max = has_max


class Downloader:
    @staticmethod
    def download_player_data(players, override=False):
        for name, pid in players.items():
            file_name = 'players/%s_matches.json' % name
            if override or not os.path.isfile(file_name):
                print('Downloading %s data' % name)
                url = 'https://api.opendota.com/api/players/%s/matches' % pid
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)

    @staticmethod
    def download_matches(unique_matches, override=False):
        print('')
        print('Found %s matches' % len(unique_matches))
        for match_id in unique_matches:
            file_name = 'matches/%s.json' % match_id
            if override or not os.path.isfile(file_name):
                url = 'https://api.opendota.com/api/matches/%i' % match_id
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)
