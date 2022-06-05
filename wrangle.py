import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from env import get_db_url
from sklearn.model_selection import train_test_split



##### acquire zillow data ######

def get_zillow_data():
    filename = 'zillow_data.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        df = pd.read_sql(
            '''
            SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips  FROM properties_2017 
            JOIN propertylandusetype USING (propertylandusetypeid) 
            WHERE propertylandusedesc = 'Single Family Residential'; 
            '''
            ,
            get_db_url('zillow')
        )

        df.to_csv(filename)

        return df


def handle_nulls(df):
    df = df.dropna()
    return df



def make_int(df):
    df = df.astype({'bedroomcnt':'int', 'calculatedfinishedsquarefeet':'int', 'taxvaluedollarcnt':'int', 'yearbuilt':'int','fips':'int'})
    return df




def handle_outliers(df):
    df = df[df.bathroomcnt <= 6]
    
    df = df[df.bedroomcnt <= 6]

    df = df[df.taxvaluedollarcnt < 2_000_000]

    df = df[df.calculatedfinishedsquarefeet < 100000]

    return df


def split_zillow_data(df):

    train_validate, test = train_test_split(df, test_size=.2, 
        random_state=123)

    train, validate = train_test_split(train_validate, test_size=.3, 
        random_state=123)
    return train, validate, test



def wrangle_zillow():
    df= get_zillow_data()
    df = handle_nulls(df)
    df = make_int(df)
    df = handle_outliers(df)
    df['fips'].replace({6037 : 'LA' , 6059 : 'Orange' , 6111: 'Ventura'}, inplace = True)
    return df 


