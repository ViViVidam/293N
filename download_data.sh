#!/bin/bash

mkdir ./data/real_0252525
cd ./data/real_052525
# data analyzed from May 25, 2025
wget https://storage.googleapis.com/puffer-data-release/2025-05-24T11_2025-05-25T11/video_sent_2025-05-24T11_2025-05-25T11.csv
wget https://storage.googleapis.com/puffer-data-release/2025-05-29T11_2025-05-30T11/video_acked_2025-05-29T11_2025-05-30T11.csv 
wget https://storage.googleapis.com/puffer-data-release/2025-05-29T11_2025-05-30T11/client_buffer_2025-05-29T11_2025-05-30T11.csv
wget https://storage.googleapis.com/puffer-data-release/2025-05-29T11_2025-05-30T11/video_size_2025-05-29T11_2025-05-30T11.csv
wget https://storage.googleapis.com/puffer-data-release/2025-05-29T11_2025-05-30T11/ssim_2025-05-29T11_2025-05-30T11.csv
