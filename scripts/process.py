from dataflows import Flow, PackageWrapper, validate, delete_fields
from dataflows import add_metadata, dump_to_path, load, set_type, printer


def extract_december_rows(rows):
    for row in rows:
        if '-12' in row['Date']:
            yield row


def rename(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 'gold-prices-annual'
    package.pkg.descriptor['resources'][0]['path'] = 'data/annual.csv'
    package.pkg.descriptor['resources'][1]['name'] = 'gold-prices-monthly'
    package.pkg.descriptor['resources'][1]['path'] = 'data/monthly.csv'
    yield package.pkg
    res_iter = iter(package)
    for res in res_iter:
        yield res.it
    yield from package


# download_csv_resource()
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
        headers=['Date', 'Price', 'Empty column']
    ),
    extract_december_rows,
    load(
        load_source='http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its',
        skip_rows=[1, 2, 3, 4, 5, -1],
        headers=['Date', 'Price', 'Empty column']
    ),
    rename,
    set_type('Date', resources='gold-prices-annual', type='yearmonth', format='any'),
    set_type('Price', resources='gold-prices-annual', type='number', format='any'),
    set_type('Date', resources='gold-prices-monthly', type='yearmonth', format='any'),
    set_type('Price', resources='gold-prices-monthly', type='number', format='any'),
    validate(),
    delete_fields(['Empty column'], resources=None),
    dump_to_path(),
)
gold_price_flow.process()
