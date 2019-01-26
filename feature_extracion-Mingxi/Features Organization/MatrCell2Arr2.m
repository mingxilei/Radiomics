function [array,param] = MatrCell2Arr2(Stru,type)
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
array = zeros(40,1);
param = cell(40,1);
Matri = {'GLCM','GLRLM','GLSZM','NGTDM'};
if strcmp(type,'T1')   
    Matr = {'T1_GLCMtextures','T1_GLRLMtextures','T1_GLSZMtextures','T1_NGTDMtextures'};
    fieldname = cell(length(Matr),1);
    for k = 1:4
        fieldname{k} = fieldnames(Stru.(Matr{k}));
    end
    a = 1;
    for j = 1:4
        for i = 1:length(fieldname{j})
            array(a,1) = Stru.(Matr{j}).(fieldname{j}{i});
            param{a,1} = [Stru.PatientID,'_',Matri{j},'_',fieldname{j}{i},'_',Stru.Parameters];
            a = a+1;
        end
    end
end
if strcmp(type,'T1C')
    Matr = {'T1C_GLCMtextures','T1C_GLRLMtextures','T1C_GLSZMtextures','T1C_NGTDMtextures'};
    fieldname = cell(length(Matr),1);
    for k = 1:4
        fieldname{k} = fieldnames(Stru.(Matr{k}));
    end
    a = 1;
    for j = 1:4        
        for i = 1:length(fieldname{j})
            array(a,1) = Stru.(Matr{j}).(fieldname{j}{i});
            param{a,1} = [Stru.PatientID,'_',Matri{j},'_',fieldname{j}{i},'_',Stru.Parameters];
            a = a+1;
        end
    end
end
if strcmp(type,'T2')
    Matr = {'T2_GLCMtextures','T2_GLRLMtextures','T2_GLSZMtextures','T2_NGTDMtextures'};
    fieldname = cell(length(Matr),1);
    for k = 1:4
        fieldname{k} = fieldnames(Stru.(Matr{k}));
    end
    a = 1;
    for j = 1:4        
        for i = 1:length(fieldname{j})
            array(a,1) = Stru.(Matr{j}).(fieldname{j}{i});
            param{a,1} = [Stru.PatientID,'_',Matri{j},'_',fieldname{j}{i},'_',Stru.Parameters];
            a = a+1;
        end
    end
end
end

