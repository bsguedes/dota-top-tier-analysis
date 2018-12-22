# coding=utf-8

from tier import *
from code import Parser
from code import Category
from downloader import Downloader

PNK = 'PnK'
BLAZING_DOTA = 'Blazing Dota'
MIN_PARTY_SIZE = 4
MIN_MATCHES = 10
MIN_COUPLE_MATCHES = 10
YEARS = [2018]
TEAM_NAME = PNK

player_list = {
    PNK: {
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
    },
    BLAZING_DOTA: {
        'Pogo': 121639063,
        'Cristian': 160043364,
        'TH': 24161066,
        'Older': 124228147,
        'Blink': 204508290,
        'Steve': 243090098,
        'flesch': 120468374
    }
}

categories = [
    Category(20, 'win', text='wins', has_max=False, apply_transform=Transforms.percentage),
    Category(10, 'kills'),
    Category(10, 'deaths', reverse=False),
    Category(10, 'assists'),
    Category(10, 'kda', text='KLA', rule='kla'),
    Category(2, 'hard carry', text='hard carry win rate', rule='position'),
    Category(2, 'mid', text='mid win rate', rule='position'),
    Category(2, 'offlane', text='offlane win rate', rule='position'),
    Category(2, 'support', text='support win rate', rule='position'),
    Category(2, 'hard support', text='hard support win rate', rule='position'),
    Category(4, 'xp_per_min', text='xpm'),
    Category(4, 'total_gold', text='total gold'),
    Category(6, 'gold_per_min', text='gpm'),
    Category(8, 'hero_damage', text='hero damage'),
    Category(5, 'hero_healing', text='hero healing'),
    Category(5, 'tower_damage', text='tower damage'),
    Category(5, 'last_hits', text='last hits'),
    Category(2, 'denies'),
    Category(5, 'rune_pickups', text='runes picked up'),
    Category(8, 'obs_placed', text='observer wards placed'),
    Category(8, 'sen_placed', text='sentry wards placed'),
    Category(2, 'purchase', text='dusts purchased', rule='dust'),
    Category(2, 'purchase', text='smokes purchased', rule='smoke_of_deceit'),
    Category(2, 'purchase', text='gems of true sight purchased', rule='gem'),
    Category(5, 'purchase', text='gold in support items', rule='support_gold'),
    Category(5, 'creeps_stacked', text='creeps stacked'),
    Category(4, 'observer_kills', text='wards removed', rule='ward_kill'),
    Category(2, 'courier_kills', text='couriers killed'),
    Category(2, 'purchase_tpscroll', text='TPs purchased'),
    Category(2, 'purchase', text='tomes of knowledge purchased', rule='tome_of_knowledge'),
    Category(5, 'stuns', text='stun duration dealt'),
    Category(5, 'pings'),
    Category(4, 'lane_efficiency_pct', text='lane efficiency at 10min'),
    Category(2, 'buyback_count', text='buybacks'),
    Category(2, 'kill_streaks', text='beyond godlike streaks', rule='beyond_godlike', has_max=False),
    Category(2, 'actions_per_min', text='actions per minute'),
    Category(2, 'duration', text='duration in minutes', apply_transform=Transforms.sec_to_min)
]

if __name__ == '__main__':
    players = player_list[TEAM_NAME]
    Downloader.download_player_data(players, override=False)
    unique_matches = Parser.get_matches(TEAM_NAME, YEARS, players, min_party_size=MIN_PARTY_SIZE, ranked_only=False)
    Downloader.download_matches(unique_matches)
    
    tier_positions = Parser.identify_heroes(TEAM_NAME, players, unique_matches, min_couple_matches=MIN_COUPLE_MATCHES)
    Parser.identify_teams(TEAM_NAME, players, unique_matches)
    tiers = []

    for c in categories:
        if c.rule == 'position':
            tier = Tier(c.weight, tier_positions[c.parameter], 'Win rate as %s in %s matches'
                        % (c.parameter, TEAM_NAME))
            tier.print()
            tiers.append(tier)
        else:
            res_avg, res_max = Parser.stat_counter(players, unique_matches, c.parameter, text=c.text,
                                                   tf=c.transform, reverse=c.reverse, min_matches=MIN_MATCHES,
                                                   has_max=c.has_max, rule=c.rule, has_avg=c.has_avg)
            cat_name = c.text if c.text is not None else c.parameter
            if c.has_avg:
                tier_avg = Tier(c.weight, res_avg, 'Average %s in %s matches' % (cat_name, TEAM_NAME))
                tier_avg.print()
                tiers.append(tier_avg)
            if c.has_max:
                tier_max = Tier(c.weight, res_max, 'Maximum %s in a single match' % cat_name, is_max=True)
                tier_max.print()
                tiers.append(tier_max)

    Tier.show_results(players, tiers)
    Tier.show_results_weights(players, tiers)
