from sklearn.metrics import ndcg_score
from time import time
import os

from sentence_transformers import SentenceTransformer, util
import torch


DIRECTORY = "evaluation items"
FILES = [os.fsdecode(file) for file in os.listdir(DIRECTORY)]
OUTPUT_FILE = open("evaluation_SBERT_20.txt", "a", encoding="utf-8")
N_SENTENCES = 20

embedder = SentenceTransformer("all-MiniLM-L6-v2")

results = dict()
for FILE in FILES:
    # Load data
    gold_scores = dict()
    sentences = list()
    lines = open(DIRECTORY+"/"+FILE, "r", encoding="utf-8")
    question = next(lines).strip()
    for i, line in enumerate(lines):
        score, sentence = line.strip().split(",", 1)
        sentences.append(sentence.strip("\""))
        gold_scores.update({i: int(score)})

    # SBERT ranking
    start_time = time()
    question_embedding = embedder.encode(question, convert_to_tensor=True)
    article_embeddings = embedder.encode(sentences, convert_to_tensor=True)
    cos_scores = util.cos_sim(question_embedding, article_embeddings)[0]
    top_results = torch.topk(cos_scores, k=N_SENTENCES)
    end_time = time() - start_time
    
    # Compute NCDG
    gold = [gold_scores[i.item()] for i in top_results[1]]
    results[FILE] = ndcg_score([gold[:N_SENTENCES]], [top_results[0][:N_SENTENCES]])
    OUTPUT_FILE.write(question+"\n")
    OUTPUT_FILE.write(f"NDCG: {results[FILE]} - Time: {end_time} seconds\n\n")