# coding=utf-8

from category import Category
from code import Parser
from tier import Tier, T
import downloader
from slides import Slides
from popular_vote import PopularVotePnK2018, PopularVotePnK2019, PopularVotePnK2020
from achievements import PnKAchievements
import time
import calendar


PNK = 'PnK'
BLAZING_DOTA = 'Blazing Dota'
TEAM_NAME = PNK
ALL_TIME_YEARS = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
CURRENT_MONTH = 1
CURRENT_YEAR = 2021

# Modes
# 0: current month
# 1: current year
# 2: all time
MODE = 0
DOWNLOAD_PLAYERS = True
ONLY_RANKED = False

PRINT_TIERS = False
REDOWNLOAD_SMALL_FILES = False
BEST_TEAM = None
# BEST_TEAM = ['Zé', 'Nuvah', 'Chaos', 'Older', 'Alidio']

# PnK monthly parameters: 3, 3, 3, 2
# PnK year parameters: 30, 10, 3, 3
# PnK all-time parameters: 50, 15, 3, 4

pnk_parameters = [[4, 4, 3, 2], [30, 10, 3, 5], [50, 15, 3, 10]]

YEARS = ALL_TIME_YEARS if MODE == 2 else [CURRENT_YEAR]
MONTH = CURRENT_MONTH if MODE == 0 else None

parameters = {
    PNK: {
        'min_matches': pnk_parameters[MODE][0],
        'min_couple_matches': pnk_parameters[MODE][1],
        'min_party_size': pnk_parameters[MODE][2],
        'min_matches_with_hero': pnk_parameters[MODE][3]
    },
    BLAZING_DOTA: {
        'min_matches': 4,
        'min_couple_matches': 4,
        'min_party_size': 2,
        'min_matches_with_hero': 2
    }
}

MIN_PARTY_SIZE = parameters[TEAM_NAME]['min_party_size']
MIN_MATCHES = parameters[TEAM_NAME]['min_matches']
MIN_COUPLE_MATCHES = parameters[TEAM_NAME]['min_couple_matches']
MIN_MATCHES_WITH_HERO = parameters[TEAM_NAME]['min_matches_with_hero']

replacement_list = {
    PNK: {
        'Fallenzão': [331461200],
        'kkz': [116647196, 92129470],
        'Kiddy': [409605487, 242249397, 189723196, 365319706, 29806143],
        'Alidio': [495078],
        'Roshan': [93345002]
    },
    BLAZING_DOTA: {
        'flesch': [372670607]
    }
}

forced_replacements = {
    5725364669: {365319706: 'kkz'},
    5725394131: {365319706: 'kkz'},
    5725426780: {365319706: 'kkz'},
    5725452578: {365319706: 'kkz'},
}

discord_ids = {
    'Zé': 139193879134994432,
    'Chaos': 291727771967946754,
    'Nuvah': 126788612040687616,
    'Baco': 230178690519007232,
    'Scrider': 166322198313697280,
    'kkz': 276631463502282753,
    'tchepo': 263451833916325891,
    'Lotus': 175692038904348672,
    'Alidio': 291728906556538882,
    'Chuvisco': 280895347323305985,
    'Gilberto': 115146154919854086,
    'Older': 193946233616859137,
    'tiago': 126515896993710082,
    'shadow': 197096313647529984,
    'Osaka': 225058575809118208,
    'Cristian': 281936638593073153,
    'Pringles': 348900934522372099,
    'Alpiona': 126491764876902401,
    'Fallenzão': 302310551114219522,
    'Maionese': 319278774623404032,
    'Kiddy': 139783087109177345,
    'Roshan': 226882871724343296,
    'deliri019': 216543587373023232,
    'Pogo': 297716705805991936,
    'darkkside': 185035904216203264,
    'Xupito': 302253184775356416,
    'Vesgo': 216632803113172993,
    'Ghago': 227864196845404160,
    'Gordito': 411710047547293707
}

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
        # 'Alpiona': 30320098,
        'Fallenzão': 396690444,
        # 'Maionese': 35304398,
        'Kiddy': 32757138,
        'Roshan': 151913285,
        'deliri019': 88091172,
        # 'Pogo': 121639063,
        # 'darkkside': 112645060,
        'Xupito': 130741370,
        # 'Vesgo': 84964267,
        # 'Ghago': 106159466,
        'Gordito': 130714929,
        # 'Scar': 29806143,
        'JohnMirolho': 56828892,
        'Sgt.Peçanha': 125536148
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
if MODE == 1:
    if TEAM_NAME == PNK and 2018 in YEARS:
        popular_vote = PopularVotePnK2018()
    elif TEAM_NAME == PNK and 2019 in YEARS:
        popular_vote = PopularVotePnK2019()
    elif TEAM_NAME == PNK and 2020 in YEARS:
        popular_vote = PopularVotePnK2020()
