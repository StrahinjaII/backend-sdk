from copy import deepcopy

from game_calculations import GameCalculations
from src.calculations.statistics import get_random_outcome
from src.calculations.ways import Ways


class GameExecutables(GameCalculations):

    def evaluate_ways_board(self):
        board = self.get_eval_board()
        self.win_data = self.get_ways_data(self.config, board)
        if self.win_data["totalWin"] > 0:
            Ways.record_ways_wins(self)
            self.win_manager.update_spinwin(self.win_data["totalWin"])
        Ways.emit_wayswin_events(self)

    def mystery_event(self):
        self.mystery_record = False

        # Decide if mystery triggers (Force Stacked Mystery Symbols)
        force_mystery = get_random_outcome(self.get_current_distribution_conditions()["mystery"]["force_mystery"])
        if not force_mystery:
            return

        mystery_feature = {}

        temp_board = deepcopy(self.board)
        # Select how many reels will have mystery (Stacked Mystery Symbols Reels Amount)
        num_of_reels = get_random_outcome(self.get_current_distribution_conditions()["mystery"]["num_of_reels"])
        mystery_feature["num_of_reels"] = num_of_reels

        # Select reveal target symbol (Symbol To Replace Stacked Mystery Symbols)
        my_transform_symbol = get_random_outcome(self.get_current_distribution_conditions()["mystery"]["transform"])
        mystery_feature["my_transform_symbol"] = my_transform_symbol

        # Select which reels are forced based on count (Stacked Mystery Symbols Reels selection)
        selected_reels = get_random_outcome(self.get_current_distribution_conditions()["mystery"]["reel_selection"][num_of_reels])
        mystery_feature["selected_reels"] = selected_reels

        # Decide direction (top/bottom)
        draw_from_top = get_random_outcome(self.config.draw_from_top)
        mystery_feature["draw_from_top"] = draw_from_top

        mystery_symbol = self.create_symbol(self.config.mystery_symbol_name)
        mystery_feature["mystery_symbol"] = mystery_symbol

        changed = []
        total_applied = 0
        # For each forced reel, sample stack height (Stacked Mystery Symbols Amount Per Reel)
        for index, reel in enumerate(selected_reels):
            # and place placeholder symbols
            mysteries_per_reel = get_random_outcome(self.config.mysteries_per_reel[reel])
            applied_positions = self.apply_mystery_stack(reel, mystery_feature, mysteries_per_reel)
            changed.extend(applied_positions)
            total_applied += len(applied_positions)

        # While total mysteries < minimum:
        missing = max(0, self.config.min_mysteries - total_applied)
        max_attempts = len(self.board) * max(len(r) for r in self.board)  # safe guard
        attempts = 0

        while missing > 0 and attempts < max_attempts:
            attempts += 1

            random_reel = get_random_outcome(self.config.random_reel)

            rows = len(self.board[random_reel])
            already = self.count_symbol_on_reel(random_reel, self.config.mystery_symbol_name)
            available = max(0, rows - already)

            if available == 0:
                continue  # no progress possible on this reel

            amount_to_add = min(missing, available)

            newly_applied = self.apply_mystery_stack(random_reel, mystery_feature, amount_to_add)
            if not newly_applied:
                continue

            changed.extend(newly_applied)
            total_applied += len(newly_applied)
            missing -= len(newly_applied)

        if missing > 0:
            raise RuntimeError(
                f"Cannot reach min mysteries={self.config.min_mysteries}; ran out of available cells."
            )

        # Store mystery metadata:
        self.mystery_record = {
            "symbol": mystery_feature["my_transform_symbol"],
            "mysteryPositions": [{"reel": r, "position": c} for (r, c) in changed],
            "drawFromTop": bool(mystery_feature["draw_from_top"]),
            "totalMysteries": total_applied,
        }

    def apply_mystery_stack(self, reel_idx: int, mystery_feature, count: int) -> list[tuple[int, int]]:
        """Place up to `count` mystery placeholders on `reel_idx` from top/bottom.
        Returns list of (reel,row) that were set/changed."""
        rows = len(self.board[reel_idx])
        if rows <= 0:
            return []

        count = max(0, min(int(count), rows))

        if mystery_feature["draw_from_top"]:
            row_iter = range(0, count)
        else:
            row_iter = range(rows - 1, rows - 1 - count, -1)

        positions = []
        for r in row_iter:
            # skip if already mystery placeholder
            if self.board[reel_idx][r].name == self.config.mystery_symbol_name:
                continue
            self.board[reel_idx][r] = mystery_feature["mystery_symbol"]
            positions.append((reel_idx, r))
        return positions

    def get_eval_board(self):
        if not self.mystery_record:
            return self.board

        reveal_id = self.mystery_record["symbol"]
        reveal_symbol = self.create_symbol(reveal_id)
        placeholder_id = self.config.mystery_symbol_name

        eval_board = deepcopy(self.board)
        for reel_idx in range(len(eval_board)):
            for row_idx in range(len(eval_board[reel_idx])):
                if eval_board[reel_idx][row_idx].name == placeholder_id:
                    eval_board[reel_idx][row_idx] = reveal_symbol
        return eval_board

    def run_freespin_from_base(self, scatter_key: str = "scatter") -> None:
        """Trigger the freespin function and update total fs amount."""
        self.record(
            {
                "kind": self.count_special_symbols(scatter_key),
                "symbol": scatter_key,
                "gametype": self.gametype,
            }
        )

        # Handle choice of hte feature
        match self.count_special_symbols("scatter"):
         ## Keelhaul
            case 2:
                self.update_keelhaul()
                self.run_keelhaul()
         ## Free spins (blacksbeard and black flag)
            case 3 | 4:
                pass
        ## Free spins (notorious)
            case 5:
                pass
        self.update_freespin_amount()
        self.run_freespin()