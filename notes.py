import uuid
import json
from datetime import datetime
import argparse

def create_note():
    note_id = str(uuid.uuid4())
    title = input("Введите заголовок заметки: ")
    body = input("Введите текст заметки: ")
    timestamp = datetime.now().isoformat()

    return {"id": note_id, "title": title, "body": body, "timestamp": timestamp}

def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file)

def read_notes():
    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []

    return notes

def read_notes_by_date(notes, date_filter):
    filtered_notes = [note for note in notes if note["timestamp"].startswith(date_filter)]
    return filtered_notes

def edit_note(notes, note_id):
    if not note_id or not any(note["id"] == note_id for note in notes):
        print("Неверный ID или заметка не найдена. Редактирование не выполнено.")
        return

    for note in notes:
        if note["id"] == note_id:
            print(f"Редактирование заметки с ID {note_id}:")
            note["title"] = input(f"Новый заголовок ({note['title']}): ") or note['title']
            note["body"] = input(f"Новый текст ({note['body']}): ") or note['body']
            note["timestamp"] = datetime.now().isoformat()
            save_notes(notes)
            print("Заметка успешно отредактирована.")
            return

def delete_note(notes, note_id):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            print(f"Заметка с ID {note_id} успешно удалена.")
            return
    print(f"Заметка с ID {note_id} не найдена.")

def main():
    print("Добро пожаловать в программу управления заметками!")

    while True:
        print("Меню:")
        print("1. Добавить заметку")
        print("2. Просмотреть заметки")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выйти из программы")

        choice = input("Выберите действие (введите номер): ")

        if choice == "1":
            new_note = create_note()
            notes = read_notes()
            notes.append(new_note)
            save_notes(notes)
            print("Заметка успешно сохранена.")
        elif choice == "2":
            date_filter = input("Фильтрация по дате (гггг-мм-дд) или Enter для вывода всех заметок: ")
            filtered_notes = read_notes_by_date(notes, date_filter) if date_filter else read_notes()

            if not filtered_notes:
                print("Нет заметок для отображения.")
            else:
                for note in filtered_notes:
                    print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['timestamp']}")

                edit_option = input(
                    "Введите ID заметки для редактирования или нажмите Enter для возврата в главное меню: ")
                if edit_option and any(note["id"] == edit_option for note in filtered_notes):
                    edit_note(filtered_notes, edit_option)
                elif not edit_option:
                    continue
                else:
                    print("Неверный ID. Редактирование не выполнено.")
        elif choice == "3":
            note_id = input("Введите ID заметки для редактирования: ")
            edit_note(read_notes(), note_id)
        elif choice == "4":
            note_id = input("Введите ID заметки для удаления: ")
            delete_note(read_notes(), note_id)
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    main()
