import pyodbc
import pandas as pd
import requests
from selenium import webdriver
import numpy as np
import datetime
from string import ascii_uppercase
from lxml import html
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# %% BLOCK 0.1 - See website - OPTIONAL %% #
url = 'https://www.payscale.com/index/CA/Job/'
driver = webdriver.Chrome(
    executable_path=r'C:\Users\eric.banta\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(url)


# %% Block 1 - Connect and run query
cnxn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=ERICLOCAL;'
                      'DATABASE=Payscale;'
                      'trusted_connection=yes;')


# %% BLOCK 2 - Scrape Tables for titles %% #
# Create 'Emoty DataFrame'
todays_date = datetime.datetime.now().date()
index = pd.date_range(todays_date - datetime.timedelta(10), periods=10, freq='D')
columns = ['A']

finalDF = []
finalDF = pd.DataFrame(index=index, columns=columns)

# Loop through all webpages and append job titles to dataframe
for letter in ascii_uppercase:
    df = []
    page = requests.get('https://www.payscale.com/index/CA/Job/' + letter)
    table = pd.read_html(page.text, header=0)
    # Create DataFrame from List
    df = pd.DataFrame(table[0])
    finalDF = finalDF.append(df)

# clean DataFrame
finalDF = finalDF.dropna(how='all')
finalDF = finalDF.drop('A', 1)
finalDF = finalDF.reset_index()
finalDF = finalDF.drop('index', 1)
finalDF

# rename and reorder columns
cols = finalDF.columns.tolist()
cols = cols[-1:] + cols[:-1]
finalDF = finalDF[cols]
finalDF


# %% BLOCK 3 - For each title, pull the link associated with each %% #
url = 'https://www.payscale.com'
urls = []

for letter in ascii_uppercase:
    page = requests.get('https://www.payscale.com/index/CA/Job/' + letter)
    tree = html.fromstring(page.text)
    links = tree.xpath('//tr/td/a/@href')
    urls = urls + links

urls = [url + link for link in urls]

print(urls)
print(len(urls))


# %% BLOCK 4 - Append urls to dataframe and add datetime column %% #
urlArray = np.asarray(urls)
data = finalDF.copy()
data['URLS'] = urlArray
data['Updated Date'] = pd.to_datetime('today')
data['PayscaleId'] = range(1, 1 + len(data))
cols = data.columns.tolist()
cols = cols[-1:] + cols[:-1]
data = data[cols]
data


# %% BLOCK 5 - Dataframe to SQL
cursor = cnxn.cursor()

# delete table data
cursor.execute('TRUNCATE TABLE eric.payscaletest')


# insert new table data
qry = '''INSERT INTO eric.payscaletest([PayscaleId], [Popular Jobs], [Number of Data Profiles], [URL], [Updated Date]) values (?, ?, ?, ?, ?)'''

for index, row in data.iterrows():
    cursor.execute(qry, *row)
    cnxn.commit()

cursor.close()
cnxn.close()
