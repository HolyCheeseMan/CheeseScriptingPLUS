def example_command():
    messagebox.showinfo("Plugin", "This is an example plugin.")

example_plugin_button = customtkinter.CTkButton(master=top_frame, text="Example", width=50, height=30, font=("Roboto", 20), command=example_command)
example_plugin_button.pack(side='left', padx=5, pady=0)