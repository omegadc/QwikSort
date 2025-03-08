import tkinter as tk
from tkinter import messagebox

def on_button_click():
    user_text = entry.get()
    messagebox.showinfo("Message", f"You entered: {user_text}")

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("300x150")

# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=5)

# Create an entry widget
entry = tk.Entry(root)
entry.pack(pady=5)

# Create a button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

# Run the application
root.mainloop()
