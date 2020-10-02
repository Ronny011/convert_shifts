import os
import xl_to_csv
import iterator
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# global variable, could be assigned with a default excel spread-sheet
sheet = None


def gui():
    """
    manages the app interface and logic
    """
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

    def convert_listener(name):
        """
        "convert" button click action
        :param name:worker name
        """
        error_label = Label(root)
        # making sure worker enters his name
        try:
            if len(box.get()) < 2:
                raise NameError("Error: didn't enter name")
            else:
                print("Worker name:", name)
                xl_to_csv.convert(name, sheet)
                lbl_conversion = Label(root, text="Conversion completed")
                lbl_conversion.config(bg="#b7e1ff")
                lbl_conversion.config(fg="#00a505")
                # makes sure labels aren't destroyed if they don't exist
                if lbl_enter_name.winfo_exists():
                    lbl_enter_name.destroy()
                lbl_conversion.grid(row=0, column=0, sticky=W, pady=10, padx=10)
                if error_label.winfo_exists():
                    error_label.destroy()
                response = messagebox.askquestion("Google API", "Upload to calendar?")
                if response:
                    iterator.iterate()
        except NameError as ne:
            error_label = Label(root, text=ne)
            error_label.grid(row=0, column=0, sticky=W, pady=10, padx=10)
            error_label.config(bg="#b7e1ff")
            error_label.config(fg="red")
            if lbl_enter_name.winfo_exists():
                lbl_enter_name.destroy()
            error_label.grid()
            print("error raised - didn't enter name")
            # messagebox.showerror("Error", ne) # alternative - a new windows pops up with an alert

    def browse_listener():
        """
        "browse" button click action
        """
        global sheet
        try:
            sheet = filedialog.askopenfile(initialdir="/convert",
                                           title="Choose a schedule file",
                                           filetypes=(("Excel files", "*.xlsx"),
                                                      # accept all files and excel .xlsx - redundant
                                                      ("all files", "*.*")))
            sheet = os.path.basename(sheet.name)
            print("File name: ", sheet)
            button.state(["!disabled"])  # enable convert button
        except AttributeError:
            print("error raised - didn't choose file")

    # gui elements - buttons, labels, colors and alignment
    lbl_enter_name = Label(root, text="Enter name")
    lbl_enter_name.config(bg="#b7e1ff")
    lbl_enter_name.config(fg="#00a505")
    lbl_enter_name.config(font='-weight bold')
    lbl_enter_name.grid(row=0, column=0, sticky=W, pady=10, padx=10)
    button = ttk.Button(root, text="Convert ➡", command=lambda: convert_listener(box.get()))
    button.grid(row=1, column=0, ipadx=10)
    button.state(["disabled"])
    button2 = ttk.Button(root, text="Browse", command=lambda: browse_listener())
    button2.grid(row=0, column=0)
    box = Entry(root, width=20)
    box.grid(row=1, column=0, sticky=W, pady=10, padx=10)
    root.mainloop()
