import requests
import os.path
import json
from time import *


class Parser:
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
        for match_id in matches:
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

        for name, pid in players.items():
            averages[name] = totals[name]/matches_played[name]

        sorted_average = sorted(averages.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_average.reverse()

        for name, value in sorted_average:
            if matches_played[name] > min_matches:
                print('%s has %i %s in %i matches (avg %.2f)'
                      % (name, totals[name], text, matches_played[name], averages[name]))
        print('')

        sorted_maximum = sorted(maximum_value.items(), key=lambda kv: kv[1])
        if reverse:
            sorted_maximum.reverse()

        for pid, value in sorted_maximum:
            if matches_played[inv_p[pid]] > min_matches:
                print('%s: %i %s (match id: %i)'
                      % (inv_p[pid], maximum_value[pid], text, maximum_match[pid]))
        print('')

    @staticmethod
    def get_matches_for_year(year, players):
        matches = dict()
        for name, pid in players.items():
            content = open('players/%s_matches.json' % name, 'r').read()
            obj = json.loads(content)
            for o in obj:
                y = gmtime(int(o['start_time'])).tm_year
                if y == year:
                    if not o['match_id'] in matches:
                        matches[o['match_id']] = []
                    matches[o['match_id']].append(name)
        for i in range(0, 5):
            print('Matches played by party of size %i: %s'
                  % (i+1, len({k: v for k, v in matches.items() if len(v) == i+1})))
        print('')
        return [k for k, v in matches.items() if len(v) >= 2]


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
