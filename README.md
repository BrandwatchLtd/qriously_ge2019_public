# Introduction
This repo contains simplified code and data to replicate the Brandwatch Qriously 2019 UK General Election Prediction. 

We hope that releasing this code and data will help people understand more about survey methodology, how pollsters make scientific predictions of elections, and gain further insights about the election that go beyond the analysis Brandwatch Qriously has already [released](https://www.brandwatch.com/blog/general-election-2019-qrioulsy-prediction/).
Although the code in this repository is written in Python, non-Python users are welcome to open the raw polling data provided in .xlsx format with software of their choice (such as R Studio, Stata, SPSS, or Excel).

Please note that this repository contains the minimal code and data required to replicate the prediction, and allow users to do their own further analysis. In reality, the Brandwatch Qriously Data Science team used significantly more code, particularly to process the data and check its integrity. For the sake of brevity, this extra code has not been included.

# Guide to data and information for non-Python users
The raw polling data file can be found in `data/raw`. The Jupyter Notebook included in this repo will open and analyse that file, but if you are not using Python, you can open that file in your software of choice.

The raw polling data contains shortened variable names, rather than the full question text. You can view a full list of the questions asked, as well as a map of the question text to the shortened variable names in `data/information/questions_options_variables.xlsx`. Please note that other variables have been added to the dataset through inference or metadata; for example, the variable NUTS1_region is inferred from the respondents' constituency, which was in turn determined by Qriously's geolocation system.

# Installation
Be sure to install the latest version of Python 3.x and Pipenv. You can then install all the necessary libraries required to run this code through going into this repository's root directory (where you see the Pipfile) and running `pipenv install`. You can read more about use of Pipenv [here](https://pipenv-fork.readthedocs.io/en/latest/basics.html). If you prefer to use a different method to manage environments, such as Conda, you can view the libraries required by opening the Pipfile.

# Licences
Please see LICENSE.md for information about licensing.

# Disclaimer
Please note that this is intended as a one-off, and Brandwatch Qriously makes no commitment to make further releases. We hope that this release encourages learning and experimentation.

This is not an official or supported Brandwatch library, and should be implemented at the users' own risk.

# Contact
Please contact peterf@brandwatch.com if you have any questions.