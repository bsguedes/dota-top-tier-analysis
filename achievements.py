import abc
from constants import *

NO_DISABLE_HEROES = [
    'Abbadon',
    'Bristleback',
    'Huskar',
    'Io',
    'Lifestealer',
    'Lycan',
    'Night Stalker',
    'Omniknight',
    'Timbersaw',
    'Undying',
    'Anti-Mage',
    'Arc Warden',
    'Bloodseeker',
    'Bounty Hunter',
    'Broodmother',
    'Clinkz',
    'Drow Ranger',
    'Juggernaut',
    'Lone Druid',
    'Phantom Assassin',
    'Phantom Lancer',
    'Razor',
    'Riki',
    'Shadow Fiend',
    'Sniper',
    'Spectre',
    'Templar Assassin',
    'Terrorblade',
    'Troll Warlord',
    'Ursa',
    'Venomancer',
    'Viper',
    'Weaver',
    'Chen',
    'Dark Seer',
    'Dazzle',
    'Death Prophet',
    'Disruptor',
    'Enchantress',
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
            ach.initialize(self.player_list, self.match_list)


class PnKAchievements(AchievementBase):
    def __init__(self, players, matches):
        AchievementBase.__init__(self, players, matches)
        self.add_ach(WinWithPlayerAchievement('Toxic Couple', ['Baco', 'Alidio']))
        self.add_ach(WinWithPlayerAchievement('I AM ARCHON', ['Scrider', 'Older', 'tchepo']))
        self.add_ach(WinWithPlayerAchievement('Feldmann Brothers', ['Lotus', 'Pringles']))
        self.add_ach(WinWithoutPlayerAchievement('Subs Captain', ['Zé']))
        self.add_ach(WinCarriedByAchievement('Best Hooks for Enemy Team', 'Cristian', 'Pudge'))
        self.add_ach(WinCarriedByAchievement('Pushing Far From Your Friends', 'Nuvah', 'Lina'))
        self.add_ach(WinCarriedByAchievement('Heavier than a Black Hole', 'Alidio', 'Wraith King'))
        self.add_ach(WinCarriedByAchievement('What is a Hero Pool?', 'Chuvisco', 'Necrophos'))
        self.add_ach(StreakAchievement('All Green Profile', 8))
        self.add_ach(StreakAchievement('All Red Profile', -8))
        self.add_ach(ItemAchievement('Trump Card', 'rapier', 'Divine Rapier', 1))
        self.add_ach(ItemAchievement('Next Lebel Farming', 'radiance', 'Radiance', 2))
        self.add_ach(ItemAchievement('Multiple Midas', 'hand_of_midas', 'Hand of Midas', 3))
        self.add_ach(ItemAchievement('Maximum Blink', 'blink', 'Blink Dagger', 5))
        self.add_ach(MultiKillAchievement('RAMPAGE!', '5'))
        self.add_ach(ComeBackFromMegaCreepsAchievement('Overwhelming Odds'))
        self.add_ach(WinBattleCupPartyAchievement('Battle Cup Winners'))
        self.add_ach(PlayerOnLowestParameterAchievement('Naked Baco', 'Baco', 'total_gold', 'net worth',
                                                        img='naked_baco.png'))
        self.add_ach(PlayerOnHeroAchievement('Brainless Baco', 'Baco', UNDEAD_HEROES, 'an undead hero',
                                             img='brainless_baco.png'))
        self.add_ach(PlayerOnHeroAchievement('Mustache Baco', 'Baco', MUSTACHE_HEROES, 'a hero with a mustache',
                                             img='mustache_baco.png'))
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
        return {'matches': self.games, 'wins': self.wins, 'winners': self.winners,
                'wr': 0 if self.games == 0 else 100 * self.wins / self.games}

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


class StreakAchievement(Achievement):
    def __init__(self, name, amount):
        Achievement.__init__(self, name)
        self.amount = amount
        self.description = 'Get a %s Streak of %i Matches' % ('Win' if amount > 0 else 'Loss', abs(amount))

    def evaluate(self):
        player_count = {i: 0 for p, i in self.player_list.items()}
        for match_id, data in self.match_list.items():
            self.games += 1
            if (data['win'] and self.amount > 0) or (self.amount < 0 and not data['win']):
                for player in data['players']:
                    player_count[player] += 1
                    if player_count[player] == abs(self.amount):
                        self.winners[player].append(match_id)
            else:
                for player in data['players']:
                    player_count[player] = 0
        self.wins = sum([len(w) for p, w in self.winners.items()])
        return super(StreakAchievement, self).evaluate()


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


class PlayerOnLowestParameterAchievement(Achievement):
    def __init__(self, name, player, parameter, parameter_name, img=None):
        Achievement.__init__(self, name, img=img)
        self.player = player
        self.parameter = parameter
        self.description = 'Win a game with %s having lowest %s' % (player, parameter_name)

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
    def __init__(self, name, player, heroes, msg=None, img=None):
        Achievement.__init__(self, name, img=img)
        self.player = player
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a game with %s playing one of %s' % (player, sequence(heroes))
        else:
            self.description = 'Win a game with %s playing %s' % (player, msg)
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
        for match_id, data in self.match_list.items():
            if data['barracks'] == 0:
                self.games += 1
                if data['win']:
                    self.wins += 1
                    for player_id in data['players']:
                        self.winners[player_id].append(match_id)
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
