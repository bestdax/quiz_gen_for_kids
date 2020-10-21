from fpdf import FPDF
from quizzes import quiz_gen, today_string


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Yahei", '', "Yahei.ttf", True)
        self.add_font("dkzt", '', "dkzt.ttf", True)

    def set_title(self, title):
        self.set_xy(0, 0)
        self.set_font("Yahei", '', 24)
        self.cell(210, 40, txt=title, border=0, ln=2, align="C")

    def set_date(self):
        self.set_xy(0, 20)
        self.set_font("Yahei", '', 14)
        underline = '_' * 13
        self.multi_cell(195, 10, txt=today_string(), border=0, ln=2, align="R")
        self.multi_cell(210, 13, txt='姓名' + underline + '开始时间' + underline + '结束时间' + underline + '得分' + underline,
                        border=0, ln=2, align="C")

    def set_quizzes(self):
        start_x, start_y = 15, 50
        cell_height = 6.6
        cell_width = 60
        self.set_xy(start_x, start_y)
        self.set_font("dkzt", '', 12)
        quizzes = quiz_gen().split('\n')
        for index in range(100):
            row = index // 3
            col = index % 3
            formula = quizzes[index]
            next_x = start_x + cell_width * (col + 1) if col < 2 else start_x
            next_y = start_y + cell_height * row if col < 2 else start_y + cell_height * (row + 1)
            self.multi_cell(cell_width, cell_height, txt=formula, border=0, ln=2, align="L")
            self.set_xy(next_x, next_y)


if __name__ == '__main__':
    pdf = PDF()
    pdf.add_page()
    pdf.set_title('四则运算练习')
    pdf.set_date()
    pdf.set_quizzes()
    pdf.output('quizzes.pdf', 'F')
