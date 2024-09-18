import customtkinter
import os
import subprocess
import ctypes
import webbrowser
import requests
import sys
import tkinter.messagebox as messagebox
import datetime
import winreg
import pythoncom
import win32com.client

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

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

root = customtkinter.CTk()
root.geometry("500x250")
root.minsize(500, 250)
root.title("Installer")

username = os.getenv('USERNAME') or os.getenv('USER')
exe_path = os.path.join(f'C:\\Users\\{username}\\AppData\\Roaming\\HolyCheeseMan\\CheeseScriptingPlus\\APP', 'CheeseScriptingPlus.exe')
destination_folder = os.path.join(f'C:/Users/{username}/AppData/Roaming/HolyCheeseMan/CheeseScriptingPlus/APP/')
os.makedirs(destination_folder, exist_ok=True)

reg_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CheeseScriptingPlus"
app_name = "Cheese Scripting +"
app_version = "1.0.0 - VD18M09Y24"
app_publisher = "Holy Cheese Man"
app_install_location = exe_path
app_uninstall_string = os.path.join(destination_folder, 'Uninstaller.exe')

install_date = datetime.datetime.now().strftime("%Y%m%d")

url_main = "https://github.com/HolyCheeseMan/CheeseScriptingPLUS/raw/refs/heads/Main/APP/CheeseScriptingPlus.exe"
url_uninstaller = "https://github.com/HolyCheeseMan/CheeseScriptingPLUS/raw/refs/heads/Main/APP/Uninstaller.exe"
url_icon = "https://raw.githubusercontent.com/HolyCheeseMan/CheeseScriptingPLUS/refs/heads/Main/APP/CSPICON.ico"

def csplus():
    webbrowser.open('https://github.com/HolyCheeseMan/CheeseScriptingPLUS/blob/Main/README.md')

def download_file(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        raise

estimated_size = 28 * 1024

def create_registry_entry():
    with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_key) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, app_name)
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, app_version)
        winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, app_publisher)
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, app_install_location)
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, app_uninstall_string)
        winreg.SetValueEx(key, "QuietUninstallString", 0, winreg.REG_SZ, app_uninstall_string)
        winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, install_date)
        winreg.SetValueEx(key, "Logo", 0, winreg.REG_SZ, os.path.join(destination_folder, 'CSPICON.ico'))
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, os.path.join(destination_folder, 'CSPICON.ico'))
        winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(destination_folder, 'CSPICON.ico'))
        
        winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)

        winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, estimated_size)

def create_shortcut(target, icon_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_path = os.path.join(os.path.expanduser("~"), "Downloads", "Cheese Scripting +.lnk")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.Description = "Launches Cheese Scripting +"
    if icon_path and os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    shortcut.save()

def show_loading_animation():
    try:
        # Download main executable
        download_file(url_main, os.path.join(destination_folder, 'CheeseScriptingPlus.exe'))

        # Download uninstaller
        download_file(url_uninstaller, os.path.join(destination_folder, 'Uninstaller.exe'))

        # Download the icon
        icon_destination = os.path.join(destination_folder, 'CSPICON.ico')
        download_file(url_icon, icon_destination)

        loading_label.pack_forget()
        global last_label2
        last_label2 = customtkinter.CTkLabel(master=frame, text="Finishing...", font=("Roboto", 40))
        last_label2.pack(pady=40, padx=10)

        # Create registry entry
        create_registry_entry()

        # Create shortcut
        create_shortcut(exe_path, icon_destination)

        # Proceed to final message
        root.after(2000, show_final_message)

    except Exception as e:
        loading_label.pack_forget()
        error_label = customtkinter.CTkLabel(master=frame, text="Installation failed!", font=("Roboto", 24), text_color="red")
        error_label.pack(pady=10, padx=10)

def show_final_message():
    last_label2.pack_forget() 
    last_label = customtkinter.CTkLabel(master=frame, text="Installed.", font=("Roboto", 40))
    last_label.pack(pady=40, padx=10)
    button2 = customtkinter.CTkButton(master=frame, text="Launch App", width=100, height=35, font=("Roboto", 20), command=launch)
    button2.pack(pady=10, padx=10)

def launch():
    try:
        subprocess.run(exe_path, check=True)
        print("Executable launched successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error launching executable: {e}")
    except FileNotFoundError:
        print("Executable not found. Please check the path.")
    root.quit()

def install():
    print("Attempting to run as admin...")
    run_as_admin()
    print("Admin privileges acquired.")
    label.pack_forget()
    button.pack_forget()
    button2.pack_forget()
    global loading_label
    loading_label = customtkinter.CTkLabel(master=frame, text="Installing...", font=("Roboto", 40))
    loading_label.pack(pady=40, padx=10)
    root.after(2000, show_loading_animation)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=5, padx=5, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Do you want to install Cheese Scripting?", font=("Roboto", 24))
label.pack(pady=16, padx=10)

button = customtkinter.CTkButton(master=frame, text="Install", width=100, height=50, font=("Roboto", 30), command=install)
button.pack(pady=20, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Github Page", width=100, height=35, font=("Roboto", 20), command=csplus)
button2.pack(pady=10, padx=10)

root.mainloop()
