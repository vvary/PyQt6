import sys
import sqlite3 as sq
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QRadioButton, QMessageBox
import time
import pandas as pd

local = time.ctime(time.time())

with sq.connect("employees.db") as base:
    sql = base.cursor()
    sql.execute('DROP TABLE IF EXISTS employees')
    sql.execute("""CREATE TABLE IF NOT EXISTS employees(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        job TEXT,
        phone TEXT,
        email TEXT,
        enter TEXT ,
        exit TEXT 
        );
        """)
    sql.executemany("INSERT INTO employees VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)", pd.read_excel('employees.xlsx'))
base.commit()

with sq.connect("guests.db") as base2:
    sql2 = base2.cursor()
    sql2.execute('DROP TABLE IF EXISTS guests')
    sql2.execute("""CREATE TABLE IF NOT EXISTS guests(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        target TEXT,
        phone TEXT,
        email TEXT,
        enter INt,
        exit INT 
        );
        """)
base2.commit()


class PassControlApp(QWidget):
    def __init__(self):
        super().__init__()
        global sql
        global base
        global employees
        global guests
        self.sql = 0
        self.car = 0

        self.issue_pass_button2 = QPushButton('Меню гостя')
        self.issue_pass_button = QPushButton('Вход')
        self.issue_pass_button3 = QPushButton('Выход')

        self.issue_pass_button.clicked.connect(self.ENTER)
        self.issue_pass_button3.clicked.connect(self.EXIT)
        self.issue_pass_button2.clicked.connect(self.GST_ENTRY)

        self.RadioButton.toggled.connect(self.update)

        self.name = QLineEdit(self, placeholderText="Ведите почту сотрудника...")

        self.passv = QLineEdit(self, placeholderText="Ведите имя...")

        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.passv)
        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button2)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.issue_pass_button3)

        self.setLayout(layout)
        self.setWindowTitle('Терминал Охраны')

    def GST_ENTRY(self):
        pass1.show()

    def ENTER(self):
        global guests
        global employees
        self.adc = self.name.text().find("@")
        self.dfe = self.name.text()

        self.local_time = time.ctime(time.time())
        if self.car == 1:

            if employees != 0:
                if employees < 5 and guests > 0:
                    employees = employees - 1
                    guests = guests - 1
                else:
                    employees = employees - 1
                sql.execute(f"""UPDATE employees SET enter = ? where email = ? """, [self.local_time, self.dfe])

                sql.execute('SELECT email FROM employees')

                self.rows = sql.fetchall()
                if self.rows.count((self.name.text(),)):
                    print("Сотрудник", self.dfe, "Вошёл")
                else:
                    print("Такой почты нет в базе данных")
                base.commit()

            else:
                print("Извините мест нет")

        elif self.car == 0:
            sql.execute(f"""UPDATE employees SET enter = ? where email = ? """, [self.local_time, self.dfe])
            base.commit()
            sql.execute('SELECT email FROM employees')
            self.rows = sql.fetchall()
            if self.rows.count((self.name.text(),)):
                print("Сотрудник", self.dfe, "Вошёл")
            else:
                print("Такой почты нет в базе данных")

    def EXIT(self):
        global guests
        global employees
        self.dfe = self.name.text()
        if self.car == 1:
            if employees < 5 and guests < 5:
                employees = employees + 1
                guests = guests + 1
            employees = employees + 1
        self.local_time = time.ctime(time.time())
        sql.execute(f"""UPDATE employees SET exit = ? where email = ? AND enter != 'NULL' """,
                    [self.local_time, self.dfe])
        sql.execute('SELECT email FROM employees')
        self.rows = sql.fetchall()
        if self.rows.count((self.name.text(),)):
            print("Сотрудник", self.dfe, "Вышел")
        else:
            print("Такой почты нет в базе данных")
        base.commit()

    base.commit()

    def update(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        print(self.car)


class gst_term(QWidget):
    def __init__(self):

        super().__init__()
        self.car = 0
        global sql2
        global base2
        global employees
        global guests

        self.pass_label = QLabel('Пропускные документы: 0')

        self.issue_pass_button2 = QPushButton('Выход')
        self.issue_pass_button = QPushButton('Вход')

        self.issue_pass_button.clicked.connect(self.issue_pass)
        self.issue_pass_button2.clicked.connect(self.gostevoy)
        self.RadioButton.toggled.connect(self.update)

        self.exit = QLineEdit(self, placeholderText="Ведите контактную почту для выхода...")

        self.firstname = QLineEdit(self, placeholderText="Ведите фамилию ...")
        self.name = QLineEdit(self, placeholderText="Ведите имя...")
        self.lastname = QLineEdit(self, placeholderText="Ведите отчество...")
        self.birth = QLineEdit(self, placeholderText="Ведите дату рождения...")
        self.target = QLineEdit(self, placeholderText="Ведите цель визита...")
        self.phone = QLineEdit(self, placeholderText="Ведите номер телефона...")
        self.email = QLineEdit(self, placeholderText="Ведите контактную почту...")

        layout = QVBoxLayout()

        layout.addWidget(self.pass_label)

        layout.addWidget(self.firstname)
        layout.addWidget(self.name)
        layout.addWidget(self.lastname)
        layout.addWidget(self.birth)
        layout.addWidget(self.target)
        layout.addWidget(self.phone)
        layout.addWidget(self.email)

        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.exit)
        layout.addWidget(self.issue_pass_button2)

        self.setLayout(layout)
        self.setWindowTitle('Гостевой Терминал')

    def update(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        if guests == 0:
            print("Места Закончились")

    def gostevoy(self):
        global guests
        global employees
        if self.car == 1:
            employees = employees + 1
            guests = guests + 1
        self.exi = self.exit.text()
        self.time = time.time()
        self.local_time = time.ctime(time.time())
        sql2.execute(f"""UPDATE guests SET exit = ? where email = ? """, [self.time, self.exi])
        sql2.execute('SELECT email FROM guests')
        self.rows = sql2.fetchall()
        if self.rows.count((self.exit.text(),)):
            print("Гость", self.exi, "Вышел")
            sql2.execute('SELECT enter , exit FROM guests WHERE email = ? ', (self.pochtat,))
            self.rows2 = sql2.fetchall()
            self.tkk = self.rows2[0]
            self.tk, self.tx = self.tkk
            if self.tx - self.tk > 10:
                print(
                    f"Гость {self.exi} - привысил время посещения на {(self.tx) - (self.tk) - 10} сек, 'Просим обратиться к начальству'")
            if self.tx - self.tk < 10:
                print(f"Гость {self.exi} пробыл внутри {(self.tx) - (self.tk)} ")
        else:
            print("Такой почты нет в базе данных")

    def issue_pass(self):
        global guests
        global employees
        if self.car == 1:
            if guests == 0:
                print("Места закончились!!!")
            else:
                employees = employees - 1
                guests = guests - 1
                self.time = time.time()
                self.familt = self.firstname.text()
                self.namet = self.name.text()
                self.otcht = self.lastname.text()
                self.datet = self.birth.text()
                self.celt = self.target.text()
                self.nomert = self.phone.text()
                self.pochtat = self.email.text()
                self.CORT = [(self.familt, self.namet, self.otcht, self.datet, self.celt, self.nomert, self.pochtat,
                              self.time, 0)]

                sql2.execute('SELECT email FROM guests')
                self.rows = sql2.fetchall()
                if self.rows.count((self.email.text(),)):
                    print("Такая почта уже есть")
                else:
                    print("Гость", self.pochtat, "Вошёл")
                    sql2.executemany("INSERT INTO guests VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)", self.CORT)
                    base2.commit()
        else:
            self.time = time.time()
            self.familt = self.firstname.text()
            self.namet = self.name.text()
            self.otcht = self.lastname.text()
            self.datet = self.phone.text()
            self.celt = self.target.text()
            self.nomert = self.phone.text()
            self.pochtat = self.email.text()
            self.CORT = [
                (self.familt, self.namet, self.otcht, self.datet, self.celt, self.nomert, self.pochtat, self.time, 0)]
            sql2.execute('SELECT email FROM guests')
            self.rows = sql2.fetchall()
            if self.rows.count((self.email.text(),)):
                print("Такая почта уже есть")
            else:
                print("Гость", self.pochtat, "Вошёл")
                sql2.executemany("INSERT INTO guests VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)", self.CORT)
                base2.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass_control = PassControlApp()
    pass1 = gst_term()
    pass_control.show()
    sys.exit(app.exec())
