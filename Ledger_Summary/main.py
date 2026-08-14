import os
import sys
import shutil
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from config.settings import (INPUT_FOLDER,FAILED_FOLDER,OUTPUT_LEDGERSUMMARY_FOLDER,LOG_LEDGERSUMMARY_FOLDER,Ledger_Sumaary_RequiredColumns)
from common.logger import (write_log,save_logs_html)
from common.file_reader import read_input_file
from common.trim_Alldata import trim_dataFrame
from common.ledger_summary_processor import filtered_LedgerSummary
from common.write_ledgersummary_dataframe import write_df_LedgerSumaary
from common.sftp_client import download_files_from_sftp,upload_processed_files_to_sftp


def main():
     write_log(f" Ledger Summary Process starting datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
     download_files_from_sftp(local_folder=INPUT_FOLDER,remote_folder=os.getenv("REMOTE_DOWNLOAD_LEDGERSUMMARY"))
     
     for index , filepath in enumerate(INPUT_FOLDER.glob("*")):
         try:
            if "read" in filepath.stem:
                write_log(f"File {filepath.name} is already processed and renamed with read, so skipping this file")
                continue
            
            write_log(f"Processing file {filepath.name} started")
            
            #Read input file
            df = read_input_file(filePath=filepath)
            
            #Trim input file data
            df = trim_dataFrame(df=df)
            
            excel_columns = [col.strip().lower() for col in df.columns]
            
            Ledger_Sumaary_missing_cols = [col for col in Ledger_Sumaary_RequiredColumns if col.strip().lower() not in excel_columns]
            
            if Ledger_Sumaary_missing_cols == False:
                write_log(f"Missing columns in file {filepath.name} is :- {', '.join(Ledger_Sumaary_missing_cols)}")
                shutil.move(str(filepath), str(FAILED_FOLDER / filepath.name))
                write_log(f"Moved file :- {filepath} to Failed folder :- {FAILED_FOLDER}")
                continue
            else:
                write_log(f"All required columns are present in file {filepath.name}")
                
                df_SuccessLedgerSummary,df_FailedLedgerSummary = filtered_LedgerSummary(df=df)
                write_df_LedgerSumaary(df_SuccessLedgerSummary,df_FailedLedgerSummary)
                upload_processed_files_to_sftp(local_folder=OUTPUT_LEDGERSUMMARY_FOLDER,remote_folder=os.getenv("REMOTE_UPLOAD_LEDGERSUMMARY"))
                
            input_file_Rename = f"{filepath.stem}_read{filepath.suffix}"
            input_file_Rename_path = filepath.with_name(input_file_Rename)
            filepath.rename(input_file_Rename_path)
            write_log(f"Input file is renamed to :- {input_file_Rename_path.name}")
             
            write_log(f"Ledger Summary Process script is completed successfully")
             
         except Exception as e:
             write_log(f"Error while processing file :- {filepath} and error is :- {str(e)}")
             shutil.move(str(filepath),str(FAILED_FOLDER / filepath.name))
             write_log(f"Moved file :- {filepath} to Failed folder :- {FAILED_FOLDER}")
             continue    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
            write_log(f"Fatal error and stopped process: {str(e)}")
    finally:
        write_log(f"Ledger Summary Process ended datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        save_logs_html(index=0,LOG_FOLDER=LOG_LEDGERSUMMARY_FOLDER)      
        
    
    

       