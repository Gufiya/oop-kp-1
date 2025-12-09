
# Для любого пользователя пароль для входа 123

import csv
import os
import glob
from datetime import date
from dataclasses import dataclass
from typing import List, Optional

TEST_CSV_FILE = "ТЕСТ_Студенты_и_стипендии.csv"
CSV_FILE = "Студенты_и_стипендии.csv"
BANK_SPRAV = {"044525974": "Сбербанк", "044525225": "ВТБ"}
FACULTIES = {
    "ИИМРТ": ["ИВТ-21", "ИВТ-22", "ПМИ-21", "ИВТ-31"],
    "ИПЧ": ["ПСИ-31", "БИО-41", "ХИМ-31", "ПСИ-41"]
}
USERS = {
    "deanery": ("123", "Петрова Е.С.", "Деканат"),
    "accountant": ("123", "Иванова А.В.", "Бухгалтер"),
    "commission": ("123", "Сидоров Д.А.", "Стипендиальная комиссия"),
    "admin": ("123", "Администратор", "Администратор")
}
SOCIAL_LABELS = {
    "": "Нет",
    "low_income": "Малоимущий",
    "orphan": "Сирота",
    "disabled": "Инвалид",
    "на рассмотрении": "На рассмотрении"
}
STIP_SIZES = {
    "академическая": 3000.0,
    "повышенная академическая": 5000.0,
    "социальная": 3340.0
}

@dataclass
class Student:
    id: int
    full_name: str 
    faculty: str
    group: str
    avg_grade: float
    social_status: str
    semester: str = ""
    bank_bik: str = ""
    account: str = ""

@dataclass
class Scholarship:
    student_id: int
    type: str
    period: str
    amount: float
    assigned_at: date
    status: str = "назначена"

class FileHandler:
    @staticmethod
    def init_test_csv():
        if not os.path.exists(TEST_CSV_FILE):
            with open(TEST_CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([
                    "ID", "Фамилия", "Имя", "Отчество", "Факультет", "Группа",
                    "Средний балл", "Соц.статус", "Семестр", "БИК банка", "Счет"
                ])
                test_data = [
                    [1, "Иванов", "Алексей", "Сергеевич", "ИИМРТ", "ИВТ-21", "4,75", "low_income", "", "044525974", "1111111111"],
                    [2, "Петрова", "Анна", "Владимировна", "ИИМРТ", "ИВТ-22", "5,00", "orphan", "", "044525974", "2222222222"],
                    [3, "Смирнов", "Дмитрий", "Андреевич", "ИИМРТ", "ПМИ-21", "3,90", "", "", "044525225", "3333333333"],
                    [4, "Козлова", "Елена", "Игоревна", "ИПЧ", "ПСИ-31", "4,50", "на рассмотрении", "", "044525974", "4444444444"],
                    [5, "Волков", "Иван", "Павлович", "ИПЧ", "БИО-41", "4,85", "disabled", "", "044525225", "5555555555"],
                    [6, "Морозова", "Мария", "Николаевна", "ИИМРТ", "ИВТ-31", "4,20", "", "", "044525974", "6666666666"],
                    [7, "Лебедев", "Артём", "Михайлович", "ИПЧ", "ХИМ-31", "3,75", "", "", "044525225", "7777777777"],
                    [8, "Новикова", "Софья", "Дмитриевна", "ИИМРТ", "ИВТ-21", "4,95", "low_income", "", "044525974", "8888888888"],
                    [9, "Федоров", "Максим", "Сергеевич", "ИПЧ", "ПСИ-41", "5,00", "", "осень 2025", "044525225", "9999999999"],
                    [10, "Гусев", "Андрей", "Викторович", "ИИМРТ", "ПМИ-21", "4,60", "на рассмотрении", "", "044525974", "1010101010"],
                    [11, "Соколова", "Виктория", "Алексеевна", "ИПЧ", "БИО-41", "4,30", "orphan", "осень 2025", "044525225", "1212121212"]
                ]
                writer.writerows(test_data)


    @staticmethod
    def init_csv():
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([
                    "ID", "Фамилия", "Имя", "Отчество", "Факультет", "Группа",
                    "Средний балл", "Соц.статус", "Семестр", "БИК банка", "Счет"
                ])

    @staticmethod
    def save_students(students: List[Student]):
        with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "ID", "Фамилия", "Имя", "Отчество", "Факультет", "Группа",
                "Средний балл", "Соц.статус", "Семестр", "БИК банка", "Счет"
            ])
            for s in students:
                parts = s.full_name.split()
                surname = parts[0] if len(parts) > 0 else ""
                name = parts[1] if len(parts) > 1 else ""
                patronymic = parts[2] if len(parts) > 2 else ""
                writer.writerow([
                    s.id, surname, name, patronymic, s.faculty, s.group,
                    str(s.avg_grade).replace(".", ","), s.social_status, s.semester, s.bank_bik, s.account
                ])

    @staticmethod
    def load_students() -> List[Student]:
        FileHandler.init_csv()
        students = []
        if os.path.getsize(CSV_FILE) > 0:
            with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                next(reader, None)
                for row in reader:
                    if row and len(row) >= 7:
                        avg = row[6].replace(",", ".")
                        avg = float(avg) if avg.replace(".", "", 1).isdigit() else 0.0
                        while len(row) < 11:
                            row.append("")
                        full_name = f"{row[1]} {row[2]} {row[3]}".strip()
                        s = Student(
                            id=int(row[0]),
                            full_name=full_name,
                            faculty=row[4],
                            group=row[5],
                            avg_grade=avg,
                            social_status=row[7],
                            semester=row[8],
                            bank_bik=row[9],
                            account=row[10]
                        )
                        students.append(s)
        return students

