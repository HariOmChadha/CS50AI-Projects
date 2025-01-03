import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl("corpus0")
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
    dict = {}
    pages = list(corpus.keys())
    for p in pages:
        if p in corpus[page]:
            dict[p] = (1 - damping_factor)/len(pages) + damping_factor/(len(pages) - 1)
        else:
            dict[p] = 0
    
    if corpus[page] == {}:
        for p in pages:
            dict[p] = 1/len(pages)
    else:
        dict[page] = (1 - damping_factor)/len(pages)
    return dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    dict = {page: 0.0 for page in pages}
    choice = random.choice(pages)
    dict[choice] += 1
    for i in range (1, n):
        options = transition_model(corpus, choice, damping_factor)
        choice = random.choices(list(options.keys()), weights = list(options.values()))
        choice = choice.pop()
        dict[choice] += 1
    for p in dict.keys():
        dict[p] /= n
    return dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    dict = {page: 1.0/len(pages) for page in pages}
    change = True
    while change:
        change = False
        for page in pages:
            old = dict[page]
            sum = 0
            check = corpus[page]
            if check == {}:
                check = list(corpus.keys())

            for i in pages:
                if page in corpus[i] or corpus[i] == {}:
                    sum += dict[i]/(len(corpus[i]) if corpus[i] != {} else len(corpus.keys()))

            dict[page] = (1 - damping_factor)/len(pages) + damping_factor*sum
            if abs(old - dict[page]) > 0.001:
                change = True
    return dict

if __name__ == "__main__":
    main()
    #sample_pagerank({"A":1, "B":2}, "A", 10)