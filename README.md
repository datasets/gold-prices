Monthly gold prices in USD since 1833 (sourced from the World Gold Council). The data is derived from historical records compiled by Timothy Green and supplemented by data provided by the World Bank.

## Data

* [Worldbank-Commodity-Market](https://www.worldbank.org/en/research/commodity-markets)

## Preparation

You will need Python 3.6 or greater and dataflows library to run the script

To update the data run the process script locally:

```
# Install requirements
pip install -r scripts/requirements.txt
python scripts/process.py
```

### Notes from the Sources

* Currently data has been sourced using multiple datasets, 
  - This one is presented by Timothy Green Historical Gold Price Table the description is available [historical-data-1883](https://nma.org/wp-content/uploads/2016/09/historic_gold_prices_1833_pres.pdf) and the data used up until 1960 year.
  - The second dataset was obtained from the [Worldbank-Commodity-Market](https://www.worldbank.org/en/research/commodity-markets), which is regularly updated and provides comprehensive, up-to-date data on a wide range of commodity prices. This dataset includes historical data dating back to 1960, extending up to the present day.


## Automation

This dataset is automatically updates every month on the datahub.io site: http://datahub.io/core/gold-prices

## License

The maintainers have licensed under the Public Domain Dedication and License. The source at the Bundesbank indicates no obvious restrictions on the data and the amount means that database rights are doubtful.
