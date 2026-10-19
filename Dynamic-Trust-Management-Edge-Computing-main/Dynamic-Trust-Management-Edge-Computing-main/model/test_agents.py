from agents import collect, analyze, compute

data = collect("node_1")

if data:
    f = analyze(data)
    score = compute(f)
    print("Trust Score:", score)
else:
    print("No data")