#!/usr/bin/zsh

echo ----- $(hostname) $(date) -----
if [ ! -d tweet_env ]; then
    conda create --yes --prefix ./tweet_env pandas twython
fi
conda activate ./tweet_env

echo ----- tweet_env is activated -----
python3 tweet.py

echo ----- Start running R code $(date) -----
Rscript plots_dori.R
