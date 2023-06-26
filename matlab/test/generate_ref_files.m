addpath("matlab/labsonar_sp/")
data_folder="./test_data/";

config = struct();
config.input = 'input.wav';

tpsw_config = struct();
tpsw_config.default = 'tpsw.wav';

args = struct();
args.filename = 'tpsw_512_10_5_3.wav';
args.npts = 512;
args.n = 10;
args.p = 5;
args.a = 3;

tpsw_config.args = args;
config.tpsw = tpsw_config;

info = audioinfo(fullfile(data_folder, config.input));
[y, FS] = audioread(fullfile(data_folder, config.input));

t = tpsw(y);
audiowrite(fullfile(data_folder, tpsw_config.default), t, FS);

t = tpsw(y, args.npts, args.n, args.p, args.a);
audiowrite(fullfile(data_folder, args.filename), t, FS);

fid = fopen(fullfile(data_folder, 'config.json'), 'w');
fwrite(fid, jsonencode(config, PrettyPrint=true), 'char');
fclose(fid);
