import pandas as pd
import sys
import os
import shutil
from common.logger import write_log
from common.remark_generator import is_integer,is_invalid,is_datetimeformat
pd.set_option('future.no_silent_downcasting', True)

def filtered_InvoiceSummary(df):
    
    filter_InvoiceSummary_df = df.loc[df['Document Type']=='RV']
    write_log(f"Invoice summary has filtered column :-Document Type == RV  \n length of Invoice summary filtered dataframe is :- {len(filter_InvoiceSummary_df)}" )
    output_InvoiceSummary_rows = []
    
    for index, row in filter_InvoiceSummary_df.iterrows():
        remarks = []
        amount = row.get("Amount in local currency")
        posting_date = row.get("Posting Date")
        
        
        if is_invalid(amount) : #this add new remark logic as per changes 10-08-2026
            remarks.append(f"Debit Amount is blank")
        if not is_integer(amount) :
            remarks.append(f"Debit Amount must be integer")  
        if not is_datetimeformat(str(posting_date)):
            remarks.append(f"Invalid Posting Date")
             
        new_row = {
            'Customer' : row.get("Account"),
            'Customer Name' : "",#row['Name of Customer / Vendor'],
            'Posting Date'  : posting_date,
            'Document Number' : row.get("Document Number"),
            'Document Type' : row.get("Document Type"),
            'Document Type Description' : "",
            'Bill No./Ref. No.' : row.get("Billing Document"),
            'Debit Amount' : amount,
            'Remark' : ", ".join(remarks)
        }
        output_InvoiceSummary_rows.append(new_row)
         
    df_output_InvoiceSummary = pd.DataFrame(output_InvoiceSummary_rows)
    
    success_df = df_output_InvoiceSummary[df_output_InvoiceSummary['Remark']==""].drop(columns= ['Remark'])
    failed_df = df_output_InvoiceSummary[df_output_InvoiceSummary['Remark']!=""]
    
    write_log(f"Success DF length = {len(success_df)}.\n Successfully processed Invoice Summary success records.\n {success_df}")
    write_log(f"Failed DF length = {len(failed_df)}.\n Successfully processed Invoice Summary failed records.\n {failed_df}")
    return success_df,failed_df 
    
    
    
    