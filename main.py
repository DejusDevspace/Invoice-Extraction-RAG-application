import streamlit as st
import invoiceutil as util

def main():

    st.set_page_config(
        page_title='Extraction Bot',
        page_icon=':pencil:'
    )

    st.title('Invoice Extraction Bot :rocket:')
    st.write("""Let's save your time extracting invoice data!""")

    # Upload invoice file(s)
    uploaded_files = st.file_uploader(
        'Upload your invoice(s). Only pdf format supported', 
        type=['pdf'],
        accept_multiple_files=True,
    )

    submit = st.button('Extract')

    if submit:
        with st.spinner('Extracting data...'):
            df = util.create_documents(uploaded_files)
            # Display the first columns of the invoice dataframe
            st.write(df.head())
            # Provide the invoice data in csv format for download 
            invoice_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='Download Invoice',
                data=invoice_csv,
                file_name='invoice_data.csv',
                mime='text/csv',
                key='csv-download-invoice',
            )
            st.success('Invoice Extracted Successfully!')

if __name__ == '__main__':
    main()
