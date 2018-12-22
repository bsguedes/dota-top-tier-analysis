import requests
import os.path


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
                print('Downloading match %i data' % match_id)
                url = 'https://api.opendota.com/api/matches/%i' % match_id
                r = requests.get(url, allow_redirects=True)
                open(file_name, 'wb').write(r.content)
