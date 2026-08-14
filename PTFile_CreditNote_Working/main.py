import os
import shutil
import sys
import pathlib as Path
from dotenv import load_dotenv
from datetime import datetime
from common.logger import write_log,save_logs_html
from config.settings import (INPUT_FOLDER, FAILED_FOLDER,OUTPUT_PTFILE_FOLDER,LOG_PTFILE_FOLDER,OUTPUT_CREDITNOTEWORKING_FOLDER,LOG_CREDITNOTEWORKING_FOLDER,PTFiles_RequiredColumns,CreditNoteWorking_RequiredColumns)
from common.file_reader import read_input_file
from common.trim_Alldata import trim_dataFrame
from common.ptfiles_processor import filtered_PTFiles
from common.createnoteworking_proccessor import filtered_CreditNoteWorking
from common.write_creditnoteworking_dataframe import write_df_CreditNoteWorking
from common.write_ptfiles_dataframe import write_df_PTFiles
from common.sftp_client import download_files_from_sftp,upload_processed_files_to_sftp


def main():
    write_log(f"PT_Files and Credit_Note Working Process starting datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    download_files_from_sftp(local_folder=INPUT_FOLDER,remote_folder=os.getenv("REMOTE_DOWNLOAD_PTFILESCREDITNOTEWORKING"))
    
    
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
            
            #Check for missing columns in input file
            PTFiles_missing_cols = [col for col in PTFiles_RequiredColumns if col.strip().lower() not in excel_columns]
            
            #Check for missing columns in input file
            CreditNoteWorking_missing_cols = [col for col in CreditNoteWorking_RequiredColumns if col.strip().lower() not in excel_columns]
            
            if (PTFiles_missing_cols and CreditNoteWorking_missing_cols)==False:
                
                write_log(f"Missing columns in PT file {filepath.name}: {', '.join(PTFiles_missing_cols)} | "f"Missing columns in CreditNoteWorking: {', '.join(CreditNoteWorking_missing_cols)}")
                
                shutil.move(str(filepath), str(FAILED_FOLDER / filepath.name))
                write_log(f"Moved file :- {filepath} to Failed folder :- {FAILED_FOLDER}")
                continue
            
            else:
                
                write_log(f"All required columns present in file {filepath.name}")
                write_log(f"PT Files output generating in file started")
                
                # filter for Invoice Summary != ['ZRET']            
                df_SuccessPTFiles,df_FailedPTFiles = filtered_PTFiles(df=df)
                write_df_PTFiles(df_SuccessPTFiles,df_FailedPTFiles)
                upload_processed_files_to_sftp(local_folder=OUTPUT_PTFILE_FOLDER,remote_folder=os.getenv("REMOTE_UPLOAD_PTFILES"))
                
                write_log(f"Credit Note working output generating in file started")
                # filter for Credit Note Working =  ['ZRET']
                df_SuccessCreditNoteWorking,df_FailedCreditNoteWorking = filtered_CreditNoteWorking(df=df)
                write_df_CreditNoteWorking(df_SuccessCreditNoteWorking,df_FailedCreditNoteWorking)
                upload_processed_files_to_sftp(local_folder=OUTPUT_CREDITNOTEWORKING_FOLDER,remote_folder=os.getenv("REMOTE_UPLOAD_CREDITNOTEWORKING"))
                

            input_file_Rename = f"{filepath.stem}_read{filepath.suffix}"
            input_file_Rename_path = filepath.with_name(input_file_Rename)
            filepath.rename(input_file_Rename_path)
            
            write_log(f"Input file is renamed to :- {input_file_Rename_path.name}") 
            write_log(f"PTFiles and Credit_Note Working Process script is completed successfully")
            
            
            
        except Exception as e:
            write_log(f"Error while processing file :- {filepath} and error is :- {str(e)}")
            shutil.move(str(filepath), str(FAILED_FOLDER / filepath.name))
            write_log(f"Moved file :- {filepath} to Failed folder :- {FAILED_FOLDER}")
            continue
                  
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
       write_log(f"Fatal error and stopped process: {str(e)}")
    finally:
        write_log(f"PT_Files and Credit_Note Working Process ended datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        save_logs_html(index=0,LOG_FOLDER=LOG_PTFILE_FOLDER)
        save_logs_html(index=0,LOG_FOLDER=LOG_CREDITNOTEWORKING_FOLDER)
        
        
    
                    