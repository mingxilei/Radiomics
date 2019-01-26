clear
tic
%% Extraction Parameter
R_mat = [1/2,2/3,1,3/2,2];
scale_cell = {'pixelW',1,2,3,4,5};
algo_cell = {'Equal'};
Ng_mat = [8,16,32,64];
Histograms_bins = 100;
scanType = 'MRscan';
%% Addpath
mname = mfilename;
mpath = mfilename('fullpath');
mdir = mpath(1:end-length(mname));
cd(mdir);
addpath(genpath(mdir))
%% Choose folder
[pathname] = uigetdir2(pwd, 'Ñ¡ÔñÑù±¾');
if isempty(pathname)
    return
end
%% read ALL sample
ALLMask = readALLMask (pathname);
ALLVolume = readALLVolume (pathname);
nSample = length(ALLMask);
%% Data Checking
check = dataChecking(ALLVolume,ALLMask,nSample);
if check
    return
end
% check = twoDcheck(ALLMask);
fprintf('\n*********************** Reading Successfully!***********************\n Sample Size: %d\n',nSample);
%% Features Extraction
[ALLfeatures_Matrix,ALLfeatures_Global] = calculateALLfeatures2(R_mat, scale_cell, algo_cell, Ng_mat, Histograms_bins, scanType, ALLMask, ALLVolume, nSample);
%% Features Organization
[T1,T1C,T2,T1_para,T1C_para,T2_para] = organaizefeatures2(ALLfeatures_Global, ALLfeatures_Matrix);
T = toc;
fprintf('\ntotal time: %f\n',T);