function [GlobalTextures] = calcGlobal(VolumeInfo,Mask,scanType,R,Scale,Histograms_bins)
%UNTITLED2 �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
ROIonly = prepareVolume(VolumeInfo.Volume,Mask,scanType,VolumeInfo.pixelW,VolumeInfo.sliceS,R,Scale,'Global');
GlobalTextures = getGlobalTextures(ROIonly,Histograms_bins);
end

