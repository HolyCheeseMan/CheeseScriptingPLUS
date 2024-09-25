import sys
import time
import customtkinter
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from tkinter import simpledialog
import subprocess
import webbrowser
import requests

message_shown = False
message_shown_java = False


try:
    username = os.getlogin()
except Exception as e:
    print(f"Error getting username: {e}")
    username = "DefaultUser"


preferences_dir = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP"
preferences_user_dir = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus"
preferences_file = os.path.join(preferences_user_dir, "userpreferences.csp")
version_current_file = "VD25M09Y24"

destination_installer = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\Installer.bat"

print(fr"Checking for {destination_installer}")
if os.path.exists(destination_installer):
    os.unlink(destination_installer)
else:
    print(f"{destination_installer} does not exist.")


os.makedirs(preferences_dir, exist_ok=True)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x500")
root.minsize(1000, 500)
root.resizable(True, True)
root.title("Cheese Scripting+")

file_path = None  
text_editor = None

def load_preferences():
    if os.path.exists(preferences_file):
        with open(preferences_file, 'r') as file:
            lines = file.readlines()
            mode = "dark"
            for line in lines:
                if "mode =" in line:
                    mode = line.split('=')[1].strip().strip('*')
                elif "file =" in line:
                    last_file = line.split('=')[1].strip().strip('*')
                    if os.path.exists(last_file):
                        load_last_file(last_file)
            customtkinter.set_appearance_mode(mode)
            update_text_editor_colors(mode)
    per_path = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\userpreferences.csp"
    if os.path.exists(per_path):
        print("Path Exists")
    else:
        info_csp()


def save_preferences(mode, last_file=None):
    with open(preferences_file, 'w') as file:
        file.write("< CSP ADMIN >\n")
        file.write("user-preference {\n")
        file.write("\tappearance {\n")
        file.write(f"\t\tmode = *{mode}*\n")
        file.write("\t}\n")
        if last_file:
            file.write("\tlast_opened_file {\n")
            file.write(f"\t\tfile = *{last_file}*\n")
            file.write("\t}\n")
        file.write("}\n")

def load_last_file(last_file):
    global file_path, text_editor
    file_path = last_file
    if text_editor is None:
        newfile()
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        text_editor.delete(1.0, tk.END)
        text_editor.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load last opened file: {e}")

def search():
    def perform_search():
        search_term = entry.get()
        if search_term:
            text_editor.tag_remove("highlight", 1.0, tk.END) 
            start_index = text_editor.search(search_term, 1.0, tk.END)
            if start_index:
                end_index = f"{start_index}+{len(search_term)}c"
                text_editor.tag_add("highlight", start_index, end_index)
                text_editor.tag_config("highlight", background="orange")
                text_editor.mark_set("insert", end_index) 
                text_editor.see("insert") 
            else:
                messagebox.showinfo("Not Found", f"'{search_term}' not found.")
        
        if start_index is not None:
            search_window.destroy()

    search_window = customtkinter.CTkToplevel(root)
    search_window.title("Search")
    search_window.geometry("500x150")
    search_window.attributes("-topmost", True)

    label = customtkinter.CTkLabel(search_window, text="Enter text to search:", font=("Roboto", 24))
    label.pack(pady=10)

    entry = customtkinter.CTkEntry(search_window, width=300, font=("Roboto", 18))
    entry.pack(pady=10)

    search_button = customtkinter.CTkButton(search_window, text="Search", command=perform_search, font=("Roboto", 16), width=100, height=40)
    search_button.pack(pady=10)

    entry.focus_set()


