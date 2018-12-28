class PopularVotePnK2018:

    def __init__(self):
        self.top_five = ['kkz', 'Osaka', 'Chaos', 'Zé', 'Lotus']
        self.votes = [
            {
                'category': 'Maior evolução',
                'options': ['Chuvisco', 'tchepo', 'Scrider'],
                'votes': [8, 4, 2],
                'winner': 'Chuvisco'
            },
            {
                'category': 'Prêmio Melhor Pessoa',
                'options': ['Baco', 'tchepo', 'Older', 'Keera'],
                'votes': [3, 4, 7, 0],
                'winner': 'Older'
            },
            {
                'category': 'Mais Tóxico',
                'options': ['Chuvisco', 'Alidio', 'kkz', 'Lotus'],
                'votes': [3, 8, 2, 1],
                'winner': 'Alidio'
            },
            {
                'category': 'Favorito para adicionar no grupo em 2019',
                'options': ['Kiddy', 'Ronan', 'tiago', 'Cristian', 'Alpiona', 'Fallenzão'],
                'votes': [2, 1, 3, 6, 0, 1],
                'winner': 'Cristian'
            },
            {
                'category': 'Melhor imitação',
                'options': [
                    'Chaos imitando o Chuvisco',
                    'Zé imitando o Chuvisco traveco',
                    'tchepo imitando o Scrider',
                    'tchepo imitando o Alidio',
                    'tchepo imitando o Osaka'
                ],
                'votes': [5, 0, 4, 0, 5],
                'winner': ['Chaos', 'Chuvisco', 'tchepo']
            },
            {
                'category': 'Treta do Ano',
                'options': ['Alidio vs Scrider', 'Baco fofoqueiro', 'Lotus pistola mas de boas', 'Baco vs Chuvisco'],
                'votes': [1, 5, 4, 4],
                'winner': 'Baco'
            },
            {
                'category': 'Acontecimentos não dotísticos do ano',
                'options': [
                    'Alidio no Brasil',
                    'Baco em Porto Alegre',
                    'Baco em Guaporé com tchepo e o celular',
                    'P90 vs Crossfit'
                ],
                'votes': [6, 6, 1, 1],
                'winner': ['Alidio', 'Baco']
            },
            {
                'category': 'Acontecimentos dotísticos do grupo',
                'options': [
                    'Chuva Ancient',
                    'Dota night! Lan do Tier Guedes',
                    'tchepo 20 wins streak',
                    'kkz vice das universidades de BH'
                ],
                'votes': [5, 2, 7, 0],
                'winner': 'tchepo'
            },
            {
                'category': 'Highlight do ano',
                'options': [
                    'Smoke no ult do sniper do tchepo',
                    'Combo Osaka, Chaos e tchepo',
                    'Insta quad do shaker no roshan'
                ],
                'votes': [4, 4, 2],
                'winner': ['Osaka', 'Chaos', 'tchepo']
            },
            {
                'category': 'Melhor partida do ano',
                'options': [
                    'Partida do 1hp trono',
                    'A partida que não acabou (Valve tirou nossa vitória)',
                    'Virada de 30k (Ember + Void)'
                ],
                'votes': [9, 3, 2]
            },
            {
                'category': 'Melhor posição 1',
                'options': ['Nuvah', 'Roshan', 'kkz', 'Pringles', 'Baco'],
                'votes': [0, 0, 11, 0, 3],
                'winner': 'kkz'
            },
            {
                'category': 'Melhor posição 2',
                'options': ['Zé', 'Nuvah', 'kkz', 'Osaka', 'Chaos'],
                'votes': [6, 0, 0, 6, 2],
                'winner': 'Osaka'
            },
            {
                'category': 'Melhor posição 3',
                'options': ['Osaka', 'Roshan', 'Chuvisco', 'Alidio', 'Chaos'],
                'votes': [3, 0, 1, 4, 6],
                'winner': 'Chaos'
            },
            {
                'category': 'Melhor posição 4',
                'options': ['Baco', 'Zé', 'Scrider', 'Chaos', 'Alidio'],
                'votes': [3, 6, 0, 2, 3],
                'winner': 'Zé'
            },
            {
                'category': 'Melhor posição 5',
                'options': ['Lotus', 'Baco', 'Older', 'Scrider', 'Tchepo'],
                'votes': [6, 4, 2, 1, 1],
                'winner': 'Lotus'
            }
        ]
        self.message = 'Popular Vote thanks to Cap'

    def get_categories(self):
        return self.votes

    def get_top_five(self):
        return self.top_five
