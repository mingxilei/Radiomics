function [GlobalTextures] = calcGlobal(VolumeInfo,Mask,scanType,R,Scale,Histograms_bins)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
ROIonly = prepareVolume(VolumeInfo.Volume,Mask,scanType,VolumeInfo.pixelW,VolumeInfo.sliceS,R,Scale,'Global');
GlobalTextures = getGlobalTextures(ROIonly,Histograms_bins);
end

