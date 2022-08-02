import pandas as pd
from env import user, password, host
import acquire_zillow

df = acquire_zillow.get_zillow_data()


def null_dropper(df, prop_required_column, prop_required_row):
    
    prop_null_column = 1 - prop_required_column
    
    for col in list(df.columns):
        
        null_sum = df[col].isna().sum()
        null_pct = null_sum / df.shape[0]
        
        if null_pct > prop_null_column:
            df.drop(columns=col, inplace=True)
            
    row_threshold = int(prop_required_row * df.shape[1])
    
    df.dropna(axis=0, thresh=row_threshold, inplace=True)
    
    return df


def rename_cols(df): #rename columns
    df = df.rename(columns = {'bedroomcnt':'bedroom', 'bathroomcnt':'bathroom', 'calculatedfinishedsquarefeet':'sqft', 'taxvaluedollarcnt':'home_value', 'yearbuilt':'year_built', 'taxamount':'tax_amount', 'poolcnt':'pool'})
    return df


def handle_outliers(df):
    df = df[df.bathroomcnt <= 7]
    
    df = df[df.bedroomcnt <= 7]

    df = df[df.taxvaluedollarcnt < 2_000_000]

    df = df[df.calculatedfinishedsquarefeet < 7000]

    return df


def wrangle_zillow(df):
    df = null_dropper()

    df = handle_outliers(df)

    df = rename_cols(df)

    return df

