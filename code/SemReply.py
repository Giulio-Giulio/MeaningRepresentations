import regex as re
import spacy
import amrlib
import smatch
from smatch import amr

from WikiSearcher import WikiSearcher

from time import time


class SemReply:
    """
    Class for answering questions using Wikipedia and semantic
    representations (AMRs).
    """
    
    def ask(question, n_answers=5, n_sentences=10, return_scores=False, skim_sentences=False):
        """
        Takes in a question, searches a Wikipedia article about it,
        and parses the article into AMRs (semantic representations)
        to find the best sentence from the article to reply to the
        question.

        Args:
            question (str): question or query.
            n_answers (int, optional): how many sentences should be returned. Defaults to 5.
            n_sentences (int, optional): how many sentences from the article will be parsed. Defaults to 20.
            skim_sentences(bool, optional): whether to do an initial skimming of the sentences based on lemma matching. Defaults to False.

        Returns:
            list: list of top sentences answering the question.
        """
        # search, scrape, and segment wiki article
        print("Retrieving wiki article...", end="")
        searcher = WikiSearcher()
        url, text = searcher.search(question)
        sentences = SemReply._segment_sentences(text)
        print(f"\rRetrieved content of {url} in {round(time() - start)} seconds")
        # question -> AMR
        model = amrlib.load_stog_model("resources/model_stog")
        query_amr = model.parse_sents([question])[0]
        query_amr = " ".join(query_amr.split("\n")[1:]) # remove initial comment line
        # lemma-based skimming of the sentences
        if skim_sentences:
            sentences = SemReply._skim_sentences(sentences, query_amr)
        # compute smatch F score between question and sentences
        return SemReply.score_sentences(sentences, model, query_amr, n_sentences, n_answers, return_scores)

    def score_sentences(sentences, model, query_amr, n_sentences, n_answers, return_scores):
        # sentences -> AMRs
        print("Parsing AMRs...", end="", flush=True)
        search_amrs = model.parse_sents(sentences[:n_sentences])
        # compute smatch F score between question and sentences
        print("Computing SMATCH scores...", end="")
        sent2f = dict() # sentence idx to F score
        for i, search_amr in enumerate(search_amrs):
            search_amr = " ".join(search_amr.split("\n")[1:]) # remove initial comment line
            best_match_num, test_triple_num, gold_triple_num = smatch.get_amr_match(query_amr, search_amr)
            f_score = smatch.compute_f(best_match_num, test_triple_num, gold_triple_num)
            sent2f.update({i: f_score})
        # rank article sentences based on F score
        top_matches = sorted(sent2f.items(), key=lambda x: x[1][2], reverse=True)[:n_answers]
        if return_scores:
            return [(sentences[i], f) for i, f in top_matches]
        else:
            return [sentences[i] for i, _ in top_matches]
    
    def _segment_sentences(text):
        """
        Turns a text into a list of sentences using spacy.

        Args:
            text (str): English text as a string.

        Returns:
            list: list of sentences from the text.
        """
        doc = spacy.load("en_core_web_sm")(text)
        return [re.sub(r"\n+", " ", sent.text) for sent in doc.sents]
    
    
    def _skim_sentences(sentences, query_amr):
        skimmed_sentences = list()
        query_lemmas = SemReply._extract_query_main_lemmas(query_amr)
        for sentence in sentences:
            sentence_lemmas = SemReply._extract_sentence_lemmas(sentence)
            if len(query_lemmas.intersection(sentence_lemmas)) > 0:
                skimmed_sentences.append(sentence)
        print(len(sentences))
        print(len(skimmed_sentences))
        return skimmed_sentences


    def _extract_query_main_lemmas(query_amr_str):
        query_amr_line = amr.AMR.get_amr_line(query_amr_str.split("\n"))
        query_amr = amr.AMR.parse_AMR_line(query_amr_line)
        instance_triples, _, relation_triples = query_amr.get_triples()
        var_unknown = ""
        for _, var, concept in instance_triples:
            if concept == "amr-unknown":
                var_unknown = var
                break
        rel_unknown = ""
        for _, rel, var in relation_triples:
            if var == var_unknown:
                rel_unknown = rel
                break
        siblings_unknown = list()
        for _, rel, var in relation_triples:
            if rel == rel_unknown and var != var_unknown:
               for _, var2, concept in instance_triples:
                   if var2 == var:
                        siblings_unknown.append(concept)
        for _, var, concept in instance_triples:
            if var == rel_unknown:
                rel_unknown = concept
                break
        lemmas = set()
        for concept in [rel_unknown] + siblings_unknown:
            lemmas.add(concept.split("-")[0])
        return lemmas
    
    
    def _extract_sentence_lemmas(sentence):
        nlp = spacy.load('en_core_web_sm',  disable=["parser", "ner"])
        lemmas = set()
        for token in nlp(sentence):
            lemmas.add(token.lemma_)
        return lemmas
    
     
if __name__ == "__main__":
    SemReply.ask("When was the telephone invented?", n_answers=1, n_sentences=1)