import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import Callable
import tifffile
import random
import string


import labsonar_sp.analysis as sp
import labsonar_sp.plot as sp_plt

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def get_class(filename:str) -> str:
    return os.path.basename(os.path.dirname(filename))

def get_file_id(filename:str) -> str:
    return filename

def create_window_dataframe(analysis: sp.Analysis,
                            input_dir: str,
                            output_filename: str,
                            extension: str = ".wav",
                            extract_class: Callable[[str], str] = get_class,
                            extract_file_id: Callable[[str], str] = get_file_id,
                            **kwargs):

    manager = sp_plt.Plot_manager(
                        [analysis],
                        [sp_plt.Plot_type.EXPORT_TIFF],
                        spectre_format=True,
                        **kwargs
                    )

    output_dir = "/tmp/labsonar/" + get_random_string(10)

    file_map_list = manager.eval_dir(input_dir=input_dir, output_dir=output_dir, extension=extension)

    dfs = []
    for file_map in tqdm(file_map_list, desc='Files', leave=False):
        class_id = extract_class(file_map['input'])
        file_id = extract_file_id(file_map['input'])

        data = tifffile.imread(file_map['output'])
        data = data.T

        df_file = pd.DataFrame(data, columns=[f"feature_{i}" for i in range(data.shape[1])])
        df_file["file_id"] = file_id
        df_file["class_id"] = class_id

        dfs.append(df_file)

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(output_filename, index=False)