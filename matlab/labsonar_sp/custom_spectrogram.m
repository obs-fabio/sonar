function [B]=custom_spectrogram(arquivo,npts,novr,fmax)

    info = audioinfo(arquivo); % Le infos
    fs = info.SampleRate; % Set SampleRate

    if (nargin<2) || isempty(npts)
        npts=1024;
    end
    if (nargin<3) || isempty(novr)
        novr=0;
    end
    if (nargin<4) || isempty(fmax)
        fmax=fs/2;
    end
    nfft=npts*2;
    if novr < 1
        novr=floor(nfft*novr);
    else
        novr=novr*2;
    end
    if fmax > fs/2
        disp('fmax > fs/2 -> corrigindo para fs/2')
        fmax=fs/2;
    end
    R=floor(fs/2/fmax);
    fs=fs/R;
    fmax=fs/2;

    disp(['fs=' num2str(fs) ', fmax=' num2str(fmax) ', npts=' num2str(npts) ', novr=' num2str(novr) ',R=' num2str(R)]);

    y=audioread(arquivo);
    y=y(:,1);
    y=y-mean(y);
    if R>1
        y=decimate(y,R);
    end
    B=specgram(y,nfft,fs,hanning(nfft),novr);
    B=abs(B);
