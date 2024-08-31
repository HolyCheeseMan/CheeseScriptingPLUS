import customtkinter
import tkinter as tk
from tkinter import filedialog
import os

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x500")

root.minsize(1000, 500)
root.resizable(True, True)

root.title("Cheese Scripting+")

username = os.getlogin()

file_path = None  
text_editor = None


def loadfile():
    global file_path, text_editor
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Open File"
    )
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        text_editor.delete(1.0, tk.END)
        text_editor.insert(tk.END, content)

def newfile():
    global file_path, text_editor
    file_path = None  
    label.pack_forget()
    button.pack_forget()
    frame.pack_forget()
    
    editor_frame = customtkinter.CTkFrame(master=root, fg_color="#2e2e2e")
    editor_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    text_editor = tk.Text(
        master=editor_frame,
        wrap='word',
        bg="#2e2e2e",   
        fg='white',     
        insertbackground='white',  
        font=("Consolas", 18) 
    )
    text_editor.pack(side="left", fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(master=editor_frame, command=text_editor.yview)
    scrollbar.pack(side='right', fill='y')
    text_editor.config(yscrollcommand=scrollbar.set)

    scrollbar.config(
        background="#4a4a4a",   
        troughcolor="#2e2e2e",   
        sliderlength=30,        
        width=20,               
        relief="flat"
    )

def savefile():
    global file_path, text_editor
    if file_path:
        with open(file_path, 'w') as file:
            content = text_editor.get(1.0, tk.END)
            content = content.rstrip('\n')  
            file.write(content)
    else:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save As"
        )
        if file_path:
            savefile()

top_frame = customtkinter.CTkFrame(master=root)
top_frame.pack(fill="x", padx=5, pady=5)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=5, padx=5, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Cheese Scripting+", font=("Roboto", 64))
label.pack(pady=16, padx=10)

button = customtkinter.CTkButton(master=frame, text="New File", width=200, height=50, font=("Roboto", 30), command=newfile)
button.pack(pady=40, padx=10)

button = customtkinter.CTkButton(master=frame, text="Load File", width=200, height=50, font=("Roboto", 30), command=loadfile)
button.pack(pady=1, padx=1)

file_menu = tk.Menu(root, tearoff=0)
file_menu.add_command(label="New", command=newfile)
file_menu.add_command(label="Open", command=loadfile)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(root, tearoff=0)
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
edit_menu.add_separator()
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")

file_button = customtkinter.CTkButton(
    master=top_frame, text="File", width=50, height=30, font=("Roboto", 20)
)

file_button.pack(side='left', padx=5, pady=10)
file_button.bind("<Button-1>", lambda event: show_menu(file_menu, event))

edit_button = customtkinter.CTkButton(
    master=top_frame, text="Edit", width=50, height=30, font=("Roboto", 20)
)
edit_button.pack(side='left', padx=5, pady=0)
edit_button.bind("<Button-1>", lambda event: show_menu(edit_menu, event))

view_button = customtkinter.CTkButton(
    master=top_frame, text="View", width=50, height=30, font=("Roboto", 20)
)
view_button.pack(side='left', padx=5, pady=0)
view_button.bind("<Button-1>", lambda event: show_menu(view_menu, event))

button_save = customtkinter.CTkButton(master=top_frame, text="Save", width=50, height=30, font=("Roboto", 20), command=savefile)
button_save.pack(side='right', padx=5, pady=0)

def system():
    customtkinter.set_appearance_mode("system")

def dark():
    customtkinter.set_appearance_mode("dark")

def light():
    customtkinter.set_appearance_mode("light")

view_menu = tk.Menu(root, tearoff=0)
view_menu.add_command(label="System", command=system)
view_menu.add_command(label="Dark", command=dark)
view_menu.add_command(label="Light", command=light)

def show_menu(menu, event):
    menu.tk_popup(event.x_root, event.y_root)

root.mainloop()
