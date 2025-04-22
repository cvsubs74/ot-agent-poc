import streamlit as st

def green_expander(title, expanded=False):
    """
    Creates a custom expander with green styling.
    
    Args:
        title (str): The title of the expander
        expanded (bool): Whether the expander should be expanded by default
    
    Returns:
        A streamlit expander object with green styling
    """
    # Create the expander
    expander = st.expander(title, expanded=expanded)
    
    # Apply custom styling to the expander
    st.markdown("""
    <style>
    /* Target the most recently created expander */
    .st-emotion-cache-1y4p8pa:last-of-type, 
    .st-emotion-cache-ztfqz8:last-of-type,
    .st-emotion-cache-19rxjzo:last-of-type {
        background-color: #eaf7ea !important;
        border-left: 5px solid #27ae60 !important;
    }
    .st-emotion-cache-1eheh84:last-of-type,
    .st-emotion-cache-16idsys:last-of-type {
        border-left: 5px solid #27ae60 !important;
        background-color: #f8f9fa !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return expander
