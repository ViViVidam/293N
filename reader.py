import os
from collections import defaultdict
import json

video_sent_attr = ["timestamp","session_id","index","expt_id","channel","video_ts","format","size","ssim_index","cwnd","in_flight","min_rtt","rtt","delivery_rate"]
buffer_attr = ["timestamp","session_id","index","expt_id","channel","event","buffer","cum_rebuf"]
video_acked_attr = ["timestamp","session_id","index","expt_id","channel","video_ts"]

class Reader:
    def __init__(self,data_folder:str="./data"):
        self.data_folder = data_folder
        self.scheme = defaultdict(defaultdict)
        self.sent_chunks = list(defaultdict)
        self.buffer_level = list(defaultdict)
        self.acked_chunks = list(defaultdict)

        self.load_scheme()
        self.load_video_acked()
        self.load_video_sent()
        self.load_buffer_level()
    def load_scheme(self):
        exp_settings_path = os.path.join(self.data_folder, "logs")
        with open(os.path.join(exp_settings_path, "expt_settings")) as f:
            for line in f.readlines():
                scheme_id, setting = line.strip().split(" ",maxsplit=1)
                self.scheme[scheme_id] = json.loads(setting)

    def load_video_acked(self):
        for filename in os.listdir(self.data_folder):
            if filename.startswith("video_acked"):
                with open(os.path.join(self.data_folder, filename)) as f:
                    for line in f.readlines()[1:]:
                        stat = line.strip().split(',')
                        self.acked_chunks.append({attr:st for attr,st in zip(video_acked_attr,stat)})

    def load_video_sent(self):
        for filename in os.listdir(self.data_folder):
            if filename.startswith("video_sent"):
                with open(os.path.join(self.data_folder, filename)) as f:
                    for line in f.readlines()[1:]:
                        stat = line.strip().split(',')
                        self.sent_chunks.append({attr:st for attr,st in zip(video_sent_attr,stat)})

        # video_sent_path = os.path.join(self.data_folder, "video_sent")
    def load_buffer_level(self):
        for filename in os.listdir(self.data_folder):
            if filename.startswith("client_buffer"):
                with open(os.path.join(self.data_folder, filename)) as f:
                    for line in f.readlines()[1:]:
                        stat = line.strip().split(',')
                        self.buffer_level.append({attr:st for attr,st in zip(buffer_attr,stat)})

    def get_exp_setting(self,expt_id:str)->defaultdict:
        return self.scheme[expt_id]
if __name__ == "__main__":
    reader = Reader()
    print(reader.scheme['1'].keys())