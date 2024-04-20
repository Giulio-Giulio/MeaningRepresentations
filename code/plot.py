from matplotlib import pyplot as plt
import csv

FILES = {
    "SBERT": "evaluation_SBERT_20.csv",
    "Smatch": "evaluation_SMATCH_20.csv"
    }

# load data
ndcg = dict()
time = dict()
for file in FILES.items():
    ndcg_tmp = list()
    time_tmp = list()
    with open(file[1], "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for entry in reader:
            ndcg_tmp.append(float(entry[1]))
            time_tmp.append(float(entry[2]))
    ndcg.update({file[0]: ndcg_tmp})
    time.update({file[0]: time_tmp})

# Plot ranking performance
print("\nRanking performance")
print("SBERT Average:", round(sum(ndcg["SBERT"]) / len(ndcg["SBERT"]), 2))
print("Smatch Average:", round(sum(ndcg["Smatch"]) / len(ndcg["Smatch"]), 2))
fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
fig.suptitle("Ranking Performance", fontweight="bold")
fig.text(0.5, 0.04, "Normalized Discounted Cumulative Gain (NDCG)", ha="center")
fig.text(0.04, 0.5, "N samples", va="center", rotation="vertical")
ax1.hist(sorted(ndcg["SBERT"]), linewidth=8.0)
ax1.set_title("SBERT")
ax2.hist(sorted(ndcg["Smatch"]), linewidth=8.0)
ax2.set_title("Smatch")
plt.show()

# Plot time performance
print("\nTime performance")
print("SBERT Average:", round(sum(time["SBERT"]) / len(time["SBERT"]), 2))
print("Smatch Average:", round(sum(time["Smatch"]) / len(time["Smatch"]), 2))
fig, (ax1, ax2) = plt.subplots(2, sharey=True)
fig.suptitle("Time Performance", fontweight="bold")
fig.text(0.5, 0.04, "Time (Seconds)", ha="center")
fig.text(0.04, 0.5, "N samples", va="center", rotation="vertical")
ax1.hist(sorted(time["SBERT"])[:-1], linewidth=8.0) # remove outlier
ax1.set_title("SBERT")
ax2.hist(sorted(time["Smatch"]), linewidth=8.0)
ax2.set_title("Smatch")
plt.show()