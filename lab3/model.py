import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class FileManagerModel:
    def __init__(self):
        self.current_path = os.getcwd()
        self.history_file = 'file_manager_history.json'
        self.load_history()

    def list_files(self):
        try:
            return os.listdir(self.current_path)
        except Exception as e:
            return [f"Ошибка доступа: {e}"]

    def change_dir(self, new_path):
        if os.path.isdir(new_path):
            self.current_path = new_path

    def create_folder(self, name):
        try:
            os.mkdir(os.path.join(self.current_path, name))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать папку: {e}")

    def delete_file(self, name):
        path = os.path.join(self.current_path, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить: {e}")

    def copy_file(self, src, dst):
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")

    def move_file(self, src, dst):
        try:
            shutil.move(src, dst)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переместить: {e}")

    def save_history(self):
        data = {'last_path': self.current_path}
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_path = data.get('last_path', os.getcwd())


class FileManagerView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller  # Сохраняем ссылку на контроллер
        self.root.title('Файловый менеджер')
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Открыть папку', command=self.on_open_dir)
        filemenu.add_command(label='Сохранить состояние', command=self.on_save)
        filemenu.add_command(label='Загрузить состояние', command=self.on_load)
        menubar.add_cascade(label='Файл', menu=filemenu)
        
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label='Удалить', command=self.on_delete)
        editmenu.add_command(label='Копировать', command=self.on_copy)
        editmenu.add_command(label='Переместить', command=self.on_move)
        menubar.add_cascade(label='Правка', menu=editmenu)
        
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.path_entry = tk.Entry(self.root)
        self.path_entry.pack(fill='x')
        
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(fill='both', expand=True)
        
        # Создаем фрейм-контейнер для кнопок
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill='x')
        
        # Кнопка "Создать папку" находится ВНУТРИ btn_frame
        self.create_btn = tk.Button(btn_frame, text='Создать папку', command=self.on_create_folder)
        self.create_btn.pack(side='left', padx=2, pady=2)
        
        # Кнопка "Удалить" также находится ВНУТРИ btn_frame
        self.delete_btn = tk.Button(btn_frame, text='Удалить', command=self.on_delete)
        self.delete_btn.pack(side='left', padx=2, pady=2)
        
    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def update_path_entry(self, path):
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def on_open_dir(self):
        self.controller.open_dir()

    def on_save(self):
        self.controller.save_history()

    def on_load(self):
        self.controller.load_history()
        self.controller.update_view() # Обновляем интерфейс после загрузки

    def on_create_folder(self):
        self.controller.create_folder()

    def on_delete(self):
        self.controller.delete_file()

    def on_copy(self):
        self.controller.copy_file()

    def on_move(self):
        self.controller.move_file()
class FileManagerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def open_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.model.change_dir(path)
            self.update_view()
    
    def save_history(self):
        self.model.save_history()
    
    def load_history(self):
        self.model.load_history()
    
    def create_folder(self):
        name = simpledialog.askstring('Создать папку', 'Введите имя папки:')
        if name and name.strip():
            self.model.create_folder(name.strip())
            self.update_view()
    
    def delete_file(self):
        selected = self.view.listbox.curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите файл или папку для удаления.")
            return
        
        name = self.view.listbox.get(selected[0])
        
        if name in ['.', '..']:
            messagebox.showwarning("Ошибка", "Нельзя удалить системные элементы.")
            return

        if messagebox.askyesno("Подтверждение", f"Удалить '{name}'?"):
            self.model.delete_file(name)
            self.update_view()
    
    def copy_file(self):
         # Упрощённая реализация копирования (в ту же папку с префиксом _copy_)
         selected = self.view.listbox.curselection()
         if not selected:
             messagebox.showwarning("Внимание", "Выберите файл или папку для копирования.")
             return

         name = self.view.listbox.get(selected[0])
         if name in ['.', '..']:
             messagebox.showwarning("Ошибка", "Нельзя копировать системные элементы.")
             return

         src = os.path.join(self.model.current_path, name)
         dst = os.path.join(self.model.current_path, f"_copy_{name}")
         self.model.copy_file(src, dst)
         self.update_view()
    
    def move_file(self):
         selected = self.view.listbox.curselection()
         if not selected:
             messagebox.showwarning("Внимание", "Выберите файл или папку для перемещения.")
             return

         name = self.view.listbox.get(selected[0])
         if name in ['.', '..']:
             messagebox.showwarning("Ошибка", "Нельзя перемещать системные элементы.")
             return

         src = os.path.join(self.model.current_path, name)
         dst = os.path.join(self.model.current_path, f"_moved_{name}")
         self.model.move_file(src, dst)
         self.update_view()
    
    def update_view(self):
         files = self.model.list_files()
         self.view.update_listbox(files)
         self.view.update_path_entry(self.model.current_path)

if __name__ == '__main__':
    root = tk.Tk()
    model = FileManagerModel()
    view = FileManagerView(root, controller=None) # Создаем View первым (можно передать None временно)
    controller = FileManagerController(model, view) # Создаем Контроллер
    
    # Теперь передаем готовый контроллер в представление
    view.controller = controller 
    
    # Первоначальное обновление интерфейса
    controller.update_view()
    root.mainloop()