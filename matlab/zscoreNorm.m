function [ROIonlyNorm] = zscoreNorm(ROIonly)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
ROIonly = double(ROIonly);
temp = ROIonly(~isnan(ROIonly));
u = mean(temp);
sigma = std(temp);
ROIonlyNorm = (ROIonly-u)./sigma;
end

