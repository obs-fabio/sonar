classdef FIR
    %FIR: FIR Design Techniques.
    %   - Taps: just input the taps in a float vector
    %   - DesignPC: the technique of design FIR filters using Parks McClelan
    %   algorithm.
    %   - DesignWindowing: the simpliest technique of design FIR filters
    %   using windows multiplication in time. The possible windows are
    %   rectangular, hamming, hanning, blackman, kaiser, and bartlett.
    methods (Static)
        function test = testando(x,x2)
           test = x+x2; 
        end
        function Taps(filterObj, filterParams)
           filterObj.taps = filterParams.taps; 
        end
        function DesignPC(filterObj, filterParams)
            %code
            switch filterParams.freqType
                case FilterType.allpass
                    %code
                case FilterType.bandpass
                    %code
                case FilterType.bandstop
                    %code
                case FilterType.highpass
                    %code
                case FilterType.lowpass
                    %code
                case FilterType.notch
                    %code
                case FilterType.none

            end
        end
        function DesignWindowing(filterObj, filterParams)
            %code
            switch filterParams.window
                case WindowType.rectangular
                    %code
                case WindowType.hamming
                    %code
                case WindowType.hanning
                    %code
                case WindowType.blackman
                    %code
                case WindowType.kaiser
                    %code
                case FilterType.notch
                    %code
                case WindowType.none
                    %code
            end
            switch filterParams.freqType
                case FilterType.allpass
                    %code
                case FilterType.bandpass
                    %code
                case FilterType.bandstop
                    %code
                case FilterType.highpass
                    %code
                case FilterType.lowpass
                    %code
                case FilterType.notch
                    %code
                case FilterType.none
                    %code
            end
        end
    end
end