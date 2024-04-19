import sys, os

from SemReply import SemReply


def app():
    """
    Terminal interface for SemReply.
    """
    prompt = "x"
    while prompt.strip():
        # prompt user
        question = input("\nAsk a question about a famous person, event, place, or anything:\n")
        if question.strip() == "":
            exit(0)
        
        # get results
        # sys.stdout = open(os.devnull, 'w') # disable writing to stdout (printing) FIXME
        results = SemReply.ask(question, n_answers=10, n_sentences=10, skim=False, prerank=True)
        # sys.stdout = sys.__stdout__ # enable writing to stdout FIXME
        
        # print results
        for i, result in enumerate(results):
            print("\t"+str(i+1)+".", result.strip())


if __name__ == "__main__":
    app()