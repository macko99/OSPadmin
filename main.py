import os

import PDFmaker as pdf
import database

db = database.DataBase("tmp.json")
pdf_save_path = "Raporty"
pdf_deleted_path = "Raporty/usuniete"


def intoPDF(uuid_num, path):
    dane = db.get_report(uuid_num)
    modDate = dane['modDate']
    id_number = dane['innerID']
    dep_date = dane['depDate']
    dep_time = dane['depTime']
    spot_time = dane['spotTime']
    location = dane['location']
    type_of_action = dane['type']
    section_com = dane['sectionCom']
    action_com = dane['actionCom']
    driver = dane['driver']
    perpetrator = dane['perpetrator']
    victim = dane['victim']
    section = dane['section']
    details = dane['details']
    return_date = dane['returnDate']
    end_time = dane['endTime']
    home_time = dane['homeTime']
    stan_licznika = dane['stanLicznika']
    km_location = dane['KM']
    tab = [id_number, dep_date, dep_time, spot_time, location, type_of_action, section_com, action_com, driver,
           perpetrator, victim, section, details,
           return_date, end_time, home_time, stan_licznika, km_location, modDate]

    pdf.makePDF(tab, path)


def delete_old_pdf(files, name):
    for item in files:
        if name in item:
            os.remove(pdf_save_path + "/" + item + ".pdf")


def main():
    reports = db.get_all_friendly()
    deleted = db.get_deleted()
    local_files = []
    local_files_modDate = []

    for file in os.listdir(pdf_save_path):
        if ".pdf" in file:
            local_files_modDate.append(file[:-4])
            local_files.append(file[:-10])

    for item in reports:
        if item not in deleted and "__" not in item:
            if item in local_files_modDate:
                continue
            elif item[:-6] in local_files:
                delete_old_pdf(local_files_modDate, item[:-6])
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path)
            else:
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path)

    for item in deleted:
        if item in local_files_modDate:
            os.replace(pdf_save_path + "/" + item + ".pdf", pdf_deleted_path + "/" + item + ".pdf")
        elif item[:-6] in local_files:
            delete_old_pdf(local_files_modDate, item[:-6])
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path)
        else:
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path)


if __name__ == "__main__":
    if not os.path.exists(pdf_save_path):
        os.makedirs(pdf_save_path)
    if not os.path.exists(pdf_deleted_path):
            os.makedirs(pdf_deleted_path)
    main()
    os.remove("tmp.json")
