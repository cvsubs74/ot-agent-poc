import streamlit as st

class PageConfigurator:
    """Class to handle Streamlit page configuration and styling."""
    
    @staticmethod
    def configure_page():
        """Configure the Streamlit page settings."""
        st.set_page_config(page_title="OneTrust Platform", layout="wide")

        # Store the current section in session state if not already there
        if 'current_section' not in st.session_state:
            st.session_state['current_section'] = 'Core'

        # Inject custom CSS for styling
        st.markdown("""
        <style>
        /* Import Font Awesome for icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
        
        /* Main styling */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Page header styling */
        .page-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            padding-bottom: 0.25rem;
            display: flex;
            align-items: center;
        }
        
        .page-header i {
            margin-right: 0.75rem;
            color: #3498db;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: white;
            border-radius: 4px;
            padding: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: 4px;
            color: #495057;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #e9f7fe !important;
            color: #3498db !important;
            font-weight: 600;
        }
        
        /* Card styling for content sections */
        .stDataFrame, div.stTable {
            border: none !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            border-radius: 6px !important;
        }
                
        /* Sidebar styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #f0f0f0;
        }
        
        /* Tab styling */
        .stTabs [role="tablist"] {
            background-color: #f4f4f4;
            padding: 5px;
            border-radius: 10px;
        }
        
        .stTabs [role="tab"] {
            background-color: #3498db;
            color: white;
            font-size: 16px;
            margin-right: 2px;
            padding: 10px 15px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .stTabs [role="tab"]:hover {
            background-color: #2980b9;
            color: white;
        }
        
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #1a5276;
            color: white;
        }
        
        /* Card styling */
        .card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar menu styling */
        .sidebar-menu {
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            color: #333;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
            text-align: left;
            display: flex;
            align-items: center;
        }
        
        .sidebar-menu:hover {
            background-color: #f8f9fa;
            border-left: 3px solid #3498db;
        }
        
        .sidebar-menu.active {
            background-color: #f8f9fa;
            border-left: 3px solid #1abc9c;
            font-weight: 600;
        }
        
        /* Icon styling */
        .sidebar-menu i {
            width: 20px;
            text-align: center;
            margin-right: 8px;
        }
        
        /* Sidebar section headers */
        .sidebar-section-header {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #eee;
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: #2c3e50;
        }
        
        /* Table styling */
        .dataframe {
            border-collapse: collapse;
            width: 100%;
            border-radius: 5px;
            overflow: hidden;
        }
        
        .dataframe th {
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        .dataframe td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        
        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        .dataframe tr:hover {
            background-color: #e6f7ff;
        }
        </style>
        """, unsafe_allow_html=True)

        # Style the menu items with improved CSS for left alignment
        st.markdown(f"""
            <style>
            /* Style for all buttons */
            div[data-testid="stButton"] > button {{
                background-color: #e6f3ff; /* Light blue background for all buttons */
                color: #333;
                border: 1px solid #a8d8ff; /* Light blue border for all buttons */
                text-align: left !important;
                font-weight: normal;
                padding: 8px 10px;
                border-radius: 4px;
                box-shadow: none;
                width: 100%;
                margin: 0;
                transition: all 0.2s ease;
                display: flex !important;
                align-items: center !important;
                justify-content: flex-start !important;
            }}
            
            /* Style for active button */
            div[data-testid="stButton"] > button#{'core_constructs_button' if st.session_state['current_section'] == 'Core' else 
                                                 'regulatory_btn' if st.session_state['current_section'] == 'Regulatory' else
                                                 'decision_tree_btn' if st.session_state['current_section'] == 'Decision Tree' else
                                                 'sensitivity_api_btn' if st.session_state['current_section'] == 'Sensitivity API' else
                                                 'legal_basis_api_btn' if st.session_state['current_section'] == 'Legal Basis API' else
                                                 'breach_api_btn'} {{
                color: #3498db;
                font-weight: 600;
                background-color: #f8f9fa;
                border: 1px solid #3498db; /* Darker blue border for active button */
                border-left: 3px solid #3498db;
            }}
            
            /* Hover effect for buttons */
            div[data-testid="stButton"] > button:hover {{
                background-color: #cce5ff; /* Darker blue background on hover */
                color: #3498db;
            }}
            
            /* Force text alignment in buttons */
            div[data-testid="stButton"] > button p {{
                text-align: left !important;
                display: inline-block;
                margin: 0;
                padding: 0;
            }}
            
            /* Override any Streamlit defaults that might center text */
            .stButton {{
                text-align: left !important;
            }}
            
            /* Section header styling */
            .sidebar-section-header {{
                font-size: 0.9rem;
                font-weight: 600;
                color: #6c757d;
                margin-top: 20px;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                text-align: left;
            }}
            </style>
            """, unsafe_allow_html=True)  
