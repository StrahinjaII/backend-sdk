"""Template game configuration file, detailing required user-specified inputs."""
from src.config.distributions import Distribution
from src.config.config import BetMode
from src.plugins.config_fms import Config_FMS


class GameConfig(Config_FMS):
    """Template configuration class."""

    def __init__(self):
        super().__init__()
        self.game_id = "FMS_BB_r960"
        self.provider_numer = 0
        self.working_name = "Blackbeard's Revenge"
        self.wincap = 500 #TODO: Needs to be fixed and changed to 15000 later
        self.win_type = "ways"
        self.rtp = 0.97
        self.construct_paths()

        self.basegame_type = "basegame"
        self.freegame_type = "freegame"
        self.freegame1_type = "freegame1"
        self.freegame2_type = "freegame2"
        self.respin_type = "respin"

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [3,4,4,4,3]  # Optionally include variable number of rows per reel
        # Board and Symbol Properties
        self.paytable = {
            (5, "W"): 40,
            (5, "H1"): 40,
            (5, "H2"): 20,
            (5, "H3"): 18,
            (5, "H4"): 16,
            (5, "H5"): 14,
            (5, "L1"): 12,
            (5, "L2"): 10,
            (5, "L3"): 8,
            (5, "L4"): 6,
            (5, "L5"): 5,

            (4, "W"): 20,
            (4, "H1"): 20,
            (4, "H2"): 16,
            (4, "H3"): 14,
            (4, "H4"): 12,
            (4, "H5"): 10,
            (4, "L1"): 8,
            (4, "L2"): 6,
            (4, "L3"): 5,
            (4, "L4"): 4,
            (4, "L5"): 3,

            (3, "W"): 10,
            (3, "H1"): 10,
            (3, "H2"): 9,
            (3, "H3"): 8,
            (3, "H4"): 7,
            (3, "H5"): 6,
            (3, "L1"): 5,
            (3, "L2"): 4,
            (3, "L3"): 3,
            (3, "L4"): 2,
            (3, "L5"): 1,

            (5, "MY"): 0,
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "multiplier": ["W"]}

        self.freespin_triggers = {
            self.basegame_type: {2: 1, 3: 6, 4: 8, 5: 10},
            self.freegame_type: {5: 2},
            self.freegame1_type: {5: 2},
            self.freegame2_type: {5: 2},
            self.respin_type: {2: 1}
        }
        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 4,
            self.freegame1_type: 4,
            self.freegame2_type: 4,
            self.respin_type: 5
        }
        # Reels
        reels = {
            "RS0": "reel_set_0.csv",
            "RS1": "reel_set_1.csv",
            "RS2": "reel_set_2.csv",
            "RS3": "reel_set_3.csv",
            "RS4": "reel_set_4.csv",
            "RS5": "reel_set_5.csv",
            "RS6": "reel_set_6.csv",
            "RS7": "reel_set_7.csv",
            "RS8": "reel_set_8.csv",
            "RS9": "reel_set_9.csv",
            "RS10": "reel_set_10.csv",
            "RS11": "reel_set_11.csv",
            "RS12": "reel_set_12.csv",
            "RS13": "reel_set_13.csv",
            "RS14": "reel_set_14.csv",
            "RS15": "reel_set_15.csv",
            "RS16": "reel_set_16.csv",
            "RS17": "reel_set_17.csv",
            "RS18": "reel_set_18.csv",
            "RS19": "reel_set_19.csv",
            "RS20": "reel_set_20.csv",
            "RS21": "reel_set_21.csv",
            "RS22": "reel_set_22.csv",
            "RS23": "reel_set_23.csv"
        }
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_vertical_reels_csv(str.join("/", [self.reels_path, f]))

        self.mysteries_per_reel = {
            0: {
                2: 200,
                3: 50,
                4: 2
            },
            1: {
                2: 200,
                3: 50,
                4: 2
            },
            2: {
                2: 200,
                3: 40,
                4: 1
            },
            3: {
                2: 400,
                3: 40,
                4: 1
            },
            4: {
                2: 500,
                3: 40,
                4: 1
            }
        }
        self.draw_from_top = {True: 1, False: 1}
        self.mystery_symbol_name = "MY"
        self.min_mysteries = 6
        self.random_reel = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}

        self.trigger_keelhaul = {True: 1, False: 2}
        self.keelhaul_scatter_amount = {2: 500, 3: 314, 4: 178, 5: 6}

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: { "RS0" : 5, "RS1" : 200, "RS2" : 106, "RS3" : 18, "RS4" : 520, "RS5" : 520, "RS6" : 520, "RS7" : 17830, "RS8" : 9700, "RS9" : 9800, "RS10": 135, "RS11": 496, "RS12": 500, "RS13": 250, "RS14": 150, "RS15": 510, "RS16": 510, "RS17": 400, "RS18": 400, "RS21": 16 },
                                self.freegame_type: {"RS2": 40, "RS4": 80, "RS5": 80, "RS6": 80, "RS7": 20, "RS13": 5, "RS14": 5, "RS15": 60, "RS16": 50, "RS21": 15},
                                self.freegame1_type: {"RS2": 26, "RS3": 16, "RS4": 90, "RS5": 90, "RS6": 90, "RS7": 150, "RS13": 20, "RS14": 20, "RS15": 59, "RS16": 59, "RS22": 76, "RS23": 76},
                                self.freegame2_type: {"RS2": 3, "RS3": 3, "RS4": 15, "RS5": 15, "RS6": 15, "RS7": 30, "RS15": 56, "RS16": 56, "RS22": 15, "RS23": 15},
                                self.respin_type: {"RS0": 5, "RS1": 200, "RS8": 9700, "RS9": 9800, "RS10": 135},
                            },
                            "scatter_triggers": {2: 1, 3: 6, 4: 8, 5: 10},
                            "force_wincap": True,
                            "force_freegame": False,
                            "mult_values": {2: 777, 3: 60, 4: 1},
                            "mystery": {
                                "force_mystery": {True: 1, False: 40},
                                "num_of_reels": {2: 1500, 3: 3000, 4: 8, 5: 1},
                                "transform": {
                                    "H1": 5,
                                    "H2": 10,
                                    "H3": 20,
                                    "H4": 40,
                                    "H5": 60,
                                    "L1": 90,
                                    "L2": 110,
                                    "L3": 130,
                                    "L4": 150,
                                    "L5": 170
                                },
                                "reel_selection": {
                                    2: {
                                        (0, 1): 20,
                                        (0, 2): 10,
                                        (0, 3): 10,
                                        (0, 4): 10,
                                        (1, 2): 10,
                                        (1, 3): 10,
                                        (1, 4): 10,
                                        (2, 3): 10,
                                        (2, 4): 10,
                                        (3, 4): 5,
                                    },
                                    3: {
                                        (0, 1, 2): 15,
                                        (0, 1, 3): 10,
                                        (0, 1, 4): 5,
                                        (0, 2, 3): 5,
                                        (0, 2, 4): 5,
                                        (0, 3, 4): 5,
                                        (1, 2, 3): 5,
                                        (1, 2, 4): 5,
                                        (1, 3, 4): 5,
                                        (2, 3, 4): 5
                                    },
                                    4: {
                                        (0, 1, 2, 3): 10,
                                        (0, 1, 2, 4): 10,
                                        (0, 1, 3, 4): 10,
                                        (0, 2, 3, 4): 5,
                                        (1, 2, 3, 4): 5
                                    },
                                    5: {
                                        (0, 1, 2, 3, 4): 1
                                    }
                                }
                            }
                        },
                    ),
                    # Distribution(
                    #     criteria="freegame",
                    #     quota=0.1,
                    #     conditions={
                    #         "reel_weights": {
                    #             self.basegame_type: { "RS0" : 5, "RS1" : 200, "RS8" : 9700, "RS9" : 9800, "RS10": 135},
                    #             self.freegame_type: { "RS2": 40, "RS4": 80, "RS5": 80, "RS6": 80, "RS7": 20, "RS13": 5, "RS14": 5, "RS15": 60, "RS16": 50, "RS21": 15 },
                    #         },
                    #         "force_wincap": False,
                    #         "force_freegame": True,
                    #         "scatter_triggers": {3: 6},
                    #         "mult_values": {2: 100, 3: 80, 4: 50},
                    #         "num_of_rows": [3,4,4,4,3],
                    #         "mystery": {
                    #             "force_mystery": { True: 1, False: 40 },
                    #             "num_of_reels": { 2: 1500, 3: 3000, 4: 40, 5: 1 },
                    #             "transform": {
                    #                 "H1":   1,
                    #                 "H2":   5,
                    #                 "H3":  10,
                    #                 "H4":  20,
                    #                 "H5":  40,
                    #                 "L1":   70,
                    #                 "L2":  110,
                    #                 "L3":  130,
                    #                 "L4":  150,
                    #                 "L5":  170
                    #             },
                    #             "reel_selection": {
                    #                 2: {
                    #                     (0, 1): 10,
                    #                     (0, 2): 10,
                    #                     (0, 3): 10,
                    #                     (0, 4): 10,
                    #                     (1, 2): 10,
                    #                     (1, 3): 10,
                    #                     (1, 4): 5,
                    #                     (2, 3): 5,
                    #                     (2, 4): 5,
                    #                     (3, 4): 5,
                    #                 },
                    #                 3: {
                    #                     (0, 1, 2): 15,
                    #                     (0, 1, 3): 15,
                    #                     (0, 1, 4): 10,
                    #                     (0, 2, 3): 10,
                    #                     (0, 2, 4): 10,
                    #                     (0, 3, 4): 10,
                    #                     (1, 2, 3): 5,
                    #                     (1, 2, 4): 5,
                    #                     (1, 3, 4): 5,
                    #                     (2, 3, 4): 5
                    #                 },
                    #                 4: {
                    #                     (0, 1, 2, 3): 10,
                    #                     (0, 1, 2, 4): 10,
                    #                     (0, 1, 3, 4): 5,
                    #                     (0, 2, 3, 4): 5,
                    #                     (1, 2, 3, 4): 5
                    #                 },
                    #                 5: {
                    #                     (0, 1, 2, 3, 4): 10
                    #                 }
                    #             }
                    #         }
                    #     },
                    # ),
                    # Distribution(
                    #     criteria="respin",
                    #     quota=0.1,
                    #     conditions={
                    #         "reel_weights": {
                    #             self.basegame_type: {"RS0": 5, "RS1": 200, "RS8": 9700, "RS9": 9800, "RS10": 135},
                    #             self.respin_type: {"RS0": 5, "RS1": 200, "RS8": 9700, "RS9": 9800, "RS10": 135},
                    #         },
                    #         "force_wincap": False,
                    #         "force_freegame": True,
                    #         "scatter_triggers": {2: 1},
                    #         "mult_values": {2: 777, 3: 60},
                    #     }
                    # ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: { "RS0" : 5, "RS1" : 200, "RS2" : 106, "RS3" : 18, "RS4" : 520, "RS5" : 520, "RS6" : 520, "RS7" : 17830, "RS8" : 9700, "RS9" : 9800, "RS10": 135, "RS11": 496, "RS12": 500, "RS13": 250, "RS14": 150, "RS15": 510, "RS16": 510, "RS17": 400, "RS18": 400, "RS21": 16 }
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": {2: 777, 3: 60},
                            "num_of_rows": [3,4,4,4,3],
                            "mystery": {
                                "force_mystery": { True: 1, False: 40 },
                                "num_of_reels": { 2: 1500, 3: 3000, 4: 8, 5: 1 },
                                "transform": {
                                    "H1":   5,
                                    "H2":  10,
                                    "H3":  20,
                                    "H4":  40,
                                    "H5":  60,
                                    "L1":   90,
                                    "L2":  110,
                                    "L3":  130,
                                    "L4":  150,
                                    "L5":  170
                                },
                                "reel_selection": {
                                    2: {
                                        (0, 1): 20,
                                        (0, 2): 10,
                                        (0, 3): 10,
                                        (0, 4): 10,
                                        (1, 2): 10,
                                        (1, 3): 10,
                                        (1, 4): 10,
                                        (2, 3): 10,
                                        (2, 4): 10,
                                        (3, 4): 5,
                                    },
                                    3: {
                                        (0, 1, 2): 15,
                                        (0, 1, 3): 10,
                                        (0, 1, 4): 5,
                                        (0, 2, 3): 5,
                                        (0, 2, 4): 5,
                                        (0, 3, 4): 5,
                                        (1, 2, 3): 5,
                                        (1, 2, 4): 5,
                                        (1, 3, 4): 5,
                                        (2, 3, 4): 5
                                    },
                                    4: {
                                        (0, 1, 2, 3): 10,
                                        (0, 1, 2, 4): 10,
                                        (0, 1, 3, 4): 10,
                                        (0, 2, 3, 4): 5,
                                        (1, 2, 3, 4): 5
                                    },
                                    5: {
                                        (0, 1, 2, 3, 4): 1
                                    }
                                }
                            }
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: { "RS0" : 5, "RS1" : 200, "RS2" : 106, "RS3" : 18, "RS4" : 520, "RS5" : 520, "RS6" : 520, "RS7" : 17830, "RS8" : 9700, "RS9" : 9800, "RS10": 135, "RS11": 496, "RS12": 500, "RS13": 250, "RS14": 150, "RS15": 510, "RS16": 510, "RS17": 400, "RS18": 400, "RS21": 16 }
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": {2: 777, 3: 60},
                            "num_of_rows": [3,4,4,4,3],
                            "mystery": {
                                "force_mystery": { True: 1, False: 40 },
                                "num_of_reels": { 2: 1500, 3: 3000, 4: 8, 5: 1 },
                                "transform": {
                                    "H1":   5,
                                    "H2":  10,
                                    "H3":  20,
                                    "H4":  40,
                                    "H5":  60,
                                    "L1":   90,
                                    "L2":  110,
                                    "L3":  130,
                                    "L4":  150,
                                    "L5":  170
                                },
                                "reel_selection": {
                                    2: {
                                        (0, 1): 20,
                                        (0, 2): 10,
                                        (0, 3): 10,
                                        (0, 4): 10,
                                        (1, 2): 10,
                                        (1, 3): 10,
                                        (1, 4): 10,
                                        (2, 3): 10,
                                        (2, 4): 10,
                                        (3, 4): 5,
                                    },
                                    3: {
                                        (0, 1, 2): 15,
                                        (0, 1, 3): 10,
                                        (0, 1, 4): 5,
                                        (0, 2, 3): 5,
                                        (0, 2, 4): 5,
                                        (0, 3, 4): 5,
                                        (1, 2, 3): 5,
                                        (1, 2, 4): 5,
                                        (1, 3, 4): 5,
                                        (2, 3, 4): 5
                                    },
                                    4: {
                                        (0, 1, 2, 3): 10,
                                        (0, 1, 2, 4): 10,
                                        (0, 1, 3, 4): 10,
                                        (0, 2, 3, 4): 5,
                                        (1, 2, 3, 4): 5
                                    },
                                    5: {
                                        (0, 1, 2, 3, 4): 1
                                    }
                                }
                            }
                        },
                    ),
                ],
            ),
        ]
