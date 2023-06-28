function [S_dB, freqs, times] = melgram(data, fs, n_fft, n_mels, decimation_rate)
    if nargin < 3
        n_fft = 512;
    end
    if nargin < 4
        n_mels = 32;
    end
    if nargin < 5
        decimation_rate = 2;
    end

    if decimation_rate>1
        data=decimate(data, decimation_rate);
        fs=fs/decimation_rate;
    end

    fmax = fs/2;
    data = normalize(data,1);

    [S, freqs , times] = melSpectrogram(data, ...
                                fs, ...
                                'Window', hanning(n_fft), ...
                                'OverlapLength',0, ...
                                'FFTLength',n_fft, ...
                                'SpectrumType', 'magnitude', ...
                                'NumBands', n_mels, ...
                                'FrequencyRange', [0 fmax] ...
                            );
    S_dB = pow2db(S);
end