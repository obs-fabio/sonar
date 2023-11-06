classdef Filter < handle
    %FILTER: An abtract class for designing Digital Filters
    %   The filter can be FIR_Filter or IIR_Filter inherited from FILTER.
    %   The Filter can be designed by characteristics in Angular Frequency,
    %   such as the 'enum classes' allpass, bandpass, bandstop, highpass,
    %   lowpass, and none.
    %
    %AGO2023 IPqM-GSAS, Alcantara.
    properties (Abstract)
    end
    methods (Abstract)
%         design(designMethod, filterParams) 
        apply(obj, data)
    end
end

