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
        function test_tpsw(testCase)
            config_file = fullfile(testCase.source_folder, 'config.json');
            test_config = jsondecode(fileread(config_file));
            
            [input, ~] = audioread(fullfile(testCase.source_folder, test_config.input));
            [tpsw_default, ~] = audioread(fullfile(testCase.source_folder, test_config.tpsw.default));
            args = test_config.tpsw.args;
            [tpsw_alt, ~] = audioread(fullfile(testCase.source_folder, args.filename));
            
            tpsw_default = tpsw_default(:, 1);
            tpsw_alt = tpsw_alt(:, 1);
            
            py_tpsw_default = tpsw(input);
            py_tpsw_alt = tpsw(input, args.npts, args.n, args.p, args.a);
            
            defaul_diff = nnz(py_tpsw_default - tpsw_default > 1);
            alt_diff = nnz(py_tpsw_alt - tpsw_alt > 1);
            
            testCase.verifyEqual(defaul_diff, 0);
            testCase.verifyEqual(alt_diff, 0);
        end
    end
end