achievements = None

categories = [
    Category(20, 'win', unit='%', text='wins', has_max=False, apply_transform=T.percentage),
    Category(10, 'kills', unit='kills'),
    Category(10, 'deaths', unit='deaths', reverse=False),
    Category(10, 'assists', unit='assists'),
    Category(10, 'kda', text='KLA', rule='kla', max_format='%.2f'),
    Category(10, 'duration', text='time between each kill/assist', rule='time_kill_assist', unit='s',
             reverse=False, minimize=True, max_format='%.2f'),
    Category(10, 'versatility', rule='versatility', avg_format='%.3f'),
    # Category(1, 'discord_avg', unit='%', text='time spoken on Discord per total game duration', rule='discord_avg',
    #         reverse=False),
    # Category(1, 'discord', unit='min', text='time spoken on Discord', rule='discord'),
    Category(10, 'fantasy_value', unit='₭', text='total fantasy cards worth', rule='fantasy_value', avg_format='%i'),
    Category(5, 'kasino_net_worth', unit='₭', text='total PnKasino worth in ₭', rule='fantasy_worth', avg_format='%i'),
    Category(5, 'hard carry', unit='%', text='hard carry win rate', rule='position'),
    Category(5, 'mid', unit='%', text='mid win rate', rule='position'),
    Category(5, 'offlane', unit='%', text='offlane win rate', rule='position'),
    Category(5, 'support', unit='%', text='support win rate', rule='position'),
    Category(5, 'hard support', unit='%', text='hard support win rate', rule='position'),
    Category(4, 'xp_per_min', unit='xpm', text='xpm'),
    Category(4, 'total_gold', unit='gold', text='total gold'),
    Category(6, 'gold_per_min', unit='gpm', text='gpm'),
    Category(8, 'hero_damage', unit='dmg', text='hero damage'),
    Category(8, 'hero_healing', unit='heal', text='hero healing'),
    Category(5, 'tower_damage', unit='dmg', text='tower damage'),
    Category(5, 'damage_taken', unit='dmg', reverse=False, text='damage taken', rule='accumulate', minimize=True),
    Category(5, 'teamfight_participation', unit='%', text='team fight participation',
             apply_transform=T.percentage, max_format='%.2f'),
    Category(8, 'tf_max_damage', unit='dmg', text='damage in a teamfight', has_avg=False),
    Category(8, 'tf_max_healing', unit='heal', text='healing in a teamfight', has_avg=False),
    Category(4, 'actions', unit='activations', text='glyphs used', rule='24'),
    Category(4, 'actions', unit='uses', text='scans used', rule='31'),
    Category(8, 'life_state_dead', unit='min', text='minutes dead', minimize=True,
             apply_transform=T.sec_to_min, max_format='%.2f', reverse=False),
    Category(1, 'randomed', rule='bool', unit='%', text='randomed games', has_max=False, apply_transform=T.percentage),
    Category(5, 'last_hits', unit='last hits', text='last hits'),
    Category(2, 'denies', unit='denies'),
    Category(5, 'rune_pickups', unit='runes', text='runes picked up'),
    Category(8, 'obs_placed', unit='wards', text='observer wards placed'),
    Category(8, 'sen_placed', unit='sentries', text='sentry wards placed'),
    Category(2, 'multi_kills', unit='double kills', text='double kills', rule='2', has_max=False, avg_format='%.3f'),
    Category(3, 'multi_kills', unit='triple kills', text='triple kills', rule='3', has_max=False, avg_format='%.3f'),
    Category(4, 'multi_kills', unit='ultra kills', text='ultra kills', rule='4', has_max=False, avg_format='%.3f'),
    Category(5, 'multi_kills', unit='rampages', text='rampages', rule='5', has_max=False, avg_format='%.3f'),
    Category(5, 'purchase', unit='bkbs', text='BKBs purchased', rule='black_king_bar', has_max=False),
    Category(3, 'purchase', unit='dusts', text='dusts purchased', rule='dust', avg_format='%.3f'),
    Category(3, 'purchase', unit='smokes', text='smokes purchased', rule='smoke_of_deceit', avg_format='%.3f'),
    Category(2, 'purchase', unit='gems', text='gems of true sight purchased', rule='gem', avg_format='%.3f'),
    Category(8, 'purchase', unit='gold', text='gold in support items', rule='support_gold'),
    Category(8, 'firstblood_claimed', unit='first bloods', text='first blood kills', has_max=False, avg_format='%.3f'),
    Category(5, 'creeps_stacked', unit='creeps', text='creeps stacked'),
    Category(8, 'observer_kills', unit='wards', text='wards removed', rule='ward_kill'),
    Category(2, 'courier_kills', unit='couriers', text='couriers killed', avg_format='%.3f'),
    Category(2, 'purchase_tpscroll', unit='TPs', text='TPs purchased'),
    Category(2, 'purchase', unit='tomes', text='tomes of knowledge purchased', rule='tome_of_knowledge'),
    Category(5, 'stuns', unit='seconds', text='stun duration dealt', max_format='%.2f'),
    Category(3, 'pings', unit='pings'),
    Category(4, 'item_uses', unit='times', text='kavukochão', rule='trusty_shovel'),
    Category(5, 'abandons', unit='abandons', has_max=False, reverse=False, avg_format='%.3f'),
    Category(8, 'win_streak', unit='matches', text='win streak', rule='win_streak', avg_format='%s'),
    Category(8, 'loss_streak', unit='matches', text='loss streak', rule='loss_streak', reverse=False, avg_format='%s'),
    Category(4, 'lane_efficiency_pct', unit='%', text='lane efficiency at 10min'),
    Category(2, 'buyback_count', unit='buybacks', text='buybacks'),
    Category(3, 'kill_streaks', unit='streaks', text='beyond godlike streaks', rule='beyond_godlike', has_max=False),
    Category(10, 'kill_streaks', unit='kills', text='kill streak', rule='max_streak', has_avg=False),
    Category(2, 'actions_per_min', unit='apm', text='actions per minute'),
    Category(2, 'duration', unit='min', text='duration in minutes', apply_transform=T.sec_to_min, max_format='%.2f')
]


