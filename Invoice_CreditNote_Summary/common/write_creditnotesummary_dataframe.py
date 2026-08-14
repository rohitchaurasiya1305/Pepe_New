import pandas as pd
import os
from datetime  import datetime
from config.settings import OUTPUT_CREDITNOTESUMMARY_FOLDER,FAILED_ROWS_CREDITNOTESUMMARY_FOLDER
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def write_df_CreditNoteSummary(df_SuceessCreditNoteSummary,df_FailedCreditNoteSummary):
    
    write_log(f"start Saving ouput file of CreditNoteSUMMARY")
    
    date_str = datetime.now().strftime("%d_%m_%y")
    
    #File Name
    file_name = f"CNS_{date_str}.csv"
    
    #write to csv
    full_path = os.path.join(OUTPUT_CREDITNOTESUMMARY_FOLDER, file_name)
    df_SuceessCreditNoteSummary.to_csv(full_path,index=False)
    
    write_log(f"Saccessfully Saved success rows of CREDITNOTESUMMARY :-{file_name} in folder :- {OUTPUT_CREDITNOTESUMMARY_FOLDER}")
    
    if len(df_FailedCreditNoteSummary)>0:
        file_name = f"CNS_Failed_{date_str}.csv"
        full_path = os.path.join(FAILED_ROWS_CREDITNOTESUMMARY_FOLDER, file_name)
        df_FailedCreditNoteSummary.to_csv(full_path,index=False)
                        
        write_log(f"Saccessfully Saved failed rows of CreditNoteSUMMARY :-{file_name} in folder :- {FAILED_ROWS_CREDITNOTESUMMARY_FOLDER}")
                         
        
    
    