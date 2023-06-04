"""utility module

Handles streamlit-aggrid to support the pages.
"""


import streamlit as st

def page_setting(page_title='', icon=':smile:', layout='centered'):
    """Uses streamlit's set_page_config function."""
    st.set_page_config(
        page_title=page_title,
        page_icon=icon,
        layout=layout
    )

def login_warning():
    """Shows a message as user warning."""
    st.markdown('''
    Por favor, realize **log in** para acessar o conteúdo do site.
    ''')