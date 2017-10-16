# Roman coins
## Overview
Python project for analyzing roman coin data
Project contains:
* scrapper parsing numismatics.org site for retrieving roman coin images (built with [scrapy](https://scrapy.org/) library)
* script for preparing collected images to machine learning processing

## Commands
* clear output folder and run scrapper: `./run_nomismaspider.sh`
* normalize and organize images to folders: `python ImageNormalizer.py`
* Find dirs with at least 100 images: `cd normalized-images && ../count_dir_files.sh | grep -P  '\d{3}'`