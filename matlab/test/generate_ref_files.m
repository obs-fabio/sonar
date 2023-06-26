%%
addpath("matlab/labsonar_sp/")
data_folder="./test_data/";

config = struct();
config.input = 'input.wav';

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

fid = fopen(fullfile(data_folder, 'config.json'), 'w');
fwrite(fid, jsonencode(config, PrettyPrint=true), 'char');
fclose(fid);

%%
info = audioinfo(fullfile(data_folder, config.input));
[y, FS] = audioread(fullfile(data_folder, config.input));

t = tpsw(y);
audiowrite(fullfile(data_folder, tpsw_config.default), t, FS);

t = tpsw(y, args.npts, args.n, args.p, args.a);
audiowrite(fullfile(data_folder, args.filename), t, FS);

%%
B = lofar(fullfile(data_folder, config.input));
B = normalize(B)';
export_tiff(B, fullfile(data_folder, lofar_config.default))

B = lofar(fullfile(data_folder, config.input), lofar_args.npts, lofar_args.novr, lofar_args.fmax);
B = normalize(B)';
export_tiff(B, fullfile(data_folder, lofar_args.filename))
