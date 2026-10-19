# # import redis
# # import json
# # import time
# # import torch

# # from model.transformer_model import TrustTransformer

# # # -----------------------------
# # # Redis Connection
# # # -----------------------------
# # r = redis.Redis(
# #     host="redis-service",
# #     port=6379,
# #     decode_responses=True
# # )

# # # -----------------------------
# # # Load Transformer Model
# # # -----------------------------
# # model = TrustTransformer()
# # model.eval()

# # # -----------------------------
# # # Parameters
# # # -----------------------------
# # ALPHA = 0.7
# # NODES = [f"edge-{i}" for i in range(10)]

# # print("🚀 Worker (Alvarium Confidence Engine) started...", flush=True)


# # # ======================================================
# # # NORMALIZATION FUNCTIONS
# # # ======================================================

# # def normalize_latency(x):
# #     return max(0.0, 1 - (x / 3000))


# # def normalize_cpu(x):
# #     return max(0.0, 1 - (x / 100))


# # def normalize_memory(x):
# #     return max(0.0, 1 - (x / 100))


# # def normalize_uptime(x):
# #     return min(1.0, x / 3600)


# # # ======================================================
# # # COLLECTOR AGENT
# # # ======================================================

# # def collector_agent(node):

# #     key = f"annotation:{node}"

# #     # latest 5 annotations
# #     data = r.lrange(key, -5, -1)

# #     records = []

# #     for item in data:
# #         try:
# #             records.append(json.loads(item))
# #         except:
# #             pass

# #     return records


# # # ======================================================
# # # ANALYZER AGENT
# # # ======================================================

# # def analyzer_agent(records):

# #     if len(records) == 0:
# #         return None

# #     # keep only valid records
# #     valid = []

# #     for x in records:

# #         if isinstance(x, dict) and "annotations" in x:
# #             valid.append(x)

# #     if len(valid) == 0:
# #         return None

# #     keys = [
# #         "latency",
# #         "success_rate",
# #         "uptime",
# #         "availability",
# #         "cpu",
# #         "memory"
# #     ]

# #     avg = {}

# #     for key in keys:

# #         total = 0

# #         for x in valid:
# #             total += x["annotations"].get(key, 0)

# #         avg[key] = total / len(valid)

# #     return avg

# # # ======================================================
# # # RULE CONFIDENCE AGENT
# # # ======================================================

# # def rule_confidence(node, avg):

# #     old = r.get(f"confidence:{node}")

# #     if old is None:
# #         old = 0.5
# #     else:
# #         old = float(old)

# #     current = (
# #         0.25 * avg["success_rate"] +
# #         0.20 * avg["availability"] +
# #         0.15 * normalize_latency(avg["latency"]) +
# #         0.15 * normalize_cpu(avg["cpu"]) +
# #         0.15 * normalize_memory(avg["memory"]) +
# #         0.10 * normalize_uptime(avg["uptime"])
# #     )

# #     confidence = ALPHA * old + (1 - ALPHA) * current

# #     return round(confidence, 4)


# # # ======================================================
# # # AI CONFIDENCE AGENT
# # # ======================================================

# # def ai_prediction(records):

# #     seq = []

# #     for x in records:

# #         if "annotations" not in x:
# #             continue

# #         a = x["annotations"]

# #         row = [
# #             a.get("latency", 0),
# #             a.get("success_rate", 0),
# #             a.get("uptime", 0),
# #             a.get("availability", 0),
# #             a.get("cpu", 0),
# #             a.get("memory", 0)
# #         ]

# #         seq.append(row)

# #     if len(seq) < 5:
# #         return 0.5

# #     tensor = torch.tensor([seq], dtype=torch.float32)

# #     with torch.no_grad():
# #         pred = model(tensor).item()

# #     return round(pred, 4)


# # # ======================================================
# # # FINAL CONFIDENCE
# # # ======================================================

# # def final_score(rule_score, ai_score):

# #     score = (0.6 * rule_score) + (0.4 * ai_score)

# #     return round(score, 4)


# # # ======================================================
# # # BLOCKCHAIN AGENT (Redis currently)
# # # ======================================================

# # def blockchain_agent(node, score):

# #     r.set(f"confidence:{node}", score)


# # # ======================================================
# # # MAIN LOOP
# # # ======================================================

# # while True:

# #     found = False

# #     for node in NODES:

# #         records = collector_agent(node)

# #         if len(records) == 0:
# #             continue

# #         avg = analyzer_agent(records)

# #         if avg is None:
# #             continue

# #         found = True

# #         rule_score = rule_confidence(node, avg)

# #         ai_score = ai_prediction(records)

# #         confidence = final_score(rule_score, ai_score)

# #         blockchain_agent(node, confidence)

# #         print(f"Node: {node}", flush=True)
# #         print(f"Rule Confidence : {rule_score}", flush=True)
# #         print(f"AI Confidence   : {ai_score}", flush=True)
# #         print(f"Final Confidence: {confidence}", flush=True)
# #         print("-" * 35, flush=True)

# #     if not found:
# #         print("No valid annotations found yet...", flush=True)

# #     time.sleep(5)


# import redis
# import json
# import time
# import torch

# from model.transformer_model import TrustTransformer

# # -----------------------------
# # Redis Connection
# # -----------------------------

# r = redis.Redis(
#     host="redis-service",
#     port=6379,
#     decode_responses=True
# )

# # -----------------------------
# # Load Transformer Model
# # -----------------------------

# model = TrustTransformer()
# model.eval()

# # -----------------------------
# # Parameters
# # -----------------------------

# ALPHA=0.5

# NODES = [f"edge-{i}" for i in range(10)]

# print(
#     "🚀 Worker (Alvarium Confidence Engine) started...",
#     flush=True
# )

# # =====================================================
# # NORMALIZATION
# # =====================================================

# def normalize_latency(x):

#     score=1-(x/5000)

#     return max(
#         0.1,
#         min(1,score)
#     )

# def normalize_cpu(x):

#     return max(
#         0.0,
#         1 - (x / 100)
#     )


# def normalize_memory(x):

#     return max(
#         0.0,
#         1 - (x / 100)
#     )


# def normalize_uptime(x):

#     return min(
#         1.0,
#         x / 3600
#     )

# # =====================================================
# # COLLECTOR AGENT
# # =====================================================

# def collector_agent(node):

#     key = f"annotation:{node}"

#     data = r.lrange(
#         key,
#         -5,
#         -1
#     )

#     records=[]

#     for item in data:

#         try:

#             records.append(
#                 json.loads(item)
#             )

#         except:

#             pass

#     return records

# # =====================================================
# # ANALYZER AGENT
# # =====================================================

# def analyzer_agent(records):

#     if len(records)==0:

#         return None

#     valid=[]

#     for x in records:

#         if (

#             isinstance(x,dict)

#             and

#             "annotations" in x

#         ):

#             valid.append(x)

#     if len(valid)==0:

#         return None

#     keys=[

#         "latency",

#         "success_rate",

#         "uptime",

#         "availability",

#         "cpu",

#         "memory"

#     ]

#     avg={}

#     for key in keys:

#         total=0

#         for x in valid:

#             total += (

#                 x["annotations"]

#                 .get(key,0)

#             )

#         avg[key] = (

#             total/

#             len(valid)

#         )

#     return avg

# # =====================================================
# # RULE CONFIDENCE
# # =====================================================

# def rule_confidence(node,avg):

#     old = r.get(

#         f"confidence:{node}"

#     )

#     if old is None:

#         old=0.5

#     else:

#         old=float(old)

#     latency = normalize_latency(

#         avg["latency"]

#     )

#     cpu = normalize_cpu(

#         avg["cpu"]

#     )

#     memory = normalize_memory(

#         avg["memory"]

#     )

#     uptime = normalize_uptime(

#         avg["uptime"]

#     )

#     success = avg["success_rate"]

#     availability = avg["availability"]

#     # ----------------
#     # Operational
#     # ----------------

#     operational=(

# 0.35*success+

# 0.35*availability+

# 0.30*latency

# )

#     # ----------------
#     # Resource
#     # ----------------

#     resource=(

#         0.5*cpu +

#         0.5*memory

#     )

#     # ----------------
#     # Network
#     # ----------------

#     packet_loss=(

#         1-success

#     )

#     network=(

# 0.4*latency+

# 0.3*success+

# 0.3*availability

# )

#     # ----------------
#     # Data
#     # ----------------

#     data=(

#         0.4*availability +

#         0.3*uptime +

#         0.3*success

#     )

#     # ----------------
#     # Historical
#     # ----------------

#     historical=(

#         0.4*uptime +

#         0.3*success +

#         0.3*old

#     )

#     # ----------------
#     # Multi Dimensional
#     # ----------------

#     current=(

#         0.25*operational +

#         0.15*resource +

#         0.20*network +

#         0.20*data +

#         0.20*historical

#     )

#     confidence=(

#         ALPHA*old +

#         (1-ALPHA)*current

#     )

#     trusts={

#         "operational":

#         round(
#             operational,
#             4
#         ),

#         "resource":

