import requests
import os
import os.path
import json
import urllib.request
import time


def download_heroes():
    if not os.path.exists('data/heroes'):
        os.makedirs('data/heroes')
    hs = open('data/heroes_images.json', 'r', encoding='utf-8').read()
    hs_json = json.loads(hs)
    heroes_urls = [h['path'] for h in hs_json]
    hs = open('data/heroes.json', 'r', encoding='utf-8').read()
    hs_json = json.loads(hs)
    heroes = {h['id']: h['localized_name'] for h in hs_json}
    for h_id, h_name in heroes.items():
        file_name = 'data/heroes/%i.jpg' % h_id
        if not os.path.isfile(file_name):
            name_parts = h_name.lower().replace('\'', '').split(' ')
            for url in heroes_urls:
                if name_parts[0] == 'io' and '/io' in url or name_parts[0] != 'io' and all(
                        part in url for part in name_parts):
                    print('Downloading %s image' % h_name)
                    urllib.request.urlretrieve(url, file_name)
                    break


def download_player_data(players, replacements, override=True):
    if not os.path.exists('players'):
        os.makedirs('players')
    for name, pid in players.items():
        file_name = 'players/%s_matches.json' % name
        if override or not os.path.isfile(file_name):
            start = time.time()
            url = 'https://api.opendota.com/api/players/%s/matches?project=start_time' % pid
            r = requests.get(url, allow_redirects=True)
            print('Downloaded %s data: %.3f seconds' % (name, time.time() - start))
            open(file_name, 'wb').write(r.content)
    if replacements is not None:
        for name, pid in replacements.items():
            file_name = 'players/%s_matches_r.json' % name
            if override or not os.path.isfile(file_name):
                start = time.time()
                url = 'https://api.opendota.com/api/players/%s/matches?project=start_time' % pid
                r = requests.get(url, allow_redirects=True)
                print('Downloaded %s replacement data: %.3f seconds' % (name, time.time() - start))
                open(file_name, 'wb').write(r.content)


def download_matches(unique_matches, override=False, download_again=False):
    print('')
    print('Found %s matches' % len(unique_matches))
    if not os.path.exists('matches'):
        os.makedirs('matches')
    for match_id in unique_matches:
        file_name = 'matches/%s.json' % match_id
        if override or not os.path.isfile(file_name):
            start = time.time()
            url = 'https://api.opendota.com/api/matches/%i' % match_id
            r = requests.get(url, allow_redirects=True)
            print('Downloaded match %i data: %.3f seconds' % (match_id, time.time() - start))
            open(file_name, 'wb').write(r.content)
        if os.path.getsize(file_name) < 35000 and download_again:
            os.remove(file_name)
            print('Downloading again match %i data' % match_id)
            url = 'https://api.opendota.com/api/matches/%i' % match_id
            r = requests.get(url, allow_redirects=True)
            open(file_name, 'wb').write(r.content)
    matches_to_parse = 0
    for match_id in unique_matches:
        file_name = 'matches/%s.json' % match_id
        if os.path.getsize(file_name) < 35000:
            matches_to_parse += 1
            print("Should re-parse match %i on OpenDota" % match_id)
    return matches_to_parse

