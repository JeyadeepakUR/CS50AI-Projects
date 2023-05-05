from operator import truediv
import os
import random
import re
import sys

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
    n = len(corpus)
    
    res = dict()
    m = len(corpus[page])
    for i in corpus:
        if len(corpus[page]) != 0:
            if i in corpus[page]:
                res[i] = (1 - damping_factor) / n + damping_factor / m
            else:
                res[i] = (1 - damping_factor) / n
        else:
            res[i] = 1 / n
            
    return res

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples_dict = corpus.copy()
    for i in samples_dict:
        samples_dict[i] = 0
    sample = None

    for _ in range(n):
        if sample:
            dist = transition_model(corpus, sample, damping_factor)
            dist_lst = list(dist.keys())
            dist_weights = [dist[i] for i in dist]
            sample = random.choices(dist_lst, dist_weights, k=1)[0]
        else:
            sample = random.choice(list(corpus.keys()))

        samples_dict[sample] += 1

    for item in samples_dict:
        samples_dict[item] /= n

    return samples_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    old_dict = {}
    corpus_reverse = dict()
    numlinks = dict()
    
    for i in corpus:
        corpus_reverse[i] = set()
        if (len(corpus[i]) == 0):
            corpus[i] = set(corpus.keys())
        
    for i in corpus:
        for j in corpus[i]:
            corpus_reverse[j].add(i)
        numlinks[i] = len(corpus[i])
   
    for i in corpus:
        old_dict[i] = 1/n

    while True:
        new_page = dict()
        for i in corpus:
            new_page[i] = (1-damping_factor)/n
            for j in corpus_reverse[i]:
                new_page[i] += damping_factor*old_dict[j]/numlinks[j]
        s = 0
        flag = True
        for i in corpus:
            diff = abs(new_page[i]-old_dict[i])
            if diff > 0.001:
                flag = False
            old_dict[i] = new_page[i]
            s += old_dict[i]
        if flag:
            break
    return old_dict
    
if __name__ == "__main__":
    main()
