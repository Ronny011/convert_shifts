import os
import xl_to_csv
# from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# global variable, could be assigned with a default excel spread-sheet
sheet = 0


def gui():
    # root widget initialization
    root = Tk()
    root.title("Shift converter")
    root.iconbitmap("icon.ico")

    # background setup
    c = Canvas(root, bg="blue", height=150, width=445)
    photo = PhotoImage(file="bg.png")
    background_label = Label(root, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    c.grid(row=0, column=0)

    # convert button click action
    def convert_listener(name):
        # making sure worker enters his name
        try:
            if len(box.get()) < 2:
                raise NameError("Error: didn't enter name")
            else:
                print("Worker name:", name)
                xl_to_csv.convert(name, sheet)
                my_label2 = Label(root, text="Conversion completed")
                my_label2.config(bg="#b7e1ff")
                my_label2.config(fg="#00a505")
                # makes sure labels aren't destroyed if they don't exist
                if my_label.winfo_exists():
                    my_label.destroy()
                my_label2.grid(row=0, column=0, sticky=W, pady=10, padx=10)
                if gui.error_label.winfo_exists():
                    gui.error_label.destroy()
        except NameError as ne:
            gui.error_label = Label(root, text=ne)
            gui.error_label.grid(row=0, column=0, sticky=W, pady=10, padx=10)
            gui.error_label.config(bg="#b7e1ff")
            gui.error_label.config(fg="red")
            if my_label.winfo_exists():
                my_label.destroy()
            gui.error_label.grid()
            print("error raised - didn't enter name")
            # messagebox.showerror("Error", ne) # alternative - a new windows pops up with an alert

    # browse button click action
    def browse_listener():
        global sheet
        sheet = filedialog.askopenfile(initialdir="/convert",
                                       title="Choose a schedule file",
                                       filetypes=(("Excel files", "*.xlsx"),
                                                  ("all files", "*.*")))  # accept all files and excel .xlsx - redundant
        sheet = os.path.basename(sheet.name)
        print("File name: ", sheet)
        button.state(["!disabled"])  # enable convert button

    # gui elements - buttons, labels...
    my_label = Label(root, text="Enter name")
    my_label.config(bg="#b7e1ff")
    my_label.config(fg="#00a505")
    my_label.config(font='-weight bold')
    my_label.grid(row=0, column=0, sticky=W, pady=10, padx=10)
    button = ttk.Button(root, text="Convert ➡", command=lambda: convert_listener(box.get()))
    button.grid(row=1, column=0, ipadx=10)
    button.state(["disabled"])
    button2 = ttk.Button(root, text="Browse", command=lambda: browse_listener())
    button2.grid(row=0, column=0)
    box = Entry(root, width=20)
    box.grid(row=1, column=0, sticky=W, pady=10, padx=10)
    root.mainloop()
