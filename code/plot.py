from matplotlib import pyplot as plt
import csv

FILES = {
    "SBERT": "evaluation_SBERT_20.csv",
    "SMATCH": "evaluation_SMATCH_20.csv"
    }

for file in FILES.items():
    ndcg = list()
    time = list()
    with open(file[1], "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for entry in reader:
            ndcg.append(float(entry[1]))
            time.append(float(entry[2]))
            
    
    plt.hist(sorted(ndcg), linewidth=8.0)
    plt.xlabel("Normalized Discounted Cumulative Gain (NDCG)")
    plt.ylabel("N samples")
    plt.title(file[0]+" ranking performance")
    plt.show()
    plt.hist(sorted(time), linewidth=8.0)
    plt.xlabel("Time (seconds)")
    plt.ylabel("N samples")
    plt.title(file[0]+" time performance")
    plt.show()