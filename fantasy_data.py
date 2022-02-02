class FantasyData:
    def __init__(self):
        self.roles = {}

    def add_role(self, role_name):
        self.roles[role_name] = {}

    def add_category(self, role, category_name):
        self.roles[role][category_name] = {}

    def add_category_properties(self, role, category, weight, properties):
        self.roles[role][category]['weight'] = weight
        for prop, value in properties.items():
            self.roles[role][category][prop] = value
        self.roles[role][category]['players'] = {}

    def add_player_to_role(self, role, category, player):
        self.roles[role][category]['players'][player] = {}

    def add_player_value(self, role, category, player, value):
        self.roles[role][category]['players'][player]['value'] = value

    def add_player_fantasy_score(self, role, category, player, fantasy_score):
        self.roles[role][category]['players'][player]['fantasy_score'] = fantasy_score

    def add_player_relative_position(self, role, category, player, position):
        self.roles[role][category]['players'][player]['relative_position'] = position

    def add_player_matches(self, role, category, player, matches):
        self.roles[role][category]['players'][player]['matches'] = matches

    def get_categories_at_role(self, role):
        return sorted([[category_name, category_data] for category_name, category_data in self.roles[role].items()],
                      key=lambda x: -x[1]['weight'])

    def get_players_at_category(self, role, category):
        return sorted([[player_name, player_data]
                       for player_name, player_data in self.roles[role][category]['players'].items()],
                      key=lambda x: -sum([self.roles[role][c]['players'][x[0]]['fantasy_score']
                                          for c, _ in self.roles[role].items()]))

    def get_players_score(self, role):
        result = sorted([[player_name, sum([self.roles[role][c]['players'][player_name]['fantasy_score']
                                            for c, _ in self.roles[role].items()])] for cat_name, cat_data in
                         self.roles[role].items() for player_name, player_data in
                         cat_data['players'].items() if self.roles[role][cat_name]['weight'] == 5], key=lambda x: -x[1])
        return result

    def get_players_matches(self, role, player):
        return self.roles[role][role]['players'][player]['matches']

    def get_score_for_player(self, role, player):
        if self.player_in_role(role, player):
            return next(s for p, s in self.get_players_score(role) if p == player)
        return 0

    def player_in_role(self, role, player):
        return player in self.roles[role][role]['players']
