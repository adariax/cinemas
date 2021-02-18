import sys
import sqlite3
import csv
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem, QCompleter
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QDateTime, QDate, QTime
from PyQt5.Qt import Qt

from ui_main import Ui_MainWindow
from ui_reg import Ui_Dialog_R
from ui_ent import Ui_Dialog_L
from ui_card import Ui_Form_P
from ui_sess import Ui_Dialog_S
from ui_cin import Ui_Dialog_C
from ui_addfilm import Ui_Dialog_AF
from ui_halls import Ui_Dialog_H
from ui_info import Ui_Form

# for showing hall map
HALL_MINI = [[0, 0, 1, 1, 1, 1, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 1, 1]]

HALL_MIDI = [[0, 0, 1, 1, 1, 1, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 0]]

HALL_MAXI = [[0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

HALL_ELITE = [[0, 0, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 0],
              [1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1, 0]]

TYPES = ('Малый', 'Средний', 'Большой', 'Elite')

# for session info
MONTHS_FOR_SESSIONS = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
                       5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
                       9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}


class Session:
    def __init__(self, id, time, date, film_id, cinema_id, hall_name, price):
        self.id = id
        self.time = QTime(int(time.split(':')[0]), int(time.split(':')[1]))
        date = date.split('-')
        self.date = QDate(int(date[0]), int(date[1]), int(date[2]))
        self.film_id = film_id
        self.cinema_id = cinema_id
        self.hall = hall_name
        self.price = price

        self.create_csv(self.get_hall_map())  # load hall map

    def __str__(self):
        info = self.get_info()
        return f'{info[0]}, {info[1]} {info[2]} {info[3]} руб.\n' \
            f'Кинотеатр {info[4]}, зал {info[5]}'

    def get_info(self):
        time = str(self.time.toPyTime().isoformat()[:5])  # only hours and minutes
        date = ' '.join(map(str, [self.date.day(), MONTHS_FOR_SESSIONS[self.date.month()],
                                  self.date.year()]))

        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        film = cur.execute(f'SELECT title FROM Films WHERE id = {self.film_id}').fetchone()
        film = film[0]
        cinema = cur.execute(f'SELECT name FROM cinemas WHERE id = {self.cinema_id}').fetchone()
        cinema = cinema[0]
        con.close()

        return (time, date, film, str(self.price), cinema, self.hall)  # str values to output

    def to_list(self):  # return info about session to show it tu user/admin
        info = self.get_info()
        return f'{info[0]}, {info[1]} {info[2]}\nцена: {info[3]} руб.'

    def delete(self):  # delete from DataBase all info about session
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        cur.execute(f'DELETE FROM sessions WHERE id = {self.id}').fetchone()
        con.commit()
        con.close()

        os.remove(f'{self.get_csv_name()}')

    def get_hall_map(self):  # return one of 4 halls' types
        with open(self.get_csv_name(), encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            hall_map = []
            for row in reader:
                row_h = []
                for elem in row:
                    row_h.append(int(elem))
                hall_map.append(row_h)
        return hall_map

    def get_csv_name(self):  # return name of csv file
        return f'{self.cinema_id}_{self.price}_{self.hall}.csv'

    def create_csv(self, places):  # create file with information about bought ticket
        with open(self.get_csv_name(), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(places)


class Hall(QDialog, Ui_Dialog_H):
    def __init__(self, is_admin, func, obj):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.halls_type.currentTextChanged.connect(self.load_map)
        self.add_hall_btn.clicked.connect(self.func_choice)

        self.window = None
        self.admin_mode = is_admin
        self.cinema_or_sess = obj  # cinema name or session obj
        self.sql_req = func
        self.table.selectedItem = []

        if not self.admin_mode:  # change mode
            self.add_hall_btn.setText('Купить билет')
            self.info.setText(self.cinema_or_sess.get_info()[2])
            self.info.setEnabled(False)
            self.halls_type.setDisabled(not False)
            self.load_table(self.cinema_or_sess.get_hall_map())

        self.load_types()

    def buy_ticket(self):
        place = self.table.selectedIndexes()
        if len(place) == 1:  # user must choose ONE place
            index = (place[0].row(), place[0].column())
            if self.table.item(*index).background().color() == QColor(70, 70, 70):
                self.window = Payment(self.cinema_or_sess, index, self.table.item(*index).text())
                self.window.exec()
                if self.window.finished:
                    self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Это место выбрать нельзя')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберете одно место')

    def func_choice(self):  # start different functions for buying ticket or adding hall
        self.add_hall() if self.admin_mode else self.buy_ticket()

    def resizeEvent(self, QResizeEvent):  # makes resize when window size has changed
        self.change_size()

    def change_size(self):  # resize table columns and rows
        x, y = self.table.width(), self.table.height()
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, (x - 25) // self.table.columnCount())
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, (y - 30) // self.table.rowCount())

    def load_table(self, hall_type):  # create table for hall_type
        self.table.setColumnCount(len(hall_type[0]))
        headers = ('\t' for _ in range(len(hall_type[0])))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)
        for i, row in enumerate(hall_type):
            self.table.setRowCount(self.table.rowCount() + 1)
            n = 1  # for showing number of seat
            for j, el in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(n) if el != 0 else ''))
                if el == 0:
                    self.table.item(i, j).setBackground(QColor(140, 140, 140))
                elif el == 1:
                    n += 1
                    self.table.item(i, j).setBackground(QColor(70, 70, 70))
                elif el == 2:
                    n += 1
                    self.table.item(i, j).setBackground(QColor(200, 20, 70))
        self.change_size()

    def load_map(self):  # load hall map of chosen type
        selected_ind = self.halls_type.currentIndex()
        if selected_ind == 1:
            self.load_table(HALL_MINI)
        elif selected_ind == 2:
            self.load_table(HALL_MIDI)
        elif selected_ind == 3:
            self.load_table(HALL_MAXI)
        elif selected_ind == 4:
            self.load_table(HALL_ELITE)

    def load_types(self):  # add types of halls to combobox
        self.halls_type.addItem('')
        for i in TYPES:
            self.halls_type.addItem(i)

    def add_hall(self):  # add hall to draft table
        name, type_h = self.info.text(), self.halls_type.currentIndex()
        if name and type_h:
            con = sqlite3.connect('film_library.db')
            cur = con.cursor()
            if name not in map(lambda x: x[0], cur.execute(f'''SELECT name 
                           FROM halls_{self.cinema_or_sess}''').fetchall()):
                self.sql_req(f'''INSERT INTO halls_{self.cinema_or_sess} 
                VALUES ({type_h}, "{name}")''')

                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Зал с таким именем существует')
            con.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')


