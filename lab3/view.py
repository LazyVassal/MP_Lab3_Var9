# view.py
import tkinter as tk
from tkinter import filedialog, simpledialog

class FileManagerView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
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
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill='x')
        
        self.create_btn = tk.Button(btn_frame, text='Создать папку', command=self.on_create_folder)
        self.create_btn.pack(side='left', padx=2, pady=2)
        
        self.delete_btn = tk.Button(btn_frame, text='Удалить', command=self.on_delete)
        self.delete_btn.pack(side='left', padx=2, pady=2)
    
    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def update_path_entry(self, path):
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    # Обработчики событий (вызывают методы контроллера)
    def on_open_dir(self): self.controller.open_dir()
    def on_save(self): self.controller.save_history()
    def on_load(self): self.controller.load_history()
    def on_create_folder(self): self.controller.create_folder()
    def on_delete(self): self.controller.delete_file()
    def on_copy(self): self.controller.copy_file()
    def on_move(self): self.controller.move_file()