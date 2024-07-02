import time as t
from datetime import time, datetime
import numpy as np
from matplotlib import colors, pyplot as plt
import yaml

from BacktestEngine import BacktestEngine
from Strategies.LongCallStrat import LongCallStrat
from TestLongCallStrategy import test_long_call_strategy


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def create_strategy(strategy_name):
    if strategy_name == 'LongCallStrat':
        return LongCallStrat
    raise ValueError("Unknown strategy type")


def time_range(start, end, step):
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    step_td = datetime.strptime(step, "%H:%M") - datetime.min

    current = start_dt
    while current <= end_dt:
        yield current.time()
        current += step_td


def generate_strategies(config):
    strategy_class = config['strategy']
    fixed_params = config['fixed_params']
    range_params = config['range_params']

    strategies = []

    param_ranges = []
    # Generate param combinations
    for param_name, param_config in range_params.items():
        if 'time' in param_name:
            param_ranges.append(list(time_range(param_config['start'], param_config['end'], param_config['step'])))
        else:
            param_ranges.append(np.arange(param_config['start'], param_config['end'] + param_config['step'],
                                          param_config['step']))

    param_combinations = np.array(np.meshgrid(*param_ranges)).T.reshape(-1, len(range_params))

    for combination in param_combinations:
        strat = create_strategy(strategy_class)
        params = fixed_params.copy()
        for (param_name, _), value in zip(range_params.items(), combination):
            if 'time' in param_name:
                params[param_name] = datetime.strptime(value, "%H:%M").time()
            else:
                params[param_name] = value

        strat.setup(params)
        strategies.append(strat)

    return strategies
        


def test_strat():
    strategies = []
    for pct_otm in range(-100, 100, 2):
        for profit_target_pct in range(5, 401, 5):
            strat = LongCallStrat()
            strat.setup({
                'pct_otm': pct_otm / 100,
                'profit_target_pct': profit_target_pct,
                'stop_loss_pct': 100,
                'open_time': time(hour=9, minute=30),
                'close_time': time(hour=16, minute=0)
            })
            strategies.append(strat)

    bte = BacktestEngine(90, strategies)
    bte.run()

    targ = []
    otm = []
    pnl = []
    win_pct = []
    for strat in strategies:
        targ.append(strat.params['profit_target_pct'])
        otm.append(strat.params['pct_otm'])
        pnl.append(sum(strat.pnl_history))

        win_cnt = sum(1 for value in strat.pnl_history if value > 0)
        win_pct.append(win_cnt / len(strat.pnl_history) * 100)

    targ_grid, otm_grid = np.meshgrid(np.unique(targ), np.unique(otm))
    pnl_grid = np.reshape(pnl, targ_grid.shape)
    win_pct_grid = np.reshape(win_pct, targ_grid.shape)

    def create_colormap():
        return colors.LinearSegmentedColormap.from_list("", [
            (0, "darkred"), (0.25, "red"), (0.5, "white"),
            (0.75, "green"), (1, "darkgreen")
        ])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=False)

    fig.suptitle('Long 0DTE SPY Call - Buy at Open - Close at target or EOD - 90 Day Backtest')

    pnl_cmap = create_colormap()
    vmax_pnl = max(abs(np.min(pnl_grid)), abs(np.max(pnl_grid)))
    mesh1 = ax1.pcolormesh(targ_grid, otm_grid, pnl_grid, cmap=pnl_cmap,
                           norm=colors.TwoSlopeNorm(vmin=-vmax_pnl, vcenter=0, vmax=vmax_pnl),
                           shading='auto')
    ax1.set_xlabel('Target Profit Percentage')
    ax1.set_ylabel('Percent out of the Money (Strike Price)')
    fig.colorbar(mesh1, ax=ax1, label='PnL')

    winrate_cmap = create_colormap()
    mesh2 = ax2.pcolormesh(targ_grid, otm_grid, win_pct_grid, cmap=winrate_cmap,
                           norm=colors.TwoSlopeNorm(vmin=0, vcenter=50, vmax=100),
                           shading='auto')
    ax2.set_xlabel('Target Profit Percentage')
    ax2.set_ylabel('Percent out of the Money (Strike Price)')
    fig.colorbar(mesh2, ax=ax2, label='Win Percentage')

    plt.tight_layout()
    plt.show()


def main():
    start = t.time()
    test_strat()
    end = t.time()
    print(f"TIME: {end - start}")


if __name__ == '__main__':
    main()