def loadfile():
    global file_path, text_editor
    if text_editor is None:
        newfile()
    file_path = filedialog.askopenfilename(
        defaultextension=".",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"), 
                       ("Batch Files", "*.bat"), 
                       ("Powershell Files", "*.ps1"),
                       ("Python Files", "*.py"), 
                       ("JavaScript Files", "*.js"), 
                       ("Java Files", "*.java"), 
                       ("C# Files", "*.cs"), 
                       ("Lua Files", "*.lua")],
            initialdir = fr"C:\Users\{username}\Downloads",
        title="Open File"
    )
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, content)
            save_preferences(customtkinter.get_appearance_mode(), file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

def newfile():
    global file_path, text_editor
    file_path = None
    if text_editor:
        text_editor.delete(1.0, tk.END)
    if text_editor is None:
        editor_frame = customtkinter.CTkFrame(master=root, fg_color="#2e2e2e")
        editor_frame.pack(pady=10, padx=20, fill="both", expand=True)

        text_editor = tk.Text(
            master=editor_frame,
            wrap='word',
            bg="#2e2e2e",
            fg='white',
            insertbackground='white',
            font=("Consolas", 18),
            undo=True
        )
        text_editor.pack(side="left", fill='both', expand=True)

        scrollbar = tk.Scrollbar(master=editor_frame, command=text_editor.yview)
        scrollbar.pack(side='right', fill='y')
        text_editor.config(yscrollcommand=scrollbar.set)
        scrollbar.config(
            background="#4a4a4a",
            troughcolor="#2e2e2e",
            width=20,
            relief="flat"
        )
    
    show_new()


def savefile():
    global file_path, text_editor
    if text_editor is None:
        messagebox.showerror("Error", "No file open. Please create or load a file first.")
        return
    content = text_editor.get(1.0, tk.END).strip()

    if file_path:
        with open(file_path, 'w') as file:
            if content:
                file.write(content)
                save_preferences(customtkinter.get_appearance_mode(), file_path)
                show_tick()
            else:
                messagebox.showerror("Error", "No content to save.")
    else:
        if content == "":
            messagebox.showerror("Error", "No content to save. Please create or load a file first.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"), 
                       ("Batch Files", "*.bat"), 
                       ("Powershell Files", "*.ps1"), 
                       ("Python Files", "*.py"), 
                       ("JavaScript Files", "*.js"), 
                       ("Java Files", "*.java"), 
                       ("C# Files", "*.cs"), 
                       ("Lua Files", "*.lua")],
            title="Save As"
        )
        if file_path:
            savefile()

def show_tick():
    tick_label.configure(text="✔")
    tick_label.after(1000, clear_tick)

def clear_tick():
    tick_label.configure(text="")

def show_new():
    new_label.configure(text="</>")
    new_label.after(1000, clear_new)

def clear_new():
    new_label.configure(text="")

def undo():
    if text_editor:
        text_editor.event_generate("<<Undo>>")

def redo():
    if text_editor:
        text_editor.event_generate("<<Redo>>")

def cut():
    if text_editor:
        text_editor.event_generate("<<Cut>>")

def copy():
    if text_editor:
        text_editor.event_generate("<<Copy>>")

def paste():
    if text_editor:
        text_editor.event_generate("<<Paste>>")

def update_text_editor_colors(mode):
    if mode == "Light":
        text_editor.config(bg="white", fg="black", insertbackground="black")
    else:
        if mode == "light":
            text_editor.config(bg="white", fg="black", insertbackground="black")
        else:
            text_editor.config(bg="#2e2e2e", fg="white", insertbackground="white")

def dark():
    mode = "dark"
    customtkinter.set_appearance_mode(mode)
    update_text_editor_colors(mode)
    save_preferences(mode, file_path)

def light():
    mode = "light"
    customtkinter.set_appearance_mode(mode)
    update_text_editor_colors(mode)
    save_preferences(mode, file_path)



def show_menu(menu, event):
    menu.tk_popup(event.x_root, event.y_root)

