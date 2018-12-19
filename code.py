# coding=utf-8

import requests
import os.path
import json
from time import *


class Parser:
    @staticmethod
    def identify_teams(players, matches, min_matches=10):
        account_ids = [v for k, v in players.items()]
        match_summary = {k: {'isRadiant': False, 'players': [], 'win': False} for k, v in matches.items()}
        for match_id, match_players in matches.items():
            content = open('matches/%i.json' % match_id, 'r', encoding='utf-8').read()
            obj = json.loads(content)
            for p in obj['players']:
                if p['account_id'] in account_ids:
                    if p['isRadiant']:
                       match_summary[match_id] = {'isRadiant': True, 'players': match_players, 'win': p['win'] > 0}
                    else:
                       match_summary[match_id] = {'isRadiant': False, 'players': match_players, 'win': p['win'] > 0} 
                    break
        print('')
        print ('PnK winrate: %.2f %%' % (100 * len([x for x,y in match_summary.items() if y['win']]) / len(matches)))

        match_count = {k: 0 for k, v in players.items()}
        win_count = {k: 0 for k, v in players.items()}
        win_perc = {k: 0 for k, v in players.items()}
        for name, pid in players.items():
            match_count[name] = len([k for k, v in match_summary.items() if name in v['players']])
            win_count[name] = len([k for k, v in match_summary.items() if name in v['players'] and v['win']])
            win_perc[name] = win_count[name] / match_count[name]

        print('')
        sorted_wins = sorted(win_perc.items(), key=lambda kv: kv[1])
        sorted_wins.reverse()

        count = 0
        total_players = len([k for k, v in match_count.items() if v > min_matches])
        tier_size = int(total_players / 3)
        for name, value in sorted_wins:
            if match_count[name] > min_matches:
                if count % tier_size == 0:               
                    print('')     
                    print('Tier %i:' % (count / tier_size + 1))
                count += 1
                print('%s has won %i matches with PnK from %i total (win rate %.2f %%)'
                      % (name, win_count[name], match_count[name], 100 * win_perc[name]))
        


    @staticmethod
    def pnk_counters(players, matches, parameter, reverse=True, min_matches=10, text=None):
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
                if p['account_id'] in account_ids and p[parameter] is not None:
                    if not inv_p[p['account_id']] in totals:
                        totals[inv_p[p['account_id']]] = 0
                        matches_played[inv_p[p['account_id']]] = 0
                    totals[inv_p[p['account_id']]] += p[parameter]
                    if p[parameter] > maximum_value[p['account_id']]:
                        maximum_value[p['account_id']] = p[parameter]
                        maximum_match[p['account_id']] = match_id
                    matches_played[inv_p[p['account_id']]] += 1

        print('Average %s per match:' % text)

        for name, pid in players.items():
            averages[name] = totals[name]/matches_played[name]

        sorted_average = sorted(averages.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_average.reverse()

        count = 0
        total_players = len([k for k, v in matches_played.items() if v > min_matches])
        tier_size = int(total_players / 3)
        for name, value in sorted_average:
            if matches_played[name] > min_matches:
                if count % tier_size == 0:               
                    print('')     
                    print('Tier %i:' % (count / tier_size + 1))
                count += 1
                print('%s has %i %s in %i matches (avg %.2f)'
                      % (name, totals[name], text, matches_played[name], averages[name]))
        print('')

        print('Maximum %s in a single match:' % text)

        sorted_maximum = sorted(maximum_value.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_maximum.reverse()

        count = 0    
        for pid, value in sorted_maximum:
            if matches_played[inv_p[pid]] > min_matches:
                if count % tier_size == 0:               
                    print('')     
                    print('Tier %i:' % (count / tier_size + 1))
                count += 1
                print('%s: %i %s (match id: %i)'
                      % (inv_p[pid], maximum_value[pid], text, maximum_match[pid]))
        print('')

    @staticmethod
    def get_matches_for_year(year, players):
        matches = dict()
        total_matches = {n: 0 for n, pid in players.items()}
        for name, pid in players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)            
            total_matches[name] = 0
            for o in obj:
                y = gmtime(int(o['start_time'])).tm_year
                if y == year:
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
            matches_with_pnk = len([i for i, v in matches.items() if len(v) >= 2 and name in v])
            perc_with_pnk = matches_with_pnk / match_count
            print('%s played %i matches -- %i matches (%.2f %%) played with PnK' 
                % (name, match_count, matches_with_pnk, 100 * perc_with_pnk))

        return {k: v for k, v in matches.items() if len(v) >= 2}


class Downloader:
    @staticmethod
    def download_player_data(players, override=False):
        for name, pid in players.items():
            file_name = 'players/%s_matches.json' % name
            if override or not os.path.isfile(file_name):
                url = 'https://api.opendota.com/api/players/%s/matches' % pid
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)

    @staticmethod
    def download_matches(unique_matches, override=False):
        for match_id in unique_matches:
            file_name = 'matches/%s.json' % match_id
            if override or not os.path.isfile(file_name):
                url = 'https://api.opendota.com/api/matches/%i' % match_id
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)
