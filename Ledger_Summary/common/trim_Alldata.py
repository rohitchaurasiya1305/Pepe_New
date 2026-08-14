import pandas as pd
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def trim_dataFrame(df):
    
    write_log(f"Input data trimming process has started in the DataFrame.")
    
    #trim Header columns
    df.columns = [str(col).strip() for col in df.columns]
    
    #Trime Values
    df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) else "")
    
    return df