from collections import defaultdict

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome
from src.calculations.symbol import Symbol
from src.events.event_constants import EventConstants
from src.events.events import json_ready_sym
from src.config.config import Config
from src.wins.multiplier_strategy import apply_global_mult, apply_added_symbol_mult, apply_combined_mult
from src.calculations.board import Board


class GameStateOverride(GameExecutables):
    """
    This class is is used to override or extend universal state.py functions.
    e.g: A specific game may have custom book properties to reset
    """

    def reset_book(self):
        """Reset game specific properties"""
        super().reset_book()

    def assign_special_sym_function(self):
        self.special_symbol_functions = {
            "M": [self.assign_mult_property],
            "W": [self.assign_mult_property],
        }

    def assign_mult_property(self, symbol):
        multiplier_value = get_random_outcome(
            self.get_current_distribution_conditions()["mult_values"]
        )
        symbol.multiplier = multiplier_value

    def check_game_repeat(self):
        if self.repeat == False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True

    def reveal_event(self):
        """Display the initial board drawn from reelstrips. Modified to have mystery record as well"""
        board = self.get_eval_board()
        board_client = []
        special_attributes = list(self.config.special_symbols.keys())
        for reel, _ in enumerate(board):
            board_client.append([])
            for row in range(len(board[reel])):
                board_client[reel].append(json_ready_sym(board[reel][row], special_attributes))

        if self.config.include_padding:
            for reel, _ in enumerate(board_client):
                board_client[reel] = [json_ready_sym(self.top_symbols[reel], special_attributes)] + board_client[
                    reel
                ]
                board_client[reel].append(json_ready_sym(self.bottom_symbols[reel], special_attributes))

        if not self.mystery_record:
            self.mystery_record = False
        event = {
            "index": len(self.book.events),
            "type": EventConstants.REVEAL.value,
            "board": board_client,
            "paddingPositions": self.reel_positions,
            "gameType": self.gametype if self.gametype == self.config.basegame_type else self.config.freegame_type,
            "anticipation": self.anticipation,
            "mystery": self.mystery_record,
        }
        self.book.add_event(event)

    def get_ways_data(
            self,
            config: Config,
            board: list[list[Symbol]],
            wild_key: str = "wild",
            global_multiplier: int = 1,
            multiplier_key: str = "multiplier",
            multiplier_strategy: str = "symbol",
    ):
        """Ways calculation with possibility for global multiplier application."""
        return_data = {
            "totalWin": 0,
            "wins": [],
        }
        assert multiplier_strategy in ["symbol", "board", "global"]
        board_mult_count = 0
        potential_wins = defaultdict()
        wilds = [[] for _ in range(len(board))]
        for reel, _ in enumerate(board):
            for row, _ in enumerate(board[reel]):
                sym = board[reel][row]
                if reel == 0 and sym.name not in potential_wins:
                    potential_wins[sym.name] = [[] for _ in range(len(board))]
                    potential_wins[sym.name][0] = [{"reel": reel, "row": row}]
                elif sym.name in potential_wins:
                    potential_wins[sym.name][reel].append({"reel": reel, "row": row})

                if sym.name in config.special_symbols[wild_key]:
                    wilds[reel].append({"reel": reel, "row": row})
                    if board[reel][row].check_attribute(multiplier_key):
                        wilds[reel][-1][multiplier_key] = board[reel][row].get_attribute(multiplier_key)

        for symbol in potential_wins:
            kind, ways = (0, 1)
            cumulative_sym_mult = 0 if self.gametype != self.config.freegame2_type else 1
            for reel, _ in enumerate(potential_wins[symbol]):
                if len(potential_wins[symbol][reel]) > 0 or len(wilds[reel]) > 0:
                    kind += 1
                    reel_sym_count = 0
                    # Note that here multipliers on subsequent reels multiply (not add, like in lines games)
                    symbols_have_mult = False
                    for s in potential_wins[symbol][reel]:
                        if board[s["reel"]][s["row"]].check_attribute(multiplier_key):
                            symbols_have_mult = True

                    if symbols_have_mult is False:
                        reel_sym_count += len(potential_wins[symbol][reel])
                    else:
                        reel_sym_count = 0
                        for s in potential_wins[symbol][reel]:
                            if (
                                    board[s["reel"]][s["row"]].check_attribute(multiplier_key)
                                    and multiplier_strategy == "symbol"
                            ):
                                reel_sym_count += board[s["reel"]][s["row"]].get_attribute(multiplier_key)
                            else:
                                reel_sym_count += 1
                                if (
                                        board[s["reel"]][s["row"]].check_attribute(multiplier_key)
                                        and multiplier_strategy == "board"
                                ):
                                    gm = board[s["reel"]][s["row"]].get_attribute(multiplier_key)
                                    board_mult_count += gm * (gm > 1)

                    if len(wilds[reel]) > 0:
                        for sym in wilds[reel]:
                            if board[sym["reel"]][sym["row"]].check_attribute(
                                    multiplier_key
                            ) and multiplier_strategy in ["board", "symbol"]:
                                wild_mult_val = board[sym["reel"]][sym["row"]].get_attribute(multiplier_key)
                                cumulative_sym_mult = (cumulative_sym_mult + (wild_mult_val * (wild_mult_val > 1))) if self.gametype != self.config.freegame2_type else (cumulative_sym_mult * (wild_mult_val * (wild_mult_val > 1)))
                                if multiplier_strategy == "board":
                                    reel_sym_count += 1
                                    board_mult_count += wild_mult_val * (wild_mult_val > 1)
                                else:
                                    reel_sym_count += wild_mult_val
                            else:
                                reel_sym_count += 1

                    ways *= reel_sym_count

                else:
                    break

            match multiplier_strategy:
                case "global":
                    win_multiplier = global_multiplier
                case "board":
                    win_multiplier = max(board_mult_count, 1)
                case "symbol":
                    win_multiplier = 1

            if (kind, symbol) in config.paytable:
                positions = []
                for reel in range(kind):
                    for pos in potential_wins[symbol][reel]:
                        positions += [pos]
                    for pos in wilds[reel]:
                        positions += [pos]

                win = round(config.paytable[kind, symbol] * ways, 2)
                win_amt, multiplier = self.apply_mult(
                    board=board,
                    strategy="global",
                    win_amount=win,
                    global_multiplier=win_multiplier,
                )
                if multiplier_strategy == "symbol":
                    assert win_amt == win

                return_data["wins"] += [
                    {
                        "symbol": symbol,
                        "kind": kind,
                        "win": win_amt,
                        "positions": positions,
                        "meta": {
                            "ways": ways,
                            "globalMult": multiplier,
                            "winWithoutMult": win,
                            "symbolMult": cumulative_sym_mult,
                        },
                    }
                ]
                return_data["totalWin"] += win_amt

        return return_data

    def apply_mult(
            self,
            board: Board,
            strategy: str,
            win_amount: float = 0.0,
            global_multiplier: int = 1,
            positions: list = [],
            multiplier_key: str = "multiplier",
    ):
        """Apply multiplier method to win_amount and winning symbol positions."""
        strat = {
            "global": apply_global_mult(win_amount, global_multiplier),
            "symbol": apply_added_symbol_mult(board, win_amount, positions, multiplier_key=multiplier_key) if self.fs_type != "notorious" else self.apply_multiplied_symbol_mult(board, win_amount, positions, multiplier_key=multiplier_key),
            "combined": apply_combined_mult(
                board, win_amount, global_multiplier, positions, multiplier_key=multiplier_key
            ),
        }
        return strat[strategy]

    def count_symbol_on_reel(self, reel, symbol_name):
        """Count number of sumbols on the board matching the target name."""
        symbol_count = 0
        for idy, _ in enumerate(self.board[reel]):
            if self.board[reel][idy].name.upper() == symbol_name.upper():
                symbol_count += 1
        return symbol_count