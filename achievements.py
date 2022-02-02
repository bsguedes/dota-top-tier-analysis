import abc
from constants import *

NO_DISABLE_HEROES = [
    'Abbadon',
    'Brewmaster',
    'Bristleback',
    'Clockwerk',
    'Doom',
    'Earth Spirit',
    'Huskar',
    'Io',
    'Kunkka',
    'Lifestealer',
    'Lycan',
    'Night Stalker',
    'Omniknight',
    'Phoenix',
    'Timbersaw',
    'Treant Protector',
    'Underlord',
    'Undying',
    'Anti-Mage',
    'Arc Warden',
    'Bloodseeker',
    'Bounty Hunter',
    'Broodmother',
    'Clinkz',
    'Drow Ranger',
    'Ember Spirit',
    'Juggernaut',
    'Lone Druid',
    'Medusa',
    'Meepo',
    'Mirana',
    'Naga Siren',
    'Phantom Assassin',
    'Phantom Lancer',
    'Razor',
    'Riki',
    'Shadow Fiend',
    'Slark',
    'Sniper',
    'Spectre',
    'Templar Assassin',
    'Terrorblade',
    'Troll Warlord',
    'Ursa',
    'Venomancer',
    'Viper',
    'Weaver',
    'Ancient Apparition',
    'Chen',
    'Crystal Maiden',
    'Dark Seer',
    'Dark Willow',
    'Dazzle',
    'Death Prophet',
    'Disruptor',
    'Enchantress',
    'Grimstroke',
    'Leshrac',
    'Lina',
    'Nature\'s Prophet',
    'Oracle',
    'Pugna',
    'Queen of Pain',
    'Silencer',
    'Skywrath Mage',
    'Techies',
    'Tinker',
    'Zeus'
]

MELEE_HEROES = [
    'Monkey King',
    'Doom',
    'Tiny',
    'Abaddon',
    'Alchemist',
    'Anti-Mage',
    'Axe',
    'Beastmaster',
    'Bloodseeker',
    'Bounty Hunter',
    'Brewmaster',
    'Bristleback',
    'Broodmother',
    'Centaur Warrunner',
    'Chaos Knight',
    'Clockwerk',
    'Dark Seer',
    'Earth Spirit',
    'Earthshaker',
    'Elder Titan',
    'Ember Spirit',
    'Faceless Void',
    'Juggernaut',
    'Kunkka',
    'Legion Commander',
    'Lifestealer',
    'Lycan',
    'Magnus',
    'Mars',
    'Meepo',
    'Naga Siren',
    'Night Stalker',
    'Nyx Assassin',
    'Ogre Magi',
    'Omniknight',
    'Phantom Assassin',
    'Phantom Lancer',
    'Pudge',
    'Riki',
    'Sand King',
    'Slardar',
    'Slark',
    'Spectre',
    'Spirit Breaker',
    'Sven',
    'Tidehunter',
    'Timbersaw',
    'Treant Protector',
    'Tusk',
    'Underlord',
    'Undying',
    'Ursa',
    'Wraith King',
    'Void Spirit',
    'Marci',
    'Dawnbreaker'
]

UNDEAD_HEROES = [
    'Undying',
    'Lich',
    'Wraith King',
    'Death Prophet',
    'Pugna',
    'Clinkz',
    'Necrophos'
]

MUSTACHE_HEROES = [
    'Gyrocopter',
    'Zeus',
    'Storm Spirit',
    'Kunkka',
    'Lone Druid',
    'Omniknight',
    'Dark Seer',
    'Brewmaster',
    'Tusk',
    'Beastmaster',
    'Sniper',
    'Void Spirit'
]

FEMALE_HEROES = [
    'Legion Commander',
    'Drow Ranger',
    'Mirana',
    'Vengeful Spirit',
    'Templar Assassin',
    'Luna',
    'Naga Siren',
    'Phantom Assassin',
    'Broodmother',
    'Spectre',
    'Medusa',
    'Crystal Maiden',
    'Windranger',
    'Lina',
    'Enchantress',
    'Queen of Pain',
    'Death Prophet',
    'Winter Wyvern',
    'Dark Willow',
    'Snapfire',
    'Hoodwink',
    'Dawnbreaker',
    'Marci'
]


class AchievementBase:
    def __init__(self, players, matches):
        self.achievement_list = list()
        self.player_list = players
        self.match_list = matches

    def get_achievements(self):
        return self.achievement_list

    def add_ach(self, achievement):
        self.achievement_list.append(achievement)

    def initialize_achievements(self):
        for ach in self.achievement_list:
            ach.initialize(self.player_list, self.match_list)


