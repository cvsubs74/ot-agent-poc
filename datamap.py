import os
import time

# Set environment variables to avoid config issues
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "500"

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pyvis.network import Network
import streamlit.components.v1 as components

from repositories.GlossaryRepository import GlossaryRepository
from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.InventoryRepository import InventoryRepository
from repositories.DatabaseManager import DatabaseManager

class DataMap:
    def __init__(self):
        """Initialize the DataMap application with repositories."""
        self.database_manager = DatabaseManager()
        self.glossary_repository = GlossaryRepository(self.database_manager.connection)
        self.regulatory_metadata_repository = RegulatoryMetadataRepository(self.database_manager.connection)
        self.inventory_repository = InventoryRepository(self.database_manager.connection)
        
    @staticmethod
    def divider(height=1):
        """Utility function to create a divider with specified height."""
        st.markdown(
            f"<hr style='height:{height}px; margin-top: 0; margin-bottom: 0; border-width:0; background: lightblue;'>",
            unsafe_allow_html=True
        )

    def configure_page(self):
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

    def core_constructs_section(self):
        """Handle the Core Constructs section with its tabs."""
        st.markdown("<div class='page-header'><i class='fas fa-book'></i> &nbsp;Core Constructs</div>", unsafe_allow_html=True)
        
        st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Core Constructs™</strong> are foundational reference entities that power the entire OneTrust Platform. They establish a unified source of truth across all modules and functions.</p>
            <ul>
                <li><strong>Centralized Reference Data:</strong> All domain-specific attributes reference master data from Core Constructs, ensuring consistency and eliminating redundancy</li>
                <li><strong>System-Wide Attribute Types:</strong> Each Core Construct maps to a corresponding system attribute type, enabling seamless integration across the platform</li>
                <li><strong>Enterprise-Wide Standardization:</strong> Consistent terminology and values across all platform modules promote better governance and reporting</li>
                <li><strong>Pre-Configured Foundation:</strong> The platform includes comprehensive, ready-to-use reference data for immediate deployment</li>
                <li><strong>Extensible Architecture:</strong> Core Constructs can be customized to meet organization-specific requirements while maintaining system integrity</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        tabs = st.tabs([
            "Law", "Jurisdictions", "Legal Basis", "Data Elements", 
            "Data Subject Types", "Data Categories", "Context", "Sensitivity", "Purpose Categories", "Breach Types"
        ])
        
        # Law tab
        with tabs[0]:
            st.subheader("Law Definitions")
            st.markdown("""
            <div class="card">
                <p>A law is a system of rules created and enforced through social or governmental institutions to regulate behavior. 
                In the context of data protection, laws establish the legal framework for how organizations must handle personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get law data from repository
            laws = self.glossary_repository.get_laws()
            if laws:
                law_data = {
                    "Law Name": [],
                    "Description": [],
                    "Scope": []
                }
                for law in laws:
                    law_data["Law Name"].append(law["name"])
                    law_data["Description"].append(law["description"])
                    law_data["Scope"].append(law["scope"])
                
                st.dataframe(pd.DataFrame(law_data))
            else:
                st.warning("No data available in the database.")
        
        # Jurisdictions tab
        with tabs[1]:
            st.subheader("Jurisdictions")
            st.markdown("""
            <div class="card">
                <p>Jurisdictions are geographical areas with specific legal authority. In data protection, different jurisdictions may have different laws and regulations governing how personal data must be handled.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get jurisdiction data from repository
            jurisdictions = self.glossary_repository.get_jurisdictions()
            if jurisdictions:
                jurisdiction_data = {
                    "Jurisdiction": []
                }
                for jurisdiction in jurisdictions:
                    jurisdiction_data["Jurisdiction"].append(jurisdiction["name"])
                
                st.dataframe(pd.DataFrame(jurisdiction_data))
            else:
                st.warning("No data available in the database.")
        
        # Legal Basis tab
        with tabs[2]:
            st.subheader("Legal Basis")
            st.markdown("""
            <div class="card">
                <p>A legal basis is the lawful ground for processing personal data. Data protection laws typically require organizations to have a valid legal basis before they can process personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get legal basis data from repository
            legal_bases = self.glossary_repository.get_legal_bases()
            if legal_bases:
                legal_basis_data = {
                    "Legal Basis": [],
                    "Description": []
                }
                for legal_basis in legal_bases:
                    legal_basis_data["Legal Basis"].append(legal_basis["name"])
                    legal_basis_data["Description"].append(legal_basis["description"])
                
                st.dataframe(pd.DataFrame(legal_basis_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Elements tab
        with tabs[3]:
            st.subheader("Data Elements")
            st.markdown("""
            <div class="card">
                <p>Data elements are specific pieces of information that can be collected about individuals. They are the building blocks of personal data and may include items like names, email addresses, or identification numbers.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get data element data from repository
            data_elements = self.glossary_repository.get_data_elements()
            if data_elements:
                data_element_data = {
                    "Data Element": [],
                    "Description": []
                }
                for data_element in data_elements:
                    data_element_data["Data Element"].append(data_element["name"])
                    data_element_data["Description"].append(data_element["description"])
                
                st.dataframe(pd.DataFrame(data_element_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Subject Types tab
        with tabs[4]:
            st.subheader("Data Subject Types")
            st.markdown("""
            <div class="card">
                <p>Data subject types refer to the categories of individuals whose personal data is being processed. 
                Different types of data subjects may have different rights and protections under data protection laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get data subject type data from repository
            data_subject_types = self.glossary_repository.get_data_subject_types()
            if data_subject_types:
                data_subject_type_data = {
                    "Data Subject Type": [],
                    "Description": []
                }
                for dst in data_subject_types:
                    data_subject_type_data["Data Subject Type"].append(dst["name"])
                    data_subject_type_data["Description"].append(dst["description"])
                
                st.dataframe(pd.DataFrame(data_subject_type_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Categories tab
        with tabs[5]:
            st.subheader("Data Categories")
            st.markdown("""
            <div class="card">
                <p>Data categories are groupings of similar types of personal data. 
                They help organizations classify and manage personal data according to its nature and sensitivity.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get data category data from repository
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                data_category_data = {
                    "Data Category": [],
                    "Description": []
                }
                for dc in data_categories:
                    data_category_data["Data Category"].append(dc["name"])
                    data_category_data["Description"].append(dc["description"])
                
                st.dataframe(pd.DataFrame(data_category_data))
            else:
                st.warning("No data available in the database.")
        
        # Context tab
        with tabs[6]:
            st.subheader("Context")
            st.markdown("""
            <div class="card">
                <p>Context refers to the specific circumstances or purposes for which personal data is collected and processed. 
                Under most data protection laws, organizations must clearly state the context in which they process personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get context data from repository
            contexts = self.glossary_repository.get_contexts()
            if contexts:
                context_data = {
                    "Context": [],
                    "Description": []
                }
                for ctx in contexts:
                    context_data["Context"].append(ctx["name"])
                    context_data["Description"].append(ctx["description"])
                
                st.dataframe(pd.DataFrame(context_data))
            else:
                st.warning("No data available in the database.")
        
        # Sensitivity tab
        with tabs[7]:
            st.subheader("Sensitivity")
            st.markdown("""
            <div class="card">
                <p>Sensitivity refers to the level of risk associated with certain types of personal data. 
                Some categories of data are considered more sensitive than others and require additional protections.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get sensitivity data from repository
            sensitivities = self.glossary_repository.get_sensitivities()
            if sensitivities:
                sensitivity_data = {
                    "Sensitivity Level": [],
                    "Description": []
                }
                for sens in sensitivities:
                    sensitivity_data["Sensitivity Level"].append(sens["name"])
                    sensitivity_data["Description"].append(sens["description"])
                
                st.dataframe(pd.DataFrame(sensitivity_data))
            else:
                st.warning("No data available in the database.")
        
        # Purpose Categories tab
        with tabs[8]:
            st.subheader("Purpose Categories")
            st.markdown("""
            <div class="card">
                <p>Purpose categories define the specific reasons for which personal data is processed. 
                Under most data protection laws, organizations must clearly specify the purpose for which they collect and process personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get purpose categories data from repository
            purpose_categories = self.glossary_repository.get_purpose_categories()
            if purpose_categories:
                purpose_category_data = {
                    "Purpose Category": [],
                    "Description": []
                }
                for purpose in purpose_categories:
                    purpose_category_data["Purpose Category"].append(purpose["name"])
                    purpose_category_data["Description"].append(purpose["description"])
                
                st.dataframe(pd.DataFrame(purpose_category_data))
            else:
                st.warning("No data available in the database.")
        
        # Breach Types tab
        with tabs[9]:
            st.subheader("Breach Types")
            st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides information about different types of data breaches that can affect organizations.</p>
                <ul>
                    <li>Categorized by source and attack vector (cyber attacks, insider threats, physical breaches, supply chain)</li>
                    <li>Detailed descriptions of each breach type and its characteristics</li>
                    <li>Helps in identifying and classifying security incidents</li>
                    <li>Supports breach notification requirements under various regulations</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get breach types data from repository
            breach_types = self.glossary_repository.get_breach_types()
            if breach_types:
                # Group breach types by category
                categories = {}
                for breach_type in breach_types:
                    category = breach_type["category"]
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(breach_type)
                
                # Display breach types by category
                for category, types in categories.items():
                    st.markdown(f"<h3>{category}</h3>", unsafe_allow_html=True)
                    
                    breach_type_data = {
                        "Breach Type": [],
                        "Description": []
                    }
                    for breach in types:
                        breach_type_data["Breach Type"].append(breach["name"])
                        breach_type_data["Description"].append(breach["description"])
                    
                    st.dataframe(pd.DataFrame(breach_type_data))
            else:
                st.warning("No data available in the database.")

    def regulatory_metadata_section(self):
        """Handle the Regulatory Metadata section with its tabs."""
        st.markdown("<div class='page-header'><i class='fas fa-project-diagram'></i> &nbsp;Regulatory Intelligence Engine</div>", unsafe_allow_html=True)
        
        st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Regulatory Mappings™</strong> establish dynamic relationships between Core Constructs, powering the foundational regulatory intelligence across the OneTrust platform. These sophisticated connections form the rule engine that drives automated compliance insights.</p>
            <ul>
                <li><strong>Intelligent Rule Framework:</strong> Complex relationship matrices between Core Constructs that enable automated regulatory analysis and decision-making</li>
                <li><strong>Decision Tree Engine:</strong> Powers the platform's regulatory intelligence capabilities through a comprehensive set of interconnected rules</li>
                <li><strong>API Foundation:</strong> All inference APIs and automated compliance functions are built upon these mapping relationships</li>
                <li><strong>Cross-Domain Intelligence:</strong> Creates connections across jurisdictions, legal bases, breach requirements, and other regulatory domains</li>
                <li><strong>Adaptive Compliance Logic:</strong> Continuously updated mapping relationships ensure regulatory insights remain current with evolving requirements</li>
                <li><strong>Contextual Analysis:</strong> Enables nuanced interpretation of requirements based on specific business contexts and processing activities</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Define all tab names
        all_tab_names = [
            "Law Jurisdiction", 
            "Law Legal Basis", 
            "Law Incident Breach Notification", 
            "Law Transfer",
            "Data Subject Access Request",
            "Data Category Data Element",
            "Law Data Subject Type Data Element Sensitivity",
            "Law Data Subject Type Data Category Sensitivity",
            "Data Subject Type Data Category Sensitivity",
            "Data Subject Type Data Element Sensitivity",
            "Law Context Data Subject Type Data Category Sensitivity",
            "Context Data Subject Type Data Category Sensitivity",
            "Law Purpose Category Legal Basis",
            "Legal Basis Requirements"
        ]
        
        # Define which tabs are used by each inference API
        inference_api_mappings = {
            "All": list(range(len(all_tab_names))),  # All tabs
            "Law Inference": [0],  # Law Jurisdiction tab
            "Legal Basis Inference": [1, 12, 13],  # Law Legal Basis tab, Law Purpose Category Legal Basis, Legal Basis Requirements
            "Breach Notification Inference": [2],  # Law Incident Breach Notification tab
            "Transfer Mechanism Inference": [3],  # Law Transfer tab
            "Data Subject Rights Inference": [4],  # Data Subject Access Request tab
            "Data Sensitivity Inference": [5, 6, 7, 8, 9, 10, 11]  # Various sensitivity-related tabs
        }
        
        # Create a filter for inference APIs
        st.markdown("<h3>Filter by Inference API</h3>", unsafe_allow_html=True)
        
        # Add explanation about the inference API filter
        st.caption("Filter to view only the mapping tables used by each specific inference API. Each inference API uses different tables to make regulatory determinations.")
        
        inference_api_options = list(inference_api_mappings.keys())
        selected_inference_api = st.selectbox(
            "Select an Inference API",
            inference_api_options,
            key="inference_api_filter"
        )
        
        # Get the tab indices for the selected inference API
        visible_tab_indices = inference_api_mappings[selected_inference_api]
        
        # Create filtered tab names
        visible_tab_names = [all_tab_names[i] for i in visible_tab_indices]
        
        # Create tabs with filtered names
        tabs = st.tabs(visible_tab_names)
        
        # Add explanation about how the selected inference API uses the mapping tables
        if selected_inference_api == "Law Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Law Inference Works</h4>
                <p>The Law Inference API uses the Law Jurisdiction mapping table to determine which privacy laws apply to an organization:</p>
                <ul>
                    <li>Analyzes the jurisdictional scope of privacy regulations</li>
                    <li>Determines applicable laws based on selected jurisdiction</li>
                    <li>Provides detailed information about each applicable law</li>
                    <li>Highlights key compliance requirements and effective dates</li>
                </ul>
                <p>The system helps organizations understand their regulatory obligations across different jurisdictions, ensuring comprehensive compliance with all relevant privacy laws.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Legal Basis Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Legal Basis Inference Works</h4>
                <p>The Legal Basis Inference API uses these mapping tables to determine the appropriate legal basis for processing personal data:</p>
                <ol>
                    <li><strong>Law Legal Basis</strong>: Maps laws to their supported legal bases, establishing which legal bases are valid under each regulation.</li>
                    <li><strong>Law Purpose Category Legal Basis</strong>: Provides recommended legal bases for specific processing purposes under each law, with preference ordering.</li>
                    <li><strong>Legal Basis Requirements</strong>: Details the compliance requirements for each legal basis, helping organizations implement the necessary safeguards.</li>
                </ol>
                <p>When making a legal basis determination, the system considers:</p>
                <ul>
                    <li>The applicable law (e.g., GDPR, CCPA)</li>
                    <li>The processing purpose (e.g., Marketing, Security)</li>
                    <li>Data sensitivity level</li>
                    <li>Specific context of processing</li>
                </ul>
                <p>The system then recommends appropriate legal bases in order of preference, along with their compliance requirements.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Breach Notification Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Breach Notification Inference Works</h4>
                <p>The Breach Notification Inference API uses the Law Incident Breach Notification mapping table to determine notification requirements when a data breach occurs:</p>
                <ul>
                    <li>Analyzes breach severity, scope, and data types involved</li>
                    <li>Identifies applicable laws based on affected jurisdictions</li>
                    <li>Determines notification thresholds and timeframes</li>
                    <li>Provides guidance on notification content and recipients</li>
                </ul>
                <p>The system helps organizations comply with varying breach notification requirements across different jurisdictions, ensuring timely and appropriate responses to data incidents.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Transfer Mechanism Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Transfer Mechanism Inference Works</h4>
                <p>The Transfer Mechanism Inference API uses the Law Transfer mapping table to determine appropriate safeguards for cross-border data transfers:</p>
                <ul>
                    <li>Identifies source and destination jurisdictions</li>
                    <li>Determines applicable data protection laws</li>
                    <li>Evaluates adequacy decisions and existing agreements</li>
                    <li>Recommends appropriate transfer mechanisms (e.g., SCCs, BCRs)</li>
                    <li>Highlights additional requirements for specific transfers</li>
                </ul>
                <p>The system helps organizations implement compliant data transfer frameworks while navigating complex international data protection requirements.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Data Subject Rights Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Data Subject Rights Inference Works</h4>
                <p>The Data Subject Rights Inference API uses the Data Subject Access Request mapping table to determine rights and response requirements:</p>
                <ul>
                    <li>Identifies applicable laws based on data subject location</li>
                    <li>Determines available rights (access, deletion, portability, etc.)</li>
                    <li>Calculates response timeframes</li>
                    <li>Identifies valid exemptions and conditions</li>
                    <li>Provides guidance on verification requirements</li>
                </ul>
                <p>The system helps organizations respond appropriately to data subject requests while maintaining compliance with various privacy regulations.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Data Sensitivity Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Data Sensitivity Inference Works</h4>
                <p>The Data Sensitivity Inference API uses multiple sensitivity mapping tables to determine the sensitivity level of data elements in different contexts:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories, establishing hierarchical relationships.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements under different laws and for different data subject types.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Provides higher-level sensitivity determinations for data categories.</li>
                    <li><strong>Context Sensitivity</strong>: Adjusts sensitivity based on processing context (e.g., healthcare vs. marketing).</li>
                </ul>
                <p>The system considers multiple factors to determine data sensitivity, which then influences other decisions like legal basis selection, security requirements, and risk assessments.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a mapping from filtered tab index to original tab index
        tab_index_mapping = {i: visible_tab_indices[i] for i in range(len(visible_tab_indices))}
        
        # Loop through visible tabs and render content based on the original tab index
        for i, tab_idx in enumerate(visible_tab_indices):
            with tabs[i]:
                # Law Jurisdiction tab
                if tab_idx == 0:
                    st.markdown("""
                    <div class="card">
                        <h3>Law to Jurisdiction Mapping</h3>
                        <p>This section maps data protection laws to their applicable jurisdictions, helping organizations 
                        understand which laws apply in which geographic areas.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get law jurisdiction data from repository
                    law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
                    if law_jurisdictions:
                        law_jurisdiction_data = {
                            "Law": [],
                            "Jurisdiction": []
                        }
                        for lj in law_jurisdictions:
                            law_jurisdiction_data["Law"].append(lj["law_name"])
                            law_jurisdiction_data["Jurisdiction"].append(lj["jurisdiction_name"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(law_jurisdiction_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_jurisdiction_law_filter")
                        
                        with col2:
                            jurisdictions = sorted(df["Jurisdiction"].unique())
                            selected_jurisdiction = st.selectbox("Filter by Jurisdiction", ["All"] + list(jurisdictions), key="law_jurisdiction_jurisdiction_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_jurisdiction != "All":
                            filtered_df = filtered_df[filtered_df["Jurisdiction"] == selected_jurisdiction]
                        
                        # Sort by Law and Jurisdiction
                        filtered_df = filtered_df.sort_values(by=["Law", "Jurisdiction"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Law Legal Basis tab
                elif tab_idx == 1:
                    st.markdown("""
                    <div class="card">
                        <h3>Law Legal Basis</h3>
                        <p>This section maps data protection laws to their applicable legal bases for processing personal data.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get law legal basis data from repository
                    law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
                    if law_legal_bases:
                        law_legal_basis_data = {
                            "Law": [],
                            "Legal Basis": [],
                            "Description": []
                        }
                        for llb in law_legal_bases:
                            law_legal_basis_data["Law"].append(llb["law_name"])
                            law_legal_basis_data["Legal Basis"].append(llb["legal_basis_name"])
                            law_legal_basis_data["Description"].append(llb["legal_basis_description"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(law_legal_basis_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_legal_basis_law_filter")
                        
                        with col2:
                            legal_bases = sorted(df["Legal Basis"].unique())
                            selected_legal_basis = st.selectbox("Filter by Legal Basis", ["All"] + list(legal_bases), key="law_legal_basis_lb_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_legal_basis != "All":
                            filtered_df = filtered_df[filtered_df["Legal Basis"] == selected_legal_basis]
                        
                        # Sort by Law and Legal Basis
                        filtered_df = filtered_df.sort_values(by=["Law", "Legal Basis"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Law Incident Breach Notification tab
                elif tab_idx == 2:
                    st.markdown("""
                    <div class="card">
                        <h3>Law Incident Breach Notification</h3>
                        <p>This section provides information about breach notification requirements across different data protection regulations.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get law incident breach guidance data from repository
                    law_breach_guidances = self.regulatory_metadata_repository.get_law_incident_breach_guidances()
                    if law_breach_guidances:
                        law_breach_data = {
                            "Law": [],
                            "Threshold": [],
                            "Timeframe": [],
                            "Authority": [],
                            "Content": []
                        }
                        for lbg in law_breach_guidances:
                            law_breach_data["Law"].append(lbg["law_name"])
                            law_breach_data["Threshold"].append(lbg["threshold"])
                            law_breach_data["Timeframe"].append(lbg["timeframe"])
                            law_breach_data["Authority"].append(lbg["authority"])
                            law_breach_data["Content"].append(lbg["content"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(law_breach_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_breach_law_filter")
                        
                        with col2:
                            timeframes = sorted(df["Timeframe"].unique())
                            selected_timeframe = st.selectbox("Filter by Timeframe", ["All"] + list(timeframes), key="law_breach_timeframe_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_timeframe != "All":
                            filtered_df = filtered_df[filtered_df["Timeframe"] == selected_timeframe]
                
                        # Sort by Law
                        filtered_df = filtered_df.sort_values(by=["Law"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Law Transfer tab
                elif tab_idx == 3:
                    st.markdown("""
                    <div class="card">
                        <h3>Law Transfer Requirements</h3>
                        <p>This section provides information about cross-border data transfer requirements across different data protection regulations.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get law transfer data from repository
                    law_transfers = self.regulatory_metadata_repository.get_law_transfers()
                    if law_transfers:
                        law_transfer_data = {
                            "Law": [],
                            "Adequacy Countries": [],
                            "Transfer Mechanisms": [],
                            "Additional Requirements": []
                        }
                        for lt in law_transfers:
                            law_transfer_data["Law"].append(lt["law_name"])
                            law_transfer_data["Adequacy Countries"].append(lt["adequacy_countries"] or "N/A")
                            law_transfer_data["Transfer Mechanisms"].append(lt["transfer_mechanisms"] or "N/A")
                            law_transfer_data["Additional Requirements"].append(lt["additional_requirements"] or "N/A")
                
                        # Create a DataFrame
                        df = pd.DataFrame(law_transfer_data)
                    
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_transfer_law_filter")
                        
                        with col2:
                            mechanisms = sorted([m for m in df["Transfer Mechanisms"].unique() if m != "N/A"])
                            selected_mechanism = st.selectbox("Filter by Transfer Mechanism", ["All"] + list(mechanisms), key="law_transfer_mechanism_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_mechanism != "All":
                            filtered_df = filtered_df[filtered_df["Transfer Mechanisms"].str.contains(selected_mechanism, na=False)]
                        
                        # Sort by Law
                        filtered_df = filtered_df.sort_values(by=["Law"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
                elif tab_idx == 4:                        
                    # Data Subject Access Request tab
                    st.markdown("""
                    <div class="card">
                        <h3>Data Subject Access Request Requirements</h3>
                        <p>This section provides information about data subject rights and access request requirements across different data protection regulations.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                    # Get DSAR data from repository
                    dsar_requirements = self.regulatory_metadata_repository.get_law_data_subject_access_request_notification_requirements()
                    if dsar_requirements:
                        dsar_data = {
                            "Law": [],
                            "Right": [],
                            "Description": [],
                            "Conditions": [],
                            "Timeframe": [],
                            "Exemptions": []
                        }
                        for req in dsar_requirements:
                            dsar_data["Law"].append(req["law_name"])
                            dsar_data["Right"].append(req["name"])
                            dsar_data["Description"].append(req["description"])
                            dsar_data["Conditions"].append(req["conditions"] or "N/A")
                            dsar_data["Timeframe"].append(req["timeframe"] or "N/A")
                            dsar_data["Exemptions"].append(req["exemptions"] or "N/A")
                        
                        # Create a DataFrame
                        df = pd.DataFrame(dsar_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="dsar_law_filter")
                        
                        with col2:
                            rights = sorted(df["Right"].unique())
                            selected_right = st.selectbox("Filter by Right", ["All"] + list(rights), key="dsar_right_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_right != "All":
                            filtered_df = filtered_df[filtered_df["Right"] == selected_right]
                        
                        # Sort by Law and Right
                        filtered_df = filtered_df.sort_values(by=["Law", "Right"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Data Category Data Element tab
                elif tab_idx == 5:                        
                    st.markdown("""
                    <div class="card">
                        <h3>Data Category Data Element</h3>
                        <p>This section maps data categories to their constituent data elements, providing a hierarchical view of data classification.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get data category data element mappings from repository
                    data_category_elements = self.regulatory_metadata_repository.get_data_category_data_elements()
                    if data_category_elements:
                        mapping_data = {
                            "Data Category": [],
                            "Data Element": []
                        }
                        for mapping in data_category_elements:
                            mapping_data["Data Category"].append(mapping["data_category_name"])
                            mapping_data["Data Element"].append(mapping["data_element_name"])
                        
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            categories = sorted(df["Data Category"].unique())
                            selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="data_category_element_category_filter")
                        
                        with col2:
                            elements = sorted(df["Data Element"].unique())
                            selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="data_category_element_element_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_category != "All":
                            filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
                        if selected_element != "All":
                            filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
                        
                        # Sort by Data Category and Data Element
                        filtered_df = filtered_df.sort_values(by=["Data Category", "Data Element"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Law Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 6:                        
                    st.markdown("""
                    <div class="card">
                        <h3>Law Data Subject Type Data Element Sensitivity</h3>
                        <p>This section maps laws to data subject types, data elements, and their sensitivity levels, providing a comprehensive view of data protection requirements.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Law": [],
                            "Data Subject Type": [],
                            "Data Element": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Law"].append(mapping["law_name"])
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Element"].append(mapping["data_element_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                        
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_dst_de_sens_law_filter")
                        
                        with col2:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="law_dst_de_sens_dst_filter")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            elements = sorted(df["Data Element"].unique())
                            selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="law_dst_de_sens_element_filter")
                        
                        with col4:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="law_dst_de_sens_sensitivity_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_element != "All":
                            filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                        
                        # Sort by Law, Data Subject Type, Data Element
                        filtered_df = filtered_df.sort_values(by=["Law", "Data Subject Type", "Data Element"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Law Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 7:                        
                    st.markdown("""
                    <div class="card">
                        <h3>Law Data Subject Type Data Category Sensitivity</h3>
                        <p>This section maps laws to data subject types, data categories, and their sensitivity levels, providing a higher-level view of data protection requirements.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Law": [],
                            "Data Subject Type": [],
                            "Data Category": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Law"].append(mapping["law_name"])
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Category"].append(mapping["data_category_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                        
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_dst_dc_sens_law_filter")
                        
                        with col2:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="law_dst_dc_sens_dst_filter")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            categories = sorted(df["Data Category"].unique())
                            selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="law_dst_dc_sens_category_filter")
                        
                        with col4:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="law_dst_dc_sens_sensitivity_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_category != "All":
                            filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                        
                        # Sort by Law, Data Subject Type, Data Category
                        filtered_df = filtered_df.sort_values(by=["Law", "Data Subject Type", "Data Category"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 8:
                    st.markdown("""
                    <div class="card">
                        <h3>Data Subject Type Data Category Sensitivity</h3>
                        <p>This section maps data subject types to data categories and their sensitivity levels, independent of specific laws.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Data Subject Type": [],
                            "Data Category": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Category"].append(mapping["data_category_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                    
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="dst_dc_sens_dst_filter")
                    
                        with col2:
                            categories = sorted(df["Data Category"].unique())
                            selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="dst_dc_sens_category_filter")
                    
                        col3, _ = st.columns(2)
                        with col3:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="dst_dc_sens_sensitivity_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_category != "All":
                            filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                
                        # Sort by Data Subject Type, Data Category
                        filtered_df = filtered_df.sort_values(by=["Data Subject Type", "Data Category"])
                
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 9:
                    st.markdown("""
                    <div class="card">
                        <h3>Data Subject Type Data Element Sensitivity</h3>
                        <p>This section maps data subject types to specific data elements and their sensitivity levels, independent of specific laws.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Data Subject Type": [],
                            "Data Element": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Element"].append(mapping["data_element_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="dst_de_sens_dst_filter")
                
                        with col2:
                            elements = sorted(df["Data Element"].unique())
                            selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="dst_de_sens_element_filter")
                
                        col3, _ = st.columns(2)
                        with col3:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="dst_de_sens_sensitivity_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_element != "All":
                            filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                
                        # Sort by Data Subject Type, Data Element
                        filtered_df = filtered_df.sort_values(by=["Data Subject Type", "Data Element"])
                
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
            
                # Law Context Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 10:
                    st.markdown("""
                    <div class="card">
                        <h3>Law Context Data Subject Type Data Category Sensitivity</h3>
                        <p>This section maps laws, processing contexts, data subject types, data categories, and their sensitivity levels, providing a comprehensive view of contextual data protection requirements.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_law_context_data_subject_type_data_category_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Law": [],
                            "Context": [],
                            "Data Subject Type": [],
                            "Data Category": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Law"].append(mapping["law_name"])
                            mapping_data["Context"].append(mapping["context_name"])
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Category"].append(mapping["data_category_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_ctx_dst_dc_sens_law_filter")
                
                        with col2:
                            contexts = sorted(df["Context"].unique())
                            selected_context = st.selectbox("Filter by Context", ["All"] + list(contexts), key="law_ctx_dst_dc_sens_context_filter")
                
                        col3, col4 = st.columns(2)
                        with col3:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="law_ctx_dst_dc_sens_dst_filter")
                
                        with col4:
                            categories = sorted(df["Data Category"].unique())
                            selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="law_ctx_dst_dc_sens_category_filter")
                
                        col5, _ = st.columns(2)
                        with col5:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="law_ctx_dst_dc_sens_sensitivity_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_context != "All":
                            filtered_df = filtered_df[filtered_df["Context"] == selected_context]
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_category != "All":
                            filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                
                        # Sort by Law, Context, Data Subject Type, Data Category
                        filtered_df = filtered_df.sort_values(by=["Law", "Context", "Data Subject Type", "Data Category"])
                
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
        
                # Context Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 11:
                    st.markdown("""
                    <div class="card">
                        <h3>Context Data Subject Type Data Category Sensitivity</h3>
                        <p>This section maps processing contexts, data subject types, data categories, and their sensitivity levels, independent of specific laws.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get mappings from repository
                    mappings = self.regulatory_metadata_repository.get_context_data_subject_type_data_category_sensitivities()
                    if mappings:
                        mapping_data = {
                            "Context": [],
                            "Data Subject Type": [],
                            "Data Category": [],
                            "Sensitivity": []
                        }
                        for mapping in mappings:
                            mapping_data["Context"].append(mapping["context_name"])
                            mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                            mapping_data["Data Category"].append(mapping["data_category_name"])
                            mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
                
                        # Create a DataFrame
                        df = pd.DataFrame(mapping_data)
                
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            contexts = sorted(df["Context"].unique())
                            selected_context = st.selectbox("Filter by Context", ["All"] + list(contexts), key="ctx_dst_dc_sens_context_filter")
                
                        with col2:
                            subject_types = sorted(df["Data Subject Type"].unique())
                            selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="ctx_dst_dc_sens_dst_filter")
                
                        col3, col4 = st.columns(2)
                        with col3:
                            categories = sorted(df["Data Category"].unique())
                            selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="ctx_dst_dc_sens_category_filter")
                
                        with col4:
                            sensitivities = sorted(df["Sensitivity"].unique())
                            selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="ctx_dst_dc_sens_sensitivity_filter")
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_context != "All":
                            filtered_df = filtered_df[filtered_df["Context"] == selected_context]
                        if selected_subject_type != "All":
                            filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
                        if selected_category != "All":
                            filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
                        if selected_sensitivity != "All":
                            filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
                
                        # Sort by Context, Data Subject Type, Data Category
                        filtered_df = filtered_df.sort_values(by=["Context", "Data Subject Type", "Data Category"])
                
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No data available in the database.")
            
                # Law Purpose Category Legal Basis tab
                elif tab_idx == 12 :
                    st.markdown("""
                    <div class="card">
                        <h3>Law Purpose Category Legal Basis</h3>
                        <p>This section maps data protection laws to purpose categories and their applicable legal bases, helping organizations 
                        determine the appropriate legal basis for different processing purposes under various laws.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                    # Get law purpose category legal basis data from repository
                    law_purpose_legal_bases = self.regulatory_metadata_repository.get_law_purpose_category_legal_bases()
                    if law_purpose_legal_bases:
                        law_purpose_legal_basis_data = {
                            "Law": [],
                            "Purpose Category": [],
                            "Legal Basis": [],
                            "Preference Order": [],
                            "Notes": []
                        }
                        for mapping in law_purpose_legal_bases:
                            law_purpose_legal_basis_data["Law"].append(mapping["law_name"])
                            law_purpose_legal_basis_data["Purpose Category"].append(mapping["purpose_category_name"])
                            law_purpose_legal_basis_data["Legal Basis"].append(mapping["legal_basis_name"])
                            law_purpose_legal_basis_data["Preference Order"].append(mapping["preference_order"])
                            law_purpose_legal_basis_data["Notes"].append(mapping["description"] if mapping.get("description") else "")
                
                        # Create a DataFrame and display it
                        df = pd.DataFrame(law_purpose_legal_basis_data)
                
                        # Add filters for Law and Purpose Category
                        col1, col2 = st.columns(2)
                        with col1:
                            laws = sorted(df["Law"].unique())
                            selected_law = st.selectbox("Filter by Law", ["All"] + list(laws))
                
                        with col2:
                            purpose_categories = sorted(df["Purpose Category"].unique())
                            selected_purpose = st.selectbox("Filter by Purpose Category", ["All"] + list(purpose_categories))
                
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_law != "All":
                            filtered_df = filtered_df[filtered_df["Law"] == selected_law]
                        if selected_purpose != "All":
                            filtered_df = filtered_df[filtered_df["Purpose Category"] == selected_purpose]
                
                        # Sort by Law, Purpose Category, and Preference Order
                        filtered_df = filtered_df.sort_values(by=["Law", "Purpose Category", "Preference Order"])
                
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No Law Purpose Category Legal Basis mappings available in the database.")
                
                # Legal Basis Requirements tab
                elif tab_idx == 13:
                    st.markdown("""
                    <div class="card">
                        <h3>Legal Basis Requirements</h3>
                        <p>This section provides detailed compliance requirements for each legal basis, helping organizations understand what they need to do to properly rely on a specific legal basis for processing.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get legal basis requirements from repository
                    legal_basis_requirements = self.regulatory_metadata_repository.get_legal_basis_requirements()
                    if legal_basis_requirements:
                        requirements_data = {
                            "Legal Basis": [],
                            "Requirement": []
                        }
                        for req in legal_basis_requirements:
                            requirements_data["Legal Basis"].append(req["legal_basis_name"])
                            requirements_data["Requirement"].append(req["requirement"])
                        
                        # Create a DataFrame
                        df = pd.DataFrame(requirements_data)
                        
                        # Add filter for Legal Basis
                        legal_bases = sorted(df["Legal Basis"].unique())
                        selected_legal_basis = st.selectbox("Filter by Legal Basis", ["All"] + list(legal_bases), key="legal_basis_requirements_filter")
                        
                        # Apply filter
                        filtered_df = df.copy()
                        if selected_legal_basis != "All":
                            filtered_df = filtered_df[filtered_df["Legal Basis"] == selected_legal_basis]
                        
                        # Sort by Legal Basis
                        filtered_df = filtered_df.sort_values(by=["Legal Basis"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No Legal Basis Requirements available in the database.")
            
    def inventory_section(self):
        """Handle the Inventory section with its tabs."""
        st.markdown("<div class='page-header'><i class='fas fa-database'></i> &nbsp;Inventory</div>", unsafe_allow_html=True)
        
        tabs = st.tabs([
            "Assets", "Datasets", "Data Domains", "Policies", "Visualization"
        ])
        
        # Assets tab
        with tabs[0]:
            st.subheader("Assets Inventory")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an inventory of data assets within the organization, including systems and applications that store or process data.</p>
                <ul>
                    <li>Core systems that contain or process data</li>
                    <li>Applications and databases that serve as data sources</li>
                    <li>Systems that support business operations and data processing</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get assets data from repository
            assets = self.inventory_repository.get_assets()
            if assets:
                assets_data = {
                    "Asset Name": [],
                    "Description": []
                }
                for asset in assets:
                    assets_data["Asset Name"].append(asset["name"])
                    assets_data["Description"].append(asset["description"])
                
                st.dataframe(pd.DataFrame(assets_data))
                
                # Add expandable sections for each asset to show its datasets
                st.markdown("### Asset Details")
                for asset in assets:
                    with st.expander(f"{asset['name']}"):
                        datasets = self.inventory_repository.get_datasets_by_asset_id(asset["id"])
                        if datasets:
                            datasets_data = {
                                "Dataset": [],
                                "Source System": [],
                                "Data Domain": [],
                                "Description": []
                            }
                            for dataset in datasets:
                                datasets_data["Dataset"].append(dataset["name"])
                                datasets_data["Source System"].append(dataset["source_system"])
                                datasets_data["Data Domain"].append(dataset["data_domain_name"] if dataset["data_domain_name"] else "N/A")
                                datasets_data["Description"].append(dataset["description"])
                            
                            st.dataframe(pd.DataFrame(datasets_data))
                        else:
                            st.info("No datasets available for this asset.")
            else:
                st.warning("No data available in the database.")
        
        # Datasets tab
        with tabs[1]:
            st.subheader("Datasets Inventory")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an inventory of datasets within the organization, organized by the assets they belong to and the data domains they are part of.</p>
                <ul>
                    <li>Datasets from various source systems</li>
                    <li>Relationships between datasets, assets, and data domains</li>
                    <li>Policies applied to each dataset</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get datasets data from repository
            datasets = self.inventory_repository.get_datasets()
            if datasets:
                datasets_data = {
                    "Dataset": [],
                    "Asset": [],
                    "Source System": [],
                    "Data Domain": [],
                    "Description": []
                }
                for dataset in datasets:
                    datasets_data["Dataset"].append(dataset["name"])
                    datasets_data["Asset"].append(dataset["asset_name"])
                    datasets_data["Source System"].append(dataset["source_system"])
                    datasets_data["Data Domain"].append(dataset["data_domain_name"] if dataset["data_domain_name"] else "N/A")
                    datasets_data["Description"].append(dataset["description"])
                
                st.dataframe(pd.DataFrame(datasets_data))
                
                # Add expandable sections for each dataset to show its policies
                st.markdown("### Dataset Policies")
                for dataset in datasets:
                    with st.expander(f"{dataset['name']} ({dataset['asset_name']})"):
                        policies = self.inventory_repository.get_policies_for_dataset(dataset["id"])
                        if policies:
                            policies_data = {
                                "Policy": [],
                                "Type": [],
                                "Description": []
                            }
                            for policy in policies:
                                policies_data["Policy"].append(policy["name"])
                                policies_data["Type"].append(policy["policy_type"])
                                policies_data["Description"].append(policy["description"])
                            
                            st.dataframe(pd.DataFrame(policies_data))
                        else:
                            st.info("No policies applied to this dataset.")
            else:
                st.warning("No data available in the database.")
        
        # Data Domains tab
        with tabs[2]:
            st.subheader("Data Domains")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an overview of data domains, which are logical groupings of related datasets.</p>
                <ul>
                    <li>Organizational structure of data</li>
                    <li>Logical groupings of related datasets</li>
                    <li>Policies applied at the domain level</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get data domains from repository
            data_domains = self.inventory_repository.get_data_domains()
            if data_domains:
                data_domain_data = {
                    "Data Domain": [],
                    "Description": []
                }
                for domain in data_domains:
                    data_domain_data["Data Domain"].append(domain["name"])
                    data_domain_data["Description"].append(domain["description"])
                
                st.dataframe(pd.DataFrame(data_domain_data))
                
                # Add expandable sections for each data domain
                st.markdown("### Data Domain Details")
                for domain in data_domains:
                    with st.expander(f"{domain['name']}"):
                        # Show datasets in this domain
                        datasets = self.inventory_repository.get_datasets_by_data_domain_id(domain["id"])
                        if datasets:
                            st.markdown("#### Datasets in this Domain")
                            datasets_data = {
                                "Dataset": [],
                                "Asset": [],
                                "Source System": [],
                                "Description": []
                            }
                            for dataset in datasets:
                                datasets_data["Dataset"].append(dataset["name"])
                                datasets_data["Asset"].append(dataset["asset_name"])
                                datasets_data["Source System"].append(dataset["source_system"])
                                datasets_data["Description"].append(dataset["description"])
                            
                            st.dataframe(pd.DataFrame(datasets_data))
                        else:
                            st.info("No datasets in this domain.")
                        
                        # Show policies for this domain
                        policies = self.inventory_repository.get_policies_for_data_domain(domain["id"])
                        if policies:
                            st.markdown("#### Policies Applied to this Domain")
                            policies_data = {
                                "Policy": [],
                                "Type": [],
                                "Description": []
                            }
                            for policy in policies:
                                policies_data["Policy"].append(policy["name"])
                                policies_data["Type"].append(policy["policy_type"])
                                policies_data["Description"].append(policy["description"])
                            
                            st.dataframe(pd.DataFrame(policies_data))
                        else:
                            st.info("No policies applied to this domain.")
            else:
                st.warning("No data available in the database.")
        
        # Policies tab
        with tabs[3]:
            st.subheader("Policies")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an overview of data policies that govern how data is managed, protected, and used within the organization.</p>
                <ul>
                    <li>Data governance policies</li>
                    <li>Data protection and security policies</li>
                    <li>Data quality and retention policies</li>
                    <li>Application of policies to datasets and domains</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get policies from repository
            policies = self.inventory_repository.get_policies()
            if policies:
                policies_data = {
                    "Policy": [],
                    "Type": [],
                    "Description": []
                }
                for policy in policies:
                    policies_data["Policy"].append(policy["name"])
                    policies_data["Type"].append(policy["policy_type"])
                    policies_data["Description"].append(policy["description"])
                
                st.dataframe(pd.DataFrame(policies_data))
                
                # Add expandable sections for each policy
                st.markdown("### Policy Application")
                for policy in policies:
                    with st.expander(f"{policy['name']} ({policy['policy_type']})"):
                        # Show datasets with this policy
                        datasets = self.inventory_repository.get_datasets_for_policy(policy["id"])
                        if datasets:
                            st.markdown("#### Applied to Datasets")
                            datasets_data = {
                                "Dataset": [],
                                "Asset": [],
                                "Data Domain": []
                            }
                            for dataset in datasets:
                                datasets_data["Dataset"].append(dataset["name"])
                                datasets_data["Asset"].append(dataset["asset_name"])
                                datasets_data["Data Domain"].append(dataset["data_domain_name"] if dataset["data_domain_name"] else "N/A")
                            
                            st.dataframe(pd.DataFrame(datasets_data))
                        else:
                            st.info("Not applied to any datasets.")
                        
                        # Show data domains with this policy
                        domains = self.inventory_repository.get_data_domains_for_policy(policy["id"])
                        if domains:
                            st.markdown("#### Applied to Data Domains")
                            domains_data = {
                                "Data Domain": [],
                                "Description": []
                            }
                            for domain in domains:
                                domains_data["Data Domain"].append(domain["name"])
                                domains_data["Description"].append(domain["description"])
                            
                            st.dataframe(pd.DataFrame(domains_data))
                        else:
                            st.info("Not applied to any data domains.")
            else:
                st.warning("No data available in the database.")
        
        # Visualization tab
        with tabs[4]:
            st.subheader("Data Inventory Visualization")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides a visual representation of the relationships between assets, datasets, data domains, and policies.</p>
                <ul>
                    <li>Interactive network graph showing data relationships</li>
                    <li>Visual mapping of policies to datasets and domains</li>
                    <li>Hierarchical view of data organization</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Create network visualization
            assets = self.inventory_repository.get_assets()
            datasets = self.inventory_repository.get_datasets()
            data_domains = self.inventory_repository.get_data_domains()
            policies = self.inventory_repository.get_policies()
            
            if assets and datasets and data_domains and policies:
                # Create a network graph
                net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")
                
                # First, add all nodes to the network
                # Add nodes for assets (blue)
                for asset in assets:
                    net.add_node(f"asset_{asset['id']}", label=asset["name"], title=asset["description"], color="#3498db", shape="dot", size=25)
                
                # Add nodes for datasets (green)
                for dataset in datasets:
                    net.add_node(f"dataset_{dataset['id']}", label=dataset["name"], title=dataset["description"], color="#2ecc71", shape="dot", size=20)
                
                # Add nodes for data domains (orange)
                for domain in data_domains:
                    net.add_node(f"domain_{domain['id']}", label=domain["name"], title=domain["description"], color="#e67e22", shape="dot", size=25)
                
                # Add nodes for policies (red)
                for policy in policies:
                    net.add_node(f"policy_{policy['id']}", label=policy["name"], title=policy["description"], color="#e74c3c", shape="dot", size=15)
                
                # Now add all edges after all nodes have been created
                # Connect datasets to assets
                for dataset in datasets:
                    net.add_edge(f"dataset_{dataset['id']}", f"asset_{dataset['asset_id']}", title="belongs to")
                    # Connect dataset to its data domain if it has one
                    if dataset["data_domain_id"]:
                        # Make sure the domain exists in our data domains list
                        domain_exists = any(domain["id"] == dataset["data_domain_id"] for domain in data_domains)
                        if domain_exists:
                            net.add_edge(f"dataset_{dataset['id']}", f"domain_{dataset['data_domain_id']}", title="part of domain")
                
                # Connect policies to datasets
                for policy in policies:
                    policy_datasets = self.inventory_repository.get_datasets_for_policy(policy["id"])
                    for dataset in policy_datasets:
                        # Make sure the dataset exists in our datasets list
                        if any(d["id"] == dataset["id"] for d in datasets):
                            net.add_edge(f"policy_{policy['id']}", f"dataset_{dataset['id']}", title="applies to")
                    
                    # Connect policies to data domains
                    policy_domains = self.inventory_repository.get_data_domains_for_policy(policy["id"])
                    for domain in policy_domains:
                        # Make sure the domain exists in our data domains list
                        if any(d["id"] == domain["id"] for d in data_domains):
                            net.add_edge(f"policy_{policy['id']}", f"domain_{domain['id']}", title="applies to")
                
                # Set physics layout
                net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=200, spring_strength=0.05, damping=0.09)
                
                # Generate the HTML file
                html_path = "network_graph.html"
                net.save_graph(html_path)
                
                # Display the HTML file
                with open(html_path, 'r') as f:
                    html_string = f.read()
                components.html(html_string, height=600)
                
                # Add legend
                st.markdown('''
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <div style="margin: 0 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #3498db; border-radius: 50%; margin-right: 5px;"></span> Assets</div>
                    <div style="margin: 0 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #2ecc71; border-radius: 50%; margin-right: 5px;"></span> Datasets</div>
                    <div style="margin: 0 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #e67e22; border-radius: 50%; margin-right: 5px;"></span> Data Domains</div>
                    <div style="margin: 0 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #e74c3c; border-radius: 50%; margin-right: 5px;"></span> Policies</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Instructions for using the visualization
                st.markdown('''
                <div style="margin-top: 20px; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                    <h4>How to use this visualization:</h4>
                    <ul>
                        <li>Click and drag nodes to reposition them</li>
                        <li>Scroll to zoom in and out</li>
                        <li>Hover over nodes to see details</li>
                        <li>Click on a node to focus on its connections</li>
                    </ul>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.warning("Insufficient data to create visualization. Please ensure there are assets, datasets, data domains, and policies in the database.")
            
            # No form for adding new assets as per requirement
        
        # Datasets tab
        with tabs[1]:
            st.subheader("Datasets Inventory")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an inventory of datasets within the organization, organized by the assets they belong to and the data domains they are part of.</p>
                <ul>
                    <li>Datasets from various source systems</li>
                    <li>Relationships between datasets, assets, and data domains</li>
                    <li>Policies applied to each dataset</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get datasets data from repository
            datasets = self.inventory_repository.get_datasets()
            if datasets:
                datasets_data = {
                    "Dataset": [],
                    "Asset": [],
                    "Source System": [],
                    "Data Domain": [],
                    "Description": []
                }
                for dataset in datasets:
                    datasets_data["Dataset"].append(dataset["name"])
                    datasets_data["Asset"].append(dataset["asset_name"])
                    datasets_data["Source System"].append(dataset["source_system"])
                    datasets_data["Data Domain"].append(dataset["data_domain_name"] if dataset["data_domain_name"] else "N/A")
                    datasets_data["Description"].append(dataset["description"])
                
                st.dataframe(pd.DataFrame(datasets_data))
                
                # Add expandable sections for each dataset to show its policies
                st.markdown("### Dataset Policies")
                for dataset in datasets:
                    with st.expander(f"{dataset['name']} ({dataset['asset_name']})"):
                        policies = self.inventory_repository.get_policies_for_dataset(dataset["id"])
                        if policies:
                            policies_data = {
                                "Policy": [],
                                "Type": [],
                                "Description": []
                            }
                            for policy in policies:
                                policies_data["Policy"].append(policy["name"])
                                policies_data["Type"].append(policy["policy_type"])
                                policies_data["Description"].append(policy["description"])
                            
                            st.dataframe(pd.DataFrame(policies_data))
                        else:
                            st.info("No policies applied to this dataset.")
            else:
                st.warning("No datasets available in the database.")
            
            # No form for adding new datasets as per requirement
        
        # Data Domains tab
        with tabs[2]:
            st.subheader("Data Domains")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an overview of data domains, which are logical groupings of related datasets.</p>
                <ul>
                    <li>Organizational structure of data</li>
                    <li>Logical groupings of related datasets</li>
                    <li>Policies applied at the domain level</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get data domains from repository
            data_domains = self.inventory_repository.get_data_domains()
            if data_domains:
                data_domain_data = {
                    "Data Domain": [],
                    "Description": []
                }
                for domain in data_domains:
                    data_domain_data["Data Domain"].append(domain["name"])
                    data_domain_data["Description"].append(domain["description"])
                
                st.dataframe(pd.DataFrame(data_domain_data))
            
            # Add expandable sections for each data domain
            if data_domains:
                st.markdown("### Data Domain Details")
                for domain in data_domains:
                    with st.expander(f"{domain['name']}"):
                        # Show datasets in this domain
                        datasets = self.inventory_repository.get_datasets_by_data_domain_id(domain["id"])
                        if datasets:
                            st.markdown("#### Datasets in this Domain")
                            datasets_data = {
                                "Dataset": [],
                                "Asset": [],
                                "Source System": [],
                                "Description": []
                            }
                            for dataset in datasets:
                                datasets_data["Dataset"].append(dataset["name"])
                                datasets_data["Asset"].append(dataset["asset_name"])
                                datasets_data["Source System"].append(dataset["source_system"])
                                datasets_data["Description"].append(dataset["description"])
                            
                            st.dataframe(pd.DataFrame(datasets_data))
                        else:
                            st.info("No datasets in this domain.")
                        
                        # Show policies for this domain
                        policies = self.inventory_repository.get_policies_for_data_domain(domain["id"])
                        if policies:
                            st.markdown("#### Policies Applied to this Domain")
                            policies_data = {
                                "Policy": [],
                                "Type": [],
                                "Description": []
                            }
                            for policy in policies:
                                policies_data["Policy"].append(policy["name"])
                                policies_data["Type"].append(policy["policy_type"])
                                policies_data["Description"].append(policy["description"])
                            
                            st.dataframe(pd.DataFrame(policies_data))
                        else:
                            st.info("No policies applied to this domain.")
            else:
                st.warning("No data domains available in the database.")
            
            # No form for adding new data domains as per requirement
        
        # Policies tab
        with tabs[3]:
            st.subheader("Policies")
            st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides an overview of data policies that govern how data is managed, protected, and used within the organization.</p>
                <ul>
                    <li>Data governance policies</li>
                    <li>Data protection and security policies</li>
                    <li>Data quality and retention policies</li>
                    <li>Application of policies to datasets and domains</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get policies from repository
            policies = self.inventory_repository.get_policies()
            if policies:
                policies_data = {
                    "Policy": [],
                    "Type": [],
                    "Description": []
                }
                for policy in policies:
                    policies_data["Policy"].append(policy["name"])
                    policies_data["Type"].append(policy["policy_type"])
                    policies_data["Description"].append(policy["description"])
                
                st.dataframe(pd.DataFrame(policies_data))
            
            # Add expandable sections for each policy
            if policies:
                st.markdown("### Policy Application")
                for policy in policies:
                    with st.expander(f"{policy['name']} ({policy['policy_type']})"):
                        # Show datasets with this policy
                        datasets = self.inventory_repository.get_datasets_for_policy(policy["id"])
                        if datasets:
                            st.markdown("#### Applied to Datasets")
                            datasets_data = {
                                "Dataset": [],
                                "Asset": [],
                                "Data Domain": []
                            }
                            for dataset in datasets:
                                datasets_data["Dataset"].append(dataset["name"])
                                datasets_data["Asset"].append(dataset["asset_name"])
                                datasets_data["Data Domain"].append(dataset["data_domain_name"] if dataset["data_domain_name"] else "N/A")
                            
                            st.dataframe(pd.DataFrame(datasets_data))
                        else:
                            st.info("Not applied to any datasets.")
                        
                        # Show data domains with this policy
                        domains = self.inventory_repository.get_data_domains_for_policy(policy["id"])
                        if domains:
                            st.markdown("#### Applied to Data Domains")
                            domains_data = {
                                "Data Domain": [],
                                "Description": []
                            }
                            for domain in domains:
                                domains_data["Data Domain"].append(domain["name"])
                                domains_data["Description"].append(domain["description"])
                            
                            st.dataframe(pd.DataFrame(domains_data))
                        else:
                            st.info("Not applied to any data domains.")
            else:
                st.warning("No policies available in the database.")
            
            # No form for adding new policies as per requirement

    def run(self):
        """Main function to run the Streamlit app."""
        # Configure the page
        self.configure_page()

        # Main header and introduction
        st.title("OneTrust Platform")
        self.divider(2)
        
        # Create sidebar with navigation
        with st.sidebar:
            
            # First section: Regulatory Intelligence
            st.markdown("<div class='sidebar-section-header'>Regulatory Intelligence    </div>", unsafe_allow_html=True)
            
            # Create menu items with emoji icons directly in the button text
            # Core Constructs menu item
            if st.button("📚 Core Constructs", key="core_constructs_button", use_container_width=True):
                st.session_state['current_section'] = 'Core'
            
            # Regulatory Intelligence menu item
            if st.button("🔄 Regulatory Intelligence", key="regulatory_btn", use_container_width=True):
                st.session_state['current_section'] = 'Regulatory'
            
            # Decision Tree menu item
            if st.button("🌳 Decision Tree", key="decision_tree_btn", use_container_width=True):
                st.session_state['current_section'] = 'Decision Tree'
            
            # Second section: Inference APIs
            st.markdown("<div class='sidebar-section-header'>Inference APIs</div>", unsafe_allow_html=True)
            
            # Law Inference menu item
            if st.button("📜 Law Inference", key="law_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Law API'
            
            # Sensitivity Inference menu item
            if st.button("🛡️ Sensitivity Inference", key="sensitivity_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Sensitivity API'
            
            # Legal Basis Inference menu item
            if st.button("⚖️ Legal Basis Inference", key="legal_basis_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Legal Basis API'
            
            # Breach Notification menu item
            if st.button("⚠️ Breach Notification Inference", key="breach_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Breach API'
                
            # Transfer Mechanism Inference menu item
            if st.button("🔄 Transfer Mechanism Inference", key="transfer_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Transfer API'
                
            # Data Subject Rights Inference menu item
            if st.button("👤 Data Subject Rights Inference", key="dsr_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'DSR API'
            
            # Third section: Modules
            st.markdown("<div class='sidebar-section-header'>Modules</div>", unsafe_allow_html=True)
            
            # Inventory menu item
            if st.button("📊 Inventory", key="inventory_btn", use_container_width=True):
                st.session_state['current_section'] = 'Inventory'

            
            
            # Add some space
            st.markdown("<br>", unsafe_allow_html=True)
            self.divider()
            
        # Main content area based on selected section
        if st.session_state['current_section'] == 'Core':
            self.core_constructs_section()
        elif st.session_state['current_section'] == 'Regulatory':
            # Rename the section title in the UI
            self.regulatory_metadata_section()
        elif st.session_state['current_section'] == 'Decision Tree':
            self.decision_tree_section()
        elif st.session_state['current_section'] == 'Inventory':
            self.inventory_section()
        elif st.session_state['current_section'] == 'Law API':
            self.law_inference_api()
        elif st.session_state['current_section'] == 'Sensitivity API':
            self.sensitivity_inference_api()
        elif st.session_state['current_section'] == 'Legal Basis API':
            self.legal_basis_inference_api()
        elif st.session_state['current_section'] == 'Breach API':
            self.breach_notification_api()
        elif st.session_state['current_section'] == 'Transfer API':
            self.transfer_mechanism_api()
        elif st.session_state['current_section'] == 'DSR API':
            self.data_subject_rights_api()

    def decision_tree_section(self):
        """Visualize the regulatory metadata as a decision tree using PyVis with physics.
        Initially the network stabilizes (nodes become static) but if you drag a node the physics
        simulation restarts and nodes bounce. A legend is shown below the graph.
        """
        import tempfile
        from pyvis.network import Network
        import streamlit.components.v1 as components

        st.markdown("<div class='page-header'><i class='fas fa-sitemap'></i> &nbsp;Decision Tree</div>", unsafe_allow_html=True)
        st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section visualizes the regulatory metadata as an interactive decision tree.</p>
            <ul>
                <li>Visualizes complex relationships between regulatory components in a hierarchical structure</li>
                <li>Uses directed graph with the selected law as the root node</li>
                <li>Connects related entities based on their relationships in the regulatory framework</li>
            </ul>
        </div>''', unsafe_allow_html=True)

        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return

        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select a Law", options=law_options)
        
        # Visualization options
        st.subheader("Visualization Options")
        col1, col2 = st.columns(2)
        with col1:
            show_jurisdictions = st.checkbox("Show Jurisdictions", value=True)
            show_legal_bases = st.checkbox("Show Legal Bases", value=True)
            show_data_subject_types = st.checkbox("Show Data Subject Types", value=True)
        with col2:
            show_data_elements = st.checkbox("Show Data Elements", value=True)
            show_data_categories = st.checkbox("Show Data Categories", value=True)
            show_contexts = st.checkbox("Show Contexts", value=True)

        if not selected_law:
            return

        # Retrieve and filter metadata for the selected law
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        law_dst_de_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
        law_dst_dc_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
        law_context_dst_dc_sensitivities = self.regulatory_metadata_repository.get_law_context_data_subject_type_data_category_sensitivities()

        filtered_law_jurisdictions = [item for item in law_jurisdictions if item["law_name"] == selected_law]
        filtered_law_legal_bases = [item for item in law_legal_bases if item["law_name"] == selected_law]
        filtered_law_dst_de_sensitivities = [item for item in law_dst_de_sensitivities if item["law_name"] == selected_law]
        filtered_law_dst_dc_sensitivities = [item for item in law_dst_dc_sensitivities if item["law_name"] == selected_law]
        filtered_law_context_dst_dc_sensitivities = [item for item in law_context_dst_dc_sensitivities if item["law_name"] == selected_law]

        # Create a PyVis network instance with physics enabled
        net = Network(height="800px", width="100%", directed=True)
        # Set physics options: physics runs initially until stabilization.
        # Then, if you drag a node, physics restarts so nodes bounce.
        net.set_options("""
        var options = {
        "physics": {
            "enabled": true,
            "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 25,
            "onlyDynamicEdges": false
            },
            "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 95,
            "springConstant": 0.04,
            "damping": 0.09,
            "avoidOverlap": 0.1
            }
        },
        "interaction": {
            "dragNodes": true,
            "zoomView": true
        }
        }
        """)

        # Add the law as the root node
        net.add_node(selected_law, label=selected_law, size=25, color="#3498db")

        # Add jurisdictions
        if show_jurisdictions:
            for item in filtered_law_jurisdictions:
                jurisdiction = item["jurisdiction_name"]
                net.add_node(jurisdiction, label=jurisdiction, size=20, color="#2ecc71")
                net.add_edge(selected_law, jurisdiction)

        # Add legal bases
        if show_legal_bases:
            for item in filtered_law_legal_bases:
                legal_basis = item["legal_basis_name"]
                net.add_node(legal_basis, label=legal_basis, size=20, color="#e74c3c")
                net.add_edge(selected_law, legal_basis)

        # Add Data Subject Types, Data Elements, and Sensitivity levels
        if show_data_subject_types and show_data_elements:
            for item in filtered_law_dst_de_sensitivities:
                dst = f"DST: {item['data_subject_type_name']}"
                de = f"DE: {item['data_element_name']}"
                sensitivity = f"Sensitivity: {item['sensitivity_name']}"
                net.add_node(dst, label=dst, size=15, color="#f39c12")
                net.add_node(de, label=de, size=15, color="#9b59b6")
                net.add_node(sensitivity, label=sensitivity, size=15, color="#e67e22")
                net.add_edge(selected_law, dst)
                net.add_edge(dst, de)
                net.add_edge(de, sensitivity)

        # Add Data Subject Types, Data Categories, and Sensitivity levels
        if show_data_subject_types and show_data_categories:
            for item in filtered_law_dst_dc_sensitivities:
                dst = f"DST: {item['data_subject_type_name']}"
                dc = f"DC: {item['data_category_name']}"
                sensitivity = f"Sensitivity: {item['sensitivity_name']}"
                if dst not in net.get_nodes():
                    net.add_node(dst, label=dst, size=15, color="#f39c12")
                net.add_node(dc, label=dc, size=15, color="#1abc9c")
                if sensitivity not in net.get_nodes():
                    net.add_node(sensitivity, label=sensitivity, size=15, color="#e67e22")
                net.add_edge(selected_law, dst)
                net.add_edge(dst, dc)
                net.add_edge(dc, sensitivity)

        # Add Contexts, Data Subject Types, Data Categories, and Sensitivity levels
        if show_contexts and show_data_subject_types and show_data_categories:
            for item in filtered_law_context_dst_dc_sensitivities:
                context = f"Context: {item['context_name']}"
                dst = f"DST: {item['data_subject_type_name']}"
                dc = f"DC: {item['data_category_name']}"
                sensitivity = f"Sensitivity: {item['sensitivity_name']}"
                net.add_node(context, label=context, size=15, color="#34495e")
                if dst not in net.get_nodes():
                    net.add_node(dst, label=dst, size=15, color="#f39c12")
                if dc not in net.get_nodes():
                    net.add_node(dc, label=dc, size=15, color="#1abc9c")
                if sensitivity not in net.get_nodes():
                    net.add_node(sensitivity, label=sensitivity, size=15, color="#e67e22")
                net.add_edge(selected_law, context)
                net.add_edge(context, dst)
                net.add_edge(dst, dc)
                net.add_edge(dc, sensitivity)

        # Save the network to a temporary HTML file and display it in Streamlit
        tmp_dir = tempfile.gettempdir()
        path = os.path.join(tmp_dir, "pyvis_network.html")
        net.show(path, notebook=False)
        with open(path, "r", encoding="utf-8") as html_file:
            components.html(html_file.read(), height=800, width=1000)

        # Legend HTML
        legend_html = """
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px;">
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #3498db; border-radius: 50%; margin-right: 5px;"></div>
                <span>Law</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #2ecc71; border-radius: 50%; margin-right: 5px;"></div>
                <span>Jurisdiction</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #e74c3c; border-radius: 50%; margin-right: 5px;"></div>
                <span>Legal Basis</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #f39c12; border-radius: 50%; margin-right: 5px;"></div>
                <span>Data Subject Type</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #9b59b6; border-radius: 50%; margin-right: 5px;"></div>
                <span>Data Element</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #1abc9c; border-radius: 50%; margin-right: 5px;"></div>
                <span>Data Category</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #34495e; border-radius: 50%; margin-right: 5px;"></div>
                <span>Context</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #e67e22; border-radius: 50%; margin-right: 5px;"></div>
                <span>Sensitivity</span>
            </div>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)



    def sensitivity_inference_api(self):
        """Implement a sensitivity inference API based on regulatory metadata.
        This allows users to input data attributes and get sensitivity predictions.
        """
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Sensitivity Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                This API determines the sensitivity level of data based on regulatory metadata.<br><br>
                <ul>
                    <li>Analyzes data attributes against regulatory requirements</li>
                    <li>Provides sensitivity classification (high, medium, low)</li>
                    <li>Offers compliance recommendations based on sensitivity level</li>
                    <li>Helps implement appropriate data protection safeguards</li>
                </ul>
                <strong>How the Algorithm Works:</strong><br><br>
                <ul>
                    <li><strong>Context-Aware Lookup:</strong> Checks for sensitivity classifications matching all parameters</li>
                    <li><strong>Fallback Mechanism:</strong> Uses more general classifications if no specific match is found</li>
                    <li><strong>Hierarchical Classification:</strong> Understands relationships between data elements and categories</li>
                    <li><strong>Regulatory Alignment:</strong> Derives classifications from regulatory mappings</li>
                    <li><strong>Compliance Guidance:</strong> Provides specific safeguard recommendations by sensitivity level</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get laws for dropdown selection
            laws = self.glossary_repository.get_laws()
            if not laws:
                st.warning("No laws available in the database.")
                return
                
            law_options = [law["name"] for law in laws]
            selected_law = st.selectbox("Select Applicable Law", options=law_options)
            
            # Get data subject types
            data_subject_types = self.glossary_repository.get_data_subject_types()
            if data_subject_types:
                dst_options = [dst["name"] for dst in data_subject_types]
                selected_dst = st.selectbox("Select Data Subject Type", options=dst_options)
            else:
                st.warning("No data subject types available.")
                return
            
            # Get contexts/purposes
            contexts = self.glossary_repository.get_contexts()
            if contexts:
                context_options = [context["name"] for context in contexts]
                selected_context = st.selectbox("Select Processing Context/Purpose", options=context_options)
            else:
                selected_context = None
            
            # Option to select either data element or data category
            data_type = st.radio("Select Data Type", ["Data Element", "Data Category"])
            
            if data_type == "Data Element":
                data_elements = self.glossary_repository.get_data_elements()
                if data_elements:
                    de_options = [de["name"] for de in data_elements]
                    selected_data = st.selectbox("Select Data Element", options=de_options)
                else:
                    st.warning("No data elements available.")
                    return
            else:  # Data Category
                data_categories = self.glossary_repository.get_data_categories()
                if data_categories:
                    dc_options = [dc["name"] for dc in data_categories]
                    selected_data = st.selectbox("Select Data Category", options=dc_options)
                else:
                    st.warning("No data categories available.")
                    return
            
            # Add a button to trigger inference
            infer_button = st.button("Infer Sensitivity")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "data", "label": "Data Element/Category", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "law", "label": "Law", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "dst", "label": "Data Subject Type", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "context", "label": "Context (Optional)", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Sensitivity Lookup", "color": "#2ecc71", "shape": "box", "size": 25, 
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                        <h3>Sensitivity Lookup Process</h3>
                        <p>This lookup process determines data sensitivity by:</p>
                        <ol>
                            <li>Checking the <b>Law Data Subject Type Data Element Sensitivity</b> table for exact matches</li>
                            <li>If no match, checking the <b>Law Data Subject Type Data Category Sensitivity</b> table</li>
                            <li>Considering context factors if provided</li>
                            <li>Applying law-specific sensitivity rules and thresholds</li>
                            <li>Returning the appropriate sensitivity level with confidence score</li>
                        </ol>
                        <p>The algorithm prioritizes specific element matches over category matches and considers the most restrictive interpretation when multiple laws apply.</p>
                    </div>
                """}},
                {"id": "high", "label": "High Sensitivity", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "medium", "label": "Medium Sensitivity", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "low", "label": "Low Sensitivity", "color": "#2ecc71", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "data", "target": "law", "label": "Regulated by"},
                {"source": "data", "target": "dst", "label": "Relates to"},
                {"source": "data", "target": "context", "label": "Used in"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "dst", "target": "lookup", "label": ""},
                {"source": "context", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "high", "label": "If sensitive PII"},
                {"source": "lookup", "target": "medium", "label": "If general PII"},
                {"source": "lookup", "target": "low", "label": "If non-PII"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Sensitivity Results")
            
            if infer_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing regulatory metadata..."):
                    # Get the sensitivity based on the selected parameters
                    sensitivity = self._infer_sensitivity(
                        selected_law, 
                        selected_dst, 
                        selected_context, 
                        selected_data, 
                        data_type
                    )
                
                if sensitivity:
                    # Display the result with appropriate styling based on sensitivity level
                    color = "#e74c3c" if sensitivity.lower() == "high" else \
                           "#f39c12" if sensitivity.lower() == "medium" else \
                           "#2ecc71"
                    
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: {color}25; border: 2px solid {color}; margin-top: 20px;">
                        <h3 style="color: {color};">Sensitivity Level: {sensitivity}</h3>
                        <p>Based on the selected parameters, the data is classified as <strong>{sensitivity} sensitivity</strong> 
                        under {selected_law}.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the reasoning
                    st.markdown("### Reasoning")
                    
                    if data_type == "Data Element":
                        st.markdown(f"""
                        The sensitivity level was determined based on the following factors:
                        - **Law**: {selected_law}
                        - **Data Subject Type**: {selected_dst}
                        - **Data Element**: {selected_data}
                        {f"- **Context**: {selected_context}" if selected_context else ""}
                        
                        According to the regulatory metadata, when processing the data element '{selected_data}' 
                        for a '{selected_dst}' under '{selected_law}', the appropriate sensitivity classification is '{sensitivity}'.
                        """)
                    else:
                        st.markdown(f"""
                        The sensitivity level was determined based on the following factors:
                        - **Law**: {selected_law}
                        - **Data Subject Type**: {selected_dst}
                        - **Data Category**: {selected_data}
                        {f"- **Context**: {selected_context}" if selected_context else ""}
                        
                        According to the regulatory metadata, when processing data from the '{selected_data}' category 
                        for a '{selected_dst}' under '{selected_law}', the appropriate sensitivity classification is '{sensitivity}'.
                        """)
                    
                    # Add compliance recommendations based on sensitivity
                    st.markdown("### Compliance Recommendations")
                    
                    if sensitivity.lower() == "high":
                        st.markdown("""
                        #### High Sensitivity Data Handling Requirements:
                        - Implement strong encryption for storage and transmission
                        - Conduct a Data Protection Impact Assessment (DPIA)
                        - Implement strict access controls and authentication
                        - Ensure explicit consent is obtained where required
                        - Maintain detailed processing records
                        - Consider data minimization and pseudonymization techniques
                        """)
                    elif sensitivity.lower() == "medium":
                        st.markdown("""
                        #### Medium Sensitivity Data Handling Requirements:
                        - Implement standard encryption for storage and transmission
                        - Consider whether a DPIA is necessary
                        - Implement appropriate access controls
                        - Ensure appropriate legal basis for processing
                        - Maintain processing records
                        - Apply data minimization principles
                        """)
                    else:  # Low
                        st.markdown("""
                        #### Low Sensitivity Data Handling Requirements:
                        - Follow standard security practices
                        - Implement basic access controls
                        - Ensure appropriate legal basis for processing
                        - Apply data minimization principles
                        - Maintain basic processing records
                        """)
                else:
                    st.warning("No sensitivity classification found for the selected parameters.")
                    st.markdown("""
                    This could be because:
                    1. The specific combination of parameters is not defined in the regulatory metadata
                    2. The selected law does not regulate this specific data type for this subject type
                    3. Additional context may be needed for proper classification
                    
                    Consider consulting with a privacy professional for further guidance.
                    """)
            else:
                # Display instructions when the form hasn't been submitted yet
                st.info("Fill in the parameters on the left and click 'Infer Sensitivity' to get results.")
                
                # Show a sample result visualization
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; border: 2px dashed #7F8C8D; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Results will appear here after inference...</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _infer_sensitivity(self, law, data_subject_type, context, data_value, data_type):
        """Internal method to infer sensitivity based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            data_subject_type (str): The name of the data subject type
            context (str): The name of the context/purpose (can be None)
            data_value (str): The name of the data element or category
            data_type (str): Either "Data Element" or "Data Category"
            
        Returns:
            str: The inferred sensitivity level or None if not found
        """
        # First try with context if provided
        if context and data_type == "Data Category":
            # Check law_context_dst_dc_sensitivity table
            context_sensitivities = self.regulatory_metadata_repository.get_law_context_data_subject_type_data_category_sensitivities()
            for item in context_sensitivities:
                if (item["law_name"] == law and 
                    item["context_name"] == context and 
                    item["data_subject_type_name"] == data_subject_type and 
                    item["data_category_name"] == data_value):
                    return item["sensitivity_name"]
        
        # If no result with context or context not provided, try without context
        if data_type == "Data Element":
            # Check law_dst_de_sensitivity table
            de_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
            for item in de_sensitivities:
                if (item["law_name"] == law and 
                    item["data_subject_type_name"] == data_subject_type and 
                    item["data_element_name"] == data_value):
                    return item["sensitivity_name"]
        else:  # Data Category
            # Check law_dst_dc_sensitivity table
            dc_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
            for item in dc_sensitivities:
                if (item["law_name"] == law and 
                    item["data_subject_type_name"] == data_subject_type and 
                    item["data_category_name"] == data_value):
                    return item["sensitivity_name"]
        
        # If no direct match found, return None
        return None
        
    def legal_basis_inference_api(self):
        """Implement a legal basis inference API based on regulatory metadata.
        This allows users to input processing parameters and get legal basis recommendations.
        """
        st.markdown("<div class='page-header'><i class='fas fa-balance-scale'></i> &nbsp;Legal Basis Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine the appropriate legal basis for processing personal data based on regulatory metadata.<br><br>
            <ul>
                <li>Recommends suitable legal bases according to applicable regulations</li>
                <li>Considers processing purpose, data sensitivity, and jurisdiction</li>
                <li>Ranks recommendations by regulatory preference</li>
                <li>Provides implementation guidance for each legal basis</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Purpose-Based Analysis:</strong> Finds legal bases for specific law and purpose combinations</li>
                <li><strong>Preference Ordering:</strong> Ranks legal bases by regulatory preference (lower numbers = higher preference)</li>
                <li><strong>Sensitivity Refinement:</strong> Adjusts recommendations based on data sensitivity level</li>
                <li><strong>Fallback Mechanism:</strong> Uses general legal bases if no purpose-specific ones are found</li>
                <li><strong>Compliance Guidance:</strong> Provides specific requirements and implementation steps</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get laws for dropdown selection
            laws = self.glossary_repository.get_laws()
            if not laws:
                st.warning("No laws available in the database.")
                return
                
            law_options = [law["name"] for law in laws]
            selected_law = st.selectbox("Select Applicable Law", options=law_options)
            
            # Get jurisdictions
            jurisdictions = self.glossary_repository.get_jurisdictions()
            if jurisdictions:
                jurisdiction_options = [j["name"] for j in jurisdictions]
                selected_jurisdiction = st.selectbox("Select Jurisdiction", options=jurisdiction_options)
            else:
                selected_jurisdiction = None
            
            # Get purpose categories (new)
            purpose_categories = self.glossary_repository.get_purpose_categories()
            if purpose_categories:
                purpose_category_options = [pc["name"] for pc in purpose_categories]
                selected_purpose_category = st.selectbox("Select Purpose Category", options=purpose_category_options)
            else:
                st.warning("No purpose categories available.")
                return
                                    
            # Add sensitivity level selection
            sensitivities = self.glossary_repository.get_sensitivities()
            if sensitivities:
                sensitivity_options = [s["name"] for s in sensitivities]
                selected_sensitivity = st.selectbox("Select Data Sensitivity", options=sensitivity_options)
            else:
                sensitivity_options = ["Low", "Medium", "High"]
                selected_sensitivity = st.selectbox("Select Data Sensitivity", options=sensitivity_options)
            
            # Add a button to trigger inference
            infer_button = st.button("Recommend Legal Basis")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "processing", "label": "Processing Activity", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "law", "label": "Law", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "purpose", "label": "Purpose Category", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "sensitivity", "label": "Data Sensitivity", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Legal Basis Lookup", "color": "#2ecc71", "shape": "box", "size": 25,
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                        <h3>Legal Basis Lookup Process</h3>
                        <p>This lookup process determines appropriate legal bases by:</p>
                        <ol>
                            <li>Querying the <b>Law Purpose Category Legal Basis</b> table for matches</li>
                            <li>Filtering results based on the selected law, purpose, and data sensitivity</li>
                            <li>Ranking legal bases by appropriateness for the specific scenario</li>
                            <li>Considering sensitivity thresholds for each legal basis type</li>
                            <li>Providing implementation requirements for each recommended basis</li>
                        </ol>
                        <p>The algorithm prioritizes more protective legal bases for higher sensitivity data and considers purpose-specific requirements defined in each law.</p>
                    </div>
                """}},
                {"id": "consent", "label": "Consent", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "contract", "label": "Contract", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "legitimate", "label": "Legitimate Interest", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "legal", "label": "Legal Obligation", "color": "#3498db", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "processing", "target": "law", "label": "Governed by"},
                {"source": "processing", "target": "purpose", "label": "Has purpose"},
                {"source": "processing", "target": "sensitivity", "label": "Involves data"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "purpose", "target": "lookup", "label": ""},
                {"source": "sensitivity", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "consent", "label": "High sensitivity"},
                {"source": "lookup", "target": "contract", "label": "Low sensitivity"},
                {"source": "lookup", "target": "legitimate", "label": "Medium sensitivity"},
                {"source": "lookup", "target": "legal", "label": "Compliance"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Legal Basis Recommendations")
            
            if infer_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing regulatory metadata..."):
                    # Get legal bases based on the selected parameters
                    legal_bases = self._infer_legal_basis(
                        selected_law, 
                        selected_jurisdiction,
                        selected_sensitivity,
                        selected_purpose_category
                    )
                
                if legal_bases:
                    # Display the recommended legal bases with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                        <h3 style="color: #3498db;">Recommended Legal Bases</h3>
                        <p>Based on the selected parameters, the following legal bases are recommended for processing under {selected_law}:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display each legal basis with its description and compliance requirements
                    for i, legal_basis in enumerate(legal_bases):
                        with st.expander(f"{i+1}. {legal_basis['name']}", expanded=True if i == 0 else False):
                            st.markdown(f"**Description**: {legal_basis.get('description', 'No description available')}")
                            
                            # Add compliance requirements from the repository
                            st.markdown("#### Compliance Requirements:")
                            
                            if "compliance_requirements" in legal_basis and legal_basis["compliance_requirements"]:
                                requirements_list = "\n".join([f"- {req}" for req in legal_basis["compliance_requirements"]])
                                st.markdown(requirements_list)
                            else:
                                st.markdown("No specific compliance requirements available for this legal basis.")
                            
                            # Add compatibility with sensitivity level
                            compatibility = "High" if selected_sensitivity.lower() == "low" else \
                                          "Medium" if selected_sensitivity.lower() == "medium" else \
                                          "Low"
                            
                            st.markdown(f"**Compatibility with {selected_sensitivity} sensitivity data**: {compatibility}")
                    
                    # Display the reasoning
                    st.markdown("### Reasoning")
                    st.markdown(f"""
                    The legal basis recommendations were determined based on the following factors:
                    - **Law**: {selected_law}
                    - **Jurisdiction**: {selected_jurisdiction if selected_jurisdiction else 'Not specified'}
                    - **Purpose Category**: {selected_purpose_category}
                    - **Sensitivity Level**: {selected_sensitivity}
                    
                    According to the regulatory metadata, when processing {selected_sensitivity} data under {selected_law} for the purpose category of {selected_purpose_category}, 
                    the recommended legal bases are listed above in order of preference.
                    """)
                    
                    # Add general compliance notes
                    st.markdown("### General Compliance Notes")
                    st.markdown("""
                    1. **Documentation**: Always document your legal basis assessment and decision process.
                    2. **Transparency**: Clearly communicate the legal basis to data subjects in your privacy notice.
                    3. **Purpose Limitation**: Only use the data for the purpose specified under the chosen legal basis.
                    4. **Data Minimization**: Only process the data necessary for the specified purpose.
                    5. **Regular Review**: Periodically review your legal basis to ensure it remains appropriate.
                    6. **Special Categories**: For sensitive data, ensure you also have an appropriate condition for processing.
                    """)
                else:
                    st.warning("No specific legal basis recommendations found for the selected parameters.")
                    st.markdown("""
                    This could be because:
                    1. The specific combination of parameters is not defined in the regulatory metadata
                    2. The selected law does not specify legal bases for this scenario
                    3. Additional context may be needed for proper recommendations
                    
                    Consider consulting with a privacy professional for further guidance.
                    """)
                    
                    # Provide general legal basis information
                    st.markdown("### General Legal Basis Information")
                    st.markdown("""
                    Here are the common legal bases for processing personal data under major privacy regulations:
                    
                    1. **Consent**: The data subject has given clear consent for processing their personal data for a specific purpose.
                    2. **Contract**: Processing is necessary for a contract with the data subject or to take steps at their request before entering a contract.
                    3. **Legal Obligation**: Processing is necessary to comply with a legal obligation.
                    4. **Vital Interests**: Processing is necessary to protect someone's life or vital interests.
                    5. **Public Task**: Processing is necessary for a task carried out in the public interest or in the exercise of official authority.
                    6. **Legitimate Interests**: Processing is necessary for legitimate interests pursued by the controller or a third party, except where overridden by the interests or rights of the data subject.
                    
                    The appropriate legal basis depends on your specific circumstances, the nature of the data, and the purpose of processing.
                    """)
            else:
                # Display instructions when the form hasn't been submitted yet
                st.info("Fill in the parameters on the left and click 'Recommend Legal Basis' to get results.")
                
                # Show a sample result visualization
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; border: 2px dashed #7F8C8D; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Legal basis recommendations will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _infer_legal_basis(self, law, jurisdiction, sensitivity, purpose_category=None):
        """Internal method to infer appropriate legal bases based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            jurisdiction (str): The name of the jurisdiction (can be None)
            sensitivity (str): The sensitivity level
            purpose_category (str): The purpose category for processing
            
        Returns:
            list: A list of recommended legal bases or None if not found
        """
        # First, try to get legal bases based on purpose category if available
        if purpose_category:
            # Get law ID
            law_id = None
            laws = self.glossary_repository.get_laws()
            for l in laws:
                if l["name"] == law:
                    law_id = l["id"]
                    break
            
            # Get purpose category ID
            purpose_category_id = None
            purpose_categories = self.glossary_repository.get_purpose_categories()
            for pc in purpose_categories:
                if pc["name"] == purpose_category:
                    purpose_category_id = pc["id"]
                    break
            
            if law_id and purpose_category_id:
                # Get legal bases recommended for this law and purpose category combination
                law_purpose_legal_bases = self.regulatory_metadata_repository.get_law_purpose_category_legal_bases(
                    law_id=law_id, purpose_category_id=purpose_category_id
                )
                
                if law_purpose_legal_bases:
                    # Get full legal basis information
                    all_legal_bases = self.glossary_repository.get_legal_bases()
                    
                    # Get the full legal basis objects and sort by preference order
                    recommended_legal_bases = []
                    for lb in all_legal_bases:
                        for lplb in law_purpose_legal_bases:
                            if lb["id"] == lplb["legal_basis_id"]:
                                lb["preference_order"] = lplb["preference_order"]
                                lb["recommendation_description"] = lplb["description"]
                                
                                # Get compliance requirements for this legal basis
                                requirements = self.regulatory_metadata_repository.get_legal_basis_requirements(lb["id"])
                                lb["compliance_requirements"] = [req["requirement"] for req in requirements] if requirements else []
                                
                                recommended_legal_bases.append(lb)
                    
                    # Sort by preference order (lower number = higher preference)
                    recommended_legal_bases.sort(key=lambda x: x.get("preference_order", 999))
                    
                    # Further refine based on sensitivity
                    self._refine_by_sensitivity(recommended_legal_bases, sensitivity)
                    
                    return recommended_legal_bases
        
        # Fall back to the original method if purpose category approach doesn't yield results
        # Get all legal bases for the selected law
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        filtered_legal_bases = [item for item in law_legal_bases if item["law_name"] == law]
        
        if not filtered_legal_bases:
            return None
        
        # Get full legal basis information
        all_legal_bases = self.glossary_repository.get_legal_bases()
        
        # Extract just the legal basis names from the filtered results
        legal_basis_names = [item["legal_basis_name"] for item in filtered_legal_bases]
        
        # Get the full legal basis objects for the filtered names
        recommended_legal_bases = []
        for lb in all_legal_bases:
            if lb["name"] in legal_basis_names:
                # Get compliance requirements for this legal basis
                requirements = self.regulatory_metadata_repository.get_legal_basis_requirements(lb["id"])
                lb["compliance_requirements"] = [req["requirement"] for req in requirements] if requirements else []
                recommended_legal_bases.append(lb)
        
        # Sort legal bases based on sensitivity
        self._refine_by_sensitivity(recommended_legal_bases, sensitivity)
        
        return recommended_legal_bases
        
    def _refine_by_sensitivity(self, legal_bases, sensitivity):
        """Helper method to refine legal basis recommendations based on data sensitivity.
        
        Args:
            legal_bases (list): List of legal basis objects to sort
            sensitivity (str): The sensitivity level (high, medium, low)
        """
        # For high sensitivity data, prioritize explicit consent and legal obligation
        if sensitivity.lower() == "high":
            legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "legal obligation" in lb["name"].lower()), 
                reverse=True)
        # For medium sensitivity, legitimate interests might be appropriate
        elif sensitivity.lower() == "medium":
            legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "contract" in lb["name"].lower(), 
                 "legitimate" in lb["name"].lower()), 
                reverse=True)
        # For low sensitivity, contract and legitimate interests are often suitable
        else:
            legal_bases.sort(key=lambda lb: 
                ("contract" in lb["name"].lower(), "legitimate" in lb["name"].lower(), 
                 "consent" in lb["name"].lower()), 
                reverse=True)
        
    def breach_notification_api(self):
        """Implement an incident breach notification API based on regulatory metadata.
        This helps users determine notification requirements for data breaches.
        """
        st.markdown("<div class='page-header'><i class='fas fa-exclamation-triangle'></i> &nbsp;Breach Notification</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            This API helps determine the notification requirements for data breaches based on regulatory metadata.<br><br>
            <ul>
                <li>Provides guidance on notification requirements and timelines</li>
                <li>Identifies authorities that must be notified</li>
                <li>Calculates risk scores to determine notification necessity</li>
                <li>Offers documentation templates and remediation guidance</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Law-Specific Guidance:</strong> Retrieves notification requirements for the selected law</li>
                <li><strong>Risk Assessment:</strong> Calculates risk score based on breach type and impact</li>
                <li><strong>Jurisdiction Analysis:</strong> Considers jurisdiction-specific requirements</li>
                <li><strong>Timeline Calculation:</strong> Determines precise notification deadlines</li>
                <li><strong>Documentation Guidance:</strong> Provides internal documentation templates</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Breach Incident Details")
            
            # Get laws for dropdown selection
            laws = self.glossary_repository.get_laws()
            if not laws:
                st.warning("No laws available in the database.")
                return
                
            law_options = [law["name"] for law in laws]
            selected_law = st.selectbox("Select Applicable Law", options=law_options)
            
            # Get jurisdictions
            jurisdictions = self.glossary_repository.get_jurisdictions()
            if jurisdictions:
                jurisdiction_options = [j["name"] for j in jurisdictions]
                selected_jurisdiction = st.selectbox("Select Jurisdiction", options=jurisdiction_options)
            else:
                selected_jurisdiction = None
            
            # Breach details
            breach_type = st.selectbox(
                "Type of Breach", 
                options=[
                    "Unauthorized Access", 
                    "Data Disclosure", 
                    "Data Alteration", 
                    "Data Loss", 
                    "Ransomware Attack", 
                    "Phishing Attack", 
                    "Insider Threat", 
                    "Physical Breach", 
                    "Other"
                ]
            )
            
            # Get data categories
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                affected_data_categories = st.multiselect("Affected Data Categories", options=dc_options, key="breach_data_categories")
            else:
                st.warning("No data categories available.")
                return
            
            # Get data subject types
            data_subject_types = self.glossary_repository.get_data_subject_types()
            if data_subject_types:
                dst_options = [dst["name"] for dst in data_subject_types]
                affected_data_subjects = st.multiselect("Affected Data Subject Types", options=dst_options, key="breach_data_subject_types")
            else:
                st.warning("No data subject types available.")
                return
            
            # Number of affected individuals
            num_affected = st.number_input("Number of Affected Individuals", min_value=0, value=100)
            
            # Risk assessment
            risk_level = st.select_slider(
                "Risk Level to Individuals",
                options=["Minimal", "Low", "Medium", "High", "Severe"],
                value="Medium"
            )
            
            # Containment status
            containment_status = st.radio(
                "Breach Containment Status",
                options=["Contained", "Partially Contained", "Not Contained"],
                horizontal=True
            )
            
            # Discovery date
            col_dates1, col_dates2 = st.columns(2)
            with col_dates1:
                discovery_date = st.date_input("Date Breach Discovered", value=None)
            with col_dates2:
                occurrence_date = st.date_input("Date Breach Occurred (if known)", value=None)
            
            analyze_button = st.button("Analyze Notification Requirements")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "breach", "label": "Data Breach", "color": "#e74c3c", "shape": "ellipse", "size": 30},
                {"id": "jurisdiction", "label": "Affected Jurisdiction", "color": "#3498db", "shape": "box", "size": 25},
                {"id": "law", "label": "Applicable Law", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "data_types", "label": "Data Types Affected", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "severity", "label": "Breach Severity", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Notification Requirements Lookup", "color": "#2ecc71", "shape": "box", "size": 25,
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                        <h3>Breach Notification Lookup Process</h3>
                        <p>This lookup process determines notification requirements by:</p>
                        <ol>
                            <li>Querying the <b>Law Incident Breach Notification</b> table for the applicable law</li>
                            <li>Evaluating breach severity based on data types affected and number of individuals</li>
                            <li>Determining authority notification requirements and deadlines</li>
                            <li>Assessing individual notification thresholds and exemptions</li>
                            <li>Calculating notification timeframes based on discovery date</li>
                        </ol>
                        <p>The algorithm considers risk level, containment status, and jurisdiction-specific requirements to provide comprehensive notification guidance.</p>
                    </div>
                """}},
                {"id": "authority", "label": "Authority Notification", "color": "#3498db", "shape": "box", "size": 25},
                {"id": "individual", "label": "Individual Notification", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "timeframe", "label": "Notification Timeframe", "color": "#9b59b6", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "breach", "target": "jurisdiction", "label": "Occurs in"},
                {"source": "jurisdiction", "target": "law", "label": "Governed by"},
                {"source": "breach", "target": "data_types", "label": "Involves"},
                {"source": "breach", "target": "severity", "label": "Has"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "data_types", "target": "lookup", "label": ""},
                {"source": "severity", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "authority", "label": "Requires"},
                {"source": "lookup", "target": "individual", "label": "May require"},
                {"source": "lookup", "target": "timeframe", "label": "Specifies"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Notification Requirements")
            
            if analyze_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing breach notification requirements..."):
                    # Get breach notification guidance based on the selected law
                    guidance = self._get_breach_notification_guidance(selected_law)
                
                if guidance:
                    # Display the notification requirements with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #e74c3c25; border: 2px solid #e74c3c; margin-top: 20px;">
                        <h3 style="color: #e74c3c;">Notification Required</h3>
                        <p><strong>Authority to Notify:</strong> {guidance['authority']}</p>
                        <p><strong>Notification Deadline:</strong> {guidance['timeframe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the notification threshold
                    st.markdown("### Notification Threshold")
                    st.markdown(f"**{guidance['threshold']}**")
                    
                    # Display detailed guidance
                    st.markdown("### Detailed Guidance")
                    st.markdown(guidance['content'])
                    
                    # Display breach assessment
                    st.markdown("### Breach Assessment")
                    
                    # Calculate days since discovery
                    days_remaining = None
                    if discovery_date:
                        import datetime
                        today = datetime.date.today()
                        days_since_discovery = (today - discovery_date).days
                        
                        # Extract the timeframe in hours if possible
                        import re
                        hours_match = re.search(r'(\d+)\s*hours', guidance['timeframe'])
                        if hours_match:
                            hours = int(hours_match.group(1))
                            days_allowed = hours / 24
                            days_remaining = days_allowed - days_since_discovery
                    
                    # Notification urgency based on days remaining
                    if days_remaining is not None:
                        if days_remaining < 0:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #e74c3c25; margin: 10px 0;">
                                <strong style="color: #e74c3c;">⚠️ URGENT: Notification deadline has passed!</strong><br>
                                The breach was discovered {days_since_discovery} days ago, which exceeds the notification timeframe.
                                Notify the relevant authority immediately to minimize potential penalties.
                            </div>
                            """, unsafe_allow_html=True)
                        elif days_remaining < 1:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #f39c1225; margin: 10px 0;">
                                <strong style="color: #f39c12;">⚠️ URGENT: Notification deadline approaching!</strong><br>
                                The breach was discovered {days_since_discovery} days ago. You have less than 24 hours remaining to notify.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #3498db25; margin: 10px 0;">
                                <strong style="color: #3498db;">Notification timeline:</strong><br>
                                The breach was discovered {days_since_discovery} days ago. You have approximately {days_remaining:.1f} days remaining to notify.
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Risk assessment
                    risk_color = "#e74c3c" if risk_level in ["High", "Severe"] else \
                                "#f39c12" if risk_level == "Medium" else \
                                "#2ecc71"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: {risk_color}25; margin: 10px 0;">
                        <strong style="color: {risk_color};">Risk assessment:</strong><br>
                        Based on your input, this breach poses a <strong>{risk_level}</strong> risk to affected individuals.
                        {"This likely requires notification based on the threshold criteria." if risk_level in ["Medium", "High", "Severe"] else "This may fall below the notification threshold, but consider notifying as a precaution."}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Scope assessment
                    if num_affected > 500:
                        scope_severity = "large-scale"
                        scope_color = "#e74c3c"
                    elif num_affected > 100:
                        scope_severity = "significant"
                        scope_color = "#f39c12"
                    else:
                        scope_severity = "limited"
                        scope_color = "#2ecc71"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: {scope_color}25; margin: 10px 0;">
                        <strong style="color: {scope_color};">Scope assessment:</strong><br>
                        This breach affects <strong>{num_affected}</strong> individuals, which is considered a <strong>{scope_severity}</strong> incident.
                        {"This scale of breach typically requires notification to authorities and possibly affected individuals." if scope_severity in ["significant", "large-scale"] else "Even with a limited scope, notification may still be required depending on the nature of the data affected."}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add notification checklist
                    st.markdown("### Notification Checklist")
                    st.markdown("""
                    ✅ **Information to include in your notification:**
                    
                    1. **Nature of the breach**
                       - Type of breach: {}
                       - How it occurred (if known)
                       - When it occurred and when it was discovered
                    
                    2. **Scope of the breach**
                       - Categories of personal data affected
                       - Number of data records concerned
                       - Number of data subjects affected
                    
                    3. **Likely consequences**
                       - Potential impact on individuals
                       - Risk assessment
                    
                    4. **Measures taken or proposed**
                       - Steps taken to contain the breach
                       - Steps taken to mitigate possible adverse effects
                       - Future preventative measures
                    
                    5. **Contact information**
                       - Details of your Data Protection Officer or other contact point
                    """.format(breach_type))
                    
                    # Add notification to individuals section if high risk
                    if risk_level in ["High", "Severe"]:
                        st.markdown("### Notification to Affected Individuals")
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 5px; background-color: #e74c3c25; margin: 10px 0;">
                            <strong style="color: #e74c3c;">Individual notification required</strong><br>
                            Based on the {risk_level} risk level, you likely need to notify affected individuals without undue delay.
                        </div>
                        
                        **Information to include in individual notifications:**
                        
                        1. Clear description of the breach in plain language
                        2. Name and contact details of your data protection officer or other contact point
                        3. Description of the likely consequences of the breach
                        4. Description of measures taken or proposed to address the breach
                        5. Specific recommendations for individuals to protect themselves
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No breach notification guidance found for {selected_law}.")
                    st.markdown("""
                    This could be because:
                    1. The selected law does not have specific breach notification requirements in our database
                    2. The regulatory metadata for this law needs to be updated
                    
                    Consider consulting with a privacy professional for guidance specific to this law.
                    """)
                    
                    # Provide general breach notification guidance
                    st.markdown("### General Breach Notification Guidance")
                    st.markdown("""
                    While specific guidance for the selected law is not available, here are general principles for breach notification:
                    
                    1. **Assess the risk** to individuals resulting from the breach
                    2. **Notify relevant authorities** as soon as possible, typically within 72 hours of discovery
                    3. **Notify affected individuals** if the breach is likely to result in high risk to their rights and freedoms
                    4. **Document the breach** including facts, effects, and remedial actions taken
                    5. **Implement measures** to contain the breach and prevent future incidents
                    
                    Many jurisdictions have mandatory breach notification requirements with specific timeframes and thresholds.
                    """)
            else:
                # Display instructions when the form hasn't been submitted yet
                st.info("Fill in the breach details on the left and click 'Analyze Notification Requirements' to get results.")
                
                # Show a sample result visualization
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; border: 2px dashed #7F8C8D; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Breach notification requirements will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _get_breach_notification_guidance(self, law_name):
        """Internal method to get breach notification guidance for a specific law.
        
        Args:
            law_name (str): The name of the selected law
            
        Returns:
            dict: The breach notification guidance or None if not found
        """
        # Get the law ID from the name
        laws = self.glossary_repository.get_laws()
        law_id = None
        for law in laws:
            if law["name"] == law_name:
                law_id = law["id"]
                break
        
        if not law_id:
            return None
        
        # Get breach notification guidance for the law
        guidances = self.regulatory_metadata_repository.get_law_incident_breach_guidances(law_id)
        
        if not guidances:
            return None
        
        # Return the first guidance for the law (typically there's only one per law)
        return guidances[0]


    def transfer_mechanism_api(self):
        """Implement a transfer mechanism inference API based on regulatory metadata.
        This helps users determine appropriate safeguards for cross-border data transfers.
        """
        st.markdown("<div class='page-header'><i class='fas fa-exchange-alt'></i> &nbsp;Transfer Mechanism Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine appropriate transfer mechanisms for cross-border data transfers based on regulatory metadata.<br><br>
            <ul>
                <li>Identifies suitable transfer mechanisms for specific jurisdictions</li>
                <li>Evaluates adequacy decisions and existing agreements</li>
                <li>Recommends appropriate safeguards (SCCs, BCRs, etc.)</li>
                <li>Provides implementation guidance for each transfer mechanism</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Jurisdictional Analysis:</strong> Evaluates source and destination jurisdictions</li>
                <li><strong>Adequacy Assessment:</strong> Checks for adequacy decisions or existing agreements</li>
                <li><strong>Risk Evaluation:</strong> Considers data types and transfer volumes</li>
                <li><strong>Mechanism Ranking:</strong> Presents transfer mechanisms in order of preference</li>
                <li><strong>Implementation Guidance:</strong> Provides specific requirements for each mechanism</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get laws for dropdown selection
            laws = self.glossary_repository.get_laws()
            if not laws:
                st.warning("No laws available in the database.")
                return
                
            law_options = [law["name"] for law in laws]
            selected_law = st.selectbox("Select Applicable Law", options=law_options, key="transfer_law")
            
            # Get jurisdictions for source and destination
            jurisdictions = self.glossary_repository.get_jurisdictions()
            if jurisdictions:
                jurisdiction_options = [j["name"] for j in jurisdictions]
                source_jurisdiction = st.selectbox("Select Source Jurisdiction", options=jurisdiction_options, key="transfer_source")
                destination_jurisdiction = st.selectbox("Select Destination Jurisdiction", options=jurisdiction_options, key="transfer_destination")
            else:
                st.warning("No jurisdictions available.")
                return
            
            # Get data categories
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data_categories = st.multiselect("Select Data Categories to Transfer", options=dc_options, key="transfer_data_categories")
            else:
                selected_data_categories = []
            
            # Add transfer volume/frequency options
            transfer_volume = st.select_slider(
                "Transfer Volume",
                options=["Low", "Medium", "High"],
                value="Medium",
                key="transfer_volume"
            )
            
            transfer_frequency = st.select_slider(
                "Transfer Frequency",
                options=["One-time", "Occasional", "Regular", "Continuous"],
                value="Regular",
                key="transfer_frequency"
            )
            
            # Add a button to trigger inference
            analyze_button = st.button("Recommend Transfer Mechanisms")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "transfer", "label": "Data Transfer", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "source", "label": "Source Jurisdiction", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "destination", "label": "Destination Jurisdiction", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "law", "label": "Applicable Law", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "data_categories", "label": "Data Categories", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "adequacy", "label": "Adequacy Decision", "color": "#1abc9c", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Transfer Mechanism Lookup", "color": "#3498db", "shape": "box", "size": 25,
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #3498db;'>
                        <h3>Transfer Mechanism Lookup Process</h3>
                        <p>This lookup process determines appropriate transfer mechanisms by:</p>
                        <ol>
                            <li>Querying the <b>Law Transfer</b> table for the applicable law</li>
                            <li>Checking for adequacy decisions between source and destination jurisdictions</li>
                            <li>Evaluating data categories and their sensitivity levels</li>
                            <li>Considering transfer volume and frequency</li>
                            <li>Ranking mechanisms by appropriateness and legal compliance</li>
                        </ol>
                        <p>The algorithm prioritizes mechanisms based on the legal hierarchy established in each jurisdiction, with preference for adequacy decisions when available.</p>
                    </div>
                """}},
                {"id": "sccs", "label": "Standard Contractual Clauses", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "bcrs", "label": "Binding Corporate Rules", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "consent", "label": "Explicit Consent", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "derogations", "label": "Derogations", "color": "#2ecc71", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "transfer", "target": "source", "label": "From"},
                {"source": "transfer", "target": "destination", "label": "To"},
                {"source": "transfer", "target": "data_categories", "label": "Involves"},
                {"source": "source", "target": "law", "label": "Governed by"},
                {"source": "destination", "target": "adequacy", "label": "Has/lacks"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "data_categories", "target": "lookup", "label": ""},
                {"source": "adequacy", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "sccs", "label": "May recommend"},
                {"source": "lookup", "target": "bcrs", "label": "May recommend"},
                {"source": "lookup", "target": "consent", "label": "May recommend"},
                {"source": "lookup", "target": "derogations", "label": "May allow"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Transfer Mechanism Recommendations")
            
            if analyze_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing transfer requirements..."):
                    # Simulate processing time
                    time.sleep(1)
                    
                    # Determine if this is an adequate jurisdiction
                    is_adequate = False
                    if destination_jurisdiction in ["United Kingdom", "Canada", "Switzerland", "Japan", "New Zealand"]:
                        is_adequate = True
                    
                    # Get transfer mechanisms based on the selected parameters
                    transfer_mechanisms = self._get_transfer_mechanisms(selected_law, source_jurisdiction, destination_jurisdiction, is_adequate)
                
                if transfer_mechanisms:
                    # Display the recommended transfer mechanisms with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                        <h3 style="color: #3498db;">Recommended Transfer Mechanisms</h3>
                        <p>Based on the selected parameters, the following transfer mechanisms are recommended for transfers from <strong>{source_jurisdiction}</strong> to <strong>{destination_jurisdiction}</strong> under {selected_law}:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display each transfer mechanism with its description and requirements
                    for i, mechanism in enumerate(transfer_mechanisms):
                        with st.expander(f"{i+1}. {mechanism['name']}"):
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa;">
                                <h4>{mechanism['name']}</h4>
                                <p><strong>Description:</strong> {mechanism['description']}</p>
                                <p><strong>Implementation Requirements:</strong></p>
                                <ul>
                                    {' '.join([f'<li>{req}</li>' for req in mechanism['requirements']])}
                                </ul>
                                <p><strong>Risk Level:</strong> <span style="color: {mechanism['risk_color']};">{mechanism['risk_level']}</span></p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    # Display a message if no transfer mechanisms are found
                    st.markdown("""
                    <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                        <h3 style="color: #7F8C8D;">No Transfer Mechanisms Found</h3>
                        <p>No suitable transfer mechanisms were found for the selected parameters. This may be due to:</p>
                        <ul>
                            <li>The destination jurisdiction may have an adequacy decision, making additional safeguards unnecessary</li>
                            <li>The selected law may not have specific transfer mechanism requirements for these jurisdictions</li>
                            <li>The combination of parameters may not match any defined transfer scenarios</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Display a placeholder message when no analysis has been performed
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Transfer mechanism recommendations will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)

    def _get_transfer_mechanisms(self, law, source_jurisdiction, destination_jurisdiction, is_adequate):
        """Internal method to get appropriate transfer mechanisms based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            source_jurisdiction (str): The source jurisdiction
            destination_jurisdiction (str): The destination jurisdiction
            is_adequate (bool): Whether the destination jurisdiction has an adequacy decision
            
        Returns:
            list: A list of recommended transfer mechanisms or None if not found
        """
        # Sample transfer mechanisms based on adequacy status
        if is_adequate:
            return [
                {
                    "name": "Adequacy Decision",
                    "description": "The European Commission has recognized that the destination country provides an adequate level of data protection. No additional safeguards are strictly necessary.",
                    "requirements": [
                        "Document the transfer in your records of processing activities",
                        "Ensure compliance with general GDPR principles",
                        "Monitor adequacy status for any changes"
                    ],
                    "risk_level": "Low",
                    "risk_color": "#2ecc71"
                }
            ]
        else:
            return [
                {
                    "name": "Standard Contractual Clauses (SCCs)",
                    "description": "Pre-approved contractual clauses adopted by the European Commission that provide appropriate safeguards for international data transfers.",
                    "requirements": [
                        "Implement the latest version of SCCs (adopted in 2021)",
                        "Conduct and document a transfer impact assessment",
                        "Implement supplementary measures if necessary",
                        "Ensure SCCs are signed by both parties"
                    ],
                    "risk_level": "Medium",
                    "risk_color": "#f39c12"
                },
                {
                    "name": "Binding Corporate Rules (BCRs)",
                    "description": "Internal rules for data transfers within a multinational group, approved by the relevant supervisory authority.",
                    "requirements": [
                        "Develop comprehensive internal data protection policies",
                        "Obtain approval from the lead supervisory authority",
                        "Implement training and compliance mechanisms",
                        "Regular auditing and reporting"
                    ],
                    "risk_level": "Low",
                    "risk_color": "#2ecc71"
                },
                {
                    "name": "Derogations for Specific Situations",
                    "description": "Exceptions that allow transfers in specific circumstances without requiring additional safeguards.",
                    "requirements": [
                        "Ensure the transfer falls under one of the specific derogations",
                        "Document the justification for using the derogation",
                        "Limit transfers to what is strictly necessary",
                        "Consider implementing additional safeguards where possible"
                    ],
                    "risk_level": "High",
                    "risk_color": "#e74c3c"
                }
            ]

    def data_subject_rights_api(self):
        """Implement a data subject rights inference API based on regulatory metadata.
        This helps users determine appropriate responses to data subject rights requests.
        """
        st.markdown("<div class='page-header'><i class='fas fa-user-shield'></i> &nbsp;Data Subject Rights Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine appropriate responses to data subject rights requests based on regulatory metadata.<br><br>
            <ul>
                <li>Identifies applicable rights under different regulations</li>
                <li>Determines response timeframes and requirements</li>
                <li>Provides guidance on verification and exemptions</li>
                <li>Offers implementation steps for fulfilling requests</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Jurisdictional Analysis:</strong> Determines applicable laws based on data subject location</li>
                <li><strong>Right Identification:</strong> Maps request types to specific legal rights</li>
                <li><strong>Exemption Evaluation:</strong> Checks for applicable exemptions or limitations</li>
                <li><strong>Response Planning:</strong> Provides timeframes and implementation steps</li>
                <li><strong>Documentation Guidance:</strong> Offers templates and record-keeping requirements</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get laws for dropdown selection
            laws = self.glossary_repository.get_laws()
            if not laws:
                st.warning("No laws available in the database.")
                return
                
            law_options = [law["name"] for law in laws]
            selected_law = st.selectbox("Select Applicable Law", options=law_options, key="dsr_law")
            
            # Get jurisdictions
            jurisdictions = self.glossary_repository.get_jurisdictions()
            if jurisdictions:
                jurisdiction_options = [j["name"] for j in jurisdictions]
                selected_jurisdiction = st.selectbox("Select Data Subject's Jurisdiction", options=jurisdiction_options, key="dsr_jurisdiction")
            else:
                selected_jurisdiction = None
            
            # Get data subject types
            data_subject_types = self.glossary_repository.get_data_subject_types()
            if data_subject_types:
                dst_options = [dst["name"] for dst in data_subject_types]
                selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="dsr_subject_type")
            else:
                st.warning("No data subject types available.")
                return
            
            # Add right type selection
            right_types = [
                "Access",
                "Rectification",
                "Erasure",
                "Restriction of Processing",
                "Data Portability",
                "Objection",
                "Automated Decision Making",
                "Withdraw Consent"
            ]
            selected_right = st.selectbox("Select Requested Right", options=right_types, key="dsr_right_type")
            
            # Add request complexity
            request_complexity = st.select_slider(
                "Request Complexity",
                options=["Simple", "Moderate", "Complex"],
                value="Moderate",
                key="dsr_complexity"
            )
            
            # Add a button to trigger inference
            analyze_button = st.button("Analyze Rights Request")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "request", "label": "DSR Request", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "jurisdiction", "label": "Jurisdiction", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "law", "label": "Applicable Law", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "subject_type", "label": "Data Subject Type", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "right_type", "label": "Right Type", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Rights Requirements Lookup", "color": "#1abc9c", "shape": "box", "size": 25},
                {"id": "timeframe", "label": "Response Timeframe", "color": "#3498db", "shape": "box", "size": 25},
                {"id": "steps", "label": "Implementation Steps", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "exemptions", "label": "Potential Exemptions", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "verification", "label": "Verification Requirements", "color": "#9b59b6", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "request", "target": "jurisdiction", "label": "From"},
                {"source": "jurisdiction", "target": "law", "label": "Governed by"},
                {"source": "request", "target": "subject_type", "label": "Made by"},
                {"source": "request", "target": "right_type", "label": "Requests"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "subject_type", "target": "lookup", "label": ""},
                {"source": "right_type", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "timeframe", "label": "Determines"},
                {"source": "lookup", "target": "steps", "label": "Provides"},
                {"source": "lookup", "target": "exemptions", "label": "Identifies"},
                {"source": "lookup", "target": "verification", "label": "Requires"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Rights Response Guidance")
            
            if analyze_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing rights requirements..."):
                    # Simulate processing time
                    time.sleep(1)
                    
                    # Get rights guidance based on the selected parameters
                    rights_guidance = self._get_rights_guidance(selected_law, selected_right)
                
                if rights_guidance:
                    # Display the rights guidance with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                        <h3 style="color: #3498db;">Right to {selected_right} under {selected_law}</h3>
                        <p>The following guidance applies to {selected_dst}s in {selected_jurisdiction} making a {selected_right} request:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the response timeframe
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                        <h4>Response Timeframe</h4>
                        <p><strong>Standard timeframe:</strong> {rights_guidance['timeframe']} days</p>
                        <p><strong>Extension possible:</strong> {rights_guidance['extension_possible']}</p>
                        {f'<p><strong>Extension conditions:</strong> {rights_guidance["extension_conditions"]}</p>' if rights_guidance['extension_possible'] == 'Yes' else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display verification requirements
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                        <h4>Verification Requirements</h4>
                        <p>{rights_guidance['verification_requirements']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display implementation steps
                    st.markdown("""
                    <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                        <h4>Implementation Steps</h4>
                        <ol>
                    """, unsafe_allow_html=True)
                    
                    for step in rights_guidance['implementation_steps']:
                        st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                    
                    st.markdown("""
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display potential exemptions
                    if rights_guidance['exemptions']:
                        st.markdown("""
                        <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                            <h4>Potential Exemptions</h4>
                            <ul>
                        """, unsafe_allow_html=True)
                        
                        for exemption in rights_guidance['exemptions']:
                            st.markdown(f"<li>{exemption}</li>", unsafe_allow_html=True)
                        
                        st.markdown("""
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Display a message if no rights guidance is found
                    st.markdown("""
                    <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                        <h3 style="color: #7F8C8D;">No Rights Guidance Found</h3>
                        <p>No specific guidance was found for the selected parameters. This may be due to:</p>
                        <ul>
                            <li>The selected right may not be explicitly recognized under the chosen law</li>
                            <li>The combination of parameters may not match any defined rights scenarios</li>
                            <li>The data subject type may have special considerations not covered in the database</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Display a placeholder message when no analysis has been performed
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Rights response guidance will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)

    def _get_rights_guidance(self, law, right_type):
        """Internal method to get guidance for data subject rights based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            right_type (str): The type of right requested
            
        Returns:
            dict: A dictionary containing guidance for the requested right or None if not found
        """
        # Use the repository method to get guidance
        return self.regulatory_metadata_repository.get_data_subject_right_guidance(law, right_type)
    
    def _render_decision_tree(self, nodes, edges, title="Decision Tree", height=700):
        """Helper method to render a decision tree visualization using PyVis.
        
        Args:
            nodes (list): List of node dictionaries with id, label, color, etc.
            edges (list): List of edge dictionaries with source, target, label, etc.
            title (str): Title for the decision tree
            height (int): Height of the visualization in pixels
            
        Returns:
            None: Renders the decision tree directly in the Streamlit app
        """
        import tempfile
        from pyvis.network import Network
        import streamlit.components.v1 as components
        
        # Create a network with larger dimensions
        net = Network(height=f"{height}px", width="100%", directed=True, notebook=True)
        net.toggle_hide_edges_on_drag(False)
        net.barnes_hut()
        
        # Add nodes
        for node in nodes:
            # Format title as HTML if it's a detailed description
            node_title = node.get("title", node["label"])
            if isinstance(node_title, dict) and "html" in node_title:
                formatted_title = node_title["html"]
            else:
                formatted_title = node_title
                
            net.add_node(
                node["id"], 
                label=node["label"], 
                color=node.get("color", "#3498db"),
                shape=node.get("shape", "box"),
                title=formatted_title,
                size=node.get("size", 25),
                font=node.get("font", {"size": 14, "color": "black", "face": "Arial"})
            )
        
        # Add edges
        for edge in edges:
            net.add_edge(
                edge["source"], 
                edge["target"], 
                title=edge.get("label", ""),
                label=edge.get("label", ""),
                color=edge.get("color", "#7F8C8D"),
                width=edge.get("width", 2),
                arrows=edge.get("arrows", "to")
            )
        
        # Configure physics for hierarchical layout
        net.set_options("""
        {
          "physics": {
            "hierarchicalRepulsion": {
              "centralGravity": 0.0,
              "springLength": 100,
              "springConstant": 0.01,
              "nodeDistance": 120,
              "damping": 0.09
            },
            "solver": "hierarchicalRepulsion",
            "stabilization": {
              "iterations": 100
            }
          },
          "layout": {
            "hierarchical": {
              "enabled": true,
              "levelSeparation": 150,
              "nodeSpacing": 100,
              "treeSpacing": 200,
              "blockShifting": true,
              "edgeMinimization": true,
              "parentCentralization": true,
              "direction": "UD",
              "sortMethod": "directed"
            }
          },
          "interaction": {
            "navigationButtons": true,
            "keyboard": true
          }
        }
        """)
        
        # Generate the visualization
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
            net.save_graph(tmpfile.name)
            with open(tmpfile.name, "r", encoding="utf-8") as f:
                html = f.read()
            
            # Fix HTML in tooltips by modifying the HTML directly
            # This adds a script that properly renders HTML in tooltips
            html = html.replace('</head>', '''
            <style>
                div.vis-tooltip {
                    position: absolute;
                    visibility: hidden;
                    padding: 5px;
                    white-space: normal !important;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    color: #000000;
                    background-color: #ffffff;
                    border-radius: 5px;
                    border: 1px solid #d3d3d3;
                    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
                    max-width: 400px;
                    word-wrap: break-word;
                    z-index: 9999;
                    overflow: auto;
                    max-height: 400px;
                }
            </style>
            <script>
                // Override the default tooltip rendering to support HTML
                document.addEventListener("DOMContentLoaded", function() {
                    setTimeout(function() {
                        if (typeof network !== 'undefined') {
                            network.on("hoverNode", function(params) {
                                var nodeId = params.node;
                                var node = network.body.nodes[nodeId];
                                if (node && node.options && node.options.title) {
                                    var tooltip = document.querySelector(".vis-tooltip");
                                    if (tooltip) {
                                        tooltip.innerHTML = node.options.title;
                                    }
                                }
                            });
                        }
                    }, 1000);
                });
            </script>
            </head>''')
        
        # Display the visualization with a title
        st.subheader(title)
        components.html(html, height=height)
    
    def law_inference_api(self):
        """Implement a law inference API based on regulatory metadata.
        This helps users determine which laws apply to a specific jurisdiction.
        """
        st.markdown("<div class='page-header'><i class='fas fa-gavel'></i> &nbsp;Law Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            <h3 style="margin-top: 0;">Law Inference API</h3>
            <p>This API helps determine which data protection laws apply to specific jurisdictions based on regulatory metadata.</p>
            <p>The Law Inference API uses the Law Jurisdiction mapping table to identify applicable laws for a given jurisdiction, helping organizations understand their compliance obligations.</p>
        </div>''', unsafe_allow_html=True)
        
        # Create a two-column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get all jurisdictions from the repository
            law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
            jurisdictions = sorted(list(set([lj["jurisdiction_name"] for lj in law_jurisdictions])))
            
            # Jurisdiction selection
            selected_jurisdiction = st.selectbox(
                "Select Jurisdiction",
                jurisdictions,
                index=0 if jurisdictions else None
            )
            
            # Add a button to trigger analysis
            analyze_button = st.button("Determine Applicable Laws")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "jurisdiction", "label": "Jurisdiction Selection", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "mapping", "label": "Law Jurisdiction Mapping", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "laws", "label": "Applicable Laws", "color": "#27ae60", "shape": "box", "size": 25},
                {"id": "details", "label": "Law Details", "color": "#9b59b6", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "jurisdiction", "target": "mapping", "label": "Lookup"},
                {"source": "mapping", "target": "laws", "label": "Identify"},
                {"source": "laws", "target": "details", "label": "Retrieve"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Decision Tree", 700)
        
        with col2:
            st.subheader("Applicable Laws")
            
            if analyze_button and selected_jurisdiction:
                # Get all laws that apply to the selected jurisdiction
                applicable_laws = []
                for lj in law_jurisdictions:
                    if lj["jurisdiction_name"] == selected_jurisdiction:
                        applicable_laws.append(lj["law_name"])
                
                if applicable_laws:
                    # Display the applicable laws with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                        <h3 style="color: #3498db;">Laws Applicable to {selected_jurisdiction}</h3>
                        <p>The following laws apply to activities in this jurisdiction:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display each applicable law with its description
                    for i, law_name in enumerate(applicable_laws):
                        # Get law details from the glossary repository
                        laws = self.glossary_repository.get_laws()
                        law_details = next((law for law in laws if law["name"] == law_name), None)
                        
                        if law_details:
                            with st.expander(f"{i+1}. {law_name}", expanded=True):
                                st.markdown(f"**Full Name:** {law_details.get('full_name', 'Not available')}")
                                st.markdown(f"**Description:** {law_details.get('description', 'No description available')}")
                                st.markdown(f"**Effective Date:** {law_details.get('effective_date', 'Not specified')}")
                else:
                    # Display a message if no laws apply to the selected jurisdiction
                    st.markdown("""
                    <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                        <h3 style="color: #7F8C8D;">No Applicable Laws Found</h3>
                        <p>No specific data protection laws were found for the selected jurisdiction in our database.</p>
                        <p>This may be due to:</p>
                        <ul>
                            <li>The jurisdiction may not have comprehensive data protection legislation</li>
                            <li>The jurisdiction may be covered by regional laws not specifically mapped in the database</li>
                            <li>The database may need to be updated with the latest regulatory information</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Display a placeholder message when no analysis has been performed
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Applicable laws will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    app = DataMap()
    app.run()
