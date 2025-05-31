with open("data/fugu_bbr_exp/video_sent.1.log","r") as f:
    for f in f.readlines():
        print(len(f.split(',')))
        break

with open("data/video_sent_2019-01-26T11_2019-01-27T11.csv","r") as f:
    for f in f.readlines():
        print(len(f.split(',')))
        break