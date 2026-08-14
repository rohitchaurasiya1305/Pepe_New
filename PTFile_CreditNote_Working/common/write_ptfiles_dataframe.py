import pandas as pd
import os
from datetime  import datetime
from config.settings import OUTPUT_PTFILE_FOLDER,FAILED_ROWS_PTFILE_FOLDER
from common.logger import write_log
pd.set_option('future.no_silent_downcasting', True)

def write_df_PTFiles(df_SuccessPTFiles,df_FailedPTFiles):
    
    write_log(f"start Saving ouput file of PTFILES")
    
    date_str = datetime.now().strftime("%d_%m_%y")
    
    #File Name
    file_name = f"PT_{date_str}.csv"
    
    #write to csv
    full_path = os.path.join(OUTPUT_PTFILE_FOLDER, file_name)
    df_SuccessPTFiles.to_csv(full_path,index=False)
    
    write_log(f"Successfully Saved output file of PTFILES :-{file_name} in folder :- {OUTPUT_PTFILE_FOLDER}")
    
    if len(df_FailedPTFiles)>0:
        file_name = f"PT_Failed_{date_str}.csv"
        full_path = os.path.join(FAILED_ROWS_PTFILE_FOLDER, file_name)
        df_FailedPTFiles.to_csv(full_path,index=False)
                    
        write_log(f"Saccessfully Saved failed rows of PTFILES :-{file_name} in folder :- {FAILED_ROWS_PTFILE_FOLDER}")
                     