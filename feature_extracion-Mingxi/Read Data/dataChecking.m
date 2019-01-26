function [check] = dataChecking(ALLVolume,ALLMask,nSample)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
check = 0;
waitbarHandle = waitbar(0,'Data Checking...');
for i=1:nSample
%     if ~isequal(size(ALLVolume{i}.T1.Volume),size(ALLMask{i}.T1))||...
%             ~isequal(size(ALLVolume{i}.T2.Volume),size(ALLMask{i}.T2))||...
%             ~isequal(size(ALLVolume{i}.T1C.Volume),size(ALLMask{i}.T1C))||...
%             ~strcmp(ALLMask{i}.PatientID,ALLVolume{i}.PatientID)
%         check=fprintf('size incompatible!  ID = %s No.%d\n',ALLMask{i}.PatientID,i)+check;
%         waitbar(i/nSample,waitbarHandle);
%     end
    if ~isequal(size(ALLVolume{i}.T1.Volume),size(ALLMask{i}.T1))
        fprintf('T1 size mismatch!  ID = %s No.%d\nVolume size: %d %d %d   Mask size: %d %d %d\n',...
                ALLMask{i}.PatientID,i,size(ALLVolume{i}.T1.Volume),size(ALLMask{i}.T1));
        check = 1;
        s = [size(ALLVolume{i}.T1.Volume,1),size(ALLVolume{i}.T1.Volume,2)];
        for j = 1:size(ALLMask{i}.T1,3)
            temp(:,:,j) = imresize(ALLMask{i}.T1(:,:,j),s,'nearest');
        end
        ALLMask{i}.T1 = temp;
%         fprintf('T1 Mask resized\n');
        clear temp
    end
    if ~isequal(size(ALLVolume{i}.T2.Volume),size(ALLMask{i}.T2))
        fprintf('T2 size mismatch!  ID = %s No.%d\nVolume size: %d %d %d   Mask size: %d %d %d\n',...
                ALLMask{i}.PatientID,i,size(ALLVolume{i}.T2.Volume),size(ALLMask{i}.T2));
        check = 1;
        s = [size(ALLVolume{i}.T2.Volume,1),size(ALLVolume{i}.T2.Volume,2)];
        for j = 1:size(ALLMask{i}.T2,3)
            temp(:,:,j) = imresize(ALLMask{i}.T2(:,:,j),s,'nearest');
        end
        ALLMask{i}.T2 = temp;
%         fprintf('T2 Mask resized\n');
        clear temp
    end
    if ~isequal(size(ALLVolume{i}.T1C.Volume),size(ALLMask{i}.T1C))
        fprintf('T1C size mismatch!  ID = %s No.%d\nVolume size: %d %d %d   Mask size: %d %d %d\n',...
                ALLMask{i}.PatientID,i,size(ALLVolume{i}.T1C.Volume),size(ALLMask{i}.T1C));
        check = 1;
        s = [size(ALLVolume{i}.T1C.Volume,1),size(ALLVolume{i}.T1C.Volume,2)];
        for j = 1:size(ALLMask{i}.T1C,3)
            temp(:,:,j) = imresize(ALLMask{i}.T1C(:,:,j),s,'nearest');
        end
        ALLMask{i}.T1C = temp;
%         fprintf('T1C Mask resized\n');
        clear temp
    end
end
close(waitbarHandle)
end

