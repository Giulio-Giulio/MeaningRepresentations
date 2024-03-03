# Parametres
API_KEY = "AIzaSyC_QwWK92uqibxcparazASdZSLLUH-nQPM"
SEARCH_ENGINE_ID = "433439d65ad294955"
query = "When was Palermo founded?"

# TODO Extract main ARG of query

# Google Custom Search API
print("Searching on Google...")
import requests

url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
data = requests.get(url).json()
# get the result items
search_items = data.get("items")
for i in search_items:
    print(i.get("link"))
first_item = search_items[0]  
    # get the page title
title = first_item.get("title")
    # page snippet
snippet = first_item.get("snippet")
    # alternatively, you can get the HTML snippet (bolded keywords)
html_snippet = first_item.get("htmlSnippet")
    # extract the page url
link = first_item.get("link")


# Web Scraper
print("Scraping Wikipedia article...")
from bs4 import BeautifulSoup
import regex as re

page = requests.get(link)
soup = BeautifulSoup(page.content, "html.parser")
#TODO Following 2 loops to one 
for table in soup("table"):
    table.decompose()
for style in soup("style"):
    style.decompose()

ref_res = ""
#find all the tags p li and h2
r = soup.find("div", {"class" : "mw-content-ltr mw-parser-output" }).findAll(["p", "li", "h2"])
#exclude the unwanted tag
for element in r:
    if element.name == "h2":
        if "See also" in element.text: break
        else: continue
    ref_res += '\n' + ''.join(element.findAll(string = True))
#get rid of reference links
res = re.sub(r'\[(\d+|update|citation needed)\]', '', ref_res)


# AMR
print("Parsing AMRs...")
import amrlib as amr
import spacy

# sentence segmentation
doc = spacy.load("en_core_web_sm")(res)
sentences = list()
for sent in doc.sents:
    sentences.append(re.sub(r"\n", "", sent.text))

# semantic parsing
model = amr.load_stog_model("resources/model_stog")
query_amr = model.parse_sents([query])[0]
search_amrs = model.parse_sents(sentences[:10])


# smatch
import smatch

sent2f = dict()
query_amr = " ".join(query_amr.split("\n")[1:]) # remove initial comment line
for i, search_amr in enumerate(search_amrs):
    search_amr = " ".join(search_amr.split("\n")[1:]) # remove initial comment line
    
    best_match_num, test_triple_num, gold_triple_num = smatch.get_amr_match(query_amr, search_amr)
    f_score = smatch.compute_f(best_match_num, test_triple_num, gold_triple_num)
    sent2f.update({i: f_score})


top_matches = sorted(sent2f.items(), key=lambda x: x[1], reverse=True)
for i, _ in top_matches:
    print(sentences[i])
    
# TODO filter out sentences that do not contain the unknown (e.g. )
# https://github.com/SapienzaNLP/spring 

# scrematura frasi
# parse della domanda -> estrazione del predicate dell'amr-unknown e dei suoi "sibling"