class ScholarshipRegistry:
    def load_from_students(self, students: List[Student]):
        for s in students:
            if s.semester:
                amount, type_stip = StipendCalculator.calculate(s.avg_grade, s.social_status)
                if amount > 0:
                    sch = Scholarship(
                        student_id=s.id,
                        type=type_stip,
                        period=s.semester,
                        amount=amount,
                        assigned_at=date.today(),
                    )
                    self.assignments.append(sch)


    def __init__(self):
        self.assignments: List[Scholarship] = []

    def is_duplicate(self, student_id: int, period: str) -> bool:
        return any(
            s.student_id == student_id and s.period == period
            for s in self.assignments
            if s.status != "отменена"
        )

    def add_scholarship(self, student_id: int, type_: str, period: str, amount: float) -> bool:
        if self.is_duplicate(student_id, period):
            return False
        sch = Scholarship(student_id, type_, period, amount, date.today())
        self.assignments.append(sch)
        return True

    def save_assignment(self, filename: str, assignments: List[dict]):
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ФИО", "Группа", "Факультет", "Тип стипендии", "Сумма в месяц"])
            for a in assignments:
                writer.writerow([a["ФИО"], a["Группа"], a["Факультет"], a["Тип"], a["Сумма"]])

class StipendCalculator:
    @staticmethod
    def calculate(avg: float, social: str) -> tuple[float, str]:
        stip = 0.0
        type_stip = ""
        if avg >= 5.0:
            stip = STIP_SIZES["повышенная академическая"]
            type_stip = "Повышенная академическая"
        elif avg >= 4.0:
            stip = STIP_SIZES["академическая"]
            type_stip = "Академическая"
        if social in ["low_income", "orphan", "disabled"]:
            stip += STIP_SIZES["социальная"]
            type_stip += ", Социальная" if type_stip else "Социальная"
        return stip, type_stip

