import sys, os

from SemReply import SemReply

ANSI = {
    "white": "\x1b[37m",
    "gray": "\033[38;5;247m",
    "blue": "\033[34;3m",
    "reset": "\033[0m"
}


def app(n_answers=3, n_sentences=-1):
    """
     Terminal interface for SemReply.

    Args:
        n_answers (int, optional): Number of top answers shown. Defaults to 3.
        n_sentences (int, optional): Number of article sentences taken into analysis in order of appearance. Defaults to -1 (all).
    """
    print(ANSI["gray"] + f"\n[Currently set on {n_answers} answers]")
    prompt = "x"
    while prompt.strip():
        # prompt user
        question = input(
            ANSI["reset"] +
            ANSI["gray"] +
            "\nAsk a question about a famous person, event, place, or anything:\n" +
            ANSI["white"] +
            "> ")
        if question.strip() == "":
            exit(0)
        
        # get results
        sys.stdout = open(os.devnull, 'w') # disable writing to stdout (printing) FIXME
        results, url = SemReply.ask(question, n_answers=n_answers, n_sentences=n_sentences, skim=False, prerank=False)
        sys.stdout = sys.__stdout__ # enable writing to stdout FIXME
        
        # print results
        print(ANSI["gray"] + "Ranking sentences from:")
        print(ANSI["blue"] + url)
        for i, result in enumerate(results):
            print(ANSI["gray"] + "\t" + str(i+1) +  ".", ANSI["white"] + result.strip())


if __name__ == "__main__":
    app(n_answers=3, n_sentences=20)