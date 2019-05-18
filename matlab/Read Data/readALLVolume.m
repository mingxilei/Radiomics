function Volume = readALLVolume ( folder )
% subdir  = dir( mdir );
waitbarHandle = waitbar(0,'Loading DICOM files...','WindowStyle','modal');
nSample = length(folder);
elementNum = 0;
subdir = cell(1,nSample);
Volume = cell(1,nSample);
for i=1:nSample
    subdir{i}=dir(folder{i});
end
for i = 1 : nSample
    for j = 1:length(subdir{i})
        if( isequal( subdir{ i }(j).name, '.' )||...
                isequal( subdir{ i }(j).name, '..')||...
                ~subdir{ i }(j).isdir)               % 如果不是目录则跳过
            continue;
        end
        %     if M_data_num==num
        %         break;
        %     end
        subdir2 = fullfile( folder{i}, subdir{ i }(j).name,'*.dcm' );
        mat = dir(subdir2);
        %     for k = 1:length(subdir2path)
        %         if( isequal( subdir2path( k ).name, '.' )||...
        %                 isequal( subdir2path( k ).name, '..'))               % 如果不是目录则跳过
        %             continue;
        %         end
        %         subdir3path = fullfile( mdir, subdir( i ).name, subdir2path( k ).name, '*.dcm' );
        %         mat = dir( subdir3path );               % 子文件夹下找后缀为dcm的文件
        if ~isempty(mat)
            DICOMpath = fullfile( folder{i}, subdir{ i }(j).name);
            if strcmp(subdir{ i }(j).name,'T1')
                temp=readDICOMdir(DICOMpath,0);
                Volume{elementNum+1}.PatientID = temp{3}.PatientID;
                Volume{elementNum+1}.T1.Volume = temp{2}.scan.volume;
                Volume{elementNum+1}.T1.pixelW = temp{2}.scan.pixelW;
                Volume{elementNum+1}.T1.sliceS = temp{2}.scan.sliceS;
                
            elseif strcmp(subdir{ i }(j).name,'T2')
                temp=readDICOMdir(DICOMpath,0);
                Volume{elementNum+1}.T2.Volume = temp{2}.scan.volume;
                Volume{elementNum+1}.T2.pixelW = temp{2}.scan.pixelW;
                Volume{elementNum+1}.T2.sliceS = temp{2}.scan.sliceS;
                
            elseif strcmp(subdir{ i }(j).name,'T1C')
                temp=readDICOMdir(DICOMpath,0);
                Volume{elementNum+1}.T1C.Volume = temp{2}.scan.volume;
                Volume{elementNum+1}.T1C.pixelW = temp{2}.scan.pixelW;
                Volume{elementNum+1}.T1C.sliceS = temp{2}.scan.sliceS;
                
            end
            if length(fieldnames(Volume{elementNum+1}))==4
                elementNum=elementNum+1;
                waitbar(elementNum/nSample,waitbarHandle);
            end
        end
        %     end
    end
end
close(waitbarHandle)
end