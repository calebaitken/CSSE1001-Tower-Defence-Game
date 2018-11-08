"""GUI Elements for pop-up windows

Created due to issues with tkinter's built-in messagebox module."""

import tkinter as tk

__author__ = "Caleb Aitken"

class MessageWindow(tk.Toplevel):
    """Displays a pop-up window requiring a user response"""

    def __init__(self, master, title, message, callback1, callback2, size=(298,120), **kwargs):
        """asdf"""

        self.size = size
        self.master = master

        self.width, self.height = width, height = tuple(i for i in self.size)

        tk.Toplevel.__init__(self, master, width=width, height=height, **kwargs)
        self.grab_set()
        self.transient()
        self.pack_propagate(False)
        self.title(title)

        self.message_label = tk.Label(self, text=message)
        self.message_label.pack(side=tk.TOP, expand=True, fill="both")

        self.yes_button = tk.Button(self, text="Yes", width=10, command=lambda:[callback1(),self.destroy()])
        self.yes_button.pack(side=tk.LEFT, expand=True)

        self.no_button = tk.Button(self, text="No", width=10, command=lambda:[callback2(),self.destroy()])
        self.no_button.pack(side=tk.LEFT, expand=True)