import os
import requests
import pdfplumber
import pandas as pd

from bs4 import BeautifulSoup
from operator import itemgetter

data = 'data/'
cache = 'cache/'
source = 'https://www.worldbank.org/en/research/commodity-markets'
source_pdf = 'https://nma.org/wp-content/uploads/2016/09/historic_gold_prices_1833_pres.pdf'
pdf_file_name = 'historical_gold_prices.pdf'

def month_divider(year):
    for i in range(1, 13):
        yield f"{year}-{i:02d}"

def download_pdf():
    response = requests.get(source_pdf)
    with open(f'{cache}{pdf_file_name}', 'wb') as file:
        file.write(response.content)

def get_hrefs():
    response = requests.get(source)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    monthly = ''
    annual = ''
    for link in links:
        if 'monthly prices' in link.text.lower():
            monthly = link.get('href')
        if 'annual prices' in link.text.lower():
            annual = link.get('href')
    return monthly, annual

def download_xls():
    monthly, annual = get_hrefs()
    response_monthly = requests.get(monthly)
    response_annual = requests.get(annual)
    if os.path.exists(cache) == False:
        os.mkdir(cache)
    with open(cache + 'monthly.xls', 'wb') as file:
        file.write(response_monthly.content)
    with open(cache + 'annual.xls', 'wb') as file:
        file.write(response_annual.content)

def modify_and_create(name_file, symbol, sheetname,index_to_drop,drop_row):
    dfs = pd.read_excel(f"{cache}{name_file}.xls", sheet_name=sheetname)
    dfs = dfs.iloc[drop_row:]
    dfs.reset_index(drop=True, inplace=True)
    dfs.drop(index=index_to_drop, inplace=True)
    header = dfs.iloc[0]
    dfs = dfs[1:]
    dfs.columns = header
    dfs.rename(columns={ dfs.columns[0]: "Date" }, inplace = True)
    df = dfs.filter(['Date', 'Gold'])
    df.reset_index(drop=True, inplace=True)
    if symbol in str(df.Date[0]):
        df.Date = df.Date.str.replace(symbol, '-')
    df.Gold = df.Gold.astype(float)
    df.to_csv(f"{data}{name_file}.csv", index=False)

def pdf_historical(name_file):
    with pdfplumber.open(f"{cache}{name_file}") as pdf:
        # Access the first page
        page = pdf.pages[0]
        
        # Extract text if needed
        text = page.extract_text()
        
        # Extract table data
        tables = page.extract_tables()
        get_vals = []
        # Parse the table until 1960 data since, we already have that data from annual and monthly
        parsed = False
        for table in tables:
            if parsed:
                break
            for row in table:
                if 'Year' in row[0]:
                    continue
                if '1960' in str(row[0]):
                    parsed = True
                    break
                get_vals.append(row)

    return get_vals

def process_and_merge_pdf():
    values = pdf_historical(pdf_file_name)
    # Get the first value and price
    first_value = values[0][0]
    price = values[0][1]

    years_range = first_value.split('-')

    values = values[1:]

    # Get the start and end year
    start_year = int(years_range[0])
    end_year = int("18" + years_range[1].replace('*', ''))

    # Generate a list of lists for each year in the range
    expanded_list = [[str(year), price] for year in range(start_year, end_year + 1)]
    values = expanded_list + values
    sorted(values,key=itemgetter(0))
    monthly_values = []
    for elem in values:
        for month in month_divider(elem[0]):
            monthly_values.append([month, elem[1]])

    with open(f"{data}annual.csv", 'a') as file:
        for value in values:
            file.write(f"{value[0]},{value[1]}\n")
    
    with open(f"{data}monthly.csv", 'a') as file:
        for value in monthly_values:
            file.write(f"{value[0]},{value[1]}\n")
    
    sort_annual = pd.read_csv(f"{data}annual.csv")
    sort_annual.sort_values(by=['Date'], inplace=True)
    sort_annual.drop_duplicates(subset=['Date'], inplace=True)
    sort_annual.Gold = sort_annual.Gold.apply(lambda x: '{0:.3f}'.format(x))
    sort_annual.to_csv(f"{data}annual.csv", index=False)

    sort_monthly = pd.read_csv(f"{data}monthly.csv")
    sort_monthly.sort_values(by=['Date'], inplace=True)
    sort_monthly.drop_duplicates(subset=['Date'], inplace=True)
    sort_monthly.Gold = sort_monthly.Gold.apply(lambda x: '{0:.3f}'.format(x))
    sort_monthly.to_csv(f"{data}monthly.csv", index=False)

def process():
    print('Processing...')
    download_xls()

    print('Downloaded XLS files')
    download_pdf()
    
    print('Process XLS files (annual/monthly) and transform them into csvs')
    modify_and_create('monthly','M','Monthly Prices',[1],3)
    modify_and_create('annual','A','Annual Prices (Nominal)',[1,2],5)

    print('Downloaded PDF file and process it into csv and merge with the main source')
    process_and_merge_pdf()
    
    print('Done!')

if __name__ == '__main__':
    process()


    