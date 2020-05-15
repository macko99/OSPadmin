import os
import sys
import PDFmaker as pdf
import database
import tkinter as tk

db = database.DataBase("tmp.json", "OSPadmin_dane/strażacy.txt", "OSPadmin_dane/hasło_mobilne.txt")
pdf_save_path = "Raporty"
pdf_deleted_path = "Raporty/usuniete"
pdf_final_path = "Raporty/kompletne"

delete = False


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

    if path == pdf_deleted_path:
        pdf.makePDF(tab, path)
    elif dane['ready'] == "Tak":
        pdf.makePDF(tab, pdf_final_path)
    else:
        pdf.makePDF(tab, path)


def delete_old_pdf(files, name, ready):
    for item in files:
        if name in item:
            if ready:
                os.remove(pdf_final_path + "/" + item + ".pdf")
            else:
                os.remove(pdf_save_path + "/" + item + ".pdf")


def main():
    reports, completed = db.get_all_friendly()
    deleted = db.get_deleted()
    local_files = []
    local_files_modDate = []
    local_ready_files = []
    local_ready_files_modDate = []

    for file in os.listdir(pdf_save_path):
        if ".pdf" in file:
            local_files_modDate.append(file[:-4])
            local_files.append(file[:-10])

    for file in os.listdir(pdf_final_path):
        if ".pdf" in file:
            local_ready_files_modDate.append(file[:-4])
            local_ready_files.append(file[:-10])

    for item in reports:
        if item not in deleted and "__" not in item:
            if item in local_files_modDate or item in local_ready_files_modDate:
                continue
            elif item[:-6] in local_files:
                delete_old_pdf(local_files_modDate, item[:-6], False)
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path)
            elif item[:-6] in local_ready_files:
                delete_old_pdf(local_ready_files_modDate, item[:-6], True)
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path)
            else:
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path)

    for item in deleted:
        if item in local_files_modDate:
            os.replace(pdf_save_path + "/" + item + ".pdf", pdf_deleted_path + "/" + item + ".pdf")
        elif item in local_ready_files_modDate:
            os.replace(pdf_final_path + "/" + item + ".pdf", pdf_deleted_path + "/" + item + ".pdf")
        elif item[:-6] in local_files:
            delete_old_pdf(local_files_modDate, item[:-6], False)
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path)
        elif item[:-6] in local_ready_files:
            delete_old_pdf(local_ready_files_modDate, item[:-6], True)
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path)
        else:
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path)

    global delete
    if delete:
        db.firebase_delete_all()


def init_gui():
    def handle_click(event):
        sys.exit()

    def handle_click_yes(event):
        global delete
        delete = True
        run(event)

    def run(event):
        greeting.destroy()
        button.destroy()
        button2.destroy()
        running = tk.Label(text="Porszę czekać...", width=60, height=10)
        running.pack()
        window.update()
        try:
            main()
        except Exception as e:
            os.remove("tmp.json")
            running.destroy()
            greeting2 = tk.Label(text="ERROR " + str(e), width=60, height=10)
            button3 = tk.Button(text="Zamknij!")
            button3.bind("<Button-1>", handle_click)
            greeting2.pack()
            button3.pack()
        else:
            os.remove("tmp.json")
            running.destroy()
            greeting2 = tk.Label(text="GOTOWE", width=60, height=10)
            button3 = tk.Button(text="Zamknij!")
            button3.bind("<Button-1>", handle_click)
            greeting2.pack()
            button3.pack()

    window = tk.Tk()
    window.wm_title("OSPadmin")
    # window.iconbitmap("OSPadmin_dane/logo.ico")

    greeting = tk.Label(text="Wyczyścić bazę danych po pobraniu raportów?", width=60, height=10)
    button = tk.Button(text="TAK")
    button.bind("<Button-1>", handle_click_yes)
    button2 = tk.Button(text="NIE")
    button2.bind("<Button-1>", run)

    greeting.pack()
    button.pack()
    button2.pack()
    window.mainloop()


if __name__ == "__main__":
    if not os.path.exists(pdf_save_path):
        os.makedirs(pdf_save_path)
    if not os.path.exists(pdf_deleted_path):
        os.makedirs(pdf_deleted_path)
    if not os.path.exists(pdf_final_path):
        os.makedirs(pdf_final_path)
    init_gui()