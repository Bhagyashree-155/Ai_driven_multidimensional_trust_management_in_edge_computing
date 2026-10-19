# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # import redis
# # import json

# # app = FastAPI()

# # r = redis.Redis(
# #     host="redis-service",
# #     port=6379,
# #     decode_responses=True
# # )

# # class Metrics(BaseModel):
# #     node_id: str
# #     latency: float
# #     success_rate: float
# #     uptime: float
# #     availability: float
# #     cpu: float
# #     memory: float

# # @app.get("/")
# # def home():
# #     return {"status": "API Running"}

# # @app.post("/metrics")
# # def receive_metrics(data: Metrics):
# #     key = f"node:{data.node_id}"

# #     r.rpush(key, json.dumps(data.dict()))
# #     r.ltrim(key, -50, -1)

# #     return {"stored": True}

# from fastapi import FastAPI
# import redis
# import json
# import time

# app = FastAPI()

# # connect to Redis (Kubernetes service name)
# r = redis.Redis(host="redis-service", port=6379, decode_responses=True)


# @app.get("/")
# def home():
#     return {"message": "API running"}


# @app.post("/metrics")
# async def receive_annotation(data: dict):

#     node = data["node_id"]

#     # 🔹 store full annotation history (Alvarium style)
# r.lpush(f"annotation:{node}", json.dumps({
#     "annotations": payload,
#     "timestamp": time.time()
# }))
#     # 🔹 keep only last 50 records (avoid memory overflow)
#     r.ltrim(f"annotation:{node}", 0, 49)

#     # 🔹 store latest snapshot (quick access)
#     r.set(f"latest:{node}", json.dumps(data))

#     # 🔹 optional: store timestamped key (debug/demo)
#     r.set(f"log:{node}:{int(time.time())}", json.dumps(data))

#     return {"status": "stored", "node": node}


from fastapi import FastAPI
import redis
import json
import time

app = FastAPI()

r = redis.Redis(host="redis-service", port=6379, decode_responses=True)

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/metrics")
async def receive_annotation(data: dict):

    node = data["node_id"]

    # store annotation directly (already in correct format)
    r.lpush(f"annotation:{node}", json.dumps(data))

    # keep last 50
    r.ltrim(f"annotation:{node}", 0, 49)

    return {"status": "stored", "node": node}