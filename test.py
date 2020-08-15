try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

def change_case(event=None):
    new_text = str.swapcase(lab["text"])
    lab.config(text=new_text)

def red_text(event=None):
    lab.config(fg="red")

def black_text(event=None):
    lab.config(fg="black")

root = tk.Tk()

lab = tk.Label(root,text="this is a test")

lab.bind("<Button-1>",change_case)
lab.bind("<Enter>",red_text)
lab.bind("<Leave>",black_text)

lab.grid()
root.mainloop()