class Information(QWidget, Ui_Form):  # window to show information for admin/user
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))


class AddCinema(QDialog, Ui_Dialog_C):
    def __init__(self, is_admin):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.admin_mod = is_admin
        self.window = None

        self.h_name = 'new_cinema_need_to_change_title'
        self.sql_req(f'''DROP TABLE if exists halls_{self.h_name}''')  # clean draft table

        self.one_hall = True
        self.titles = []

        self.load_completer()

        # load connection events

        self.add_hall_btn.clicked.connect(self.add_hall)
        self.del_hall_btn.clicked.connect(self.del_hall)
        self.add_cin_btn.clicked.connect(self.add_cin)
        self.del_cin_btn.clicked.connect(self.del_cin)

    def add_cin(self):  # add cinema's info to DataBase and create correct table for halls
        title, address = self.name.text(), self.adrs.text()
        if title and address and self.halls.count() != 0:
            con = sqlite3.connect('film_library.db')
            cur = con.cursor()
            if title not in map(lambda x: x[0], cur.execute('SELECT name FROM cinemas').fetchall()):
                # get all halls' info to rewrite it in table with correct name
                halls_for_cinema = cur.execute(f'''SELECT * FROM halls_{self.h_name}''').fetchall()

                # get cinema's id
                id_cin = max(map(lambda x: x[0],
                                 cur.execute('''SELECT id FROM cinemas''').fetchall())) + 1
                con.close()

                self.sql_req(f'''DROP TABLE halls_{self.h_name}''')  # delete draft halls table

                self.sql_req(f'''CREATE TABLE halls_{title} (
                                type  NOT NULL,
                                name  NOT NULL
                                );''')  # create new table for halls info with correct name

                for hall in halls_for_cinema:
                    self.sql_req(f'''INSERT INTO halls_{title} VALUES {hall}''')  # load halls info

                self.sql_req(f'''INSERT INTO cinemas VALUES 
                ({id_cin}, "{title}", "{address}", "halls_{title}")''')  # add cinema's info

                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Кинотеатр с таким названием существует')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')

    def del_cin(self):  # delete existed cinema and its halls from DataBase
        name = self.name.text()
        if name in self.titles:
            self.sql_req(f'''DROP TABLE halls_{name}''')
            self.sql_req(f'''DELETE FROM cinemas WHERE name = "{name}"''')

            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка удаления', 'Такого кинотеатра не существует')

    def add_hall(self):  # create table in data base to write info about halls
        if self.one_hall:
            self.sql_req(f'''CREATE TABLE halls_{self.h_name} (
                type  NOT NULL,
                name  NOT NULL
                );''')
        self.window = Hall(self.admin_mod, self.sql_req, self.h_name)
        self.window.exec()
        self.one_hall = False
        if self.window.finished:
            self.load_halls()

    def del_hall(self):  # delete chosen in combobox hall of new cinema
        self.sql_req(f'''DELETE FROM halls_{self.h_name} 
        WHERE name = "{self.halls.currentText()}"''')

        self.load_halls()

    def load_halls(self):  # load titles (names) of existing halls for new cinema
        self.halls.clear()

        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        halls = cur.execute(f'''SELECT name FROM halls_{self.h_name}''').fetchall()
        con.close()
        for el in halls:
            self.halls.addItem(el[0])

    def load_completer(self):  # load completer of existing cinemas
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        self.titles = list(map(lambda x: x[0],
                               cur.execute('''SELECT name FROM cinemas''').fetchall()))
        con.close()

        completer = QCompleter(self.titles, self.name)
        self.name.setCompleter(completer)

    def sql_req(self, req):  # changes DataBate but DON'T return list for request "SELECT ..."
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        cur.execute(req)
        con.commit()
        con.close()


