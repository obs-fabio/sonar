import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
from tqdm import tqdm
import scipy.io.wavfile as wavfile
import skimage.io as skimage

import labsonar_sp.analysis as sp
import labsonar_sp.plot as sp_plt
import labsonar_sp.dataframe as sp_df

n_pts=1024
n_overlap=0
n_mels=64
decimation_rate=4

input_dir = "/home/sonar/Data/4classes"

# def get_class(abs_filename:str) -> str:
#     path, rel_filename = os.path.split(abs_filename)
#     filename, extension = os.path.splitext(rel_filename)
#     return filename.split('_')[0]

analyzes = [sp.Analysis.LOG_SPECTROGRAM, sp.Analysis.LOFAR, sp.Analysis.MELGRAM]
for analysis in tqdm(analyzes, desc='DataFrames'):
    sp_df.create_window_dataframe(analysis,
            input_dir,
            input_dir + "/df_{:s}.csv".format(str(analysis)),
            # extract_class=get_class,
            n_pts=n_pts,
            n_overlap=n_overlap,
            n_mels=n_mels,
            decimation_rate=decimation_rate
        )