import requests
from bs4 import BeautifulSoup
import regex as re


class WikiSearcher:
    """
    Provides methods for searching and scraping Wikipedia articles through
    Google's Custom Search API and Leonard Richardson's Beautiful Soup 4.
    """
    
    def __init__(self, search_engine_id="433439d65ad294955",
                 api_key="AIzaSyC_QwWK92uqibxcparazASdZSLLUH-nQPM"):
        self.search_engine_id = search_engine_id
        self.api_key = api_key
    
    
    def search(self, query, i=0, scrape=True):
        """
        Performs a search with Google's Custom Search API on
        en.wikipedia.org. Returns the url of the ith search result.

        Args:
            query (str): query for google search.
            i (int, optional): index of search result to be considered. Defaults to 0.
            scrape (bool, optional): if True, also returns scraped text content.

        Returns:
            (str, str): (url of ith search result, scraped text content)
        """
        # perform search
        search_url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.search_engine_id}&q={query}"
        data = requests.get(search_url).json()
        # extract link of ith search result
        first_result_url = data.get("items")[i].get("link")
        # return scraped page
        if scrape:
            return first_result_url, self.scrape(first_result_url)
        else:
            return first_result_url
    
    
    def scrape(self, url):
        """
        Scrapes web page, optimized for Wikipedia articles. Extracts
        p and li elements from main content, excluding anything
        coming after the "See also" section. Removes reference indices
        such as [1], [update], [citation needed].

        Args:
            url (str): url of web page.

        Returns:
            str: scraped text as a single string.
        """
        # initialise scraper
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # remove tables and style specifications
        for table in soup("table"):
            table.decompose()
        for style in soup("style"):
            style.decompose()
        for ipa in soup({"class" : "IPA"}):
            ipa.decompose()
        # extract p, li and h2 elements
        r = soup.find("div", {"class" : "mw-content-ltr mw-parser-output" }).findAll(["p", "li", "h2"])
        # convert to string
        text = ""
        for element in r:
            # skip h2 elements and stop once "See also" section is reached
            if element.name == "h2":
                if "See also" in element.text: break 
                else: continue
            text += '\n' + ''.join(element.findAll(string = True))
        # remove reference links
        return re.sub(r'\[(\d+|update|citation needed|N \d+)\]', '', text)