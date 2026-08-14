from typing import Text

import pandas as pd

InvoiceSummary_columns = [
    "Customer",
    "Customer Name",
    "Posting Date",
    "Document Type",
    "Document Type Description",
    "Bill No./Ref. No.",
    "Debit Amount"
]

df_InvoiceSummary = pd.DataFrame(columns=InvoiceSummary_columns)

CreditNoteSummary_columns = [
    "Customer", 
    "Customer Name",
    "Posting Date",
    "Document Number",
    "Document Type",
    "Document Type Description",
    "Text",
    "Bill No./Ref. No.",
    "Debit Amount",
    "Credit Amount"
]

df_CreditNoteSummary = pd.DataFrame(columns=CreditNoteSummary_columns)  

