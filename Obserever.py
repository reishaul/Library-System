import tkinter as tk
from tkinter import  messagebox
"""
Displays a notification message using a popup window. The function creates a temporary hidden Tkinter root window,
uses a messagebox to show the provided message, and then destroys the root window to prevent lingering processes.
"""

def notify(self, message: str):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Notification", message)
    root.destroy()
