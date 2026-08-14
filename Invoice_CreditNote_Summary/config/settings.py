import os
import glob
import pandas as pd
from datetime import datetime
from pathlib  import Path

from common.logger import write_log

BASE_DIR = Path.cwd()
#BASE_DIR = Path(__file__).resolve().parent.parent

INVOICESUMMARY__FOLDER = BASE_DIR / "InvoiceSummary_Folder"
CREDITNOTESUMMARY_FOLDER = BASE_DIR / "CreditNoteSummary_Folder"

INPUT_FOLDER  = BASE_DIR / "InputFiles"
FAILED_FOLDER = BASE_DIR / "FailedFiles"

OUTPUT_INVOICESUMMARY_FOLDER = INVOICESUMMARY__FOLDER / "OutputFiles"
LOG_INVOICESUMMARY_FOLDER    = INVOICESUMMARY__FOLDER / "LogFiles"
FAILED_ROWS_INVOICESUMMARY_FOLDER = INVOICESUMMARY__FOLDER / "FailedRows"

OUTPUT_CREDITNOTESUMMARY_FOLDER = CREDITNOTESUMMARY_FOLDER / "OutputFiles"
LOG_CREDITNOTESUMMARY_FOLDER = CREDITNOTESUMMARY_FOLDER / "LogFiles"
FAILED_ROWS_CREDITNOTESUMMARY_FOLDER = CREDITNOTESUMMARY_FOLDER / "FailedRows"


for folder in [INPUT_FOLDER,FAILED_FOLDER,OUTPUT_INVOICESUMMARY_FOLDER,LOG_INVOICESUMMARY_FOLDER,OUTPUT_CREDITNOTESUMMARY_FOLDER,LOG_CREDITNOTESUMMARY_FOLDER,FAILED_ROWS_INVOICESUMMARY_FOLDER,FAILED_ROWS_CREDITNOTESUMMARY_FOLDER]:
    folder.mkdir(parents=True,exist_ok=True)
      
print(f"successfully created folders :- [InputFiles , FailedFiles,INVOICESUMMARY__FOLDER(OutputFiles,LogFiles) , CREDITNOTESUMMARY_FOLDER(OutputFiles,LogFiles)]")


Invoice_Summary_RequiredColumns =["Account",
    "Name of Customer / Vendor",
    "Posting Date",
    "Document Type",
    "Billing Document",
    "Amount in Local Currency"]
    
Credit_Note_Summary_RequiredColumns =[ "Account",
    "Name of Customer / Vendor",
    "Posting Date",
    "Document Number",
    "Document Type",
    "Text",
    "Billing Document",
    "Amount in Local Currency"
]
write_log(f"Invoice Summary Required Columns name are :- {Invoice_Summary_RequiredColumns}")
write_log(f"Credit Note Summary Required Columns name are :- {Credit_Note_Summary_RequiredColumns}")