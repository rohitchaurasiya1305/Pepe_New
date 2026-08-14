import pandas as pd
import sys
import os
from common.logger import write_log
from common.remark_generator import is_integer,is_invalid,is_datetimeformat
pd.set_option('future.no_silent_downcasting', True)

def filtered_PTFiles(df):
    
    filter_PTFiles_df = df.loc[df['Order Type']!='ZRET']
    #df['Order Type'] = df['Order Type'].str.lower()
    #filter_PTFiles_df = df.loc[df['Order Type'] != 'zret']  
    write_log(f"PT_Files has filtered column :-Order Type Not equal to  ZRET  \n length of PT_Files filtered dataframe is :- {len(filter_PTFiles_df)}" )
    output_PTFiles_rows = []
    for index, row in filter_PTFiles_df.iterrows():
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
            'Brand Name': "",
            'Invoice Number': row.get('Billing Document'),
            'Invoice Date': posting_date,
            'Bill To Party': row.get('Name Sold-To-Party'),
            'Ship To Party Code': row.get('Ship-To Party'),
            'Ship To Party Name': row.get('Name Ship-To-Party'),
            'Order Type': row.get('Order Type'),
            'SPSN': "",
            'Category': "",
            'Group Category': "",
            'Delivery No.': "",
            'G Article': "",
            'Sizes': "",
            'EAN Code': row.get('EAN Code'),
            'Item Description': row.get('Description'),
            'Fit': "",
            'Style': "",
            'Colour': "",
            'Invoice Qty': row.get('Actual Invoiced Quantity'),
            'Unit MRP': row.get('Max. Ret. Price'),
            'Channel': "",
            'Sales Ofc': "",
            'Basic Amount': amount ,#row.get('Net Value'),
            'Discount Value': "",
            'Discount %': "",
            'Taxable Value': amount, #row.get('Net Value'),
            'Cost per Unit': "",
            'HSN Code': row.get('HSN Code'),
            'Brand Type': "",
            'Line Item Number': row.get('Item'),
            'Supplying Plant': row.get('Plant'),
            'IGST Value': row.get('Tax Amount'),
            'CGST Value': row.get('Tax Amount'),
            'SGST Value': row.get('Tax Amount'),
            'IGST Tax %': "",
            'CGST Tax %': "",
            'SGST Tax %': "",
            'Docket No.': "",
            'Docket Date': "",
            'Acknowledgement No.': "",
            'Article Season': "",
            'Remark' : ", ".join(remarks)
        }
        output_PTFiles_rows.append(new_row)
    df_output_PTFiles = pd.DataFrame(output_PTFiles_rows)
     
    success_df = df_output_PTFiles[df_output_PTFiles['Remark']==""].drop(columns= ['Remark'])
    failed_df = df_output_PTFiles[df_output_PTFiles['Remark']!=""]
    
    write_log(f"Success DF length = {len(success_df)}.\n Successfully processed PTFiles success records.\n {success_df}")
    write_log(f"Failed DF length = {len(failed_df)}.\n Successfully processed PTFiles failed records.\n {failed_df}")
    return success_df,failed_df 
    
    
    