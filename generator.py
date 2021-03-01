## Generates a content.html file
## with entries for each page on the wiki
## with summaries
from mediawiki import MediaWiki
from bs4 import BeautifulSoup as BS
import dic_creator
import concurrent.futures
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

QUERY_LIMIT = 50000
URL = "https://witcher.fandom.com/api.php"
MAX_THREADS = 8

# This is a bit hacky solution, but it seems to work
# Retrieves the summary of a wiki page by joining
# all the p elements going backwards from the TOC
def getSummaryFromHtml(html):
    soup = BS(html, 'html.parser')
    summary = ""
    elem = soup.select_one("#toc")
    if not elem:
        return None
    elem = elem.find_previous("p")
    if not elem:
        return None
    while(elem and elem.name=="p" and elem.text != ""):
        if elem.find("aside"):
            elem = elem.previous_sibling
            continue;
        summary = elem.text+summary
        elem = elem.previous_sibling
    return summary

def getAllTitles(wiki_obj):
    titles = wiki_obj.allpages(results=QUERY_LIMIT)
    # Retrive all page titles from wiki
    while True:
        res = wiki_obj.allpages(titles[-1],results=QUERY_LIMIT)
        if res[-1]==titles[-1]:
            titles = list(set(titles))
            break
        titles.extend(res)
    return titles

def gen_entry(wiki_obj, title):
    try:
        p = wiki_obj.page(title)
        summary = getSummaryFromHtml(p.html)
        if summary:
            return dic_creator.create_entry(p.title, summary)
    except ValueError as exc:
        return None




def main():

    wiki = MediaWiki(url=URL)
    gen_entry_lam = lambda x : gen_entry(wiki, x)

    print("Retriving all titles")
    titles = getAllTitles(wiki)
    titles.sort()

    print("Retriving summaries for titles")
    entries = thread_map(gen_entry_lam, titles, max_workers=MAX_THREADS)
    entries = list(filter(None, entries))

    print("Creating file lines")
    file_lines = dic_creator.create_file_text_lines(entries)
    print("Writing to file")
    with open("content.html","w") as file:
        file.writelines(file_lines)

if __name__ == "__main__":
    main()

