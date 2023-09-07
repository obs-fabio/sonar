import os
from tqdm import tqdm
import skimage.io as skimage
import matplotlib
import labsonar_sp.plot as lab_plt

files = lab_plt.get_files("/home/sonar/Data/4classes/analysis/melgram", ".tiff")
output_dir = "/home/sonar/Data/4classes/analysis3/melgram"

for abs_filename in tqdm(files):

    path, rel_filename = os.path.split(abs_filename)
    filename, extension = os.path.splitext(rel_filename)


    data = skimage.imread(abs_filename)

    # matplotlib.image.imsave(
    #         f"{output_dir}/{filename}.png",
    #         data,
    #         cmap="gray",
    #     )

    n_freqs = int(32)
    n_step = int(n_freqs/2)
    n_lines = int(data.shape[1])

    index = 0
    i = 0
    while ((index + n_freqs) < n_lines):
        frag = data[:,index:(index + n_freqs)]

        print("\t", frag.shape)
        matplotlib.image.imsave(
            f"{output_dir}/{filename}_{i}.png",
            frag,
            cmap="gray",
        )

        index = index + n_step
        i = i + 1