%%
addpath("matlab/labsonar_sp/")
data_folder="./test_data/";

config = struct();
config.input = 'input.wav';

% TPSW
tpsw_config = struct();
tpsw_config.default = 'tpsw.wav';

args = struct();
args.filename = 'tpsw_args.wav';
args.npts = 512;
args.n = 10;
args.p = 5;
args.a = 3;

tpsw_config.args = args;
config.tpsw = tpsw_config;


% SPECTOGRAM
spectrogram_config = struct();
spectrogram_config.default = 'spectrogram.tiff';
config.spectrogram = spectrogram_config;

% LOFAR
lofar_config = struct();
lofar_config.default = 'lofar.tiff';

lofar_args = struct();
lofar_args.filename = 'lofar_args.tiff';
lofar_args.npts = 2048;
lofar_args.novr = 2048-128;
lofar_args.decimation = 5;
lofar_args.fmax = 44100/2/lofar_args.decimation;

lofar_config.args = lofar_args;
config.lofar = lofar_config;

% MELGRAM
mel_config = struct();
mel_config.default = 'mel.tiff';

mel_args = struct();
mel_args.filename = 'mel_args.tiff';
mel_args.n_mels = 64;
mel_args.decimation = 5;

mel_config.args = mel_args;
config.mel = mel_config;


% saving JSON

fid = fopen(fullfile(data_folder, 'config.json'), 'w');
fwrite(fid, jsonencode(config, PrettyPrint=true), 'char');
fclose(fid);

%%

t = tpsw(y);
audiowrite(fullfile(data_folder, tpsw_config.default), t, FS);

t = tpsw(y, args.npts, args.n, args.p, args.a);
audiowrite(fullfile(data_folder, args.filename), t, FS);

%%
S = custom_spectrogram(fullfile(data_folder, config.input));
S = normalize(S);
export_tiff(S, fullfile(data_folder, spectrogram_config.default))

%%
B = lofar(fullfile(data_folder, config.input));
B = normalize(B)';
export_tiff(B, fullfile(data_folder, lofar_config.default))

B = lofar(fullfile(data_folder, config.input), lofar_args.npts, lofar_args.novr, lofar_args.fmax);
B = normalize(B)';
export_tiff(B, fullfile(data_folder, lofar_args.filename))

%%
info = audioinfo(fullfile(data_folder, config.input));
[y, FS] = audioread(fullfile(data_folder, config.input));

S = melgram(y(:,1), FS);
S = normalize(S);
export_tiff(S, fullfile(data_folder, mel_config.default))

S = melgram(y(:,1), FS, mel_args.n_mels, mel_args.decimation);
S = normalize(S);
export_tiff(S, fullfile(data_folder, mel_args.filename))
