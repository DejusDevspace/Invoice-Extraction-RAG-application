from langchain_google_genai import GoogleGenerativeAI
import os
from pypdf import PdfReader
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
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
        text = ''
        # print('Processing ---', filename)

        # Read the pages and add them to the text as 
        pdf_reader = PdfReader(filename)
        for page in pdf_reader.pages:
            # print(page)
            # print('\n\n------', page.extract_text())
            text += page.extract_text()

        # Template for invoice formatting
        template = """Extract all the following values : invoice no., Description, Quantity, date, 
            Unit price , Amount, Total, email, phone number and address from the following Invoice content: 

            {texts}

            The fields and values in the above content may be jumbled up as they are extracted from a PDF. Please use your judgement to align
            the fields and values correctly based on the fields asked for in the question above.

            Expected output format: 

            {{'Invoice no.': xxxxxxxx','Description': 'xxxxxx','Quantity': 'x','Date': 'dd/mm/yyyy',
            'Unit price': xxx.xx','Amount': 'xxx.xx,'Total': xxx,xx,'Email': 'xxx@xxx.xxx','Phone number': 'xxxxxxxxxx','Address': 'xxxxxxxxx'}}

            Remove any dollar symbols or currency symbols from the extracted values. Also, ALWAYS avoid writing 'json' before the dictionary in the output.
            """
        
        # Prompt template
        prompt = PromptTemplate.from_template(template)
        # Chain
        chain = prompt | llm
        # Invoke the chain to get the dictionary 
        data = chain.invoke(text)
        # print('Dict ---', data)

        # Add the output from the llm to the pandas dataframe
        row_df = pd.DataFrame([eval(data)], columns=df.columns)
        df = pd.concat([df, row_df], ignore_index=True)  

    # print(df) 
    return df


# test = create_documents(['invoice_1001329.pdf'])

# print(test.head())