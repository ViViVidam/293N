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
    reader = Reader()
    stream_init = defaultdict(lambda: defaultdict(list))
    stream_startup = defaultdict(lambda: defaultdict(list))

    for item in reader.buffer_level:
        if item["event"] == "init":
            session_id, index = item["session_id"],item["index"]
            stream_init[session_id][index].append(int(item["timestamp"]))
        elif item["event"] == "startup":
            session_id, index = item["session_id"],item["index"]
            stream_startup[session_id][index].append(int(item["timestamp"]))
        int(item["timestamp"])
    # each session use one ABR algorithm

    ana = reader.analyze()
    expt_id2sess = defaultdict(list)
    sess2abr = defaultdict(str)
    for a in ana.itertuples():
        expt_id2sess[a.expt_id].append(a.session_id)
    for k,ele in reader.scheme.items():
        if "session_id" not in ele.keys():
            continue
        for sess in expt_id2sess[ele["expt_id"]]:
            sess2abr[sess] = ele["abr"]

    x = []
    y = []
    for session in stream_init.keys():
        for index in stream_startup[session].keys():
            for idx in len(stream_startup[session][index]):
                startup_delay = stream_startup[session][index][idx] - stream_init[session][index][idx]
                assert(startup_delay > 0)
                x.append(startup_delay)
                y.append(sess2abr[session])
    sns.boxplot(x=x,y=y)
    plt.show()
# session, index -> exp_settings, channel, qualitys
# x:ABR y:StartUp time