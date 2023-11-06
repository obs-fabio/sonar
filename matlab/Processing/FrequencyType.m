classdef (Sealed) FrequencyType
    % FILTERTYPE: An Enum Class for the type of digital filtering. It 
    % determines how the design method will procedure to make the filter 
    % properties.
    %   - allpass: to make designable filters for equalization purpose.
    %   - bandpass: Filter design in frequency domain, with 7 parameters,
    %   2 for ripples in pass and stop bands, 4 for the frequency intervals
    %   and 1 for filter order.
    %   - bandstop: similar to bandpass but the conjugated.
    %   - highpass: Filter design in frequency domain, with 5 parameters,
    %   2 for ripples in pass and stop bands, 2 for the frequency intervals
    %   and 1 for filter order.
    %   - lowpass: similar to highpass but the conjugated.
    %   - none: only need the digital filter parameters.
    enumeration
        allpass,
        bandpass,
        bandstop,
        highpass,
        lowpass,
        notch,
        none,
    end
end