class PnKAchievements(AchievementBase):
    def __init__(self, players, matches):
        AchievementBase.__init__(self, players, matches)
        self.add_ach(WinWithPlayerAchievement('Toxic Couple', ['Baco', 'Alidio']))
        # self.add_ach(WinWithPlayerAchievement('I AM ARCHON', ['Scrider', 'Older']))
        self.add_ach(WinWithPlayerAchievement('Feldmann Brothers', ['Lotus', 'Pringles']))
        # self.add_ach(WinWithPlayerAchievement('Scrider Brothers', ['Scrider', 'Gordito']))
        self.add_ach(WinWithPlayerAchievement('Alves Brothers', ['Kiddy', 'Xupito']))
        self.add_ach(WinWithPlayerAchievement('Cold Blood', ['Baco', 'Alidio', 'Chuvisco']))
        self.add_ach(WinWithoutPlayerAchievement('No Immortals Allowed', ['kkz', 'Kiddy']))
        self.add_ach(StreakAchievement('Bela Tentativa', -2, same_hero=True))
        self.add_ach(MaelkAchievement('Maelk Award', 20))
        self.add_ach(ItemSequenceAchievement('Primeiro Rad, depois Aghanim', ['radiance', 'ultimate_scepter'],
                                             'Build a Radiance and an Aghanim`s Scepter, in this order.'))
        self.add_ach(WinWithoutPlayerAchievement('Subs Captain', ['Zé']))
        # self.add_ach(PlayerOnParameterAchievement('Vem Tranquilo', 'Scrider', 'kills', 'kill count',
        #                                          lowest=False, win=True))
        self.add_ach(WinCarriedByAchievement('Pushing Far From Your Friends', 'Nuvah', 'Lina'))
        self.add_ach(WinCarriedByAchievement('Heavier than a Black Hole', 'Alidio', 'Wraith King'))
        self.add_ach(WinCarriedByAchievement('My Big Hero Pool', 'Chuvisco', 'Ursa', unless=True))
        self.add_ach(WinCarriedByAchievement('Best Hooks for Enemy Team', 'Cristian', 'Pudge'))
        self.add_ach(WinWithPlayerOnRoleAchievement('Olderiagace', 'Older', 'hard carry'))
        self.add_ach(StreakAchievement('All Green Profile', 8))
        self.add_ach(StreakAchievement('All Red Profile', -8))
        self.add_ach(AllRunesAchievement('I am Inevitable'))
        self.add_ach(ItemAchievement('Trump Card', 'rapier', 'Divine Rapier', 1))
        self.add_ach(ItemAchievement('Next Lebel Farming', 'radiance', 'Radiance', 2))
        self.add_ach(ItemAchievement('Multiple Midas', 'hand_of_midas', 'Hand of Midas', 3))
        self.add_ach(ItemAchievement('Maximum Blink', 'blink', 'Blink Dagger', 5))
        self.add_ach(MultiKillAchievement('RAMPAGE!', '5'))
        self.add_ach(WinWithBuildingStatus('Overwhelming Odds', 'barracks', 0, 'against Mega Creeps'))
        self.add_ach(
            WinWithBuildingStatus('No Tower Shall Fall', 'towers', 2047, 'losing no tower', count_on_building=False))
        self.add_ach(WinBattleCupPartyAchievement('Battle Cup Winners'))
        self.add_ach(PlayerOnParameterAchievement('Naked Baco', 'Baco', 'total_gold', 'net worth',
                                                  img='naked_baco.png'))
        self.add_ach(PlayerOnParameterAchievement('CEOsmar', 'Baco', 'total_gold', 'net worth', lowest=False,
                                                  img='ceosmar.png'))
        self.add_ach(PlayerOnHeroAchievement('Brainless Baco', 'Baco', UNDEAD_HEROES, 'an undead hero',
                                             img='brainless_baco.png'))
        self.add_ach(PlayerOnHeroAchievement('Mustache Baco', 'Baco', MUSTACHE_HEROES, 'a hero with a mustache',
                                             img='mustache_baco.png'))
        self.add_ach(PlayerOnParameterAchievement('Fap Baco', 'Baco', 'apm', 'actions per min', win=False, lowest=False,
                                                  img='fap_baco.png'))
        self.add_ach(WinWithHeroAchievement('Girl Power', FEMALE_HEROES, 'are female heroes'))
        self.add_ach(WinWithHeroAchievement('Melee Only', MELEE_HEROES, 'are melee heroes'))
        self.add_ach(WinWithHeroAchievement('No Disables', NO_DISABLE_HEROES, 'have no reliable stuns'))
        super(PnKAchievements, self).initialize_achievements()


