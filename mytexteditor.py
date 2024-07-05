import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
        root.title(f"Simple Text Editor - {os.path.basename(file_path)}")
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, tk.END))

def about():
    messagebox.showinfo("About", "Simple Text Editor made by xurshidbro.uz.\n Visit website for more information ")

def undo():
    text_area.edit_undo()

def redo():
    text_area.edit_redo()

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def find():
    find_window = tk.Toplevel(root)
    find_window.title("Find")
    
    tk.Label(find_window, text="Find:").grid(row=0, column=0, padx=4, pady=4)
    find_entry = tk.Entry(find_window)
    find_entry.grid(row=0, column=1, padx=4, pady=4)
    

    def clear_highlight():
        text_area.tag_remove('highlight', '1.0', tk.END)

    def find_text():
        text_area.tag_remove('highlight', '1.0', tk.END)
        find_string = find_entry.get()
        if find_string:
            start_idx = '1.0'
            while True:
                start_idx = text_area.search(find_string, start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(find_string)}c"
                text_area.tag_add('highlight', start_idx, end_idx)
                start_idx = end_idx
            text_area.tag_config('highlight', background='yellow')


    tk.Button(find_window, text="Find", command=find_text).grid(row=0, column=2, padx=4, pady=4)

    find_window.protocol("WM_DELETE_WINDOW", lambda: (clear_highlight(), find_window.destroy()))



root = tk.Tk()
root.title("Notes")

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

#Edit menu
edit_menu=tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find)
menu_bar.add_cascade(label="Edit", menu=edit_menu)


# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create text area
text_area = tk.Text(root, undo=True)
text_area.pack(expand=True, fill='both')

root.mainloop()
