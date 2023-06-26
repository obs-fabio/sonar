import numpy as np
import scipy.signal as sci

def normalize(x, type=0):
    if type==0:
        return (x - np.min(x, axis=0))/(np.max(x, axis=0) - np.min(x, axis=0))
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
        h = np.concatenate((np.ones((n-p+1)), np.zeros(2 * p-1), np.ones((n-p+1))), axis=None)
    else:
        h = np.ones((1, 2*n+1))
        p = 1

    h /= np.linalg.norm(h, 1)
    def apply_on_spectre(xs):
        return sci.convolve(h, xs, mode='full')

    mx = np.apply_along_axis(apply_on_spectre, arr=x, axis=0)
    ix = int(np.floor((h.shape[0] + 1)/2.0)) # Defasagem do filtro
    mx = mx[ix-1:npts+ix-1] # Corrige da defasagem
    # Corrige os pontos extremos do espectro
    ixp = ix - p
    mult=2*ixp/np.concatenate([np.ones(p-1)*ixp, range(ixp,2*ixp + 1)], axis=0)[:, np.newaxis] # Correcao dos pontos extremos
    mx[:ix,:] = mx[:ix,:]*(np.matmul(mult, np.ones((1, x.shape[1])))) # Pontos iniciais
    mx[npts-ix:npts,:]=mx[npts-ix:npts,:]*np.matmul(np.flipud(mult),np.ones((1, x.shape[1]))) # Pontos finais

    # Elimina picos para a segunda etapa da filtragem
    #indl= np.where((x-a*mx) > 0) # Pontos maiores que a*mx
    indl = (x-a*mx) > 0
    #x[indl] = mx[indl]
    x = np.where(indl, mx, x)
    mx = np.apply_along_axis(apply_on_spectre, arr=x, axis=0)
    mx=mx[ix-1:npts+ix-1,:]
    #Corrige pontos extremos do espectro
    mx[:ix,:]=mx[:ix,:]*(np.matmul(mult,np.ones((1, x.shape[1])))) # Pontos iniciais
    mx[npts-ix:npts,:]=mx[npts-ix:npts,:]*(np.matmul(np.flipud(mult),np.ones((1,x.shape[1])))) # Pontos finais
    return mx

def spectogram(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1):

    n_pts = n_pts * 2
    if n_overlap < 1:
        n_overlap = np.floor(n_pts * n_overlap)
    else:
        n_overlap = n_overlap * 2

    if decimation_rate > 1:
        dec_data = sci.decimate(data, decimation_rate, 10, 'fir', zero_phase=True)
        Fs = fs/decimation_rate
    else:
        dec_data = data
        Fs=fs

    freq, time, power = sci.spectrogram(dec_data,
                                    window=('hann'),
                                    nperseg=n_pts,
                                    noverlap=n_overlap,
                                    nfft=n_pts,
                                    fs=Fs,
                                    detrend=False,
                                    axis=0,
                                    scaling='spectrum',
                                    mode='magnitude')

    return power, freq, time

def log_spectogram(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1):

    power, freq, time = spectogram(data, fs, n_pts, n_overlap, decimation_rate)
    power = np.absolute(power)
    power[power == 0] = 1e-9
    power = 20*np.log10(power)

    return power, freq, time

def lofar(data, fs, n_pts=1024, n_overlap=0, decimation_rate=1):

    power, freq, time = log_spectogram(data, fs, n_pts, n_overlap, decimation_rate)
    power = power - tpsw(power)
    power[power < -0.2] = 0

    return power, freq, time
