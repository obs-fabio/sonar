from enum import Enum
import numpy as np
import scipy.signal as sci
import librosa


def normalize(x, type=0):
    if type == 0: # normalize between 0 and 1
        return (x - np.min(x, axis=0))/(np.max(x, axis=0) - np.min(x, axis=0))
    if type == 1: # normalize -1 e 1, keeping 0 in place (librosa.util.normalize)
        return x/np.max(np.abs(x), axis=0)
    if type == 2:
        return x/np.linalg.norm(x, axis=0)
    raise UnboundLocalError("normalization {:d} not implemented".format(type))

def tpsw(x, npts=None, n=None, p=None, a=None):
    if x.ndim == 1:
        x = x[:, np.newaxis]
    if npts is None:
        npts = x.shape[0]
    else:
        x = x[:npts, :]
    if n is None:
        n=int(round(npts*.04/2.0+1))
    if p is None:
        p =int(round(n / 8.0 + 1))
    if a is None:
        a = 2.0
    if p>0:
        h = np.concatenate((np.ones((n-p+1)), np.zeros(2 * p-1), np.ones((n-p+1))))
    else:
        h = np.ones((1, 2*n+1))
        p = 1

    h /= np.linalg.norm(h, 1)
    def apply_on_spectre(xs):
        return sci.convolve(h, xs, mode='full')
    mx = np.apply_along_axis(apply_on_spectre, arr=x, axis=0)

    ix = int(np.floor((h.shape[0] + 1)/2.0))
    mx = mx[ix-1:npts+ix-1]
    ixp = ix - p
    mult=2*ixp/np.concatenate([np.ones(p-1)*ixp, range(ixp,2*ixp + 1)], axis=0)[:, np.newaxis]
    mx[:ix,:] = mx[:ix,:]*(np.matmul(mult, np.ones((1, x.shape[1]))))
    mx[npts-ix:npts,:]=mx[npts-ix:npts,:]*np.matmul(np.flipud(mult),np.ones((1, x.shape[1])))

    indl = (x-a*mx) > 0
    x = np.where(indl, mx, x)
    mx = np.apply_along_axis(apply_on_spectre, arr=x, axis=0)
    # mx = sci.convolve2d(h, x, mode='valid')
    mx=mx[ix-1:npts+ix-1,:]
    mx[:ix,:]=mx[:ix,:]*(np.matmul(mult,np.ones((1, x.shape[1]))))
    mx[npts-ix:npts,:]=mx[npts-ix:npts,:]*(np.matmul(np.flipud(mult),np.ones((1,x.shape[1]))))
    return mx

def spectrogram(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1, **kwargs):

    data = data - np.mean(data)

    n_pts = n_pts * 2
    if n_overlap < 1:
        n_overlap = np.floor(n_pts * n_overlap)
    else:
        n_overlap = n_overlap * 2

    if decimation_rate > 1:
        data = sci.decimate(data, decimation_rate)
        Fs = fs/decimation_rate
    else:
        data = data
        Fs=fs

    freq, time, power = sci.spectrogram(data,
                                    nfft=n_pts,
                                    fs=Fs,
                                    window=np.hanning(n_pts),
                                    noverlap=n_overlap,
                                    detrend=False,
                                    scaling='spectrum',
                                    mode='complex')
    power = np.abs(power)*n_pts/2
    power = power[1:,:]
    freq = freq[1:]
    return power, freq, time

def log_spectrogram(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1, **kwargs):

    power, freq, time = spectrogram(data, fs, n_pts, n_overlap, decimation_rate)
    aux = power
    power[power == 0] = 1e-9
    power = 20*np.log10(power)

    return power, freq, time

def lofar(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1, **kwargs):

    power, freq, time = log_spectrogram(data, fs, n_pts, n_overlap, decimation_rate)
    power = power - tpsw(power)
    aux = power
    power[power < -0.2] = 0
    return power, freq, time

def melgram(data, fs, n_pts=1024, n_overlap=0, n_mels=256, decimation_rate=1, **kwargs):

    n_fft=n_pts*2
    n_overlap *= 2
    hop_length=n_fft-n_overlap
    discard=int(np.floor(n_fft/hop_length))

    normalize_id = kwargs.get('norm', 1)

    if decimation_rate > 1:
        data = sci.decimate(data, decimation_rate)
        fs = fs/decimation_rate

    fmax=fs/2
    n_data = normalize(data, normalize_id).astype(float)
    S = librosa.feature.melspectrogram(
                    y=n_data,
                    sr=fs,
                    n_fft=n_fft,
                    hop_length=hop_length,
                    win_length=n_fft,
                    window=np.hanning(n_fft),
                    n_mels=n_mels,
                    power=2,
                    fmax=fmax)
    S_dB = librosa.power_to_db(S, ref=np.max)
    S_dB = S_dB[:,discard:]

    freqs = librosa.core.mel_frequencies(n_mels=n_mels, fmin=0.0, fmax=fmax)

    start_time = n_pts/fs
    step_time = (n_fft-n_overlap)/fs
    times = [start_time + step_time * valor for valor in range(S_dB.shape[1])]
    return S_dB, freqs, times


class Analysis(Enum): 
    SPECTROGRAM = 1
    LOG_SPECTROGRAM = 2
    LOFAR = 3
    LOFARGRAM = 3
    MELGRAM = 4

    def __str__(self):
        return str(self.name).split('.')[-1].lower()

    def eval(self, *args, **kwargs):
        return globals()[self.__str__()](*args, **kwargs)