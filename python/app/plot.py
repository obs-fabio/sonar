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

n_pts=512
n_overlap=128
n_mels=64
decimation_rate=1


def get_class(abs_filename:str) -> str:
    path, rel_filename = os.path.split(abs_filename)
    filename, extension = os.path.splitext(rel_filename)
    return filename.split('_')[0]

def get_id(abs_filename:str) -> str:
    path, rel_filename = os.path.split(abs_filename)
    filename, extension = os.path.splitext(rel_filename)
    return filename.split('_')[-1]

analyzes = [sp.Analysis.LOG_SPECTROGRAM, sp.Analysis.LOFAR, sp.Analysis.MELGRAM]
for ana in tqdm(analyzes, desc='DataFrames'):
    sp_df.create_window_dataframe(ana,
            "/home/sonar/Data/4classes_mini",
            "/home/sonar/Data/4classes_mini/df_{:s}.csv".format(str(ana)),
            extract_class=get_class,
        )

# manager = sp_plt.Plot_manager(
#                     [sp.Analysis.LOG_SPECTROGRAM, sp.Analysis.LOFAR, sp.Analysis.MELGRAM],
#                     [sp_plt.Plot_type.EXPORT_TIFF, sp_plt.Plot_type.EXPORT_PNG],
#                     spectre_format=True,
#                     n_mels=n_mels,
#                     n_pts=n_pts,
#                     n_overlap=n_overlap,
#                     decimation_rate=decimation_rate
#                 )

# manager.eval_files(sp_plt.get_files("/home/sonar/Data/4classes",".wav")[0:3], "/home/sonar/Data/4classes-analyzes")



# fs, input = wavfile.read("sonar/test_data/input.wav")
# input = input[:,0]
# print(input.shape)

# for analysis in [sp.Analysis.SPECTROGRAM, sp.Analysis.LOG_SPECTROGRAM, sp.Analysis.LOFAR, sp.Analysis.MELGRAM]:
# for analysis in [sp.Analysis.LOFAR]:
    # sp_plt.plot(analysis, input, fs, spectre_format=True, n_mels=n_mels, n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)

# sp_plt.plot(sp.Analysis.LOFAR, input, fs, plot_type = sp_plt.Plot_type.EXPORT_TIFF, filename = "fig.tiff", n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)
# sp_plt.plot(sp.Analysis.LOFAR, input, fs, plot_type = sp_plt.Plot_type.EXPORT_TEX, filename = "fig.tex", n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)
# sp_plt.plot(sp.Analysis.LOFAR, input, fs, plot_type = sp_plt.Plot_type.EXPORT_PNG, filename = "fig.png", n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)
# sp_plt.plot(sp.Analysis.LOFAR, input, fs, plot_type = sp_plt.Plot_type.SHOW_FIG, n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)


# import tifffile
# data = tifffile.imread("/home/sonar/Data/4classes-analyzes/lofar/1_00.tiff")
# print(data.shape)
# print(type(data), type(data[0,0]))
# print(data[0:10,0:10])



# mel, _, mel_time = sp.Analysis.MELGRAM.eval(input, fs, n_pts=n_pts, n_overlap=n_overlap, n_mels=n_mels, decimation_rate=decimation_rate)
# lofar, lofar_f, lofar_time = sp.lofar(input, fs, n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)
# spectro, _, spectro_time = sp.log_spectrogram(input, fs, n_pts=n_pts, n_overlap=n_overlap, decimation_rate=decimation_rate)

# print(input.shape)
# print("mel: ", mel.shape)
# print("lofar: ", lofar.shape)
# print("spectro: ", spectro.shape)

# print("mel_time: ", mel_time[0], " ", mel_time[1], " ", mel_time[-1])
# print("lofar_time: ", lofar_time[0], " ", lofar_time[1], " ", lofar_time[-1])
# print("spectro_time: ", spectro_time[0], " ", spectro_time[1], " ", spectro_time[-1])


# fig, ax = plt.subplots()
# plt.magma()
# img = ax.imshow(mel, interpolation='nearest', aspect='auto')

# fig, ax = plt.subplots()
# plt.magma()
# img = ax.imshow(lofar, interpolation='nearest', aspect='auto')

# fig, ax = plt.subplots()
# plt.magma()
# img = ax.imshow(spectro, interpolation='nearest', aspect='auto')

# plt.show()


# # Parâmetros do sinal
# sr = 22050  # Taxa de amostragem (Hz)
# duration = 5  # Duração do sinal (segundos)
# f1 = 440  # Frequência do primeiro seno (Hz)
# f2 = 880  # Frequência do segundo seno (Hz)

# # Cálculo do Melgrama
# n_fft = 1024
# hop_length = 1024

# # Geração do sinal
# t = np.linspace(0, duration, int(sr * duration), endpoint=False)
# t=t[0:int(np.floor(len(t)/n_fft)*n_fft)]
# signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)


# signal=sp.normalize(signal, 1)
# S = librosa.feature.melspectrogram(
#                 y=signal,
#                 sr=sr,
#                 n_fft=n_fft,
#                 hop_length=hop_length,
#                 win_length=n_fft,
#                 window=np.hanning(n_fft),
#                 n_mels=64,
#                 power=2)
# S_dB = 20*np.log10(S)

# S_dB = sp.normalize(S_dB)


# mel_default = skimage.imread(os.path.join("sonar/test_data/sins.tiff"))

# print(t.shape[0]/n_fft)
# print(S_dB.shape)
# print(mel_default.shape)

# S_dB1 = S_dB[:,:-1]
# S_dB2 = S_dB[:,1:]

# S_dB1 = sp.normalize(S_dB1)
# S_dB2 = sp.normalize(S_dB2)

# mel1 = np.abs(np.subtract(mel_default, S_dB1))
# mel2 = np.abs(np.subtract(mel_default, S_dB2))

# default_diff1 = np.count_nonzero(mel1 > 1e-1)/mel1.size
# default_diff2 = np.count_nonzero(mel2 > 1e-1)/mel2.size

# print("S_dB1: ", np.min(S_dB1), np.max(S_dB1))
# print("S_dB2: ", np.min(S_dB2), np.max(S_dB2))

# print("mel1: ", np.min(mel1), np.mean(mel1), np.max(mel1))
# print("mel2: ", np.min(mel2), np.mean(mel2), np.max(mel2))

# print("default_diff1: ", default_diff1)
# print("default_diff2: ", default_diff2)