class Achievement:
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, img=None):
        self.name = name
        self.img_path = img
        self.description = ''
        self.games = 0
        self.wins = 0
        self.player_list = None
        self.match_list = None
        self.winners = None
        self.special_description = False

    @abc.abstractmethod
    def evaluate(self):
        return {
            'matches': self.games,
            'wins': self.wins,
            'winners': self.winners,
            'wr': win_rate(self.wins, self.games)
        }

    def initialize(self, players, matches):
        self.player_list = players
        self.match_list = matches
        self.winners = {i: [] for p, i in self.player_list.items()}


class MultiKillAchievement(Achievement):
    def __init__(self, name, amount):
        Achievement.__init__(self, name)
        self.amount = amount
        self.description = 'Get a multi-kill streak of %s kills' % amount

    def evaluate(self):
        for match_id, data in self.match_list.items():
            self.games += 1
            for player in data['players']:
                if self.amount in data['multi_kills'][player]:
                    self.wins += data['multi_kills'][player][self.amount]
                    for i in range(data['multi_kills'][player][self.amount]):
                        self.winners[player].append(match_id)
        return super(MultiKillAchievement, self).evaluate()


class MaelkAchievement(Achievement):
    def __init__(self, name, amount):
        Achievement.__init__(self, name)
        self.amount = amount
        self.description = 'Win a game with no kills and %s or more deaths' % amount

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if data['win']:
                self.games += 1
                for player_id in data['players']:
                    kills = data['player_desc'][player_id]['kills']
                    deaths = data['player_desc'][player_id]['deaths']
                    if kills == 0 and deaths >= self.amount:
                        self.wins += 1
                        self.winners[player_id].append(match_id)
        return super(MaelkAchievement, self).evaluate()


class WinWithPlayerOnRoleAchievement(Achievement):
    def __init__(self, name, player, role):
        Achievement.__init__(self, name)
        self.player = player
        self.role = role
        self.description = 'Win a match with %s playing as %s' % (player, role)

    def evaluate(self):
        pid = self.player_list[self.player]
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players'] and 'roles' in data and \
                    data['roles']['positions'][pid] == self.role:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(WinWithPlayerOnRoleAchievement, self).evaluate()


class StreakAchievement(Achievement):
    def __init__(self, name, amount, same_hero=False):
        Achievement.__init__(self, name)
        self.amount = amount
        fmt = 'Get a %s streak of %i matches with the same hero' if same_hero else 'Get a %s streak of %i matches'
        values = ('Win' if amount > 0 else 'Loss', abs(amount))
        self.description = fmt % values
        self.same_hero = same_hero

    def evaluate(self):
        player_count = {i: 0 for p, i in self.player_list.items()}
        player_hero = {i: None for p, i in self.player_list.items()}
        for match_id, data in self.match_list.items():
            self.games += 1
            if (data['win'] and self.amount > 0) or (self.amount < 0 and not data['win']):
                for player in data['players']:
                    if self.same_hero:
                        hero = data['player_desc'][player]['hero']
                        if player_hero[player] != hero:
                            player_count[player] = 0
                        player_hero[player] = hero
                    player_count[player] += 1
                    if player_count[player] == abs(self.amount):
                        self.winners[player].append(match_id)
            else:
                for player in data['players']:
                    player_count[player] = 0
        self.wins = sum([len(w) for p, w in self.winners.items()])
        return super(StreakAchievement, self).evaluate()


class ItemSequenceAchievement(Achievement):
    def __init__(self, name, items, description):
        Achievement.__init__(self, name)
        self.items = items
        self.description = description

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if data['items'] is not None:
                self.games += 1
                some_win = False
                for player in data['players']:
                    min_times = []
                    for it in self.items:
                        if len(data['items'][it][player]['times']) > 0 and data['items'][it][player]['count'] > 0:
                            min_times.append(data['items'][it][player]['times'])
                    if len(min_times) == len(self.items) and all(
                            min_times[i] <= min_times[i + 1] for i in range(len(min_times) - 1)):
                        self.winners[player].append(match_id)
                        some_win = True
                if some_win:
                    self.wins += 1
        return super(ItemSequenceAchievement, self).evaluate()


class ItemAchievement(Achievement):
    def __init__(self, name, item_code, item_name, amount):
        Achievement.__init__(self, name)
        self.item_code = item_code
        self.item_name = item_name
        self.amount = amount
        self.description = 'Win a match with %i %s on your team' % (amount, item_name)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if data['items'] is not None:
                if len([1 for x in data['items'][self.item_code].values() if x['count'] > 0]) >= self.amount:
                    self.games += 1
                    if data['win']:
                        self.wins += 1
                        for player in data['players']:
                            self.winners[player].append(match_id)
        return super(ItemAchievement, self).evaluate()


class AllRunesAchievement(Achievement):
    def __init__(self, name):
        Achievement.__init__(self, name)
        self.description = 'Get all 7 runes in a match'

    def evaluate(self):
        for match_id, data in self.match_list.items():
            counted = False
            self.games += 1
            for player in data['players']:
                value = data['player_desc'][player]['runes']
                if value is not None and len(value) == 7:
                    if not counted:
                        self.wins += 1
                        counted = True
                    self.winners[player].append(match_id)
        return super(AllRunesAchievement, self).evaluate()


class WinWithPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a match with %s on your team' % sequence(players)

    def evaluate(self):
        inv_p = {v: k for k, v in self.player_list.items()}
        for match_id, data in self.match_list.items():
            valid_game = True
            for player_name in self.players:
                if self.player_list[player_name] not in data['players']:
                    valid_game = False
            if valid_game:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        if inv_p[player_id] not in self.players:
                            self.winners[player_id].append(match_id)
        return super(WinWithPlayerAchievement, self).evaluate()


class WinWithHeroAchievement(Achievement):
    def __init__(self, name, heroes, msg=None):
        Achievement.__init__(self, name)
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a match with %s on your team' % sequence(heroes)
        else:
            self.description = 'Win a match where all heroes %s' % msg
            self.special_description = True

    def evaluate(self):
        for match_id, data in self.match_list.items():
            match_heroes = data['our_team_heroes']
            valid_game = len(match_heroes) == 5
            for hero in match_heroes:
                if hero not in self.heroes:
                    valid_game = False
            if valid_game:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        self.winners[player_id].append(match_id)
        return super(WinWithHeroAchievement, self).evaluate()


class WinBattleCupPartyAchievement(Achievement):
    def __init__(self, name):
        Achievement.__init__(self, name)
        self.description = 'Win a Battle Cup match'

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if data['lobby_type'] == 'battle_cup':
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        self.winners[player_id].append(match_id)
        return super(WinBattleCupPartyAchievement, self).evaluate()


class PlayerOnParameterAchievement(Achievement):
    def __init__(self, name, player, parameter, parameter_name, img=None, win=True, lowest=True):
        Achievement.__init__(self, name, img=img)
        self.player = player
        self.parameter = parameter
        self.lowest = lowest
        self.win = win
        txt = 'lowest' if lowest else 'highest'
        prefix = 'Win' if win else 'Play'
        self.description = '%s a match with %s having %s %s' % (prefix, player, txt, parameter_name)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players']:
                self.games += 1
                value = data['player_desc'][self.player_list[self.player]][self.parameter]
                comp = min([v[self.parameter] for k, v in data['player_desc'].items()]) if self.lowest else max(
                    [v[self.parameter] for k, v in data['player_desc'].items()])
                if (not self.win or data['win']) and value == comp and comp > 0:
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(PlayerOnParameterAchievement, self).evaluate()


class PlayerOnHeroAchievement(Achievement):
    def __init__(self, name, player, heroes, msg=None, img=None):
        Achievement.__init__(self, name, img=img)
        self.player = player
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a match with %s playing one of %s' % (player, sequence(heroes))
        else:
            self.description = 'Win a match with %s playing %s' % (player, msg)
            self.special_description = True

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players'] \
                    and data['player_desc'][self.player_list[self.player]]['hero'] in self.heroes:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(PlayerOnHeroAchievement, self).evaluate()


class WinCarriedByAchievement(Achievement):
    def __init__(self, name, player, hero, unless=False):
        Achievement.__init__(self, name)
        self.player = player
        self.hero = hero
        self.unless = unless
        self.description = 'Win a match being carried by %s on any hero except %s' % (
            player, hero) if unless else 'Win a match being carried by %s on %s' % (player, hero)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players'] \
                    and ((
                    data['player_desc'][self.player_list[self.player]]['hero'] == self.hero and not self.unless) or (
                    data['player_desc'][self.player_list[self.player]]['hero'] != self.hero and self.unless)):
                self.games += 1
                nw = data['player_desc'][self.player_list[self.player]]['total_gold']
                if data['win'] and nw == max([v['total_gold'] for k, v in data['player_desc'].items()]):
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(WinCarriedByAchievement, self).evaluate()


class WinWithBuildingStatus(Achievement):
    def __init__(self, name, building, value, text, count_on_building=True):
        Achievement.__init__(self, name)
        self.building = building
        self.value = value
        self.count_on_building = count_on_building
        self.description = 'Win a match %s' % text

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if not self.count_on_building and data['win']:
                self.games += 1
            if data[self.building] == self.value:
                if self.count_on_building:
                    self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        self.winners[player_id].append(match_id)
        return super(WinWithBuildingStatus, self).evaluate()


class WinWithoutPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a match as 5 players without %s on team' % sequence(players)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            valid_game = len(data['players']) == 5
            for player_name in self.players:
                if self.player_list[player_name] in data['players']:
                    valid_game = False
            if valid_game:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        self.winners[player_id].append(match_id)
        return super(WinWithoutPlayerAchievement, self).evaluate()
