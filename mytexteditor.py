import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, font
from tkinter import messagebox
import os


#FUNCTIONS

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


def change_font():
    font_window = tk.Toplevel(root)
    font_window.title("Choose Font")

    tk.Label(font_window, text="Select Font:").pack(padx=10, pady=10)

    font_list = ['Arial', 'Courier New', 'Comic Sans MS', 'Fixedsys', 'MS Sans Serif', 'MS Serif', 'Symbol', 'System', 'Times New Roman', 'Verdana']
    listbox = tk.Listbox(font_window, selectmode=tk.SINGLE)
    listbox.pack(padx=10, pady=10)

    
    for item in font_list:
        listbox.insert(tk.END, item)

    def set_font():
        selected_font = listbox.get(tk.ACTIVE)
        if selected_font:
            current_font = font.Font(font=text_area['font'])
            current_font.config(family=selected_font)
            text_area.config(font=current_font)
        font_window.destroy()
    
    tk.Button(font_window, text="Apply", command=set_font).pack(padx=10, pady=10)


def change_font_size():
    size_choice = simpledialog.askinteger("Font Size", "Enter font size:", minvalue=1, maxvalue=100)
    if size_choice:
        current_font = font.Font(font=text_area['font'])
        current_font.config(size=size_choice)
        text_area.config(font=current_font)


def change_text_color():
    color_choice = colorchooser.askcolor(title="Choose text color")
    if color_choice:
        text_area.config(fg=color_choice[1])


def toggle_bold():
    current_font = font.Font(font=text_area['font'])
    if current_font.actual()['weight'] == 'normal':
        current_font.config(weight='bold')
    else:
        current_font.config(weight='normal')
    text_area.config(font=current_font)


def toggle_italic():
    current_font = font.Font(font=text_area['font'])
    if current_font.actual()['slant'] == 'roman':
        current_font.config(slant='italic')
    else:
        current_font.config(slant='roman')
    text_area.config(font=current_font)


def toggle_underline():
    current_font = font.Font(font=text_area['font'])
    if current_font.actual()['underline'] == 0:
        current_font.config(underline=1)
    else:
        current_font.config(underline=0)
    text_area.config(font=current_font)


def update_status(event=None):
    row, col = text_area.index(tk.INSERT).split('.')
    chars = len(text_area.get(1.0, tk.END)) - 1
    status_bar.config(text=f"Row: {row} | Column: {col}")
    word_count_label.config(text=f"Characters: {chars}")




root = tk.Tk()
root.title("Notes")
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


#   MENUBAR

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)


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


format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Font", command=change_font)
format_menu.add_command(label="Font Size", command=change_font_size)
format_menu.add_command(label="Text Color", command=change_text_color)
format_menu.add_separator()
format_menu.add_command(label="Bold", command=toggle_bold)
format_menu.add_command(label="Italic", command=toggle_italic)
format_menu.add_command(label="Underline", command=toggle_underline)
menu_bar.add_cascade(label="Format", menu=format_menu)


help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)


text_area = tk.Text(root, undo=True)
text_area.pack(expand=True, fill='both')
text_area.bind('<KeyRelease>', update_status)


status_frame = tk.Frame(root)
status_frame.pack(side='bottom', fill='x')

status_bar = tk.Label(status_frame, text="Row: 1 | Column: 0", anchor='w')
status_bar.pack(side='left')

word_count_label = tk.Label(status_frame, text="Characters: 0", anchor='e')
word_count_label.pack(side='right')


root.mainloop()
