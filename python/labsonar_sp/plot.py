from enum import Enum
import os
from tqdm import tqdm
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib as tikz
import tifffile
import scipy.io.wavfile as wav_file
from PIL import Image

import labsonar_sp.analysis as sp
import labsonar_sp.prefered_number as sp_pn

def get_files(directory: str, extension: str):
	file_list = []
	for root, _, files in os.walk(directory):
		for file in files:
			if file.endswith(extension):
				file_list.append(os.path.join(root, file))
	return sorted(file_list)

class Plot_type(Enum): 
    SHOW_FIG = 0
    EXPORT_PNG = 1
    EXPORT_TIFF = 2
    EXPORT_TEX = 3
    EXPORT_MAGMA = 4
    EXPORT_JET = 5

    def get_extension(self):
        return ["",".png",".tiff",".tex",".png",".png"][self.value]

def plot(analysis: sp.Analysis, *args, plot_type: Plot_type = Plot_type.SHOW_FIG, filename: str = "fig", spectre_format: bool=False, **kwargs) -> str:

    S, f, t = analysis.eval(*args, **kwargs)
    S = sp.normalize(S)

    if analysis == sp.Analysis.LOFAR and not spectre_format:
        S = S.T

    if (plot_type == Plot_type.EXPORT_MAGMA) or (plot_type == Plot_type.EXPORT_JET):
        colormap = plt.cm.magma if (plot_type == Plot_type.EXPORT_MAGMA) else plt.cm.jet
        S = colormap(S)
        S_color = (S * 255).astype(np.uint8)
        image = Image.fromarray(S_color)
        image.save(filename)
        return

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
            plt.close()
        elif plot_type == Plot_type.EXPORT_TEX:
            tikz.save(filename)
            plt.close()

    else:
        tifffile.imwrite(filename, S.astype(np.float32))


class Plot_manager():
    def __init__(self, analyzes: List[sp.Analysis], plot_types: List[Plot_type], *args, override=True, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.plot_types = plot_types
        self.override = override
        self.analyzes = analyzes

    def eval_files(self, file_list: List[str], output_dir: str) -> List[str]:

        os.makedirs(output_dir, exist_ok=True)
        output_file_list = []

        for input_file in tqdm(file_list, desc='Files', leave=False):
            fs, input = wav_file.read(input_file)

            if input.ndim != 1:
                input = input[:,0]

            path, rel_filename = os.path.split(input_file)
            filename, extension = os.path.splitext(rel_filename)

            if len(self.analyzes) > 1:
                for analysis in self.analyzes:
                    os.makedirs(os.path.join(output_dir, str(analysis)), exist_ok=True)

            for analysis in tqdm(self.analyzes, desc='Analyzes', leave=False):
                output_analysis_dir = os.path.join(output_dir, str(analysis)) if (len(self.analyzes) > 1) else output_dir

                for plot_type in tqdm(self.plot_types, desc='Plots', leave=False):
                    output_file = os.path.join(output_analysis_dir, filename + plot_type.get_extension())
                    output_file_list.append({
                            'input': input_file,
                            'output': output_file,
                        })

                    if os.path.exists(output_file) and not self.override:
                        continue

                    plot(analysis,
                        input,
                        fs,
                        *self.args,
                        plot_type=plot_type,
                        filename=output_file,
                        **self.kwargs)
        return output_file_list

    def eval_dir(self, input_dir: str, output_dir: str, extension: str = ".wav"):
        return self.eval_files(get_files(input_dir,extension), output_dir)

