# controller.py
import os
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

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
        self.update_view() # Обновляем интерфейс после загрузки
    
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