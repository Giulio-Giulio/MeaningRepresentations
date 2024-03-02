import regex as re
import spacy
import amrlib as amr
import smatch

from WikiSearcher import WikiSearcher


class SemReply:
    """
    Class for answering questions using Wikipedia and semantic
    representations (AMRs).
    """
    
    def ask(question, n_answers=5, n_sentences=10):
        """
        Takes in a question, searches a Wikipedia article about it,
        and parses the article into AMRs (semantic representations)
        to find the best sentence from the article to reply to the
        question.

        Args:
            question (str): question or query.
            n_answers (int, optional): how many sentences should be returned. Defaults to 5.
            n_sentences (int, optional): how many sentences from the article will be parsed. Defaults to 20.

        Returns:
            list: list of top sentences answering the question.
        """
        # search, scrape, and segment wiki article
        searcher = WikiSearcher()
        _, text = searcher.search(question)
        sentences = SemReply._segment_sentences(text)
        # sentences -> AMRs
        model = amr.load_stog_model("resources/model_stog")
        query_amr = model.parse_sents([question])[0]
        search_amrs = model.parse_sents(sentences[:n_sentences])
        # compute smatch F score between question and sentences
        sent2f = dict() # sentence idx to F score
        query_amr = " ".join(query_amr.split("\n")[1:]) # remove initial comment line
        for i, search_amr in enumerate(search_amrs):
            search_amr = " ".join(search_amr.split("\n")[1:]) # remove initial comment line
            best_match_num, test_triple_num, gold_triple_num = smatch.get_amr_match(query_amr, search_amr)
            f_score = smatch.compute_f(best_match_num, test_triple_num, gold_triple_num)
            sent2f.update({i: f_score})
        # rank article sentences based on F score
        top_matches = sorted(sent2f.items(), key=lambda x: x[1], reverse=True)[:n_answers]
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
        return [re.sub(r"\n+", "\n", sent.text) for sent in doc.sents]