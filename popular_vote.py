class PopularVotePnK2019:

    def __init__(self):
        self.top_five = ['kkz', 'Kiddy', 'Chuvisco', 'Zé', 'Nuvah']
        self.votes = [
            {
                'category': 'Partida do Ano',
                'options': [
                    'Techies 90 minutos de jogo',
                    'Partida vencendo o time do Rayuur',
                    'Comeback de 90 minutos Silencer (kkz) e Ember (Pringles)'
                ],
                'votes': [6, 2, 8],
                'winner': ['kkz', 'Pringles']
            },
            {
                'category': 'Melhor Draft Temático',
                'options': [
                    'Engenheiros',
                    'Taxado',
                    'John Cena',
                    'Fora de posição',
                    'Tu me cura eu te curo',
                    'Boi Doido'
                ],
                'votes': [1, 2, 2, 7, 1, 3]
            },
            {
                'category': 'Best Brothers',
                'options': ['Scrider e Gordito', 'Lotus e Pringles', 'Kiddy e Xupito', 'Roshan e Sioux'],
                'votes': [5, 3, 8, 0],
                'winner': ['Kiddy', 'Xupito']
            },
            {
                'category': 'Highlight do Ano',
                'options': ['Nuvah e Zé Chrono+Sun Strike', 'Lotus matando 6 couriers', 'Wombo Combo Roshan Phoenix'],
                'votes': [10, 2, 4],
                'winner': ['Nuvah', 'Zé']
            },
            {
                'category': 'Jogo Alternativo do Ano',
                'options': ['Archero', 'AutoChess/Underlords', 'Apex Legends', 'WoW', 'Overwatch'],
                'votes': [6, 7, 1, 2, 0]
            },
            {
                'category': 'Prêmio Melhor Pessoa',
                'options': ['Scrider', 'Older', 'Tchepo', 'Keera', 'Baco'],
                'votes': [4, 7, 3, 0, 2],
                'winner': 'Older'
            },
            {
                'category': 'Toxic Player Award',
                'options': ['kkz', 'Kiddy', 'Alidio', 'Pringles', 'Lotus'],
                'votes': [1, 1, 4, 0, 10],
                'winner': 'Lotus'
            },
            {
                'category': 'Favorito para adicionar no grupo em 2020',
                'options': ['Pogo', 'Gordito', 'tiago', 'Vesgo', 'darkkside'],
                'votes': [4, 8, 3, 1, 0],
                'winner': 'Gordito'
            },
            {
                'category': 'Enfermidade do Ano',
                'options': [
                    'Apendicite do Bruno Silva Guedes',
                    'Trombose do Osmar Graciola Junior',
                    'Ombro deslocado do Felippe Ferreira Alves',
                    'Vômitos e diarreia do José Paulo Zanchin',
                ],
                'votes': [2, 6, 8, 0],
                'winner': 'Xupito'
            },
            {
                'category': 'Treta do Ano',
                'options': [
                    'Qual o conceito de hero pool?',
                    'Throw / Rage do Ghago(FDP)',
                    'Critérios de Admin do grupo',
                    'Lotus e Scrider'
                ],
                'votes': [6, 1, 5, 4],
            },
            {
                'category': 'Bordão do Ano',
                'options': [
                    'Primeiro Rad, depois Aghanim',
                    'Falta disciplina no PnK',
                    'Não é o ideal, mas acontece',
                    'Foi uma bela tentativa',
                    'Hora de vender a cama'
                ],
                'votes': [5, 1, 6, 3, 1],
                'winner': 'Scrider'
            },
            {
                'category': 'Acontecimentos não dotísticos do ano',
                'options': [
                    'Baco no show do Iron',
                    'PnK Tênis',
                    'Older e Feldmann brothers em Gramado',
                    'Baco piradaço nas baladas'
                ],
                'votes': [1, 4, 3, 8],
                'winner': 'Baco'
            },
            {
                'category': 'Acontecimentos dotísticos do Grupo',
                'options': [
                    'Lan do Guedes',
                    'Kiddy e kkz chegando a Immortal',
                    'Baco Streamer Season',
                    'PnK Mixes',
                    'kkz campeão, não mais um vice'
                ],
                'votes': [4, 5, 3, 2, 2],
                'winner': ['Kiddy', 'kkz']
            },
            {
                'category': 'Melhor Estiquer',
                'options': [
                    ['1.png', 'Wondering Zé'],
                    ['2.png', 'Sócio e Proprietário'],
                    ['3.png', 'Injured Xupito'],
                    ['4.png', 'Drinking Gigante'],
                    ['5.png', 'Zé Invokinho'],
                    ['6.png', 'Penis Alidio']
                ],
                'votes': [11, 0, 1, 0, 3, 1],
                'winner': ['1.png', 'Wondering Zé']
            },
            {
                'category': 'Melhor Estiquer do Baco',
                'options': [
                    ['b1.png', 'Fap Baco'],
                    ['b2.png', 'Grandpa Baco'],
                    ['b3.png', 'CEOsmar'],
                    ['b4.png', 'Eyebrow Baco'],
                    ['b5.png', 'Drinking Baco'],
                    ['b6.png', 'Winning Baco']
                ],
                'votes': [5, 1, 0, 3, 6, 1],
                'winner': ['b5.png', 'Drinking Baco']
            },
            {
                'category': 'Melhor posição 1',
                'options': ['Nuvah', 'Alidio', 'kkz', 'Pringles', 'Baco', 'Cristian'],
                'votes': [2, 1, 11, 0, 1, 1],
                'winner': 'kkz'
            },
            {
                'category': 'Melhor posição 2',
                'options': ['Chaos', 'kkz', 'Pringles', 'Zé', 'Kiddy', 'Osaka'],
                'votes': [4, 0, 1, 6, 5, 0],
                'winner': 'Zé'
            },
            {
                'category': 'Melhor posição 3',
                'options': ['Kiddy', 'Older', 'Chaos', 'Chuvisco', 'Alidio', 'Xupito'],
                'votes': [5, 1, 0, 10, 0, 0],
                'winner': 'Chuvisco'
            },
            {
                'category': 'Melhor posição 4',
                'options': ['Zé', 'Xupito', 'Scrider', 'Cristian', 'tchepo', 'Lotus'],
                'votes': [10, 2, 2, 1, 1, 0],
                'winner': 'Zé'
            },
            {
                'category': 'Melhor posição 5',
                'options': ['Baco', 'Older', 'Lotus', 'tchepo', 'Scrider', 'Nuvah'],
                'votes': [2, 4, 4, 2, 0, 4],
                'winner': ['Older', 'Lotus', 'Nuvah']
            },
            {
                'category': 'Melhor posição 5 (segundo turno)',
                'options': ['Older', 'Lotus', 'Nuvah'],
                'votes': [5, 3, 6],
                'winner': 'Nuvah'
            }
        ]
        self.message = 'Popular Vote thanks to Tier Guedes and Cap'

    def get_categories(self):
        return self.votes

    def get_top_five(self):
        return self.top_five

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
