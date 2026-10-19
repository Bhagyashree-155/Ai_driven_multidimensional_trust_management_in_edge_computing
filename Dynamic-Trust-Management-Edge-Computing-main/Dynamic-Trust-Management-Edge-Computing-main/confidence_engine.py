import json

def score_annotation(a):
    x = a["annotations"]

    score = 0.0

    if x["latency"] < 200:
        score += 0.2
    else:
        score -= 0.1

    score += 0.3 * x["success_rate"]
    score += 0.2 * x["availability"]

    if x["cpu"] < 70:
        score += 0.1
    else:
        score -= 0.05

    if x["memory"] < 80:
        score += 0.1

    return max(0.0, min(1.0, score))


def compute_confidence(r, node):
    raw = r.lrange(f"annotation:{node}", 0, 9)

    if not raw:
        return 0.0

    anns = [json.loads(x) for x in raw]
    scores = [score_annotation(a) for a in anns]

    return sum(scores) / len(scores)