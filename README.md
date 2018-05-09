## Introduction

FX rates are challenging for prediction, but potentially lucrative and intrinsically interesting. In this repository, we present a project to predict FX rates for the world’s six most-traded currencies against the USD: AUD, CAD, CHF, EUR, GBP, and JPY. Data on major economic indicators was obtained from the Federal Reserve Bank of St. Louis, the Energy Information Administration, Quandl, and The Economist. We fitted prediction models for both regression and classification, using classic machine learning (including ARIMA, GAM, random forest, boosting, and SVM) and neural networks (including LSTM and FFNN). Results showed that regression on rates couldn’t overcome the ‘random walk’ in seven-day FX rate movements. Classification of the direction of FX rate movement six months in advance, however, resulted in an average ROC AUC score near 80%. In general, the most resource-intensive economies offered the best predictions, while the least resource-intensive economies offered the worst predictions. Methodologically, a robust and streamlined software framework (in Python) was needed for efficient exploration of the modeling space.

## Report and Presentation

* [Final Report (PDF)](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/13_Report_B.pdf)
* [Final Presentation (Keynote)](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/14_Presentation_Modjeska_Murphy_Dec14_C_1.key)

## Code before Report

* [Data Acquisition (by Dominic Murphy)](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/01_DataAquisition_10Dec2017_C.py)
* [Data Exploration](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/02_Exploration_10Dec2017B.ipynb)
* [ARIMA](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/03_Auto_Arima.Rmd)
* [LSTM Regression](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/04_LSTM_10Dec2017A.ipynb)
* [GAM](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/05_GAM_10Dec2017A.ipynb)
* [Random Forest Regression](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/06_RF_10Dec2017A.ipynb)
* [XGBoost Regression](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/07_XGB_10Dec2017A.ipynb)
* [Ensemble Model Regression](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/08_Ensemble_10Dec2017A.ipynb)
* [Prediction Scores Summary for Regression](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/09_Summary_10Dec2017A.ipynb)
* [LSTM Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/10_LSTM_C_12Dec2017A.ipynb)
* [Support Vector Machine](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/10_SVM_11Dec2017E.ipynb)
* [FFNN Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/11_FFNN_C_12Dec2017A.ipynb)
* [Prediction Scores Summary for Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_Before_Report/12_Summary_12Dec2017B.ipynb)

## Code after Report

* [Random Forest Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_After_Report/09_RFC_6Jan2018.ipynb)
* [Support Vector Machine (Feature Selection](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_After_Report/09_SVM_17Jan2018_Features2.ipynb)
* [Support Vector Machine (Hyperparameter Tuning](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_After_Report/09_SVM_17Jan2018_Hyperparameters.ipynb)
* [XGBoost Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_After_Report/09_XGBC_6Jan2018.ipynb)
* [Prediction Scores Summary for Classification](https://github.com/dmodjeska/predict_fx_rate_movements/blob/master/Code_After_Report/12_Summary_14Jan2018.ipynb)


