function [ALLfeatures_Matrix,ALLfeatures_Global] = calculateALLfeatures2(R_mat, scale_cell, algo_cell, Ng_mat, Histograms_bins, scanType, ALLMask, ALLVolume, nSample)
%UNTITLED3 此处显示有关此函数的摘要
%   此处显示详细说明
ALLfeatures_Matrix = cell( numel(R_mat),numel(scale_cell),numel(algo_cell),numel(Ng_mat),nSample);
ALLfeatures_Global = cell( numel(R_mat),numel(scale_cell),nSample);
% Rweight = numel(scale_cell)*numel(algo_cell)*numel(Ng_mat);
% Sweight = numel(algo_cell)*numel(Ng_mat);
% Aweight = numel(Ng_mat);
% Gweight = numel(scale_cell);
elenum = 0; 
nCal = nSample*numel(R_mat)*numel(scale_cell)*numel(algo_cell)*numel(Ng_mat);
waitbarHandle = waitbar(0,'Please wait...','CreateCancelBtn','setappdata(gcbf,''canceling'',1)');
for j = 1:nSample
%      ALLfeatures_Matrix{r,s,k,l}=ALLMask{j}.PatientID;
%      ALLfeatures_Global{r,j}=ALLMask{j}.PatientID;
     
    for r = 1:numel(R_mat)
        for s = 1:numel(scale_cell) 
            
            ALLfeatures_Global{r,s,j}.T1_Globaltextures = calcGlobal(ALLVolume{j}.T1,ALLMask{j}.T1,scanType,R_mat(r),scale_cell{s},Histograms_bins);
            ALLfeatures_Global{r,s,j}.T1C_Globaltextures = calcGlobal(ALLVolume{j}.T1C,ALLMask{j}.T1C,scanType,R_mat(r),scale_cell{s},Histograms_bins);
            ALLfeatures_Global{r,s,j}.T2_Globaltextures = calcGlobal(ALLVolume{j}.T2,ALLMask{j}.T2,scanType,R_mat(r),scale_cell{s},Histograms_bins);
            
            ALLfeatures_Global{r,s,j}.Parameters= [ num2str(R_mat(r),'%.2f'),'_',num2str(scale_cell{s})];
            ALLfeatures_Global{r,s,j}.PatientID = ALLMask{j}.PatientID;
            for k = 1:numel(algo_cell)
                for l = 1:numel(Ng_mat)
                    
                    [ALLfeatures_Matrix{r,s,k,l,j}.T1_GLCMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1_GLRLMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1_GLSZMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1_NGTDMtextures] = calcMatrix(ALLVolume{j}.T1,ALLMask{j}.T1,scanType,R_mat(r),scale_cell{s},algo_cell{k},Ng_mat(l));
                 
                    [ALLfeatures_Matrix{r,s,k,l,j}.T1C_GLCMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1C_GLRLMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1C_GLSZMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T1C_NGTDMtextures] = calcMatrix(ALLVolume{j}.T1C,ALLMask{j}.T1C,scanType,R_mat(r),scale_cell{s},algo_cell{k},Ng_mat(l));
                 
                    [ALLfeatures_Matrix{r,s,k,l,j}.T2_GLCMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T2_GLRLMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T2_GLSZMtextures,...
                     ALLfeatures_Matrix{r,s,k,l,j}.T2_NGTDMtextures] = calcMatrix(ALLVolume{j}.T2,ALLMask{j}.T2,scanType,R_mat(r),scale_cell{s},algo_cell{k},Ng_mat(l));

                    
                    ALLfeatures_Matrix{r,s,k,l,j}.Parameters = [num2str(R_mat(r),'%.2f'),'_',num2str(scale_cell{s}),'_',algo_cell{k},'_',num2str(Ng_mat(l))];
                    ALLfeatures_Matrix{r,s,k,l,j}.PatientID = ALLMask{j}.PatientID;
                    if getappdata(waitbarHandle,'canceling')
                        delete(waitbarHandle)
                        return
                    end
                    elenum = elenum+1;
                    waitbar(elenum/nCal,waitbarHandle,['Sample: ',num2str(j),' of ',num2str(nSample),'     ','Experiment: ',num2str(elenum),' of ',num2str(nCal)]);
                end
            end
        end
    end
end
delete(waitbarHandle)
fprintf('\n\n******************* Features Extraction Successfully!*******************\nSample ID:\n');
for m = 1:nSample
    fprintf('%s ',ALLMask{m}.PatientID);
end
fprintf('\n');
end

