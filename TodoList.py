import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def load_tasks(): 
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        tasks = []
    return tasks

def save_tasks(tasks): 
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

def show_tasks(tasks_listbox, tasks): 
    tasks_listbox.delete(0, tk.END)
    if not tasks:
        tasks_listbox.insert(tk.END, "할 일이 없습니다.")
    else:
        for index, task in enumerate(tasks, start=1):
            formatted_timestamp = task.get('timestamp', '시간 정보 없음')
            tasks_listbox.insert(tk.END, f"{index}. [{task['status']}] {task['description']} ({formatted_timestamp})")

def add_task(entry, tasks_listbox, tasks): 
    description = entry.get()
    if description:
        new_task = {'description': description, 'status': '미완료', 'timestamp': str(datetime.now())}
        tasks.append(new_task)
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("경고", "할 일을 입력하세요.")

def complete_task(tasks_listbox, tasks): 
    try:
        selected_index = tasks_listbox.curselection()[0]
        tasks[selected_index]['status'] = '완료'
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")
 
def delete_task(tasks_listbox, tasks): 
    try:
        selected_index = tasks_listbox.curselection()[0]
        del tasks[selected_index]
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")

def undo_complete_task(tasks_listbox, tasks): 
    try:
        selected_index = tasks_listbox.curselection()[0]
        tasks[selected_index]['status'] = '미완료'
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")

def in_progress_task(tasks_listbox, tasks): 
    try:
        selected_index = tasks_listbox.curselection()[0]
        tasks[selected_index]['status'] = '진행 중'
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")

def edit_task(entry, tasks_listbox, tasks):
    try:
        selected_index = tasks_listbox.curselection()[0]
        new_description = entry.get()
        if new_description:
            tasks[selected_index]['description'] = new_description
            tasks[selected_index]['timestamp'] = str(datetime.now())  # Update timestamp
            save_tasks(tasks)
            show_tasks(tasks_listbox, tasks)
            entry.delete(0, tk.END)
        else:
            messagebox.showwarning("경고", "수정할 내용을 입력하세요.")
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")

def mark_as_important(tasks_listbox, tasks): 
    try:
        selected_index = tasks_listbox.curselection()[0]
        tasks[selected_index]['status'] = '중요'
        save_tasks(tasks)
        show_tasks(tasks_listbox, tasks)
    except IndexError:
        messagebox.showwarning("경고", "할 일을 선택하세요.")

def main():
    tasks = load_tasks()

    window = tk.Tk()
    window.title("TODO 프로그램")

    label = tk.Label(window, text="TODO 프로그램", font=("Helvetica", 16))
    label.pack(pady=10)

    tasks_listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=60, height=20)
    tasks_listbox.pack(pady=10)

    show_tasks(tasks_listbox, tasks)

    entry_font = ("나눔고딕", 12)  
    entry = tk.Entry(window, width=40, font=entry_font)
    entry.pack(pady=10)

    add_button = tk.Button(window, text="추가", command=lambda: add_task(entry, tasks_listbox, tasks))
    add_button.pack(pady=5)

    complete_button = tk.Button(window, text="완료", command=lambda: complete_task(tasks_listbox, tasks))
    complete_button.pack(pady=5)

    undo_complete_button = tk.Button(window, text="미완료로 변경", command=lambda: undo_complete_task(tasks_listbox, tasks))
    undo_complete_button.pack(pady=5)

    in_progress_button = tk.Button(window, text="진행 중", command=lambda: in_progress_task(tasks_listbox, tasks))
    in_progress_button.pack(pady=5)

    edit_button = tk.Button(window, text="수정", command=lambda: edit_task(entry, tasks_listbox, tasks))
    edit_button.pack(pady=5)

    delete_button = tk.Button(window, text="삭제", command=lambda: delete_task(tasks_listbox, tasks))
    delete_button.pack(pady=5)

    important_button = tk.Button(window, text="중요", command=lambda: mark_as_important(tasks_listbox, tasks))
    important_button.pack(pady=5)

    exit_button = tk.Button(window, text="종료", command=window.destroy)
    exit_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()