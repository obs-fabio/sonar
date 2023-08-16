classdef test_analysis < matlab.unittest.TestCase
    
    properties
        source_folder
    end
    
    methods(TestMethodSetup)
        function setup(testCase)
            testCase.source_folder = "./test_data/";
        end
    end
    
    methods(Test)

        function test_filtering_FIR_taps(testCase)
            %code
            %Testar inicialmente para filtro fir, fornecendo os taps, depois comparar com a funcao filter do matlab
            config_file = fullfile(testCase.source_folder, 'config.json');
            test_config = jsondecode(fileread(config_file));

            taps = csvread(fullfile(testCase.source_folder, test_config.filter.h));
            x = csvread(fullfile(testCase.source_folder, test_config.filter.in));
            y = csvread(fullfile(testCase.source_folder, test_config.filter.out));
            
            %need: addpath ./matlab/Processing
            params = FilterParams();
            params.taps = taps;
            test_filter = FIR_Filter(@FIR.Taps, params);

            defaul_diff = nnz(y - test_filter.apply(x) > 1);
            testCase.verifyEqual(defaul_diff, 0);
        end

        function test_tpsw(testCase)
            config_file = fullfile(testCase.source_folder, 'config.json');
            test_config = jsondecode(fileread(config_file));
            
            [input, ~] = audioread(fullfile(testCase.source_folder, test_config.input));
            [tpsw_default, ~] = audioread(fullfile(testCase.source_folder, test_config.tpsw.default));
            args = test_config.tpsw.args;
            [tpsw_alt, ~] = audioread(fullfile(testCase.source_folder, args.filename));
            
            tpsw_default = tpsw_default(:, 1);
            tpsw_alt = tpsw_alt(:, 1);
            
            matlab_tpsw_default = tpsw(input);
            matlab_tpsw_alt = tpsw(input, args.npts, args.n, args.p, args.a);
            
            defaul_diff = nnz(matlab_tpsw_default - tpsw_default > 1);
            alt_diff = nnz(matlab_tpsw_alt - tpsw_alt > 1);
            
            testCase.verifyEqual(defaul_diff, 0);
            testCase.verifyEqual(alt_diff, 0);
        end
        
        function test_lofar(testCase)
            config_file = fullfile(testCase.source_folder, 'config.json');
            test_config = jsondecode(fileread(config_file));
            
            lofar_default = imread(fullfile(testCase.source_folder, test_config.lofar.default));
            args = test_config.lofar.args;
            lofar_alt = imread(fullfile(testCase.source_folder, args.filename));
            
            matlab_lofar_default = lofar(fullfile(testCase.source_folder, test_config.input));
            matlab_lofar_default  = normalize(matlab_lofar_default)';
            matlab_lofar_alt = lofar(fullfile(testCase.source_folder, test_config.input), args.npts, args.novr, args.fmax);
            matlab_lofar_alt = normalize(matlab_lofar_alt)';
            
            defaul_diff = nnz(matlab_lofar_default - lofar_default > 1);
            alt_diff = nnz(matlab_lofar_alt - lofar_alt > 1);
            
            testCase.verifyEqual(defaul_diff, 0);
            testCase.verifyEqual(alt_diff, 0);
        end
    end
end


