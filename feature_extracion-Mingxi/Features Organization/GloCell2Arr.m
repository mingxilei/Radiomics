function [array,param] = GloCell2Arr(Stru,type,para)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
array = zeros(3,1);
param = cell(3,1);
if strcmp(type,'T1')
    array(1,1)= Stru.T1_Globaltextures.Variance;
    array(2,1)= Stru.T1_Globaltextures.Skewness;
    array(3,1)= Stru.T1_Globaltextures.Kurtosis;
    param{1,1}= ['Global_Variance_',para];
    param{2,1}= ['Global_Variance_',para];
    param{3,1}= ['Global_Variance_',para];
end
if strcmp(type,'T1C')
    array(1,1)= Stru.T1C_Globaltextures.Variance;
    array(2,1)= Stru.T1C_Globaltextures.Skewness;
    array(3,1)= Stru.T1C_Globaltextures.Kurtosis;
    param{1,1}= ['Global_Variance_',para];
    param{2,1}= ['Global_Variance_',para];
    param{3,1}= ['Global_Variance_',para];
end
if strcmp(type,'T2')
    array(1,1)= Stru.T2_Globaltextures.Variance;
    array(2,1)= Stru.T2_Globaltextures.Skewness;
    array(3,1)= Stru.T2_Globaltextures.Kurtosis;
    param{1,1}= ['Global_Variance_',para];
    param{2,1}= ['Global_Variance_',para];
    param{3,1}= ['Global_Variance_',para];
end
end

