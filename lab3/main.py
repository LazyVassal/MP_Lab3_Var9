import tkinter as tk
from models import FileManagerModel
from view import FileManagerView
from controller import FileManagerController

if __name__ == '__main__':
    root = tk.Tk()
    model = FileManagerModel()
    view = FileManagerView(root, controller=None) 
    controller = FileManagerController(model, view) 
    
    view.controller = controller 
    
    controller.update_view()
    root.mainloop()