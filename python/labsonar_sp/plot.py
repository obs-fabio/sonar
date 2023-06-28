from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib as tikz
import tifffile

import labsonar_sp.analysis as sp
import labsonar_sp.prefered_number as sp_pn

class Plot_type(Enum): 
    SHOW_FIG = 1
    EXPORT_PNG = 2
    EXPORT_TIFF = 3
    EXPORT_TEX = 4

def plot(analysis: sp.Analysis, *args, plot_type: Plot_type = Plot_type.SHOW_FIG, filename: str = "fig", spectre_format: bool=False, **kwargs) -> str:

    S, f, t = analysis.eval(*args, **kwargs)
    S = sp.normalize(S)

    if analysis == sp.Analysis.LOFAR and not spectre_format:
        S = S.T

    if plot_type != Plot_type.EXPORT_TIFF:

        t[0] = 0
        f[0] = 0

        n_ticks = 5
        x_labels = [sp_pn.get_engineering_notation(t[i], "s") for i in np.linspace(0, len(t)-1, num=n_ticks, dtype=int)]
        y_labels = [sp_pn.get_engineering_notation(f[i], "Hz") for i in np.linspace(0, len(f)-1, num=n_ticks, dtype=int)]
        x_ticks = [(x/4 * (len(t)-1)) for x in range(n_ticks)]
        y_ticks = [(y/4 * (len(f)-1)) for y in range(n_ticks)]

        plt.figure()
        plt.imshow(S, aspect='auto', origin='lower', cmap='jet')
        plt.colorbar()

        if analysis == sp.Analysis.LOFAR and not spectre_format:
            plt.ylabel('Time')
            plt.xlabel('Frequency')
            plt.yticks(x_ticks)
            plt.gca().set_yticklabels(x_labels)
            plt.xticks(y_ticks)
            plt.gca().set_xticklabels(y_labels)
            plt.gca().invert_yaxis()
        else:
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.xticks(x_ticks)
            plt.gca().set_xticklabels(x_labels)
            plt.yticks(y_ticks)
            plt.gca().set_yticklabels(y_labels)

        if plot_type == Plot_type.SHOW_FIG:
            plt.show()
        elif plot_type == Plot_type.EXPORT_PNG:
            plt.savefig(filename)
        elif plot_type == Plot_type.EXPORT_TEX:
            tikz.save(filename)

    else:
        tifffile.imwrite(filename, S.astype(np.float32))
