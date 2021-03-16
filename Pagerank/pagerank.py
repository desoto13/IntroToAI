import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    decimal_places = 4
    result = {}
    curr_page = corpus[page]
    total_links = len(corpus)

    if len(curr_page) == 0:
        equal_proba = round(1 / len(corpus), decimal_places)
        for x in corpus:
            result[x] = equal_proba

        return result
    
    random_proba = round(1 - damping_factor, decimal_places)
    random_proba_per_page = round(random_proba / total_links, decimal_places)
    proba_per_page = round(damping_factor / len(curr_page), decimal_places)

    for x in corpus.keys():
        result[x] = random_proba_per_page   

    for x in curr_page:
        result[x] = round(proba_per_page + random_proba_per_page, decimal_places)
    
    return result



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    for page in corpus.keys():
        page_rank[page] = 0

    # # problem assumes n is at least 1
    for i in range(1, n):
        if i == 0:
            page = random.choice(list(corpus.keys()))

        curr_dist = transition_model(corpus, page, damping_factor)
        for key in curr_dist.keys():
            page_rank[key] = page_rank[key] + curr_dist[key]

        page_rank_keys = list(curr_dist.keys())
        page_rank_values = list(curr_dist.values())

        #random.choices(sequence, weights=None, cum_weights=None, k=1)
        page = random.choices(page_rank_keys, weights=page_rank_values)[0]

    for key in page_rank.keys():
        page_rank[key] = round(page_rank[key] / n, 4)

    return page_rank        



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    #initialize 1/N as initial pagerank

    for x in corpus.keys():
        pagerank[x] = 1/len(corpus)
    
    diverged = True
    
    while diverged:
        diverged = False
        pagerank_iterative = copy.deepcopy(pagerank)
        
        for x in corpus.keys():
            pagerank_iteration = 0


            #summation formula
            for i in linkedpages(corpus, x):
                if len(corpus[i]) == 0:
                    pagerank_iteration += pagerank_iterative[i]/len(corpus)
                elif len(corpus[i]) != 0:
                   pagerank_iteration += pagerank_iterative[i]/len(corpus[i])


            pagerank[x] = ((1 - damping_factor)/len(corpus)) + (pagerank_iteration*damping_factor)
         
        for x in pagerank:
            if abs(pagerank_iterative[x] - pagerank[x]) > 0.001:
                diverged = True
                break
    return pagerank_iterative

    #raise NotImplementedError


def linkedpages(corpus, page):
    linkedpage = set()

    for i in corpus.keys():
        if page in corpus[i] or corpus[i] == set():
            linkedpage.add(i)

    return linkedpage


if __name__ == "__main__":
    main()
