import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image
from bankstatementextractor.banks_utils import *
import json
import fitz  # PyMuPDF library
import PyPDF2  # PyPDF2 library
import os
import subprocess
import torch
from pdf2image import convert_from_path
from unidecode import unidecode
import pandas as pd
import itertools    
os.sys.path
from io import StringIO

class Banks:

    def __init__(self):
        pass
    # adcb_1
    def adcb_1(self,pdf_path):
        try:
            # Open the PDF file and read it as bytes
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            output = []  # Initialize the output list

            for page in doc:
                try:
                    page_output = page.get_text("blocks")
                    output.append(page_output)
                except Exception as e:
                    print(f"Error while processing page: {e}")
                    return None

            plain_text_data = []

            for page_output in output:
                previous_block_id = 0
                page_plain_text_data = []

                for block in page_output:
                    try:
                        if block[6] == 0:
                            if previous_block_id != block[5]:
                                plain_text = unidecode(block[4])
                                page_plain_text_data.append(plain_text)
                                previous_block_id = block[5]
                    except Exception as e:
                        print(f"Error while processing block: {e}")
                        return None

                if 'Consolidated Statement\n' in page_plain_text_data:
                    continue

                page_plain_text_data = [text for text in page_plain_text_data if not text.startswith(('balance', 'opening'))]

                plain_text_data.append(page_plain_text_data)

            account_num = None
            name = None
            opening_balance = None
            closing_balance = None

            # Iterate through the first sublist
            for line in plain_text_data[0]:
                try:
                    if line.startswith('Account Name(s)'):
                        name = line.split('\n')[1]
                    elif line.startswith('Account Number'):
                        account_number_with_currency = line.split('\n')[1]
                        account_number = account_number_with_currency.split(' ')[0]
                        currency_code = account_number_with_currency.split(' ')[1]   
                    elif line.startswith('Opening Balance'):
                        opening_balance_with_currency = line.split('\n')[1]
                        opening_balance = float(opening_balance_with_currency.replace(',', '').replace('AED', ''))
                    elif line.startswith('Closing Balance'):
                        closing_balance_with_currency = line.split('\n')[1]
                        closing_balance = float(closing_balance_with_currency.replace(',', '').replace('AED', ''))
                except Exception as e:
                    print(f"Error while processing account info: {e}")
                    return None

            obj = {
                "account_id": "",
                "name": name,
                "currency_code": currency_code,
                "type": "",
                "iban": "",
                "account_number": account_number,
                "bank_name": "ADCB",
                "branch": "",
                "credit": "",
                "address":""
            }       
            new_lst = []

            for sublist in plain_text_data:
                keep = False  # Flag to indicate whether to keep the elements
                
                for i, element in enumerate(sublist):
                    if element.startswith('Posting Date\nValue Date\nDescription\nRef/Cheque No'):
                        keep = True  
                        new_sublist = sublist[i+1:]  # Create a new sublist starting from the target element
                        break
                
                if keep:
                    new_lst.append(new_sublist)  # Add the new sublist to the result list if the target element is found

            flat_data = [item for sublist in new_lst for item in sublist]
            split_data = [entry.strip().split('\n') for entry in flat_data]

            # Create a DataFrame with specific column names
            df = pd.DataFrame(split_data, columns=['timestamp', 'Value Date', 'description', 'Ref/Cheque No', 'debit', 'credit', 'running_balance'])
            df['debit'] = df['debit'].str.replace(',', '').astype(float)
            df['credit'] = df['credit'].str.replace(',', '').astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y')
            df['running_balance'] = df['running_balance'].str.replace(',', '').astype(float)
            df['amount'] = df.apply(lambda row: -row['debit'] if row['debit'] != 0 else row['credit'], axis=1)
            for key, value in obj.items():
                df[key] = value
            df.drop(['debit', 'credit','Value Date','Ref/Cheque No'], axis=1, inplace = True)
            error_flags = {
                "data_cover_last_3_months": False,
                "statement_extracted_last_7_days": False,
                "outstanding_amount_match": False
            }

            Check if the data covers the last 3 months
            if (df['timestamp'].max() - df['timestamp'].min()).days < 90:
                error_flags["data_cover_last_3_months"] = True
                print("Error: Upload a 3 months bank statement")
                return None

            Check if the statement was extracted within the last 7 days of upload
            if (datetime.now().date() - df['timestamp'].max().to_pydatetime().date()).days > 7:
                error_flags["statement_extracted_last_7_days"] = True
                print("Error: Upload a statement extracted within the last 7 days")
                return None

            # Check if the outstanding amount matches the expected total
            if round(df['amount'].sum(), 2) != round(abs(opening_balance - closing_balance), 2):
                error_flags["outstanding_amount_match"] = True
                print("Error: Upload not edited bank statement")

            # If any condition failed (error flag is True), return None
            if any(error_flags.values()):
                return None
            
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
            json_data = df.to_json(orient='records')
            return json_data
        
        except Exception as e:
            print(f"Error during processing: {e}")
            return None
        

    
        
    