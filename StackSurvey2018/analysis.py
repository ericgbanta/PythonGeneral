"""
IMPORTING & CLEANING

"""

# %% Import libraries and packages
import pandas as pd
import numpy as np
from numpy import array
from pandas import Series

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
color = sns.color_palette()

# Supress unnecessary warnings so that presentation looks clean
import warnings
warnings.filterwarnings('ignore')

# Print all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# %% Block 1 - Import stack & schema data and print shape
data = pd.read_csv(r'C:\Users\eric.banta\Documents\Python Scripts\Data Science\Stack Overflow Developer Survey 2018\survey_results_public.csv')
schema = pd.read_csv(r'C:\Users\eric.banta\Documents\Python Scripts\Data Science\Stack Overflow Developer Survey 2018\survey_results_schema.csv')

print('Size of data:', data.shape)


# %% Block 2 - Print first 5 columns of data
data.head()


# %% Block 3 - Print all columns and their descriptions
pd.options.display.max_colwidth = 300
schema

# %% Block 4 - Checking for missing data - print percentages of missing
total = data.isnull().sum().sort_values(ascending=False)
percent = (data.isnull().sum() / data.isnull().count() * 100).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data

'''
EXPLORATORY DATA ANALYSIS

'''

# %% Block 1 - Hobby Developers vs Other
prep = data['Hobby'].value_counts()
df = pd.DataFrame({'labels': prep.index,
                   'values': prep.values
                   })
# Donut Chart
my_circle = plt.Circle((0, 0), 0.5, color='white')
plt.pie(df['values'], labels=None, autopct='%.1f%%', pctdistance=0.8, colors=['skyblue', 'salmon'])
plt.legend(labels=df['labels'], loc='best')
p = plt.gcf()
p.gca().add_artist(my_circle)
p.gca().set_title('% of Developers Who Code as a Hobby')
plt.show()


# %% Block 2 - Devs that contribute to open source projects
prep = data['OpenSource'].value_counts()
df = pd.DataFrame({'labels': prep.index,
                   'values': prep.values
                   })
# Donut Chart
my_circle = plt.Circle((0, 0), 0.5, color='white')
plt.pie(df['values'], labels=None, autopct='%.1f%%', pctdistance=0.8, colors=['skyblue', 'salmon'])
plt.legend(labels=df['labels'], loc='best')
p = plt.gcf()
p.gca().add_artist(my_circle)
p.gca().set_title('% of Devs Who Contribute to Open Source')
plt.show()


# %% Block 3 - Devs that are students
prep = data['Student'].value_counts()
df = pd.DataFrame({'labels': prep.index,
                   'values': prep.values
                   })
# Donut Chart
my_circle = plt.Circle((0, 0), 0.7, color='white')
plt.pie(df['values'], labels=None, autopct='%.1f%%', pctdistance=0.85, colors=['skyblue', 'salmon', 'lightgreen'])
plt.legend(labels=df['labels'], loc='best')
p = plt.gcf()
p.gca().add_artist(my_circle)
p.set_size_inches(7, 7)
p.gca().set_title('% of Devs Who are Students')
plt.show()


# %% Block 4 - Employment Status of Devs
prep = data['Employment'].value_counts()
df = pd.DataFrame({'labels': prep.index,
                   'values': prep.values
                   })
# Donut Chart
my_circle = plt.Circle((0, 0), 0.7, color='white')
plt.pie(df['values'], labels=None, autopct='%.1f%%', pctdistance=0.85,
        colors=['skyblue', 'salmon', 'lightgreen', 'plum', 'lightgrey', 'tan'])
plt.legend(labels=df['labels'], loc='best')
p = plt.gcf()
p.gca().add_artist(my_circle)
p.set_size_inches(15, 15)
p.gca().set_title('Employment Status of Devs')
plt.show()
