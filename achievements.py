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
        self.append_achievement(ItemAchievement('Next lebel Farming', 'radiance', 2))
        self.append_achievement(ItemAchievement('Multiple Midas', 'midas', 3))
        self.append_achievement(ItemAchievement('Maximum Blink', 'blink', 4))
        self.append_achievement(WinWithPlayerAchievement('Toxic Couple', ['Baco', 'Alidio']))
        self.append_achievement(WinWithPlayerAchievement('Forever Archon', ['Scrider', 'Older', 'tchepo']))
        self.append_achievement(WinWithPlayerAchievement('Feldmann Brothers', ['Lotus', 'Pringles']))
        self.append_achievement(WinCarriedByAchievement('Best hooks for enemy team', 'Cristian', 'Pudge'))
        self.append_achievement(WinCarriedByAchievement('Mid Lina', 'Nuvah', 'Lina'))
        self.append_achievement(WinCarriedByAchievement('Worst hero in Dota', 'Alidio', 'Wraith King'))
        self.append_achievement(WinCarriedByAchievement('New ranged offlane', 'Chuvisco', 'Necrophos'))
        self.append_achievement(PlayerOnLowestParameter('Naked Baco', 'Baco', 'total_gold'))
        self.append_achievement(PlayerOnHero('Brainless Baco', 'Baco', 'Undying'))


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
        self.description = 'Win a game with %s on your time' % ' and '.join(players)


class PlayerOnLowestParameter(Achievement):
    def __init__(self, name, player, parameter):
        Achievement.__init__(self, name)
        self.player = player
        self.parameter = parameter
        self.description = 'Win a game with %s having lowest %s' % (player, parameter)


class PlayerOnHero(Achievement):
    def __init__(self, name, player, hero):
        Achievement.__init__(self, name)
        self.player = player
        self.hero = hero
        self.description = 'Win a game with %s playing %s' % (player, hero)


class WinCarriedByAchievement(Achievement):
    def __init__(self, name, player, hero):
        Achievement.__init__(self, name)
        self.player = player
        self.hero = hero
        self.description = 'Win a game being carried by %s on %s' % (player, hero)
