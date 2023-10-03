import numpy as np
import pandas as pd


def convert_MeteoSwiss(df):
    
    """
    Parameters
    ----------
    df : DataFrame containting 3 columns: stn; time; rre150z0
        Raw MeteoSwiss rainfall data

    Returns
    -------
    df : DataFrame with 2 columns: "time" (timestamps) and "value" (numeric values)
        Formatted rainfall data

    """
    
    df.drop(df.columns[[0]],axis=1,inplace=True)
    df.replace('-',np.nan,inplace=True)
    df.dropna(inplace=True)
    df.columns = ['time','value']
    df.time = pd.to_datetime(df.time,format='%Y%m%d%H%M')
    df.value = df.value.astype('float')
    df.reset_index(inplace=True,drop=True)
    
    return df