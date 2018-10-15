from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, dump_to_path, load, set_type, printer
import os
import urllib.request
import logging
import csv

downloaded = 'cache/bbk_WU5500.csv'
source_url = 'http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its'


def download_csv_resource():
    source_url = 'http://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.XAU.USD.EA.AC.C06&its_csvFormat=en&its_fileFormat=csv&mode=its'
    downloaded_csv_filepath = 'cache/bbk_WU5500.csv'
    if not os.path.exists('cache'):
        os.makedirs('cache')
    urllib.request.urlretrieve(source_url, downloaded_csv_filepath)


def rename(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 'gold-prices-monthly'
    package.pkg.descriptor['resources'][0]['path'] = 'data/monthly.csv'
    package.pkg.descriptor['resources'][1]['name'] = 'gold-prices-annual'
    package.pkg.descriptor['resources'][1]['path'] = 'data/annual.csv'
    yield package.pkg
    res_iter = iter(package)
    for res in res_iter:
        yield res.it
    yield from package


def fix_rows(rows):
    # We skip top 5 rows and trim notes from the bottom. Also as dates are without day specified
    # we are taking the first day in month by default
    newrows = [[row[0], row[1]] for row in rows[5:-1]]
    return newrows


def extract_gold_prices(frequency):
    reader = csv.reader(open(downloaded))
    rows = [row for row in reader]
    fixed_rows = fix_rows(rows)
    for row in fixed_rows:
        if frequency == 'monthly':
            yield {'Date': row[0], 'Price': row[1]}
        elif frequency == 'annual':
            if row[0].split('-')[1] == '01':
                yield {'Date': row[0], 'Price': row[1]}


download_csv_resource()
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
        version="0.2.0"
    ),
    extract_gold_prices('monthly'),
    extract_gold_prices('annual'),
    set_type('Date', type='yearmonth', format='any'),
    set_type('Price', type='number', format='any'),
    rename,
    validate(),
    dump_to_path(),
)
gold_price_flow.process()
