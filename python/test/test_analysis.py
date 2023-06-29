import unittest, os, json
import numpy as np
import pandas as pd
import scipy.io.wavfile as wavfile
import skimage.io as skimage
import matplotlib.pyplot as plt

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
        input = input.astype(np.float32)/(32767)
        _, tpsw_default = wavfile.read(os.path.join(source_folder, test_config["tpsw"]["default"]))
        tpsw_default = tpsw_default.astype(np.float32)/(32767)
        args = test_config["tpsw"]["args"]
        _, tpsw_alt = wavfile.read(os.path.join(source_folder, args["filename"]))
        tpsw_alt = tpsw_alt.astype(np.float32)/(32767)

        if tpsw_default.ndim == 1:
            tpsw_default = tpsw_default[:, np.newaxis]
        if tpsw_alt.ndim == 1:
            tpsw_alt = tpsw_alt[:, np.newaxis]

        py_tpsw_default = sp.tpsw(input)
        py_tpsw_alt = sp.tpsw(input, args["npts"], args["n"], args["p"], args["a"])

        default_diff = np.count_nonzero(np.abs(np.subtract(py_tpsw_default,tpsw_default) > 1e-3))
        default_diff = default_diff/py_tpsw_default.size
        alt_diff = np.count_nonzero(np.abs(np.subtract(py_tpsw_alt,tpsw_alt) > 1e-3))
        alt_diff = alt_diff/py_tpsw_alt.size

        print("-TPSW(error > 1e-3) < 5\%")
        print("\tdefault: ", default_diff)
        print("\targs: ", alt_diff)

        self.assertTrue(default_diff < 0.05)
        self.assertTrue(alt_diff < 0.05)

    def test_spectrogram(self):
        source_folder=find_source_folder()

        with open(os.path.join(source_folder,"config.json"), 'r') as f:
            test_config = json.load(f)

        fs, input = wavfile.read(os.path.join(source_folder, test_config["input"]))
        input = input.astype(np.float32)/(32767)
        spectrogram_default = skimage.imread(os.path.join(source_folder, test_config['spectrogram']['default']))

        py_spectrogram_default, _, _ = sp.spectrogram(input[:,0], fs)
        py_spectrogram_default = sp.normalize(py_spectrogram_default)


        default_diff = np.count_nonzero(np.abs(np.subtract(py_spectrogram_default, spectrogram_default) > 1e-3))
        default_diff = default_diff/spectrogram_default.size

        print("-Spectrogram(error > 1e-3) < 5\%")
        print("\tdefault: ", default_diff)

        self.assertTrue(default_diff < 0.05)


    def test_lofar(self):
        source_folder=find_source_folder()

        with open(os.path.join(source_folder,"config.json"), 'r') as f:
            test_config = json.load(f)

        fs, input = wavfile.read(os.path.join(source_folder, test_config["input"]))
        input = input.astype(np.float32)/(32767)
        lofar_default = skimage.imread(os.path.join(source_folder, test_config['lofar']['default']))
        args = test_config['lofar']['args']
        lofar_alt = skimage.imread(os.path.join(source_folder, args['filename']))

        py_lofar_default, _, _ = sp.lofar(input[:,0], fs)
        py_lofar_default = sp.normalize(py_lofar_default).T
        py_lofar_alt, _, _ = sp.lofar(input[:,0], fs, args["npts"], args["novr"], args["decimation"])
        py_lofar_alt = sp.normalize(py_lofar_alt).T

        default_diff = np.count_nonzero(np.abs(np.subtract(py_lofar_default, lofar_default) > 1e-3))
        default_diff = default_diff/py_lofar_default.size
        alt_diff = np.count_nonzero(np.abs(np.subtract(py_lofar_alt, lofar_alt) > 1e-3))
        alt_diff = alt_diff/py_lofar_alt.size

        print("-LOFAR(error > 1e-3) < 5\%")
        print("\tdefault: ", default_diff)
        print("\targs: ", alt_diff)

        self.assertTrue(default_diff < 0.05)
        self.assertTrue(alt_diff < 0.05)

    def test_melgrama(self):
        source_folder=find_source_folder()

        with open(os.path.join(source_folder,"config.json"), 'r') as f:
            test_config = json.load(f)

        fs, input = wavfile.read(os.path.join(source_folder, test_config["input"]))
        mel_default = skimage.imread(os.path.join(source_folder, test_config['mel']['default']))
        args = test_config['mel']['args']
        mel_alt = skimage.imread(os.path.join(source_folder, args['filename']))

        py_mel_default, _, _ = sp.melgrama(input[:,0], fs)
        py_mel_default = sp.normalize(py_mel_default)
        py_mel_args, _, _  = sp.melgrama(input[:,0], fs, args['n_mels'], args['decimation'])
        py_mel_args = sp.normalize(py_mel_args)

        default_diff = np.count_nonzero(np.abs(np.subtract(py_mel_default, mel_default) > 1e-3))
        default_diff = default_diff/mel_default.size
        alt_diff = np.count_nonzero(np.abs(np.subtract(py_mel_args, mel_alt) > 1e-3))
        alt_diff = alt_diff/mel_alt.size

        print("-Melgrama(error > 1e-3) < 5\%")
        print("\tdefault: ", default_diff)
        print("\targs: ", alt_diff)

        self.assertTrue(default_diff < 0.05)
        self.assertTrue(alt_diff < 0.05)

if __name__ == '__main__':
    test = TestAnalysis()
    test.test_tpsw()
    test.test_spectrogram()
    test.test_lofar()
    test.test_melgrama()