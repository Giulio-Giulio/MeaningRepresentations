import csv
import os
from WikiSearcher import WikiSearcher
from SemReply import SemReply

PATH = "../code/evaluation"
QUERIES = ["What is Semantic?","What is the Fibonacci sequence?","what is the first book printed?","what is the aurora borealis?,","what is the most selled music album?","what is a semantic parser?","what are the causes of second world war?","what is python?","what are the main fields of linguistics?","What is the millennium bug?","What is the concept of inertia in physics?","When did the Industrial Revolution begin?","When was the Declaration of Independence signed?","When did humans first land on the Moon?","When did the Protestant Reformation begin?","When did World War II end?","When was the invention of the printing press?","When was the fall of the Roman Empire?","When was the first vaccine developed?","When was the first computer virus discovered?","When was the start of the Great Depression?","When was the first modern Olympic Games held?","When did the internet become publicly available?","where is Tübingen","Where is the Great Barrier Reef located?","Where was the Declaration of Independence signed?","Where is the Amazon forest located?","Where is Everest located?","Where is the Great Wall?","Where is the Etna?","Where is the Po' river's basin located?","Where is the Valley of the Kings?","Where is the Dead Sea located?","Where is the largest active volcano in Japan located?","where","Who painted Monnalisa?","Who wrote the Decameron?","Who is the Jhon Kennedy' murder?","Who has been the first president of United States of America?","Who are the Apple's founders?","Who was the first woman to win a Nobel Prize?","Who founded the Red Cross?","who was Sigmund Freud?","Who is Peter Sloterdijk?","Who founded the social networking site Facebook?","Who founded the philosophy of existentialism?","Who was the first person to win the Nobel Prize in Literature?"]
for query in QUERIES:
    try:
        file = f'{query.lower().replace(" ", "").replace("?", "")}.csv'
        file_path = os.path.join(PATH, file)

        # create a csv file for each query
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # initialize CSV writer and file
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([query])

            searcher = WikiSearcher()
            _, txt = searcher.search(query)
            text = SemReply._segment_sentences(txt)
            for t in text[:20]:
                csv_writer.writerow([" ", t])
    except Exception as e:
        print(f"Error '{query}': {e}")
        continue 