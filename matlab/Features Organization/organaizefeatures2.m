function [T1,T1C,T2,T1para,T1Cpara,T2para] = organaizefeatures2(ALLfeatures_Global, ALLfeatures_Matrix)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
nSample = size(ALLfeatures_Global,3);

T1 = [];        T1para = [];
T1C = [];       T1Cpara = [];
T2 = [];        T2para = [];
for n = 1:nSample
    T1_array = [];      T1_para = [];
    T1C_array = [];     T1C_para = [];
    T2_array = [];      T2_para = [];
    for r = 1:size(ALLfeatures_Global,1)
        for s = 1:size(ALLfeatures_Global,2)
            [temp1,temp2] = GloCell2Arr2(ALLfeatures_Global{r,s,n},'T1');
            T1_array = [T1_array;temp1];
            T1_para = [T1_para;temp2];
            [temp1,temp2] = GloCell2Arr2(ALLfeatures_Global{r,s,n},'T1C');
            T1C_array = [T1C_array;temp1];
            T1C_para = [T1C_para;temp2];
            [temp1,temp2] = GloCell2Arr2(ALLfeatures_Global{r,s,n},'T2');
            T2_array = [T2_array;temp1];
            T2_para = [T2_para;temp2];
        end
    end
    for r = 1:size(ALLfeatures_Matrix,1)
        for s = 1:size(ALLfeatures_Matrix,2)
            for k = 1:size(ALLfeatures_Matrix,3)
                for l = 1:size(ALLfeatures_Matrix,4)
                    [temp1,temp2] = MatrCell2Arr2(ALLfeatures_Matrix{r,s,k,l,n},'T1');
                    T1_array = [T1_array;temp1];
                    T1_para = [T1_para;temp2];
                    [temp1,temp2] = MatrCell2Arr2(ALLfeatures_Matrix{r,s,k,l,n},'T1C');
                    T1C_array = [T1C_array;temp1];
                    T1C_para = [T1C_para;temp2];
                    [temp1,temp2] = MatrCell2Arr2(ALLfeatures_Matrix{r,s,k,l,n},'T2');
                    T2_array = [T2_array;temp1];
                    T2_para = [T2_para;temp2];
                end
            end
        end
    end
    T1 = [T1 T1_array];         T1para = [T1para T1_para];
    T1C = [T1C T1C_array];      T1Cpara = [T1Cpara T1C_para];
    T2 = [T2 T2_array];         T2para = [T2para T2_para];
end
end

