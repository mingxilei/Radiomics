function Mdata = readALLMask ( folder )
% subdir  = dir( mdir );
waitbarHandle = waitbar(0,'Loading MAT files...','WindowStyle','modal');
nSample = length(folder);
elementNum = 0;
subdir = cell(1,nSample);
Mdata = cell(1,nSample);
for i=1:nSample
    subdir{i}=dir(folder{i});
end
for i = 1 : nSample
    %     for j = 1:length(subdir{i})
    %     if( isequal( subdir{ i }(j).name, '.' )||...
    %             isequal( subdir{ i }(j).name, '..')||...
    %             subdir{ i }(j).isdir)               % 如果不是目录则跳过
    %         continue;
    %     end
    %     if M_data_num==num
    %         break;
    %     end
    subdirpath = fullfile( folder{i},'*.mat' );
    mat = dir( subdirpath );               % 子文件夹下找后缀为mat的文件
    if ~isempty(mat)
        elementNum=elementNum+1;
        index_dir=strfind(folder{i},'\');
        str_temp=folder{i}(index_dir(end)+1:end);
        Mdata{elementNum}.PatientID = str_temp;
        for k = 1 : length( mat )
            matpath = fullfile( folder{i}, mat( k ).name);
            %fid = fopen( datpath );
            temp = load (matpath) ;
            if contains(matpath,'T2_Label_1')
                Mdata{elementNum}.T2=temp.seg1;
            elseif contains(matpath,'T1_Label_1')
                Mdata{elementNum}.T1=temp.seg1;
            elseif contains(matpath,'T1C_Label_1')
                Mdata{elementNum}.T1C=temp.seg1;
            end
            % 此处添加你的对文件读写操作 %
            
        end
        waitbar(elementNum/nSample,waitbarHandle);
    end
    
end
close(waitbarHandle)
end