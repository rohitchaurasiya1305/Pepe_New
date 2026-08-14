import os
import pandas as pd
from datetime  import datetime
from config.settings import OUTPUT_LEDGERSUMMARY_FOLDER,FAILED_ROWS_LEDGERSUMMARY_FOLDER
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def write_df_LedgerSumaary(df_SuccessLedgerSummary,df_FailedLedgerSummary):
    
    write_log(f"start Saving ouput file of LEDGERSUMMARY")
    
    date_str = datetime.now().strftime("%d_%m_%y")
    
    #File Name
    file_name = f"LS_{date_str}.csv"
    
    #write to csv
    full_path = os.path.join(OUTPUT_LEDGERSUMMARY_FOLDER, file_name)
    df_SuccessLedgerSummary.to_csv(full_path,index=False)
    
    write_log(f"Saccessfully Saved ouput file of LEDGERSUMMARY :-{file_name} in folder :- {OUTPUT_LEDGERSUMMARY_FOLDER}")
    
    if len(df_FailedLedgerSummary)>0:
        file_name = f"LS_Failed_{date_str}.csv"
        full_path = os.path.join(FAILED_ROWS_LEDGERSUMMARY_FOLDER, file_name)
        df_FailedLedgerSummary.to_csv(full_path,index=False)
                    
        write_log(f"Saccessfully Saved failed rows of LEDGERSUMMARY :-{file_name} in folder :- {FAILED_ROWS_LEDGERSUMMARY_FOLDER}")
                     
    
    
        