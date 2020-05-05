import re
import math
import collections
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pymystem3 import Mystem
from nltk.stem.snowball import SnowballStemmer

stemmer = Mystem()
stemmer_nltk = SnowballStemmer("russian")

remove_pattern = re.compile('\W')


def normalize_text(text):
    return remove_pattern.sub(' ', text).lower().strip()


def filter_empty(lst):
    return [i for i in map(lambda x: x.strip(), lst) if len(i) > 0]


def lemm(text):
    return filter_empty(stemmer.lemmatize(normalize_text(text)))


def lemm_m(text):
    return filter_empty(stemmer_nltk.stem(x.strip()) for x in normalize_text(text).split())


def lemm_h(text):
    return list(map(stemmer_nltk.stem, filter_empty(stemmer.lemmatize(normalize_text(text)))))


def norm_stat(kw):
    sm = math.sqrt(sum(map(lambda x: x * x, kw.values())))
    if sm == 0: return {}
    return {i: v / sm for i, v in kw.items()}


def distance(seq1, seq2):
    n, m = len(seq1), len(seq2)
    if n > m: seq1, seq2, n, m = seq2, seq1, m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if seq1[j - 1] != seq2[i - 1]: change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def calc_stat(text, remove_commons=True):
    return keywords(text, remove_commons=remove_commons)


def keywords(text, remove_commons=True):
    if remove_commons:
        normal_stop_words = lemm(" ".join(set(stopwords.words('russian'))) + " ( . : , ! )")
        filtered_words = list(filter(lambda x: not x in normal_stop_words, text))
    else:
        filtered_words = list(text)
    words = [j for j in [i.strip(' .!?"-\u2026,_') for i in filtered_words] if j]
    return freq(words)


def multiply2stats(stat1, stat2, max_dist=2):
    res = {}
    for i, v in stat1.items():
        if max_dist > 0:
            for ii, vv in stat2.items():
                d = distance(i, ii)
                if d <= max_dist:
                    res[(i, ii)] = v * vv
            continue
        vv = stat2.get(i, None)
        if vv is None: continue
        selector = i if max_dist == 0 else (i, i)
        res[selector] = vv * v
    return res


def sum_stat(kw):
    return sum(kw.values())


def freq(it):
    r = collections.defaultdict(int)
    for i in it:
        r[i] += 1
    return dict(r)