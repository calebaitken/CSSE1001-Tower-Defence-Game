"""GUI Elements for the side bar"""

import tkinter as tk

__author__ = "Caleb Aitken"

class PlayControls(tk.Frame):
    """Displays play control buttons for the user to interact with"""

    def __init__(self, master, wave, playpause, size=(280,30), **kwargs):
        """asdf"""

        self.size = size
        self.master = master
        self._enabled = True

        self.width, self.height = width, height = tuple(i for i in self.size)

        tk.Frame.__init__(self, master, width=width, height=height, **kwargs)
        self.pack_propagate(False)

        self.wave_button = tk.Button(self, text='Next Wave', command=wave)
        self.wave_button.pack(side=tk.LEFT, expand=True, anchor=tk.E)

        self.playpause_button = tk.Button(self, text='Pause', command=playpause)
        self.playpause_button.pack(side=tk.LEFT, expand=True, anchor=tk.W)

    def set_playpause(self, text):
        self.playpause_button['text'] = text

    def toggle_enabled(self, enabled=None, wave=True):
        if enabled is None:
            enabled = not self._enabled

        if not enabled:
            self.playpause_button['state'] = "disabled"
            self.wave_button['state'] = "disabled"
        else:
            self.playpause_button['state'] = "normal"
            self.wave_button['state'] = "normal"

        if not wave:
            self.wave_button['state'] = "disabled"

        self._enabled = enabled


class StatusBar(tk.Frame):
    """Displays information to the user about their status in the game"""

    def __init__(self, master, size=(280,75), **kwargs):
        """
        Constructs a status bar
        """

        self.size = size
        self.coins = tk.PhotoImage(file="images\coins.gif")
        self.heart = tk.PhotoImage(file="images\heart.gif")

        self.width, self.height = width, height = tuple(i for i in self.size)

        tk.Frame.__init__(self, master, width=width, height=height, **kwargs)
        self.pack_propagate(False)

        self.wave_label = tk.Label(self, text="")
        self.wave_label.pack(side=tk.TOP, expand=True)

        self.score_label = tk.Label(self, text="")
        self.score_label.pack(side=tk.TOP, expand=True)

        self.coins_image = tk.Label(self, image=self.coins)
        self.coins_label = tk.Label(self, text="")
        self.coins_image.pack(side=tk.LEFT)
        self.coins_label.pack(side=tk.LEFT, expand=True, anchor=tk.W)

        self.lives_image = tk.Label(self, image=self.heart)
        self.lives_label = tk.Label(self, text="")
        self.lives_image.pack(side=tk.LEFT)
        self.lives_label.pack(side=tk.LEFT, expand=True, anchor=tk.W)

    def set_wave(self, wave, max_waves):
        self.wave_label['text'] = "Wave: " + str(int(wave)) + "/" + str(int(max_waves))

    def set_score(self, score):
        self.score_label['text'] = str(int(score))

    def set_coins(self, coins):
        self.coins_label['text'] = str(int(coins)) + " coins"

    def set_lives(self, lives):
        self.lives_label['text'] = str(int(lives)) + " lives"