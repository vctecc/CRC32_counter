"""
GUI приложение для подсчета контрольной суммы по алгоритму CRC32.
При первичной проверке выполняется индексация файлов иказанного каталога.
В каталоге со скриптом создается папка со списком проидесированнх файлов и их контрольной суммой.
При вторичной проверке выполяется повторная индексация выбранного каталога и сравнение полученных
данных с первой проверкой, обнаруженные несовпадения выводятся в фаил error
"""
from tkinter import Button, Tk, Frame, Label, messagebox, filedialog, Entry
from crc32counter import crc32_function
import os


class Terminal(Tk):
    """
    Этот класс стоит переработать. Отдельно написать GUI, отдельно написать все остальное.
    """
    def __init__(self):

        self.FIRST_FILE = 'crc32'
        self.TEMP_FILE = 'temp'
        self.ERR_FILE = 'error'

        self.path = ''
        self.root = Tk()
        self.root.title("CRC32 counter")
        self.ignore = (self.FIRST_FILE, self.TEMP_FILE, self.ERR_FILE)
        self.make_ask_dir(self.root)
        self.make_choice_panel(self.root)

        self.root.mainloop()

    def make_choice_panel(self, master):
        self.choice_panel = Frame(master)
        self.choice_panel.pack(side='top')

        Label(self.choice_panel, text='Тип проверки').pack(side='top')

        button_panel = Frame(self.choice_panel)
        button_panel.pack()

        but_1 = Button(button_panel, text='Первичная проверка',
                       command=lambda: self.primary_verification(self.path, self.FIRST_FILE))
        but_1.grid(row=0, column=0)

        but_2 = Button(button_panel, text='Вторичная проверка',
                       command=lambda: self.secondary_verification(self.path, self.TEMP_FILE, self.ignore))
        but_2.grid(row=0, column=1)

    def make_ask_dir(self, master):
        """

        :param master:
        :return:
        """
        ask_dir_frame = Frame(master)
        ask_dir_frame.pack()

        self.path_entry = Entry(ask_dir_frame)
        self.path_entry.pack(side='left')
        Button(ask_dir_frame, text='Выбор директории', command=lambda: self.ask_dir()).pack(side='right')

    def ask_dir(self):
        self.path = filedialog.askdirectory()
        self.path_entry.delete(0, 100)  # с этим нужно что-то сделать, так оставлять не правильно
        self.path_entry.insert(0, self.path)
        print(self.path)

    def primary_verification(self, path, outfile):

        if self.path:
            crc32_function(path, outfile)
            messagebox.showinfo('Good!', 'Контрольная сумма посчитана')
        else:
            messagebox.showwarning('Error!', 'Не указан путь')

    def secondary_verification(self, path, outfile,  ignore):
        """
        Поиск файла с контрольными суммами, вычисление контрольной суммы для всех файлов указанного каталога,
        запись результатов во временный фаил, сравнение (при наличии) с результатми предыдущей проверки.
        При обноружении несоответствий происходит создание файла несоответствий.
        """
        crc32_function(path, outfile, ignore)

        answer = self.compare(self.FIRST_FILE, 'temp')
        if not answer:
            messagebox.showwarning('Bad!', 'Контрольные суммы не совпадают')
        elif answer == 'error':
            messagebox.showerror('Error!', 'Произошла ошибка')
        else:
            messagebox.showinfo('Good!', 'Контрольные суммы совпадают')

        # os.remove('temp')   # TODO необходимо передавать полный путь до файла

    @staticmethod
    def compare(first_name, second_name):   # необходимо перенести эту функцию отсюда
        """Сравнение двух файлов и вовод различий на экран"""

        first = open(first_name, 'rb')
        second = open(second_name, 'rb')
        error = open('error', 'wb')

        while True:
            data_f = first.readline()
            data_s = second.readline()

            if (not data_f) and (not data_s):
                answer = True
                break

            elif not data_f:
                answer = False
                for line in second:
                    error.write(line)
                break

            elif not data_s:
                answer = False
                for line in first:
                    error.write(line)
                break

            if len(data_f) != len(data_s):
                error.write(data_s)
            else:
                for symbol in range(len(data_f)):
                    if data_f[symbol] != data_s[symbol]:
                        error.write(data_s)
                        break

        first.close()
        second.close()
        error.close()

        os.remove(second_name)

        if os.path.getsize('error') == 0:
            os.remove('error')
        else:
            answer = False

        return answer

if __name__ == '__main__':
    window = Terminal()
