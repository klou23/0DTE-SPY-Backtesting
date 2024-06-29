from BacktestEngine import BacktestEngine
from Strategies.LongCallStrategy import LongCallStrategy
import matplotlib.pyplot as plt
import numpy as np

def test_long_call_strategy():
    strategies = []
    for profit_target_pct in range(1, 500):
        for pct_otm in range(-5, 6):
            strategies.append(LongCallStrategy(pct_otm / 10, profit_target_pct, 100))

    bte = BacktestEngine(90, strategies)
    bte.run()

    targ = []
    otm = []
    pnl = []
    for strategy in strategies:
        targ.append(strategy.profit_target_pct)
        otm.append(strategy.pct_otm)
        pnl.append(sum(strategy.historicalPnl))

    # Create a meshgrid for targ and otm
    targ_grid, otm_grid = np.meshgrid(np.unique(targ), np.unique(otm))

    # Reshape pnl to match the grid
    pnl_grid = np.reshape(pnl, targ_grid.shape)

    # Create the 2D plot
    plt.figure(figsize=(10, 8))

    # Create a contour plot
    contour = plt.contourf(targ_grid, otm_grid, pnl_grid, levels=20, cmap='viridis')

    # Add labels and title
    plt.xlabel('targ')
    plt.ylabel('otm')
    plt.title('PNL as a function of targ and otm')

    # Add a color bar
    plt.colorbar(contour, label='pnl')

    # Show the plot
    plt.show()