#         round(
#             resource,
#             4
#         ),

#         "network":

#         round(
#             network,
#             4
#         ),

#         "data":

#         round(
#             data,
#             4
#         ),

#         "historical":

#         round(
#             historical,
#             4
#         )

#     }

#     return (

#         round(
#             confidence,
#             4
#         ),

#         trusts

#     )

# # =====================================================
# # AI CONFIDENCE
# # =====================================================

# def ai_prediction(records):

#     seq=[]

#     for x in records:

#         if (

#             "annotations"

#             not in x

#         ):

#             continue

#         a=x["annotations"]

#         seq.append([

#             a.get(
#                 "latency",
#                 0
#             ),

#             a.get(
#                 "success_rate",
#                 0
#             ),

#             a.get(
#                 "uptime",
#                 0
#             ),

#             a.get(
#                 "availability",
#                 0
#             ),

#             a.get(
#                 "cpu",
#                 0
#             ),

#             a.get(
#                 "memory",
#                 0
#             )

#         ])

#     if len(seq)<5:

#         return 0.5

#     tensor=torch.tensor(

#         [seq],

#         dtype=torch.float32

#     )

#     with torch.no_grad():

#         pred=(

#             model(

#                 tensor

#             )

#             .item()

#         )

#     return round(

#         pred,

#         4

#     )

# # =====================================================
# # FINAL CONFIDENCE
# # =====================================================

# def final_score(

#     rule_score,

#     ai_score

# ):

#     score=(

#         0.6*

#         rule_score

#         +

#         0.4*

#         ai_score

#     )

#     return round(

#         score,

#         4

#     )

# # =====================================================
# # STORAGE
# # =====================================================

# def blockchain_agent(

#     node,

#     score

# ):

#     r.set(

#         f"confidence:{node}",

#         score

#     )

# # =====================================================
# # MAIN LOOP
# # =====================================================

# while True:

#     found=False

#     for node in NODES:

#         records=(

#             collector_agent(

#                 node

#             )

#         )

#         if len(records)==0:

#             continue

#         avg=(

#             analyzer_agent(

#                 records

#             )

#         )

#         if avg is None:

#             continue

#         found=True

#         rule_score,trusts=(

#             rule_confidence(

#                 node,

#                 avg

#             )

#         )

#         ai_score=(

#             ai_prediction(

#                 records

#             )

#         )

#         confidence=(

#             final_score(

#                 rule_score,

#                 ai_score

#             )

#         )

#         blockchain_agent(

#             node,

#             confidence

#         )

#         print()

#         print(

#             f"Node: {node}"

#         )

#         print(

#             f"Operational Trust : {trusts['operational']}"

#         )

#         print(

#             f"Resource Trust    : {trusts['resource']}"

#         )

#         print(

#             f"Network Trust     : {trusts['network']}"

#         )

#         print(

#             f"Data Trust        : {trusts['data']}"

#         )

#         print(

#             f"Historical Trust  : {trusts['historical']}"

#         )

#         print()

#         print(

#             f"Rule Confidence : {rule_score}"

#         )

#         print(

#             f"AI Confidence   : {ai_score}"

#         )

#         print(

#             f"Final Confidence: {confidence}"

#         )

#         print(

#             "-"*40

#         )

#     if not found:

#         print(

#             "No valid annotations found yet...",

#             flush=True

#         )

#     time.sleep(5)

import redis
import json
import time
import torch
from datetime import datetime

from model.transformer_model import TrustTransformer

# -----------------------------
# Redis Connection
# -----------------------------
r = redis.Redis(
    host="redis-service",
    port=6379,
    decode_responses=True
)

# -----------------------------
# Load Transformer Model
# -----------------------------
model = TrustTransformer()
model.eval()

# -----------------------------
# Parameters
# -----------------------------
ALPHA = 0.5
NODES = [f"edge-{i}" for i in range(10)]

print("🚀 Worker (Alvarium Confidence Engine) started...", flush=True)

# =====================================================
# NORMALIZATION
# =====================================================
def normalize_latency(x):
    score = 1 - (x / 5000)
    return max(0.1, min(1, score))

def normalize_cpu(x):
    return max(0.0, 1 - (x / 100))

def normalize_memory(x):
    return max(0.0, 1 - (x / 100))

def normalize_uptime(x):
    return min(1.0, x / 3600)

# =====================================================
# COLLECTOR AGENT
# =====================================================
def collector_agent(node):
    key = f"annotation:{node}"
    data = r.lrange(key, -5, -1)
    records = []
    for item in data:
        try:
            records.append(json.loads(item))
        except:
            pass
    return records

