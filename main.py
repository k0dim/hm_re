import re
import csv
import os
import tkinter as tk
from tkinter import messagebox as mb

HM_RE_DIRECTORY = os.getcwd()
# in
CSV_IN = 'csv_files_in'
FILE_IN = 'phonebook_raw.csv'
FULL_PATH_IN = os.path.join(HM_RE_DIRECTORY, CSV_IN, FILE_IN)
# out
CSV_OUT = 'csv_files_out'
FILE_OUT = 'phonebook.csv'
FULL_PATH_OUT = os.path.join(HM_RE_DIRECTORY, CSV_OUT, FILE_OUT)

new_list = []

with open(FULL_PATH_IN, encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    

def create_fio():
    all_list = [contacts_list[0]]
    for col in contacts_list[1:]:
        fio = (col[0] + col[1] + col[2])
        pattern_1 = r'([А-Я])'
        repl_1 = r' \1'
        fio_new = (re.sub(pattern_1, repl_1, fio)).split()
        if len(fio_new) == 2:
            fio_new.append('')
        elif len(fio_new) == 1:
            fio_new.append('')
            fio_new.append('')
        for element in col[3:]:
            fio_new.append(element)
        pattern_2 = re.compile(
            r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
        phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'
        fio_new[5] = pattern_2.sub(phone_substitution, fio_new[5])
        all_list.append(fio_new)
    return all_list


def duplicates_combining(all_list):
    total = 0
    for line in all_list[1:]:
        first_name = line[0]
        last_name = line[1]
        total += 1
        for contact in all_list:
            new_first_name = contact[0]
            new_last_name = contact[1]
            if first_name == new_first_name and last_name == new_last_name:
                if line[2] == '':
                    line[2] = contact[2]
                if line[3] == '':
                    line[3] = contact[3]
                if line[4] == '':
                    line[4] = contact[4]
                if line[5] == '':
                    line[5] = contact[5]
                if line[6] == '':
                    line[6] = contact[6]

    for contact in all_list:
        if contact not in new_list:
            new_list.append(contact)

class Window_start(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Регулярные выражения")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('330x150+{}+{}'.format(w//2, h//2))
        self.lebel = tk.Label(self, text = "Положите, пожалуйста, файл в 'csv_files_out'")
        self.lebel.grid(column=0, row=0)
        self.lebel = tk.Label(self, text = "Для выполнения программы нажмите OK")
        self.lebel.grid(column=0, row=1)
        self.but = tk.Button(self, text="OK", command=self.clicke)
        self.but.grid(column=0, row=2)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

    def confirm_delete(self):
            message = "Вы уверены, что хотите закрыть это окно?"
            if mb.askyesno(message=message, parent=self):
                self.destroy()

    
    def clicke(self):
        try:
            all_list = create_fio()
            duplicates_combining(all_list)
            mb.showinfo('Выполненно', 'Успешно!')
        except:
            mb.showerror('Ошибка', 'Упс..Ошибочка вышла')

        with open(FULL_PATH_OUT, "w", encoding='utf-8') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(new_list)

if __name__ == '__main__':
    win = Window_start()
    win.mainloop()
