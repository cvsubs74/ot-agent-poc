import streamlit as st

def apply_green_expander_styling():
    """
    Apply green styling to all expanders in the application.
    This function should be called at the beginning of the application.
    """
    st.markdown("""
    <style>
    /* Target Streamlit expanders with direct attribute selectors */
    div[data-testid="stExpander"] {
        border: 1px solid #27ae60 !important;
        border-radius: 4px !important;
        margin-bottom: 10px !important;
    }
    
    /* Target the header of the expander */
    div[data-testid="stExpander"] > div:first-child {
        background-color: #eaf7ea !important;
        border-left: 5px solid #27ae60 !important;
        padding: 10px !important;
    }
    
    /* Target the content of the expander */
    div[data-testid="stExpander"] > div:last-child {
        border-left: 5px solid #27ae60 !important;
        background-color: #f8f9fa !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
