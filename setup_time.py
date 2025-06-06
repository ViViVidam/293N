from collections import defaultdict
from typing import Dict, List
from reader import Reader
import seaborn as sns
from matplotlib import pyplot as plt
def reformat_scheme(reader:Reader)->Dict[dict,str]:
    datas = defaultdict(defaultdict)
    for k,ele in reader.scheme.items():
        if "session_id" not in ele.keys():
            continue
        session_id, index = ele["session_id"], ele["index"]
        datas[session_id][index] = ele["abr"]
    return datas
if __name__ == '__main__':
    reader_fugu = Reader(data_folder="./data/fugu_bbr_exp/")
    reader_linear = Reader(data_folder="./data/linear_bba_exp/")

    ana = reader_fugu.analyze()
    expt_id2sess = defaultdict(list)
    sess2abr = defaultdict(str)
    for a in ana.itertuples():
        expt_id2sess[int(a.expt_id)].append(a.session_id)
    for k, ele in reader_fugu.scheme.items():
        for sess in expt_id2sess[ele["expt_id"]]:
            sess2abr[sess] = ele["abr"]

    streams = defaultdict(lambda: defaultdict(int))
    # defaultdict(lambda : defaultdict(list))
    x = []
    y = []
    for item in reader_fugu.buffer_level:
        if item["event"] == "init":
            session_id,channel = item["session_id"],item["channel"]
            streams[session_id][channel] = int(item["timestamp"])
        elif item["event"] == "startup":
            session_id,channel = item["session_id"],item["channel"]
            if streams[session_id][channel] == 0:
                continue
            startup_delay = int(item["timestamp"]) - streams[session_id][channel]
            streams[session_id][channel] = 0
            assert(startup_delay > 0)
            x.append(startup_delay)
            y.append(sess2abr[session_id])
        #int(item["timestamp"])
    # each session use one ABR algorithm





    #for session in stream_init.keys():
    #    for idx in range(len(stream_startup[session])):
    ##        startup_delay = stream_startup[session][idx] - stream_init[session][idx]
     #       assert(startup_delay > 0)
     #       x.append(startup_delay)
     #       y.append(sess2abr[session])
    ana = reader_linear.analyze()
    expt_id2sess.clear()
    sess2abr.clear()
    for a in ana.itertuples():
        expt_id2sess[int(a.expt_id)].append(a.session_id)
    for k, ele in reader_linear.scheme.items():
        for sess in expt_id2sess[ele["expt_id"]]:
            sess2abr[sess] = ele["abr"]

    streams.clear()

    for item in reader_linear.buffer_level:
        if item["event"] == "init":
            session_id, channel = item["session_id"], item["channel"]
            streams[session_id][channel] = int(item["timestamp"])
        elif item["event"] == "startup":
            session_id, channel = item["session_id"], item["channel"]
            if streams[session_id][channel] == 0:
                continue
            startup_delay = int(item["timestamp"]) - streams[session_id][channel]
            streams[session_id][channel] = 0
            assert (startup_delay > 0)
            if (startup_delay > 1e5):
                print(streams[session_id][channel],item)
            x.append(startup_delay)
            y.append(sess2abr[session_id])
    # each session use one ABR algorithm


    x = [i/1000 for i in x]

    #print(y)
    plot = sns.boxplot(x=y,y=x)
    plt.ylabel("Time (ms)")
    plt.xlabel("ABR algorithm")
    plt.show()
    plt.draw()
    plot.get_figure().savefig('setup_delay.png')
# session, index -> exp_settings, channel, qualitys
# x:ABR y:StartUp time