import sys, os

from SemReply import SemReply

ANSI = {
    "white": "\x1b[37m",
    "gray": "\033[38;5;247m",
    "blue": "\033[34;3m",
    "reset": "\033[0m"
}


def app():
    """
    Terminal interface for SemReply.
    """
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
        results, url = SemReply.ask(question, n_answers=5, n_sentences=-1, skim=False, prerank=False)
        sys.stdout = sys.__stdout__ # enable writing to stdout FIXME
        
        # print results
        print(ANSI["gray"] + "Ranking sentences from:")
        print(ANSI["blue"] + url)
        for i, result in enumerate(results):
            print(ANSI["gray"] + "\t" + str(i+1) +  ".", ANSI["white"] + result.strip())


if __name__ == "__main__":
    app()