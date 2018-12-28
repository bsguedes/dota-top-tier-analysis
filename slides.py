from pptx import Presentation
from pptx.util import Inches, Pt
from tier import TierItem
from pptx.enum.text import PP_ALIGN
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LEGEND_POSITION
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.chart.data import ChartData
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor


class Slides:
    def __init__(self, team_name, tit, sub, players):
        self.presentation = Presentation()
        self.team_name = team_name
        self.players = players
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
        p.text = 'The list of players is: %s' % (', '.join(self.players.keys()))
        p.level = 1
        p.font.size = Pt(16)

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
        title_shape.text = 'Top 10 Comebacks'
        headers = ['Match ID', 'Gold', 'Players']
        keys = ['match', 'gold', 'players']
        formats = ['%s', '%s', '%s']
        Slides.create_table(slide, comebacks, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15)

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Top 10 Throws'
        Slides.create_table(slide, throws, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 13, 15)

    def add_match_summary_by_player(self, summary, team):
        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Most Matches Played'
        scores = [TierItem(summary[i]['player'], summary[i]['matches'], '') for i in range(0, 3)]
        self.add_top_three_table(scores, slide, True, 'matches', Inches(1), Inches(2))

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Most Matches Played with %s' % self.team_name
        scores = [TierItem(team[i]['player'], team[i]['team_matches'], '') for i in range(0, 3)]
        self.add_top_three_table(scores, slide, True, 'matches', Inches(1), Inches(2))

        slide = self.add_slide(5, 152, 251, 152)
        title_shape = slide.shapes.title
        title_shape.text = 'Match Summary by Player'
        headers = ['Player', 'Total Matches', 'Matches with %s' % self.team_name, '%% with %s' % self.team_name]
        keys = ['player', 'matches', 'team_matches', 'perc_with_team']
        formats = ['%s', '%s', '%s', '%.2f %%']
        Slides.create_table(slide, summary, headers, keys, formats, Inches(0.5), Inches(1.5), Inches(9), 1, 11, 14)

    def add_tier_slides(self, tier, category):
        texts = tier.list_to_print()

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = texts[1]
        scores = tier.get_top_three()
        self.add_top_three_table(scores, slide, tier.is_max, category.unit, Inches(0.7), Inches(1.8))

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
        tf.text = "%s - weights %i points" % (texts[1], tier.weight)
        tf.paragraphs[0].font.bold = True
        for i in range(2, len(texts)):
            p = tf.add_paragraph()
            p.text = texts[i]
            p.font.size = Pt(14)

    def add_top_three_table(self, scores, slide, is_max, unit, left, top):
        for i, name in [(0, '1st'), (1, '2nd'), (2, '3rd')]:
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
            text_format = "%s %s" if is_max else "%.2f %s"
            tf.text = text_format % (scores[i].score, unit)
            p = tf.paragraphs[0]
            p.font.size = Pt(22)
            p.alignment = PP_ALIGN.CENTER

            pic_path = 'data/pics/%s.jpg' % self.players[scores[i].name]
            slide.shapes.add_picture(pic_path, left + Inches(3*i), top + Inches(2.5), height=Inches(2.5))

    def add_results_slides(self, medals, points):
        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Results Compilation'
        scores = [TierItem(medals[i][0], medals[i][1], '') for i in range(0, 3)]
        self.add_top_three_table(scores, slide, True, '', Inches(0.7), Inches(1.8))

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Results Compilation'
        headers = ['Player', 'Gold', 'Silver', 'Bronze']
        keys = ['player', 'gold', 'silver', 'bronze']
        scores = [{'player': k, 'gold': v[0], 'silver': v[1], 'bronze': v[2]} for k, v in medals]
        formats = ['%s', '%s', '%s', '%s']
        Slides.create_table(slide, scores, headers, keys, formats, Inches(2), Inches(1.5), Inches(6), 1, 11, 14)

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Weighted Points Competition'
        scores = [TierItem(points[i][0], points[i][1], '') for i in range(0, 3)]
        self.add_top_three_table(scores, slide, True, '', Inches(0.7), Inches(1.8))

        slide = self.add_slide(5, 255, 255, 224)
        title_shape = slide.shapes.title
        title_shape.text = 'Top Tier Weighted Points Competition'
        headers = ['Player', 'Points']
        keys = ['player', 'points']
        scores = [{'player': k, 'points': v} for k, v in points]
        formats = ['%s', '%s']
        Slides.create_table(slide, scores, headers, keys, formats, Inches(3), Inches(1.5), Inches(3), 1, 11, 14)

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
                slide.shapes.add_picture(pic_path, Inches(8.3), Inches(2.3 + 1.55 * i), height=Inches(1))
                tx_box = slide.shapes.add_textbox(Inches(8.3), Inches(2.3 + 1.55 * i + 1.08), Inches(2), Inches(0.4))
                tf = tx_box.text_frame
                tf.text = popular_vote_category['winner'][i]
        elif 'winner' in popular_vote_category:
            tx_box = slide.shapes.add_textbox(Inches(8), Inches(1.8), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = "Vencedor"
            pic_path = 'data/pics/%s.jpg' % self.players[popular_vote_category['winner']]
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
        for i in range(0, 5):
            pic_path = 'data/pics/%s.jpg' % self.players[top[i]]
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
        self.presentation.save('report.pptx')

    @staticmethod
    def change_slide_color(slide, r, g, b):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(r, g, b)

    @staticmethod
    def create_table(slide, data, headers, keys, formats, left, top, width, height, font_size, header_size):
        table_shape = slide.shapes.add_table(len(data) + 1, len(headers), left, top, width, height)
        table = table_shape.table
        for i in range(0, len(headers)):
            table.cell(0, i).text = headers[i]
        for i in range(0, len(data)):
            for j in range(0, len(keys)):
                table.cell(i + 1, j).text = formats[j] % data[i][keys[j]]
        Slides.set_table_font_size(table, font_size)
        for i in range(0, len(keys)):
            table.cell(0, i).text_frame.paragraphs[0].runs[0].font.size = Pt(header_size)

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
