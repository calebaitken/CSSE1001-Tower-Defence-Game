"""GUI Elements for the status bar"""

import tkinter as tk

__author__ = "Caleb Aitken"


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
        self.wave_label['text'] = "Wave: " + str(wave) + "/" + str(max_waves)

    def set_score(self, score):
        self.score_label['text'] = str(score)

    def set_coins(self, coins):
        self.coins_label['text'] = str(coins) + " coins"

    def set_lives(self, lives):
        self.lives_label['text'] = str(lives) + " lives"