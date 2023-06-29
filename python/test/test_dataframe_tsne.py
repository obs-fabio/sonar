import os, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib as tikz
from sklearn.manifold import TSNE

import labsonar_sp.analysis as sp
import labsonar_sp.plot as sp_plt
import labsonar_sp.dataframe as sp_df

input_dir = "/home/sonar/Data/4classes"

for abs_filename in sp_plt.get_files(input_dir,".csv"):

    df = pd.read_csv(abs_filename)
    print(abs_filename)

    features = df[df.columns[:-2]].values
    target = df[df.columns[-1]].values

    tsne = TSNE(n_components=2, random_state=42)
    features_tsne = tsne.fit_transform(features)

    plt.scatter(features_tsne[:, 0], features_tsne[:, 1], c=target, cmap='viridis')
    plt.xlabel('Componente 1')
    plt.ylabel('Componente 2')
    plt.colorbar()

    path, rel_filename = os.path.split(abs_filename)
    filename, extension = os.path.splitext(rel_filename)

    # plt.title(file)
    tikz.save(os.path.join(path, "t-sne_{:s}.tex".format(filename)))
    plt.savefig(os.path.join(path, "t-sne_{:s}.png".format(filename)))
    plt.close()