class AddFilm(QDialog, Ui_Dialog_AF):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.btn.clicked.connect(self.add_film)

        self.load_cb()

    def load_cb(self):  # load genres ri combobox
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        genres = cur.execute('''SELECT DISTINCT title FROM genres''').fetchall()
        con.close()

        genres = list(map(lambda x: str(x[0]), genres))

        self.genre.addItem('')
        for i in sorted(genres):
            self.genre.addItem(i)

    def add_film(self):  # insert info about film into DataBase
        title = self.title.text()
        year = self.year.text()
        genre = self.genre.currentText()
        dur = self.dur.text()

        if title == '' or year == '' or genre == '' or dur == '':
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        elif not year.isdigit() or not dur.isdigit():
            QMessageBox.warning(self, 'Ошибка', 'Неверное заполнение')
        else:
            con = sqlite3.connect('film_library.db')
            cur = con.cursor()
            genre = cur.execute(f'SELECT id FROM genres WHERE title = "{genre}"').fetchone()[0]
            cur.execute(f'''INSERT INTO Films VALUES 
            ({cur.execute("""SELECT id FROM Films""").fetchall()[-1][0] + 1}, 
            "{title}", {year}, {genre}, {dur})''')
            con.commit()
            con.close()

            self.close()


class AddSession(QDialog, Ui_Dialog_S):  # ДОПИСАТЬ ДОБАВЛЕНИЕ В ФАЙЛ
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.load_cb()

        # load clicked events

        self.add_sess.clicked.connect(self.add_and_close)
        self.serch_btn.clicked.connect(self.search)
        self.table.cellClicked.connect(self.row_focus)
        self.add_film_btn.clicked.connect(self.add_film)
        self.cinema_cb.currentIndexChanged.connect(self.load_halls)

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.not_one_con = False
        self.user_choice = None
        self.sql_req = None

    def add_film(self):  # add film to DataBase
        self.win = AddFilm()
        self.win.exec()
        if self.win.finished:
            films = self.db_req('SELECT * FROM Films')
            self.add_to_table(films)

    def row_focus(self):  # select all column of chosen film
        for i in range(4):
            self.table.item(self.table.currentRow(), i).setSelected(True)

    def load_cb(self):  # load info to ComboBox about cinemas, film's years and genres
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        years = list(map(lambda x: str(x[0]),
                         cur.execute('''SELECT DISTINCT year FROM Films''').fetchall()))
        genres = list(map(lambda x: str(x[0]),
                          cur.execute('''SELECT DISTINCT title FROM genres''').fetchall()))
        cinemas = list(map(lambda x: str(x[0]),
                           cur.execute('''SELECT name FROM cinemas''').fetchall()))

        con.close()

        self.year_cb.addItem('')
        self.genre_cb.addItem('')
        self.cinema_cb.addItem('')
        for i in sorted(years):
            self.year_cb.addItem(i)
        for i in sorted(genres):
            self.genre_cb.addItem(i)
        for i in sorted(cinemas):
            self.cinema_cb.addItem(i)

    def load_halls(self):  # load info to ComboBox about halls of chosen cinemas
        self.hall_cb.clear()

        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        hall = cur.execute(f'''SELECT name 
        FROM {cur.execute(f"""SELECT halls FROM cinemas 
        WHERE name = '{self.cinema_cb.currentText()}'""").fetchall()[0][0]}''').fetchall()
        con.close()

        hall = list(map(lambda x: str(x[0]), hall))

        self.hall_cb.addItem('')
        for i in sorted(hall):
            self.hall_cb.addItem(i)

    def check(self, req):  # check if sql requests or requests from lineedit/combobox are empty
        return True if req[0] == req[1] == req[2] == req[3] == '' else False

    def search(self):
        self.not_one_con = False

        self.sql_req = (self.year_sql.text(), self.title_sql.text(),
                        self.dur_sql.text(), self.genre_sql.text())
        self.user_choice = (self.year_cb.currentText(), self.title_le.text(),
                            self.dur_le.text(), self.genre_cb.currentText())
        if self.check(self.sql_req) and self.check(self.user_choice):
            films = self.db_req('SELECT * FROM Films')
        else:
            films = self.db_req('SELECT * FROM Films WHERE' + self.combo_search())

        self.add_to_table(films)

    def combo_search(self):  # sql requests and requests from lineedit/combobox join with 'AND'
        return self.sql_search() + self.easy_user_search()

    def easy_user_search(self):
        req = ''
        if self.user_choice[0]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' year = ' + self.user_choice[0]
            self.not_one_con = True
        if self.user_choice[1]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' title = "' + self.user_choice[1] + '"'
            self.not_one_con = True
        if self.user_choice[2]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' duration = ' + self.user_choice[2]
            self.not_one_con = True
        if self.user_choice[3]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' genre IN ' + f'(SELECT id FROM genres ' \
                f'WHERE title = "{self.user_choice[3]}")'
        return req

    def sql_search(self):
        req = ''
        if self.sql_req[0]:
            req = req + ' year ' + self.sql_req[0]
            self.not_one_con = True
        if self.sql_req[1]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' title ' + self.sql_req[1]
            self.not_one_con = True
        if self.sql_req[2]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' duration ' + self.sql_req[2]
            self.not_one_con = True
        if self.sql_req[3]:
            req += ' AND' if self.not_one_con else ''
            req = req + ' genre IN ' + f'(SELECT id FROM genres WHERE title {self.sql_req[3]})'
            self.not_one_con = True
        return req

    def db_req(self, req):  # makes db request and return list of films
        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        films = cur.execute(req).fetchall()
        films = list(map(lambda x: (x[1], x[2], cur.execute(f'''SELECT title FROM 
                            genres WHERE id={x[3]}''').fetchone()[0], x[4] if x[4] else '-'),
                         films))
        con.close()
        return films

    def add_to_table(self, res):  # load/reload table with found films by search
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Название', 'Год', 'Жанр', 'Длительность, мин'))
        self.table.setRowCount(0)
        for i, row in enumerate(res):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, el in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(el)))
        self.table.resizeColumnsToContents()

    def add_and_close(self):  # add session to file if all fields is not empty
        cinema = self.cinema_cb.currentText()
        hall = self.hall_cb.currentText()
        price = self.price_le.text()
        data, time = self.dateTimeEdit.date().toPyDate().isoformat(), \
                     str(self.dateTimeEdit.time().toPyTime().isoformat())[:8]
        if cinema and hall:
            if price.isdigit():
                if self.table.selectedItems():
                    film_title = self.table.selectedItems()[0].text()

                    con = sqlite3.connect('film_library.db')
                    cur = con.cursor()
                    id_s = cur.execute('''SELECT id FROM sessions''').fetchall()[-1][0] + 1 \
                        if cur.execute('''SELECT id FROM sessions''').fetchall() else 1
                    cinema_id = cur.execute(f"""SELECT id FROM cinemas 
                                        WHERE name = '{cinema}'""").fetchall()[0][0]

                    hall_type = cur.execute(f'SELECT type FROM halls_{cinema} '
                                            f'WHERE name = "{hall}"').fetchone()[0]
                    # chose hall map
                    if hall_type == 1:
                        type_h = HALL_MINI
                    elif hall_type == 2:
                        type_h = HALL_MIDI
                    elif hall_type == 3:
                        type_h = HALL_MAXI
                    elif hall_type == 4:
                        type_h = HALL_ELITE
                    with open(f'{cinema_id}_{price}_{hall}.csv',
                              'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f, delimiter=';')
                        writer.writerows(type_h)  # create clean hall map for session

                    cur.execute(f'''INSERT INTO sessions VALUES 
                    ({id_s}, "{time}", "{data}", 
                    {cur.execute(f"""SELECT id FROM Films WHERE title = "{film_title}" 
                    AND year={self.table.selectedItems()[1].text()}""").fetchall()[0][0]},
                    {cinema_id}, "{hall}", {price})''')

                    con.commit()
                    con.close()

                    self.close()
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Не выбран фильм')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный формат ввода стоимости билета')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все данные')


