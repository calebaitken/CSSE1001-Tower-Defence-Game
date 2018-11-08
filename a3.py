import tkinter as tk

from model import TowerGame
from tower import SimpleTower, MissileTower
from enemy import SimpleEnemy
from utilities import Stepper
from view import GameView
from level import AbstractLevel

from a3_side_bar import StatusBar, PlayControls
from a3_message_window import MessageWindow

BACKGROUND_COLOUR = "#4a2f48"

__author__ = "Caleb Aitken"
__copyright__ = ""


# Could be moved to a separate file, perhaps levels/simple.py, and imported
class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 20

    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave_n (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order
        """
        enemies = []

        if wave == 1:
            # A hardcoded singleton list of (step, enemy) pairs

            enemies = [(10, SimpleEnemy())]
        elif wave == 2:
            # A hardcoded list of multiple (step, enemy) pairs

            enemies = [(10, SimpleEnemy()), (15, SimpleEnemy()), (30, SimpleEnemy())]
        elif 3 <= wave < 10:
            # List of (step, enemy) pairs spread across an interval of time (steps)

            steps = int(40 * (wave ** .5))  # The number of steps to spread the enemies across
            count = wave * 2  # The number of enemies to spread across the (time) steps

            for step in self.generate_intervals(steps, count):
                enemies.append((step, SimpleEnemy()))

        elif wave == 10:
            # Generate sub waves
            sub_waves = [
                # (steps, number of enemies, enemy constructor, args, kwargs)
                (50, 10, SimpleEnemy, (), {}),  # 10 enemies over 50 steps
                (100, None, None, None, None),  # then nothing for 100 steps
                (50, 10, SimpleEnemy, (), {})  # then another 10 enemies over 50 steps
            ]

            enemies = self.generate_sub_waves(sub_waves)

        else:  # 11 <= wave <= 20
            # Now it's going to get hectic

            sub_waves = [
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    SimpleEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                # ...
            ]
            enemies = self.generate_sub_waves(sub_waves)

        return enemies


class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None

    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """

        self._master = master
        super().__init__(master, delay=delay)

        self._game = game = TowerGame()

        self.setup_menu()

        # create a game view and draw grid borders
        self._view = view = GameView(master, size=game.grid.cells,
                                     cell_size=game.grid.cell_size,
                                     bg='antique white')
        view.pack(side=tk.LEFT, expand=True)

        self.sidebar_container = tk.Frame(master)
        self.sidebar_container.pack(side=tk.LEFT, expand=True, fill='both')

        # Task 1.3 (Status Bar): instantiate status bar
        self._statusbar = statusbar = StatusBar(self.sidebar_container)
        statusbar.pack(side=tk.TOP, anchor=tk.N)

        # Task 1.5 (Play Controls): instantiate widgets here
        self._play_controls = playcontrols = PlayControls(self.sidebar_container, self.next_wave, self._toggle_paused)
        playcontrols.pack(side=tk.BOTTOM, anchor=tk.S)

        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # Task 1.2 (Tower Placement): bind mouse events to canvas here
        self._view.bind("<Button-1>", self._left_click)
        self._view.bind("<Motion>", self._move)
        self._view.bind("<Leave>", self._mouse_leave)
        self._view.bind("<Button-2>", self._sell_tower)
        self._view.bind("<Button-3>", self._sell_tower)

        # Level
        self._level = MyLevel()

        self.select_tower(SimpleTower)

        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()

    def setup_menu(self):
        # Task 1.4: construct file menu here
        self._menubar = tk.Menu(self._master)
        self._filemenu = tk.Menu(self._menubar, tearoff=0)
        self._filemenu.add_command(label="New Game", command=self._new_game)
        self._filemenu.add_command(label="Exit", command=self._exit)
        self._menubar.add_cascade(label="File", menu=self._filemenu)

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        # Task 1.5 (Play Controls): Reconfigure the pause button here
        if paused:
            self.pause()
            self._play_controls.set_playpause('Play')
        else:
            self.start()
            self._play_controls.set_playpause('Pause')

        self._paused = paused

    def _setup_game(self):
        self._wave = 0
        self._score = 0
        self._coins = 50
        self._lives = 20
        self._game.towers = {}
        self._game._unspawned_enemies = []
        self._game.enemies = []

        self._won = False

        # Task 1.3 (Status Bar): Update status here
        self._statusbar.set_wave(self._wave, self._level.get_max_wave())
        self._statusbar.set_score(self._score)
        self._statusbar.set_coins(self._coins)
        self._statusbar.set_lives(self._lives)

        # Task 1.5 (Play Controls): Re-enable the play controls here (if they were ever disabled)
        self._play_controls.toggle_enabled(enabled=True)

        self._game.reset()

        # Auto-start the first wave
        self.next_wave()
        self._toggle_paused(paused=True)

    # Task 1.4 (File Menu): Complete menu item handlers here (including docstrings!)
    def _new_game(self):
        self.start()
        self._game.reset()
        self._setup_game()
        self.refresh_view()
        self._view.draw_enemies(self._game.enemies)

    def _exit(self):
        self.pause()
        MessageWindow(self._master, "Exit", "Are you sure you wish to quit the game?", self._master.quit, self.start)

    def refresh_view(self):
        """Refreshes the game view"""
        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)
        self._view.draw_towers(self._game.towers)
        self._view.draw_obstacles(self._game.obstacles)

    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

        Returns:
            (bool) True if the game is still running
        """
        if not self._has_game_ended():
            self._game.step()
            self.refresh_view()
            return not self.is_paused()
        else:
            return False

    # Task 1.2 (Tower Placement): Complete event handlers here (including docstrings!)
    # Event handlers: _move, _mouse_leave, _left_click
    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        if self._current_tower.get_value() > self._coins:
            return

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position

        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]
        self._view.draw_path(path)

        # Task 1.2 (Tower placement): Draw the tower preview here
        self._view.draw_preview(self._current_tower, legal)

    def _mouse_leave(self, event):
        """..."""
        self._view.delete("path", "shadow", "range")
        # Task 1.2 (Tower placement): Delete the preview
        # Hint: Relevant canvas items are tagged with: 'path', 'range', 'shadow'
        #       See tk.Canvas.delete (delete all with tag)

    def _left_click(self, event):
        """..."""
        # retrieve position to place tower
        if self._current_tower is None:
            return
        if self._current_tower.get_value() > self._coins:
            return

        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)

        if not self._has_game_ended() and self._game.place(cell_position, tower_type=self._current_tower.__class__):
            self._game.place(cell_position, tower_type=self._current_tower.__class__)
            self._coins -= self._current_tower.get_value()

            self._view.draw_towers(self._game.towers)
            self._statusbar.set_coins(self._coins)

        if self._current_tower.get_value() > self._coins:
            self._view.delete("path", "shadow", "range")

    def _sell_tower(self, event):
        """..."""
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)

        if cell_position in self._game.towers:
            self._coins += self._game.towers[cell_position].get_value() * 0.8
            self._statusbar.set_coins(self._coins)

            self._game.remove(cell_position)
            self._view.draw_towers(self._game.towers)

    def next_wave(self):
        """Sends the next wave of enemies against the player"""
        if self._wave == self._level.get_max_wave():
            return

        self._wave += 1

        # Task 1.3 (Status Bar): Update the current wave display here
        self._statusbar.set_wave(self._wave, self._level.get_max_wave())

        # Task 1.5 (Play Controls): Disable the add wave button here (if this is the last wave)
        if self._wave == self._level.get_max_wave():
            self._play_controls.toggle_enabled()
            self._play_controls.toggle_enabled(wave=False)

        # Generate wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)

    def _has_game_ended(self):
        """yiss"""
        if self._lives == 0:
            return True
        elif self._won:
            return True
        else:
            return False


    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)

        # Task 1.3 (Status Bar): Update coins & score displays here
        self._statusbar.set_score(self._score)
        self._statusbar.set_coins(self._coins)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
        """
        self._lives -= len(enemies)
        if self._lives < 0:
            self._lives = 0

        # Task 1.3 (Status Bar): Update lives display here
        self._statusbar.set_lives(self._lives)

        # Handle game over
        if self._lives == 0:
            self._handle_game_over(won=False)

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)"""
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)

    def _handle_game_over(self, won=False):
        """Handles game over

        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
        """
        self._won = won
        self._toggle_paused(paused=True)
        self._play_controls.toggle_enabled(enabled=False)

        # Task 1.4 (Dialogs): show game over dialog here
        if self._won:
            MessageWindow(self._master, "Game Over", "You Won!\nWould you like to play again?", self._new_game, self._exit)
        else:
            MessageWindow(self._master, "Game Over", "You Lost!\nWould you like to play again?", self._new_game, self._exit)


# Task 1.1 (App Class): Instantiate the GUI here
if __name__ == "__main__":
    root = tk.Tk()
    app = TowerGameApp(root)
    root.title("Towers")
    root.config(menu=app._menubar)
    root.mainloop()