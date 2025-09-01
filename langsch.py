import csv
import os

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
                # Языки хранятся в CSV через запятую
                language_classes = row['language_classes'].split(';')
                students[name] = {'age': age, 'language_classes': set(language_classes)}
    return students

def save_students(students):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'age', 'language_classes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, info in students.items():
            # Записываем языки через точку с запятой
            languages_str = ';'.join(sorted(info['language_classes']))
            writer.writerow({'name': name, 'age': info['age'], 'language_classes': languages_str})

def add_student(students):
    name = input('Введите имя ученика: ').strip()
    age = input('Введите возраст ученика: ').strip()
    print('Выберите класс (можно несколько, через запятую):')
    for idx, lang in enumerate(LANGUAGES, 1):
        print(f'{idx}. {lang}')
    choices = input('Введите номер(а) языка(ов), например 1,3: ').strip()
    selected_indexes = [c.strip() for c in choices.split(',') if c.strip() in ['1','2','3']]

    if not selected_indexes:
        print('Неверный выбор, попробуйте снова.')
        return

    selected_languages = {LANGUAGES[int(i) - 1] for i in selected_indexes}

    if name in students:
        # Если ученик уже есть, обновляем возраст и добавляем новые языки
        if students[name]['age'] != age:
            print(f"Обновляем возраст ученика {name} с {students[name]['age']} на {age}.")
            students[name]['age'] = age
        students[name]['language_classes'].update(selected_languages)
        print(f"Языки ученика {name} обновлены: {', '.join(sorted(students[name]['language_classes']))}.")
    else:
        students[name] = {'age': age, 'language_classes': selected_languages}
        print(f"Ученик {name} добавлен с языками: {', '.join(sorted(selected_languages))}.")

def list_students(students):
    if not students:
        print('Список учеников пуст.')
        return
    print('Ученики:')
    for i, (name, info) in enumerate(students.items(), 1):
        languages_str = ', '.join(sorted(info['language_classes']))
        print(f"{i}. {name}, Возраст: {info['age']}, Классы: {languages_str}")

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
