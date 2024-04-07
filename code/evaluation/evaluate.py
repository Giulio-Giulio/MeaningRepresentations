from SemReply import SemReply


from sklearn.metrics import ndcg_score
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from time import time
import json

FILE = "queries/whereissicily.csv"

gold = list()
for line in open(FILE, "r", encoding="utf-8"):
    score, sentence = line.strip().split(",", 1)
    gold.append(score)

predictions = list()
for sentence, score in SemReply().ask("Where is Sicily?", n_sentences=10, return_scores=True):
    predictions.append(score)

print(ndcg_score(gold, predictions))


