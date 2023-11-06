wc = pi/4;
%filter order (Oppenheim PDS Book)
M = 21;
n = 0:M;
h = sin(wc*(n-M/2))./(pi*(n-M/2));
freqz(h,1,2^10);

w0 = pi/6;
w1 = pi/3;
N = 200;
n = 0:N-1;
x = cos(w0*n) + cos(w1*n);
y = filter(h,1,x);