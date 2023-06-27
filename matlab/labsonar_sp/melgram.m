function [S_dB, freqs, times] = melgram(data, fs, n_mels, decimation_rate)
    if nargin < 3
        n_mels = 128;
    end
    if nargin < 4
        decimation_rate = 1;
    end

    fmax = fs/2/decimation_rate;
    data = normalize(data,1);
    [S, freqs , times] = melSpectrogram(data, fs, 'NumBands', n_mels, 'FrequencyRange', [0 fmax]);
    S_dB = pow2db(S);
end