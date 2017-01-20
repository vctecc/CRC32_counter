"""
Необходимо запилить выбор каталога, сравнение старого файла и нового, отображение несоответсвтия,
генерацию xml файла.
"""
from tkinter import Button, Tk, Frame, Label, messagebox, filedialog, Entry
from crc32counter import crc32_function
import os


def compare(first_name, second_name):   # необходимо перенести эту функцию отсюда
    """Сравнение двух файлов и вовод различий на экран"""

    first = open(first_name, 'rb')
    second = open(second_name, 'rb')

    while True:
        data_f = first.read(1)
        data_s = second.read(1)

        if (not data_f) and (not data_s):
            break
        elif (not data_f) and (not data_s):
            first.close()
            second.close()
            return False
        # TODO необходимо добавить заипсь различающихся данных в файл
        if data_f != data_s:
            first.close()
            second.close()
            return False

    first.close()
    second.close()
    return True


class Terminal(Tk):
    """

    """
    def __init__(self):
        self.path = ''
        self.root = Tk()
        self.root.title("CRC32 counter")
        self.ignore = ('crc32', 'temp',)
        self.make_ask_dir(self.root)
        self.make_choice_panel(self.root)

        self.root.mainloop()

    def make_choice_panel(self, master):
        self.choice_panel = Frame(master)
        self.choice_panel.pack(side='top')
        Label(self.choice_panel, text='Тип проверки').pack(side='top')

        button_panel = Frame(self.choice_panel)
        button_panel.pack()
        but_1 = Button(button_panel, text='Первичная првоверка',
                       command=lambda: self.initial_verification(self.path))
        but_1.grid(row=0, column=0)
        but_2 = Button(button_panel, text='Вторичная првоверка',
                       command=lambda: self.secondary_verification(self.path, self.ignore))
        but_2.grid(row=0, column=1)

    def initial_verification(self, path):
        crc32_function(path, 'crc32')

    def secondary_verification(sels, path, ignore):
        """
        Поиск файла с контрольными суммами, вычисление контрольной суммы для всех файлов указанного каталога,
        запись результатов во временный фаил, сравнение (при наличии) с результатми предыдущей проверки.
        При обноружении несоответствий происходит создание файла несоответствий.

        """
        crc32_function(path, 'temp', ignore)
        answer = compare('crc32', 'temp')
        if not answer:
            messagebox.showwarning('Bad!', 'Контрольные суммы не совпадают')
        elif answer == 'error':
            messagebox.showerror('Error!', 'Произошла ошибка')
        else:
            messagebox.showinfo('Good!', 'Контрольные суммы совпадают')

        # os.remove('temp')   # TODO необходимо передавать полный путь до файла

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

if __name__ == '__main__':
    window = Terminal()