def get_title():
    return 'PnK Gaming Awards' if TEAM_NAME == 'PnK' else TEAM_NAME


def get_subtitle():
    if MONTH is not None:
        return "%i %s Edition" % (YEARS[0], calendar.month_abbr[MONTH])
    if len(YEARS) == 1:
        return "%i Edition" % YEARS[0]
    else:
        return "%i - %i Edition" % (min(YEARS), max(YEARS))


if __name__ == '__main__':
    start = time.time()
    YEARS = [2018, 2019] if BEST_TEAM is not None else YEARS
    players = player_list[TEAM_NAME]
    replacements = replacement_list[TEAM_NAME] if TEAM_NAME in replacement_list else None
    s = Slides(TEAM_NAME, YEARS, get_title(), get_subtitle(), players, month=MONTH)
    p = Parser(TEAM_NAME, YEARS, MONTH, players, MIN_MATCHES, MIN_PARTY_SIZE, MIN_MATCHES_WITH_HERO)

    downloader.download_heroes()
    downloader.download_player_data(players, replacements, override=DOWNLOAD_PLAYERS)
    discord_data = None  # downloader.download_discord()
    if TEAM_NAME == PNK:
        fantasy_data = downloader.download_fantasy()
        fantasy_scores = downloader.download_fantasy_scores()
    unique_matches = p.get_matches(replacements, month=MONTH, ranked_only=ONLY_RANKED)
    to_parse = downloader.download_matches(unique_matches, download_again=REDOWNLOAD_SMALL_FILES)
    matches_json = Parser.load_matches(unique_matches)
    tier_positions = p.identify_heroes(replacements, matches_json, forced_replacements,
                                       min_couple_matches=MIN_COUPLE_MATCHES)

    tiers = []
    for c in categories:
        if c.rule == 'position':
            tier = Tier(c.weight, tier_positions[c.parameter], 'Win rate as %s in %s matches'
                        % (c.parameter, TEAM_NAME))
            tiers.append((tier, c))
        elif c.rule == 'versatility':
            tier = Tier(c.weight, p.player_versatility(), 'Versatility in %s matches' % TEAM_NAME)
            tiers.append((tier, c))
        elif c.rule == 'discord' and TEAM_NAME == PNK:
            tier = Tier(c.weight, p.discord(discord_ids, discord_data), 'Total time spoken on Discord')
            tiers.append((tier, c))
        elif c.rule == 'fantasy_value' and TEAM_NAME == PNK:
            tier = Tier(c.weight, p.fantasy_value_tiers(fantasy_data), 'Sum of Fantasy Cards in PnKoins')
            tiers.append((tier, c))
        elif c.rule == 'fantasy_worth' and TEAM_NAME == PNK:
            tier = Tier(c.weight, p.fantasy_worth(fantasy_scores), 'Player worth in PnKoins on PnKasino')
            tiers.append((tier, c))
        elif c.rule == 'discord_avg' and TEAM_NAME == PNK:
            tier = Tier(c.weight, p.discord(discord_ids, discord_data, avg=True),
                        'Average percentage of time playing and speaking on Discord', reverse=False)
            tiers.append((tier, c))
        elif c.rule == 'win_streak':
            tier = Tier(c.weight, p.win_streak(), 'Best win streak in %s matches' % TEAM_NAME)
            tiers.append((tier, c))
        elif c.rule == 'loss_streak':
            tier = Tier(c.weight, p.loss_streak(), 'Worst loss streak in %s matches' % TEAM_NAME, reverse=False)
            tiers.append((tier, c))
        else:
            res_avg, res_max = p.stat_counter(matches_json, c.parameter, text=c.text, unit=c.unit, tf=c.transform,
                                              max_fmt=c.max_format, avg_fmt=c.avg_format, minimize=c.minimize,
                                              reverse=c.reverse, has_max=c.has_max, rule=c.rule, has_avg=c.has_avg)
            cat_name = c.text if c.text is not None else c.parameter
            if c.has_avg:
                tier_avg = Tier(c.weight, res_avg, 'Average %s in %s matches' % (cat_name, TEAM_NAME),
                                reverse=c.reverse)
                tiers.append((tier_avg, c))
            if c.has_max:
                tier_max = Tier(c.weight, res_max, 'Maximum %s in a single match' % cat_name, reverse=c.reverse,
                                is_max=True)
                tiers.append((tier_max, c))

    if TEAM_NAME == PNK:
        fantasy_values = p.fantasy(tiers)
        fantasy_scores = p.calculate_fantasy_score(fantasy_values, fantasy_scores)

    if BEST_TEAM is not None:
        combinations = p.best_team(BEST_TEAM)
        if len(combinations) > 0:
            s.add_divider_slide("%s Draft Helper (BETA)" % TEAM_NAME, 'Suggestions for Draft based on recent success')
            s.add_draft_suggestion(p.heroes, p.inv_p, combinations)
    else:
        s.add_divider_slide("%s General Statistics" % TEAM_NAME,
                            'Win Rate, Comebacks, Throws, Heroes, Compositions, Pairs')
        s.add_intro_slide(len(unique_matches), MIN_PARTY_SIZE, MIN_MATCHES, MIN_COUPLE_MATCHES)
        s.add_win_rate_slide(p.win_rate, len(unique_matches), p.matches_by_party_size, p.factions)
        s.add_win_rate_details_slide(p.first_blood_win_rate(), p.bounties())
        s.add_match_details(to_parse, p.match_types, p.match_skill)
        s.add_five_player_compositions(p.five_player_compositions, p.full_party_matches)
        s.add_match_summary_by_player(p.match_summary_by_player, p.match_summary_by_team, p.min_party_size)
        s.add_top_fifteen(p.top_comebacks, p.top_throws, p.top_fast_wins, p.top_fast_losses, p.longest_matches)
        s.add_advantage_chart(p.gold_variance, 'Gold Advantage')
        s.add_advantage_chart(p.xp_variance, 'Experience Advantage')
        s.add_best_team(p.evaluate_best_team_by_hero(MIN_COUPLE_MATCHES, True), 'Best', MIN_COUPLE_MATCHES)
        s.add_best_team(p.evaluate_best_team_by_hero(MIN_COUPLE_MATCHES, False), 'Worst', MIN_COUPLE_MATCHES)
        s.add_best_team_by_player(p.evaluate_best_team_by_hero_player(MIN_COUPLE_MATCHES / 2, True), 'Best',
                                  MIN_COUPLE_MATCHES / 2)
        s.add_best_team_by_player(p.evaluate_best_team_by_hero_player(MIN_COUPLE_MATCHES / 2, False), 'Worst',
                                  MIN_COUPLE_MATCHES / 2)
        s.add_lane_partners(p.lane_partners[0:15], 'Best', MIN_MATCHES / 2)
        s.add_lane_partners(p.lane_partners[-15:][::-1], 'Worst', MIN_MATCHES / 2)
        s.add_couples(p.player_couples[0:10], 'Best', MIN_COUPLE_MATCHES)
        s.add_couples(p.player_couples[-10:][::-1], 'Worst', MIN_COUPLE_MATCHES)
        s.add_hero_player_couples(p.hero_player_couples[0:10], 'Best', MIN_MATCHES_WITH_HERO)
        s.add_hero_player_couples(p.hero_player_couples[-10:][::-1], 'Worst', MIN_MATCHES_WITH_HERO)
        s.add_spammers(p.hero_spammers[0:10])
        s.add_trios(p.trios[0:15], 'Best', MIN_COUPLE_MATCHES)
        s.add_trios(p.trios[-15:][::-1], 'Worst', MIN_COUPLE_MATCHES)
        s.add_rivals(p.rivals[0:15])
        s.add_compositions(p.compositions)
        s.add_win_rate_by_date(p.win_rate_by_hour, 'Hour')
        s.add_win_rate_by_date(p.win_rate_by_weekday, 'Weekday')
        if MONTH is None:
            s.add_win_rate_by_date(p.win_rate_by_month, 'Month')
        s.add_hero_lanes(p.hero_lane_partners[0:10], 'Best', MIN_MATCHES_WITH_HERO)
        s.add_hero_lanes(p.hero_lane_partners[-10:][::-1], 'Worst', MIN_MATCHES_WITH_HERO)

        if MODE == 0 and TEAM_NAME == PNK:
            s.add_divider_slide("%s Fantasy Game" % TEAM_NAME, 'Fantasy Game based on Player Performance')
            s.add_fantasy_ranking(fantasy_scores)
            s.add_fantasy_slide(fantasy_values, 'hard carry')
            s.add_fantasy_slide(fantasy_values, 'mid')
            s.add_fantasy_slide(fantasy_values, 'offlane')
            s.add_fantasy_slide(fantasy_values, 'support')
            s.add_fantasy_slide(fantasy_values, 'hard support')
            s.add_fantasy_data(fantasy_data, 'hard carry')
            s.add_fantasy_data(fantasy_data, 'mid')
            s.add_fantasy_data(fantasy_data, 'offlane')
            s.add_fantasy_data(fantasy_data, 'support')
            s.add_fantasy_data(fantasy_data, 'hard support')

        if MODE == 0:
            s.add_divider_slide("%s Match Details" % TEAM_NAME, 'With players and positions per match')
            s.add_match_roles_summary(p.role_summary())

        s.add_divider_slide("%s Hero Summary" % TEAM_NAME, 'Most and least played heroes')
        s.add_win_rate_heroes(p.with_heroes, 'Playing')
        s.add_most_played([v for v in p.most_played_heroes if v['matches'] > 0], True)
        s.add_most_played([v for v in p.most_played_heroes if v['matches'] == 0], False)
        s.add_win_rate_heroes(p.against_heroes, 'Against')

        s.add_divider_slide("%s Players" % TEAM_NAME, 'Roles, Pairings and Most Played Heroes')
        s.add_player_summary(p.player_descriptor, MIN_MATCHES)
        s.add_player_mmr(p.mmr_change())
        for item in sorted(p.player_descriptor, key=lambda e: e['rating'], reverse=True):
            if item['matches'] > 0:
                s.add_player_data_slide(item, MIN_MATCHES_WITH_HERO)
                s.add_player_tables_slide(item, {
                    c['position']: c['current_value']
                    for c in fantasy_data if c['name'] == item['name']})
                if MONTH is None:
                    s.add_player_activity_data(item)

        s.add_divider_slide("%s Technical Categories" % TEAM_NAME, 'Averages and Maximum for many statistics')
        for tier, category in tiers:
            if PRINT_TIERS:
                tier.print()
            s.add_tier_slides(tier, category)
        medals = Tier.show_results(players, [t for t, c in tiers])
        points = Tier.show_results_weights(players, [t for t, c in tiers])
        s.add_results_slides(medals, points)

        if MONTH is None:
            s.add_divider_slide("Individual Hero Statistics", 'Positions, Win Rate and Best Players at each Hero')
            s.add_heroes(p.hero_statistics, MIN_MATCHES_WITH_HERO)

        s.add_divider_slide("%s Items" % TEAM_NAME, 'Win rate based on items at the end of the game')
        s.add_item_slides(p.generate_item_statistics())

        if TEAM_NAME == PNK:
            achievements = PnKAchievements(players, p.match_summary)

        if achievements is not None:
            s.add_divider_slide("%s Achievements" % TEAM_NAME, 'Awarded to the most exquisite accomplishments')
            for achievement in achievements.get_achievements():
                result = achievement.evaluate()
                s.add_achievement_slide(achievement, result)

        if popular_vote is not None:
            s.add_divider_slide("%s Popular Vote" % TEAM_NAME, popular_vote.message)
            for category in popular_vote.votes:
                s.add_popular_vote_category_slides(category)
            s.add_top_five_slides(popular_vote.get_top_five())

    s.save()

    print('')
    print("Running Time took %.2f seconds." % (time.time() - start))
