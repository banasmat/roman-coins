#!/bin/bash

rm nomismaspider-output.json
touch nomismaspider-output.json

rm nomismaspider/output/full/*
scrapy crawl nomismaspider -o nomismaspider-output.json