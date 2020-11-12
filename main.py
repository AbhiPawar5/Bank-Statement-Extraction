import tabula
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--File", help="PDF file of Bank Statement to parse")
parser.add_argument("-o", "--Output", help="Name of Output CSV file to store transcation table")
args = parser.parse_args()

if args.File:
	pdf_path = args.File
else:
	pdf_path = "statement_masked.pdf"

dfs = tabula.read_pdf(pdf_path, stream=True, pages="all", silent=True)

maindf = pd.concat([x for x in dfs], ignore_index=True, sort=False)
maindf = maindf[maindf["Tran Id"].notna()]

maindf = maindf.rename(columns={'Tran Id': 'Reference_Number', 'Tran Date': 'Date', 'Remarks': 'Description',
                                'Amount (Rs.)':'Amount', 'Balance (Rs.)':'Balance'})
maindf.reset_index(drop=True, inplace=True)


def get_transcation_type(row):
    if "Cr" in row["Amount"]:
        return "Credit"
    elif "Dr" in row["Amount"]:
        return "Debit"

maindf["Transcation_Type"] = maindf.apply(get_transcation_type, axis=1)

finaldf = maindf.reindex(columns=['Date','Amount','Description','Reference_Number','Transcation_Type','Balance'])

if args.Output:
	finaldf.to_csv(args.Output, index=False)
else:
	finaldf.to_csv("transcation_table.csv", index=False)