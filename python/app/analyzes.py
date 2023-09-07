import labsonar_sp.analysis as sp
import labsonar_sp.plot as sp_plt

n_pts=2048
n_overlap=1024
n_mels=128
decimation_rate=3

# image_height = 1024
# fs = 48000
# image_time = image_height*((n_pts - n_overlap)/(fs/decimation_rate))/60 #min
# print(image_time)

manager = sp_plt.Plot_manager(
                    [sp.Analysis.LOFAR, sp.Analysis.MELGRAM],
                    # [sp.Analysis.LOG_SPECTROGRAM, sp.Analysis.LOFAR, sp.Analysis.MELGRAM],
                    # [sp.Analysis.LOFAR],
                    [sp_plt.Plot_type.EXPORT_TIFF, sp_plt.Plot_type.EXPORT_JET],
                    # [sp_plt.Plot_type.EXPORT_MAGMA],
                    # spectre_format=True,
                    n_mels=n_mels,
                    n_pts=n_pts,
                    n_overlap=n_overlap,
                    decimation_rate=decimation_rate,
                    norm=2
                )

# manager.eval_dir("/home/sonar/Data/ShipsEar/audio", "/home/sonar/Data/ShipsEar/analysis")
# manager.eval_dir("/home/sonar/Data/DeepShip/data", "/home/sonar/Data/DeepShip/analysis/lofar")
manager.eval_dir("/home/sonar/Data/4classes/data", "/home/sonar/Data/4classes/icassp")

