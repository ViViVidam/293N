from collections import defaultdict

from reader import Reader

if __name__ == '__main__':
    reader = Reader()
    stream_init = defaultdict(defaultdict)
    stream_startup = defaultdict(defaultdict)
    for item in reader.buffer_level:
        if item["event"] == "init":
            session_id, index = item["session_id"],item["index"]
            stream_init[session_id][index] = int(item["timestamp"])
        elif item["event"] == "startup":
            session_id, index = item["session_id"],item["index"]
            stream_startup[session_id][index] = int(item["timestamp"])
        int(item["timestamp"])
    settings = reader.analyze()

# session, index -> exp_settings, channel, qualitys