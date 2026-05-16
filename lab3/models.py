# models.py
import os
import json
import shutil
import tkinter.messagebox as messagebox

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