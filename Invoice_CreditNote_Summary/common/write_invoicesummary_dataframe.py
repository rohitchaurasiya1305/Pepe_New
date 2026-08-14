import pandas as pd
import os
from datetime  import datetime
from config.settings import OUTPUT_INVOICESUMMARY_FOLDER,FAILED_ROWS_INVOICESUMMARY_FOLDER
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def write_df_InvoiceSummary(df_SuccessInvoiceSummary,df_FailedInvoiceSummary):
    
    write_log(f"start Saving ouput file of INVOICESUMMARY")
    
    date_str = datetime.now().strftime("%d_%m_%y")
    
    #File Name
    file_name = f"CIS_{date_str}.csv"
    
    #write to csv
    
    full_path = os.path.join(OUTPUT_INVOICESUMMARY_FOLDER, file_name)
    df_SuccessInvoiceSummary.to_csv(full_path,index=False)
                
    write_log(f"Saccessfully Saved Success rows of INVOICESUMMARY :-{file_name} in folder :- {OUTPUT_INVOICESUMMARY_FOLDER}")
               
    if len(df_FailedInvoiceSummary)>0:
        file_name = f"CIS_Failed_{date_str}.csv"
        full_path = os.path.join(FAILED_ROWS_INVOICESUMMARY_FOLDER, file_name)
        df_FailedInvoiceSummary.to_csv(full_path,index=False)
                    
        write_log(f"Saccessfully Saved failed rows of INVOICESUMMARY :-{file_name} in folder :- {FAILED_ROWS_INVOICESUMMARY_FOLDER}")
                     
    
    
        
    
    