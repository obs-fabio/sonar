classdef (Sealed) WindowType
    %WINDOWTYPE: 
    enumeration
        rectangular,
        hamming,
        hanning,
        blackman,
        kaiser,
        bartlett,
        none
    end
end