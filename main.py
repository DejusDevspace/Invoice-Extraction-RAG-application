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
        pass


if __name__ == '__main__':
    main()
