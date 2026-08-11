import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec as gsc

class Sim_Plotter:
    def plot_arrays(self, x, y, title="vars", save_fig=False):
        assert len(x) == len(y)

        fig = plt.figure(figsize=(14,10))

        if len(y) % 2 == 0:
            plot_size = len(y)//2
            gs = gsc(2, plot_size)
            for ind, elem in enumerate(y):
                ax = plt.subplot(gs[ind%2, ind//2])
                for ind_var, vars in enumerate(elem):
                    ax.plot(x[ind], vars[0], label=vars[1], color=vars[2], linestyle=vars[3])
                ax.legend()
                ax.margins(x=0)
                ax.grid()

        elif len(y) % 2 != 0:
            plot_size = len(y)//2 + 1
            gs = gsc(2, plot_size)
            for ind, elem in enumerate(y):
                if ind == len(y) - 1:
                    ax = plt.subplot(gs[:, ind//2])
                else:
                    ax = plt.subplot(gs[ind%2, ind//2])
                for ind_var, vars in enumerate(elem):
                    ax.plot(x[ind], vars[0], label=vars[1], color=vars[2], linestyle=vars[3])
                ax.legend()
                ax.margins(x=0)
                ax.grid()

        if save_fig:
            plt.savefig(f"plot{title}")

        plt.tight_layout()
        plt.show()