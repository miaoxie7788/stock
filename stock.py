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
from joblib import dump, load
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVR


def ingest_func_imf_qi(df):
    qi = df.loc["Australia"]
    qi.index = pd.to_datetime(qi.index)
    qi = pd.to_numeric(qi, errors='coerce', downcast='float').dropna()

    return qi


def ingest_func_cash_rate(df):
    qi = df["cash_rate_target"]

    return qi


def ingest_func_div(df):
    qi = df["dividend"]
    # Deal with duplicated dates.
    qi = qi.groupby(qi.index).agg(sum)

    return qi


def construct_qis_ingest_dict(asx_code):
    constant_qi_path = "data/constant"
    variable_qi_path = "data/{asx_code}".format(asx_code=asx_code)

    # constant qi: imf qis (acc, cpi, fin, gdp, ppl), cash rate
    imf_qi_ingest_params = {
        'header': 0,
        'index_col': 0,
        'encoding': 'ISO-8859-1',
    }

    cash_rate_ingest_params = {
        'header': 0,
        'index_col': 'effective_date',
        'parse_dates': ['effective_date'],
    }

    # variable qi: div
    div_ingest_params = {
        'header': 0,
        'index_col': 'ex_dividend_date',
        'parse_dates': ['ex_dividend_date', 'payment_date'],
    }

    imf_qi_names = ['acc', 'cpi', 'fin', 'gdp', 'ppl']

    qis_ingest_dict = dict()
    for qi_name in imf_qi_names:
        qis_ingest_dict[qi_name] = {
            'filename': "{path}/{name}.csv".format(path=constant_qi_path, name=qi_name),
            'ingest_params': imf_qi_ingest_params,
            'ingest_func': ingest_func_imf_qi,
        }

    qi_name = 'cash_rate'
    qis_ingest_dict[qi_name] = {
        'filename': "{path}/{name}.csv".format(path=constant_qi_path, name=qi_name),
        'ingest_params': cash_rate_ingest_params,
        'ingest_func': ingest_func_cash_rate,
    }

    qi_name = 'div'
    qis_ingest_dict[qi_name] = {
        'filename': "{path}/{name}.csv".format(path=variable_qi_path, name=qi_name),
        'ingest_params': div_ingest_params,
        'ingest_func': ingest_func_div,
    }

    return qis_ingest_dict


def ingest_qis(qis_ingest_dict):
    qis_dict = dict()
    for key, val in qis_ingest_dict.items():
        df = pd.read_csv(filepath_or_buffer=val['filename'], **val['ingest_params'])
        qi = val['ingest_func'](df)
        qis_dict[key] = qi

    return qis_dict


def ingest_share(asx_code):
    share_path = "data/{asx_code}".format(asx_code=asx_code)
    share_ingest_params = {
        'header': 0,
        'parse_dates': ['date'],
    }

    filename = "{path}/{name}.csv".format(path=share_path, name=asx_code)
    df = pd.read_csv(filepath_or_buffer=filename, **share_ingest_params)
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


def extract_qis(row, qis):
    date = row.date
    for qi_name, qi in qis.items():
        row[qi_name] = extract_qi(date, qi)

    return row


def save_features(asx_code, df):
    share_path = "data/{asx_code}".format(asx_code=asx_code)

    filename = "{path}/{name}.csv".format(path=share_path, name='features')
    df.to_csv(filename, index=False)


def load_features(asx_code):
    share_path = "data/{asx_code}".format(asx_code=asx_code)

    filename = "{path}/features.csv".format(path=share_path)
    df = pd.read_csv(filepath_or_buffer=filename)

    return df


def extract_features(asx_code):
    # Construct ingest_dict for QIs.
    qis_ingest_dict = construct_qis_ingest_dict(asx_code=asx_code)

    # Ingest QIs.
    qis = ingest_qis(qis_ingest_dict)

    # Ingest share.
    share = ingest_share(asx_code)

    collated_share = share.apply(lambda row: extract_qis(row, qis), axis=1)
    save_features(asx_code=asx_code, df=collated_share)

    return collated_share


def select_features(asx_code, target_col='close', n_iter=100, n_fold=3):
    """
        Select QIs (features) that influence the share's price most significantly.
    """

    df = load_features(asx_code=asx_code)
    print(df)
    qi_names = list(set(df.columns) - {'date', target_col})

    X = df[qi_names]
    y = df[target_col]

    svr = LinearSVR(max_iter=n_iter)

    # RFECV
    # selector = RFECV(estimator=svr, cv=n_fold)
    # selector.fit(X, y)
    #
    # selected_qi_names = np.array(qi_names)[selector.support_]
    # print("The most significant QIs are:", list(selected_qi_names))
    # return selected_qi_names

    # SelectFromModel
    model = SelectFromModel(svr, prefit=True)


def select_parameters(asx_code, feature_cols, target_col='close'):
    df = load_features(asx_code=asx_code)

    X = df[feature_cols]
    y = df[target_col]

    param_grid = {
        'epsilon': [0.0, 0.1, 0.2],
        'C': [0.1, 1, 2],
        'max_iter': [10000],
    }

    svr = LinearSVR()
    grid_search_cv = GridSearchCV(svr, param_grid=param_grid, n_jobs=-1, cv=5)
    grid_search_cv.fit(X, y)
    return grid_search_cv.best_estimator_


def fit(asx_code, estimator, feature_cols, target_col='close'):
    input_filename = make_extracted_filename(asx_code=asx_code)
    df = pd.read_csv(input_filename)

    X = df[feature_cols]
    y = df[target_col]

    estimator.set_params(max_iter=10000)
    estimator.fit(X, y)

    output_filename = make_fitted_filename(asx_code=asx_code)
    dump(estimator, output_filename)
    return estimator


def predict(asx_code):
    filename = make_fitted_filename(asx_code=asx_code)
    fitted_svr = load(filename)
    print(fitted_svr)
    vol = 32929415
    cpi = 2.2
    gdp = 1.2
    ppl = 8.5
    acc = -3
    fin = -2.5
    cash = 0.25
    div = 8

    x = [vol, gdp, ppl, cash, div]
    input_filename = make_extracted_filename(asx_code=asx_code)
    df = pd.read_csv(input_filename)

    X = df[['volume', 'gdp', 'ppl', 'cash', 'div']]
    y = fitted_svr.predict(X)
    print(y)


def main(asx_code):
    # --------------------------------------------------------------------------------------------------
    # 1 feature engineering
    # --------------------------------------------------------------------------------------------------
    # 1.1 feature extraction
    # feature_extraction(asx_code=asx_code)

    # 1.2 feature selection
    select_features(asx_code=asx_code)
    selected_qi_names = ['volume', 'gdp', 'ppl', 'cash', 'div']
    # --------------------------------------------------------------------------------------------------
    # 2 fit
    # --------------------------------------------------------------------------------------------------
    # 2.1 parameter selection
    # svr = parameter_selection(asx_code=asx_code, feature_cols=selected_qi_names)
    # print(svr)

    # 2.2 fit with best estimator
    # fitted_svr = fit(asx_code=asx_code, estimator=svr, feature_cols=selected_qi_names)

    # --------------------------------------------------------------------------------------------------
    # 3 apply / predict
    # --------------------------------------------------------------------------------------------------
    # predict(asx_code=asx_code)


if __name__ == "__main__":
    # execute only if run as a script
    main('tls')
