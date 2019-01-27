import math
import os
import os.path
from pptx import Presentation
from pptx.util import Inches, Pt
from tier import TierItem
from category import Category
from pptx.enum.text import PP_ALIGN
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LEGEND_POSITION
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.chart.data import ChartData
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from constants import roles
import calendar


class Slides:
    def __init__(self, team_name, years, tit, sub, players, month=None):
        self.presentation = Presentation()
        self.team_name = team_name
        self.players = players
        y = '_'.join([str(x) for x in years])
        self.dates = y if month is None else "%s_%s" % (y, calendar.month_abbr[month])
        self.add_divider_slide(tit, "%s" % sub)

    def add_slide(self, layout, r, g, b):
        slide_layout = self.presentation.slide_layouts[layout]
        slide = self.presentation.slides.add_slide(slide_layout)
        Slides.change_slide_color(slide, r, g, b)
        return slide

    def add_divider_slide(self, text, sub_text):
        slide = self.add_slide(0, 230, 230, 230)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = text
        subtitle.text = sub_text

    def add_heroes(self, hero_stats, min_matches_with_hero):
        for hero in hero_stats:
            if hero['matches'] > 0:
                slide = self.add_slide(5, 204, 255, 255)
                title_shape = slide.shapes.title
                title_shape.text = '%s' % hero['name']
                title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT

                pic_path = 'data/heroes/%s.jpg' % hero['id']
                slide.shapes.add_picture(pic_path, Inches(7), Inches(0.2), height=Inches(1.1))

                headers = ['Role', 'Matches', 'Win Rate']
                keys = ['role', 'matches', 'wr']
                formats = ['%s', '%s', '%.2f %%']
                widths = [1.5, 1, 1]
                Slides.create_table(slide, hero['roles'], headers, keys, formats, Inches(0.5), Inches(1.5), Inches(3.5),
                                    1,
                                    12, 15, widths=widths)

                tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(1.5), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s has %s matches' % (hero['name'], hero['matches'])

                s = sorted([x for x in hero['played_by'] if x['matches'] >= min_matches_with_hero],
                           key=lambda e: (e['rating'], e['matches']),
                           reverse=True)
                if len(s) > 0:
                    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.3), Inches(1.5), Inches(0.5))
                    tf = tx_box.text_frame
                    p = tf.paragraphs[0]
                    p.text = 'Best players with at least %s matches:' % min_matches_with_hero
                    p.font.size = Pt(16)
                    for i in range(min(3, len(s))):
                        pic_path = 'data/pics/%s.jpg' % self.players[s[i]['name']]
                        if os.path.isfile(pic_path):
                            slide.shapes.add_picture(pic_path, Inches(0.25), Inches(4.8) + i * Inches(0.8),
                                                     height=Inches(0.7))

                        tx_box = slide.shapes.add_textbox(Inches(1.1), Inches(4.85) + i * Inches(0.8), Inches(1.5),
                                                          Inches(0.5))
                        p = tx_box.text_frame.paragraphs[0]
                        p.text = '%.1f' % s[i]['rating']
                        p.font.size = Pt(24)
                        p.font.bold = True

                        tx_box = slide.shapes.add_textbox(Inches(1.8), Inches(5.05) + i * Inches(0.8), Inches(1.5),
                                                          Inches(0.5))
                        p = tx_box.text_frame.paragraphs[0]
                        p.text = '%i-%i (%.2f %% wr)' % (s[i]['wins'], s[i]['matches'] - s[i]['wins'], s[i]['wr'])
                        p.font.size = Pt(18)

                        tx_box = slide.shapes.add_textbox(Inches(1.8), Inches(4.75) + i * Inches(0.8), Inches(1.5),
                                                          Inches(0.5))
                        p = tx_box.text_frame.paragraphs[0]
                        p.text = '%s' % s[i]['name']
                        p.font.size = Pt(14)
                        p.font.bold = True

                headers = ['Played by', 'Matches', 'Wins', 'Win Rate', 'Rating']
                keys = ['name', 'matches', 'wins', 'wr', 'rating']
                formats = ['%s', '%s', '%s', '%.2f %%', '%.1f']
                widths = [1.3, 1, 0.8, 1, 0.9]
                Slides.create_table(slide, hero['played_by'], headers, keys, formats, Inches(4.5), Inches(1.5),
                                    Inches(5), 1, 11, 15, widths=widths)

    def add_player_slides(self, player_name, player_roles, heroes, pairs):
        slide = self.add_slide(5, 255, 229, 204)
        title_shape = slide.shapes.title
        title_shape.text = '%s' % player_name
        title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT

        tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.35), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = '%s played %s distinct heroes' % (player_name, len([x for x in heroes.values() if x['matches'] > 0]))

        tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = '%s played %s matches' % (player_name, sum([x['matches'] for x in heroes.values()]))

        pic_path = 'data/pics/%s.jpg' % self.players[player_name]
        if os.path.isfile(pic_path):
            slide.shapes.add_picture(pic_path, Inches(8), Inches(0.2), height=Inches(1.1))

        headers = ['Role', 'Matches', 'Win Rate']
        keys = ['role', 'matches', 'wr']
        formats = ['%s', '%s', '%.2f %%']
        widths = [1.5, 1, 1]
        Slides.create_table(slide, player_roles, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(3.5), 1, 12, 15,
                            widths=widths)

        heroes = sorted(heroes.items(), key=lambda e: e[1]['rating'], reverse=True)
        for i in range(4):
            if heroes[i][1]['matches'] > 0:
                pic_path = 'data/heroes/%s.jpg' % heroes[i][0]
                slide.shapes.add_picture(pic_path, Inches(0.5), Inches(4.2) + i * Inches(0.8), height=Inches(0.7))
                tx_box = slide.shapes.add_textbox(Inches(2), Inches(4.3) + i * Inches(0.8), Inches(1.6), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%.1f' % heroes[i][1]['rating']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(24)
                tx_box = slide.shapes.add_textbox(Inches(2.6), Inches(4.4) + i * Inches(0.8), Inches(1.5), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s matches' % heroes[i][1]['matches']
                p.font.size = Pt(16)

        headers = ['Paired with', 'Matches', 'Wins', 'Win Rate']
        keys = ['name', 'matches', 'wins', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        widths = [1.5, 1, 1, 1]
        Slides.create_table(slide, pairs, headers, keys, formats, Inches(4.5), Inches(1.5), Inches(4.5), 1, 11, 15,
                            widths=widths)

    def add_intro_slide(self, match_count, min_player_count, min_matches, min_couples_matches):
        slide = self.add_slide(1, 152, 251, 152)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]

        title_shape.text = '%s Summary' % self.team_name
        tf = body_shape.text_frame
        tf.text = 'A total of %i matches were analyzed.' % match_count
        p = tf.add_paragraph()
        p.text = 'Parties with at least %i %s players.' % (min_player_count, self.team_name)
        p.level = 1
        p = tf.add_paragraph()
        p.text = 'Average metrics consider players with at least %i matches.' % min_matches
        p.level = 1
        p = tf.add_paragraph()
        p.text = 'For best pairings and best players in roles, a minimum of %i matches.' % min_couples_matches
        p.level = 2
        p = tf.add_paragraph()
        p.text = 'Best team per hero on each role requires a minimum of %i matches for that hero.' % min_couples_matches
        p.level = 2
        p = tf.add_paragraph()
        p.text = 'Best team per hero and player on each role requires a minimum of %i matches.' \
                 % (min_couples_matches / 2)
        p.level = 2
        p = tf.add_paragraph()
        p.text = 'The list of players is: %s' % (', '.join(self.players.keys()))
        p.level = 1
        p.font.size = Pt(18)

    def add_five_player_compositions(self, comp, matches):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Full Parties with >= %i matches' % matches
        headers = ['Players', 'Wins', 'Matches', 'Win Rate']
        keys = ['players', 'wins', 'matches', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        widths = [4.5, 1.5, 1.5, 1.5]
        Slides.create_table(slide, comp, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15,
                            widths=widths)

    def add_win_rate_slide(self, win_rate, match_count, party_size):
        slide = self.add_slide(1, 152, 251, 152)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = '%s Win Rate' % self.team_name
        tf = body_shape.text_frame
        tf.text = 'Win rate: %.2f %%' % win_rate
        p = tf.add_paragraph()
        p.text = 'Match count: %s' % match_count
        tf.add_paragraph()
        for i in range(1, 6):
            p = tf.add_paragraph()
            p.text = '%s matches with party size = %i' % (party_size[i-1], i)

    def add_comebacks_throws(self, comebacks, throws):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Top 10 %s Comebacks' % self.team_name
        headers = ['Match ID', 'Gold', 'Players']
        keys = ['match', 'gold', 'players']
        formats = ['%s', '%s', '%s']
        widths = [2, 2, 5]
        Slides.create_table(slide, comebacks, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15,
                            widths=widths)

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Top 10 %s Throws' % self.team_name
        Slides.create_table(slide, throws, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15,
                            widths=widths)

    def add_compositions(self, compositions):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Lane Compositions'
        headers = ['Lane Composition', 'Wins', 'Matches', 'Win Rate']
        keys = ['comp', 'wins', 'matches', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        Slides.create_table(slide, compositions, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15)

    def add_win_rate_heroes(self, versus, text):
        versus = [v for v in versus if v['matches'] > 0]
        for c in range(math.ceil(len(versus)/14)):
            slide = self.add_slide(5, 204, 255, 204)
            title_shape = slide.shapes.title
            title_shape.text = '%s Win Rate %s Heroes [%i]' % (self.team_name, text, c + 1)
            for y in range(2):
                for x in range(7):
                    index = c*14 + y*7 + x
                    if len(versus) > index:
                        hero = versus[index]
                        pic_path = 'data/heroes/%s.jpg' % hero['id']
                        slide.shapes.add_picture(pic_path, Inches(0.5) + y * Inches(5), Inches(1.8) + x * Inches(0.8),
                                                 height=Inches(0.7))
                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2),
                                                          Inches(1.65) + x * Inches(0.8), Inches(1.5), Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = '%i-%i (%.2f %% wr)' % (hero['wins'], hero['matches'] - hero['wins'], hero['wr'])
                        p.font.size = Pt(22)
                        p.alignment = PP_ALIGN.CENTER
                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2),
                                                          Inches(1.65) + x * Inches(0.8) + Inches(0.5), Inches(1.5),
                                                          Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = hero['name']
                        p.font.size = Pt(12)
                        p.font.bold = True
                        p.alignment = PP_ALIGN.CENTER

    def add_most_played(self, heroes):
        heroes = [v for v in heroes if v['matches'] > 0]
        for c in range(math.ceil(len(heroes)/14)):
            slide = self.add_slide(5, 255, 204, 255)
            title_shape = slide.shapes.title
            title_shape.text = '%s\'s Most Played Heroes [%i]' % (self.team_name, c + 1)
            for y in range(2):
                for x in range(7):
                    index = c*14 + y*7 + x
                    if len(heroes) > index:
                        hero = heroes[index]
                        pic_path = 'data/heroes/%s.jpg' % hero['id']
                        slide.shapes.add_picture(pic_path, Inches(0.5) + y * Inches(5), Inches(1.8) + x * Inches(0.8),
                                                 height=Inches(0.7))
                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2),
                                                          Inches(1.65) + x * Inches(0.8), Inches(1.5), Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = '%s matches' % (hero['matches'])
                        p.font.size = Pt(22)
                        p.alignment = PP_ALIGN.CENTER
                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2),
                                                          Inches(1.65) + x * Inches(0.8) + Inches(0.5), Inches(1.5),
                                                          Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = hero['name']
                        p.font.size = Pt(12)
                        p.font.bold = True
                        p.alignment = PP_ALIGN.CENTER

    def add_match_summary_by_player(self, summary, team):
        cat = Category(0, '', unit='matches')

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Most Matches Played'
        scores = [TierItem(summary[i]['player'], summary[i]['matches'], '') for i in range(3)]
        self.add_top_three_table(scores, slide, True, cat, Inches(1), Inches(2))

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Most Matches Played with %s' % self.team_name
        scores = [TierItem(team[i]['player'], team[i]['team_matches'], '') for i in range(3)]
        self.add_top_three_table(scores, slide, True, cat, Inches(1), Inches(2))

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Match Summary by Player'
        headers = ['Player', 'Total Matches', 'Matches with %s' % self.team_name, '%% with %s' % self.team_name]
        keys = ['player', 'matches', 'team_matches', 'perc_with_team']
        formats = ['%s', '%s', '%s', '%.2f %%']
        Slides.create_table(slide, [x for x in summary if x['team_matches'] > 0], headers, keys, formats, Inches(0.5),
                            Inches(1.5), Inches(9), 1, 11, 14)

    def add_tier_slides(self, tier, category):
        texts = tier.list_to_print()

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = texts[1]
        scores = tier.get_top_three()
        self.add_top_three_table(scores, slide, tier.is_max, category, Inches(0.7), Inches(1.8))

        if len(tier.scores_array) > 0:
            slide = self.add_slide(5, 255, 255, 224)
            title_shape = slide.shapes.title
            title_shape.text = texts[1]
            chart_data = CategoryChartData()
            chart_data.categories = [x.name for x in tier.scores_array]
            chart_data.add_series(texts[1], [x.score for x in tier.scores_array])
            x, y, cx, cy = Inches(1), Inches(1.6), Inches(8), Inches(5)
            slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)

        slide = self.add_slide(6, 255, 255, 224)
        left = top = width = height = Inches(0.4)
        txt_box = slide.shapes.add_textbox(left, top, width, height)
        tf = txt_box.text_frame
        tf.text = "%s - weights %s points" % (texts[1], tier.weight)
        tf.paragraphs[0].font.bold = True
        for i in range(2, len(texts)):
            p = tf.add_paragraph()
            p.text = texts[i]
            p.font.size = Pt(14)

    def add_top_three_table(self, scores, slide, is_max, category, left, top):
        pos = [(0, '1st'), (1, '2nd'), (2, '3rd')]
        val = min(3, len(scores))
        for i, name in pos[0:val]:
            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(0), Inches(2.5), Inches(0.7))
            tf = tx_box.text_frame
            p = tf.paragraphs[0]
            p.text = name
            p.font.size = Pt(24)
            p.alignment = PP_ALIGN.CENTER

            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(0.75), Inches(2.5), Inches(0.7))
            tf = tx_box.text_frame
            tf.text = scores[i].name
            p = tf.paragraphs[0]
            p.font.size = Pt(24)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER

            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(1.5), Inches(2.5), Inches(0.7))
            tf = tx_box.text_frame
            if not isinstance(scores[i].score, str):
                fmt = (category.max_format if is_max else category.avg_format) % scores[i].score
            else:
                fmt = scores[i].score
            tf.text = "%s %s" % (fmt, category.unit)
            p = tf.paragraphs[0]
            p.font.size = Pt(22)
            p.alignment = PP_ALIGN.CENTER

            pic_path = 'data/pics/%s.jpg' % self.players[scores[i].name]
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, left + Inches(3*i), top + Inches(2.5), height=Inches(2.5))

    def add_best_team(self, best_team):
        slide = self.add_slide(5, 152, 251, 152)
        slide.shapes.title.text = "Best Team by Hero Performance"
        i = 0
        for r in roles().values():
            pic_path = 'data/heroes/%s.jpg' % best_team[r][0]['hero_id']
            slide.shapes.add_picture(pic_path, Inches(0.5 + 1.8 * i), Inches(2), height=Inches(0.8))
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(3), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = best_team[r][0]['hero_name']
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(18)
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(3.6), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = '%.1f' % best_team[r][0]['rating']
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.size = Pt(24)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(1.5), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = '%s' % best_team[r][0]['role']
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.size = Pt(18)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            for j in range(1, 5):
                pic_path = 'data/heroes/%s.jpg' % best_team[r][j]['hero_id']
                slide.shapes.add_picture(pic_path, Inches(0.5 + 1.8 * i), Inches(4.5 + (j - 1) * 0.7),
                                         height=Inches(0.5))
                tx_box = slide.shapes.add_textbox(Inches(1.6 + 1.8 * i), Inches(4.5 + (j - 1) * 0.7), Inches(1.6),
                                                  Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%.1f' % best_team[r][j]['rating']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(16)
                tf.paragraphs[0].alignment = PP_ALIGN.LEFT
            i += 1

    def add_best_team_by_player(self, best_team):
        slide = self.add_slide(5, 152, 251, 152)
        slide.shapes.title.text = "Best Player/Hero by Position"
        i = 0
        for r in roles().values():
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(1.5), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = '%s' % best_team[r][0]['role']
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.size = Pt(18)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER

            pic_path = 'data/heroes/%s.jpg' % best_team[r][0]['hero_id']
            slide.shapes.add_picture(pic_path, Inches(0.5 + 1.8 * i), Inches(2), height=Inches(0.8))

            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(3), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = best_team[r][0]['hero_name']
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(18)

            pic_path = 'data/pics/%s.jpg' % best_team[r][0]['player_id']
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(0.8 + 1.8 * i), Inches(3.45), height=Inches(1))

            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(4.4), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = best_team[r][0]['player_name']
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(18)

            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(4.85), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = '%.1f' % best_team[r][0]['rating']
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.size = Pt(24)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER

            for j in range(1, 5):
                pic_path = 'data/heroes/%s.jpg' % best_team[r][j]['hero_id']
                slide.shapes.add_picture(pic_path, Inches(0.5 + 1.8 * i), Inches(5.6 + (j - 1) * 0.45),
                                         height=Inches(0.35))
                pic_path = 'data/pics/%s.jpg' % best_team[r][j]['player_id']
                if os.path.isfile(pic_path):
                    slide.shapes.add_picture(pic_path, Inches(1.2 + 1.8 * i), Inches(5.6 + (j - 1) * 0.45),
                                             height=Inches(0.35))
                tx_box = slide.shapes.add_textbox(Inches(1.6 + 1.8 * i), Inches(5.6 + (j - 1) * 0.45), Inches(1.6),
                                                  Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%.1f' % best_team[r][j]['rating']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(16)
                tf.paragraphs[0].alignment = PP_ALIGN.LEFT
            i += 1

    def add_results_slides(self, medals, points):
        cat = Category(0, '', max_format='%s')
        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Results Compilation'
        scores = [
            TierItem(medals[i][0], str(medals[i][1]), '', medals[i][1][0] * 3 + medals[i][1][1] * 2 + medals[i][1][2])
            for i in range(3)]
        self.add_top_three_table(scores, slide, True, cat, Inches(0.7), Inches(1.8))

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Results Compilation'
        headers = ['Player', 'Gold', 'Silver', 'Bronze']
        keys = ['player', 'gold', 'silver', 'bronze']
        scores = [{'player': k, 'gold': v[0], 'silver': v[1], 'bronze': v[2]} for k, v in medals]
        formats = ['%s', '%s', '%s', '%s']
        Slides.create_table(slide, [x for x in scores if x['gold'] + x['silver'] + x['bronze'] > 0], headers, keys,
                            formats, Inches(2), Inches(1.5), Inches(6), 1, 11, 14)

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Weighted Points'
        scores = [TierItem(points[i][0], str(points[i][1]), '') for i in range(3)]
        self.add_top_three_table(scores, slide, True, cat, Inches(0.7), Inches(1.8))

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Weighted Points'
        headers = ['Player', 'Points']
        keys = ['player', 'points']
        scores = [{'player': k, 'points': v} for k, v in points]
        formats = ['%s', '%s']
        Slides.create_table(slide, [x for x in scores if x['points'] > 0], headers, keys, formats, Inches(3),
                            Inches(1.5), Inches(3), 1, 11, 14)

    def add_popular_vote_category_slides(self, popular_vote_category):
        slide = self.add_slide(1, 221, 160, 221)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = popular_vote_category['category']
        tf = body_shape.text_frame
        tf.text = 'Opções: '
        for item in popular_vote_category['options']:
            p = tf.add_paragraph()
            p.text = item
            p.level = 1
        if 'winner' in popular_vote_category and isinstance(popular_vote_category['winner'], list):
            tx_box = slide.shapes.add_textbox(Inches(8), Inches(1.8), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = "Vencedores"
            for i in range(0,len(popular_vote_category['winner'])):
                pic_path = 'data/pics/%s.jpg' % self.players[popular_vote_category['winner'][i]]
                if os.path.isfile(pic_path):
                    slide.shapes.add_picture(pic_path, Inches(8.3), Inches(2.3 + 1.55 * i), height=Inches(1))
                tx_box = slide.shapes.add_textbox(Inches(8.3), Inches(2.3 + 1.55 * i + 1.08), Inches(2), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = popular_vote_category['winner'][i]
        elif 'winner' in popular_vote_category:
            tx_box = slide.shapes.add_textbox(Inches(8), Inches(1.8), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = "Vencedor"
            pic_path = 'data/pics/%s.jpg' % self.players[popular_vote_category['winner']]
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(8), Inches(2.5), height=Inches(1.4))
            tx_box = slide.shapes.add_textbox(Inches(8), Inches(4), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = popular_vote_category['winner']

        slide = self.add_slide(5, 221, 160, 221)
        slide.shapes.title.text = popular_vote_category['category']
        chart_data = ChartData()
        chart_data.categories = popular_vote_category['options']
        v = sum(popular_vote_category['votes'])
        chart_data.add_series("%i answers" % v, [x / v for x in popular_vote_category['votes']])
        x, y, cx, cy = Inches(1), Inches(1.8), Inches(7), Inches(5)
        chart = slide.shapes.add_chart(XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data).chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.RIGHT
        chart.legend.include_in_layout = False
        chart.plots[0].has_data_labels = True
        data_labels = chart.plots[0].data_labels
        data_labels.number_format = '0%'
        data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
        tx_box = slide.shapes.add_textbox(Inches(8), Inches(6), Inches(2), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = "%i respostas" % v

    def add_top_five_slides(self, top):
        slide = self.add_slide(5, 221, 160, 221)
        slide.shapes.title.text = "Dream Team by Popular Vote"
        for i in range(5):
            pic_path = 'data/pics/%s.jpg' % self.players[top[i]]
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(0.5 + 1.8 * i), Inches(2), height=Inches(1.6))
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(4), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = top[i]
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tx_box = slide.shapes.add_textbox(Inches(0.5 + 1.8 * i), Inches(5), Inches(1.6), Inches(0.4))
            tf = tx_box.text_frame
            tf.text = str(i + 1)
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.size = Pt(36)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    def save(self):
        self.presentation.save('report_%s_%s.pptx' % (self.team_name, self.dates))

    @staticmethod
    def change_slide_color(slide, r, g, b):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(r, g, b)

    @staticmethod
    def create_table(slide, data, headers, keys, formats, left, top, width, height, font_size, header_size,
                     widths=None):
        table_shape = slide.shapes.add_table(len(data) + 1, len(headers), left, top, width, height)
        table = table_shape.table
        for i in range(len(headers)):
            table.cell(0, i).text = headers[i]
        for i in range(len(data)):
            for j in range(len(keys)):
                table.cell(i + 1, j).text = formats[j] % data[i][keys[j]]
        Slides.set_table_font_size(table, font_size)
        for i in range(len(keys)):
            table.cell(0, i).text_frame.paragraphs[0].runs[0].font.size = Pt(header_size)
        if widths is not None:
            for i in range(len(widths)):
                table.columns[i].width = Inches(widths[i])

    @staticmethod
    def iter_cells(table):
        for row in table.rows:
            for cell in row.cells:
                yield cell

    @staticmethod
    def set_table_font_size(table, size):
        for cell in Slides.iter_cells(table):
            for paragraph in cell.text_frame.paragraphs:
                paragraph.space_before = Pt(1)
                paragraph.space_after = Pt(1)
                for run in paragraph.runs:
                    run.font.size = Pt(size)
