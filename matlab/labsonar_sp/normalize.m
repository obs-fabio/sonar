function y=normalize(x, type)
    if nargin < 2
        type = 0;
    end
    
    switch type
        case 0 % normalize between 0 and 1
            y = (x - min(x))./(max(x) - min(x));
        case 1 % normalize -1 e 1, keeping 0 in place (librosa.util.normalize)
            y = x./max(abs(x));
        otherwise
            disp('not implemented')
    end

    
