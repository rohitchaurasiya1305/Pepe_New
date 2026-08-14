import os
import sys
import pandas as pd
from pathlib import Path
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def read_input_file(filePath):
    try:
        write_log(f"File reading process started.")
        
        file_Path = Path(filePath)
        
        extension = str(file_Path.suffix.lower())
        
        write_log(f"Input file extension is {extension}.")
        
        if extension == ".xlsx":
            return pd.read_excel(filePath,dtype=str)
        
        elif extension == ".xls":
            return pd.read_excel(filePath,dtype=str)
        
        elif extension == ".csv":
            return pd.read_csv(filePath,dtype=str)
        
        else:
            return None
        
    except Exception as e:
        write_log(f"Failed to read the file:-  {filePath}   exception:-  {e}")
        return None   