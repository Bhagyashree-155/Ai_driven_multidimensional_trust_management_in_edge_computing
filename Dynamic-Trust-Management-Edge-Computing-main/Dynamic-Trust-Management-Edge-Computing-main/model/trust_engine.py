import redis
import json
import time
import torch
import torch.nn as nn
import numpy as np

# ---------------- REDIS ----------------
r = redis.Redis(host='redis-service', port=6379, decode_responses=True)

# ---------------- PARAMETERS ----------------
ALPHA = 0.7
TIMEOUT = 10  # seconds
SEQ_LEN = 10  # number of past records


# ---------------- TRANSFORMER MODEL ----------------
class TrustTransformer(nn.Module):
    def __init__(self, input_dim=3, d_model=32, nhead=4, num_layers=2):
        super().__init__()

        self.embedding = nn.Linear(input_dim, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.fc = nn.Linear(d_model, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)

        # take last timestep output
        x = x[:, -1, :]

        x = self.fc(x)
        return self.sigmoid(x)


# ---------------- LOAD MODEL ----------------
model = TrustTransformer()
model.eval()

# initialize weights (pseudo-trained)
for param in model.parameters():
    if param.dim() > 1:
        nn.init.xavier_uniform_(param)


# ---------------- TRANSFORMER SCORE ----------------
def compute_score(data_list):
    if len(data_list) < 5:
        return 0.5

    sequence = []

    for item in data_list[-SEQ_LEN:]:
        d = json.loads(item)

        sequence.append([
            d["latency"] / 1000,   # better normalization
            d["success_rate"],
            d["error_rate"]
        ])

    sequence = np.array(sequence)
    sequence = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0)

    # Transformer output
    with torch.no_grad():
        transformer_score = model(sequence).item()

    # 🔥 Rule-based correction (VERY IMPORTANT)
    latest = json.loads(data_list[-1])

    latency = latest["latency"]
    success = latest["success_rate"]
    error = latest["error_rate"]

    rule_score = (
        0.4 * success +
        0.3 * max(0, 1 - latency / 1000) +
        0.3 * (1 - error)
    )

    # 🔥 Combine both
    final_score = 0.5 * transformer_score + 0.5 * rule_score

    return max(0, min(final_score, 1))

# ---------------- TRUST UPDATE ----------------
def update_trust(node_id):
    key = f"node:{node_id}"
    trust_key = f"trust:{node_id}"

    data_list = r.lrange(key, -SEQ_LEN, -1)

    if not data_list:
        return None

    # 🔥 Transformer-based score
    current_score = compute_score(data_list)

    old_trust = r.get(trust_key)
    old_trust = float(old_trust) if old_trust else 0.5

    # smoothing
    new_trust = ALPHA * old_trust + (1 - ALPHA) * current_score

    r.set(trust_key, new_trust)

    return new_trust


# ---------------- TRUST DECAY ----------------
def apply_decay(node_id):
    key = f"node:{node_id}"
    trust_key = f"trust:{node_id}"

    data = r.lrange(key, -1, -1)

    if not data:
        return

    last = json.loads(data[0])
    last_time = last["timestamp"]

    if time.time() - last_time > TIMEOUT:
        old_trust = float(r.get(trust_key) or 0.5)
        decayed = old_trust * 0.9
        r.set(trust_key, decayed)