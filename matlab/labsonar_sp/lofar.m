function [B,f,t,Et,Bm,nsiz,nbits,fs]=lofar(arquivo,npts,novr,fmax)
%
% [B,f,t,Et,Bm,nsiz,nbits,fs]=lofar(arquivo,npts,novr,fmax)
%
% Faz espectrograma de arquivo .wav
%
% arquivo	= nome do arquivo .wav
% npts		= numero de pontos a serem apresentados (nfft/2) (default=1024)
% novr		= numero de pontos a serem reutilizados (em relacao a npts) (default=0)
% fmax		= frequencia maxima analisada (determina a decimacao do sinal) (default=fs/2)
%
% B			= Matriz com espectrograma normalizado usando tpsw.m e log
% f			= Vetor com escala de frequencia
% t			= Vetor com escala de tempo
% Et		= Vetor com energia de cada espectro
% Bm		= Vetor com espectro medio
% nsiz		= Numero de pontos no arquivo .wav
% nbits		= Numero de bits por amostra no arquivo .wav
% fs		= Frequencia de amostragem do arquivo .wav
%
info = audioinfo(arquivo); % Le infos
nbits = info.BitsPerSample; % Set numero de bits
nsiz = info.TotalSamples; % Set TotalSamples
fs = info.SampleRate; % Set SampleRate
disp([arquivo ' --> size=' num2str(nsiz) ' nbits=' num2str(nbits) ' fs=' num2str(fs)])

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
%nlim=floor(300000/nfft)*nfft*R;

disp(['fs=' num2str(fs) ', fmax=' num2str(fmax) ', npts=' num2str(npts) ', novr=' num2str(novr) ',R=' num2str(R)]);

B=[];
Bm=[];
cnt=[];
Et=[];

y=audioread(arquivo);
y=y(:,1);
y=y-mean(y);
if R>1
	y=decimate(y,R);
end
B=specgram(y,nfft,fs,hanning(nfft),novr);
B=abs(B);
B(B == 0) = 1e-9;
Et=var(B);
Bm=mean(B',1);
%B = B ./ tpsw(B);
B=20*log10(B);
B=B-tpsw(B);
B(find(B<-.2))=0;
f=(0:npts)*fmax/npts;
t=(0:size(B,2)-1)*(npts-novr/2)/fmax;

return

%% Quando tiver problemas com pouca memoria
%% usar o trecho abaixo, em que o espectrograma
%% e' feito por partes.

fid=fopen('flofar.bak','wb');

tic
for i=1:nlim:nsiz
	y=audioread(arquivo,[i min([i+nlim-1 nsiz])]);
	y=y(:,1);	% Apenas canal esquerdo
	y=y-mean(y);
	if R>1
		y=decimate(y,R);
	end
	b=specgram(y,nfft,fs,hanning(nfft),novr);
	b=abs(b);
	Et=[Et var(b)];
	nesp=size(b,2);
	Bm=[Bm;mean(b',1)*nesp];
	cnt=[cnt nesp];
%t	mb=tpsw(b,1025,15,4,2);
%t	B=[B b./mb];
	b=log10(b);
	b=b-tpsw(b);
	b(find(b<-.2))=0;
	fwrite(fid,b,'float');
%	B=[B b];
%	disp(['Trecho ' num2str(floor(i/nlim)+1) ' --> ' num2str(toc)])
end
fclose(fid);
fid=fopen('flofar.bak','rb');
B=fread(fid,'float');
B=reshape(B,npts+1,length(B)/(npts+1));
f=(0:npts)*fmax/npts;
t=(0:size(B,2)-1)*(npts-novr/2)/fmax;

Bm=Bm./sum(cnt);
