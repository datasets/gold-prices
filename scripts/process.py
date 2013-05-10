import os
import urllib
import logging
import csv

downloaded = 'cache/bbk_WU5500.csv'
outpath = 'data/data.csv'

def download():
    if not os.path.exists('cache'):
        os.makedirs('cache')
    url = 'http://www.bundesbank.de/statistik/statistik_zeitreihen_download.en.php?func=directcsv&from=&until=&filename=bbk_WU5500&csvformat=en&euro=mixed&tr=WU5500'
    urllib.urlretrieve(url, downloaded)

def extract():
    reader = csv.reader(open(downloaded))
    newrows = [ row for row in reader ]
    # skip top 5 rows
    newrows = newrows[5:]
    # trim the notes from the bottom
    newrows = newrows[:-1]
    # fix up the data
    # dates are 1968-06 without day ...
    newrows = [ [row[0] + '-01', row[1]] for row in newrows ]

    existing = []
    if os.path.exists(outpath):
        fo = open(outpath)
        existing = [ row for row in csv.reader(fo) ]
        fo.close()
    
    starter = newrows[0]
    for idx,row in enumerate(existing):
        if row[0] == starter[0]:
            # remove all rows from here on
            del existing[idx:]
            break
    # and now add in new data
    outrows = existing + newrows
    fo = open(outpath, 'w')
    writer = csv.writer(fo)
    writer.writerows(outrows)
    fo.close()

def upload():
    import datastore.client as c
    dsurl = 'http://datahub.io/dataset/gold-prices/resource/b9aae52b-b082-4159-b46f-7bb9c158d013'
    client = c.DataStoreClient(dsurl)
    client.delete()
    client.upload(outpath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print 'Downloading'
    # download()
    print 'Extracting and merging'
    extract()
    print 'Uploading'
    upload()
    
