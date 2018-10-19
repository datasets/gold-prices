import os

from dataflows import Flow, PackageWrapper, validate, delete_fields
from dataflows import add_metadata, load, set_type, update_resource


def readme(fpath='README.md'):
    if os.path.exists(fpath):
        return open(fpath).read()


def extract_december_rows(rows):
    for row in rows:
        if '-12' in row['Date']:
            yield row


gold_price_flow = Flow(
    add_metadata(
        name="gold-prices",
        title="Gold Prices",
        homepage='http://www.bundesbank.de',
        licenses=[
            {
                "id": "odc-pddl",
                "name": "public_domain_dedication_and_license",
                "version": "1.0",
                "url": "http://opendatacommons.org/licenses/pddl/1.0/"
            }
        ],
        sources=[
            {
              "name": "bundesbank-gold-prices",
              "path": "'http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its'",
              "title": "Bundesbank gold prices"
            }
        ],
        views=[
            {
                "name": "graph",
                "title": "Gold Prices (Monthly in USD)",
                "specType": "simple",
                "spec": {
                    "type": "lines-and-points",
                    "group": "Date",
                    "series": [
                        "Price"
                    ]
                }
            }
        ],
        related=[
            {
                "title": "Oil prices",
                "path": "/core/oil-prices",
                "publisher": "core",
                "formats": ["CSV", "JSON"]
            },
            {
                "title": "Natural gas",
                "path": "/core/natural-gas",
                "publisher": "core",
                "formats": ["CSV", "JSON"]
            }
        ],
        version="0.2.0"
    ),
    load(
        load_source='http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its',
        skip_rows=[1, 2, 3, 4, 5, -1],
        headers=['Date', 'Price', 'Empty column'],
        format='csv',
        name='annual'
    ),
    extract_december_rows,
    load(
        load_source='http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its',
        skip_rows=[1, 2, 3, 4, 5, -1],
        headers=['Date', 'Price', 'Empty column'],
        format='csv',
        name='monthly'
    ),
    update_resource('monthly', **{'path':'data/monthly.csv', 'dpp:streaming': True}),
    update_resource('annual', **{'path':'data/annual.csv', 'dpp:streaming': True}),
    set_type('Date', resources='annual', type='yearmonth'),
    set_type('Price', resources='annual', type='number'),
    set_type('Date', resources='monthly', type='yearmonth'),
    set_type('Price', resources='monthly', type='number'),
    validate(),
    delete_fields(['Empty column'], resources=None)
)


def flow(parameters, datapackage, resources, stats):
    return gold_price_flow


if __name__ == '__main__':
    gold_price_flow.process()
