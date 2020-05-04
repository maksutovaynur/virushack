import gc
import json
import numpy as np
try: import back.lib.stats as S
except: import stats as S
from collections import defaultdict
lemm = S.lemm_h


def sum_dicts(dicts):
    r = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            r[k] += v
    return r


def div_dicts(a, b):
    return {k: v/b[k] for k, v in a.items()}


def count_dicts(dicts):
    r = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            r[k] += 1
    return r


def mul_dicts(a, b):
    return {k: v * b[k] for k, v in a.items()}


def tf_idf(df):
    doc_summs = df.loc[:, 'Kw'].agg(sum_dicts)
    doc_cnts = df.loc[:, 'Kw'].agg(count_dicts)
    idf = {k: np.log(df.shape[0] / v) for k, v in doc_cnts.items()}
    df.loc[:, 'Tf-Idf'] = df.loc[:, 'Kw'].apply(lambda x: div_dicts(x, doc_summs)).apply(lambda x: mul_dicts(x, idf))


def freq_dict(text, suff='ph'):
    txt_lemm = lemm(text)
    kwds = S.keywords(txt_lemm)
    word_cnt = len(kwds)
    word_cnt_log_inv = 1 / np.log2(word_cnt)
    kwds_sorted = sorted(kwds.items(), key=lambda x: -x[1])
    kwds_inverted = {i: word_cnt_log_inv/v for i, v in kwds.items()}
    v = kwds_inverted.values()
    with open(f'{suff}-wordimp.json', 'w') as f:
        f.write(json.dumps(kwds_inverted))
    print(f"Stats: words count: {word_cnt}, log_inv = {word_cnt_log_inv}; min = {min(v)}, max = {max(v)}")
    return kwds_inverted


def prepare_dataset(df, ds_basename, threshold=1e-2, max_len=None):
    Targ = 'Targ'
    Lemm = 'Lemm'
    Kw = 'Kw'
    KwFilt = 'KwFilt'
    df = df.loc[df.loc[:, Targ].notnull()]
    if max_len is not None:
        df = df.head(max_len)
    df.loc[:, Lemm] = df.loc[:, Targ].apply(lemm)
    df.loc[:, Kw] = df.loc[:, Lemm].apply(lambda x: {i: 1 for i, v in S.keywords(x).items()})
    
    tf_idf(df)
    
#     df.loc[:, KwMult] = df.loc[:, Kw].apply(lambda x: S.multiply2stats(kwds_inverted, x, max_dist=0))
    df.loc[:, KwFilt] = df.loc[:, 'Tf-Idf'].apply(lambda x: {i: v for i, v in x.items() if v > max(x.values())*threshold})
#     df.loc[:, FSum] = df.loc[:, KwFilt].apply(lambda x: sum(x.values()))
#     df.loc[:, KwNorm] = df.apply(lambda x: {i: v/x[FSum] for i, v in x[KwFilt].items()}, axis=1)
    
    df.drop([Lemm, Kw], axis=1, inplace=True)
    
    df.to_csv(f'{ds_basename}-kw-thr{threshold:.6f}.csv', index=False)
    gc.collect()
    return df
