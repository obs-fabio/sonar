import unittest, os, json
import numpy as np
import pandas as pd
import scipy.io.wavfile as wavfile
import skimage.io as skimage

import labsonar_sp.analysis as sp


def find_source_folder(base_folder = None):
    if base_folder is None:
        base_folder = os.getcwd()

    for _, subfolders, _ in os.walk(base_folder):
        if "test_data" in subfolders:
            return os.path.join(base_folder, "test_data")

        for subfolder in subfolders:
            ret = find_source_folder(os.path.join(base_folder, subfolder))
            if ret is not None:
                return ret
        return None

class TestAnalysis(unittest.TestCase):

    def test_tpsw(self):
        source_folder=find_source_folder()

        with open(os.path.join(source_folder,"config.json"), 'r') as f:
            test_config = json.load(f)

        _, input = wavfile.read(os.path.join(source_folder, test_config["input"]))
        _, tpsw_default = wavfile.read(os.path.join(source_folder, test_config["tpsw"]["default"]))
        args = test_config["tpsw"]["args"]
        _, tpsw_alt = wavfile.read(os.path.join(source_folder, args["filename"]))

        if tpsw_default.ndim == 1:
            tpsw_default = tpsw_default[:, np.newaxis]
        if tpsw_alt.ndim == 1:
            tpsw_alt = tpsw_alt[:, np.newaxis]

        py_tpsw_default = sp.tpsw(input)
        py_tpsw_alt = sp.tpsw(input, args["npts"], args["n"], args["p"], args["a"])

        default_diff = np.count_nonzero(np.subtract(py_tpsw_default,tpsw_default) > 1)
        alt_diff = np.count_nonzero(np.subtract(py_tpsw_alt,tpsw_alt) > 1)

        self.assertTrue(default_diff == 0)
        self.assertTrue(alt_diff == 0)

    def test_lofar(self):
        source_folder=find_source_folder()

        with open(os.path.join(source_folder,"config.json"), 'r') as f:
            test_config = json.load(f)

        fs, input = wavfile.read(os.path.join(source_folder, test_config["input"]))
        lofar_default = skimage.imread(os.path.join(source_folder, test_config['lofar']['default']))
        args = test_config['lofar']['args']
        lofar_alt = skimage.imread(os.path.join(source_folder, args['filename']))

        py_lofar_default, _, _ = sp.lofar(input[:,1], fs)
        py_lofar_default = sp.normalize(py_lofar_default).T
        py_lofar_alt, _, _ = sp.lofar(input[:,1], fs, args["npts"], args["novr"], args["decimation"])
        py_lofar_alt = sp.normalize(py_lofar_alt).T

        default_diff = np.count_nonzero(np.subtract(py_lofar_default, lofar_default) > 1)
        alt_diff = np.count_nonzero(np.subtract(py_lofar_alt, lofar_alt) > 1)

        self.assertTrue(default_diff == 0)
        self.assertTrue(alt_diff == 0)
