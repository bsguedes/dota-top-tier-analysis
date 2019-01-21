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
    def __init__(self, matches):
        self.achievement_list = list()
        self.matches = matches

    def get_achievements(self):
        return self.achievement_list

    def append_achievement(self, achievement):
        self.achievement_list.append(achievement)


class PnKAchievements(AchievementBase):
    def __init__(self, matches):
        AchievementBase.__init__(self, matches)
        self.append_achievement(WinWithPlayerAchievement('Toxic Couple', ['Baco', 'Alidio']))
        self.append_achievement(WinWithPlayerAchievement('Forever Archon', ['Scrider', 'Older', 'tchepo']))
        self.append_achievement(WinWithPlayerAchievement('Feldmann Brothers', ['Lotus', 'Pringles']))
        self.append_achievement(WinWithoutPlayerAchievement('Cap is missing!', 'Zé'))
        self.append_achievement(WinCarriedByAchievement('Best hooks for enemy team', 'Cristian', 'Pudge'))
        self.append_achievement(WinCarriedByAchievement('Mid Lina', 'Nuvah', 'Lina'))
        self.append_achievement(WinCarriedByAchievement('Worst hero in Dota', 'Alidio', 'Wraith King'))
        self.append_achievement(WinCarriedByAchievement('New ranged offlane', 'Chuvisco', 'Necrophos'))
        self.append_achievement(ItemAchievement('Next lebel Farming', 'radiance', 2))
        self.append_achievement(ItemAchievement('Multiple Midas', 'midas', 3))
        self.append_achievement(ItemAchievement('Maximum Blink', 'blink', 4))
        self.append_achievement(ComeBackFromMegaCreepsAchievement('Overwhelming Odds'))
        self.append_achievement(WinBattleCupPartyAchievement('Battle Cup Winners'))
        self.append_achievement(PlayerOnLowestParameterAchievement('Naked Baco', 'Baco', 'total_gold'))
        self.append_achievement(PlayerOnHeroAchievement('Brainless Baco', 'Baco', UNDEAD_HEROES))
        self.append_achievement(PlayerOnHeroAchievement('Mustache Baco', 'Baco', MUSTACHE_HEROES))
        self.append_achievement(WinWithHeroAchievement('Girl Power', FEMALE_HEROES))
        self.append_achievement(WinWithHeroAchievement('Melee Only', MELEE_HEROES))
        self.append_achievement(WinWithHeroAchievement('No Disables', NO_DISABLE_HEROES))


class Achievement:
    def __init__(self, name):
        self.name = name
        self.description = ''


class ItemAchievement(Achievement):
    def __init__(self, name, item_name, amount):
        Achievement.__init__(self, name)
        self.item_name = item_name
        self.amount = amount
        self.description = 'Win a game with %i %s on your team' % (item_name, amount)


class WinWithPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a game with %s on your team' % sequence(players)


class WinWithHeroAchievement(Achievement):
    def __init__(self, name, heroes):
        Achievement.__init__(self, name)
        self.heroes = heroes
        self.description = 'Win a game with %s on your team' % sequence(heroes)


class WinBattleCupPartyAchievement(Achievement):
    def __init__(self, name):
        Achievement.__init__(self, name)
        self.description = 'Win a Battle Cup'


class PlayerOnLowestParameterAchievement(Achievement):
    def __init__(self, name, player, parameter):
        Achievement.__init__(self, name)
        self.player = player
        self.parameter = parameter
        self.description = 'Win a game with %s having lowest %s' % (player, parameter)


class PlayerOnHeroAchievement(Achievement):
    def __init__(self, name, player, heroes):
        Achievement.__init__(self, name)
        self.player = player
        self.heroes = heroes
        self.description = 'Win a game with %s playing one of %s' % (player, sequence(heroes))


class WinCarriedByAchievement(Achievement):
    def __init__(self, name, player, hero):
        Achievement.__init__(self, name)
        self.player = player
        self.hero = hero
        self.description = 'Win a game being carried by %s on %s' % (player, hero)


class ComeBackFromMegaCreepsAchievement(Achievement):
    def __init__(self, name):
        Achievement.__init__(self, name)
        self.description = 'Win a game against Mega Creeps'


class WinWithoutPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a game without %s on team' % sequence(players)


def sequence(strings):
    return '%s and %s' % (', '.join(strings[:-1]), strings[-1]) if len(strings) > 1 else strings[0]
