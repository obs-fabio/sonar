classdef FilterParams
    %FILTERPARAMS: Filter Parameters depending on Filter Design technique
    %   - order: Filter order.
    %   - delta1: Passband ripple.
    %   - delta2: Stopband ripple.
    %   - wp1: end or start passband of digital frequency in a filter, depending on the FrequencyType of a filter.
    %     If freqType = lowpass => passband = [0 wp1].
    %     If freqType = highpass => passband = [wp1 pi]
    %     If freqType = bandpass => passband = [wp1 wp2] 
    %     If freqType = bandstop => passband = [0 wp1] U [wp2 pi]
    %   - ws1: start or end stopband of digital frequency in a filter, depending on the FrequencyType of a filter.
    %     If freqType = lowpass => stopband = [ws1 pi].
    %     If freqType = highpass => stopband = [0 ws1]
    %     If freqType = bandpass => stopband = [0 ws1] U [ws2 pi] 
    %     If freqType = bandstop => stopband = [ws1 ws2]
    %   - wp2: The same logic proposed in the explanation of wp1, only needed in freqType = bandpass or bandstop.
    %   - ws2: The same logic proposed in the explanation of ws1, only needed in freqType = bandpass or bandstop.
    %   - window: Only needed in FIR filter windowing design project. See the possible windows in WINDOWTYPE.
    %   - f_notch: The digital frequency that need to be rejected.
    properties
        order = [],
        freqType = FrequencyType.none,
        delta1 = [],
        delta2 = [],
        wp1 = [],
        ws1 = [],
        wp2 = [],
        ws2 = [],
        window = WindowType.none,
        f_notch = [],
        taps = [],
        num = [],
        den = [],
    end
end