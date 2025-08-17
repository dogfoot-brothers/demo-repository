from rapidfuzz.fuzz import token_set_ratio

def normalize(s):
    return s.lower().strip()

def fuzzy_score(a, b):
    return token_set_ratio(normalize(a), normalize(b)) / 100

def keyword_coverage(pred, keywords):
    p = normalize(pred)
    hit = sum(1 for kw in keywords if kw in p)
    return hit / max(1, len(keywords))

def composite_score(output, reference, keywords):
    return 0.8 * fuzzy_score(output, reference) + 0.2 * keyword_coverage(output, keywords)

