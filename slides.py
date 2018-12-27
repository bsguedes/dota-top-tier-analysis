from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LEGEND_POSITION
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.chart.data import ChartData


class Slides:
    def __init__(self, team_name, tit, sub, players, tiers):
        self.presentation = Presentation()
        self.team_name = team_name
        self.players = players
        self.tiers = tiers
        self.add_divider_slide(tit, "%s" % sub)

    def add_divider_slide(self, text, sub_text):
        slide_layout = self.presentation.slide_layouts[0]
        slide = self.presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = text
        subtitle.text = sub_text

    def add_intro_slide(self, match_count, min_player_count, min_matches):
        slide_layout = self.presentation.slide_layouts[1]
        slide = self.presentation.slides.add_slide(slide_layout)
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
        p.text = 'The list of players is: %s' % (', '.join(self.players.keys()))
        p.level = 1

    def add_win_rate_slide(self, win_rate):
        slide_layout = self.presentation.slide_layouts[1]
        slide = self.presentation.slides.add_slide(slide_layout)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]

        title_shape.text = '%s Win Rate' % self.team_name
        tf = body_shape.text_frame
        tf.text = 'Win rate: %.2f %%' % win_rate

        left = Inches(2)
        top = Inches(2.5)
        width = Inches(6)
        height = Inches(0.5)
        tx_box = slide.shapes.add_textbox(left, top, width, height)
        tf = tx_box.text_frame
        tf.text = "%s players with most matches" % self.team_name
        # self.add_top_three_table([], slide, Inches(1), Inches(2.8))

    def add_tier_slides(self, tier, category):
        texts = tier.list_to_print()

        slide_layout = self.presentation.slide_layouts[5]
        slide = self.presentation.slides.add_slide(slide_layout)
        title_shape = slide.shapes.title
        title_shape.text = texts[1]
        scores = tier.get_top_three()
        self.add_top_three_table(scores, slide, tier.is_max, category.unit, Inches(1), Inches(1.8))

        slide_layout = self.presentation.slide_layouts[6]
        slide = self.presentation.slides.add_slide(slide_layout)
        left = top = width = height = Inches(0.4)
        txt_box = slide.shapes.add_textbox(left, top, width, height)
        tf = txt_box.text_frame
        tf.text = texts[1]
        tf.paragraphs[0].font.bold = True
        for i in range(2, len(texts)):
            p = tf.add_paragraph()
            p.text = texts[i]
            p.font.size = Pt(14)

    def add_top_three_table(self, scores, slide, is_max, unit, left, top):
        for i, name in [(0, '1st'), (1, '2nd'), (2, '3rd')]:
            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(0), Inches(2.5), Inches(0.5))
            tf = tx_box.text_frame
            p = tf.paragraphs[0]
            p.text = name
            p.font.size = Pt(24)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER

            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(0.6), Inches(2.5), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = scores[i].name
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER

            tx_box = slide.shapes.add_textbox(left + Inches(3*i), top + Inches(1.2), Inches(2.5), Inches(0.5))
            tf = tx_box.text_frame
            text_format = "%s %s" if is_max else "%.2f %s"
            tf.text = text_format % (scores[i].score, unit)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER

            pic_path = 'data/pics/%s.jpg' % self.players[scores[i].name]
            slide.shapes.add_picture(pic_path, left + Inches(3*i), top + Inches(1.8), height=Inches(2.5))

    def add_popular_vote_category_slides(self, popular_vote_category):
        slide_layout = self.presentation.slide_layouts[1]
        slide = self.presentation.slides.add_slide(slide_layout)
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
            tx_box = slide.shapes.add_textbox(Inches(6), Inches(1.8), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = "Vencedores"
            for i in range(0, len(popular_vote_category['winner'])):
                pic_path = 'data/pics/%s.jpg' % self.players[popular_vote_category['winner'][i]]
                slide.shapes.add_picture(pic_path, Inches(6), Inches(2.5 + 2*i), height=Inches(1.8))
        elif 'winner' in popular_vote_category:
            tx_box = slide.shapes.add_textbox(Inches(6), Inches(1.8), Inches(2), Inches(0.5))
            tf = tx_box.text_frame
            tf.text = "Vencedor"
            pic_path = 'data/pics/%s.jpg' % self.players[popular_vote_category['winner']]
            slide.shapes.add_picture(pic_path, Inches(6), Inches(2.5), height=Inches(1.8))

        slide_layout = self.presentation.slide_layouts[5]
        slide = self.presentation.slides.add_slide(slide_layout)
        slide.shapes.title.text = popular_vote_category['category']
        chart_data = ChartData()
        chart_data.categories = popular_vote_category['options']
        v = sum(popular_vote_category['votes'])
        chart_data.add_series("%i answers" % v, [x / v for x in popular_vote_category['votes']])
        chart = slide.shapes.add_chart(
            XL_CHART_TYPE.PIE, Inches(1), Inches(1.8), Inches(7), Inches(5), chart_data
        ).chart
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

    def save(self):
        self.presentation.save('report.pptx')
