import pandas as pd

def write_tsCSO(df,filename):
    """
    Write time series data from CSOs (water level, conductivity) to a file in a specific format.

    Parameters:
    - data (DataFrame): A DataFrame containing time series data with two columns.
                       the first column should contain the timestamps, and the second contains the data values.
    - filename (str): The name of the file to which the time series data will be written.

    The function converts the provided DataFrame into a specific time series format and writes it to a file with the two columns 'time' and 'value'.

    Returns:
    None. The function writes the data to the specified file but does not return any values.
    """
    
    # Modify dataframe
    df.columns = ['time','value']
    df.time = pd.to_datetime(df.time,format='%Y-%m-%d %H:%M:%S')
    df.value = df.value.astype('float')
    df.reset_index(inplace=True,drop=True)    
    
    # Write out dataframe
    df.to_csv(filename,header=["time","value"],index=None,sep='\t')