class Payment(QDialog, Ui_Form_P):
    def __init__(self, obj, index, seat):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        for i in range(1, 6):  # makes change focus on next LineEdit possible
            eval(f'self.part{i}.textChanged.connect(self.change)')
        self.buy.clicked.connect(self.get_ticket)

        self.part = 1  # for change focus
        self.check = ''  # for check correct card enter
        self.sess = obj
        self.index = index
        self.seat = seat

    def change(self):  # set focus on next window if in window already 4 digits
        if len(eval(f'self.part{self.part}.text()')) > 3:
            self.check += eval(f'self.part{self.part}.text()')
            self.part += 1
            eval(f'self.part{self.part}.setFocus()')

    def get_ticket(self):
        if self.check.isdigit():
            save_file_name = QFileDialog.getSaveFileName(self, 'Сохранение билета', '', '.txt')
            if save_file_name:  # if name was chose
                new_map = self.sess.get_hall_map().copy()
                new_map[self.index[0]][self.index[1]] = 2
                self.sess.create_csv(new_map)  # update hall map with chosen places

                with open(f'{save_file_name[0]}.txt', 'w', encoding='utf-8') as f:
                    data = f'{str(self.sess)}, ряд {self.index[0]}, место {self.seat}'
                    f.write(data)  # save ticket

                with open(f'admin_info.txt', 'r', encoding='utf-8') as f:  # read admin's info
                    info = f.read().split()

                with open(f'admin_info.txt', 'w', encoding='utf-8') as f:  # write new admin's info
                    f.write(f'{int(info[0]) + 1} {int(info[1]) + self.sess.price}')

                login = ex.user[0]
                if login != 'admin' and login != 'guest':  # load info about watched films for user
                    con = sqlite3.connect('film_library.db')
                    cur = con.cursor()
                    films = cur.execute(f'SELECT films FROM info '
                                        f'WHERE login = "{login}"').fetchall()[0][0]
                    films = str(films) + ',' + str(self.sess.film_id) \
                        if films else str(self.sess.film_id)
                    cur.execute(f'UPDATE info SET films = "{films}" WHERE login = "{login}"')
                    con.commit()
                    con.close()

                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Сохраните билет')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неправильные атрибуты карты')


