"""
This script is to model the relationships among the major quantitative factors that influence share prices using
regression. Basically, it is to predict how volume, cash rate, dividend, inflation rate, and other company-specific
data influence the share price.

The R&D is based on Telstra Corp. Ltd. (TLS).

"""

import pandas as pd
from sklearn import linear_model

tls_ingest_params = {
    'header': 0,
    'index_col': False,
    'dtype': {'date': str,
              'open': float,
              'high': float,
              'low': float,
              'close': float,
              'volume': int,
              },
    'engine': 'c',
    'parse_dates': ['date'],

}

cash_rate_ingest_params = {
    'header': 0,
    'index_col': False,
    'dtype': {'effective_date': str,
              'change_points': float,
              'cash_rate_target': float,
              },
    'engine': 'c',
    'parse_dates': ['effective_date'],

}

dividend_ingest_params = {
    'header': 0,
    'index_col': False,
    'dtype': {'ex_date': str,
              'amount': float,
              'franking': str,
              'type': str,
              'payable': str,
              },
    'engine': 'c',
    'parse_dates': ['ex_date', 'payable'],
}

cpi_ingest_params = {
    'header': 0,
    'index_col': False,
    'dtype': {'date': str,
              'inflation_rate': float,
              'annual_change': float,
              },
    'engine': 'c',
    'parse_dates': ['date'],

}

tls_df = pd.read_csv(filepath_or_buffer='data/tls.csv', **tls_ingest_params)
cash_rate_df = pd.read_csv(filepath_or_buffer='data/cash_rate.csv', **cash_rate_ingest_params)
dividend_df = pd.read_csv(filepath_or_buffer='data/dividend.csv', **dividend_ingest_params)
cpi_df = pd.read_csv(filepath_or_buffer='data/inflation_rate.csv', **cpi_ingest_params)


def transform_date_rate_as_dict(df, date_column, rate_column):
    """
        Transform date, rate as dictionary from a given df.

        cash_rate: effective_date, cash_rate_target
        dividend: ex_date, amount
        inflation_rate: date, inflation_rate
    """
    date_rate_dict = {row[date_column]: row[rate_column] for _, row in df.iterrows()}

    return date_rate_dict


def get_rate_by_date(date, date_rate_dict):
    """
        If date appears in date_rate_dict, it returns the rate that corresponds to the date; otherwise, it returns
        the rate that corresponds to the closet date (later) appeared in date_list.
    """
    if date in date_rate_dict:
        rate = date_rate_dict[date]
    else:
        closet_date = None
        for key in date_rate_dict:
            if not closet_date:
                if (date - key).days >= 0:
                    closet_date = key
            elif (date - key).days >= 0 and key > closet_date:
                closet_date = key
        rate = date_rate_dict[closet_date]

    return rate


cash_rate_dict = transform_date_rate_as_dict(cash_rate_df, 'effective_date', 'cash_rate_target')
dividend_dict = transform_date_rate_as_dict(dividend_df, 'ex_date', 'amount')
cpi_dict = transform_date_rate_as_dict(cpi_df, 'date', 'inflation_rate')

earliest = dividend_df.iloc[-1]['ex_date']


def get_rates_by_date(row):
    date = row['date']
    if date >= earliest:
        cash_rate = get_rate_by_date(date, cash_rate_dict)
        dividend = get_rate_by_date(date, dividend_dict)
        cpi = get_rate_by_date(date, cpi_dict)
    else:
        cash_rate = 0.0
        dividend = 0.0
        cpi = 0.0

    row['cash_rate'] = cash_rate
    row['dividend'] = dividend
    row['cpi'] = cpi

    return row


enrich_tls_df = tls_df.apply(get_rates_by_date, axis=1)
enrich_tls_df = enrich_tls_df.loc[enrich_tls_df['date'] >= earliest][
    ['close', 'volume', 'cash_rate', 'dividend', 'cpi']]

X = enrich_tls_df[['volume', 'cash_rate', 'dividend', 'cpi']]
Y = enrich_tls_df['close']

reg = linear_model.BayesianRidge()
reg.fit(X, Y)

# predict the share price by giving the other factors.
vol = 28400448
cr = 0.25
div = 0.08
ir = 2.5

x = [vol, cr, div, ir]
y = reg.predict([x])
print(y)
