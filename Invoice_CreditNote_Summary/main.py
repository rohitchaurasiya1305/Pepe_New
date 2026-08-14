import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from config.settings import (INPUT_FOLDER,FAILED_FOLDER,OUTPUT_INVOICESUMMARY_FOLDER,LOG_INVOICESUMMARY_FOLDER,OUTPUT_CREDITNOTESUMMARY_FOLDER,LOG_CREDITNOTESUMMARY_FOLDER,Invoice_Summary_RequiredColumns,Credit_Note_Summary_RequiredColumns)
from common.logger import (write_log,save_logs_html)
from common.file_reader import read_input_file
from common.trim_Alldata import trim_dataFrame
from common.invoice_summary_processor import filtered_InvoiceSummary
from common.createnote_summary_proccessor import filtered_CreditNoteSummary
from common.write_invoicesummary_dataframe import write_df_InvoiceSummary
from common.write_creditnotesummary_dataframe import write_df_CreditNoteSummary
from common.sftp_client import download_files_from_sftp,upload_processed_files_to_sftp

def main():
    write_log(f"Invoice and Credit_Note Summary Process starting datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    download_files_from_sftp(local_folder=INPUT_FOLDER,remote_folder=os.getenv("REMOTE_DOWNLOAD_INVOICECREDITNOTESUMMARY"))
    
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
            InvoiceSummary_missing_cols = [col for col in Invoice_Summary_RequiredColumns if col.strip().lower() not in excel_columns]
            
            #Check for missing columns in input file
            CreditNoteSummary_missing_cols = [col for col in Credit_Note_Summary_RequiredColumns if col.strip().lower() not in excel_columns]
            
            if InvoiceSummary_missing_cols and CreditNoteSummary_missing_cols:
                write_log(f"Missing columns in PT file {filepath.name}: {', '.join(InvoiceSummary_missing_cols)} | "f"Missing columns in CreditNoteWorking: {', '.join(CreditNoteSummary_missing_cols)}")
                shutil.move(str(filepath), str(FAILED_FOLDER / filepath.name))
                write_log(f"Moved file :- {filepath} to Failed folder :- {FAILED_FOLDER}")
                continue
            
            else:
                write_log(f"All required columns present in file {filepath.name}")
                write_log(f"Invoice summary output generating in file started")
                
                # filter for Invoice Summary = ['RV']            
                df_SuccessInvoiceSummary,df_FailedInvoiceSummary = filtered_InvoiceSummary(df=df)
                write_df_InvoiceSummary(df_SuccessInvoiceSummary,df_FailedInvoiceSummary)
                upload_processed_files_to_sftp(local_folder=OUTPUT_INVOICESUMMARY_FOLDER,remote_folder=os.getenv("REMOTE_UPLOAD_INVOICESUMMARY"))
                
                write_log(f"Credit Note summary output generating in file started")
                
                # filter for Credit Note Summary =  ['RW', 'DG' , 'DA']
                df_SuccessCreditNoteSummary,df_FailedCreditNoteSummary = filtered_CreditNoteSummary(df=df)
                write_df_CreditNoteSummary(df_SuccessCreditNoteSummary,df_FailedCreditNoteSummary)
                upload_processed_files_to_sftp(local_folder=OUTPUT_CREDITNOTESUMMARY_FOLDER,remote_folder=os.getenv("REMOTE_UPLOAD_CREDITNOTESUMMARY"))
            
            input_file_Rename = f"{filepath.stem}_read{filepath.suffix}"
            input_file_Rename_path = filepath.with_name(input_file_Rename)
            filepath.rename(input_file_Rename_path)
            
            write_log(f"Input file is renamed to :- {input_file_Rename_path.name}")
            write_log(f"Invoice and Credit_Note Summary Process script is completed successfully")  
           
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
        write_log(f"Invoice and Credit_Note Summary Process ended datetime :- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        save_logs_html(index=0,LOG_FOLDER=LOG_INVOICESUMMARY_FOLDER)
        save_logs_html(index=0,LOG_FOLDER=LOG_CREDITNOTESUMMARY_FOLDER)
        
        
    