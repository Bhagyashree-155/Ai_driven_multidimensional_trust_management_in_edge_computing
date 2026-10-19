# # import requests
# # import time
# # import psutil
# # from collections import deque

# # EDGE_URL = "http://edge-service:5000/"
# # API_URL = "http://api-service:8000/metrics"

# # nodes = ["node1", "node2", "node3"]

# # history = {n: deque(maxlen=20) for n in nodes}
# # start_time = {n: time.time() for n in nodes}

# # while True:

# #     for node in nodes:

# #         success = 0

# #         try:
# #             t1 = time.time()
# #             res = requests.get(EDGE_URL, timeout=3)
# #             latency = (time.time() - t1) * 1000
# #             success = 1 if res.status_code == 200 else 0

# #         except:
# #             latency = 3000
# #             success = 0

# #         history[node].append(success)

# #         success_rate = sum(history[node]) / len(history[node])

# #         uptime = time.time() - start_time[node]

# #         availability = successful_checks[node] / total_checks[node]

# #         cpu = psutil.cpu_percent(interval=0.1)
# #         memory = psutil.virtual_memory().percent

# #         payload = {
# #             "node_id": node,
# #             "latency": latency,
# #             "success_rate": success_rate,
# #             "uptime": uptime,
# #             "availability": availability,
# #             "cpu": cpu,
# #             "memory": memory
# #         }

# #         try:
# #             requests.post(API_URL, json=payload, timeout=3)
# #             print(payload, flush=True)

# #         except:
# #             print("Failed to send", flush=True)

# #     time.sleep(3)


# import requests
# import time
# import psutil
# import json
# from collections import deque

# EDGE_URL = "http://edge-service:5000/"
# API_URL = "http://api-service:8000/metrics"

# nodes = [
#     "node1",
#     "node2",
#     "node3",
#     "node4",
#     "node5",
#     "node6",
#     "node7",
#     "node8",
#     "node9",
#     "node10"
# ]

# # sliding window (recent performance)
# history = {n: deque(maxlen=20) for n in nodes}

# # start time (for uptime)
# start_time = {n: time.time() for n in nodes}

# # for true availability
# total_checks = {n: 0 for n in nodes}
# successful_checks = {n: 0 for n in nodes}

# while True:

#     for node in nodes:

#         success = 0

#         try:
#             t1 = time.time()
#             res = requests.get(EDGE_URL, timeout=3)

#             latency = (time.time() - t1) * 1000
#             success = 1 if res.status_code == 200 else 0

#         except:
#             latency = 3000
#             success = 0

#         # update counters
#         total_checks[node] += 1
#         successful_checks[node] += success

#         # recent history (for success_rate)
#         history[node].append(success)

#         # success rate (recent)
#         success_rate = sum(history[node]) / len(history[node])

#         # uptime (seconds)
#         uptime = time.time() - start_time[node]

#         # availability (long-term)
#         availability = successful_checks[node] / total_checks[node]

#         # system metrics
#         cpu = psutil.cpu_percent(interval=0.1)
#         memory = psutil.virtual_memory().percent

#         # 🔥 Alvarium-style annotation
#         annotation = {
#             "node_id": node,
#             "type": "performance",
#             "annotations": {
#                 "latency": latency,
#                 "success_rate": success_rate,
#                 "uptime": uptime,
#                 "availability": availability,
#                 "cpu": cpu,
#                 "memory": memory
#             },
#             "timestamp": time.time(),
#             "source": "sender"
#         }

#         try:
#             requests.post(API_URL, json=annotation, timeout=3)
#             print(annotation, flush=True)

#         except:
#             print("Failed to send", flush=True)

#     time.sleep(3)

import requests
import time
import psutil
import json
from collections import deque

nodes = [f"edge-{i}" for i in range(10)]

history = {n: deque(maxlen=20) for n in nodes}

start_time = {n: time.time() for n in nodes}

total_checks = {n: 0 for n in nodes}
successful_checks = {n: 0 for n in nodes}

while True:

    for node in nodes:

        EDGE_URL = "http://edge-service:5000/"

        success = 0

        try:

            t1 = time.time()

            res = requests.get(
                EDGE_URL,
                timeout=3
            )

            latency = (time.time() - t1) * 1000

            success = 1 if res.status_code == 200 else 0

        except:

            latency = 3000
            success = 0

        total_checks[node] += 1
        successful_checks[node] += success

        history[node].append(success)

        success_rate = (
            sum(history[node]) / len(history[node])
        )

        uptime = time.time() - start_time[node]

        availability = (
            successful_checks[node] /
            total_checks[node]
        )

        cpu = psutil.cpu_percent(interval=0.1)

        memory = psutil.virtual_memory().percent

        annotation = {
            "node_id": node,
            "type": "performance",
            "annotations": {
                "latency": latency,
                "success_rate": success_rate,
                "uptime": uptime,
                "availability": availability,
                "cpu": cpu,
                "memory": memory
            },
            "timestamp": time.time(),
            "source": "sender"
        }

        try:

            requests.post(
                "http://api-service:8000/metrics",
                json=annotation,
                timeout=3
            )

            print(annotation, flush=True)

        except:

            print(
                f"Failed to send {node}",
                flush=True
            )

    time.sleep(3)