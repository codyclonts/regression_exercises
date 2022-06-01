import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from env import get_db_url



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

    return df


def wrangle_zillow():
    df= get_zillow_data()
    df = handle_nulls(df)
    df = make_int(df)
    df = handle_outliers(df)
    return df 


