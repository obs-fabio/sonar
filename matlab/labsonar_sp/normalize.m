function y=normalize(x, type)
    if nargin < 2
        type = 0;
    end
    
    switch type
        case 0
            y = (x - min(x))./(max(x) - min(x));
        otherwise
            disp('not implemented')
    end

    