def r_Batch():
    print(file_path)
    subprocess.Popen([file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def r_Powershell():
    powershell_path = fr'C:\Windows\System32\WindowsPowerShell\v1.0\Powershell.exe'
    print(file_path)
    print(powershell_path)
    subprocess.Popen([powershell_path, file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def r_Python():
    global message_shown
    global python_path
    print(file_path)
    if not message_shown:
        messagebox.showinfo("Python.exe Location", "Your python/python.exe location is needed to run this .py file.")
        message_shown = True
        initial_dir = fr'C:\Users\{username}\AppData\Local\Programs'
        python_path = filedialog.askopenfilename(
            defaultextension=".exe",
                filetypes=[("Python Executable", "*.exe*")],
                initialdir=initial_dir,
            title="Use File"
        )
    subprocess.Popen([python_path, file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def r_Javascript():
    global message_shown_java
    global java_path
    print(file_path)
    if not message_shown_java:
        messagebox.showinfo("Node.exe Location", "Your Nodejs/Node.exe location is needed to run this .js file.")
        message_shown_java = True
        initial_dir = fr'C:\Program Files'
        java_path = filedialog.askopenfilename(
            defaultextension=".exe",
                filetypes=[("Javascript Executable", "*.exe*")],
                initialdir=initial_dir,
            title="Use File"
        )
    subprocess.Popen([java_path, file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def r_Html():
    print(file_path)
    webbrowser.open(f'file:///{file_path}')

def template_check():
    global file_path
    print("Checking Templates")

    folder_path_check = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\Template"

    if os.path.isdir(folder_path_check):
        print("The folder exists.")
        initial_dir = folder_path_check
        file_path = filedialog.askopenfilename(
            defaultextension=".",
                filetypes=[("All Files", "*.*")],
                initialdir=initial_dir,
            title="Use File"
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                text_editor.delete(1.0, tk.END)
                text_editor.insert(tk.END, content)
                save_preferences(customtkinter.get_appearance_mode(), file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
        
    else:
        print("The folder does not exist.")
        template_window = customtkinter.CTkToplevel(root)
        template_window.title("Templates")
        template_window.geometry("650x150")
        template_window.attributes("-topmost", True)
        label_file_template = customtkinter.CTkLabel(template_window, text="Whoops! Looks like you don't have the templates installed!", font=("Roboto", 24))
        label_file_template.pack(pady=10)
        button_file_template = customtkinter.CTkButton(template_window, text="Install", font=("Roboto", 24), command=lambda: template_install_web(template_window))
        button_file_template.pack(pady=30)

def template_install_web(template_window):
    destination_folder = os.path.join(f'C:/Users/{username}/AppData/Roaming/HolyCheeseMan/CheeseScriptingPlus/APP/Template/')
    os.makedirs(destination_folder, exist_ok=True)
    print("Moving To Browser")
    template_window.destroy()
    urls = {
        'Batch.bat': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/Template/Batch.bat',
        'html.html': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/Template/html.html',
        'JavaScript.js': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/Template/JavaScript.js',
        'Python.py': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/Template/Python.py',
    }
    for filename, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(destination_folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {filename}: {response.status_code}")
            messagebox.showerror("Error", f"Failed to download {filename}: {response.status_code}")
    messagebox.showinfo("Templates", "The Template files have completed installation.")


def info_csp():
    global file_path
    file_path = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP\info.csp"
    if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                text_editor.delete(1.0, tk.END)
                text_editor.insert(tk.END, content)
                save_preferences(customtkinter.get_appearance_mode(), file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load info: {e}")

def github_page():
    webbrowser.open('https://github.com/HolyCheeseMan/CheeseScriptingPLUS/')
    
def reset_preferences():
    per_path = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\userpreferences.csp"
    if os.path.exists(per_path):
        os.remove(per_path)
        messagebox.showinfo("Success", "Preferences have been reset to default --> restart recommended")
    else:
        messagebox.showerror("Error", "You do not have preferences yet.")

def check_for_update():
    current = os.path.join(preferences_dir, "current.cspdata")
    cur_ver = os.path.join(preferences_dir, "cur_ver.cspdata")
    destination_folder = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP"
    with open(current, 'w') as file:
        file.write(version_current_file)
    urls = {
        'cur_ver.cspdata': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/cur_ver.cspdata',
    }
    for filename, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(destination_folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")

    with open(current, 'r') as file:
        local_current_version = file.read().strip()

    with open(cur_ver, 'r') as file:
        latest_version = file.read().strip()

    if local_current_version == latest_version:
        current_version_window = customtkinter.CTkToplevel(root)
        current_version_window.title(f"No Updates Needed, Current Version: {local_current_version}")
        current_version_window.geometry("650x150")
        current_version_window.attributes("-topmost", True)
        current_label = customtkinter.CTkLabel(current_version_window, text="Looks like you're up to date!", font=("Roboto", 26))
        current_label.pack(pady=5)
        version_label = customtkinter.CTkLabel(current_version_window, text=f"Your Version: {local_current_version}", font=("Roboto", 20))
        version_label.pack(pady=15)
        server_version_label = customtkinter.CTkLabel(current_version_window, text=f"Latest Version: {latest_version}", font=("Roboto", 20))
        server_version_label.pack(pady=1)
        print(fr"No Updates Needed - {local_current_version}")
    else:
        update_window = customtkinter.CTkToplevel(root)
        update_window.title(fr"Update Available: {latest_version}")
        update_window.geometry("650x150")
        update_window.attributes("-topmost", True)
        update_label = customtkinter.CTkLabel(update_window, text=fr"Looks like there's an update available! ({latest_version})", font=("Roboto", 24))
        update_label.pack(pady=10)
        version_label = customtkinter.CTkLabel(update_window, text=f"Your Version: {local_current_version}", font=("Roboto", 20))
        version_label.pack(pady=10)
        install_button = customtkinter.CTkButton(update_window, text="Install", font=("Roboto", 24), command=lambda: install_new_version(update_window))
        install_button.pack(pady=1)
        print(fr"Updates Needed - Current:{local_current_version}, Needed:{latest_version}")

    if os.path.exists(cur_ver):
        os.unlink(cur_ver)
        print(f"Cleared {cur_ver}")
    else:
        print(f"{cur_ver} does not exist, nothing to clear.")

def check_for_update_silent():
    current = os.path.join(preferences_dir, "current.cspdata")
    cur_ver = os.path.join(preferences_dir, "cur_ver.cspdata")
    destination_folder = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\APP"
    with open(current, 'w') as file:
        file.write(version_current_file)
    urls = {
        'cur_ver.cspdata': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/cur_ver.cspdata',
    }
    for filename, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(destination_folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")

    with open(current, 'r') as file:
        local_current_version = file.read().strip()

    with open(cur_ver, 'r') as file:
        latest_version = file.read().strip()

    if local_current_version == latest_version:
        print(fr"No Updates Needed, Current Version: {local_current_version}")
    else:
        print("Updates Needed.")
        update_window = customtkinter.CTkToplevel(root)
        update_window.title(fr"Update Available: {latest_version}")
        update_window.geometry("650x150")
        update_window.attributes("-topmost", True)
        update_label = customtkinter.CTkLabel(update_window, text=fr"Looks like there's an update available! ({latest_version})", font=("Roboto", 24))
        update_label.pack(pady=10)
        version_label = customtkinter.CTkLabel(update_window, text=f"Your Version: {local_current_version}", font=("Roboto", 20))
        version_label.pack(pady=10)
        install_button = customtkinter.CTkButton(update_window, text="Install", font=("Roboto", 24), command=lambda: install_new_version(update_window))
        install_button.pack(pady=1)
        print(fr"Updates Needed - Current:{local_current_version}, Needed:{latest_version}")

    if os.path.exists(cur_ver):
        os.unlink(cur_ver)
        print(f"Cleared {cur_ver}")
    else:
        print(f"{cur_ver} does not exist, nothing to clear.")

def installation_location():
    directory = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus"
    os.startfile(directory)

def install_new_version(update_window):
    update_window.destroy()
    print("Installing New Version")
    urls = {
        'Installer.bat': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/Installer.bat',
    }
    destination_folder = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus"
    destination_installer = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\Installer.bat"
    for filename, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(destination_folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
    if os.path.exists(destination_installer):
        subprocess.Popen([destination_installer], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
    else:
        print(f"{destination_installer} does not exist, failed.")
        messagebox.showerror("Error", "Installation failed, try installing manually or check internet.")
        

top_frame = customtkinter.CTkFrame(master=root)
top_frame.pack(fill="x", padx=5, pady=5)

file_menu = tk.Menu(root, tearoff=0)
file_menu.add_command(label="New", command=newfile)
file_menu.add_command(label="Save", command=savefile)
file_menu.add_command(label="Open", command=loadfile)
file_menu.add_command(label="Templates", command=template_check)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(root, tearoff=0)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_command(label="Search", command=search)

run_menu = tk.Menu(root, tearoff=0)
run_menu.add_command(label="Run:", state=tk.DISABLED)
run_menu.add_command(label="Python", command=r_Python)
run_menu.add_command(label="JavaScript", command=r_Javascript)
run_menu.add_command(label="Html", command=r_Html)
run_menu.add_separator()
run_menu.add_command(label="System:", state=tk.DISABLED)
run_menu.add_command(label="Batch", command=r_Batch)
run_menu.add_command(label="Powershell", command=r_Powershell)

help_menu = tk.Menu(root, tearoff=0)
help_menu.add_command(label="Info", command=info_csp)
help_menu.add_command(label="Github", command=github_page)
help_menu.add_command(label="Check For Updates", command=check_for_update)
help_menu.add_command(label="Templates", command=template_check)
help_menu.add_separator()
help_menu.add_command(label="Reset Preferences", command=reset_preferences)
help_menu.add_command(label="Installation Location", command=installation_location)

root.bind('<Control-n>', lambda event: newfile())
root.bind('<Control-o>', lambda event: loadfile())
root.bind('<Control-s>', lambda event: savefile())
root.bind('<Control-z>', lambda event: undo())
root.bind('<Control-y>', lambda event: redo())
root.bind('<Control-f>', lambda event: search())
root.bind('<Control-r>', lambda event: show_menu(run_menu, event))
root.bind('<Control-Shift-T>', lambda event: template_check())
root.bind('<Control-equal>', lambda event: change_font_size(2))
root.bind('<Control-minus>', lambda event: change_font_size(-2))

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

run_button = customtkinter.CTkButton(
    master=top_frame, text="Run", width=50, height=30, font=("Roboto", 20)
)
run_button.pack(side='left', padx=5, pady=0)
run_button.bind("<Button-1>", lambda event: show_menu(run_menu, event))

help_button = customtkinter.CTkButton(
    master=top_frame, text="Help", width=50, height=30, font=("Roboto", 20)
)
help_button.pack(side='left', padx=5, pady=0)
help_button.bind("<Button-1>", lambda event: show_menu(help_menu, event))

def change_font_size(delta):
    current_font = text_editor['font']
    current_size = int(current_font.split()[1])
    new_size = max(8, current_size + delta)
    text_editor.config(font=("Consolas", new_size))


view_menu = tk.Menu(root, tearoff=0)
view_menu.add_command(label="Appearance:", state=tk.DISABLED)
view_menu.add_command(label="Dark", command=dark)
view_menu.add_command(label="Light", command=light)
view_menu.add_separator()
view_menu.add_command(label="Zoom In", command=lambda: change_font_size(2))
view_menu.add_command(label="Zoom Out", command=lambda: change_font_size(-2))



label = customtkinter.CTkLabel(master=top_frame, text="Cheese Scripting+", font=("Roboto", 25))
label.pack(side='left', padx=5, pady=10)

button_save = customtkinter.CTkButton(master=top_frame, text="Save", width=50, height=30, font=("Roboto", 20), command=savefile)
button_save.pack(side='right', padx=5, pady=0)

editor_frame = customtkinter.CTkFrame(master=root, fg_color="#2e2e2e")
editor_frame.pack(pady=10, padx=20, fill="both", expand=True)

text_editor = tk.Text(
    master=editor_frame,
    wrap='word',
    bg="#2e2e2e",
    fg='white',
    insertbackground='white',
    font=("Consolas", 18),
    undo=True
)
text_editor.pack(side="left", fill='both', expand=True)

scrollbar = tk.Scrollbar(master=editor_frame, command=text_editor.yview)
scrollbar.pack(side='right', fill='y')
text_editor.config(yscrollcommand=scrollbar.set)
scrollbar.config(
    background="#4a4a4a",
    troughcolor="#2e2e2e",
    width=20,
    relief="flat"
)

def set_current(path):
        global current
        current = path
        print(f"Selected plugin: {current}")
        execute_script(path)

def execute_script(path):
        print(fr"Executing {path}")
        with open(current, 'r') as file:
            script_plugin = file.read().strip()

        print("\n", script_plugin)

        try:
            exec(script_plugin)
        except Exception as e:
            print(f"Error running the code: {e}")
            messagebox.showerror("Error", f"Error running the code/plugin: {e}")

def plugins():

    try:
        username = os.getlogin()
    except Exception as e:
        print(f"Error getting username: {e}")
        username = "DefaultUser"

    plugin_folder = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\Plugins"
    global current
    current = ""

    destination_example = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\Plugins\Example_Plugin.py"

    print(fr"Checking for {destination_example}")
    if os.path.exists(destination_example):
        print(fr"Plugin Exists: {destination_example}")
    else:
        print(f"{destination_example} does not exist.")
        urls = {
            'Example_Plugin.py': 'https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/Plugins/Example_Plugin.py',
        }
        destination_folder = fr"C:\Users\{username}\AppData\Roaming\HolyCheeseMan\CheeseScriptingPlus\Plugins"
        for filename, url in urls.items():
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(destination_folder, filename), 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {filename}")

    root_plugin = customtkinter.CTkToplevel(root)
    root_plugin.geometry("300x500")
    root_plugin.minsize(300, 500)
    root_plugin.resizable(False, False)
    root_plugin.title("Plugin Executor")
    root_plugin.attributes("-topmost", True)

    os.makedirs(plugin_folder, exist_ok=True)

    def list_plugins():
        print("Listing Plugins")
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        try:
            plugin_files = os.listdir(plugin_folder)
        except Exception as e:
            print(f"Error listing plugins: {e}")
            plugin_files = []

        for plugin in plugin_files:
            plugin_path = os.path.join(plugin_folder, plugin)
            button = customtkinter.CTkButton(master=scrollable_frame, text=plugin, width=250, font=("Roboto", 16), command=lambda p=plugin_path: set_current(p))
            button.pack(pady=5)

    def installation_location_plugin():
        directory = (plugin_folder)
        os.startfile(directory)

    top_frame_plugin = customtkinter.CTkFrame(master=root_plugin)
    top_frame_plugin.pack(fill="x", padx=5, pady=5)

    refresh_button = customtkinter.CTkLabel(top_frame_plugin, text="Plugin Executor", width=10, height=10, font=("Roboto", 20))
    refresh_button.pack(side="left", padx=5, pady=5)

    refresh_button = customtkinter.CTkButton(top_frame_plugin, text="⟳", width=10, height=10, font=("Roboto", 20), command=list_plugins)
    refresh_button.pack(side="right", padx=5, pady=5)

    refresh_button = customtkinter.CTkButton(top_frame_plugin, text="🗀", width=10, height=10, font=("Roboto", 20), command=installation_location_plugin)
    refresh_button.pack(side="right", padx=1, pady=5)

    scrollable_frame = customtkinter.CTkScrollableFrame(master=root_plugin, width=250, height=450)
    scrollable_frame.pack(padx=5, pady=5)

    list_plugins()

plugin_button = customtkinter.CTkButton(master=top_frame, text="Plugins", width=50, height=30, font=("Roboto", 20), command=plugins)
plugin_button.pack(side='right', padx=5, pady=0)

tick_label = customtkinter.CTkLabel(master=top_frame, text="", font=("Roboto", 20), text_color="green")
tick_label.pack(side='right', padx=5, pady=10)

new_label = customtkinter.CTkLabel(master=top_frame, text="", font=("Roboto", 20), text_color="grey")
new_label.pack(side='right', padx=5, pady=10)

load_preferences()
check_for_update_silent()
root.mainloop()