from pptx import Presentation
from pptx.util import Inches


class Slides:
    def __init__(self, team_name, tit, sub, players, tiers):
        self.presentation = Presentation()
        self.team_name = team_name
        self.players = players
        self.tiers = tiers
        slide_layout = self.presentation.slide_layouts[0]
        slide = self.presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = tit
        subtitle.text = "%s" % sub

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
        p.text = 'Matches with at least %i %s players.' % (min_player_count, self.team_name)
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
        self.add_top_three_table([], slide, Inches(1), Inches(2.8))

    def add_top_three_table(self, scores, slide, left, top):
        tx_box = slide.shapes.add_textbox(left + Inches(1), top + Inches(0), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = "1st"
        tx_box = slide.shapes.add_textbox(left + Inches(4), top + Inches(0), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = "2nd"
        tx_box = slide.shapes.add_textbox(left + Inches(7), top + Inches(0), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = "3rd"

        tx_box = slide.shapes.add_textbox(left + Inches(0), top + Inches(1.3), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = scores[0]['name']
        tx_box = slide.shapes.add_textbox(left + Inches(0), top + Inches(1.3), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = scores[1]['name']
        tx_box = slide.shapes.add_textbox(left + Inches(0), top + Inches(1.3), Inches(1.5), Inches(0.5))
        tf = tx_box.text_frame
        tf.text = scores[2]['name']

    def save(self):
        self.presentation.save('report.pptx')
