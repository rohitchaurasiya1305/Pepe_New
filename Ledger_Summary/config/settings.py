import os
import glob
from tokenize import Name
from xml.dom.minidom import Text
import pandas as pd
from datetime import datetime
from pathlib  import Path

from common.logger import write_log

BASE_DIR = Path.cwd()
#BASE_DIR = Path(__file__).resolve().parent.parent

LEDGERSUMMARY_FOLDER = BASE_DIR / "LedgerSummary_Folder"


INPUT_FOLDER  = BASE_DIR / "InputFiles"
FAILED_FOLDER = BASE_DIR / "FailedFiles"

OUTPUT_LEDGERSUMMARY_FOLDER = LEDGERSUMMARY_FOLDER / "OutputFiles"
LOG_LEDGERSUMMARY_FOLDER    = LEDGERSUMMARY_FOLDER / "LogFiles"
FAILED_ROWS_LEDGERSUMMARY_FOLDER = LEDGERSUMMARY_FOLDER / "FailedRows"




for folder in [INPUT_FOLDER,FAILED_FOLDER,OUTPUT_LEDGERSUMMARY_FOLDER,LOG_LEDGERSUMMARY_FOLDER,FAILED_ROWS_LEDGERSUMMARY_FOLDER]:
    folder.mkdir(parents=True,exist_ok=True)
      
print(f"successfully created folders :- [InputFiles , FailedFiles,LEDGERSUMMARY_FOLDER(OutputFiles,LogFiles,FailedRows)]")


Ledger_Sumaary_RequiredColumns = ["Account", 
"Name of Customer / Vendor", 
"Posting Date", 
"Document Number", 
"Document Type", 
"Assignment", 
"Text", 
"Billing Document", 
"Reference", 
"Document Date", 
"Special G/L Indicator",
"Amount in Local Currency" ]

write_log(f"Ledger Summary Required Columns name are :- {Ledger_Sumaary_RequiredColumns}")