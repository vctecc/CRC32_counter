"""
Необходимо запилить выбор каталога, сравнение старого файла и нового, отображение несоответсвтия,
генерацию xml файла.
"""
from tkinter import Button, Tk, Frame, Label, messagebox, filedialog
from crc32counter import crc32_function


def compare(first_name, second_name):
    """

    """

    first = open(first_name, 'rb')
    second = open(second_name, 'rb')

    while True:
        data_f = first.read(1)
        data_s = second.read(1)
        print('F1', data_f)
        print('F2', data_s)

        if (not data_f) and (not data_s):
            break
        elif (not data_f) and (not data_s):
            first.close()
            second.close()
            return False

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
        Button(self.root, text='Выбор директории', command=lambda: self.ask_dir()).pack()
        print(self.path)
        self.make_choice_panel(self.root)


        self.root.mainloop()

    def make_choice_panel(self, master):
        """

        """
        self.choice_panel = Frame(master)
        self.choice_panel.pack(side='top')
        Label(self.choice_panel, text='Тип проверки').pack(side='top')

        self.button_panel = Frame(self.choice_panel)
        self.button_panel.pack()
        but_1 = Button(self.button_panel, text='Первичная првоверка',
                       command=lambda: self.initial_verification(self.path))
        but_1.grid(row=0, column=0)
        but_2 = Button(self.button_panel, text='Вторичная првоверка',
                       command=lambda: self.secondary_verification(self.path))
        but_2.grid(row=0, column=1)


    def initial_verification(self, path):
        """
        Вычисление контрольной для всех файлов указанного каталога и запись результатов в фаил.

        """
        crc32_function(path, 'crc32')

    def secondary_verification(sels, path):
        """
        Поиск файла с контрольными суммами, вычисление контрольной суммы для всех файлов указанного каталога,
        запись результатов во временный фаил, сравнение (при наличии) с результатми предыдущей проверки.
        При обноружении несоответствий происходит создание файла несоответствий.

        """
        crc32_function(path, 'temp')
        answer = compare('crc32', 'temp')
        if not answer:
            messagebox.showwarning('Bad!', 'Контрольные суммы не совпадают')
        elif answer == 'error':
            messagebox.showerror('Error!', 'Произошла ошибка')
        else:
            messagebox.showinfo('Good!', 'Контрольные суммы совпадают')

    def ask_dir(self):
         self.path = filedialog.askdirectory()

if __name__ == '__main__':
    window = Terminal()
