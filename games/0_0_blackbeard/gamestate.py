"""Handles the state and output for a single simulation round"""

from game_override import GameStateOverride
from src.calculations.statistics import get_random_outcome


class GameState(GameStateOverride):
    """Handle all game-logic and event updates for a given simulation number."""

    def run_spin(self, sim, simulation_seed=None):
        self.fs_type = False

        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()

            # Create board
            self.draw_board(emit_event=False)

            # Run mystery
            self.mystery_event()

            # Create reveal event with mystery
            self.reveal_event()

            # Evaluate board
            self.evaluate_ways_board()
            self.win_manager.update_gametype_wins(self.gametype)

            # Scatter features
            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            # evaluate end of the spin
            self.evaluate_finalwin()
            self.check_repeat()


        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            self.update_freespin()
            pass

        self.end_freespin()