class Registration(QDialog, Ui_Dialog_R):  # window for registration
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # clicked events

        self.cancel.clicked.connect(self.close_w)
        self.ok.clicked.connect(self.reg)

    def close_w(self):
        self.close()

    def reg(self):  # insert new user's attributes into DataBase
        login, name, psw = self.log_ent.text(), self.name_ent.text(), self.password_ent.text()
        if self.check_login():
            if name != '' and psw != '':
                con = sqlite3.connect('film_library.db')
                cur = con.cursor()
                cur.execute(f'''INSERT INTO info VALUES 
                ("{login}", "{name}", "{str(psw)}", '')''')
                con.commit()
                con.close()

                self.close_w()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            self.log_ent.setText('')
            QMessageBox.warning(self, 'Ошибка', 'Такой логин уже существует')

    def check_login(self):  # check if entered login had taken by other user (already in DataBase)
        login = self.log_ent.text()

        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        all_log = cur.execute('''SELECT login FROM info''').fetchall()
        all_log = list(map(lambda x: x[0], all_log))
        con.close()

        return False if login in all_log else True


class Login(QDialog, Ui_Dialog_L):  # window for login (authorization)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.is_admin = False
        self.user_login = ''

        # clicked events

        self.cancel.clicked.connect(self.close_w)
        self.ok.clicked.connect(self.login)

    def close_w(self):
        self.close()

    def login(self):  # return authorized user's attributes to MainW
        if self.check():
            con = sqlite3.connect('film_library.db')
            cur = con.cursor()
            info_user = cur.execute(f'''SELECT * FROM info 
            WHERE login = "{self.user_login}"''').fetchall()
            con.close()

            ex.user = info_user[0]
            self.is_admin = True if self.log_ent.text() == 'admin' else False
            ex.is_admin = self.is_admin
            ex.reload()

            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

    def check(self):  # check login and password for authorization in DataBase
        self.user_login, psw = self.log_ent.text(), self.password_ent.text()

        con = sqlite3.connect('film_library.db')
        cur = con.cursor()
        all_log_psw = cur.execute('''SELECT login, password FROM info''').fetchall()
        check_log_psw = cur.execute(f'''SELECT * FROM info 
        WHERE login = "{self.user_login}"''').fetchall()
        con.close()

        check_log_psw = (check_log_psw[0][0], str(check_log_psw[0][2])) \
            if check_log_psw else ('', '', '', '')
        all_log = list(map(lambda x: x[0], all_log_psw))  # list of logins
        all_psw = list(map(lambda x: str(x[1]), all_log_psw))  # list of passwords

        return True if self.user_login in all_log and psw in all_psw \
                       and (self.user_login, psw) == check_log_psw else False


