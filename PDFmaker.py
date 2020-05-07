import os
import matplotlib.font_manager as fontman
from fpdf import FPDF


# method printing to pdf
# arguments: list of report values (as returned by db.getReport(), path to reports directory
def find_font_file(query):
    result = list(filter(lambda path: query in os.path.basename(path), fontman.findSystemFonts()))
    return result


def makePDF(printed_values, pdf_save_path):
    report_no = printed_values[0]

    # printing parameters
    # enable generalization
    # currenty set to printing on A4 format (210x297 mm)
    W = 190
    H = 278
    f_size = 5  # font size
    c_height = 0.02 * H  # cell height

    rep = FPDF()
    rep.add_page()

    if find_font_file('arial.ttf'):
        rep.add_font('FONT', '', find_font_file('arial.ttf')[0], uni=True)
    elif find_font_file('times.ttf'):
        rep.add_font('FONT', '', find_font_file('times.ttf')[0], uni=True)

    elif find_font_file('DejaVuSans.ttf'):
        rep.add_font('FONT', '', find_font_file('DejaVuSans.ttf')[0], uni=True)
    elif find_font_file('Ubuntu-R.ttf'):
        rep.add_font('FONT', '', find_font_file('Ubuntu-R.ttf')[0], uni=True)

    elif find_font_file('Arial.ttf'):
        rep.add_font('FONT', '', find_font_file('Arial.ttf')[0], uni=True)
    elif find_font_file('Times New Roman.ttf'):
        rep.add_font('FONT', '', find_font_file('Times New Roman.ttf')[0], uni=True)

    if find_font_file('arialbd.ttf'):
        rep.add_font('FONT', 'B', find_font_file('arialbd.ttf')[0], uni=True)
    elif find_font_file('timesbd.ttf'):
        rep.add_font('FONT', 'B', find_font_file('timesbd.ttf')[0], uni=True)

    elif find_font_file('DejaVuSans-Bold.ttf'):
        rep.add_font('FONT', 'B', find_font_file('DejaVuSans-Bold.ttf')[0], uni=True)
    elif find_font_file('Ubuntu-B.ttf'):
        rep.add_font('FONT', 'B', find_font_file('Ubuntu-B.ttf')[0], uni=True)

    elif find_font_file('Arial Bold.ttf'):
        rep.add_font('FONT', 'B', find_font_file('Arial Bold.ttf')[0], uni=True)
    elif find_font_file('Times New Roman Bold.ttf'):
        rep.add_font('FONT', 'B', find_font_file('Times New Roman Bold.ttf')[0], uni=True)

    f_type = "FONT"  # font type

    rep.set_font(f_type, 'B', size=5 * f_size)
    rep.cell(0.8 * W, 2.5 * c_height, txt="OPIS ZDARZENIA", align="C", border=1, ln=0)
    rep.set_font(f_type, 'B', size=3 * f_size)
    rep.cell(0.2 * W, 2.5 * c_height, txt="  LP.   " + str(report_no), align="L", border=1, ln=1)

    rep.ln(c_height)

    rep.set_font(f_type, 'B', size=2 * f_size)
    left_margin = rep.get_x()
    ybefore = rep.get_y()
    rep.multi_cell(0.33 * W, 1.2 * c_height, txt=" DATA WYJAZDU:\n " + printed_values[1], align="L", border=1)
    rep.set_xy(W * 0.33 + left_margin, ybefore)
    rep.multi_cell(0.33 * W, 1.2 * c_height, txt=" GODZINA WYJAZDU:\n " + printed_values[2], align="L", border=1)
    rep.set_xy(W * 0.66 + left_margin, ybefore)
    rep.multi_cell(0.34 * W, 1.2 * c_height, txt=" NA MIEJSCU: \n " + printed_values[3], align="L", border=1)

    ybefore = rep.get_y()
    left_margin = rep.get_x()
    rep.multi_cell(0.33 * W, 2 * c_height, txt=" MIEJSCE ZDARZENIA:\n " + printed_values[4], align="L", border=1)
    rep.set_xy(W * 0.33 + left_margin, ybefore)
    rep.multi_cell(0.67 * W, 2 * c_height, txt=" RODZAJ ZDARZENIA:\n " + printed_values[5], align="L", border=1)

    rep.ln(c_height)

    ybefore = rep.get_y()
    rep.multi_cell(0.33 * W, 1.2 * c_height, txt=" DOWODCA SEKCJI:\n " + printed_values[6], align="L", border=1)
    rep.set_xy(W * 0.33 + left_margin, ybefore)
    rep.multi_cell(0.33 * W, 1.2 * c_height, txt=" DOWODCA AKCJI:\n " + printed_values[7], align="L", border=1)
    rep.set_xy(W * 0.66 + left_margin, ybefore)
    rep.multi_cell(0.34 * W, 1.2 * c_height, txt=" KIEROWCA: \n " + printed_values[8], align="L", border=1)

    ybefore = rep.get_y()
    rep.multi_cell(0.33 * W, 2 * c_height, txt=" SPRAWCA:\n " + printed_values[9], align="L", border=1)
    rep.set_xy(left_margin, ybefore + 4 * c_height)
    rep.multi_cell(0.33 * W, 2 * c_height, txt=" POSZKODOWANY:\n " + printed_values[10], align="L", border=1)
    y_next = rep.get_y()
    rep.set_xy(W * 0.33 + left_margin, ybefore)

    rep.multi_cell(0.67 * W, 2 * c_height, txt=" SEKCJA:", align='L')
    y_now = rep.y
    c_h_height = c_height
    heroes = printed_values[11].split("\n", 10)
    len_sub_5 = min(len(heroes), 5)
    for h_index in range(len_sub_5):
        rep.set_xy(W * 0.33 + left_margin, y_now + c_h_height * h_index)
        rep.cell(0.33 * W, c_h_height, txt=" " + heroes[h_index].replace("\n", ", "), align='L')
    len_sub_rest = min(len(heroes) - 5, 5)
    for h_index in range(len_sub_rest):
        rep.set_xy(W * 0.66 + left_margin, y_now + c_h_height * h_index)
        rep.cell(0.33 * W, c_h_height, txt=" " + heroes[5 + h_index].replace("\n", ", "), align='L')

    rep.set_xy(W * 0.33 + left_margin, ybefore)
    rep.multi_cell(0.67 * W, 8 * c_height, txt='', align="L", border=1)
    rep.set_y(y_next)

    rep.ln(c_height)
    ybefore = rep.y
    rep.multi_cell(1 * W, 2 * c_height, txt="  SZCZEGOLY ZDARZENIA:", align='L')
    y_now = rep.y
    det = printed_values[12].replace('\n', ' ')
    det += "  " if len(det) is 0 else ""
    rows = [det[i:min(i + 90, len(det))] for i in range(0, len(det), 90)]
    for row in rows:
        rep.set_xy(left_margin, y_now + rows.index(row) * c_h_height)
        row = row[1:] if row[0] is " " else row
        rep.cell(1 * W, c_h_height, txt=" " + row + "-", align='L')
    rep.set_y(ybefore)
    rep.multi_cell(1 * W, 10 * c_height, border=1)

    rep.ln(c_height)

    ybefore = rep.get_y()
    rep.multi_cell(0.2 * W, 2 * c_height, txt=" DATA POWROTU:\n " + printed_values[13], align="L", border=1)
    rep.set_xy(W * 0.2 + left_margin, ybefore)
    rep.multi_cell(0.35 * W, 2 * c_height, txt=" GODZ. ZAKONCZ.:    " + printed_values[14], align="L", border=1)
    rep.set_xy(W * 0.2 + left_margin, ybefore + 2 * c_height)
    rep.multi_cell(0.35 * W, 2 * c_height, txt=" GODZ. W REMIZIE.:   " + printed_values[15], align="L", border=1)
    rep.set_xy(W * 0.55 + left_margin, ybefore)
    rep.multi_cell(0.2 * W, 2 * c_height, txt=" STAN LICZNIKA: \n " + printed_values[16], align="C", border=1)
    rep.set_xy(W * 0.75 + left_margin, ybefore)
    rep.multi_cell(0.25 * W, 2 * c_height, txt=" KM. DO MIEJSCA ZD: \n " + printed_values[17], align="C", border=1)

    modDate = str(printed_values[18])[11:].replace(":", "")
    path = pdf_save_path + "/" + str(report_no) + "_" + str(printed_values[4]) + "_" + str(
        printed_values[1]) + "_" + modDate + ".pdf"
    rep.output(path)
