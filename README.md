<a className="gh-badge" href="https://datahub.io/core/gold-prices"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Monthly gold prices in USD since 1833. Historical data (1833–1959) is sourced from records compiled by Timothy Green; data from 1960 to the present is sourced from the World Bank Commodity Markets ("Pink Sheet").

## Data

* [World Bank Commodity Markets](https://www.worldbank.org/en/research/commodity-markets)

## Preparation

You will need Python 3.11 or greater to run the script.

To update the data run the process script locally:

```
# Install requirements
pip install -r scripts/requirements.txt
python scripts/process.py
```

### Notes from the Sources

* Currently data has been sourced using multiple datasets:
  - **Historical data (1833–1959):** Timothy Green's Historical Gold Price Table, originally hosted at the National Mining Association. Note: as of 2026 this PDF requires a login to download; the update script handles this gracefully by skipping the PDF merge if the file is unavailable. Because only annual figures exist for this period, the monthly and monthly-processed files repeat the annual average price for every month of the year (i.e. all 12 months in 1890 carry the same value).
  - **Modern data (1960–present):** [World Bank Commodity Markets](https://www.worldbank.org/en/research/commodity-markets), which is regularly updated and provides comprehensive, up-to-date data on a wide range of commodity prices.


## Automation

This dataset is automatically updated daily via GitHub Actions. View the dataset on DataHub: https://datahub.io/core/gold-prices

## License

The maintainers have licensed this dataset under the Public Domain Dedication and License. The World Bank data is freely available with no obvious restrictions; the Timothy Green historical records similarly carry no known restrictions.
