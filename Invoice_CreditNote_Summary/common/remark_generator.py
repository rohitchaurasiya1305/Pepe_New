import pandas as pd
from datetime import datetime

def is_invalid(value):
    
    return (pd.isna(value) 
      or str(value).strip() == "" 
      or str(value).strip().lower() in ["nan", "none", "null", "na", "n/a", "undefined"])
    
def is_integer(value):
    
    try:
        
        return float(value)
    
    except ValueError:
        return False
    


def is_datetimeformat(str_date_month):
    
    format=['%d-%m-%Y','%Y-%m-%d','%Y/%m/%d','%d-%b-%Y','%Y%m','%Y-%m']
    str_date_month= str_date_month.split(" ")[0]
    
    for fmt in format:
        try:
            
            dt= datetime.strptime(str_date_month,fmt)
            return dt.strftime('%Y%m')
        
        except ValueError:
            continue
        
    return False