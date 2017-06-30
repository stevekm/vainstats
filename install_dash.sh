#!/bin/bash

# Set up Conda environment for Dash

# make sure conda has pip installed
# conda install pip

# create conda env for the dash
conda env create -f dash.yml

# activate the env
source activate dash

# deactivate with
# source deactivate

# install packages into the env with pip
pip install -r requirements.txt