class MainW(QMainWindow, Ui_MainWindow):  # the main window
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))

        self.window = None  # var for opening dialog windows
        self.user = ('guest', 'гость', 'guest', '')  # attributes for unauthorized users
        self.is_admin = False

        self.sessions_list = []

        self.load_sessions()  # load sessions from DataBase
        self.user_mode()  # load start interface for guest (it is also user)

        # loading clicked events on buttons

        self.ticket_cinema.clicked.connect(self.tickets_cinemas)
        self.del_sess.clicked.connect(self.delete_sess)
        self.sess.clicked.connect(self.add_session)
        self.reg.clicked.connect(self.open_reg_w)
        self.login.clicked.connect(self.open_login_w)
        self.info.clicked.connect(self.info_show)

    def open_reg_w(self):  # open registration window
        self.window = Registration()
        self.window.exec()

    def open_login_w(self):  # open window for login
        self.window = Login()
        self.window.exec()

    def reload(self):  # reload films sessions and makes change mods
        self.load_sessions()
        self.admin_mode() if self.is_admin else self.user_mode()

    def admin_mode(self):  # change interface for admin
        self.ticket_cinema.setText('Управление кинотеатрами')
        self.del_sess.setVisible(True)
        self.sess.setVisible(True)

    def user_mode(self):  # change interface for user
        self.ticket_cinema.setText('Купить билет')
        self.del_sess.setVisible(False)
        self.sess.setVisible(False)

    def tickets_cinemas(self):  # load function for mode admin/user
        self.add_cinema() if self.is_admin else self.buy_ticket()

    def delete_sess(self):  # admin can delete selected session
        sessions_index = self.sessisons.selectedIndexes()
        if sessions_index:  # delete if session(s) were selected
            sessions_index = map(lambda x: x.row(), sessions_index)
            for i in sessions_index:
                self.sessions_list[i].delete()
                self.sessions_list = self.sessions_list[:i] + self.sessions_list[i + 1:]

            self.load_sessions()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберете один или несколько сеансов')

    def info_show(self):  # show income to admin and list of watched films to user
        self.admin_info() if self.is_admin else self.user_info()

    def user_info(self):  # show info about watched films to authorized users
        self.window = Information()
        self.window.show()
        info = self.window.info
        if self.user[0] != 'guest':  # check user to authorizing
            info.appendPlainText(f'{self.user[1]}, эти фильмы вы смотрели у нас в кинотеатре:')
            info.appendPlainText('')

            con = sqlite3.connect('film_library.db')
            cur = con.cursor()
            films = str(cur.execute(f'SELECT films FROM info '
                                    f'WHERE login = "{self.user[0]}"').fetchall()[0][0])
            films = tuple(films.split(',')) if ',' in films else f'({films})'
            films = map(lambda x: x[0],
                        cur.execute(f'SELECT DISTINCT title FROM Films '
                                    f'WHERE id in {films}').fetchall())
            con.close()
            for film in films:
                info.appendPlainText(film)  # create list of films
        else:
            info.appendPlainText('Вы не вошли в систему')

    def admin_info(self):  # show info for admin
        self.window = Information()
        self.window.show()
        info = self.window.info
        info.appendPlainText(f'Здравствуйте, администратор')
        info.appendPlainText('Информация о работе кинотеатров:')

        with open(f'admin_info.txt', 'r', encoding='utf-8') as f:  # read admin's info
            info_for_admin = f.read().split()

        info.appendPlainText(f'Всего продано билетов: {info_for_admin[0]},')
        info.appendPlainText(f'Выручка за все время: {info_for_admin[1]} руб.')

    def load_sessions(self):  # update info about films sessions
        self.sessisons.clear()
        self.sessions_list.clear()

        con = sqlite3.connect('film_library.db')  # collect info about sessions from DataBase
        cur = con.cursor()
        sessions = cur.execute('SELECT * FROM sessions ORDER BY date, time, price').fetchall()
        con.close()

        for n, sess in enumerate(sessions):
            self.sessions_list.append(Session(*sess))  # append to list Session object
            self.sessisons.addItem(self.sessions_list[n].to_list())  # add sessions to QListWidget

    def add_cinema(self):  # create new cinema with address, working hours
        self.window = AddCinema(self.is_admin)
        self.window.exec()

    def add_session(self):  # create new session and add it to list with all sessions
        self.window = AddSession()
        self.window.exec()
        if self.window.finished:
            self.load_sessions()

    def buy_ticket(self):  # WITHOUT saving attributes anywhere
        sessions_index = self.sessisons.selectedIndexes()
        if sessions_index:
            if len(sessions_index) == 1:
                sess = self.sessions_list[sessions_index[0].row()]
                self.window = Hall(self.is_admin, AddCinema(self.is_admin).sql_req, sess)
                self.window.show()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Выберете один сеанс')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберете сеанс')


app = QApplication(sys.argv)
ex = MainW()
ex.show()
sys.exit(app.exec_())
