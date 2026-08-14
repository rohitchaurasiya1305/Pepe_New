import pandas as pd
from common.outputDataFrame import df_InvoiceSummary,df_CreditNoteSummary
from common.write_invoicesummary_dataframe import write_df_InvoiceSumaary

def map_columns(df):
    mapping = {
            "Customer": "account",
            "Customer Name": "name of customer / vendor",
            "Posting Date": "posting date",
            "Document Type": "document type",
            "Document Type Description": None,
            "Bill No./Ref. No.": "billing document",
            "Debit Amount": "amount in local currency"
        }
    
    output_df = df_InvoiceSummary
    excel_columns = [col.strip().lower() for col in df.columns]
    for new_col, old_col in mapping.items():
        try:
            if old_col is None:
                output_df[new_col] = ""
                
            elif old_col in excel_columns:
                output_df[new_col] = df[old_col]
                
            else:
                output_df[new_col] = df[old_col]
                print(f"Warning: Column '{old_col}' not found in input")     
            
        except Exception as col_err:
            print(f"Error processing column '{new_col}': {col_err}")
            output_df[new_col] = None  
    print(output_df) 
    write_df_InvoiceSumaary(df_output_InvoiceSummary=output_df)