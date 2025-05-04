import tkinter as tk
from tkinter import messagebox

def show_welcome_popup():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    messagebox.showinfo("Welcome to my Cell-o-mat", "The automaton game is starting!")
    root.destroy()