class StipendSystem:
    def __init__(self):
        self.use_test_data = False
        self.role = None
        self.name = None
        self.file_handler = FileHandler()
        self.registry = ScholarshipRegistry()

    def login(self):
        print("\n" + "="*50)
        print(" ВХОД В СИСТЕМУ")
        print("="*50)
        while True:
            login = input("Логин (deanery/accountant/commission/admin): ").strip()
            pwd = input("Пароль: ").strip()
            if login in USERS and USERS[login][0] == pwd:
                self.role = USERS[login][2]
                self.name = USERS[login][1]
                print(f"\nДобро пожаловать, {self.name} [{self.role}]!")
                return
            print("Неверный логин или пароль")

    def view_students(self):
        students = self.file_handler.load_students()
        if not students:
            print("\nСписок студентов пуст.")
            input("\n[Enter] — вернуться")
            return
        print("\n" + "="*100)
        print(f"{'№':<4} {'ФИО':<35} {'Группа':<10} {'Факультет':<12} {'Балл':<8} {'Статус':<20} {'Семестр':<10} {'Банк':<20} {'Счет':<20}")
        print("-"*100)
        for i, s in enumerate(students, 1):
            status = SOCIAL_LABELS.get(s.social_status, s.social_status) if s.social_status else "Нет"
            semester = s.semester if s.semester else "Не назначен"
            bank = BANK_SPRAV.get(s.bank_bik, s.bank_bik) if s.bank_bik else "Не указан"
            account = s.account if s.account else "Не указан"
            print(f"{i:<4} {s.full_name:<35} {s.group:<10} {s.faculty:<12} {s.avg_grade:<8.2f} {status:<20} {semester:<10} {bank:<20} {account:<20}")
        print("="*100)
        input("\n[Enter] — вернуться")

    def add_student(self):
        print("\n" + "="*55)
        print(" ДОБАВЛЕНИЕ СТУДЕНТА")
        print("="*55)
        fio = input("ФИО студента: ").strip()
        while len(fio) < 5:
            fio = input("ФИО слишком короткое, введите снова: ").strip()

        print("\nВыберите факультет:")
        for i, f in enumerate(FACULTIES, 1):
            print(f"{i}. {f}")
        while True:
            try:
                f = int(input("-> ")) - 1
                if 0 <= f < len(FACULTIES):
                    faculty = list(FACULTIES.keys())[f]
                    break
            except: print("Введите число")

        print(f"\nГруппы {faculty}:")
        for i, g in enumerate(FACULTIES[faculty], 1):
            print(f"{i}. {g}")
        while True:
            try:
                g = int(input("-> ")) - 1
                if 0 <= g < len(FACULTIES[faculty]):
                    group = FACULTIES[faculty][g]
                    break
            except: print("Введите число")
        while True:
            try:
                avg = float(input("Средний балл (0.00–5.00): ").replace(",", "."))
                if 0 <= avg <= 5:
                    avg = round(avg, 2)
                    break
            except: print("Введите число")

        print("\nСоц.статус:")
        print("1. Малоимущий\n2. Сирота\n3. Инвалид\n4. На рассмотрении\n5. Нет")
        status_map = {"1": "low_income", "2": "orphan", "3": "disabled", "4": "на рассмотрении", "5": ""}
        while True:
            ch = input("-> ").strip()
            if ch in status_map:
                social = status_map[ch]
                break
            print("Выберите от 1 до 5")

        print("\nВыберите банк:")
        bank_list = list(BANK_SPRAV.items())
        for i, (bik, name) in enumerate(bank_list, 1):
            print(f"{i}. {name} (БИК: {bik})")
        bik = ""
        while True:
            try:
                b = int(input("-> ")) - 1
                if 0 <= b < len(bank_list):
                    bik = bank_list[b][0]
                    break
            except: print("Введите число")

        account = input("Номер счета (10 цифр): ").strip()
        while len(account) != 10 or not account.isdigit():
            account = input("Неверный формат, введите 10 цифр: ").strip()
        students = self.file_handler.load_students()
        if any(s.full_name == fio and s.group == group for s in students):
            print("\nОШИБКА: Студент с таким ФИО уже есть в этой группе!")
            input("[Enter]")
            return
        new_id = len(students) + 1
        students.append(Student(new_id, fio, faculty, group, avg, social, "", bik, account))
        self.file_handler.save_students(students)
        print("\nСтудент успешно добавлен!")
        input("[Enter]")

    def edit_student(self):
        students = self.file_handler.load_students()
        if not students:
            print("\nСписок студентов пуст.")
            input("[Enter]")
            return
        self.view_students()
        while True:
            try:
                num = int(input("\nВведите № студента для редактирования (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(students):
                    s = students[num - 1]
                    break
            except:
                print("Введите число")
        print("\nРедактирование студента: " + s.full_name)

        fio = input(f"ФИО ({s.full_name}): ").strip() or s.full_name

        print("\nФакультет (" + s.faculty + "):")
        for i, f in enumerate(FACULTIES, 1):
            print(f"{i}. {f}")
        faculty = s.faculty
        ch = input("-> (Enter — без изменений): ").strip()
        if ch:
            try:
                f = int(ch) - 1
                if 0 <= f < len(FACULTIES):
                    faculty = list(FACULTIES.keys())[f]
            except: pass

        print(f"\nГруппа ({s.group}):")
        for i, g in enumerate(FACULTIES[faculty], 1):
            print(f"{i}. {g}")
        group = s.group
        ch = input("-> (Enter — без изменений): ").strip()
        if ch:
            try:
                g = int(ch) - 1
                if 0 <= g < len(FACULTIES[faculty]):
                    group = FACULTIES[faculty][g]
            except: pass

        avg = s.avg_grade
        ch = input(f"Средний балл ({avg:.2f}): ").strip()
        if ch:
            try:
                avg = float(ch.replace(",", "."))
                if 0 <= avg <= 5:
                    avg = round(avg, 2)
            except: pass

        print("\nСоц.статус (" + SOCIAL_LABELS.get(s.social_status, "Нет") + "):")
        print("1. Малоимущий\n2. Сирота\n3. Инвалид\n4. На рассмотрении\n5. Нет")
        social = s.social_status
        ch = input("-> (Enter — без изменений): ").strip()
        if ch:
            status_map = {"1": "low_income", "2": "orphan", "3": "disabled", "4": "на рассмотрении", "5": ""}
            if ch in status_map:
                social = status_map[ch]

        current_bank = BANK_SPRAV.get(s.bank_bik, "Не указан") if s.bank_bik else "Не указан"
        print(f"\nБанк ({current_bank}):")
        bank_list = list(BANK_SPRAV.items())
        for i, (bik, name) in enumerate(bank_list, 1):
            print(f"{i}. {name} (БИК: {bik})")
        bik = s.bank_bik
        ch = input("-> (Enter — без изменений): ").strip()
        if ch:
            try:
                b = int(ch) - 1
                if 0 <= b < len(bank_list):
                    bik = bank_list[b][0]
            except: pass

        account = s.account
        ch = input(f"Номер счета ({account}): ").strip()
        if ch:
            if len(ch) == 10 and ch.isdigit():
                account = ch
            else:
                print("Неверный формат, изменения не применены")
        if (fio != s.full_name or group != s.group) and any(st.full_name == fio and st.group == group and st.id != s.id for st in students):
            print("\nОШИБКА: Студент с таким ФИО уже есть в этой группе!")
            input("[Enter]")
            return
        s.full_name = fio
        s.faculty = faculty
        s.group = group
        s.avg_grade = avg
        s.social_status = social
        s.bank_bik = bik
        s.account = account
        self.file_handler.save_students(students)
        print("\nСтудент обновлён!")
        input("[Enter]")

    def delete_student(self):
        students = self.file_handler.load_students()
        if not students:
            print("\nСписок студентов пуст.")
            input("[Enter]")
            return
        self.view_students()
        while True:
            try:
                num = int(input("\nВведите № студента для удаления (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(students):
                    del students[num - 1]
                    for i, s in enumerate(students, 1):
                        s.id = i
                    self.file_handler.save_students(students)
                    print("\nСтудент удалён!")
                    input("[Enter]")
                    return
            except:
                print("Введите число")

    def filter_and_export(self):
        students = self.file_handler.load_students()
        if not students:
            print("\nСписок пуст.")
            input("[Enter]")
            return
        print("\n" + "="*55)
        print(" ФИЛЬТР И ЭКСПОРТ")
        print("="*55)
        print("1. По факультету\n2. По группе\n3. По минимальному баллу\n4. По соц.статусу\n5. По семестру\n0. Без фильтра")
        filters = []
        while True:
            ch = input("Выберите фильтр (0-5, через запятую для нескольких): ").strip()
            if ch == "0": break
            try:
                opts = [int(x) for x in ch.split(",")]
                break
            except: print("Введите числа")
        filtered = students[:]
        if 1 in opts:
            print("\nФакультеты:")
            for i, f in enumerate(FACULTIES, 1):
                print(f"{i}. {f}")
            while True:
                try:
                    f = int(input("-> ")) - 1
                    if 0 <= f < len(FACULTIES):
                        fac = list(FACULTIES.keys())[f]
                        filtered = [s for s in filtered if s.faculty == fac]
                        break
                except: print("Введите число")
        if 2 in opts:
            group = input("Группа (например, ИВТ-21): ").strip()
            filtered = [s for s in filtered if s.group == group]
        if 3 in opts:
            while True:
                try:
                    min_avg = float(input("Минимальный балл: ").replace(",", "."))
                    filtered = [s for s in filtered if s.avg_grade >= min_avg]
                    break
                except: print("Введите число")
        if 4 in opts:
            print("\nСоц.статус:")
            print("1. Малоимущий\n2. Сирота\n3. Инвалид\n4. На рассмотрении\n5. Нет")
            while True:
                ch = input("-> ").strip()
                status_map = {"1": "low_income", "2": "orphan", "3": "disabled", "4": "на рассмотрении", "5": ""}
                if ch in status_map:
                    filtered = [s for s in filtered if s.social_status == status_map[ch]]
                    break
                print("Выберите от 1 до 5")
        if 5 in opts:
            semester = input("Семестр (например, осень 2025): ").strip()
            filtered = [s for s in filtered if s.semester == semester]

        if not filtered:
            print("\nНет студентов по фильтру.")
        else:
            print("\n" + "="*100)
            print(f"{'№':<4} {'ФИО':<35} {'Группа':<10} {'Факультет':<12} {'Балл':<8} {'Статус':<20} {'Семестр':<10} {'Банк':<20} {'Счет':<20}")
            print("-"*100)
            for i, s in enumerate(filtered, 1):
                status = SOCIAL_LABELS.get(s.social_status, s.social_status) if s.social_status else "Нет"
                sem = s.semester if s.semester else "Не назначен"
                bank = BANK_SPRAV.get(s.bank_bik, s.bank_bik) if s.bank_bik else "Не указан"
                account = s.account if s.account else "Не указан"
                print(f"{i:<4} {s.full_name:<35} {s.group:<10} {s.faculty:<12} {s.avg_grade:<8.2f} {status:<20} {sem:<10} {bank:<20} {account:<20}")
            print("="*100)

        import datetime
        export_file = f"Экспорт_фильтр_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(export_file, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["ID", "ФИО", "Факультет", "Группа", "Средний балл", "Соц.статус", "Семестр", "БИК банка", "Счет"])
                for s in filtered:
                    writer.writerow([s.id, s.full_name, s.faculty, s.group, str(s.avg_grade).replace(".", ","), s.social_status, s.semester, s.bank_bik, s.account])
            print(f"\nЭкспорт создан: {export_file}")
        except PermissionError:
            print(f"\n Ошибка: Не удалось записать файл '{export_file}'. Убедитесь, что он не открыт в другом приложении.")
        input("[Enter]")


    def commission_work(self):
        students = self.file_handler.load_students()
        pending = [s for s in students if s.social_status == "на рассмотрении"]
        if not pending:
            print("\nНет заявлений на рассмотрении.")
            input("[Enter]")
            return
        print("\n" + "="*100)
        print(" ЗАЯВЛЕНИЯ НА РАССМОТРЕНИЕ")
        print(f"{'№':<4} {'ФИО':<35} {'Группа':<10} {'Факультет':<12} {'Балл':<8}")
        print("-"*100)
        for i, s in enumerate(pending, 1):
            print(f"{i:<4} {s.full_name:<35} {s.group:<10} {s.faculty:<12} {s.avg_grade:<8.2f}")
        print("="*100)
        while True:
            try:
                num = int(input("\nВведите № для рассмотрения (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(pending):
                    s = pending[num - 1]
                    break
            except:
                print("Введите число")
        print("\nРассмотрение заявления: " + s.full_name)
        print("1. Одобрить как малоимущий\n2. Одобрить как сирота\n3. Одобрить как инвалид\n4. Отклонить\n5. Оставить на рассмотрении")
        status_map = {"1": "low_income", "2": "orphan", "3": "disabled", "4": "", "5": "на рассмотрении"}
        while True:
            ch = input("-> ").strip()
            if ch in status_map:
                s.social_status = status_map[ch]
                break
            print("Выберите от 1 до 5")
        self.file_handler.save_students(students)
        print("\nЗаявление рассмотрено!")
        input("[Enter]")


    def assign_stipend(self):
        students = self.file_handler.load_students()

        self.registry.load_from_students(students)

        if not students:
            print("Список пуст")
            input("[Enter]")
            return
        semester = input("\nЗа какой семестр назначаем стипендию? (осень 2025 / весна 2026): ").strip()
        filename = f"Назначения_{semester.replace(' ', '_')}.csv"
        if os.path.exists(filename):
            print(f"\nОШИБКА: Назначение за {semester} уже создано!")
            input("[Enter]")
            return
        lines = []
        total_monthly = 0.0
        for s in students:
            stip, type_stip = StipendCalculator.calculate(s.avg_grade, s.social_status)
            if stip > 0:
                if self.registry.is_duplicate(s.id, semester):
                    print(f"Предупреждение: стипендия для {s.full_name} уже назначена на {semester}, пропуск.")
                    continue
                self.registry.add_scholarship(s.id, type_stip, semester, stip)
                lines.append({"ФИО": s.full_name, "Группа": s.group, "Факультет": s.faculty, "Тип": type_stip, "Сумма": stip})
                total_monthly += stip
                print(f"{s.full_name}: {type_stip} — {stip:.2f} руб. в месяц")
                s.semester = semester
        self.file_handler.save_students(students)
        self.registry.save_assignment(filename, lines)
        total_semester = total_monthly * 5
        print(f"\nНазначение создано: {filename}")
        print(f"Общая сумма на семестр: {total_semester:.2f} руб.")
        input("[Enter]")

    def monthly_payments(self):
        students = self.file_handler.load_students()
        if not students:
            print("Список пуст")
            input("[Enter]")
            return
        month = input("\nЗа какой месяц выплата? (декабрь 2025): ").strip()
        filename = f"Реестр_выплат_{month.replace(' ', '_')}.csv"
        if os.path.exists(filename):
            print(f"\nОШИБКА: Выплата за {month} уже создана!")
            input("[Enter]")
            return
        pp_num = "ПП-" + str(len(glob.glob("Реестр_выплат_*.csv")) + 1).zfill(3)
        lines = []
        total = 0.0
        for s in students:
            if s.semester:
                stip, type_stip = StipendCalculator.calculate(s.avg_grade, s.social_status)
                if stip > 0:
                    lines.append([s.full_name, s.group, s.faculty, type_stip, stip, s.bank_bik, s.account])
                    total += stip
        with open(filename, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Тип_записи", "Номер_документа", "Дата", "ФИО_студента", "Группа", "Факультет", "Тип_стипендии", "Семестр", "Сумма", "БИК", "Счет", "Статус"])
            for line in lines:
                w.writerow(["Платёжное поручение", pp_num, date.today().strftime("%d.%m.%Y"), line[0], line[1], line[2], line[3], s.semester, str(line[4]).replace('.', ','), line[5], line[6], "Выплачено"])
        print(f"\nРеестр выплат создан: {filename}")
        print(f"Общая сумма выплат: {total:.2f} руб.")
        input("[Enter]")

    def view_assignments(self):
        files = glob.glob("Назначения_*.csv")
        if not files:
            print("\nНет созданных назначений.")
            input("[Enter]")
            return
        print("\nСписок назначений:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        while True:
            try:
                num = int(input("\nВыберите номер для просмотра (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(files):
                    with open(files[num - 1], "r", encoding="utf-8-sig", newline="") as f:
                        reader = csv.reader(f, delimiter=";")
                        for row in reader:
                            print("; ".join(row))
                    input("\n[Enter] — вернуться")
                    break
            except:
                print("Введите число")

    def view_payments(self):
        files = glob.glob("Реестр_выплат_*.csv")
        if not files:
            print("\nНет созданных реестров выплат.")
            input("[Enter]")
            return
        print("\nСписок реестров выплат:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        while True:
            try:
                num = int(input("\nВыберите номер для просмотра (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(files):
                    with open(files[num - 1], "r", encoding="utf-8-sig", newline="") as f:
                        reader = csv.reader(f, delimiter=";")
                        for row in reader:
                            print("; ".join(row))
                    input("\n[Enter] — вернуться")
                    break
            except:
                print("Введите число")

    def add_user(self):
        print("\n" + "="*55)
        print(" ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
        print("="*55)
        login = input("Логин: ").strip().lower()
        if login in USERS:
            print("Логин уже существует!")
            input("[Enter]")
            return
        pwd = input("Пароль: ").strip()
        name = input("ФИО: ").strip()
        print("Роль: 1. Деканат\n2. Бухгалтер\n3. Стипендиальная комиссия\n4. Администратор")
        role_map = {"1": "Деканат", "2": "Бухгалтер", "3": "Стипендиальная комиссия", "4": "Администратор"}
        while True:
            ch = input("-> ").strip()
            if ch in role_map:
                role = role_map[ch]
                break
            print("Выберите от 1 до 4")
        USERS[login] = (pwd, name, role)
        print("\nПользователь добавлен!")
        input("[Enter]")

    def edit_user(self):
        if not USERS:
            print("\nНет пользователей.")
            input("[Enter]")
            return
        print("\nСписок пользователей:")
        user_list = list(USERS.keys())
        for i, login in enumerate(user_list, 1):
            u = USERS[login]
            print(f"{i}. {login} - {u[1]} [{u[2]}]")
        while True:
            try:
                num = int(input("\n№ для редактирования (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(user_list):
                    login = user_list[num - 1]
                    u = USERS[login]
                    break
            except:
                print("Введите число")
        print(f"\nРедактирование: {login}")
        pwd = input(f"Новый пароль ({'******' if u[0] else 'нет'}): ").strip() or u[0]
        name = input(f"ФИО ({u[1]}): ").strip() or u[1]
        print(f"Роль ({u[2]}): 1. Деканат\n2. Бухгалтер\n3. Стипендиальная комиссия\n4. Администратор")
        role = u[2]
        ch = input("-> (Enter — без изменений): ").strip()
        if ch:
            role_map = {"1": "Деканат", "2": "Бухгалтер", "3": "Стипендиальная комиссия", "4": "Администратор"}
            if ch in role_map:
                role = role_map[ch]
        USERS[login] = (pwd, name, role)
        print("\nПользователь обновлён!")
        input("[Enter]")

    def delete_user(self):
        if not USERS:
            print("\nНет пользователей.")
            input("[Enter]")
            return
        print("\nСписок пользователей:")
        user_list = list(USERS.keys())
        for i, login in enumerate(user_list, 1):
            u = USERS[login]
            print(f"{i}. {login} - {u[1]} [{u[2]}]")
        while True:
            try:
                num = int(input("\n№ для удаления (0 — назад): "))
                if num == 0:
                    return
                if 1 <= num <= len(user_list):
                    login = user_list[num - 1]
                    del USERS[login]
                    print("\nПользователь удалён!")
                    input("[Enter]")
                    return
            except:
                print("Введите число")

    def run(self):
        while True:
            print(" ИС студенческой бухгалтерии «Назначение стипендий» ")
            if not self.role:
                print("1. Вход в систему\n0. Выход")
                ch = input("-> ").strip()
                if ch == "1": self.login()
                elif ch == "0": break
            else:
                print(f"Пользователь: {self.name} [{self.role}]")
                if self.role == "Деканат":
                    print("\n1. Просмотреть студентов")
                    print("2. Добавить студента")
                    print("3. Редактировать студента")
                    print("7. Удалить студента")
                    print("4. Фильтр + экспорт")
                elif self.role == "Стипендиальная комиссия":
                    print("\n1. Просмотреть студентов")
                    print("2. Рассмотреть заявления")
                elif self.role == "Бухгалтер":
                    print("\n1. Просмотреть студентов")
                    print("2. Назначить стипендию (семестр)")
                    print("3. Выплата стипендии (месяц)")
                    print("5. Просмотреть назначения семестров")
                    print("6. Просмотреть реестры выплат")
                elif self.role == "Администратор":
                    print("\n1. Просмотреть студентов")
                    print("2. Добавить пользователя")
                    print("3. Редактировать пользователя")
                    print("7. Удалить пользователя")
                print("8. Использовать тестовую базу студентов" + (" (уже выбрана)" if self.use_test_data else ""))
                print("9. Выйти из аккаунта")
                ch = input("\n-> ").strip()
                if ch == "1": self.view_students()
                elif ch == "2" and self.role == "Деканат": self.add_student()
                elif ch == "3" and self.role == "Деканат": self.edit_student()
                elif ch == "7" and self.role == "Деканат": self.delete_student()
                elif ch == "4" and self.role == "Деканат": self.filter_and_export()
                elif ch == "2" and self.role == "Стипендиальная комиссия": self.commission_work()
                elif ch == "2" and self.role == "Бухгалтер": self.assign_stipend()
                elif ch == "3" and self.role == "Бухгалтер": self.monthly_payments()
                elif ch == "5" and self.role == "Бухгалтер": self.view_assignments()
                elif ch == "6" and self.role == "Бухгалтер": self.view_payments()
                elif ch == "2" and self.role == "Администратор": self.add_user()
                elif ch == "3" and self.role == "Администратор": self.edit_user()
                elif ch == "7" and self.role == "Администратор": self.delete_user()
                elif ch == "8":
                    self.use_test_data = True
                    global CSV_FILE
                    CSV_FILE = TEST_CSV_FILE
                    print("\nТестовая база студентов активирована!")
                    input("[Enter]")

                elif ch == "9": self.role = self.name = None
                else:
                    print("Недоступная команда для этой роли.")

if __name__ == "__main__":
    FileHandler.init_test_csv()
    StipendSystem().run()