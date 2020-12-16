from fpdf import FPDF
import datetime


def today_string():
    today = datetime.date.today()
    today = today.strftime('%Y年%m月%d日')
    return today


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Yahei", '', "rsc/Yahei.ttf", True)
        self.add_font("dkzt", '', "rsc/dkzt.ttf", True)

    def set_title(self, title):
        self.set_xy(0, 0)
        self.set_font("Yahei", '', 24)
        self.cell(210, 40, txt=title, border=0, align="C")

    def set_date(self, date=True):
        self.set_xy(0, 20)
        self.set_font("Yahei", '', 14)
        underline = '_' * 13
        if date:
            self.multi_cell(195, 10, txt=today_string(), border=0, align="R")
        else:
            self.multi_cell(195, 10, txt='', border=0, align='R')
        self.multi_cell(210, 13, txt='姓名' + underline + '开始时间' + underline + '结束时间' + underline + '得分' + underline,
                        border=0, align="C")

    def set_quizzes(self, quizzes):
        start_x, start_y = 15, 50
        end_x, end_y = 15, 274
        col_in_a_row = 3
        rows = len(quizzes) // col_in_a_row + 1 if len(quizzes) % col_in_a_row > 0 else len(quizzes) // col_in_a_row
        cell_height = (end_y - start_y) / rows
        cell_width = 180 / col_in_a_row
        self.set_xy(start_x, start_y)
        self.set_font("dkzt", '', 12)
        for index in range(len(quizzes)):
            row = index // 3
            col = index % 3
            formula = quizzes[index]
            next_x = start_x + cell_width * (col + 1) if col < 2 else start_x
            next_y = start_y + cell_height * row if col < 2 else start_y + cell_height * (row + 1)
            self.multi_cell(cell_width, cell_height, txt=formula, border=0, align="L")
            self.set_xy(next_x, next_y)


if __name__ == '__main__':
    pass
