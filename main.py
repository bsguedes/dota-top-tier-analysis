# coding=utf-8

from code import *

players = {
    'Zé': 25185394,
    'Chaos': 48264000,
    'Nuvah': 42856922,
    'Baco': 1997649,
    'Scrider': 116551069,
    'kkz': 86722309,
    'Tchepo': 61867497,
    'Lotus': 114872129,
    'Alidio': 92240711,
    'Chuvisco': 97418109,
    'Gilberto': 40466900,
    'Older': 124228147,
    'tiago': 42330286,
    'shadow': 81575622,
    'Osaka': 99809454,
    'Cristian': 160043364,
    'Pringles': 84962243,
    'Alpiona': 30320098,
    'Fallenzão': 396690444
}


if __name__ == '__main__':
    Downloader.download_player_data(players)
    unique_matches = Parser.get_matches_for_year(2018, players, last_days=60, min_party_size=5)
    Downloader.download_matches(unique_matches)
    
    Parser.identify_heroes(players, unique_matches)
    Parser.identify_teams(players, unique_matches)
    
    Parser.pnk_counters(players, unique_matches, 'hero_healing', text='hero healing')
    Parser.pnk_counters(players, unique_matches, 'rune_pickups', text='runes picked up')
    Parser.pnk_counters(players, unique_matches, 'pings')
    Parser.pnk_counters(players, unique_matches, 'creeps_stacked', text='creeps stacked')
    Parser.pnk_counters(players, unique_matches, 'stuns', text='stun duration dealt')
    Parser.pnk_counters(players, unique_matches, 'hero_damage', text='hero damage')
    Parser.pnk_counters(players, unique_matches, 'total_gold', text='total gold')
    Parser.pnk_counters(players, unique_matches, 'gold_per_min', text='gpm')
    Parser.pnk_counters(players, unique_matches, 'kills')
    Parser.pnk_counters(players, unique_matches, 'deaths', reverse=False)
    Parser.pnk_counters(players, unique_matches, 'assists')
    Parser.pnk_counters(players, unique_matches, 'obs_placed', text='observer wards placed')
    Parser.pnk_counters(players, unique_matches, 'sen_placed', text='sentry wards placed')

