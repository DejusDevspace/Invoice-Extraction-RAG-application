from langchain_google_genai import GoogleGenerativeAI
import os
from pypdf import PdfReader
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

llm = GoogleGenerativeAI(
    model='gemini-1.5-pro-latest',
    google_api_key=os.getenv('GOOGLE_API_KEY'),
    temperature=0
)

def create_documents(files: list[str]) -> pd.DataFrame:
    """
    Extracts data from the uploaded file(s) (invoice) and stores it in 
    a dataframe
    """

    # Empty dataframe with expected columns
    df = pd.DataFrame({
        'Invoice no.': pd.Series(dtype='str'),
        'Description': pd.Series(dtype='str'),
        'Quantity': pd.Series(dtype='str'),
        'Date': pd.Series(dtype='str'),
	    'Unit price': pd.Series(dtype='str'),
        'Amount': pd.Series(dtype='int'),
        'Total': pd.Series(dtype='str'),
        'Email': pd.Series(dtype='str'),
	    'Phone number': pd.Series(dtype='str'),
        'Address': pd.Series(dtype='str')
    })

    # Data extraction from invoice pdf(s)
    for filename in files:
        print(filename)
        text = ''
        print('Processing ---', filename)
        # Read the pages and add them to the text as 
        pdf_reader = PdfReader(filename)
        for page in pdf_reader.pages:
            print(page)
            print('\n\n------', page.extract_text())
            # texts += page.extract_text()


create_documents(['invoice_1001329.pdf'])
