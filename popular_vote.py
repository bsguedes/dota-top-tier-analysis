class PopularVotePnK2020:
    def __init__(self):
        self.top_five = ['kkz', 'Kiddy', 'Chuvisco', 'Zé', 'Lotus']
        self.votes = [
            {
                'category': 'Partida do Ano',
                'options': [
                    'Mix via Matchmaking',
                    'Mix team Xupito vs team Lotus',
                    '40k de Comeback',
                ],
                'votes': [7, 2, 7],
            },
            {
                'category': 'Highlight do Ano',
                'options': [
                    'Rampage Alidio de Medusa',
                    'Combo Invoker Shaker Tide',
                    'Kiddy salvando Xupito de Smoke',
                    'Zé Spectre Sayajin',
                    'Rolo Compressor do PnK',
                    'Glimpse e Flecha da Mirana',
                ],
                'votes': [4, 3, 1, 2, 2, 4],
                'winner': ['Alidio', 'Older', 'JohnMirolho']
            },
            {
                'category': 'Melhor x1 do Ano',
                'options': [
                    'Lotus x Xupito de Pangolier',
                    'Lotus x Xupito de Windrunner',
                    'Pringles x Kiddy de Lina',
                    'Pringles x Kiddy de Mars',
                    'Pringles x Kiddy de SF',
                ],
                'votes': [4, 5, 6, 0, 1],
                'winner': ['Pringles', 'Kiddy']
            },
            {
                'category': 'Toxic Player Award',
                'options': [
                    'Baco',
                    'Chuvisco',
                    'Alidio',
                    'Pringles',
                    'Lotus',
                ],
                'votes': [0, 4, 8, 1, 3],
                'winner': 'Alidio'
            },
            {
                'category': 'Prêmio Older Istari de Melhor Pessoa',
                'options': [
                    'tiago',
                    'tchepo',
                    'Xupito',
                    'Keera',
                    'JohnMirolho',
                ],
                'votes': [0, 5, 5, 2, 4],
                'winner': ['tchepo', 'Xupito']
            },
            {
                'category': 'Streamer do Ano',
                'options': [
                    'Alidio',
                    'Baco',
                    'Pringles',
                    'Kiddy',
                    'Chaos',
                ],
                'votes': [6, 7, 0, 2, 1],
                'winner': 'Baco'
            },
            {
                'category': 'Try hard do Ano',
                'options': [
                    'Pringles',
                    'Kiddy',
                    'Lotus',
                    'Chuvisco',
                    'Older',
                    'kkz',
                ],
                'votes': [6, 1, 2, 2, 4, 1],
                'winner': 'Pringles'
            },
            {
                'category': 'Prêmio Saudade',
                'options': [
                    'Scrider',
                    'Osaka',
                    'Gilberto',
                    'Shadow',
                    'Fallenzão',
                ],
                'votes': [9, 2, 1, 2, 2],
                'winner': 'Scrider'
            },
            {
                'category': 'Treta/Discussão do Ano',
                'options': [
                    'Montar computador da China by Scrider',
                    'O que é try hard?',
                    'Panelinha do Clã',
                    'Chuvisco não aceita críticas?',
                    'Alidio expulso do Discord do PnK',
                ],
                'votes': [2, 1, 2, 10, 1],
                'winner': 'Chuvisco'
            },
            {
                'category': 'Bordão do Ano',
                'options': [
                    'SVENON',
                    'Joao ta ai?',
                    'Eu queria dizer que... tu é um irmão velho.... 6 são foda',
                    'Eu juro que vou fazer de tudo pra perder esse jogo',
                    'It is what it is',
                    'Vai tá tudo esquematiz...hahaha huhuhui tstststs aaaaaiiiii',
                ],
                'votes': [3, 1, 4, 2, 1, 5],
                'winner': 'Baco'
            },
            {
                'category': 'Jogo Alternativo do Ano',
                'options': [
                    'Fall Guys',
                    'Among Us',
                    'Chess',
                    'WoW',
                    'Plasmophobia',
                    'Hades',
                ],
                'votes': [4, 9, 2, 0, 0, 1],
            },
            {
                'category': 'Acontecimentos não dotísticos do ano',
                'options': [
                    'Chaos ganhando um buraco na testa',
                    'Gigante ganhando Skin no Poker',
                    'Nuvah ganhando no Poker às 4 da manhã',
                    'Baco visitando Alidio no Canadá',
                    'Fundação da Tchepo Esfirras Co.',
                    'Noivado do Chuvisco',
                ],
                'votes': [2, 1, 1, 5, 5, 2],
                'winner': ['tchepo', 'Baco', 'Alidio']
            },
            {
                'category': 'Acontecimentos dotísticos do grupo',
                'options': [
                    'Chuvisco Divine maior ganho de mmr que não é da época do HoN',
                    'Criação do PnKasino by Older',
                    'Chegada do tiago no grupo',
                    'Chegada do JohnMirolho no grupo',
                ],
                'votes': [3, 7, 3, 3],
                'winner': 'Older'
            },
            {
                'category': 'Melhor Discord Server',
                'options': [
                    'KingKiddy',
                    'Cold Blood',
                    'PnK Gaming',
                ],
                'votes': [1, 5, 10],
            },
            {
                'category': 'Best Brothers',
                'options': [
                    'Lotus e Pringles',
                    'Kiddy e Xupito',
                    'Roshan e Sioux',
                ],
                'votes': [5, 10, 1],
                'winner': ['Kiddy', 'Xupito']
            },
            {
                'category': 'Counter Strike Player of the Year',
                'options': [
                    'Alidio',
                    'Baco',
                    'Chuvisco',
                    'Zé',
                    'tchepo',
                    'Nuvah',
                    'kkz',
                    'Gigante',
                    'Chaos',
                ],
                'votes': [0, 2, 5, 2, 0, 0, 0, 7, 0],
            },
            {
                'category': 'Chess Player of the Year',
                'options': [
                    'Cristian',
                    'Nuvah',
                    'Zé',
                    'Chuvisco',
                ],
                'votes': [5, 9, 2, 0],
                'winner': 'Nuvah'
            },
            {
                'category': 'Poker Player of the Year',
                'options': [
                    'Zé',
                    'Nuvah',
                    'Gigante',
                    'tchepo',
                ],
                'votes': [1, 13, 2, 0],
                'winner': 'Nuvah'
            },
            {
                'category': 'Melhor Estiquer',
                'options': [
                    ['11.png', 'Zé Tenista'],
                    ['12.png', 'Lazy Xupito'],
                    ['13.png', 'Passando com a 4x4'],
                    ['14.png', 'Chaos Crossfiteiro'],
                    ['15.png', 'Nerd Lotus'],
                    ['16.png', 'Kiddy Lanchador']
                ],
                'votes': [3, 3, 5, 4, 0, 1],
                'winner': ['13.png', 'Xupito']
            },
            {
                'category': 'Melhor Estiquer do Baco',
                'options': [
                    ['b11.png', 'Baco Comunista'],
                    ['b12.png', 'Baco Lutador'],
                    ['b13.png', 'Baco Adolescente'],
                    ['b14.png', 'Baco Testudo'],
                    ['b15.png', 'Baco Sentado?'],
                    ['b16.png', 'Baco Jovem']
                ],
                'votes': [0, 3, 2, 7, 0, 4],
                'winner': ['b14.png', 'Baco Testudo']
            },
            {
                'category': 'Melhor Estiquer Shitpost',
                'options': [
                    ['21.png', 'Menina'],
                    ['22.png', 'Cachorro'],
                    ['23.png', 'Trump'],
                    ['24.png', 'Menino'],
                    ['25.png', 'Gato'],
                ],
                'votes': [2, 12, 2, 0, 0],
                'winner': ['22.png', 'Cachorro']
            },
            {
                'category': 'Melhor Coach (prêmio "Não Cala a Boca")',
                'options': [
                    'tchepo',
                    'Chuvisco',
                    'kkz',
                    'Baco',
                    'Nuvah',
                    'Zé',
                ],
                'votes': [1, 5, 6, 2, 1, 1],
                'winner': 'kkz'
            },
            {
                'category': 'Melhor Posição 1',
                'options': [
                    'kkz',
                    'Kiddy',
                    'Alidio',
                    'Pringles',
                    'Baco',
                    'Chuvisco',
                    '',
                ],
                'votes': [7, 4, 0, 2, 1, 2],
                'winner': 'kkz'
            },
            {
                'category': 'Melhor Posição 2',
                'options': [
                    'Kiddy',
                    'Zé',
                    'kkz',
                    'Chaos',
                    'Nuvah',
                    'Pringles',
                    'Cristian',
                ],
                'votes': [5, 3, 4, 0, 2, 1, 1],
                'winner': 'Kiddy'
            },
            {
                'category': 'Melhor Posição 3',
                'options': [
                    'Roshan',
                    'Xupito',
                    'tiago',
                    'Chuvisco',
                    'Chaos',
                    'Alidio',
                ],
                'votes': [0, 5, 0, 8, 1, 2],
                'winner': 'Chuvisco'
            },
            {
                'category': 'Melhor Posição 4',
                'options': [
                    'Zé',
                    'Xupito',
                    'JohnMirolho',
                    'Cristian',
                    'tchepo',
                    'Older',
                    'Lotus',
                ],
                'votes': [11, 1, 1, 1, 2, 0, 0],
                'winner': 'Zé'
            },
            {
                'category': 'Melhor Posição 5',
                'options': [
                    'tchepo',
                    'Older',
                    'Baco',
                    'Lotus',
                    'Nuvah',
                    'JohnMirolho',
                ],
                'votes': [0, 3, 4, 5, 1, 3],
                'winner': 'Lotus'
            },
        ]
        self.message = 'Popular Vote thanks to Tier Guedes and Cap'

    def get_categories(self):
        return self.votes

    def get_top_five(self):
        return self.top_five


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
