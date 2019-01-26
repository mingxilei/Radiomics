Radiomics Method for Nasopharyngeal Carcinoma
12/2017 - 03/2018
Advisor: Shuoyu Xu

In this project, high dimentions of radiomics feature are evaluated to predict outcomes (move, relapse, dead).

1. feature extraction

ROI (region of interest) is manually segmented by professional radiologists. We run algorithms on the ROI to extract statistic-based features and texture-based features.
Pixel normalization algorithm is modified to be Z-score (it was Collewet in the toolbox).
We tuned the pre-processing parameter to multiple dimentions of feature.
toolbox: Radiomics https://github.com/mvallieres/radiomics

2. dataset resampling

Resampling is needed because of the extremely imbalanced dataset (nearly 1:9). Sixteen algorithms were used and evaluated.

3. feature selection

Features are sorted according to their significance. Top 50 features are selected to continue the following analysis.

4.