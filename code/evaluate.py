from SemReply import SemReply

import amrlib
from sklearn.metrics import ndcg_score
from time import time
import os


DIRECTORY = "evaluation items"
FILES = [os.fsdecode(file) for file in os.listdir(DIRECTORY)]
OUTPUT_FILE = open("evaluation_baseline_20.txt", "a", encoding="utf-8")
N_SENTENCES = 10


results = dict()
for FILE in FILES:
    gold_scores = dict()
    sentences = list()
    lines = open(DIRECTORY+"/"+FILE, "r", encoding="utf-8")
    question = next(lines).strip()
    print(question)
    for i, line in enumerate(lines):
        score, sentence = line.strip().split(",", 1)
        sentences.append(sentence)
        gold_scores.update({i: int(score)})

    predictions = list()
    model = amrlib.load_stog_model("resources/model_stog")
    query_amr = model.parse_sents([question])[0]
    query_amr = " ".join(query_amr.split("\n")[1:]) # remove initial comment line
    gold = list()
    for sentence, (_, _, f_score) in SemReply.score_sentences(sentences, model, query_amr, n_sentences=10, n_answers=10, return_scores=True):
        predictions.append(f_score)
        gold.append(gold_scores[sentences.index(sentence)])

    results[FILE] = ndcg_score([gold[:N_SENTENCES]], [predictions[:N_SENTENCES]])
    OUTPUT_FILE.write(question+"\n")
    OUTPUT_FILE.write(str(results[FILE])+"\n\n")
    

print(results)
