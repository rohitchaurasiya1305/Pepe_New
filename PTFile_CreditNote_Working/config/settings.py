import os
import glob
import pandas as pd
from datetime import datetime
from pathlib  import Path

from common.logger import write_log

BASE_DIR = Path.cwd()
#BASE_DIR = Path(__file__).resolve().parent.parent

PTFILE_FOLDER = BASE_DIR / "PTFiles_Folder"
CREDITNOTEWORKING_FOLDER = BASE_DIR / "CreditNoteWorking_Folder"

INPUT_FOLDER  = BASE_DIR / "InputFiles"
FAILED_FOLDER = BASE_DIR / "FailedFiles"

OUTPUT_PTFILE_FOLDER = PTFILE_FOLDER / "OutputFiles"
LOG_PTFILE_FOLDER    = PTFILE_FOLDER / "LogFiles"
FAILED_ROWS_PTFILE_FOLDER = PTFILE_FOLDER / "FailedRows"

OUTPUT_CREDITNOTEWORKING_FOLDER = CREDITNOTEWORKING_FOLDER / "OutputFiles"
LOG_CREDITNOTEWORKING_FOLDER = CREDITNOTEWORKING_FOLDER / "LogFiles"
FAILED_ROWS_CREDITNOTEWORKING_FOLDER = CREDITNOTEWORKING_FOLDER / "FailedRows"



for folder in [INPUT_FOLDER,FAILED_FOLDER,OUTPUT_PTFILE_FOLDER,LOG_PTFILE_FOLDER,OUTPUT_CREDITNOTEWORKING_FOLDER,LOG_CREDITNOTEWORKING_FOLDER,FAILED_ROWS_PTFILE_FOLDER,FAILED_ROWS_CREDITNOTEWORKING_FOLDER]:
    folder.mkdir(parents=True,exist_ok=True)
      
print(f"successfully created folders :- [InputFiles , FailedFiles,PTFILE_FOLDER(OutputFiles,LogFiles,FailedRows) , CREDITNOTEWORKING_FOLDER(OutputFiles,LogFiles,FailedRows)]")


PTFiles_RequiredColumns =[
     "Billing Document",
     "Bill Date",
     "Name Sold-To-Party",
     "Ship-To Party",
     "Name Ship-To-Party",
     "EAN Code",
     "Description",
      "Item",
     "Actual Invoiced Quantity",
     "Max. Ret. Price",
     "Net Value",
     "HSN Code",
     "Sales Item",
      "Plant",
      "Tax Amount"
]
    
CreditNoteWorking_RequiredColumns =[ 
        "Billing Document",
        "Bill Date",
        "Name Sold-To-Party",
        "Ship-To Party",
        "Name Ship-To-Party",
        "EAN Code",
        "Description",
        "Item",
        "Actual Invoiced Quantity",
        "Max. Ret. Price",
        "Net Value",
        "HSN Code",
        "Sales Item",
        "Plant",
        "Tax Amount"
    ]
write_log(f"PT Files Required Columns name are :- {PTFiles_RequiredColumns}")
write_log(f"Credit Note Working Required Columns name are :- {CreditNoteWorking_RequiredColumns}")