"""
    This script is to model the relationship between share price and other quantitative indexes (QIs) such as cpi, gdp,
    cash rate, dividend and etc.

        - cpi, gdp, unemployment rate, current account, government finance (IMF)
                            https://www.imf.org/external/datamapper/datasets
        - cash rate (RBA)   https://www.rba.gov.au/statistics/cash-rate/
        - dividend (ASX)    https://www.intelligentinvestor.com.au/
    -----------------------------------------------------------------------------------------------
        - share (ASX)       https://www.marketindex.com.au/
"""

import numpy as np
import pandas as pd
from sklearn.feature_selection import RFECV
from sklearn.svm import LinearSVR

imf_qis_filenames = {
    'cpi': "data/imf/imf-inflation-20200422.csv",
    'gdp': "data/imf/imf-gdp-20200422.csv",
    'ppl': "data/imf/imf-people-20200422.csv",
    'acc': "data/imf/imf-current account-20200422.csv",
    'fin': "data/imf/imf-government finance-20200422.csv",
}

imf_qis_ingest_params = {
    'header': 0,
    'index_col': 0,
    'encoding': 'ISO-8859-1',
}

cash_rate_ingest_params = {
    'filepath_or_buffer': "data/cash_rate.csv",
    'header': 0,
    'index_col': 'effective_date',
    'dtype': {'effective_date': str,
              'change_points': float,
              'cash_rate_target': float,
              'related_documents': str,
              },
    'parse_dates': ['effective_date'],
}

dividend_ingest_params = {
    'header': 0,
    'index_col': 'ex_dividend_date',
    'dtype': {'sector': str,
              'market_cap': str,
              'distribution_type': str,
              'dividend': float,
              'franking': str,
              'ex_dividend_date': str,
              'payment_date': str,
              'current_price': str,
              'price_7d_avg': str,
              'dividend_yield': str,
              },
    'parse_dates': ['ex_dividend_date', 'payment_date'],
}

share_ingest_params = {
    'header': 0,
    'dtype': {'date': str,
              'open': float,
              'high': float,
              'low': float,
              'close': float,
              'volume': float,
              },
    'parse_dates': ['date'],
}


def imf_qis_ingest(filenames, ingest_params):
    """
        Ingest IMF QIs.
    """
    imf_qis = dict()
    for qi_name, filename in filenames.items():
        df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)
        qi = df.loc["Australia"]
        qi.index = pd.to_datetime(qi.index)
        qi = pd.to_numeric(qi, errors='coerce', downcast='float').dropna()
        imf_qis[qi_name] = qi

    return imf_qis


def cash_rate_ingest(ingest_params):
    """
        Ingest cash rate.
    """
    df = pd.read_csv(**ingest_params)
    cash = df["cash_rate_target"]

    return cash


def dividend_ingest(asx_code, ingest_params):
    """
        Ingest dividend.
    """
    filename = "data/{asx_code}_dividend.csv".format(asx_code=asx_code)
    df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)
    div = df["dividend"]
    # Deal with duplicated dates.
    div = div.groupby(div.index).agg(sum)

    return div


def share_ingest(asx_code, ingest_params):
    """
        Ingest share.
    """
    filename = "data/{asx_code}.csv".format(asx_code=asx_code)
    df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)
    share = df[["date", "close", "volume"]]

    return share


def extract_qi(date, qi):
    """
        If date appears exactly in QI, it returns the rate that corresponds to the date; otherwise, it returns
        the rate that corresponds to the closet date (later) appeared in QI.
    """
    if date in qi:
        rate = qi[date]
    else:
        closet_date = None
        for index_date in qi.index:
            if not closet_date:
                if (date - index_date).days >= 0:
                    closet_date = index_date
            elif (date - index_date).days >= 0 and index_date > closet_date:
                closet_date = index_date
        rate = qi[closet_date]

    return rate


def collate_qis(row, qis):
    date = row.date
    for qi_name, qi in qis.items():
        row[qi_name] = extract_qi(date, qi)

    return row


def collate(asx_code):
    # Ingest QIs.
    imf_qis = imf_qis_ingest(imf_qis_filenames, imf_qis_ingest_params)
    cash_rate = cash_rate_ingest(cash_rate_ingest_params)
    dividend = dividend_ingest(asx_code, dividend_ingest_params)

    qis = imf_qis
    qis['cash'] = cash_rate
    qis['div'] = dividend

    # Ingest share.
    share = share_ingest(asx_code, share_ingest_params)

    collated_share = share.apply(lambda row: collate_qis(row, qis), axis=1)

    return collated_share


def feature_extraction(asx_code):
    df = collate(asx_code)
    df.to_csv("data/{asx_code}_collated.csv".format(asx_code="tls"), index=False)
    return df


def feature_selection(asx_code, qi_names, y_col_name='close'):
    """
        Select QIs (features) that influence the share's price most significantly.
    """
    df = pd.read_csv("data/{asx_code}_collated.csv".format(asx_code=asx_code))

    X = df[qi_names]
    y = df[y_col_name]

    svr = LinearSVR(max_iter=10000)
    selector = RFECV(estimator=svr, cv=5)
    selector.fit(X, y)

    selected_qi_names = np.array(qi_names)[selector.support_]
    print("The most significant QIs are:", list(selected_qi_names))
    return selected_qi_names


def main():
    # 1 feature engineering
    # --------------------------------------------------------------------------------------------------
    # 1.1 feature extraction
    feature_selection('tls')

    # 1.2 feature selection
    qi_names = ['volume', 'cpi', 'gdp', 'ppl', 'acc', 'fin', 'cash', 'div']
    selected_qi_names = feature_selection('tls', qi_names)
    #  selected_qi_names = ['volume', 'gdp', 'ppl', 'cash', 'div']

    # 2 fit
    # --------------------------------------------------------------------------------------------------
    # 2.1 parameter selection

    # apply

    # reg = linear_model.BayesianRidge()
    # reg.fit(X, Y)
    #
    # # predict the share price by giving the other factors.
    # vol = 28400448
    # cpi = 1.5
    # gdp = 1.2
    # people = 8.5
    # account = -3
    # finance = -2.5
    # cash = 0.25
    # div = 8
    #
    # x = [vol, cpi, gdp, people, account, finance, cash, div]
    # y = reg.predict([x])
    # print(y)


if __name__ == "__main__":
    # execute only if run as a script
    main()
