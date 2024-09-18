import customtkinter
import os
from pathlib import Path
import winreg
import webbrowser
import ctypes
import tkinter.messagebox as messagebox
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        except Exception as e:
            print(f"Error running as admin: {e}")
            messagebox.showerror("Error", "Failed to elevate to admin.")
            sys.exit()

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x250")
root.minsize(500, 250)
root.title("Uninstaller")

username = os.getenv('USERNAME') or os.getenv('USER')
file_path = Path(f'C:/Users/{username}/AppData/Roaming/HolyCheeseMan/CheeseScriptingPlus/APP/CheeseScriptingPlus.exe')
file_path2 = Path(f'C:/Users/{username}/AppData/Roaming/HolyCheeseMan/CheeseScriptingPlus/APP/CSPICON.ico')

def csplus():
    print("Moving To Browser")
    url = 'https://github.com/HolyCheeseMan/Cheese-Scripting/blob/Main/README.md'
    webbrowser.open(url)

def delete_registry_key():
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CheeseScriptingPlus")
        print("Registry key 'CheeseScriptingPlus' deleted.")
    except FileNotFoundError:
        print("Registry key 'CheeseScriptingPlus' not found.")
    except PermissionError:
        print("Permission error. Run as administrator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def show_loading_animation():
    global loading_label
    loading_label = customtkinter.CTkLabel(master=frame, text="Uninstalling...", font=("Roboto", 40))
    loading_label.pack(pady=40, padx=10)
    
    if file_path.exists():
        file_path.unlink()

    if file_path2.exists():
        file_path2.unlink()
    
    delete_registry_key()
    
    root.after(2000, show_final_message)

def show_final_message():
    loading_label.pack_forget() 
    text = customtkinter.CTkLabel(master=frame, text="Uninstalled.", font=("Roboto", 40))
    text.pack(pady=40, padx=10)
    text2 = customtkinter.CTkLabel(master=frame, text="Thanks for using!", font=("Roboto", 20))
    text2.pack(pady=1, padx=10)

def unistall():
    label.pack_forget()
    button.pack_forget()
    button2.pack_forget()
    show_loading_animation()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=5, padx=5, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Do you want to uninstall Cheese Scripting?", font=("Roboto", 24))
label.pack(pady=16, padx=10)

button = customtkinter.CTkButton(master=frame, text="Uninstall", width=100, height=50, font=("Roboto", 30), command=unistall)
button.pack(pady=20, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Cheese Scripting", width=100, height=35, font=("Roboto", 20), command=csplus)
button2.pack(pady=10, padx=10)

run_as_admin()

root.mainloop()
