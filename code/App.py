from SemReply import SemReply

"""
(Note to delete)

Interface (on the terminal or GUI) for SemReply
"""

def app():
    prompt = "x"
    while prompt.strip():
        prompt = input("\nAsk a question about a famous person, event, place, or anything:\n")
        for i, result in enumerate(SemReply.ask(prompt)):
            print("\t"+str(i)+".", result)

if __name__ == "__main__":
    app()