# 293N -- Comparison of ABR Algorithms 
Parker Carlson, Wentai Xie, Rithwik Keur


### Reproduce Our Results

##### Comparison under various bitrates
##### Comparison under start up time

Run setup_time.py will generate the corresponding graph.

##### Comparison of SSIM and rebuffering performance

1. Download data from Stanford's Puffer experiment for large-scale comparison

`./download_data.sh`

2. Run the jupyter notebook (`graphs.ipynb`) and run all cells. Graphs will be automatically produced.
3. Run the `setup_time.py` will generate a setup latency graph.


##### Comparison of %Rebuffering and Average bitrate for different video qualities
Install python dependencies (pandas, matplotlib)
run python3 reader.py
Modify line 13 to point to correct data directory to see FuGu vs Linear BBA