import csv
import os
import ast

FILENAME = 'students_db.csv'
LANGUAGES = ['English', 'Swedish', 'French']

def load_students():
    students = {}
    if os.path.exists(FILENAME):
        with open(FILENAME, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                age = row['age']
                language_classes = row.get('language_classes', '')
                grades_str = row.get('grades', '')
                if language_classes:
                    languages = set(language_classes.split(';'))
                else:
                    class_single = row.get('language_class', '')
                    languages = {class_single} if class_single else set()
                if grades_str:
                    try:
                        grades = ast.literal_eval(grades_str)
                    except:
                        grades = {}
                else:
                    grades = {}
                students[name] = {'age': age, 'language_classes': languages, 'grades': grades}
    return students

def save_students(students):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'age', 'language_classes', 'grades']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, info in students.items():
            languages_str = ';'.join(sorted(info['language_classes']))
            grades_str = str(info.get('grades', {}))
            writer.writerow({'name': name, 'age': info['age'], 'language_classes': languages_str, 'grades': grades_str})

def add_student(students):
    name = input('Введите имя ученика: ').strip()
    age = input('Введите возраст ученика: ').strip()
    print('Выберите класс(ы) (можно несколько, через запятую):')
    for idx, lang in enumerate(LANGUAGES, 1):
        print(f'{idx}. {lang}')
    choices = input('Введите номер(а) языка(ов), например 1,3: ').strip()
    selected_indexes = [c.strip() for c in choices.split(',') if c.strip() in ['1', '2', '3']]

    if not selected_indexes:
        print('Неверный выбор, попробуйте снова.')
        return

    selected_languages = {LANGUAGES[int(i) - 1] for i in selected_indexes}

    grades = {}
    for lang in selected_languages:
        while True:
            try:
                grade_input = input(f'Введите оценку ученика по {lang} в процентах (0-100): ').strip()
                grade = float(grade_input)
                if 0 <= grade <= 100:
                    grades[lang] = grade
                    break
                else:
                    print('Оценка должна быть от 0 до 100.')
            except ValueError:
                print('Пожалуйста, введите число.')

    if name in students:
        if students[name]['age'] != age:
            print(f"Обновляем возраст ученика {name} с {students[name]['age']} на {age}.")
            students[name]['age'] = age
        students[name]['language_classes'].update(selected_languages)
        students[name]['grades'].update(grades)
        print(f"Данные ученика {name} обновлены.")
    else:
        students[name] = {'age': age, 'language_classes': selected_languages, 'grades': grades}
        print(f"Ученик {name} добавлен с языками и оценками.")

def list_students(students):
    if not students:
        print('Список учеников пуст.')
        return
    print('Ученики:')
    for i, (name, info) in enumerate(students.items(), 1):
        languages_str = ', '.join(sorted(info['language_classes']))
        grades_str = ', '.join(f"{lang}: {info['grades'].get(lang, 'N/A')}%" for lang in sorted(info['language_classes']))
        print(f"{i}. {name}, Возраст: {info['age']}, Классы: {languages_str}, Оценки: {grades_str}")

def main():
    students = load_students()
    while True:
        print('\nМеню:')
        print('1. Добавить или обновить ученика')
        print('2. Показать список учеников')
        print('3. Выйти')
        choice = input('Введите номер действия: ').strip()
        if choice == '1':
            add_student(students)
            save_students(students)
        elif choice == '2':
            list_students(students)
        elif choice == '3':
            save_students(students)
            print('Данные сохранены. Выход.')
            break
        else:
            print('Неверный выбор, попробуйте снова.')

if __name__ == '__main__':
    main()
