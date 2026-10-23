"""Main file for generating results for sample lines-pay game."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # TODO: Remove this segment it is only for development and is not used for game \/
    IS_BUILD_RUN = True

    nut_t = 10
    compress = True
    num_sim = int(1e4)
    optim = True
    analysis = True

    if not IS_BUILD_RUN:
        nut_t = 1
        compress = False
        num_sim = 100
        optim = False
        analysis = False
    # TODO: Remove this segment above it is only for development and should not be used in the game /\

    num_threads = nut_t
    rust_threads = 20
    batching_size = 50000
    compression = compress
    profiling = False

    num_sim_args = {
        "base": num_sim
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": optim,
        "run_analysis": analysis,
        "run_format_checks": True,
    }
    target_modes = ["base"]

    config = GameConfig()
    gamestate = GameState(config)
    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        optimization_setup_class = OptimizationSetup(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )

    generate_configs(gamestate)

    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    if run_conditions["run_analysis"]:
        custom_keys = [{"symbol": "scatter"}]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)
