# Heatwave Wizard

## Table of Contents
- [Introduction](#introduction)
- [Motivation](#motivation)
- [Features](#features)
- [Machine Learning Models](#machine-learning-models)
- [Installation](#installation)

## Introduction
Heatwave Wizard is a web application that uses machine learning models to predict heatwave occurrences based on historical data and climate projections. It allows users to explore different scenarios of heatwave frequency, intensity and duration for various regions of the world.

## Motivation

Heatwaves are extreme events that pose serious threats to human health, ecosystems, agriculture and infrastructure. They are expected to become more frequent, persistent and intense in the future due to anthropogenic warming. Therefore, it is important to develop tools that can forecast heatwave occurrences and inform adaptation and mitigation strategies.

## Features

Heatwave Wizard provides the following features:

- A user-friendly interface with all important information about heatwaves such as heatwave causing factors, its impact on environment and 
information regarding preparations and response take in the condition of heatwave.
- A dashboard that displays the historical and projected statistics of heatwave occurrences for the data used for training machine learning model.
- A heatwave forcasting section to forcast condition of upcoming heatwaves for different cities.
- A heatwave alert mail service in which subscribers will get mail alert one day before heatwave occurances for their city.

## Machine Learning Models

Total 5 machine learning models were trained using available data which are:
- Linear Regressor
- Support vector Regressor
- Random Forest Regressor
- Neural Network Regressor
- Lasso Regressor

After training and testing these models, performances of all the models were comparied and best performing model is being used by heatwavewizard in background which is Random Forest Regressor.

## Installation

To run Heatwave Wizard locally, you need to have Python 3.7 or higher installed on your machine. You also need to install the following packages:

- names==0.3.0
- pandas==1.4.2
- pytz==2021.3
- Requests==2.30.0
- streamlit==1.21.0
- streamlit_autorefresh==0.0.1
- emails==0.6
- ssl==1.16

You can install these packages using pip or conda.

To launch Heatwave Wizard, navigate to command prompt for the project directory and run heatwave.py file using following command:

```
streamlit run heatwave.py

```


