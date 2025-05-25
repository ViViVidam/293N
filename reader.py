import os
from collections import defaultdict
import json
class Reader:
    def __init__(self,data_folder:str="./data"):
        self.data_folder = data_folder
        self.scheme = defaultdict(defaultdict)
        self.load_scheme()
    def load_scheme(self):
        exp_settings_path = os.path.join(self.data_folder, "logs")
        with open(os.path.join(exp_settings_path, "expt_settings")) as f:
            for line in f.readlines():
                scheme_id, setting = line.strip().split(" ",maxsplit=1)
                self.scheme[scheme_id] = json.loads(setting)

    def get_exp_setting(self,expt_id:str)->defaultdict:
        return self.scheme[expt_id]
if __name__ == "__main__":
    reader = Reader()
    print(reader.scheme['1'].keys())