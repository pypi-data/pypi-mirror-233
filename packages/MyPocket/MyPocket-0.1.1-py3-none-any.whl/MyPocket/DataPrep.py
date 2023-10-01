import pandas as pd
import pickle

def getDfRange(df: "pd.DataFrame")->"(float,float)":
    '''Get the range of a dataframe
    Input:
        df: pd.DataFrame
    Output:
        min,max: float, min and max value of the dataframe'''
    return df.min().min(),df.max().max()


def pickle_save(obj,filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
    # print("Data saved")

def pickle_load(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj