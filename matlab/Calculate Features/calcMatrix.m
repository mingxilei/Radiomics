function [GLCMtextures,GLRLMtextures,GLSZMtextures,NGTDMtextures] = calcMatrix(VolumeInfo,Mask,scanType,R,Scale,QuanAlgo,Ng)
%UNTITLED4 此处显示有关此函数的摘要
%   此处显示详细说明
[ROIonly,levels]=prepareVolume(VolumeInfo.Volume,Mask,scanType,VolumeInfo.pixelW,VolumeInfo.sliceS,R,Scale,'Matrix',QuanAlgo,Ng);
GLCM = getGLCM(ROIonly,levels);
GLRLM = getGLRLM(ROIonly,levels);
GLSZM = getGLSZM(ROIonly,levels);
[NGTDM,countValid] = getNGTDM(ROIonly,levels);
GLCMtextures = getGLCMtextures(GLCM);
GLRLMtextures = getGLRLMtextures(GLRLM);
GLSZMtextures = getGLSZMtextures(GLSZM);
NGTDMtextures = getNGTDMtextures(NGTDM,countValid);

end

