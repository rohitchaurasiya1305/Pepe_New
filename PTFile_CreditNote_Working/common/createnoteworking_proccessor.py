import pandas as pd
import sys
import os
import shutil
from common.logger import write_log
from common.remark_generator import is_integer,is_invalid,is_datetimeformat
pd.set_option('future.no_silent_downcasting', True)

def filtered_CreditNoteWorking(df):
    
    filter_CreditNoteWorking_df = df.loc[df['Order Type']=='ZRET']
    write_log(f"Credit Note working has filtered column :-Order Type == 'ZRET'  \n length of CreditNote working filtered dataframe is :- {len(filter_CreditNoteWorking_df)}" )
    output_CreditNoteWorking_rows = []
    for index, row in filter_CreditNoteWorking_df.iterrows():
        remarks = []
        amount = row.get("Net value")
        posting_date = row.get("Bill.Date")
                
        if is_invalid(amount) : #this add new remark logic as per changes 10-08-2026
            remarks.append(f"Net value is blank")
        if not is_integer(amount) :
            remarks.append(f"Net value must be integer")  
        if not is_datetimeformat(str(posting_date)):
            remarks.append(f"Invalid Bill.Date")
                       
        new_row = {
                "Brand Name" : "",
                "Invoice Number" : row.get('Billing Document'), 
                "Invoice Date" : posting_date,
                "Bill To Party" : row.get('Name Sold-To-Party'),
                "Ship To Party Code" : row.get('Ship-To Party'),
                "Ship To Party Name" : row.get('Name Ship-To-Party'),
                "Order Type" : row.get('Order Type'),
                "SPSN" : "",
                "Category" : "",
                "Group Category" : "",
                "Delivery No." : "",
                "G Article" : "",
                "Sizes" : "",
                "EAN Code" : row.get('EAN Code'),
                "Item Description" : row.get('Description'),
                "Fit" : "",
                "Style" : "",
                "Colour" : "",
                "Invoice Qty" : row.get('Actual Invoiced Quantity'),
                "Unit MRP" : row.get('Max. Ret. Price'),
                "Channel" : "",
                "Sales Ofc" : "",
                "Basic Amount" : row.get('Net Value'),
                "Discount Value" : "",
                "Discount %" : "",
                "Taxable Value" : row.get('Net Value'),
                "Cost per Unit" : "",
                "HSN Code" : row.get('HSN Code'),
                "Brand Type" : "",
                "Line Item Number" : row.get('Item'),
                "Supplying Plant" : row.get('Plant'),
                "IGST Value" : row.get('Tax Amount'),
                "CGST Value" : row.get('Tax Amount'),
                "SGST Value" : row.get('Tax Amount'),
                "IGST Tax %" : "",
                "CGST Tax %" : "",
                "SGST Tax %" : "",
                "Docket No." : "",
                "Docket Date" : "",
                "Acknowledgement No." : "",
                "Article Season" : "",
                "Remark" : ", ".join(remarks)
        }
        output_CreditNoteWorking_rows.append(new_row)
    df_output_CreditNoteWorking = pd.DataFrame(output_CreditNoteWorking_rows) 
    success_df = df_output_CreditNoteWorking[df_output_CreditNoteWorking['Remark']==""].drop(columns= ['Remark'])
    failed_df = df_output_CreditNoteWorking[df_output_CreditNoteWorking['Remark']!=""]
       
    write_log(f"Success DF length = {len(success_df)}.\n Successfully processed CreditNoteWorking success records.\n {success_df}")
    write_log(f"Failed DF length = {len(failed_df)}.\n Successfully processed CredutNoteWorking failed records.\n {failed_df}")
    return success_df,failed_df 
       
       
       
    
    
    