import requests
import os
import os.path

class Downloader:
    @staticmethod
    def download_player_data(players, override=True):
        if not os.path.exists('players'):
            os.makedirs('players')
        for name, pid in players.items():
            file_name = 'players/%s_matches.json' % name
            if override or not os.path.isfile(file_name):
                print('Downloading %s data' % name)
                url = 'https://api.opendota.com/api/players/%s/matches?project=start_time' % pid
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)

    @staticmethod
    def download_matches(unique_matches, override=False):
        print('')
        print('Found %s matches' % len(unique_matches))
        if not os.path.exists('players'):
            os.makedirs('players')
        for match_id in unique_matches:
            file_name = 'matches/%s.json' % match_id
            if override or not os.path.isfile(file_name):
                print('Downloading match %i data' % match_id)
                url = 'https://api.opendota.com/api/matches/%i' % match_id
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)
