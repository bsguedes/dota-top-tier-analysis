# coding=utf-8

from code import *
from tier import *

MIN_PARTY_SIZE = 4
MIN_MATCHES = 10
MIN_COUPLE_MATCHES = 10
YEARS = [2018]

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

categories = [
    Category('win', text='wins', has_max=False, apply_transform=Transforms.percentage),    
    Category('observer_kills', text='wards removed', rule='ward_kill'),
    Category('kda', text='KLA', rule='kla'),
    Category('xp_per_min', text='xpm'),
    Category('buyback_count', text='buybacks'),
    Category('kill_streaks', text='beyond godlike streaks', rule='beyond_godlike', has_max=False),
    Category('lane_efficiency_pct', text='lane efficiency at 10min'),
    Category('tower_damage', text='tower damage'),    
    Category('actions_per_min', text='actions per minute'),
    Category('purchase_tpscroll', text='TPs purchased'),
    Category('duration', text='duration in minutes', apply_transform=Transforms.sec_to_min),
    Category('last_hits', text='last hits'),
    Category('denies'),
    Category('hero_healing', text='hero healing'),
    Category('rune_pickups', text='runes picked up'),
    Category('pings'),
    Category('creeps_stacked', text='creeps stacked'),
    Category('stuns', text='stun duration dealt'),
    Category('hero_damage', text='hero damage'),
    Category('total_gold', text='total gold'),
    Category('gold_per_min', text='gpm'),
    Category('kills'),
    Category('deaths', reverse=False),
    Category('assists'),
    Category('obs_placed', text='observer wards placed'),
    Category('sen_placed', text='sentry wards placed')
]

if __name__ == '__main__':
    Downloader.download_player_data(players)
    unique_matches = Parser.get_matches(YEARS, players, min_party_size=MIN_PARTY_SIZE, ranked_only=False)
    Downloader.download_matches(unique_matches)
    
    Parser.identify_heroes(players, unique_matches, min_couple_matches=MIN_COUPLE_MATCHES)
    Parser.identify_teams(players, unique_matches)

    tiers = []
    for c in categories:
        res_avg, res_max = Parser.pnk_counters(players, unique_matches, c.parameter, text=c.text, 
                                               tf=c.transform, reverse=c.reverse, min_matches=MIN_MATCHES, 
                                               has_max=c.has_max, rule=c.rule)
        cat_name = c.text if c.text is not None else c.parameter
        tier_avg = Tier(res_avg, 'Average %s in PnK matches' % cat_name)
        tiers.append(tier_avg)
        tier_avg.print()
        if c.has_max:
            tier_max = Tier(res_max, 'Maximum %s in a single match' % cat_name)
            tier_max.print()
            tiers.append(tier_max)

    Tier.show_results(players, tiers)
