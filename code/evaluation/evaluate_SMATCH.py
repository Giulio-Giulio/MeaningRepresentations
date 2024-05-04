from SemReply import SemReply

import amrlib
from sklearn.metrics import ndcg_score
from time import time
import os


DIRECTORY = "evaluation items"
FILES = [os.fsdecode(file) for file in os.listdir(DIRECTORY)]
OUTPUT_FILE = open("evaluation_SMATCH_20.txt", "a", encoding="utf-8")
N_SENTENCES = 20


results = dict()
for FILE in FILES:
    # Load data
    gold_scores = dict()
    sentences = list()
    lines = open(DIRECTORY+"/"+FILE, "r", encoding="utf-8")
    question = next(lines).strip()
    print(question)
    for i, line in enumerate(lines):
        score, sentence = line.strip().split(",", 1)
        sentences.append(sentence)
        gold_scores.update({i: int(score)})

    # Smatch ranking
    start_time = time()
    predictions = list()
    model = amrlib.load_stog_model("resources/model_stog")
    query_amr = model.parse_sents([question])[0]
    query_amr = " ".join(query_amr.split("\n")[1:]) # remove initial comment line
    sentence_scores = SemReply.score_sentences(sentences, model, query_amr, n_sentences=N_SENTENCES, n_answers=N_SENTENCES, return_scores=True)
    end_time = time() - start_time
    
    # Compute NCDG
    gold = list()
    for sentence, (_, _, f_score) in sentence_scores:
        predictions.append(f_score)
        gold.append(gold_scores[sentences.index(sentence)])
    results[FILE] = ndcg_score([gold[:N_SENTENCES]], [predictions[:N_SENTENCES]])
    OUTPUT_FILE.write(question+"\n")
    OUTPUT_FILE.write(f"NDCG: {results[FILE]} - Time: {end_time} seconds\n\n")
    

print(results)
