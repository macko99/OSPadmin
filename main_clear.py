import sys
import os
import database_clear
import tkinter as tk


def init_gui():
    def handle_click(event):
        sys.exit()

    def run(event):
        greeting.destroy()
        button.destroy()
        button2.destroy()
        running = tk.Label(text="Porszę czekać...", width=60, height=10)
        running.pack()
        window.update()
        try:
            db = database_clear.DataBase("tmp.json")
            db.firebase_delete_all()
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
    window.wm_title("OSPadmin - czyszczenie")

    greeting = tk.Label(text="Wyczyścić bazę danych?", width=60, height=10)
    button = tk.Button(text="TAK")
    button.bind("<Button-1>", run)
    button2 = tk.Button(text="NIE")
    button2.bind("<Button-1>", handle_click)

    greeting.pack()
    button.pack()
    button2.pack()
    window.mainloop()


if __name__ == "__main__":
    init_gui()