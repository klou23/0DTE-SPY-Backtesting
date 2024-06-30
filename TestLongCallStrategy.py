from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap

from BacktestEngine import BacktestEngine
from Strategies.LongCallStrategy import LongCallStrategy
import matplotlib.pyplot as plt
import numpy as np


def test_long_call_strategy():
    strategies = []
    for pct_otm in range(-1600, 1601, 25):
        for profit_target_pct in range(5, 501, 3):
            strategies.append(LongCallStrategy(pct_otm / 1000, profit_target_pct, 100))

    bte = BacktestEngine(90, strategies)
    bte.run()

    targ = []
    otm = []
    pnl = []
    win_pct = []
    for strategy in strategies:
        targ.append(strategy.profit_target_pct)
        otm.append(strategy.pct_otm)
        pnl.append(sum(strategy.historicalPnl))

        win_cnt = sum(1 for value in strategy.historicalPnl if value > 0)
        win_pct.append(win_cnt/len(strategy.historicalPnl)*100)

    # Create a meshgrid for targ and otm
    targ_grid, otm_grid = np.meshgrid(np.unique(targ), np.unique(otm))

    # Reshape pnl and win_percentage to match the grid
    pnl_grid = np.reshape(pnl, targ_grid.shape)
    win_percentage_grid = np.reshape(win_pct, targ_grid.shape)

    # Create custom colormaps
    def create_pnl_colormap():
        return colors.LinearSegmentedColormap.from_list("", [
            (0, "darkred"), (0.25, "red"), (0.5, "white"),
            (0.75, "green"), (1, "darkgreen")
        ])

    def create_winrate_colormap():
        return colors.LinearSegmentedColormap.from_list("", [
            (0, "darkred"), (0.25, "red"), (0.5, "white"),
            (0.75, "green"), (1, "darkgreen")
        ])

    # Create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=False)

    fig.suptitle('Long 0DTE SPY Call - Buy at Open - Close at target or EOD - 90 Day Backtest')

    # PNL Plot
    pnl_cmap = create_pnl_colormap()
    vmax_pnl = max(abs(np.min(pnl_grid)), abs(np.max(pnl_grid)))
    mesh1 = ax1.pcolormesh(targ_grid, otm_grid, pnl_grid, cmap=pnl_cmap,
                           norm=colors.TwoSlopeNorm(vmin=-vmax_pnl, vcenter=0, vmax=vmax_pnl),
                           shading='auto')
    ax1.set_xlabel('Target Profit Percentage')
    ax1.set_ylabel('Percent out of the Money (Strike Price)')
    fig.colorbar(mesh1, ax=ax1, label='PnL')

    # Win Percentage Plot
    winrate_cmap = create_winrate_colormap()
    mesh2 = ax2.pcolormesh(targ_grid, otm_grid, win_percentage_grid, cmap=winrate_cmap,
                           norm=colors.TwoSlopeNorm(vmin=0, vcenter=50, vmax=100),
                           shading='auto')
    ax2.set_xlabel('Target Profit Percentage')
    ax2.set_ylabel('Percent out of the Money (Strike Price)')
    fig.colorbar(mesh2, ax=ax2, label='Win Percentage')

    plt.tight_layout()
    plt.show()
