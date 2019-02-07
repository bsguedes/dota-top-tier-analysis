import abc

NO_DISABLE_HEROES = [
    'Abbadon',
    'Bristleback',
    'Huskar',
    'Io',
    'Lifestealer',
    'Lycan',
    'Omniknight',
    'Timbersaw',
    'Undying',
    'Arc Warden',
    'Bloodseeker',
    'Broodmother',
    'Clinkz',
    'Drow Ranger',
    'Juggernaut',
    'Phantom Assassin',
    'Phantom Lancer',
    'Razor',
    'Riki',
    'Shadow Fiend',
    'Sniper',
    'Spectre',
    'Templar Assassin',
    'Terrorblade',
    'Ursa',
    'Venomancer',
    'Viper',
    'Weaver',
    'Chen',
    'Dazzle',
    'Death Prophet',
    'Enchantress',
    'Nature\'s Prophet',
    'Pugna',
    'Queen of Pain',
    'Silencer',
    'Skywrath Mage',
    'Tinker'
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
    'Wraith King'
]

UNDEAD_HEROES = [
    'Undying',
    'Lich',
    'Wraith King',
    'Death Prophet'
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
    'Sniper'
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
    'Dark Willow'
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
            ach.init(self.player_list, self.match_list)


class PnKAchievements(AchievementBase):
    def __init__(self, players, matches):
        AchievementBase.__init__(self, players, matches)
        self.add_ach(WinWithPlayerAchievement('Toxic Couple', ['Baco', 'Alidio']))
        self.add_ach(WinWithPlayerAchievement('Forever Archon', ['Scrider', 'Older', 'tchepo']))
        self.add_ach(WinWithPlayerAchievement('Feldmann Brothers', ['Lotus', 'Pringles']))
        self.add_ach(WinWithoutPlayerAchievement('Captain Replacement!', ['Zé']))
        self.add_ach(WinCarriedByAchievement('Best Hooks for Enemy Team', 'Cristian', 'Pudge'))
        self.add_ach(WinCarriedByAchievement('Pushing Far From Your Friends', 'Nuvah', 'Lina'))
        self.add_ach(WinCarriedByAchievement('Heavier than a Black Hole', 'Alidio', 'Wraith King'))
        self.add_ach(WinCarriedByAchievement('What is a Hero Pool?', 'Chuvisco', 'Necrophos'))
        self.add_ach(ItemAchievement('Next Lebel Farming', 'radiance', 'Radiance', 2))
        self.add_ach(ItemAchievement('Multiple Midas', 'hand_of_midas', 'Hand of Midas', 3))
        self.add_ach(ItemAchievement('Maximum Blink', 'blink', 'Blink Dagger', 5))
        self.add_ach(ComeBackFromMegaCreepsAchievement('Overwhelming Odds'))
        self.add_ach(WinBattleCupPartyAchievement('Battle Cup Winners'))
        self.add_ach(PlayerOnLowestParameterAchievement('Naked Baco', 'Baco', 'total_gold'))
        self.add_ach(PlayerOnHeroAchievement('Brainless Baco', 'Baco', UNDEAD_HEROES))
        self.add_ach(PlayerOnHeroAchievement('Mustache Baco', 'Baco', MUSTACHE_HEROES, 'a hero with a mustache'))
        self.add_ach(WinWithHeroAchievement('Girl Power', FEMALE_HEROES, 'are female heroes'))
        self.add_ach(WinWithHeroAchievement('Melee Only', MELEE_HEROES, 'are melee heroes'))
        self.add_ach(WinWithHeroAchievement('No Disables', NO_DISABLE_HEROES, 'have no reliable stuns'))
        super(PnKAchievements, self).initialize_achievements()


class Achievement:
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name
        self.description = ''
        self.games = 0
        self.wins = 0
        self.player_list = None
        self.match_list = None
        self.winners = None

    @abc.abstractmethod
    def evaluate(self):
        return {'matches': self.games, 'wins': self.wins, 'winners': self.winners}

    def init(self, players, matches):
        self.player_list = players
        self.match_list = matches
        self.winners = {i: [] for p, i in self.player_list.items()}


class ItemAchievement(Achievement):
    def __init__(self, name, item_code, item_name, amount):
        Achievement.__init__(self, name)
        self.item_code = item_code
        self.item_name = item_name
        self.amount = amount
        self.description = 'Win a game with %i %s on your team' % (amount, item_name)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if data['items'] is not None:
                if len([1 for x in data['items'][self.item_code].values() if x > 0]) >= self.amount:
                    self.games += 1
                    if data['win']:
                        self.wins += 1
                        for player in data['players']:
                            self.winners[player].append(match_id)
        return super(ItemAchievement, self).evaluate()


class WinWithPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a game with %s on your team' % sequence(players)

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
            self.description = 'Win a game with %s on your team' % sequence(heroes)
        else:
            self.description = 'Win a game where all heroes %s' % msg

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


class PlayerOnLowestParameterAchievement(Achievement):
    def __init__(self, name, player, parameter):
        Achievement.__init__(self, name)
        self.player = player
        self.parameter = parameter
        self.description = 'Win a game with %s having lowest %s' % (player, parameter)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players']:
                self.games += 1
                value = data['player_desc'][self.player_list[self.player]][self.parameter]
                if data['win'] and value == min([v[self.parameter] for k, v in data['player_desc'].items()]):
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(PlayerOnLowestParameterAchievement, self).evaluate()


class PlayerOnHeroAchievement(Achievement):
    def __init__(self, name, player, heroes, msg=None):
        Achievement.__init__(self, name)
        self.player = player
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a game with %s playing one of %s' % (player, sequence(heroes))
        else:
            self.description = 'Win a game with %s playing %s' % (player, msg)

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
    def __init__(self, name, player, hero):
        Achievement.__init__(self, name)
        self.player = player
        self.hero = hero
        self.description = 'Win a game being carried by %s on %s' % (player, hero)

    def evaluate(self):
        for match_id, data in self.match_list.items():
            if self.player_list[self.player] in data['players'] \
                    and data['player_desc'][self.player_list[self.player]]['hero'] == self.hero:
                self.games += 1
                nw = data['player_desc'][self.player_list[self.player]]['total_gold']
                if data['win'] and nw == max([v['total_gold'] for k, v in data['player_desc'].items()]):
                    self.wins += 1
                    for player_id in data['players']:
                        if player_id != self.player_list[self.player]:
                            self.winners[player_id].append(match_id)
        return super(WinCarriedByAchievement, self).evaluate()


class ComeBackFromMegaCreepsAchievement(Achievement):
    def __init__(self, name):
        Achievement.__init__(self, name)
        self.description = 'Win a game against Mega Creeps'

    def evaluate(self):
        return super(ComeBackFromMegaCreepsAchievement, self).evaluate()


class WinWithoutPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a game as 5 players without %s on team' % sequence(players)

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


def sequence(strings):
    return '%s and %s' % (', '.join(strings[:-1]), strings[-1]) if len(strings) > 1 else strings[0]
