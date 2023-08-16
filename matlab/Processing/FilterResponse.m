classdef (Sealed) FilterResponse
    %FILTERRESPONSE: The type of the digital filter response, Finite
    %Impulse Response (FIR) or Infinite Impulse Response (IIR)
    enumeration
        FIR,
        IIR,
    end
end