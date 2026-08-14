import pandas as pd
import sys
import os
import shutil
from sqlalchemy import Date
from common.logger import write_log
from common.remark_generator import (is_invalid,is_integer,is_datetimeformat)

pd.set_option('future.no_silent_downcasting', True)

def filtered_LedgerSummary(df):
    
    filter_LedgerSummary_df = df
    write_log(f"Ledger summary has no filtered column   \n length of Ledger summary filtered dataframe is :- {len(filter_LedgerSummary_df)}" )
    output_LedgerSummary_rows = []
    for index, row in filter_LedgerSummary_df.iterrows():
        remarks = []
        amount = row.get("Amount in local currency")
        posting_date = row.get("Posting Date")
        
        if is_invalid(amount) : #this add new remark logic as per changes 10-08-2026
            remarks.append(f"Curr/INR is blank")
        if not is_integer(amount) :
            remarks.append(f"Curr/INR must be integer")  
        if not is_datetimeformat(str(posting_date)):
            remarks.append(f"Invalid Posting Date")
        
        new_row = {
            'Customer' : row.get("Account"), 
	        'Customer Name' : "" ,#row['Name of Customer / Vendor'], 
	        'Posting Date' : posting_date,
            'Doc. No.' : row.get("Document Number"),
            'Document Type' : row.get("Document Type"),
            'Document Type Description' : "",
            'Assignment No.' : row.get("Assignment"),
            'Debit Amount' : "",  #row.get("Amount in local currency"),
            'Credit Amount' : "", #row.get("Amount in foreign currency"),
            'Balance' : "", #row.get("Balance"),
            'Opening Balance' : "", #row.get("Opening Balance"),
            'Text' : row.get("Text"),
            'Bill No./Ref. No.' : row.get("Billing Document"),
            'Reference Number' : row.get("Reference"),
        	'MIRO No.' : "", #row.get("MIRO No."),
        	'Doc./Invoice Date' : row.get("Document Date"),
        	'Special G/L' : row.get("Special G/L Ind."),
        	'Curr/INR' : amount,
        	'Foreign Currency' : "", #row.get("Foreign Currency"),
        	'Business Area ' : "", #row.get("Business Area"),
	        'TDS' : "", #row.get("TDS"), 
            'Sales Order': "", #row.get("Sales Order"), 
            'Plant' : "", #row.get("Plant"),
            'UOM' : "", #row.get("UOM"),
            'Quantity' : "", #row.get("Quantity"),
            'Billing Doc' : "", #row.get("Billing Doc")
            'Remark' : ", ".join(remarks)
            }
        output_LedgerSummary_rows.append(new_row)
    df_output_LedgerSummary = pd.DataFrame(output_LedgerSummary_rows)
    
    success_df = df_output_LedgerSummary[df_output_LedgerSummary['Remark']==""].drop(columns=['Remark'])
    failed_df = df_output_LedgerSummary[df_output_LedgerSummary['Remark']!=""]
    
    write_log(f"Success DF length = {len(success_df)}.\n Successfully processed ledger Summary success records.\n {success_df}")
    write_log(f"Failed DF length = {len(failed_df)}.\n Successfully processed ledger Summary failed records.\n {failed_df}")
    
    return success_df,failed_df  
    
    
    
    