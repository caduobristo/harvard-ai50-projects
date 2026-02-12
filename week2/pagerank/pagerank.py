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
    output = {}
    rand_prob = 1-damping_factor

    links = corpus[page]
    n_pages = len(corpus)

    if len(links) == 0:
        for p in corpus:
            output[p] = 1/len(corpus)
        return output

    for p in corpus:
        output[p] = rand_prob/n_pages

    for link in links:
        output[link] += damping_factor / len(links)

    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {p: 0 for p in corpus}

    sample = random.choice(list(corpus.keys()))

    for i in range(n):
        counts[sample] += 1
        probs = transition_model(corpus, sample, damping_factor)
        sample = random.choices(
            list(probs.keys()),
            weights=probs.values(),
            k=1
        )[0]

    for p in counts:
        counts[p] /= n

    return counts

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {}
    for page in list(corpus.keys()):
        ranks[page] = 1/n

    diff = 1

    while diff > 0.001:
        new_ranks = {}

        for p in corpus:
            pr = (1 - damping_factor) / n
            total = 0
            for i in corpus:
                if p in corpus[i]:
                    total += ranks[i] / len(corpus[i])

                if len(corpus[i]) == 0:
                    total += ranks[i] / n

            pr += damping_factor * total
            new_ranks[p] = pr

        diff = max(abs(new_ranks[p] - ranks[p]) for p in corpus)
        ranks = new_ranks

    return ranks

if __name__ == "__main__":
    main()
