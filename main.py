# coding=utf-8

from category import Category
from code import Parser
from tier import *
from downloader import Downloader
from slides import Slides
from popular_vote import PopularVotePnK2018

PNK = 'PnK'
BLAZING_DOTA = 'Blazing Dota'
MIN_PARTY_SIZE = 4
MIN_MATCHES = 35
MIN_COUPLE_MATCHES = 20
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
        'tchepo': 61867497,
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
        'Fallenzão': 396690444,
        'Maionese': 35304398
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

popular_vote = None
if TEAM_NAME == PNK:
    popular_vote = PopularVotePnK2018()

categories = [
    Category(20, 'win', unit='%', text='wins', has_max=False, apply_transform=Transforms.percentage),
    Category(10, 'kills', unit='kills'),
    Category(10, 'deaths', unit='deaths', reverse=False),
    Category(10, 'assists', unit='assists'),
    Category(10, 'kda', text='KLA', rule='kla'),
    Category(2, 'hard carry', unit='%', text='hard carry win rate', rule='position'),
    Category(2, 'mid', unit='%', text='mid win rate', rule='position'),
    Category(2, 'offlane', unit='%', text='offlane win rate', rule='position'),
    Category(2, 'support', unit='%', text='support win rate', rule='position'),
    Category(2, 'hard support', unit='%', text='hard support win rate', rule='position'),
    Category(4, 'xp_per_min', unit='xpm', text='xpm'),
    Category(4, 'total_gold', unit='gold', text='total gold'),
    Category(6, 'gold_per_min', unit='gpm', text='gpm'),
    Category(8, 'hero_damage', unit='dmg', text='hero damage'),
    Category(5, 'hero_healing', unit='heal', text='hero healing'),
    Category(5, 'tower_damage', unit='dmg', text='tower damage'),
    Category(5, 'last_hits', unit='last hits', text='last hits'),
    Category(2, 'denies', unit='denies'),
    Category(5, 'rune_pickups', unit='runes', text='runes picked up'),
    Category(8, 'obs_placed', unit='wards', text='observer wards placed'),
    Category(8, 'sen_placed', unit='sentries', text='sentry wards placed'),
    Category(2, 'purchase', unit='dusts', text='dusts purchased', rule='dust'),
    Category(2, 'purchase', unit='smokes', text='smokes purchased', rule='smoke_of_deceit'),
    Category(2, 'purchase', unit='gems', text='gems of true sight purchased', rule='gem'),
    Category(5, 'purchase', unit='gold', text='gold in support items', rule='support_gold'),
    Category(5, 'creeps_stacked', unit='creeps', text='creeps stacked'),
    Category(4, 'observer_kills', unit='wards', text='wards removed', rule='ward_kill'),
    Category(2, 'courier_kills', unit='couriers', text='couriers killed'),
    Category(2, 'purchase_tpscroll', unit='TPs', text='TPs purchased'),
    Category(2, 'purchase', unit='tomes', text='tomes of knowledge purchased', rule='tome_of_knowledge'),
    Category(5, 'stuns', unit='seconds', text='stun duration dealt'),
    Category(5, 'pings', unit='pings'),
    Category(4, 'lane_efficiency_pct', unit='%', text='lane efficiency at 10min'),
    Category(2, 'buyback_count', unit='buybacks', text='buybacks'),
    Category(2, 'kill_streaks', unit='streaks', text='beyond godlike streaks', rule='beyond_godlike', has_max=False),
    Category(2, 'actions_per_min', unit='apm', text='actions per minute'),
    Category(2, 'duration', unit='min', text='duration in minutes', apply_transform=Transforms.sec_to_min)
]


def get_title():
    return 'PnK Gaming Awards' if TEAM_NAME == 'PnK' else TEAM_NAME


def get_subtitle():
    if len(YEARS) == 1:
        return "%i Edition" % YEARS[0]
    return str(YEARS)


if __name__ == '__main__':
    players = player_list[TEAM_NAME]
    s = Slides(TEAM_NAME, get_title(), get_subtitle(), players)
    p = Parser(TEAM_NAME, YEARS, players, MIN_MATCHES, MIN_PARTY_SIZE)

    Downloader.download_heroes()
    Downloader.download_player_data(players, override=False)
    unique_matches = p.get_matches(ranked_only=False)
    Downloader.download_matches(unique_matches)

    tier_positions = p.identify_heroes(unique_matches, min_couple_matches=MIN_COUPLE_MATCHES)
    win_rate = p.identify_teams(unique_matches)

    s.add_divider_slide("%s General Statistics" % TEAM_NAME, 'Win Rate, Comebacks, Throws, Heroes, Compositions, Pairs')
    s.add_intro_slide(len(unique_matches), MIN_PARTY_SIZE, MIN_MATCHES, MIN_COUPLE_MATCHES)
    s.add_win_rate_slide(win_rate, len(unique_matches), p.matches_by_party_size)
    s.add_match_summary_by_player(p.match_summary_by_player, p.match_summary_by_team)
    s.add_comebacks_throws(p.top_comebacks, p.top_throws)
    s.add_win_rate_heroes(p.with_heroes, 'Playing')
    s.add_most_played(p.most_played_heroes)
    s.add_win_rate_heroes(p.against_heroes, 'Versus')
    s.add_compositions(p.compositions)

    s.add_divider_slide("%s Players" % TEAM_NAME, 'Roles, Pairings and Most Played Heroes')
    for p_name, pid in players.items():
        roles = p.player_roles[pid]
        player_heroes = p.player_heroes[pid]
        pairings = p.player_pairs[pid]
        s.add_player_slides(p_name, roles, player_heroes, pairings)

    s.add_divider_slide("%s Technical Categories" % TEAM_NAME, 'Averages and Maximum for many statistics')
    tiers = []
    for c in categories:
        if c.rule == 'position':
            tier = Tier(c.weight, tier_positions[c.parameter], 'Win rate as %s in %s matches'
                        % (c.parameter, TEAM_NAME))
            tier.print()
            tiers.append(tier)
            s.add_tier_slides(tier, c)
        else:
            res_avg, res_max = p.stat_counter(unique_matches, c.parameter, text=c.text, unit=c.unit, tf=c.transform,
                                              reverse=c.reverse, has_max=c.has_max, rule=c.rule, has_avg=c.has_avg)
            cat_name = c.text if c.text is not None else c.parameter
            if c.has_avg:
                tier_avg = Tier(c.weight, res_avg, 'Average %s in %s matches' % (cat_name, TEAM_NAME))
                tier_avg.print()
                tiers.append(tier_avg)
                s.add_tier_slides(tier_avg, c)
            if c.has_max:
                st = 'Maximum' if c.reverse else 'Minimum'
                tier_max = Tier(c.weight, res_max, '%s %s in a single match' % (st, cat_name), is_max=True)
                tier_max.print()
                tiers.append(tier_max)
                s.add_tier_slides(tier_max, c)

    medals = Tier.show_results(players, tiers)
    points = Tier.show_results_weights(players, tiers)
    s.add_results_slides(medals, points)

    if popular_vote is not None:
        s.add_divider_slide("%s Popular Vote" % TEAM_NAME, popular_vote.message)
        for category in popular_vote.votes:
            s.add_popular_vote_category_slides(category)
        s.add_top_five_slides(popular_vote.get_top_five())
    s.save()
