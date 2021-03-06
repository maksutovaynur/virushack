import pandas as pd
import back.lib.stats as S
import  back.lib.tf as T
import os
import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_disease_names_by_text(text, max_len):
    return real_get_disease_by_symptoms(text, max_len)


def get_doctors_by_disease(disease_name, max_len):
    return real_get_doctors_by_disease(disease_name, max_len)


def get_treatments_by_disease(disease_name, max_len):
    return real_get_treatment_by_disease(disease_name, max_len)


def _get_doctor_by_disease(disease_name):
    return f"Doctor against disease '{disease_name}'"


def _get_disease_names_by_text(max_len):
    return [randomword(10).capitalize() for i in range(max_len)]


__desease_cache__ = dict()

_base_name = os.path.abspath(__file__)
_lib_folder = os.path.dirname(_base_name)
_data_folder = os.path.join(_lib_folder, os.pardir, 'data')
converters = {'Tf-Idf': eval, 'KwFilt': eval}
Ph2, Sd2, Pd = map(
    lambda x: pd.read_csv(os.path.join(_data_folder, x), converters=converters),
    ["pharma2-kw-thr0.010000.csv", "def2-kw-thr0.010000.csv", "prof-kw-thr0.010000_1.csv"])


__cache__ = dict()


def real_get_disease_by_symptoms(text, max_des=5, threshold = 0.5):
    input_text = S.keywords(S.lemm_h(text))
    Sd2['tmp'] = Sd2['Tf-Idf'].apply(lambda x: S.multiply2stats(input_text, x, max_dist=0))
    Sd2['tmp_sum'] = Sd2['tmp'].apply(S.sum_stat)
    sSd2 = Sd2.sort_values('tmp_sum', ascending=False)
    candDeseases = sSd2.loc[sSd2.loc[:, 'tmp_sum'] > threshold * sSd2.loc[0, 'tmp_sum']]
    candDeseases = candDeseases.head(max_des)
    if candDeseases.shape[0] == 0:
        return []
    Names = list(candDeseases.loc[:, 'Name'])
    for n in Names:
        __cache__[n] = input_text
    return Names


def real_get_treatment_by_disease(name, max_len=5, threshold=0.1):
    kw = S.keywords(T.lemm(name))
    add_cache = __cache__.get(name, {})
    kw.update(add_cache)
    Ph2['tmp'] = Ph2['Tf-Idf'].apply(lambda x: S.multiply2stats(kw, x, max_dist=0))
    Ph2['tmp_sum'] = Ph2['tmp'].apply(S.sum_stat)
    sPh2 = Ph2.sort_values('Subst')
    sPh2 = sPh2.groupby('Subst').agg({'Name': list, 'Targ': 'first', 'tmp': 'first', 'tmp_sum': 'first'}).reset_index()
    sPh2 = sPh2.sort_values('tmp_sum', ascending=False)
    candPharm = sPh2.loc[sPh2.loc[:, 'tmp_sum'] > threshold * sPh2.loc[0, 'tmp_sum']]
    candPharm = candPharm.loc[:, "Name"].dropna().head(max_len)
    if len(candPharm) == 0:
        return []
    formatNames = [(n, f"https://apteka.ru/search/?q={n.split(' / ', 1)[0]}&order=products%2Cmaterials") for n in list(candPharm.apply(" / ".join))]
    return formatNames


def real_get_doctors_by_disease(name, max_len=2, threshold=0.001):
    kw = S.keywords(T.lemm(name))
    add_cache = __cache__.get(name, {})
    kw.update(add_cache)
    Pd['tmp'] = Pd['Tf-Idf'].apply(lambda x: S.multiply2stats(kw, x, max_dist=0))
    Pd['tmp_sum'] = Pd['tmp'].apply(S.sum_stat)
    sPd = Pd.sort_values('tmp_sum', ascending=False)
    candProf = sPd.loc[sPd.loc[:, 'tmp_sum'] > threshold * sPd.loc[0, 'tmp_sum']]
    candProf = candProf[['Name', 'YandexLink', 'MinPrice', 'RandName']].dropna().head(max_len)
    if candProf.shape[0] == 0:
        candProf = Pd.loc[Pd['Name'] == 'Терапевт']
        # return []
    formatNames = list(candProf.apply(
        lambda x: (x['Name'], x['YandexLink'], x["MinPrice"], x["RandName"]), axis=1))
    return formatNames



