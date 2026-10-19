import redis, json, numpy as np

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Collector Agent
def collect(node):
    data = r.lrange(node, -10, -1)
    return [json.loads(d) for d in data]

# Analyzer Agent
def analyze(data):
    lat = np.mean([d["latency"] for d in data])
    suc = np.mean([d["success_rate"] for d in data])
    err = np.mean([d["error_rate"] for d in data])
    return [lat, suc, err]

# Trust Agent
def compute(features):
    lat, suc, err = features
    return (suc*0.6) - (lat*0.002) - (err*0.4)