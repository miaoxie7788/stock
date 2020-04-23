"""
    Extract IMF data by country.

    https://www.imf.org/external/datamapper/datasets/WEO
"""

import pandas as pd


def extract_imf(imf_data_filename, country="Australia"):
    df = pd.read_csv(filepath_or_buffer=imf_data_filename, encoding="ISO-8859-1", index_col=0)
    data = df.loc[country]

    return data


def main():
    imf_cpi = "data/imf/imf-inflation-20200422.csv"
    imf_gdp = "data/imf/imf-gdp-20200422.csv"
    imf_unemployment = "data/imf/imf-people-20200422.csv"
    imf_current = "data/imf/imf-current account-20200422.csv"
    imf_government = "data/imf/imf-government finance-20200422.csv"

    aus_cpi = extract_imf(imf_cpi)
    aus_gdp = extract_imf(imf_gdp)
    aus_unemployment = extract_imf(imf_unemployment)
    aus_current = extract_imf(imf_current)
    aus_government = extract_imf(imf_government)

    print(aus_government)


if __name__ == "__main__":
    # execute only if run as a script
    main()
