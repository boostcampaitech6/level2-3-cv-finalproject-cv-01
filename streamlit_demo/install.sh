#!/bin/bash

# 환경 이름 설정
ENV_NAME=streamlit_test_3.10

conda init

conda activate $ENV_NAME

echo "Waiting for the environment to be activated..."
sleep 5

echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# TA-Lib 설치
echo "Installing TA-Lib with Conda..."
conda install -c conda-forge ta-lib -y

# source deactivate

# conda activate $ENV_NAME

