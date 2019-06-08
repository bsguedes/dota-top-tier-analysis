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
from constants import sequence
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
        if layout == 5:
            title_shape = slide.shapes.title
            title_shape.text_frame.paragraphs[0].font.size = Pt(40)
        Slides.change_slide_color(slide, r, g, b)
        return slide

    def add_divider_slide(self, text, sub_text):
        slide = self.add_slide(0, 230, 230, 230)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = text
        subtitle.text = sub_text

    def add_item_slides(self, item_data):
        for data in item_data:
            slide = self.add_slide(5, 214, 187, 242)
            title_shape = slide.shapes.title
            title_shape.text = data['item_name']
            title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
            pic_path = 'data/items/%s.jpg' % data['item_internal_name']
            slide.shapes.add_picture(pic_path, Inches(7.5), Inches(0.2), height=Inches(1.1))
            headers = ['Amount', 'Wins', 'Losses', 'Matches', 'Win Rate']
            keys = ['amount', 'wins', 'losses', 'matches', 'wr']
            formats = ['%s', '%s', '%s', '%s', '%.2f %%']
            table_data = [{'amount': a, 'wins': b, 'losses': c, 'matches': d, 'wr': e} for a, b, c, d, e in
                          zip(data['counts'], data['wins'], data['losses'], data['matches'], data['wr'])]
            Slides.create_table(slide, table_data, headers, keys, formats, Inches(2), Inches(1.8), Inches(6),
                                1, 12, 15)
            chart_data = ChartData()
            chart_data.categories = data['counts']
            chart_data.add_series('Wins', data['wins'])
            chart_data.add_series('Losses', data['losses'])
            graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(4.2), Inches(9),
                                                   Inches(3.2),
                                                   chart_data)
            chart = graphic_frame.chart
            plot = chart.plots[0]
            plot.has_data_labels = True
            data_labels = plot.data_labels
            data_labels.font.size = Pt(10)
            data_labels.font.color.rgb = RGBColor(0x0A, 0x42, 0x80)
            data_labels.position = XL_LABEL_POSITION.INSIDE_END
            chart.has_legend = True
            chart.legend.position = XL_LEGEND_POSITION.RIGHT
            chart.legend.include_in_layout = False

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

                s = sorted([x for x in hero['played_by'] if x['matches'] >= min_matches_with_hero and x['rating'] > 0],
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

    def add_player_tables_slide(self, desc):
        slide = self.add_slide(5, 255, 229, 204)
        title_shape = slide.shapes.title
        title_shape.text = desc['name']
        title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT

        pic_path = 'data/pics/%s.jpg' % desc['id']
        if os.path.isfile(pic_path):
            slide.shapes.add_picture(pic_path, Inches(8), Inches(0.2), height=Inches(1.1))

        headers = ['Role', 'Matches', 'Win Rate']
        keys = ['role', 'matches', 'wr']
        formats = ['%s', '%s', '%.2f %%']
        widths = [1.5, 1, 1]
        Slides.create_table(slide, desc['roles'], headers, keys, formats, Inches(0.5), Inches(1.5), Inches(3.5), 1, 12,
                            15,
                            widths=widths)

        headers = ['Paired with', 'Matches', 'Wins', 'Win Rate']
        keys = ['name', 'matches', 'wins', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        widths = [1.5, 1, 1, 1]
        Slides.create_table(slide, desc['pairings'], headers, keys, formats, Inches(4.5), Inches(1.5), Inches(4.5), 1,
                            11, 15, widths=widths)

        heroes = desc['top_heroes']
        if len(heroes) > 0:
            Slides.text_box(slide, 'Best %s player with (based on hero rating):' % self.team_name, 0.3, 3.4,
                            font_size=13)
            rows = 7
            columns = 4
            for y in range(columns):
                for x in range(rows):
                    index = y * rows + x
                    if index < len(heroes):
                        hero = heroes[index]
                        pic_path = 'data/heroes/%s.jpg' % hero
                        slide.shapes.add_picture(pic_path, Inches(0.3) + y * Inches(3.8 / columns),
                                                 Inches(3.8) + x * Inches(0.5),
                                                 height=Inches(0.45))

    def add_player_data_slide(self, desc):
        slide = self.add_slide(5, 255, 229, 204)
        title_shape = slide.shapes.title
        title_shape.text = desc['name']
        title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT

        pic_path = 'data/pics/%s.jpg' % desc['id']
        if os.path.isfile(pic_path):
            slide.shapes.add_picture(pic_path, Inches(8), Inches(0.2), height=Inches(1.1))

        Slides.text_box(slide, 'Rating:', 0.5, 1.6, 1.5)
        Slides.text_box(slide, 'Wins:', 0.5, 2, 1.5)
        Slides.text_box(slide, 'Losses:', 0.5, 2.4, 1.5)
        Slides.text_box(slide, 'Distinct heroes:', 0.5, 2.8, 1.5)
        Slides.text_box(slide, 'Matches played:', 0.5, 3.2, 1.5)

        Slides.text_box(slide, str(desc['wins']), 1.6, 1.95, 1.75, alignment=PP_ALIGN.RIGHT, font_size=22)
        Slides.text_box(slide, str(desc['matches'] - desc['wins']), 1.6, 2.35, 1.75, alignment=PP_ALIGN.RIGHT,
                        font_size=22)
        Slides.text_box(slide, str(len([x for x in desc['heroes'].values() if x['matches'] > 0])), 1.6, 2.75, 1.75,
                        alignment=PP_ALIGN.RIGHT, font_size=22)
        Slides.text_box(slide, str(desc['matches']), 1.6, 3.15, 1.75, alignment=PP_ALIGN.RIGHT, font_size=22)

        Slides.text_box(slide, 'Best Win Streak:', 3.6, 1.6, 1.5)
        Slides.text_box(slide, 'Worst Loss Streak:', 3.6, 2, 1.5)
        Slides.text_box(slide, 'Radiant Wins:', 3.6, 2.8, 1.5)
        Slides.text_box(slide, 'Dire Wins:', 3.6, 3.2, 1.5)

        Slides.text_box(slide, str(max(0, max(desc['streaks']))), 4.8, 1.55, 1.75, alignment=PP_ALIGN.RIGHT,
                        font_size=22)
        Slides.text_box(slide, str(abs(min(0, min(desc['streaks'])))), 4.8, 1.95, 1.75, alignment=PP_ALIGN.RIGHT,
                        font_size=22)
        Slides.text_box(slide, '%.2f %%' % desc['radiant_wr'], 4.8, 2.75, 1.75, alignment=PP_ALIGN.RIGHT, font_size=22)
        Slides.text_box(slide, '%.2f %%' % desc['dire_wr'], 4.8, 3.15, 1.75, alignment=PP_ALIGN.RIGHT, font_size=22)

        Slides.text_box(slide, 'Win Rate:', 6.7, 1.6, 1.5)
        Slides.text_box(slide, 'Versatility:', 6.7, 2, 1.5)

        tx_box = slide.shapes.add_textbox(Inches(1.6), Inches(1.5), Inches(1.75), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = '%.1f' % desc['rating']
        p.font.bold = True
        p.font.size = Pt(28)
        p.alignment = PP_ALIGN.RIGHT

        tx_box = slide.shapes.add_textbox(Inches(7.8), Inches(1.55), Inches(1.75), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = '%.2f %%' % (100 * desc['wins'] / desc['matches'])
        p.font.size = Pt(22)
        p.alignment = PP_ALIGN.RIGHT

        tx_box = slide.shapes.add_textbox(Inches(7.8), Inches(1.95), Inches(1.75), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = '%.3f' % desc['versatility']
        p.font.size = Pt(22)
        p.alignment = PP_ALIGN.RIGHT

        tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = 'Best heroes by rating'
        p.font.size = Pt(16)
        heroes = sorted(desc['heroes'].items(), key=lambda e: e[1]['rating'], reverse=True)
        for i in range(4):
            if heroes[i][1]['rating'] > 0:
                pic_path = 'data/heroes/%s.jpg' % heroes[i][0]
                slide.shapes.add_picture(pic_path, Inches(0.5), Inches(4.2) + i * Inches(0.8), height=Inches(0.7))
                tx_box = slide.shapes.add_textbox(Inches(2), Inches(4.3) + i * Inches(0.8), Inches(1.6), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%.1f' % heroes[i][1]['rating']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(24)
                tx_box = slide.shapes.add_textbox(Inches(2.6), Inches(4.2) + i * Inches(0.8), Inches(1.5), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s matches' % heroes[i][1]['matches']
                p.font.size = Pt(16)
                tx_box = slide.shapes.add_textbox(Inches(2.6), Inches(4.45) + i * Inches(0.8), Inches(1), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s - %s' % (heroes[i][1]['wins'], heroes[i][1]['matches'] - heroes[i][1]['wins'])
                p.font.size = Pt(13)
                p.alignment = PP_ALIGN.CENTER

        tx_box = slide.shapes.add_textbox(Inches(4), Inches(3.7), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = 'Most played heroes'
        p.font.size = Pt(16)
        s = sorted(heroes, key=lambda e: e[1]['matches'], reverse=True)
        for i in range(4):
            if s[i][1]['matches'] > 0:
                pic_path = 'data/heroes/%s.jpg' % s[i][0]
                slide.shapes.add_picture(pic_path, Inches(4), Inches(4.2) + i * Inches(0.8), height=Inches(0.7))
                tx_box = slide.shapes.add_textbox(Inches(5.5), Inches(4.3) + i * Inches(0.8), Inches(1.6), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%i' % s[i][1]['matches']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(24)

        tx_box = slide.shapes.add_textbox(Inches(6.5), Inches(3.7), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = 'Worst rating against'
        p.font.size = Pt(16)
        s = sorted(heroes, key=lambda e: e[1]['inv_rating'], reverse=True)
        for i in range(4):
            if s[i][1]['matches_against'] > 0:
                pic_path = 'data/heroes/%s.jpg' % s[i][0]
                slide.shapes.add_picture(pic_path, Inches(6.5), Inches(4.2) + i * Inches(0.8), height=Inches(0.7))
                tx_box = slide.shapes.add_textbox(Inches(8), Inches(4.3) + i * Inches(0.8), Inches(1.6), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = '%.1f' % s[i][1]['inv_rating']
                tf.paragraphs[0].font.bold = True
                tf.paragraphs[0].font.size = Pt(24)
                tx_box = slide.shapes.add_textbox(Inches(8.6), Inches(4.2) + i * Inches(0.8), Inches(1.5), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s matches' % s[i][1]['matches_against']
                p.font.size = Pt(16)
                tx_box = slide.shapes.add_textbox(Inches(8.6), Inches(4.45) + i * Inches(0.8), Inches(1), Inches(0.5))
                tf = tx_box.text_frame
                p = tf.paragraphs[0]
                p.text = '%s - %s' % (s[i][1]['wins_against'], s[i][1]['matches_against'] - s[i][1]['wins_against'])
                p.font.size = Pt(13)
                p.alignment = PP_ALIGN.CENTER

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
        p.font.size = Pt(20)
        p = tf.add_paragraph()
        p.text = 'Best team per hero on each role requires a minimum of %i matches for that hero.' % min_couples_matches
        p.level = 2
        p.font.size = Pt(20)
        p = tf.add_paragraph()
        p.text = 'Best team per hero and player on each role requires a minimum of %i matches.' \
                 % (min_couples_matches / 2)
        p.level = 2
        p.font.size = Pt(20)
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

    def add_match_details(self, to_parse, match_types):
        slide = self.add_slide(1, 152, 251, 152)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = '%s Summary' % self.team_name
        tf = body_shape.text_frame
        tf.text = '%s matches have incomplete data' % to_parse
        p = tf.add_paragraph()
        p.font.size = Pt(20)
        p.text = 'Login every week to OpenDota in order to have complete data to our matches'
        p = tf.add_paragraph()
        p.text = 'Match Summary per Game Type:'
        headers = ['Game Type', 'Wins', 'Matches', 'Win Rate']
        keys = ['lobby_type', 'wins', 'matches', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        widths = [4.5, 1.5, 1.5, 1.5]
        Slides.create_table(slide, match_types, headers, keys, formats, Inches(0.5), Inches(4), Inches(9), 1, 13, 15,
                            widths=widths)

    def add_win_rate_details_slide(self, fb_object, bounties):
        slide = self.add_slide(1, 152, 251, 152)
        shapes = slide.shapes
        title_shape = shapes.title
        title_shape.text = '%s Summary' % self.team_name
        textbox = slide.shapes[1]
        sp = textbox.element
        sp.getparent().remove(sp)

        Slides.text_box(slide, 'First Blood rate', 0.8, 2, font_size=24, bold=True)
        Slides.text_box(slide, '%.2f %%' % fb_object['first_blood_rate'], 4.5, 2, font_size=24)
        Slides.text_box(slide, '%s matches' % fb_object['matches'], 6, 2, font_size=24)
        Slides.text_box(slide, '%s-%s' % (fb_object['first_bloods'], fb_object['matches'] - fb_object['first_bloods']),
                        8, 2, font_size=24)

        Slides.text_box(slide, 'Wins with first blood', 0.8, 2.5, font_size=24, bold=True)
        Slides.text_box(slide, '%.2f %%' % fb_object['wr_if_first_blood'], 4.5, 2.5, font_size=24)
        Slides.text_box(slide, '%s matches' % fb_object['first_bloods'], 6, 2.5, font_size=24)
        Slides.text_box(slide, '%s-%s' % (
                                            fb_object['wins_if_first_blood'],
                                            fb_object['first_bloods'] - fb_object['wins_if_first_blood']),
                        8, 2.5, font_size=24)

        Slides.text_box(slide, 'Wins without first blood', 0.8, 3, font_size=24, bold=True)
        Slides.text_box(slide, '%.2f %%' % fb_object['wr_if_not_first_blood'], 4.5, 3, font_size=24)
        Slides.text_box(slide, '%s matches' % (fb_object['matches'] - fb_object['first_bloods']), 6, 3,
                        font_size=24)
        Slides.text_box(slide, '%s-%s' % (fb_object['wins_if_no_first_blood'],
                                          fb_object['matches'] - fb_object['first_bloods'] - fb_object[
                                              'wins_if_no_first_blood']),
                        8, 3, font_size=24)

        Slides.text_box(slide, 'Bounty runes at minute zero', 0.8, 3.8, font_size=24, bold=True)
        headers = ['Bounties', 'Wins', 'Losses', 'Matches', 'Win Rate']
        keys = ['counts', 'wins', 'losses', 'matches', 'wr']
        formats = ['%s', '%s', '%s', '%s', '%.2f %%']
        Slides.create_table(slide, bounties, headers, keys, formats, Inches(2), Inches(4.5), Inches(6),
                            1, 12, 15)

    def add_win_rate_slide(self, win_rate, match_count, party_size, faction):
        slide = self.add_slide(1, 152, 251, 152)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = '%s Summary' % self.team_name
        tf = body_shape.text_frame
        tf.text = 'Win rate: %.2f %%' % win_rate
        p = tf.add_paragraph()
        p.text = 'Match count: %s' % match_count
        tf.add_paragraph()
        for i in range(1, 6):
            p = tf.add_paragraph()
            p.font.size = Pt(20)
            p.text = '%s matches with party size = %i' % (party_size[i-1], i)
        Slides.text_box(slide, 'Radiant', 0.8, 6, font_size=24, bold=True)
        Slides.text_box(slide, 'Dire', 0.8, 6.6, font_size=24, bold=True)
        Slides.text_box(slide, '%.2f %%' % faction['r_wr'], 2.5, 6, font_size=24)
        Slides.text_box(slide, '%.2f %%' % faction['d_wr'], 2.5, 6.6, font_size=24)
        Slides.text_box(slide, '%s matches' % (faction['r_win'] + faction['r_loss']), 4, 6, font_size=24)
        Slides.text_box(slide, '%s matches' % (faction['d_win'] + faction['d_loss']), 4, 6.6, font_size=24)
        Slides.text_box(slide, '%s-%s' % (faction['r_win'], faction['r_loss']), 6, 6, font_size=24)
        Slides.text_box(slide, '%s-%s' % (faction['d_win'], faction['d_loss']), 6, 6.6, font_size=24)

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

    def add_win_rate_by_date(self, input_data, label):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = '%s Win Rate by %s' % (self.team_name, label)

        data = {a: b for a, b in input_data.items() if int(a) < 12} if label == 'Hour' else input_data
        headers = [a for a in data.keys()]
        keys = [str(i) for i in range(len(data))]
        formats = ['%.1f %%'] * len(data)
        table_data = [{str(i): o['wr'] for i, o in zip(range(len(data)), data.values())}]
        Slides.create_table(slide, table_data, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 12, 15)

        if label == 'Hour':
            data = {a: b for a, b in input_data.items() if int(a) >= 12}
            headers = [a for a in data.keys()]
            keys = [str(i) for i in range(len(data))]
            formats = ['%.1f %%'] * len(data)
            table_data = [{str(i): o['wr'] for i, o in zip(range(len(data)), data.values())}]
            Slides.create_table(slide, table_data, headers, keys, formats, Inches(0.5), Inches(2.5), Inches(9), 1, 12,
                                15)

        data = input_data
        chart_data = ChartData()
        chart_data.categories = data.keys()
        chart_data.add_series('Wins', [o['wins'] for o in data.values()])
        chart_data.add_series('Losses', [o['losses'] for o in data.values()])
        graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(3.5), Inches(9),
                                               Inches(4),
                                               chart_data)
        chart = graphic_frame.chart
        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels
        data_labels.font.size = Pt(9)
        data_labels.font.color.rgb = RGBColor(0x0A, 0x42, 0x80)
        data_labels.position = XL_LABEL_POSITION.INSIDE_END
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.RIGHT
        chart.legend.include_in_layout = False

    def add_compositions(self, compositions):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Lane Compositions'
        headers = ['Lane Composition', 'Wins', 'Matches', 'Win Rate']
        keys = ['comp', 'wins', 'matches', 'wr']
        formats = ['%s', '%s', '%s', '%.2f %%']
        Slides.create_table_with_text_boxes(slide, compositions, headers, keys, formats, 0.5, 1.5, 9, 12, 14)

    def add_win_rate_heroes(self, versus, text):
        versus = [v for v in versus if v['matches'] > 0]
        for c in range(math.ceil(len(versus)/14)):
            slide = self.add_slide(5, 204, 255, 204)
            title_shape = slide.shapes.title
            title_shape.text = '%s Performance %s Heroes' % (self.team_name, text)
            for y in range(2):
                for x in range(7):
                    index = c*14 + y*7 + x
                    if len(versus) > index:
                        hero = versus[index]
                        pic_path = 'data/heroes/%s.jpg' % hero['id']
                        slide.shapes.add_picture(pic_path, Inches(0.5) + y * Inches(5), Inches(1.8) + x * Inches(0.8),
                                                 height=Inches(0.7))
                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(1.5),
                                                          Inches(1.9) + x * Inches(0.8), Inches(1), Inches(0.4))
                        tf = tx_box.text_frame
                        tf.text = '%.1f' % hero['rating']
                        tf.paragraphs[0].font.bold = True
                        tf.paragraphs[0].font.size = Pt(24)

                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2.3),
                                                          Inches(2) + x * Inches(0.8), Inches(1.5),
                                                          Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = '%i-%i (%.2f %% wr)' % (hero['wins'], hero['matches'] - hero['wins'], hero['wr'])
                        p.font.size = Pt(16)

                        tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2.3),
                                                          Inches(1.8) + x * Inches(0.8), Inches(1.5),
                                                          Inches(0.5))
                        tf = tx_box.text_frame
                        p = tf.paragraphs[0]
                        p.text = hero['name']
                        p.font.size = Pt(12)
                        p.font.bold = True

    def add_most_played(self, heroes, most_played):
        if not most_played and len(heroes) == 0:
            return None
        rows = 7
        columns = 2 if most_played else 6
        for c in range(math.ceil(len(heroes)/(columns*rows))):
            slide = self.add_slide(5, 176, 255, 176) if most_played else self.add_slide(5, 140, 255, 140)
            title_shape = slide.shapes.title
            title_shape.text = '%s\'s %s Heroes' % (self.team_name, 'Most Played' if most_played else 'Not Played')
            for y in range(columns):
                for x in range(rows):
                    index = c*(columns * rows) + y*rows + x
                    if len(heroes) > index:
                        hero = heroes[index]
                        pic_path = 'data/heroes/%s.jpg' % hero['id']
                        slide.shapes.add_picture(pic_path, Inches(0.5) + y * Inches(9 / columns),
                                                 Inches(1.8) + x * Inches(0.8),
                                                 height=Inches(0.7))
                        if most_played:
                            tx_box = slide.shapes.add_textbox(Inches(0.5) + y * Inches(5) + Inches(2),
                                                              Inches(1.7) + x * Inches(0.8), Inches(1.5), Inches(0.5))
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

    def add_match_summary_by_player(self, summary, team, party_size):
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
        headers = ['Player', 'Total Matches', 'Matches with %s' % self.team_name, '%% with %s' % self.team_name,
                   'with party >= %s' % party_size]
        keys = ['player', 'matches', 'team_matches', 'perc_with_team', 'matches_party']
        formats = ['%s', '%s', '%s', '%.2f %%', '%s']
        Slides.create_table_with_text_boxes(slide,
                                            sorted([x for x in summary if x['team_matches'] > 0],
                                                   key=lambda e: e['team_matches'], reverse=True),
                                            headers, keys, formats, 0.5, 1.35, 9, 11, 14, line_spacing=0.225)

    def add_tier_slides(self, tier, category):
        texts = tier.list_to_print()

        slide = self.add_slide(6, 255, 255, 224)
        left = top = width = height = Inches(0.4)
        txt_box = slide.shapes.add_textbox(left, top, width, height)
        tf = txt_box.text_frame
        tf.text = texts[1]
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.size = Pt(22)

        txt_box = slide.shapes.add_textbox(Inches(8.5), top, width, height)
        tf = txt_box.text_frame
        tf.text = "Tier points: %s" % tier.weight
        tf.paragraphs[0].font.size = Pt(14)

        scores = tier.get_top_three()
        self.add_top_three_small_table(scores, slide, tier.is_max, category, 0.3, 1)

        if len(tier.scores_array) > 0:
            chart_data = CategoryChartData()
            chart_data.categories = [x.name for x in tier.scores_array]
            chart_data.add_series(texts[1], [x.score for x in tier.scores_array])
            x, y, cx, cy = Inches(0.1), Inches(2.8), Inches(5), Inches(4.7)
            chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data).chart
            category_axis = chart.category_axis
            category_axis.tick_labels.font.size = Pt(9)
            value_axis = chart.value_axis
            tick_labels = value_axis.tick_labels
            tick_labels.font.size = Pt(12)

        txt_box = slide.shapes.add_textbox(Inches(5.2), Inches(0.6), width, height)
        tf = txt_box.text_frame
        for i in range(2, len(texts)):
            p = tf.add_paragraph()
            p.text = texts[i]
            p.font.size = Pt(10)
            if texts[i].startswith("Tier"):
                p.font.bold = True

    def add_top_three_small_table(self, scores, slide, is_max, category, left, top):
        pos = [(0, '1'), (1, '2'), (2, '3')]
        spacing = 1.6
        val = min(3, len(scores))
        for i, name in pos[0:val]:
            Slides.text_box(slide, scores[i].name, left + spacing * i, top, spacing,
                            font_size=18, alignment=PP_ALIGN.CENTER, bold=True)
            if not isinstance(scores[i].score, str):
                fmt = (category.max_format if is_max else category.avg_format) % scores[i].score
            else:
                fmt = scores[i].score
            Slides.text_box(slide, "%s %s" % (fmt, category.unit), left + spacing * i, top + 1.3, spacing,
                            font_size=14, alignment=PP_ALIGN.CENTER)
            pic_path = 'data/pics/%s.jpg' % self.players[scores[i].name]
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(left + 0.4 + spacing * i), Inches(top + 0.45),
                                         height=Inches(0.8))

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

    def add_draft_suggestion(self, heroes, players, compositions):
        slide = self.add_slide(5, 152, 251, 152)
        slide.shapes.title.text = "Draft Suggestion"
        i = 0
        Slides.text_box(slide, "%.2f" % compositions[0][0], 8, 2.8, bold=True,
                        width=1.5, font_size=24, alignment=PP_ALIGN.CENTER)
        for j in range(1, min(len(compositions), 8)):
            Slides.text_box(slide, "%.2f" % compositions[j][0], 8, 4.5 + (j - 1) * 0.4, bold=True,
                            width=1.5, font_size=15, alignment=PP_ALIGN.CENTER)
        for ri, r in roles().items():
            Slides.text_box(slide, r, 0.5 + 1.5 * i, 1.5, width=1.5, font_size=14, bold=True, alignment=PP_ALIGN.CENTER)
            pic_path = 'data/heroes/%i.jpg' % compositions[0][1][ri-1][1]
            slide.shapes.add_picture(pic_path, Inches(0.7 + 1.5 * i), Inches(1.85), height=Inches(0.55))
            Slides.text_box(slide, heroes[compositions[0][1][ri-1][1]], 0.5 + 1.5 * i, 2.5,
                            width=1.5, font_size=16, alignment=PP_ALIGN.CENTER)

            pic_path = 'data/pics/%i.jpg' % compositions[0][1][ri-1][2]
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(0.85 + 1.5 * i), Inches(3), height=Inches(0.7))
            Slides.text_box(slide, players[compositions[0][1][ri-1][2]], 0.5 + 1.5 * i, 3.8,
                            width=1.5, font_size=16, alignment=PP_ALIGN.CENTER)

            for j in range(1, min(len(compositions), 8)):
                pic_path = 'data/heroes/%i.jpg' % compositions[j][1][ri - 1][1]
                slide.shapes.add_picture(pic_path, Inches(0.5 + 1.5 * i), Inches(4.5 + (j - 1) * 0.4),
                                         height=Inches(0.3))
                pic_path = 'data/pics/%i.jpg' % compositions[j][1][ri - 1][2]
                if os.path.isfile(pic_path):
                    slide.shapes.add_picture(pic_path, Inches(1.12 + 1.5 * i), Inches(4.5 + (j - 1) * 0.4),
                                             height=Inches(0.3))
            i += 1

    def add_best_team(self, best_team):
        slide = self.add_slide(5, 152, 251, 152)
        slide.shapes.title.text = "Best Team by Hero Performance"
        i = 0
        for r in roles().values():
            if len(best_team[r]) > 0:
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
                for j in range(1, min(len(best_team[r]), 5)):
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

    def add_couples(self, couples, text):
        inv_p = {v: k for k, v in self.players.items()}
        slide = self.add_slide(5, 255, 105, 180)
        slide.shapes.title.text = "%s %s Couples" % (self.team_name, text)
        y = 5
        x = 2
        left = 0.6
        player_size = 1
        pic_size = 0.8
        spacing = 2
        top = 1.2
        column_width = 4.8
        for i in range(x):
            for j in range(y):
                if i * y + j < len(couples):
                    c = couples[i * y + j]
                    Slides.text_box(slide, inv_p[c['p1']], left + column_width * i, top * (1 + j),
                                    width=player_size, font_size=14, alignment=PP_ALIGN.CENTER, bold=True)
                    Slides.text_box(slide, inv_p[c['p2']], left + player_size + spacing + column_width * i,
                                    top * (1 + j),
                                    width=player_size, font_size=14, alignment=PP_ALIGN.CENTER, bold=True)
                    pic_path = 'data/pics/%s.jpg' % c['p1']
                    if os.path.isfile(pic_path):
                        slide.shapes.add_picture(pic_path, Inches(left + 0.1 + column_width * i),
                                                 Inches(top * (1 + j) + 0.35), height=Inches(pic_size))
                    pic_path = 'data/pics/%s.jpg' % c['p2']
                    if os.path.isfile(pic_path):
                        slide.shapes.add_picture(pic_path,
                                                 Inches(left + 0.1 + player_size + spacing + column_width * i),
                                                 Inches(top * (1 + j) + 0.35), height=Inches(pic_size))
                    Slides.text_box(slide, '%.1f' % c['rating'], left + column_width * i + player_size, top * (1 + j),
                                    width=spacing, alignment=PP_ALIGN.CENTER, font_size=24, bold=True)
                    Slides.text_box(slide, '%.2f %%' % c['wr'], left + column_width * i + player_size,
                                    top * (1 + j) + 0.5,
                                    width=spacing, alignment=PP_ALIGN.CENTER, font_size=16)
                    Slides.text_box(slide, '%s matches (%s - %s)' % (c['matches'], c['wins'], c['matches'] - c['wins']),
                                    left + column_width * i + player_size, top * (1 + j) + 0.9,
                                    width=spacing, alignment=PP_ALIGN.CENTER, font_size=12)

    def add_best_team_by_player(self, best_team):
        slide = self.add_slide(5, 152, 251, 152)
        slide.shapes.title.text = "Best Player/Hero by Position"
        i = 0
        for r in roles().values():
            if len(best_team[r]) > 0:
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

                for j in range(1, min(len(best_team[r]), 5)):
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
        Slides.create_table_with_text_boxes(slide, [x for x in scores if x['gold'] + x['silver'] + x['bronze'] > 0],
                                            headers, keys, formats, 2, 1.5, 6, 11, 14)

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
        Slides.create_table_with_text_boxes(slide, [x for x in scores if x['points'] > 0], headers, keys, formats, 3,
                                            1.5, 3, 11, 14)

    def add_achievement_slide(self, achievement, result):
        inv_p = {v: k for k, v in self.players.items()}
        slide = self.add_slide(6, 0xCC, 0xCC, 0x66)
        left = top = width = height = Inches(0.4)
        txt_box = slide.shapes.add_textbox(left, top, width, height)
        tf = txt_box.text_frame
        tf.text = achievement.name
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].font.bold = True

        txt_box = slide.shapes.add_textbox(left, Inches(0.9), width, height)
        tf = txt_box.text_frame
        tf.text = achievement.description
        tf.paragraphs[0].font.size = Pt(18)
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

        txt_box = slide.shapes.add_textbox(left, Inches(1.3), width, height)
        tf = txt_box.text_frame
        tf.text = 'Achievement rate: %.2f %% (%i times in %i matches)' % (
                                            result['wr'], result['wins'], result['matches'])
        tf.paragraphs[0].font.size = Pt(12)

        if achievement.img_path is not None:
            pic_path = 'data/achievements/%s' % achievement.img_path
            if os.path.isfile(pic_path):
                slide.shapes.add_picture(pic_path, Inches(7.5), Inches(0.25), height=Inches(1.5))
        if achievement.special_description:
            txt_box = slide.shapes.add_textbox(Inches(0.2), Inches(6.7), Inches(9.5), height)
            tf = txt_box.text_frame
            tf.text = 'Hero list: %s' % sequence(achievement.heroes)
            tf.word_wrap = True
            tf.paragraphs[0].font.size = Pt(10)

        if result['wins'] > 0:
            txt_box = slide.shapes.add_textbox(left + Inches(0.45), Inches(1.8), width, height)
            tf = txt_box.text_frame
            tf.text = 'Player'
            tf.paragraphs[0].font.size = Pt(12)
            txt_box = slide.shapes.add_textbox(left + Inches(1.8), Inches(1.8), width, height)
            tf = txt_box.text_frame
            tf.text = '⭐'
            tf.paragraphs[0].font.size = Pt(14)
            txt_box = slide.shapes.add_textbox(left + Inches(2.5), Inches(1.8), width, height)
            tf = txt_box.text_frame
            tf.text = 'Match List'
            tf.paragraphs[0].font.size = Pt(12)
            i = 0
            for player_id, matches in sorted([(k, v) for k, v in result['winners'].items() if len(v) > 0],
                                             key=lambda e: len(e[1]), reverse=True)[:10]:
                pic_path = 'data/pics/%s.jpg' % player_id
                if os.path.isfile(pic_path):
                    slide.shapes.add_picture(pic_path, left, Inches(2.3 + 0.42 * i), height=Inches(0.4))
                txt_box = slide.shapes.add_textbox(left + Inches(0.45), Inches(2.3 + 0.42 * i), width, height)
                tf = txt_box.text_frame
                tf.text = inv_p[player_id]
                tf.paragraphs[0].font.size = Pt(16)
                txt_box = slide.shapes.add_textbox(left + Inches(1.8), Inches(2.3 + 0.42 * i), width, height)
                tf = txt_box.text_frame
                tf.text = '%i' % len(matches)
                tf.paragraphs[0].font.size = Pt(18)
                tf.paragraphs[0].font.bold = True
                txt_box = slide.shapes.add_textbox(left + Inches(2.5), Inches(2.35 + 0.42 * i), width, height)
                tf = txt_box.text_frame
                tf.text = sequence(['%s' % i for i in matches], 5)
                tf.paragraphs[0].font.size = Pt(12)
                i += 1
        else:
            txt_box = slide.shapes.add_textbox(left + Inches(0.45), Inches(2.5), width, height)
            tf = txt_box.text_frame
            tf.text = 'No player earned this achievement.'
            tf.paragraphs[0].font.size = Pt(16)

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
            for i in range(0, len(popular_vote_category['winner'])):
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
    def text_box(slide, text, left, top, width=None, font_size=None, alignment=None, bold=False):
        width = width if width is not None else 1
        tx_box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
        tf = tx_box.text_frame
        tf.text = text
        tf.paragraphs[0].font.bold = bold
        if font_size is not None:
            tf.paragraphs[0].font.size = Pt(font_size)
        if alignment is not None:
            tf.paragraphs[0].alignment = alignment

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
    def create_table_with_text_boxes(slide, data, headers, keys, formats, left, top, width, font_size,
                                     header_size, widths=None, line_spacing=0.25):
        if widths is None:
            widths = [width / len(headers) for _ in range(len(headers))]
        for i in range(len(headers)):
            Slides.text_box(slide, headers[i], left + sum(widths[:i]), top, widths[i], font_size=header_size, bold=True)
        for i in range(len(data)):
            for j in range(len(keys)):
                Slides.text_box(slide, formats[j] % data[i][keys[j]], left + sum(widths[:j]) + 0.05,
                                top + 0.1 + line_spacing * (i + 1), widths[j], font_size=font_size)

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