# =====================================================
# ANALYZER AGENT
# =====================================================
def analyzer_agent(records):
    if len(records) == 0:
        return None

    valid = []
    for x in records:
        if isinstance(x, dict) and "annotations" in x:
            valid.append(x)

    if len(valid) == 0:
        return None

    keys = ["latency", "success_rate", "uptime", "availability", "cpu", "memory"]
    avg = {}
    for key in keys:
        total = 0
        for x in valid:
            total += x["annotations"].get(key, 0)
        avg[key] = total / len(valid)
    return avg

# =====================================================
# RULE CONFIDENCE
# =====================================================
def rule_confidence(node, avg):
    old = r.get(f"confidence:{node}")
    if old is None:
        old = 0.5
    else:
        old = float(old)

    latency = normalize_latency(avg["latency"])
    cpu = normalize_cpu(avg["cpu"])
    memory = normalize_memory(avg["memory"])
    uptime = normalize_uptime(avg["uptime"])
    success = avg["success_rate"]
    availability = avg["availability"]

    # Operational Trust
    operational = (0.35 * success + 0.35 * availability + 0.30 * latency)

    # Resource Trust
    resource = (0.5 * cpu + 0.5 * memory)

    # Network Trust
    network = (0.4 * latency + 0.3 * success + 0.3 * availability)

    # Data Trust
    data = (0.4 * availability + 0.3 * uptime + 0.3 * success)

    # Historical Trust
    historical = (0.4 * uptime + 0.3 * success + 0.3 * old)

    # Multi-Dimensional Agregation
    current = (
        0.25 * operational +
        0.15 * resource +
        0.20 * network +
        0.20 * data +
        0.20 * historical
    )

    confidence = (ALPHA * old + (1 - ALPHA) * current)

    trusts = {
        "operational": round(operational, 4),
        "resource": round(resource, 4),
        "network": round(network, 4),
        "data": round(data, 4),
        "historical": round(historical, 4)
    }

    return round(confidence, 4), trusts

# =====================================================
# AI CONFIDENCE
# =====================================================
def ai_prediction(records):
    seq = []
    for x in records:
        if "annotations" not in x:
            continue
        a = x["annotations"]
        seq.append([
            a.get("latency", 0),
            a.get("success_rate", 0),
            a.get("uptime", 0),
            a.get("availability", 0),
            a.get("cpu", 0),
            a.get("memory", 0)
        ])

    if len(seq) < 5:
        return 0.5

    tensor = torch.tensor([seq], dtype=torch.float32)
    with torch.no_grad():
        pred = model(tensor).item()

    return round(pred, 4)

# =====================================================
# FINAL CONFIDENCE
# =====================================================
def final_score(rule_score, ai_score):
    score = (0.6 * rule_score + 0.4 * ai_score)
    return round(score, 4)

# =====================================================
# STORAGE (STATE AGENT)
# =====================================================
def blockchain_agent(node, score):
    r.set(f"confidence:{node}", score)

# =====================================================
# MAIN AUTOMATION LOOP
# =====================================================
while True:
    found = False
    for node in NODES:
        records = collector_agent(node)
        if len(records) == 0:
            continue

        avg = analyzer_agent(records)
        if avg is None:
            continue

        found = True
        rule_score, trusts = rule_confidence(node, avg)
        ai_score = ai_prediction(records)
        confidence = final_score(rule_score, ai_score)

        # Update latest execution state
        blockchain_agent(node, confidence)

        # Store structured historical timelines
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_payload = {
            "timestamp": current_time,
            "operational": trusts["operational"],
            "resource": trusts["resource"],
            "network": trusts["network"],
            "data": trusts["data"],
            "historical": trusts["historical"],
            "rule_confidence": rule_score,
            "ai_confidence": ai_score,
            "final_confidence": confidence
        }

        history_key = f"trust_history:{node}"
        r.lpush(history_key, json.dumps(history_payload))
        r.ltrim(history_key, 0, 499)

        # Terminal Standard Output Logging
        print(f"\nNode: {node}")
        print(f"Operational Trust : {trusts['operational']}")
        print(f"Resource Trust    : {trusts['resource']}")
        print(f"Network Trust     : {trusts['network']}")
        print(f"Data Trust        : {trusts['data']}")
        print(f"Historical Trust  : {trusts['historical']}")
        print(f"Rule Confidence   : {rule_score}")
        print(f"AI Confidence     : {ai_score}")
        print(f"Final Confidence  : {confidence}")
        print("-" * 40, flush=True)

    if not found:
        print("No valid annotations found yet...", flush=True)

    time.sleep(5)