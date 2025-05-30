import os
from collections import defaultdict, UserList
import json
import pandas as pd
import matplotlib.pyplot as plt


video_sent_attr = ["timestamp","session_id","index","expt_id","channel","video_ts","format","size","ssim_index","cwnd","in_flight","min_rtt","rtt","delivery_rate"]
buffer_attr = ["timestamp","session_id","index","expt_id","channel","event","buffer","cum_rebuf"]
video_acked_attr = ["timestamp","session_id","index","expt_id","channel","video_ts"]

class Reader:
    def __init__(self,data_folder:str="./data"):
        self.data_folder = data_folder
        self.scheme = defaultdict(defaultdict)
        self.sent_chunks = []
        self.buffer_level = []
        self.acked_chunks = []

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

        
    def analyze(self):
        df_sent = pd.DataFrame(self.sent_chunks)
        df_acked = pd.DataFrame(self.acked_chunks)
        df_buf  = pd.DataFrame(self.buffer_level)


        for df, dtypes in [
        (df_sent, {"timestamp": int, "size": int, "video_ts": int}),
        (df_acked, {"timestamp": int, "video_ts": int}),
        (df_buf,  {"timestamp": int, "buffer": float, "cum_rebuf": float})]:
            for col, typ in dtypes.items():
                df[col] = df[col].astype(typ)

        for df in (df_sent, df_acked, df_buf):
            df["session_id"] = df["session_id"].astype(str)


        group_keys = ["expt_id", "session_id"]

        total_rebuf = (
            df_buf
            .groupby(group_keys)["cum_rebuf"]
            .max()
            .rename("total_rebuf_s")
        )

        acked_counts = (
            df_acked
            .groupby(group_keys)
            .size()
            .rename("n_acked_chunks")
        )

        played_time = (acked_counts * 2.002).rename("played_time_s")

        df_sent["bitrate_bps"] = df_sent["size"] * 8 / 2.002

        avg_bitrate = (
            df_sent
            .groupby(group_keys)["bitrate_bps"]
            .mean()
            .rename("avg_bitrate_bps")
        )

        df_sent = df_sent.sort_values(group_keys + ["index"])
        df_sent["delta_bps"] = (
            df_sent
            .groupby(group_keys)["bitrate_bps"]
            .diff()
            .fillna(0)
        )
        pct_rebuf = (total_rebuf / played_time * 100).rename("pct_rebuf_played")

        summary = (
            pd.concat([total_rebuf, played_time, avg_bitrate, acked_counts, pct_rebuf], axis=1)
            .reset_index()
        )

        summary = summary.sort_values(["expt_id", "session_id"])
        print(summary)
        return summary

    def plotGraphs(self, summary):
        plt.figure()
        for expt_id, group in summary.groupby("expt_id"):
            plt.scatter(
                group["pct_rebuf_played"],
                group["avg_bitrate_bps"],
                label=f"{self.scheme[expt_id]["abr"]}"
            )

        plt.xlabel("% Rebuffering")
        plt.ylabel("Average Bitrate (bps)")
        plt.title("% Rebuffering vs. Average Bitrate Across ABRs")
        plt.legend()
        plt.show()   
        return summary

if __name__ == "__main__":
    reader = Reader()
    summary = reader.analyze()
    reader.plotGraphs(summary)