import os
import sys
from pathlib import Path
import PDFmaker as pdf
import database
import tkinter as tk

pdf_save_path = "Raporty"
pdf_deleted_path = "Raporty/usuniete"
pdf_final_path = "Raporty/kompletne"

version = "1.0"


def intoPDF(uuid_num, path, db):
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
    truck_number = dane['truck']
    tab = [id_number, dep_date, dep_time, spot_time, location, type_of_action, section_com, action_com, driver,
           perpetrator, victim, section, details,
           return_date, end_time, home_time, stan_licznika, km_location, modDate, truck_number]

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


def generate_pdf(db):
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
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path, db)
            elif item[:-6] in local_ready_files:
                delete_old_pdf(local_ready_files_modDate, item[:-6], True)
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path, db)
            else:
                intoPDF(db.find_report(str(item).split("_")[0]), pdf_save_path, db)

    for item in deleted:
        if item in local_files_modDate:
            os.replace(pdf_save_path + "/" + item + ".pdf", pdf_deleted_path + "/" + item + ".pdf")
        elif item in local_ready_files_modDate:
            os.replace(pdf_final_path + "/" + item + ".pdf", pdf_deleted_path + "/" + item + ".pdf")
        elif item[:-6] in local_files:
            delete_old_pdf(local_files_modDate, item[:-6], False)
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path, db)
        elif item[:-6] in local_ready_files:
            delete_old_pdf(local_ready_files_modDate, item[:-6], True)
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path, db)
        else:
            intoPDF(db.find_report(str(item).split("_")[0]), pdf_deleted_path, db)


def init_gui():
    def popup_window(msg):
        popup = tk.Tk()
        popup.geometry("+350+250")
        popup.wm_title("Uwaga!")
        label = tk.Label(popup, text="Czy na pewno wyczyścić dane?", width=60, height=3)
        label.pack()
        spacing3 = tk.Label(popup, text="", width=60, height=0)
        # spacing4 = tk.Label(popup, text="", width=60, height=0)
        B1 = tk.Button(popup, text="Tak", command=lambda: [popup.destroy(), run(msg)])
        B1.pack()
        spacing2.pack()
        B2 = tk.Button(popup, text="Nie", command=popup.destroy)
        B2.pack()
        spacing3.pack()
        popup.mainloop()

    def handle_click(event):
        sys.exit()

    def run(event):
        greeting.destroy()
        opt1.destroy()
        button1.destroy()
        opt2.destroy()
        button2.destroy()
        opt3.destroy()
        button3.destroy()
        button4.destroy()
        rights.destroy()
        spacing.destroy()
        ver.destroy()
        spacing2.destroy()
        running = tk.Label(text="Porszę czekać...", width=60, height=10)
        running.pack()
        window.update()
        try:
            db = database.DataBase("tmp.json", "OSPadmin_dane/strażacy.txt", "OSPadmin_dane/hasło_mobilne.txt",
                                   "OSPadmin_dane/zastępy.txt", version)
            if event == 2:
                db.download_data()
                generate_pdf(db)
            elif event == 3:
                db.download_data()
                db.firebase_delete_all()
        except Exception as e:
            running.destroy()
            greeting2 = tk.Label(text="ERROR " + str(e), width=60, height=10)
            button5 = tk.Button(text="Zamknij!")
            button5.bind("<Button-1>", handle_click)
            greeting2.pack()
            button5.pack()
            if Path("tmp.json").is_file():
                os.remove("tmp.json")
        else:
            if Path("tmp.json").is_file():
                os.remove("tmp.json")
            running.destroy()
            greeting3 = tk.Label(text="GOTOWE", width=60, height=10)
            button6 = tk.Button(text="Zamknij!")
            button6.bind("<Button-1>", handle_click)
            greeting3.pack()
            button6.pack()

    window = tk.Tk()
    window.geometry("+300+200")
    window.wm_title("OSPadmin - generator PDF")

    greeting = tk.Label(text="Witamy! Program posiada kilka funkcji:", width=60, font=('bold'), height=3)
    opt1 = tk.Label(text="Aktualizuj dane w bazie danych (listy strażaków itp.)", width=60, height=3)
    opt2 = tk.Label(text="Generuj pliki PDF raportów w bazie danych", width=60, height=3)
    opt3 = tk.Label(text="Wyczyść raporty z bazy danych", width=60, height=3)
    rights = tk.Label(text="Maciej Kozub, Tomasz Zachwieja", width=60, height=0, fg="gray")
    ver = tk.Label(text="AGH 2020, Version: " + version, width=60, height=0, fg="gray")
    spacing = tk.Label(text="", width=60, height=2)
    spacing2 = tk.Label(text="", width=60, height=2)

    button1 = tk.Button(text="Wyślij!", command=lambda: run(1))
    button2 = tk.Button(text="Generuj!", command=lambda: run(2))
    button3 = tk.Button(text="Czyść!", command=lambda: popup_window(3))
    button4 = tk.Button(text="Zamknij")

    button4.bind("<Button-1>", handle_click)

    greeting.pack()
    opt2.pack()
    button2.pack()
    opt1.pack()
    button1.pack()
    opt3.pack()
    button3.pack()
    spacing.pack()
    button4.pack()
    spacing2.pack()
    rights.pack()
    ver.pack()
    window.mainloop()


if __name__ == "__main__":
    if not os.path.exists(pdf_save_path):
        os.makedirs(pdf_save_path)
    if not os.path.exists(pdf_deleted_path):
        os.makedirs(pdf_deleted_path)
    if not os.path.exists(pdf_final_path):
        os.makedirs(pdf_final_path)
    init_gui()