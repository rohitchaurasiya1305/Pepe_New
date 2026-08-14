import pandas as pd
import os
from datetime  import datetime
from config.settings import OUTPUT_CREDITNOTEWORKING_FOLDER,FAILED_ROWS_CREDITNOTEWORKING_FOLDER
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def write_df_CreditNoteWorking(df_SuccessCreditNoteWorking,df_FailedCreditNoteWorking):
    
    write_log(f"start Saving ouput file of CreditNoteWorking")
    
    date_str = datetime.now().strftime("%d_%m_%y")
    
    #File Name
    file_name = f"RTNW_{date_str}.xlsx"
    
    #write to csv
    full_path = os.path.join(OUTPUT_CREDITNOTEWORKING_FOLDER, file_name)
    df_SuccessCreditNoteWorking.to_excel(full_path,index=False)

    write_log(f"Successfully Saved output file of CREDITNOTEWORKING :-{file_name} in folder :- {OUTPUT_CREDITNOTEWORKING_FOLDER}")
    
    if len(df_FailedCreditNoteWorking)>0:
            file_name = f"RTNW_Failed_{date_str}.csv"
            full_path = os.path.join(FAILED_ROWS_CREDITNOTEWORKING_FOLDER, file_name)
            df_FailedCreditNoteWorking.to_csv(full_path,index=False)
                        
            write_log(f"Saccessfully Saved failed rows of CREDITNOTEWORKING :-{file_name} in folder :- {FAILED_ROWS_CREDITNOTEWORKING_FOLDER}")
                         