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

    def add_ach(self, achievement):
        self.achievement_list.append(achievement)


class PnKAchievements(AchievementBase):
    def __init__(self, matches):
        AchievementBase.__init__(self, matches)
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
        self.add_ach(ItemAchievement('Maximum Blink', 'blink_dagger', 'Blink Dagger', 4))
        self.add_ach(ComeBackFromMegaCreepsAchievement('Overwhelming Odds'))
        self.add_ach(WinBattleCupPartyAchievement('Battle Cup Winners'))
        self.add_ach(PlayerOnLowestParameterAchievement('Naked Baco', 'Baco', 'total_gold'))
        self.add_ach(PlayerOnHeroAchievement('Brainless Baco', 'Baco', UNDEAD_HEROES))
        self.add_ach(PlayerOnHeroAchievement('Mustache Baco', 'Baco', MUSTACHE_HEROES, 'a hero with a mustache'))
        self.add_ach(WinWithHeroAchievement('Girl Power', FEMALE_HEROES, 'are female heroes'))
        self.add_ach(WinWithHeroAchievement('Melee Only', MELEE_HEROES, 'are melee heroes'))
        self.add_ach(WinWithHeroAchievement('No Disables', NO_DISABLE_HEROES, 'have no reliable stuns'))


class Achievement:
    def __init__(self, name):
        self.name = name
        self.description = ''


class ItemAchievement(Achievement):
    def __init__(self, name, item_code, item_name, amount):
        Achievement.__init__(self, name)
        self.item_code = item_code
        self.item_name = item_name
        self.amount = amount
        self.description = 'Win a game with %i %s on your team' % (amount, item_name)


class WinWithPlayerAchievement(Achievement):
    def __init__(self, name, players):
        Achievement.__init__(self, name)
        self.players = players
        self.description = 'Win a game with %s on your team' % sequence(players)


class WinWithHeroAchievement(Achievement):
    def __init__(self, name, heroes, msg=None):
        Achievement.__init__(self, name)
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a game with %s on your team' % sequence(heroes)
        else:
            self.description = 'Win a game where all heroes %s' % msg


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
    def __init__(self, name, player, heroes, msg=None):
        Achievement.__init__(self, name)
        self.player = player
        self.heroes = heroes
        if msg is None:
            self.description = 'Win a game with %s playing one of %s' % (player, sequence(heroes))
        else:
            self.description = 'Win a game with %s playing %s' % (player, msg)


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
