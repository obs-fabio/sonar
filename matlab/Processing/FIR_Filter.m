classdef FIR_Filter < Filter
    % FIR_FILTER: A class that designs a FIR filter and performes filtering
    % process
    properties (Access = ?FIR) %Private, Friend Class FIR
        taps
    end
    methods
        function obj = FIR_Filter(designMethod, filterParams)
            try
                % Validate design technique for FIR Filter
                funcInfo = functions(designMethod);
                if (isfield(funcInfo, 'function') && ~ismethod(FIR(),funcInfo.function(find(funcInfo.function == '.')+1:end)))
%                if ~ismethod(designMethod, 'FIR')
                    error('InvalidDesign', 'Design method must be applied for FIR Filter.');
                else
                    %code
                    designMethod(obj, filterParams);
                end    
            catch exception
                fprintf('An error occurred: %s\n', exception.message);
                delete(obj);
            end
        end
        function filtered_data = apply(obj, data)
            %code
            filtered_data = filter(obj.taps, 1, data);
        end
    end
end
