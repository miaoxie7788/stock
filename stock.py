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

import pandas as pd
from sklearn import linear_model

imf_filenames = {
    'cpi': "data/imf/imf-inflation-20200422.csv",
    'gdp': "data/imf/imf-gdp-20200422.csv",
    'unemployment': "data/imf/imf-people-20200422.csv",
    'current': "data/imf/imf-current account-20200422.csv",
    'government': "data/imf/imf-government finance-20200422.csv",
}

imf_ingest_params = {
    'header': 0,
    'index_col': 0,
    'encoding': 'ISO-8859-1',
}

cash_ingest_params = {
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

div_ingest_params = {
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
              'volume': int,
              },
    'parse_dates': ['date'],
}


def imf_ingest(filenames, ingest_params):
    imfs = dict()
    for qi_name, filename in filenames.items():
        df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)
        qi = df.loc["Australia"]
        qi.index = pd.to_datetime(qi.index)
        imfs[qi_name] = qi

    return imfs


def cash_ingest(ingest_params):
    df = pd.read_csv(**ingest_params)
    cash = df["cash_rate_target"]

    return cash


def div_ingest(asx_code, ingest_params):
    filename = "data/{asx_code}_dividend.csv".format(asx_code=asx_code)
    df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)
    div = df["dividend"]

    return div


def share_ingest(asx_code, ingest_params):
    filename = "data/{asx_code}.csv".format(asx_code=asx_code)
    df = pd.read_csv(filepath_or_buffer=filename, **ingest_params)

    return df


def get_rate(date, qi):
    """
        Get
        If date appears exactly in ref, it returns the rate that corresponds to the date; otherwise, it returns
        the rate that corresponds to the closet date (later) appeared in ref.
    """
    if date in qi:
        rate = qi[date]
    else:
        closet_date = None
        for idx in qi.index:
            if not closet_date:
                if (date - idx).days >= 0:
                    closet_date = idx
            elif (date - idx).days >= 0 and idx > closet_date:
                closet_date = idx
        rate = qi[closet_date]

    try:
        rate = float(rate)
    except TypeError:
        rate = 0

    return rate


def collate_qis(row, qis):
    date = row.date
    for qi_name, qi in qis.items():
        row[qi_name] = get_rate(date, qi)

    return row


def collate(asx_code):
    imfs = imf_ingest(imf_filenames, imf_ingest_params)
    cash = cash_ingest(cash_ingest_params)
    div = div_ingest(asx_code, div_ingest_params)

    qis = imfs
    qis['cash'] = cash
    qis['div'] = div

    share = share_ingest(asx_code, share_ingest_params)

    collated_share = share.apply(lambda row: collate_qis(row, qis), axis=1)

    return collated_share


def main():
    collated_share = collate('tls')
    # collated_share.to_csv("data/{asx_code}_collated.csv".format(asx_code="tls"))
    X = collated_share[['volume', 'cpi', 'gdp', 'unemployment', 'current', 'government', 'cash', 'div']]
    Y = collated_share['close'].values

    reg = linear_model.BayesianRidge()
    reg.fit(X, Y)

    # predict the share price by giving the other factors.
    vol = 28400448
    cpi = 1.5
    gdp = 1.2
    unemployment = 8.5
    current = -3
    government = -2.5
    cash = 0.25
    div = 8

    x = [vol, cpi, gdp, unemployment, current, government, cash, div]
    y = reg.predict([x])
    print(y)


if __name__ == "__main__":
    # execute only if run as a script
    main()
