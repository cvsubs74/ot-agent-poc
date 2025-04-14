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
import plotly.express as px
import plotly.graph_objects as go

from repositories.GlossaryRepository import GlossaryRepository
from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.InventoryRepository import InventoryRepository
from repositories.DatabaseManager import DatabaseManager
from repositories.ObligationRepository import ObligationRepository

class DataMap:
    def __init__(self):
        """Initialize the DataMap application with repositories."""
        self.database_manager = DatabaseManager()
        self.glossary_repository = GlossaryRepository(self.database_manager.connection)
        self.regulatory_metadata_repository = RegulatoryMetadataRepository(self.database_manager.connection)
        self.inventory_repository = InventoryRepository(self.database_manager.connection)
        self.obligation_repository = ObligationRepository(self.database_manager.connection)
        
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
            "Data Subject Types", "Data Categories", "Sensitivity", "Purpose Categories", "Breach Types", "Obligations", "Risks"
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
        

        
        # Sensitivity tab
        with tabs[6]:
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
        with tabs[7]:
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
        with tabs[8]:
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
                
        # Obligations tab
        with tabs[9]:
            st.subheader("Obligations")
            st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides information about regulatory and security obligations that organizations must fulfill.</p>
                <ul>
                    <li>Detailed descriptions of each obligation and its requirements</li>
                    <li>Tracks implementation status and policy linkage</li>
                    <li>Filter by control type, status, and source</li>
                    <li>Supports compliance with various regulations and standards</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Get obligations from repository
            obligations = self.obligation_repository.get_obligations()
            if obligations:
                # Create filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Get unique control types
                    control_types = sorted(list(set([obl["control_type"] for obl in obligations if obl["control_type"]]))) 
                    control_types = ["All"] + control_types
                    selected_control = st.selectbox("Filter by Control Type", control_types, key="obl_control_filter")
                
                with col2:
                    # Get unique statuses
                    statuses = sorted(list(set([obl["status"] for obl in obligations if obl["status"]]))) 
                    statuses = ["All"] + statuses
                    selected_status = st.selectbox("Filter by Status", statuses, key="obl_status_filter")
                
                with col3:
                    # Get unique sources
                    sources = sorted(list(set([obl["source"] for obl in obligations if obl["source"]]))) 
                    sources = ["All"] + sources
                    selected_source = st.selectbox("Filter by Source", sources, key="obl_source_filter")
                
                # Create dataframe
                df = pd.DataFrame(obligations)
                df = df.rename(columns={
                    "id": "ID",
                    "name": "Obligation",
                    "description": "Description",
                    "source": "Source",
                    "control_type": "Control Type",
                    "status": "Status",
                    "policy_name": "Policy",
                    "risk_accepted": "Risk Accepted",
                    "created_at": "Created At"
                })
                
                # Apply filters
                if selected_control != "All":
                    df = df[df["Control Type"] == selected_control]
                if selected_status != "All":
                    df = df[df["Status"] == selected_status]
                if selected_source != "All":
                    df = df[df["Source"] == selected_source]
                
                # Reorder columns for better display
                display_columns = ["ID", "Obligation", "Description", "Source", "Control Type", "Status", "Policy", "Risk Accepted"]
                df = df[display_columns]
                
                # Display the dataframe
                st.dataframe(df, use_container_width=True)
                
                # Add new obligation section
                with st.expander("Add New Obligation", expanded=False):
                    with st.form("add_obligation_form"):
                        obligation_name = st.text_input("Obligation Name")
                        obligation_desc = st.text_area("Description")
                        obligation_source = st.text_input("Source (e.g., Regulation, Standard)")
                        obligation_control = st.selectbox(
                            "Control Type",
                            ["Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"],
                            key="new_obligation_control"
                        )
                        obligation_status = st.selectbox(
                            "Status",
                            ["Open", "In Progress", "Implemented", "Accepted Risk"],
                            key="new_obligation_status"
                        )
                        
                        submitted = st.form_submit_button("Add Obligation")
                        if submitted:
                            if obligation_name and obligation_desc:
                                # Add the obligation to the repository
                                new_id = self.obligation_repository.add_obligation(
                                    obligation_name, obligation_desc, obligation_source, 
                                    obligation_control, obligation_status
                                )
                                if new_id:
                                    st.success(f"Obligation '{obligation_name}' added successfully!")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to add obligation. Please try again.")
                            else:
                                st.warning("Obligation Name and Description are required.")
            else:
                st.warning("No obligations available in the database.")
        
        # Risks tab
        with tabs[10]:
            st.subheader("Risks")
            st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This section provides information about potential privacy and security risks that organizations may face when handling personal data.</p>
                <ul>
                    <li>Detailed descriptions of common privacy and security risks</li>
                    <li>Risk categorization by type (security, privacy, compliance, etc.)</li>
                    <li>Risk assessment information including likelihood and impact</li>
                    <li>Foundation for risk-based compliance decision making</li>
                </ul>
            </div>''', unsafe_allow_html=True)
            
            # Sample risk data (in a real implementation, this would come from a repository)
            risk_data = [
                {"id": 1, "name": "Unauthorized Data Access", "description": "Unauthorized individuals gain access to sensitive personal data due to inadequate access controls", "category": "Security", "likelihood": "High", "impact": "High"},
                {"id": 2, "name": "Data Breach", "description": "Personal data is exposed, lost, altered, or accessed without authorization", "category": "Security", "likelihood": "Medium", "impact": "High"},
                {"id": 3, "name": "Excessive Data Collection", "description": "Collection of personal data beyond what is necessary for the stated purpose", "category": "Privacy", "likelihood": "High", "impact": "Medium"},
                {"id": 4, "name": "Improper Data Retention", "description": "Retention of personal data beyond the necessary period for the stated purpose", "category": "Privacy", "likelihood": "High", "impact": "Medium"},
                {"id": 5, "name": "Inadequate Consent Management", "description": "Failure to obtain, record, or manage valid consent for data processing activities", "category": "Consent", "likelihood": "Medium", "impact": "High"},
                {"id": 6, "name": "Cross-Border Transfer Violations", "description": "Transfer of personal data to jurisdictions without adequate protection or proper transfer mechanisms", "category": "Transfer", "likelihood": "Medium", "impact": "High"},
                {"id": 7, "name": "Insufficient Data Subject Rights Management", "description": "Inability to fulfill data subject requests (access, deletion, portability, etc.) within required timeframes", "category": "Rights", "likelihood": "Medium", "impact": "Medium"},
                {"id": 8, "name": "Inadequate Security Controls", "description": "Lack of appropriate technical and organizational measures to protect personal data", "category": "Security", "likelihood": "Medium", "impact": "High"},
                {"id": 9, "name": "Vendor Non-Compliance", "description": "Third-party processors handling personal data without adequate contractual controls or compliance verification", "category": "Third Party", "likelihood": "High", "impact": "Medium"},
                {"id": 10, "name": "Incomplete Data Inventory", "description": "Incomplete or inaccurate records of data processing activities and data assets", "category": "Governance", "likelihood": "High", "impact": "Medium"}
            ]
            
            # Create filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Get unique risk categories
                categories = sorted(list(set([risk["category"] for risk in risk_data if risk["category"]]))) 
                categories = ["All"] + categories
                selected_category = st.selectbox("Filter by Risk Category", categories, key="risk_category_filter")
            
            with col2:
                # Get unique likelihood levels
                likelihoods = sorted(list(set([risk["likelihood"] for risk in risk_data if risk["likelihood"]]))) 
                likelihoods = ["All"] + likelihoods
                selected_likelihood = st.selectbox("Filter by Likelihood", likelihoods, key="risk_likelihood_filter")
            
            with col3:
                # Get unique impact levels
                impacts = sorted(list(set([risk["impact"] for risk in risk_data if risk["impact"]]))) 
                impacts = ["All"] + impacts
                selected_impact = st.selectbox("Filter by Impact", impacts, key="risk_impact_filter")
            
            # Create dataframe
            df = pd.DataFrame(risk_data)
            df = df.rename(columns={
                "id": "ID",
                "name": "Risk",
                "description": "Description",
                "category": "Risk Category",
                "likelihood": "Likelihood",
                "impact": "Impact"
            })
            
            # Apply filters
            if selected_category != "All":
                df = df[df["Risk Category"] == selected_category]
            if selected_likelihood != "All":
                df = df[df["Likelihood"] == selected_likelihood]
            if selected_impact != "All":
                df = df[df["Impact"] == selected_impact]
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
            
            # Add new risk section
            with st.expander("Add New Risk", expanded=False):
                with st.form("add_risk_form"):
                    risk_name = st.text_input("Risk Name")
                    risk_desc = st.text_area("Description")
                    risk_category = st.selectbox(
                        "Risk Category",
                        ["Security", "Privacy", "Consent", "Transfer", "Rights", "Third Party", "Governance", "Other"],
                        key="new_risk_category"
                    )
                    risk_likelihood = st.selectbox(
                        "Likelihood",
                        ["Low", "Medium", "High"],
                        key="new_risk_likelihood"
                    )
                    risk_impact = st.selectbox(
                        "Impact",
                        ["Low", "Medium", "High"],
                        key="new_risk_impact"
                    )
                    
                    # Submit button
                    submitted = st.form_submit_button("Add Risk")
                    if submitted:
                        st.success(f"Risk '{risk_name}' has been added successfully!")
        

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
            "Law Purpose Category Legal Basis",
            "Legal Basis Requirements",
            "Policy Purpose",
            "Policy Purpose Data Element",
            "Policy Purpose Data Usage",
            "Sensitivity Obligations",
            "Obligation Policy",
            "Obligation Risk"
        ]
        
        # Define which tabs are used by each inference API
        inference_api_mappings = {
            "All": list(range(len(all_tab_names))),  # All tabs
            "Law Inference": [0],  # Law Jurisdiction tab
            "Legal Basis Inference": [1, 10, 11],  # Law Legal Basis tab, Law Purpose Category Legal Basis, Legal Basis Requirements
            "Breach Notification Inference": [2],  # Law Incident Breach Notification tab
            "Transfer Mechanism Inference": [3],  # Law Transfer tab
            "Data Subject Rights Inference": [4],  # Data Subject Access Request tab
            "Data Sensitivity Inference": [5, 6, 7, 8, 9, 15],  # Various sensitivity-related tabs including Sensitivity Obligations
            "Policy Inference": [12, 13, 14],  # Policy Purpose, Policy Purpose Data Element, Policy Purpose Data Usage
            "Obligation Inference": [15, 16, 17],  # Sensitivity Obligations tab, Obligation Policy, Obligation Risk
            "Obligation Policy Mapping": [16],  # Obligation Policy tab
            "Obligation Risk Mapping": [17]  # Obligation Risk tab
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
        elif selected_inference_api == "Policy Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Policy Inference Works</h4>
                <p>The Policy Inference API uses purpose limitation principles to determine whether access to data is permitted based on organizational policies:</p>
                <ul>
                    <li><strong>Policy Purpose</strong>: Maps policies to business purposes, establishing which purposes are governed by which policies.</li>
                    <li><strong>Policy Purpose Data Element</strong>: Determines which data elements can be accessed for specific purpose-policy combinations.</li>
                    <li><strong>Policy Purpose Data Usage</strong>: Defines how data can be used (read, write, share) for each purpose, with specific restrictions.</li>
                </ul>
                <p>When making an access governance determination, the system considers:</p>
                <ul>
                    <li>The business purpose for data access</li>
                    <li>The specific data elements being requested</li>
                    <li>The type of operation (read, write, share)</li>
                    <li>Any context-specific restrictions</li>
                    <li>Data sensitivity levels</li>
                </ul>
                <p>The system helps organizations enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations and internal policies.</p>
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
            

            
                # Law Purpose Category Legal Basis tab
                elif tab_idx == 10 :
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
                elif tab_idx == 11:
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
                
                # Policy Purpose tab
                elif tab_idx == 12:
                    st.markdown("""
                    <div class="card">
                        <h3>Policy to Purpose Mapping</h3>
                        <p>This section maps organizational policies to business purposes, establishing which purposes are governed by which policies.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get policy purpose data from repository
                    policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
                    if policy_purposes:
                        policy_purpose_data = {
                            "Policy": [],
                            "Purpose": []
                        }
                        for pp in policy_purposes:
                            policy_purpose_data["Policy"].append(pp["policy_name"])
                            policy_purpose_data["Purpose"].append(pp["purpose_name"])
                        
                        # Create a DataFrame
                        df = pd.DataFrame(policy_purpose_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            policies = sorted(df["Policy"].unique())
                            selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="policy_purpose_policy_filter")
                        
                        with col2:
                            purposes = sorted(df["Purpose"].unique())
                            selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="policy_purpose_purpose_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_policy != "All":
                            filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                        if selected_purpose != "All":
                            filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                        
                        # Sort by Policy and Purpose
                        filtered_df = filtered_df.sort_values(by=["Policy", "Purpose"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No Policy Purpose mappings available in the database.")
                
                # Policy Purpose Data Element tab
                elif tab_idx == 13:
                    st.markdown("""
                    <div class="card">
                        <h3>Policy Purpose Data Element Mapping</h3>
                        <p>This section defines which data elements can be accessed for specific policy-purpose combinations, a key component of purpose-based access control.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get policy purpose data element data from repository
                    policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements()
                    if policy_purpose_data_elements:
                        ppde_data = {
                            "Policy": [],
                            "Purpose": [],
                            "Data Element": [],
                            "Access Allowed": []
                        }
                        for ppde in policy_purpose_data_elements:
                            ppde_data["Policy"].append(ppde["policy_name"])
                            ppde_data["Purpose"].append(ppde["purpose_name"])
                            ppde_data["Data Element"].append(ppde["data_element_name"])
                            ppde_data["Access Allowed"].append("Yes" if ppde["access_allowed"] else "No")
                        
                        # Create a DataFrame
                        df = pd.DataFrame(ppde_data)
                        
                        # Add filters
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            policies = sorted(df["Policy"].unique())
                            selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="ppde_policy_filter")
                        
                        with col2:
                            purposes = sorted(df["Purpose"].unique())
                            selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="ppde_purpose_filter")
                            
                        with col3:
                            data_elements = sorted(df["Data Element"].unique())
                            selected_data_element = st.selectbox("Filter by Data Element", ["All"] + list(data_elements), key="ppde_data_element_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_policy != "All":
                            filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                        if selected_purpose != "All":
                            filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                        if selected_data_element != "All":
                            filtered_df = filtered_df[filtered_df["Data Element"] == selected_data_element]
                        
                        # Sort by Policy, Purpose, and Data Element
                        filtered_df = filtered_df.sort_values(by=["Policy", "Purpose", "Data Element"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No Policy Purpose Data Element mappings available in the database.")
                
                # Policy Purpose Data Usage tab
                elif tab_idx == 14:
                    st.markdown("""
                    <div class="card">
                        <h3>Policy Purpose Data Usage Mapping</h3>
                        <p>This section defines how data can be used (read, write, share) for each purpose-policy-data element combination, with specific restrictions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get policy purpose data usage data from repository
                    policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages()
                    if policy_purpose_data_usages:
                        ppdu_data = {
                            "Policy": [],
                            "Purpose": [],
                            "Data Element": [],
                            "Operation": [],
                            "Allowed": [],
                            "Restrictions": []
                        }
                        for ppdu in policy_purpose_data_usages:
                            ppdu_data["Policy"].append(ppdu["policy_name"])
                            ppdu_data["Purpose"].append(ppdu["purpose_name"])
                            ppdu_data["Data Element"].append(ppdu["data_element_name"])
                            ppdu_data["Operation"].append(ppdu["operation"])
                            ppdu_data["Allowed"].append("Yes" if ppdu["allowed"] else "No")
                            ppdu_data["Restrictions"].append(ppdu["restrictions"] if ppdu["restrictions"] else "")
                        
                        # Create a DataFrame
                        df = pd.DataFrame(ppdu_data)
                        
                        # Add filters
                        col1, col2 = st.columns(2)
                        with col1:
                            policies = sorted(df["Policy"].unique())
                            selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="ppdu_policy_filter")
                        
                        with col2:
                            purposes = sorted(df["Purpose"].unique())
                            selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="ppdu_purpose_filter")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            data_elements = sorted(df["Data Element"].unique())
                            selected_data_element = st.selectbox("Filter by Data Element", ["All"] + list(data_elements), key="ppdu_data_element_filter")
                            
                        with col4:
                            operations = sorted(df["Operation"].unique())
                            selected_operation = st.selectbox("Filter by Operation", ["All"] + list(operations), key="ppdu_operation_filter")
                        
                        # Apply filters
                        filtered_df = df.copy()
                        if selected_policy != "All":
                            filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                        if selected_purpose != "All":
                            filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                        if selected_data_element != "All":
                            filtered_df = filtered_df[filtered_df["Data Element"] == selected_data_element]
                        if selected_operation != "All":
                            filtered_df = filtered_df[filtered_df["Operation"] == selected_operation]
                        
                        # Sort by Policy, Purpose, Data Element, and Operation
                        filtered_df = filtered_df.sort_values(by=["Policy", "Purpose", "Data Element", "Operation"])
                        
                        # Display the filtered data
                        st.dataframe(filtered_df)
                    else:
                        st.warning("No Policy Purpose Data Usage mappings available in the database.")
                 
                # Sensitivity Obligations tab
                elif tab_idx == 15:
                    st.markdown("""
                        <div class="card">
                            <h3>Sensitivity Obligations Mapping</h3>
                            <p>This section defines standard security and privacy obligations that should be applied based on data sensitivity levels.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                    # Get all sensitivities
                    sensitivities = self.glossary_repository.get_sensitivities()
                    
                    # Create a filter for sensitivity
                    sensitivity_options = {s["id"]: s["name"] for s in sensitivities}
                    sensitivity_options[0] = "All Sensitivities"
                    
                    selected_sensitivity_id = st.selectbox(
                        "Filter by Sensitivity Level",
                        options=list(sensitivity_options.keys()),
                        format_func=lambda x: sensitivity_options[x],
                        index=0,
                        key="sensitivity_filter"
                    )
                    
                    # Get sensitivity obligations with filter
                    sensitivity_id = None if selected_sensitivity_id == 0 else selected_sensitivity_id
                    sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                    
                    if sensitivity_obligations:
                        # Convert to DataFrame for display
                        df = pd.DataFrame(sensitivity_obligations)
                        # Rename columns for better display
                        df = df.rename(columns={
                            "id": "ID",
                            "sensitivity_name": "Sensitivity Level",
                            "obligation_name": "Standard Obligation",
                            "obligation_description": "Description",
                            "control_type": "Control Type",
                            "priority": "Priority"
                        })
                        
                        # Reorder columns for better display
                        display_columns = ["ID", "Sensitivity Level", "Standard Obligation", "Description", "Control Type", "Priority"]
                        df = df[display_columns]
                        
                        # Display the dataframe
                        st.dataframe(df, use_container_width=True)
                        
                        # Add explanation
                        st.markdown("""
                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h4 style="margin-top: 0;">How Sensitivity Obligations Work</h4>
                            <p>This mapping table defines the standard security and privacy controls that should be applied based on data sensitivity:</p>
                            <ul>
                                <li><strong>Special Category Data:</strong> Requires the highest level of protection with strict encryption, access controls, and monitoring</li>
                                <li><strong>Restricted Data:</strong> Requires strong protection measures including encryption and access restrictions</li>
                                <li><strong>Confidential Data:</strong> Requires moderate protection with basic encryption and access controls</li>
                                <li><strong>Internal Data:</strong> Requires standard organizational controls</li>
                                <li><strong>Public Data:</strong> Requires basic integrity controls</li>
                            </ul>
                            <p>These mappings are used by the Obligation Inference API to recommend appropriate controls based on data sensitivity.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("No sensitivity-obligation mappings available in the database.")
                
                # Obligation Policy tab
                elif tab_idx == 16:
                    st.markdown("""
                        <div class="card">
                            <h3>Obligation-Policy Mapping</h3>
                            <p>This section maps obligations to organizational policies, establishing which policies address specific compliance requirements.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Get all obligations
                    obligations = self.obligation_repository.get_obligations()
                    
                    # Create a filter for obligations
                    obligation_options = {o["id"]: o["name"] for o in obligations}
                    obligation_options[0] = "All Obligations"
                    
                    # Get all policies
                    policies = self.glossary_repository.get_policies()
                    
                    # Create a filter for policies
                    policy_options = {p["id"]: p["name"] for p in policies}
                    policy_options[0] = "All Policies"
                    
                    # Create filters
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        selected_obligation_id = st.selectbox(
                            "Filter by Obligation",
                            options=list(obligation_options.keys()),
                            format_func=lambda x: obligation_options[x],
                            index=0,
                            key="obligation_policy_obligation_filter"
                        )
                    
                    with col2:
                        selected_policy_id = st.selectbox(
                            "Filter by Policy",
                            options=list(policy_options.keys()),
                            format_func=lambda x: policy_options[x],
                            index=0,
                            key="obligation_policy_policy_filter"
                        )
                    
                    with col3:
                        control_types = ["All", "Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"]
                        selected_control_type = st.selectbox(
                            "Filter by Control Type",
                            options=control_types,
                            index=0,
                            key="obligation_policy_control_filter"
                        )
                    
                    # Get obligation-policy mappings from the repository
                    obligation_policy_data = self.obligation_repository.get_obligation_policies()
                    
                    # Filter the data based on selections
                    filtered_data = obligation_policy_data
                    if selected_obligation_id != 0:
                        filtered_data = [item for item in filtered_data if item["obligation_id"] == selected_obligation_id]
                    if selected_policy_id != 0:
                        filtered_data = [item for item in filtered_data if item["policy_id"] == selected_policy_id]
                    if selected_control_type != "All":
                        filtered_data = [item for item in filtered_data if item["control_type"] == selected_control_type]
                    
                    if filtered_data:
                        # Create a DataFrame
                        df = pd.DataFrame(filtered_data)
                        df = df.rename(columns={
                            "obligation_name": "Obligation",
                            "policy_name": "Policy",
                            "control_type": "Control Type",
                            "relevance_score": "Relevance Score"
                        })
                        
                        # Display columns in a specific order
                        display_columns = ["Obligation", "Policy", "Control Type", "Relevance Score"]
                        df = df[display_columns]
                        
                        # Sort by relevance score (descending)
                        df = df.sort_values(by=["Relevance Score"], ascending=False)
                        
                        # Display the dataframe
                        st.dataframe(df, use_container_width=True)
                        
                        # Add explanation
                        st.markdown("""
                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h4 style="margin-top: 0;">How Obligation-Policy Mapping Works</h4>
                            <p>The Obligation-Policy mapping establishes which organizational policies address specific compliance obligations:</p>
                            <ul>
                                <li><strong>Relevance Score:</strong> Indicates how directly a policy addresses an obligation (1.0 = perfect match)</li>
                                <li><strong>Control Type:</strong> Categorizes the type of control implemented by the obligation</li>
                                <li><strong>Multiple Policies:</strong> An obligation may be addressed by multiple policies with varying degrees of relevance</li>
                            </ul>
                            <p>This mapping enables organizations to demonstrate compliance by linking obligations to specific policy documents.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("No obligation-policy mappings match the selected filters.")
                
                # Obligation Risk tab
                elif tab_idx == 17:
                    st.markdown("""
                        <div class="card">
                            <h3>Obligation-Risk Mapping</h3>
                            <p>This section maps obligations to potential risks, establishing which risks may materialize if specific obligations are not fulfilled.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Get all obligations
                    obligations = self.obligation_repository.get_obligations()
                    
                    # Create a filter for obligations
                    obligation_options = {o["id"]: o["name"] for o in obligations}
                    obligation_options[0] = "All Obligations"
                    
                    # Sample risk data (in a real implementation, this would come from a repository)
                    risk_data = [
                        {"id": 1, "name": "Unauthorized Data Access", "category": "Security"},
                        {"id": 2, "name": "Data Breach", "category": "Security"},
                        {"id": 3, "name": "Excessive Data Collection", "category": "Privacy"},
                        {"id": 4, "name": "Improper Data Retention", "category": "Privacy"},
                        {"id": 5, "name": "Inadequate Consent Management", "category": "Consent"},
                        {"id": 6, "name": "Cross-Border Transfer Violations", "category": "Transfer"},
                        {"id": 7, "name": "Insufficient Data Subject Rights Management", "category": "Rights"},
                        {"id": 8, "name": "Inadequate Security Controls", "category": "Security"},
                        {"id": 9, "name": "Vendor Non-Compliance", "category": "Third Party"},
                        {"id": 10, "name": "Incomplete Data Inventory", "category": "Governance"}
                    ]
                    
                    # Create a filter for risks
                    risk_options = {r["id"]: r["name"] for r in risk_data}
                    risk_options[0] = "All Risks"
                    
                    # Create filters
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        selected_obligation_id = st.selectbox(
                            "Filter by Obligation",
                            options=list(obligation_options.keys()),
                            format_func=lambda x: obligation_options[x],
                            index=0,
                            key="obligation_risk_obligation_filter"
                        )
                    
                    with col2:
                        selected_risk_id = st.selectbox(
                            "Filter by Risk",
                            options=list(risk_options.keys()),
                            format_func=lambda x: risk_options[x],
                            index=0,
                            key="obligation_risk_risk_filter"
                        )
                    
                    with col3:
                        risk_categories = ["All", "Security", "Privacy", "Consent", "Transfer", "Rights", "Third Party", "Governance"]
                        selected_risk_category = st.selectbox(
                            "Filter by Risk Category",
                            options=risk_categories,
                            index=0,
                            key="obligation_risk_category_filter"
                        )
                    
                    # Get obligation-risk mappings from the repository
                    obligation_risk_data = self.obligation_repository.get_obligation_risks()
                    
                    # Filter the data based on selections
                    filtered_data = obligation_risk_data
                    if selected_obligation_id != 0:
                        filtered_data = [item for item in filtered_data if item["obligation_id"] == selected_obligation_id]
                    if selected_risk_id != 0:
                        filtered_data = [item for item in filtered_data if item["risk_id"] == selected_risk_id]
                    if selected_risk_category != "All":
                        filtered_data = [item for item in filtered_data if item.get("category", "") == selected_risk_category]
                    
                    if filtered_data:
                        # Create a DataFrame
                        df = pd.DataFrame(filtered_data)
                        # Create a mapping of columns that might exist in the data
                        column_mapping = {}
                        if "obligation_name" in df.columns:
                            column_mapping["obligation_name"] = "Obligation"
                        if "risk_name" in df.columns:
                            column_mapping["risk_name"] = "Risk"
                        if "category" in df.columns:
                            column_mapping["category"] = "Risk Category"
                        if "likelihood" in df.columns:
                            column_mapping["likelihood"] = "Likelihood"
                        if "impact" in df.columns:
                            column_mapping["impact"] = "Impact"
                        
                        # Rename columns that exist
                        df = df.rename(columns=column_mapping)
                        
                        # Display columns in a specific order, but only include columns that exist
                        display_columns = ["Obligation", "Risk", "Risk Category", "Likelihood", "Impact"]
                        available_columns = [col for col in display_columns if col in df.columns]
                        if available_columns:
                            df = df[available_columns]
                        
                        # Sort by risk category and likelihood, but only use columns that exist
                        sort_columns = []
                        if "Risk Category" in df.columns:
                            sort_columns.append("Risk Category")
                        if "Likelihood" in df.columns:
                            sort_columns.append("Likelihood")
                        if "Impact" in df.columns:
                            sort_columns.append("Impact")
                        
                        if sort_columns:
                            df = df.sort_values(by=sort_columns)
                        
                        # Display the dataframe
                        st.dataframe(df, use_container_width=True)
                        
                        # Add explanation
                        st.markdown("""
                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h4 style="margin-top: 0;">How Obligation-Risk Mapping Works</h4>
                            <p>The Obligation-Risk mapping identifies potential risks that may materialize if specific obligations are not fulfilled:</p>
                            <ul>
                                <li><strong>Risk Assessment:</strong> Each mapping includes the likelihood and impact of the risk materializing</li>
                                <li><strong>Risk Categories:</strong> Risks are categorized by type (security, privacy, etc.) for easier management</li>
                                <li><strong>Multiple Risks:</strong> An obligation may mitigate multiple risks with varying degrees of likelihood and impact</li>
                            </ul>
                            <p>This mapping enables organizations to make risk-based decisions about which obligations to prioritize and which risks to accept.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("No obligation-risk mappings match the selected filters.")
                    
    def assets_section(self):
        """Handle the Assets section with data elements."""
        st.markdown("<div class='page-header'><i class='fas fa-database'></i> &nbsp;Assets</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an inventory of data assets within the organization, including systems and applications that store or process data.</p>
            <ul>
                <li>Core systems that contain or process data</li>
                <li>Applications and databases that serve as data sources</li>
                <li>Systems that support business operations and data processing</li>
                <li>Data elements stored or processed by each asset</li>
            </ul>
        </div>''', unsafe_allow_html=True)

        # Get assets from repository
        assets = self.inventory_repository.get_assets()
        
        if not assets:
            st.warning("No assets available in the database.")
            return
        
        # Get asset data elements
        asset_data_elements = self.inventory_repository.get_asset_data_elements()
        
        # Group data elements by asset
        asset_to_data_elements = {}
        data_element_names = set()
        for ade in asset_data_elements:
            asset_id = ade['asset_id']
            if asset_id not in asset_to_data_elements:
                asset_to_data_elements[asset_id] = []
            
            data_element_name = ade['data_element_name']
            data_element_names.add(data_element_name)
            
            asset_to_data_elements[asset_id].append({
                'name': data_element_name,
                'description': ade['data_element_description']
            })
        
        # Filter by data element
        data_element_options = list(data_element_names)
        data_element_options.sort()
        selected_data_elements = st.multiselect(
            "Filter by Data Element",
            options=data_element_options,
            help="Select one or more data elements to filter assets"
        )
        
        # Apply filters
        filtered_assets = assets
        if selected_data_elements:
            # Filter assets that contain ALL of the selected data elements (AND logic)
            filtered_asset_ids = set()
            for asset_id, data_elements in asset_to_data_elements.items():
                de_names = {de['name'] for de in data_elements}
                # Check if ALL selected data elements are in this asset's data elements
                if all(de_name in de_names for de_name in selected_data_elements):
                    filtered_asset_ids.add(asset_id)
            
            filtered_assets = [asset for asset in assets if asset['id'] in filtered_asset_ids]
        
        # Create a DataFrame for all assets
        asset_data = {
            "Asset": [],
            "Description": [],
            "Type": [],
            "Status": [],
            "Data Element Count": []
        }
        
        for asset in filtered_assets:
            # Get data elements for this asset
            data_elements = asset_to_data_elements.get(asset['id'], [])
            
            # Add to DataFrame
            asset_data["Asset"].append(asset['name'])
            asset_data["Description"].append(asset['description'])
            asset_data["Type"].append(asset.get('type', 'N/A'))
            asset_data["Status"].append(asset.get('status', 'Active'))
            asset_data["Data Element Count"].append(len(data_elements))
        
        # Convert to DataFrame for display
        df = pd.DataFrame(asset_data)
        
        # Remove any empty rows
        df = df.dropna(how='all')
        
        # Display the DataFrame with a fixed height to avoid empty rows
        st.dataframe(df, use_container_width=True, height=min(400, len(df) * 35 + 38))
        
        # Add a selectbox to choose an asset
        asset_names = [asset['name'] for asset in filtered_assets]
        if asset_names:
            selected_asset_name = st.selectbox("Select an asset to view details", asset_names)
            
            # Find the selected asset
            selected_asset = next((asset for asset in filtered_assets if asset['name'] == selected_asset_name), None)
            
            with st.container():
                # Create a card-like container with custom styling
                card_header = f'''
                <div style="background-color: white; border-radius: 10px 10px 0 0; padding: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">
                    <h3 style="color: #2c3e50; margin-top: 0;">{selected_asset['name']}</h3>
                    <p style="color: #7f8c8d;">{selected_asset['description']}</p>
                    <p><span style="background-color: #e8f4f8; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">{selected_asset.get('status', 'Active')}</span></p>
                </div>
                '''
                st.markdown(card_header, unsafe_allow_html=True)
                
                # Create a card for expanders
                card_body = '<div style="background-color: white; border-radius: 0 0 10px 10px; padding: 0 15px 15px 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">'
                st.markdown(card_body, unsafe_allow_html=True)
                
                # Get data elements for this asset
                data_elements = asset_to_data_elements.get(selected_asset['id'], [])
                
                if data_elements:
                    with st.expander(f"Data Elements ({len(data_elements)})"): 
                        # Create a DataFrame for the data elements
                        de_data = {
                            "Data Element": [],
                            "Description": []
                        }
                        
                        for de in data_elements:
                            de_data["Data Element"].append(de['name'])
                            de_data["Description"].append(de['description'])
                        
                        # Display the data elements in a styled dataframe
                        st.dataframe(pd.DataFrame(de_data), use_container_width=True)
                    
                    # Add buttons for obligation inference, policy recommendations, and risk recommendations
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        infer_obligations = st.button("Infer Obligations", key=f"infer_obligations_{selected_asset['id']}")
                    
                    with col2:
                        recommend_policies = st.button("Recommend Policies", key=f"recommend_policies_{selected_asset['id']}")
                    
                    with col3:
                        recommend_risks = st.button("Recommend Risks", key=f"recommend_risks_{selected_asset['id']}")
                    
                    # Handle Infer Obligations button
                    if infer_obligations:
                        # Get data element sensitivities
                        data_element_sensitivities = self.infer_data_element_sensitivities(data_elements)
                        
                        if data_element_sensitivities:
                            st.subheader("Data Element Sensitivity Analysis")
                            
                            # Create a DataFrame for the data element sensitivities
                            sens_data = {
                                "Data Element": [],
                                "Sensitivity": [],
                                "Source": []
                            }
                            
                            for de_name, sensitivity_info in data_element_sensitivities.items():
                                sens_data["Data Element"].append(de_name)
                                sens_data["Sensitivity"].append(sensitivity_info['sensitivity'])
                                sens_data["Source"].append(sensitivity_info['source'])
                            
                            # Display the data element sensitivities
                            st.dataframe(pd.DataFrame(sens_data), use_container_width=True)
                            
                            # Get obligations based on sensitivities
                            self.show_sensitivity_based_obligations(data_element_sensitivities)
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                    
                    # Handle Recommend Policies button
                    if recommend_policies:
                        # Get data element sensitivities first
                        data_element_sensitivities = self.infer_data_element_sensitivities(data_elements)
                        
                        if data_element_sensitivities:
                            # First get the obligations based on sensitivities
                            sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
                            all_sensitivities = self.glossary_repository.get_sensitivities()
                            sensitivity_ids = {}
                            
                            for sensitivity in all_sensitivities:
                                if sensitivity['name'] in sensitivity_levels:
                                    sensitivity_ids[sensitivity['name']] = sensitivity['id']
                            
                            # Get all obligations for these sensitivity levels
                            all_obligations = []
                            for sensitivity_name, sensitivity_id in sensitivity_ids.items():
                                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                                if sensitivity_obligations:
                                    for so in sensitivity_obligations:
                                        all_obligations.append({
                                            "id": so["obligation_id"],  # Using the actual obligation_id now
                                            "name": so["obligation_name"],
                                            "control_type": so["control_type"],
                                            "priority": so["priority"]
                                        })
                            
                            if all_obligations:
                                # Now get policies for these obligations
                                self.show_obligation_based_policies(all_obligations)
                            else:
                                st.warning("No obligations found for the sensitivities.")
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                    
                    # Handle Recommend Risks button
                    if recommend_risks:
                        # Get data element sensitivities first
                        data_element_sensitivities = self.infer_data_element_sensitivities(data_elements)
                        
                        if data_element_sensitivities:
                            # First get the obligations based on sensitivities
                            sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
                            all_sensitivities = self.glossary_repository.get_sensitivities()
                            sensitivity_ids = {}
                            
                            for sensitivity in all_sensitivities:
                                if sensitivity['name'] in sensitivity_levels:
                                    sensitivity_ids[sensitivity['name']] = sensitivity['id']
                            
                            # Get all obligations for these sensitivity levels
                            all_obligations = []
                            for sensitivity_name, sensitivity_id in sensitivity_ids.items():
                                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                                if sensitivity_obligations:
                                    for so in sensitivity_obligations:
                                        all_obligations.append({
                                            "id": so["obligation_id"],  # Using the actual obligation_id now
                                            "name": so["obligation_name"],
                                            "control_type": so["control_type"],
                                            "priority": so["priority"]
                                        })
                            
                            if all_obligations:
                                # Now get risks for these obligations
                                self.show_obligation_based_risks(all_obligations)
                            else:
                                st.warning("No obligations found for the sensitivities.")
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                else:
                    st.info(f"No data elements associated with {selected_asset['name']}")
                
                # Close the card div
                st.markdown('</div>', unsafe_allow_html=True)
        
    def infer_sensitivity(self, data_element_id=None, data_category_id=None, data_subject_type_id=None, law_id=None, jurisdiction_id=None):
        """Infer sensitivity level based on provided parameters.
        
        This method determines the sensitivity level using different approaches based on the parameters provided:
        1. If data_element_id and data_subject_type_id are provided, it checks direct data element sensitivity mappings
        2. If data_category_id and data_subject_type_id are provided, it checks data category sensitivity mappings
        3. If law_id is also provided, it checks law-specific sensitivity mappings
        4. If only data_element_id is provided, it tries to find any sensitivity mapping for that element
        5. If only data_category_id is provided, it tries to find any sensitivity mapping for that category
        
        Args:
            data_element_id: ID of the data element (optional)
            data_category_id: ID of the data category (optional)
            data_subject_type_id: ID of the data subject type (optional)
            law_id: ID of the law (optional)
            jurisdiction_id: ID of the jurisdiction (optional, used to find applicable laws)
            
        Returns:
            Dictionary with sensitivity_id, sensitivity_name, and source information
            or None if no sensitivity could be determined
        """
        # Initialize result
        result = None
        
        # Case 1: Direct lookup with data element, data subject type, and law
        if data_element_id and data_subject_type_id and law_id:
            # Get all law data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['law_id'] == law_id and 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Law-specific data element sensitivity'
                }
                return result
        
        # Case 2: Direct lookup with data category, data subject type, and law
        if data_category_id and data_subject_type_id and law_id:
            # Get all law data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['law_id'] == law_id and 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Law-specific data category sensitivity'
                }
                return result
        
        # Case 3: Direct lookup with data element and data subject type (no specific law)
        if data_element_id and data_subject_type_id:
            # Get all data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Data element sensitivity'
                }
                return result
        
        # Case 4: Direct lookup with data category and data subject type (no specific law)
        if data_category_id and data_subject_type_id:
            # Get all data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Data category sensitivity'
                }
                return result
        
        # Case 5: Find applicable laws based on jurisdiction and check their sensitivities
        if jurisdiction_id and (data_element_id or data_category_id) and data_subject_type_id:
            # Get all law jurisdictions
            law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
            
            # Filter for the specific jurisdiction
            applicable_laws = []
            for lj in law_jurisdictions:
                if lj['jurisdiction_id'] == jurisdiction_id:
                    applicable_laws.append({
                        'id': lj['law_id'],
                        'name': lj['law_name']
                    })
            
            for law in applicable_laws:
                # Try with data element first
                if data_element_id:
                    # Recursive call with the specific law
                    law_result = self.infer_sensitivity(
                        data_element_id=data_element_id,
                        data_subject_type_id=data_subject_type_id,
                        law_id=law['id']
                    )
                    
                    if law_result:
                        law_result['source'] = f'Jurisdiction-derived law ({law["name"]}) data element sensitivity'
                        return law_result
                
                # Then try with data category
                if data_category_id:
                    # Recursive call with the specific law
                    law_result = self.infer_sensitivity(
                        data_category_id=data_category_id,
                        data_subject_type_id=data_subject_type_id,
                        law_id=law['id']
                    )
                    
                    if law_result:
                        law_result['source'] = f'Jurisdiction-derived law ({law["name"]}) data category sensitivity'
                        return law_result
        
        # Case 6: If we only have data_element_id, try to find any sensitivity mapping
        if data_element_id and not result:
            # Get all data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific data element
            matching = [s for s in all_sensitivities if s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'data_subject_type_id': matching[0]['data_subject_type_id'],
                    'data_subject_type_name': matching[0]['data_subject_type_name'],
                    'source': 'Any available data element sensitivity'
                }
                return result
            
            # If not found directly, try through data category
            data_category_mappings = self.regulatory_metadata_repository.get_data_category_data_elements()
            data_category_ids = [dcde['data_category_id'] for dcde in data_category_mappings 
                               if dcde['data_element_id'] == data_element_id]
            
            if data_category_ids:
                # Try each data category
                for dc_id in data_category_ids:
                    # Recursive call with the data category
                    dc_result = self.infer_sensitivity(data_category_id=dc_id)
                    if dc_result:
                        dc_result['source'] = 'Data element derived from data category sensitivity'
                        return dc_result
        
        # Case 7: If we only have data_category_id, try to find any sensitivity mapping
        if data_category_id and not result:
            # Get all data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific data category
            matching = [s for s in all_sensitivities if s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'data_subject_type_id': matching[0]['data_subject_type_id'],
                    'data_subject_type_name': matching[0]['data_subject_type_name'],
                    'source': 'Any available data category sensitivity'
                }
                return result
        
        # If no sensitivity found, return None
        return None
    
    def infer_data_element_sensitivities(self, data_elements):
        """Infer sensitivity levels for a list of data elements.
        
        Args:
            data_elements: List of data element dictionaries with 'id', 'name', and 'description' keys
            
        Returns:
            Dictionary mapping data element names to sensitivity levels and sources
        """
        # Initialize result dictionary
        sensitivities = {}
        
        # Get all data elements from the database to map names to IDs if needed
        all_data_elements = self.glossary_repository.get_data_elements()
        name_to_id_map = {de['name']: de['id'] for de in all_data_elements}
        
        # Process each data element
        for data_element in data_elements:
            # If we have an ID, use it directly
            if 'id' in data_element and data_element['id']:
                data_element_id = data_element['id']
            # Otherwise, try to find the ID by name
            elif data_element['name'] in name_to_id_map:
                data_element_id = name_to_id_map[data_element['name']]
            else:
                # Skip if we can't find the data element
                continue
            
            # Use the infer_sensitivity method to get the sensitivity
            sensitivity_result = self.infer_sensitivity(data_element_id=data_element_id)
            
            if sensitivity_result:
                sensitivities[data_element['name']] = {
                    'sensitivity': sensitivity_result['sensitivity_name'],
                    'source': sensitivity_result['source']
                }
            else:
                # If no sensitivity found, mark as 'Unknown'
                sensitivities[data_element['name']] = {
                    'sensitivity': 'Unknown',
                    'source': 'No sensitivity mapping found'
                }
        
        return sensitivities
    
    def show_sensitivity_based_obligations(self, data_element_sensitivities):
        """Show obligations based on data element sensitivities.
        
        Args:
            data_element_sensitivities: Dictionary mapping data element names to sensitivity info dictionaries
                                        with 'sensitivity' and 'source' keys
        """
        if not data_element_sensitivities:
            st.warning("No sensitivity information available.")
            return
        
        # Get unique sensitivity levels
        sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
        
        # Get sensitivity IDs for these levels
        all_sensitivities = self.glossary_repository.get_sensitivities()
        sensitivity_ids = {}
        for sensitivity in all_sensitivities:
            if sensitivity['name'] in sensitivity_levels:
                sensitivity_ids[sensitivity['name']] = sensitivity['id']
        # Get obligations for these sensitivity levels
        st.subheader("Recommended Obligations")
        
        all_obligations = []
        for sensitivity_name, sensitivity_id in sensitivity_ids.items():
            # Get sensitivity obligations
            sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
            
            if sensitivity_obligations:
                # Group by control type
                for so in sensitivity_obligations:
                    all_obligations.append({
                        "Sensitivity": sensitivity_name,
                        "Obligation": so["obligation_name"],
                        "Description": so["obligation_description"],
                        "Control Type": so["control_type"],
                        "Priority": so["priority"]
                    })
        
        if all_obligations:
            # Create a DataFrame
            df = pd.DataFrame(all_obligations)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                control_types = ["All"] + sorted(list(set(df["Control Type"])))
                selected_control = st.selectbox(
                    "Filter by Control Type",
                    control_types,
                    key="obligation_control_filter"
                )
            
            with col2:
                priorities = ["All"] + sorted(list(set(df["Priority"])))
                selected_priority = st.selectbox(
                    "Filter by Priority",
                    priorities,
                    key="obligation_priority_filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_control != "All":
                filtered_df = filtered_df[filtered_df["Control Type"] == selected_control]
            if selected_priority != "All":
                filtered_df = filtered_df[filtered_df["Priority"] == selected_priority]
            
            # Sort by Priority and Control Type
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            filtered_df["Priority Order"] = filtered_df["Priority"].map(priority_order)
            filtered_df = filtered_df.sort_values(by=["Priority Order", "Control Type"])
            filtered_df = filtered_df.drop(columns=["Priority Order"])
            
            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True)
            
            # Add explanation
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How the Obligation Inference Algorithm Works</h4>
                <p>The algorithm follows this functional flow:</p>
                <ul>
                    <li><strong>Input:</strong> Data elements from the selected asset</li>
                    <li><strong>Sensitivity Analysis:</strong> Determine sensitivity level for each data element</li>
                    <li><strong>Obligation Mapping:</strong> Match sensitivities to relevant security and privacy obligations</li>
                    <li><strong>Control Categorization:</strong> Group obligations by control type (Encryption, Access Control, etc.)</li>
                    <li><strong>Priority Assignment:</strong> Assign implementation priority based on data sensitivity</li>
                    <li><strong>Output:</strong> Prioritized list of security and privacy obligations</li>
                </ul>
                <p>The recommendations are prioritized as follows:</p>
                <ul>
                    <li><strong>High Priority:</strong> Critical controls that must be implemented to protect sensitive data</li>
                    <li><strong>Medium Priority:</strong> Important controls that should be implemented in most cases</li>
                    <li><strong>Low Priority:</strong> Recommended controls that enhance protection but may be optional</li>
                </ul>
                <p>These obligations can be used to guide your security and compliance implementation for this asset.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No obligations defined for these sensitivity levels.")
    
    def show_obligation_based_policies(self, obligations):
        """Show policies based on obligations.
        
        Args:
            obligations: List of obligation dictionaries with 'id', 'name', 'control_type', and 'priority' keys
        """
        if not obligations:
            st.warning("No obligation information available.")
            return
        
        st.subheader("Recommended Policies")
        
        # Get policies for the given obligations from the repository
        all_policies = []
        obligation_ids = [o["id"] for o in obligations]
        
        # Get policies for each obligation using the repository
        for obligation_id in obligation_ids:
            policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
            obligation_name = next((o["name"] for o in obligations if o["id"] == obligation_id), "Unknown")
            
            for policy in policies:
                all_policies.append({
                    "Obligation": obligation_name,
                    "Policy": policy["name"],
                    "Control Type": policy.get("control_type", ""),
                    "Relevance Score": policy["relevance_score"]
                })
        
        if all_policies:
            # Create a DataFrame
            df = pd.DataFrame(all_policies)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                policy_names = ["All"] + sorted(list(set(df["Policy"])))
                selected_policy = st.selectbox(
                    "Filter by Policy",
                    policy_names,
                    key="policy_name_filter"
                )
            
            with col2:
                control_types = ["All"] + sorted(list(set(df["Control Type"])))
                selected_control = st.selectbox(
                    "Filter by Control Type",
                    control_types,
                    key="policy_control_filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_policy != "All":
                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
            if selected_control != "All":
                filtered_df = filtered_df[filtered_df["Control Type"] == selected_control]
            
            # Sort by Relevance Score (descending)
            filtered_df = filtered_df.sort_values(by=["Relevance Score"], ascending=False)
            
            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True)
            
            # Group policies by type
            policy_groups = filtered_df.groupby("Policy")["Relevance Score"].max().sort_values(ascending=False)
            top_policies = policy_groups.index.tolist()
            
            # Display top policies summary
            st.subheader("Policy Implementation Summary")
            st.markdown("""
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">Recommended Policy Implementation</h4>
                <p>Based on the data elements in this asset and their sensitivity levels, the following policies should be implemented:</p>
                <ol>
            """, unsafe_allow_html=True)
            
            for policy in top_policies[:5]:  # Show top 5 policies
                st.markdown(f"<li><strong>{policy}</strong></li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ol>
                <p>These policies will address the compliance obligations required for the sensitive data in this asset.</p>
            </div>
            
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How the Policy Recommendation Algorithm Works</h4>
                <p>The algorithm follows this functional flow:</p>
                <ul>
                    <li><strong>Input:</strong> Security and privacy obligations from sensitivity analysis</li>
                    <li><strong>Policy Discovery:</strong> Identify organizational policies that address each obligation</li>
                    <li><strong>Relevance Assessment:</strong> Determine how relevant each policy is to the specific obligations</li>
                    <li><strong>Policy Prioritization:</strong> Rank policies by their relevance to the identified obligations</li>
                    <li><strong>Policy Grouping:</strong> Group related policies to provide comprehensive coverage</li>
                    <li><strong>Output:</strong> Prioritized list of policies to implement for the asset</li>
                </ul>
                <p>The relevance score indicates how important each policy is for addressing the identified obligations.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No policies found for the identified obligations.")
    
    def show_obligation_based_risks(self, obligations):
        """Show risks based on obligations.
        
        Args:
            obligations: List of obligation dictionaries with 'id', 'name', 'control_type', and 'priority' keys
        """
        if not obligations:
            st.warning("No obligation information available.")
            return
        
        st.subheader("Potential Risks")
        
        # Get risks for the given obligations from the repository
        all_risks = []
        obligation_ids = [o["id"] for o in obligations]
        
        # Get risks for each obligation using the repository
        for obligation_id in obligation_ids:
            risks = self.obligation_repository.get_risks_for_obligation(obligation_id)
            obligation_name = next((o["name"] for o in obligations if o["id"] == obligation_id), "Unknown")
            
            for risk in risks:
                all_risks.append({
                    "Obligation": obligation_name,
                    "Risk": risk["name"],
                    "Risk Category": risk["category"],
                    "Likelihood": risk["likelihood"],
                    "Impact": risk["impact"]
                })
        
        if all_risks:
            # Create a DataFrame
            df = pd.DataFrame(all_risks)
            
            # Add filters
            col1, col2, col3 = st.columns(3)
            with col1:
                risk_categories = ["All"] + sorted(list(set(df["Risk Category"])))
                selected_category = st.selectbox(
                    "Filter by Risk Category",
                    risk_categories,
                    key="risk_category_filter"
                )
            
            with col2:
                likelihoods = ["All"] + sorted(list(set(df["Likelihood"])))
                selected_likelihood = st.selectbox(
                    "Filter by Likelihood",
                    likelihoods,
                    key="risk_likelihood_filter"
                )
            
            with col3:
                impacts = ["All"] + sorted(list(set(df["Impact"])))
                selected_impact = st.selectbox(
                    "Filter by Impact",
                    impacts,
                    key="risk_impact_filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Risk Category"] == selected_category]
            if selected_likelihood != "All":
                filtered_df = filtered_df[filtered_df["Likelihood"] == selected_likelihood]
            if selected_impact != "All":
                filtered_df = filtered_df[filtered_df["Impact"] == selected_impact]
            
            # Create risk rating column
            def get_risk_rating(row):
                if row["Likelihood"] == "High" and row["Impact"] == "High":
                    return "Critical"
                elif (row["Likelihood"] == "High" and row["Impact"] == "Medium") or \
                     (row["Likelihood"] == "Medium" and row["Impact"] == "High"):
                    return "High"
                elif (row["Likelihood"] == "Medium" and row["Impact"] == "Medium") or \
                     (row["Likelihood"] == "High" and row["Impact"] == "Low") or \
                     (row["Likelihood"] == "Low" and row["Impact"] == "High"):
                    return "Medium"
                else:
                    return "Low"
            
            filtered_df["Risk Rating"] = filtered_df.apply(get_risk_rating, axis=1)
            
            # Sort by Risk Rating
            risk_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            filtered_df["Rating Order"] = filtered_df["Risk Rating"].map(risk_order)
            filtered_df = filtered_df.sort_values(by=["Rating Order", "Risk Category"])
            filtered_df = filtered_df.drop(columns=["Rating Order"])
            
            # Display the dataframe with the new Risk Rating column
            display_columns = ["Risk", "Risk Category", "Likelihood", "Impact", "Risk Rating", "Obligation"]
            filtered_df = filtered_df[display_columns]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            # Display risk summary
            st.subheader("Risk Assessment Summary")
            
            # Count risks by rating
            risk_counts = filtered_df["Risk Rating"].value_counts()
            
            # Create a summary message based on risk counts
            summary_message = """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">Risk Assessment</h4>
                <p>If the recommended obligations are not implemented, this asset may be exposed to the following risks:</p>
                <ul>
            """
            
            if "Critical" in risk_counts:
                summary_message += f"<li><strong style='color: #d9534f;'>Critical Risks:</strong> {risk_counts['Critical']} potential critical risk(s) identified</li>"
            
            if "High" in risk_counts:
                summary_message += f"<li><strong style='color: #f0ad4e;'>High Risks:</strong> {risk_counts['High']} potential high risk(s) identified</li>"
            
            if "Medium" in risk_counts:
                summary_message += f"<li><strong style='color: #5bc0de;'>Medium Risks:</strong> {risk_counts['Medium']} potential medium risk(s) identified</li>"
            
            if "Low" in risk_counts:
                summary_message += f"<li><strong style='color: #5cb85c;'>Low Risks:</strong> {risk_counts['Low']} potential low risk(s) identified</li>"
            
            summary_message += """
                </ul>
                <p>These risks should be carefully evaluated and either mitigated through implementing the recommended obligations or formally accepted as residual risks.</p>
            </div>
            
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How the Risk Recommendation Algorithm Works</h4>
                <p>The algorithm follows this functional flow:</p>
                <ul>
                    <li><strong>Input:</strong> Security and privacy obligations from sensitivity analysis</li>
                    <li><strong>Risk Identification:</strong> Determine potential risks if obligations are not fulfilled</li>
                    <li><strong>Risk Classification:</strong> Categorize risks by type (e.g., Data Breach, Regulatory, Reputational)</li>
                    <li><strong>Impact Assessment:</strong> Evaluate the potential impact of each risk (High, Medium, Low)</li>
                    <li><strong>Likelihood Evaluation:</strong> Assess the probability of each risk occurring (High, Medium, Low)</li>
                    <li><strong>Risk Rating:</strong> Calculate overall risk rating by combining impact and likelihood</li>
                    <li><strong>Output:</strong> Prioritized list of risks with severity ratings</li>
                </ul>
                <p>The risk rating matrix combines likelihood and impact as follows:</p>
                <ul>
                    <li><strong>Critical:</strong> High likelihood + High impact</li>
                    <li><strong>High:</strong> High likelihood + Medium impact, or Medium likelihood + High impact</li>
                    <li><strong>Medium:</strong> Medium likelihood + Medium impact, High likelihood + Low impact, or Low likelihood + High impact</li>
                    <li><strong>Low:</strong> All other combinations</li>
                </ul>
            </div>
            """
            
            st.markdown(summary_message, unsafe_allow_html=True)
        else:
            st.info("No risks identified for the obligations.")
    
    def processing_activities_section(self):
        """Handle the Processing Activities section with purposes and data elements."""
        st.markdown("<div class='page-header'><i class='fas fa-cogs'></i> &nbsp;Processing Activities</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of data processing activities within the organization, including their purposes and the data elements they process.</p>
            <ul>
                <li>Processing activities represent business operations that process personal data</li>
                <li>Each processing activity has a specific business purpose</li>
                <li>Processing activities use data from one or more assets</li>
                <li>Data elements processed are tracked for compliance and transparency</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Get processing activities from repository
        processing_activities = self.inventory_repository.get_processing_activities()
        
        if not processing_activities:
            st.warning("No processing activities available in the database.")
            return
        
        # Get processing activity purposes
        processing_activity_purposes = self.inventory_repository.get_processing_activity_purposes()
        
        # Get processing activity asset data elements
        processing_activity_asset_data_elements = self.inventory_repository.get_processing_activity_asset_data_elements()
        
        # Group purposes by processing activity
        activity_to_purposes = {}
        for pap in processing_activity_purposes:
            activity_id = pap['processing_activity_id']
            if activity_id not in activity_to_purposes:
                activity_to_purposes[activity_id] = []
            activity_to_purposes[activity_id].append({
                'name': pap['purpose_name'],
                'category': pap['purpose_category'],
                'risk_level': pap['purpose_risk_level'],
                'description': pap['purpose_description']
            })
        
        # Group asset data elements by processing activity and then by asset
        activity_to_assets = {}
        for paade in processing_activity_asset_data_elements:
            activity_id = paade['processing_activity_id']
            asset_id = paade['asset_id']
            
            if activity_id not in activity_to_assets:
                activity_to_assets[activity_id] = {}
            
            if asset_id not in activity_to_assets[activity_id]:
                activity_to_assets[activity_id][asset_id] = {
                    'name': paade['asset_name'],
                    'description': paade['asset_description'],
                    'data_elements': []
                }
            
            activity_to_assets[activity_id][asset_id]['data_elements'].append({
                'name': paade['data_element_name'],
                'description': paade['data_element_description']
            })
        
        # Add filtering options at the beginning
        col1, col2 = st.columns(2)
        
        with col1:
            # Get unique purposes
            all_purposes = set()
            for purposes in activity_to_purposes.values():
                all_purposes.update([p['name'] for p in purposes])
            
            selected_purpose = st.selectbox("Filter by Purpose", ["All"] + sorted(list(all_purposes)))
        
        with col2:
            # Get unique assets
            all_assets = set()
            for assets in activity_to_assets.values():
                all_assets.update([a['name'] for _, a in assets.items()])
            
            selected_asset = st.selectbox("Filter by Asset", ["All"] + sorted(list(all_assets)))
        
        # Apply filters
        filtered_activities = processing_activities
        if selected_purpose != "All" or selected_asset != "All":
            filtered_activities = []
            
            for activity in processing_activities:
                include = True
                
                if selected_purpose != "All":
                    purposes = activity_to_purposes.get(activity['id'], [])
                    purpose_names = [p['name'] for p in purposes]
                    if selected_purpose not in purpose_names:
                        include = False
                
                if selected_asset != "All" and include:
                    assets = activity_to_assets.get(activity['id'], {})
                    asset_names = [a['name'] for _, a in assets.items()]
                    if selected_asset not in asset_names:
                        include = False
                
                if include:
                    filtered_activities.append(activity)
        
        # Create a DataFrame for all processing activities
        pa_data = {
            "Processing Activity": [],
            "Description": [],
            "Status": [],
            "Start Date": [],
            "End Date": [],
            "Purpose(s)": [],
            "Asset(s)": [],
            "Data Element Count": []
        }
        
        if not filtered_activities:
            st.warning("No processing activities match the selected filters.")
        else:
            for activity in filtered_activities:
                # Get purposes for this activity
                purposes = activity_to_purposes.get(activity['id'], [])
                purpose_names = ", ".join([p['name'] for p in purposes]) if purposes else "None"
                
                # Get assets for this activity
                assets = activity_to_assets.get(activity['id'], {})
                asset_names = ", ".join([a['name'] for _, a in assets.items()]) if assets else "None"
                
                # Count total data elements
                data_element_count = sum(len(a['data_elements']) for _, a in assets.items()) if assets else 0
                
                # Add to DataFrame
                pa_data["Processing Activity"].append(activity['name'])
                pa_data["Description"].append(activity['description'])
                pa_data["Status"].append(activity['status'])
                pa_data["Start Date"].append(activity['start_date'])
                pa_data["End Date"].append(activity['end_date'] if activity['end_date'] else "N/A")
                pa_data["Purpose(s)"].append(purpose_names)
                pa_data["Asset(s)"].append(asset_names)
                pa_data["Data Element Count"].append(data_element_count)
            
            # Convert to DataFrame for display
            df = pd.DataFrame(pa_data)
            
            # Remove any empty rows
            df = df.dropna(how='all')
            
            # Display the DataFrame with a fixed height to avoid empty rows
            st.dataframe(df, use_container_width=True, height=min(400, len(df) * 35 + 38))
            
            # Add a selectbox to choose a processing activity
            activity_names = [activity['name'] for activity in filtered_activities]
            if activity_names:
                selected_activity_name = st.selectbox("Select a processing activity to view details", activity_names)
                
                # Find the selected activity
                selected_activity = next((activity for activity in filtered_activities if activity['name'] == selected_activity_name), None)
                
                with st.container():
                    # Create a card-like container with custom styling
                    card_header = f'''
                    <div style="background-color: white; border-radius: 10px 10px 0 0; padding: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">
                        <h3 style="color: #2c3e50; margin-top: 0;">{selected_activity['name']}</h3>
                        <p style="color: #7f8c8d;">{selected_activity['description']}</p>
                        <p><span style="background-color: #e8f4f8; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">{selected_activity['status']}</span></p>
                    </div>
                    '''
                    st.markdown(card_header, unsafe_allow_html=True)
                    
                    # Create a card for expanders
                    card_body = '<div style="background-color: white; border-radius: 0 0 10px 10px; padding: 0 15px 15px 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">'
                    st.markdown(card_body, unsafe_allow_html=True)
                    
                    # Get purposes for this activity
                    purposes = activity_to_purposes.get(selected_activity['id'], [])
                    
                    if purposes:
                        with st.expander(f"Purpose{'s' if len(purposes) > 1 else ''} ({len(purposes)})"):
                            for purpose in purposes:
                                risk_color = {
                                    'Low': '#2ecc71',  # Green
                                    'Medium': '#f39c12',  # Orange
                                    'High': '#e74c3c'  # Red
                                }.get(purpose['risk_level'], '#7f8c8d')  # Default gray
                                
                                st.markdown(f'''
                                <div style="background-color: white; border-radius: 5px; padding: 10px; margin-bottom: 10px; border-left: 3px solid {risk_color};">
                                    <h4 style="margin-top: 0;">{purpose['name']}</h4>
                                    <p style="font-size: 0.9em; margin-bottom: 5px;"><strong>Category:</strong> {purpose['category'] or 'N/A'}</p>
                                    <p style="font-size: 0.9em; margin-bottom: 5px;"><strong>Risk Level:</strong> <span style="color: {risk_color};">{purpose['risk_level'] or 'N/A'}</span></p>
                                    <p style="font-size: 0.9em;">{purpose['description'] or 'No description available'}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                    else:
                        st.info(f"No purposes associated with {selected_activity['name']}")
                    
                    # Get assets and data elements for this activity
                    assets = activity_to_assets.get(selected_activity['id'], {})
                    
                    if assets:
                        with st.expander(f"Assets and Data Elements ({len(assets)})"):
                            for asset_id, asset in assets.items():
                                st.markdown(f"#### {asset['name']}")
                                st.markdown(f"*{asset['description']}*")
                                
                                # Create a DataFrame for the data elements
                                de_data = {
                                    "Data Element": [],
                                    "Description": []
                                }
                                
                                for de in asset['data_elements']:
                                    de_data["Data Element"].append(de['name'])
                                    de_data["Description"].append(de['description'])
                                
                                # Display the data elements in a styled dataframe
                                st.dataframe(pd.DataFrame(de_data), use_container_width=True)
                    else:
                        st.info(f"No assets associated with {selected_activity['name']}")
                    
                    # Close the card div
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add Policy Compliance Analysis section (outside the card)
                    if purposes and assets:
                        st.subheader("Policy Compliance Analysis")
                        
                        # Add algorithm description
                        st.markdown("""
                        <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                            <h4 style="margin-top: 0;">How Policy Compliance Analysis Works</h4>
                            <p>The Policy Compliance Analysis uses these mapping tables to determine if a processing activity complies with organizational policies:</p>
                            <ol>
                                <li><strong>Policy Purpose Data Elements</strong>: Maps which data elements are allowed for specific purposes under each policy.</li>
                                <li><strong>Policy Purpose Data Usage</strong>: Defines permitted operations (read, write, share) for each data element-purpose combination.</li>
                                <li><strong>Purpose Risk Levels</strong>: Categorizes purposes by risk level, which influences the strictness of compliance requirements.</li>
                            </ol>
                            <p>When analyzing policy compliance, the system considers:</p>
                            <ul>
                                <li>The business purpose of the processing activity</li>
                                <li>All data elements involved in the processing</li>
                                <li>The specific operation being performed (read, write, share)</li>
                                <li>Any usage restrictions defined in the policy</li>
                            </ul>
                            <p>The system then evaluates each data element against policy rules and provides a detailed compliance assessment with recommendations for addressing any violations.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("Check if this processing activity complies with organizational policies.")
                        
                        # Get the purpose for this activity (assuming one purpose per activity)
                        purpose = purposes[0]['name'] if purposes else None
                        
                        # Get all data elements from all assets
                        all_data_elements = []
                        for _, asset in assets.items():
                            for de in asset['data_elements']:
                                all_data_elements.append(de['name'])
                        
                        # Remove duplicates
                        all_data_elements = list(set(all_data_elements))
                        
                        # Add operation selection dropdown
                        operation = st.selectbox(
                            "Select Operation",
                            options=["read", "write", "share"],
                            index=0,
                            key=f"operation_select_{selected_activity['id']}"
                        )
                        
                        # Add analyze button under the dropdown
                        analyze_button = st.button(
                            "Analyze Policy Compliance", 
                            key=f"analyze_btn_{selected_activity['id']}"
                        )
                        
                        if purpose and all_data_elements:
                            if analyze_button:
                                # Display policy compliance analysis
                                st.markdown(f"### Policy Compliance Analysis for {purpose}")
                                st.markdown(f"**Operation:** {operation.upper()}")
                                
                                # Analyze for the selected operation
                                self._analyze_policy_compliance_for_activity(purpose, all_data_elements, operation)
                            else:
                                # Show placeholder message
                                st.markdown("""
                                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
                                    <h3 style="color: #7F8C8D;">Analysis Results</h3>
                                    <p>Policy compliance analysis will appear here after clicking the Analyze button...</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Insufficient data for policy compliance analysis.")
                    

        
    def purposes_page(self):
        """Display the Purposes page with all purposes from the repository."""
        st.markdown("<div class='page-header'><i class='fas fa-bullseye'></i> &nbsp;Purposes</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of business purposes for data processing activities.</p>
            <ul>
                <li>Business purposes define why data is collected and processed</li>
                <li>Each purpose has an associated risk level</li>
                <li>Purposes are used in policy compliance analysis</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Get purposes from repository
        purposes = self.glossary_repository.get_purposes()
        
        if purposes:
            # Create a DataFrame for display
            purposes_data = {
                "Purpose": [],
                "Category": [],
                "Risk Level": [],
                "Description": []
            }
            
            for purpose in purposes:
                purposes_data["Purpose"].append(purpose["name"])
                purposes_data["Category"].append(purpose["category_name"] if purpose.get("category_name") else "N/A")
                purposes_data["Risk Level"].append(purpose["risk_level"] if purpose.get("risk_level") else "N/A")
                purposes_data["Description"].append(purpose["description"] if purpose.get("description") else "")
            
            # Convert to DataFrame
            df = pd.DataFrame(purposes_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            
            with col1:
                # Get unique categories
                categories = sorted(list(set(df["Category"].tolist())))
                selected_category = st.selectbox("Filter by Category", ["All"] + categories)
            
            with col2:
                # Get unique risk levels
                risk_levels = sorted(list(set(df["Risk Level"].tolist())))
                selected_risk_level = st.selectbox("Filter by Risk Level", ["All"] + risk_levels)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Category"] == selected_category]
            
            if selected_risk_level != "All":
                filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk_level]
            
            # Display filtered data
            if not filtered_df.empty:
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.warning("No purposes match the selected filters.")
        else:
            st.warning("No purposes available in the database.")
    
    def policies_page(self):
        """Display the Policies page with tabs for Policy Purpose, Policy Purpose Data Usage, and Policy Purpose Data Element."""
        st.markdown("<div class='page-header'><i class='fas fa-clipboard-list'></i> &nbsp;Policies</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of data policies that govern how data is managed, protected, and used within the organization.</p>
            <ul>
                <li>Policies define rules for data access and usage</li>
                <li>Policy-purpose relationships establish what purposes are allowed for each policy</li>
                <li>Data element rules specify what data can be accessed for each purpose</li>
                <li>Usage rules define permitted operations (read, write, share) for each data element</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        tabs = st.tabs(["Policies", "Policy Purpose", "Policy Purpose Data Element", "Policy Purpose Data Usage"])
        
        # Policies tab
        with tabs[0]:
            # Get policies data from repository
            policies = self.glossary_repository.get_policies()
            if policies:
                policy_data = {
                    "Policy": [],
                    "Type": [],
                    "Status": [],
                    "Description": []
                }
                for policy in policies:
                    policy_data["Policy"].append(policy["name"])
                    policy_data["Type"].append(policy["policy_type"] if policy.get("policy_type") else "")
                    policy_data["Status"].append(policy["status"] if policy.get("status") else "")
                    policy_data["Description"].append(policy["description"] if policy.get("description") else "")
                
                # Convert to DataFrame
                df = pd.DataFrame(policy_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policy types
                    policy_types = sorted(list(set([t for t in df["Type"].tolist() if t])))
                    selected_type = st.selectbox("Filter by Policy Type", ["All"] + policy_types)
                
                with col2:
                    # Get unique statuses
                    statuses = sorted(list(set([s for s in df["Status"].tolist() if s])))
                    selected_status = st.selectbox("Filter by Status", ["All"] + statuses)
                
                # Apply filters
                filtered_df = df.copy()
                if selected_type != "All":
                    filtered_df = filtered_df[filtered_df["Type"] == selected_type]
                
                if selected_status != "All":
                    filtered_df = filtered_df[filtered_df["Status"] == selected_status]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policies match the selected filters.")
            else:
                st.warning("No data available in the database.")
        
        # Policy Purpose tab
        with tabs[1]:
            # Get policy purposes from repository
            policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
            
            if policy_purposes:
                # Create a DataFrame for display
                policy_purpose_data = {
                    "Policy": [],
                    "Purpose": []
                }
                
                for relation in policy_purposes:
                    policy_purpose_data["Policy"].append(relation["policy_name"])
                    policy_purpose_data["Purpose"].append(relation["purpose_name"])
                
                # Convert to DataFrame
                df = pd.DataFrame(policy_purpose_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="policy_purpose_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="policy_purpose_purpose")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose relationships match the selected filters.")
            else:
                st.warning("No policy-purpose relationships available in the database.")
        
        # Policy Purpose Data Element tab
        with tabs[2]:
            # Get policy purpose data elements from repository
            policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements()
            
            if policy_purpose_data_elements:
                # Create a DataFrame for display
                ppde_data = {
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Access Allowed": []
                }
                
                for relation in policy_purpose_data_elements:
                    ppde_data["Policy"].append(relation["policy_name"])
                    ppde_data["Purpose"].append(relation["purpose_name"])
                    ppde_data["Data Element"].append(relation["data_element_name"])
                    ppde_data["Access Allowed"].append("Yes" if relation["access_allowed"] else "No")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppde_data)
                
                # Add filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppde_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppde_purpose")
                
                with col3:
                    # Filter by access allowed
                    selected_access = st.selectbox("Filter by Access", ["All", "Yes", "No"], key="ppde_access")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppde_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_access != "All":
                    filtered_df = filtered_df[filtered_df["Access Allowed"] == selected_access]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data element relationships match the selected filters.")
            else:
                st.warning("No policy-purpose-data element relationships available in the database.")
        
        # Policy Purpose Data Usage tab
        with tabs[3]:
            # Get policy purpose data usages from repository
            policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages()
            
            if policy_purpose_data_usages:
                # Create a DataFrame for display
                ppdu_data = {
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Operation": [],
                    "Allowed": [],
                    "Restrictions": []
                }
                
                for rule in policy_purpose_data_usages:
                    ppdu_data["Policy"].append(rule["policy_name"])
                    ppdu_data["Purpose"].append(rule["purpose_name"])
                    ppdu_data["Data Element"].append(rule["data_element_name"])
                    ppdu_data["Operation"].append(rule["operation"])
                    ppdu_data["Allowed"].append("Yes" if rule["allowed"] else "No")
                    ppdu_data["Restrictions"].append(rule["restrictions"] if rule["restrictions"] else "None")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppdu_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppdu_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppdu_purpose")
                
                # Second row of filters
                col3, col4, col5 = st.columns(3)
                
                with col3:
                    # Get unique operations
                    operations = sorted(list(set(df["Operation"].tolist())))
                    selected_operation = st.selectbox("Filter by Operation", ["All"] + operations, key="ppdu_operation")
                
                with col4:
                    # Filter by allowed
                    selected_allowed = st.selectbox("Filter by Allowed", ["All", "Yes", "No"], key="ppdu_allowed")
                
                with col5:
                    # Filter by restrictions
                    has_restrictions = st.selectbox("Has Restrictions", ["All", "Yes", "No"], key="ppdu_restrictions")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppdu_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_operation != "All":
                    filtered_df = filtered_df[filtered_df["Operation"] == selected_operation]
                
                if selected_allowed != "All":
                    filtered_df = filtered_df[filtered_df["Allowed"] == selected_allowed]
                
                if has_restrictions != "All":
                    if has_restrictions == "Yes":
                        filtered_df = filtered_df[filtered_df["Restrictions"] != "None"]
                    else:
                        filtered_df = filtered_df[filtered_df["Restrictions"] == "None"]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data usage rules match the selected filters.")
            else:
                st.warning("No policy-purpose-data usage rules available in the database.")
    
    def policy_compliance_page(self):
        """Display the Policy Compliance page with the policy compliance analysis tool."""
        st.markdown("<div class='page-header'><i class='fas fa-balance-scale'></i> &nbsp;Policy Compliance</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Compliance Analysis</strong> determines whether access to data is permitted based on purpose limitation principles and organizational policies.</p>
            <p>This tool helps enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations.</p>
            <br>
            <ul>
                <li>Enforces purpose limitation principles</li>
                <li>Determines data access permissions based on business purpose</li>
                <li>Applies policy-based restrictions on data usage</li>
                <li>Provides clear decision rationale</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get purposes for dropdown selection
            try:
                purposes = self.glossary_repository.get_purposes()
                purpose_options = [purpose["name"] for purpose in purposes] if purposes else ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
            except Exception as e:
                st.warning(f"Error loading purposes: {e}")
                purpose_options = ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
                
            selected_purpose = st.selectbox("Select Business Purpose", options=purpose_options, key="policy_purpose")
            
            # Get data elements for multiselect
            try:
                data_elements = self.glossary_repository.get_data_elements()
                data_element_options = [de["name"] for de in data_elements] if data_elements else ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
            except Exception as e:
                st.warning(f"Error loading data elements: {e}")
                data_element_options = ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
                
            selected_data_elements = st.multiselect("Select Data Elements", options=data_element_options, key="policy_data_elements")
            
            # Operation selection
            operations = ["read", "write", "share"]
            selected_operation = st.selectbox("Select Operation", options=operations, key="policy_operation")
            
            # Add a button to trigger inference with custom styling
            st.markdown("""
            <style>
            div[data-testid="stButton"] > button#policy_analysis_btn {
                background-color: #3498db;
                color: white;
                border: 2px solid #3498db;
                padding: 0.5rem 1rem;
                font-weight: 600;
                border-radius: 4px;
                text-align: center;
                margin: 1rem 0;
                display: block;
                width: 100%;
            }
            div[data-testid="stButton"] > button#policy_analysis_btn:hover {
                background-color: #2980b9;
                border-color: #2980b9;
            }
            </style>
            """, unsafe_allow_html=True)
            
            analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "request", "label": "Access Request", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "purpose", "label": "Business Purpose", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "policy", "label": "Applicable Policy", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "data_elements", "label": "Data Elements", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "operation", "label": "Operation Type", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Policy Lookup", "color": "#1abc9c", "shape": "box", "size": 25,
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #1abc9c;'>
                        <h3>Policy Compliance Lookup Process</h3>
                        <p>This lookup process determines data access permissions by:</p>
                        <ol>
                            <li>Identifying the applicable <b>Access Control Policy</b></li>
                            <li>Checking if the purpose is allowed under the policy</li>
                            <li>Verifying if each data element is accessible for the purpose</li>
                            <li>Confirming if the requested operation is permitted</li>
                            <li>Applying any restrictions or conditions</li>
                        </ol>
                        <p>The algorithm uses the policy_purpose_data_usage table to determine specific access rules.</p>
                    </div>
                """}},
                {"id": "decision", "label": "Access Decision", "color": "#e67e22", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "request", "target": "purpose", "label": "For"},
                {"source": "request", "target": "data_elements", "label": "Requests"},
                {"source": "request", "target": "operation", "label": "With"},
                {"source": "purpose", "target": "policy", "label": "Governed by"},
                {"source": "policy", "target": "lookup", "label": ""},
                {"source": "data_elements", "target": "lookup", "label": ""},
                {"source": "operation", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "decision", "label": "Results in"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, "Policy Compliance Decision Process", height=500)
        
        with col2:
            st.subheader("Policy Compliance Analysis")
            
            if analyze_button:
                if not selected_purpose or not selected_data_elements:
                    st.warning("Please select both Purpose and at least one Data Element")
                else:
                    self._analyze_policy_compliance(
                        selected_purpose, 
                        selected_data_elements,
                        selected_operation
                    )
            else:
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Policy compliance analysis will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)

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
            
            # Regulatory Metadata menu item
            if st.button("📋 Regulatory Metadata", key="regulatory_btn", use_container_width=True):
                st.session_state['current_section'] = 'Regulatory'
                
            # Removed Obligations menu item (moved to Core Constructs)
            
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
                

            
            # Third section: Data Use Governance
            st.markdown("<div class='sidebar-section-header'>Data Use Governance</div>", unsafe_allow_html=True)
            
            # Purposes menu item
            if st.button("🎯 Purposes", key="purposes_btn", use_container_width=True):
                st.session_state['current_section'] = 'Purposes'
            
            # Policies menu item
            if st.button("📋 Policies", key="policies_btn", use_container_width=True):
                st.session_state['current_section'] = 'Policies'
            
            # Governance menu item
            if st.button("⚖️ Policy Compliance", key="governance_btn", use_container_width=True):
                st.session_state['current_section'] = 'Policy Compliance'
            
            # Fourth section: Inventory
            st.markdown("<div class='sidebar-section-header'>Inventory</div>", unsafe_allow_html=True)
            
            # Assets menu item
            if st.button("📊 Assets", key="assets_btn", use_container_width=True):
                st.session_state['current_section'] = 'Assets'
                
            # Processing Activities menu item
            if st.button("🔄 Processing Activities", key="processing_activities_btn", use_container_width=True):
                st.session_state['current_section'] = 'Processing Activities'

            
            
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
        elif st.session_state['current_section'] == 'Assets':
            self.assets_section()
        elif st.session_state['current_section'] == 'Processing Activities':
            self.processing_activities_section()
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
        elif st.session_state['current_section'] == 'Purposes':
            self.purposes_page()
        elif st.session_state['current_section'] == 'Policies':
            self.policies_page()
        elif st.session_state['current_section'] == 'Policy Compliance':
            self.policy_compliance_page()

    def regulatory_intelligence_section(self):
        """Handle the Regulatory Intelligence section with its tabs."""
        st.title("Regulatory Intelligence")
        st.markdown("Manage regulatory obligations and their links to policies, controls, and risks.")
        
        # Create tabs for the section (removed Sensitivity Obligations tab as it's now in Regulatory Metadata)
        tabs = st.tabs(["Obligation Inference"])
        
        # Handle each tab
        with tabs[0]:
            self.obligation_inference_page()
            
    def obligations_page(self):
        """Display the Obligations page with all obligations from the repository."""
        st.header("Obligations Management")
        st.markdown("View and manage regulatory obligations that need to be addressed.")
        
        # Create columns for filters and actions
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "In Progress", "Implemented", "Accepted Risk"],
                key="obligation_status_filter"
            )
        
        with col2:
            control_filter = st.selectbox(
                "Filter by Control Type",
                ["All", "Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"],
                key="obligation_control_filter"
            )
        
        with col3:
            policy_filter = st.selectbox(
                "Filter by Policy Status",
                ["All", "Linked to Policy", "No Policy"],
                key="obligation_policy_filter"
            )
        
        # Apply filters
        status = None if status_filter == "All" else status_filter
        control_type = None if control_filter == "All" else control_filter
        policy_linked = None
        if policy_filter == "Linked to Policy":
            policy_linked = True
        elif policy_filter == "No Policy":
            policy_linked = False
        
        # Get obligations from repository with filters
        obligations = self.obligation_repository.get_obligations(status, control_type, policy_linked)
        
        if obligations:
            # Convert to DataFrame for display
            df = pd.DataFrame(obligations)
            # Rename columns for better display
            df = df.rename(columns={
                "id": "ID",
                "name": "Obligation",
                "description": "Description",
                "source": "Source",
                "control_type": "Control Type",
                "status": "Status",
                "policy_name": "Policy",
                "risk_accepted": "Risk Accepted",
                "created_at": "Created At"
            })
            
            # Reorder columns for better display
            display_columns = ["ID", "Obligation", "Description", "Source", "Control Type", "Status", "Policy", "Risk Accepted"]
            df = df[display_columns]
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No obligations found with the selected filters.")
        
        # Add new obligation section
        with st.expander("Add New Obligation", expanded=False):
            with st.form("add_obligation_form"):
                obligation_name = st.text_input("Obligation Name")
                obligation_desc = st.text_area("Description")
                obligation_source = st.text_input("Source (e.g., Regulation, Standard)")
                obligation_control = st.selectbox(
                    "Control Type",
                    ["Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"],
                    key="new_obligation_control"
                )
                obligation_status = st.selectbox(
                    "Status",
                    ["Open", "In Progress", "Implemented", "Accepted Risk"],
                    key="new_obligation_status"
                )
                
                submitted = st.form_submit_button("Add Obligation")
                if submitted:
                    if obligation_name and obligation_desc:
                        # Add the obligation to the repository
                        new_id = self.obligation_repository.add_obligation(
                            obligation_name, obligation_desc, obligation_source, 
                            obligation_control, obligation_status
                        )
                        if new_id:
                            st.success(f"Obligation '{obligation_name}' added successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to add obligation. Please try again.")
                    else:
                        st.warning("Obligation Name and Description are required.")
        
        # Manage existing obligations
        if obligations:
            with st.expander("Manage Existing Obligations", expanded=False):
                # Select an obligation to manage
                selected_id = st.selectbox(
                    "Select Obligation to Manage",
                    options=[o["id"] for o in obligations],
                    format_func=lambda x: next((o["name"] for o in obligations if o["id"] == x), "Unknown"),
                    key="manage_obligation_id"
                )
                
                if selected_id:
                    selected_obligation = next((o for o in obligations if o["id"] == selected_id), None)
                    if selected_obligation:
                        action = st.radio(
                            "Action",
                            ["Update Status", "Link to Policy", "Accept Risk", "Delete"],
                            key="obligation_action"
                        )
                        
                        if action == "Update Status":
                            new_status = st.selectbox(
                                "New Status",
                                ["Open", "In Progress", "Implemented", "Accepted Risk"],
                                index=["Open", "In Progress", "Implemented", "Accepted Risk"].index(selected_obligation["status"]) if selected_obligation["status"] in ["Open", "In Progress", "Implemented", "Accepted Risk"] else 0,
                                key="new_status"
                            )
                            if st.button("Update Status"):
                                success = self.obligation_repository.update_obligation(
                                    selected_id, status=new_status
                                )
                                if success:
                                    st.success(f"Status updated to {new_status}")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to update status")
                                    
                        elif action == "Link to Policy":
                            # Get policies from repository
                            policies = self.glossary_repository.get_policies()
                            policy_options = {p["id"]: p["name"] for p in policies}
                            policy_options[0] = "None (Remove Link)"
                            
                            selected_policy = st.selectbox(
                                "Select Policy",
                                options=list(policy_options.keys()),
                                format_func=lambda x: policy_options[x],
                                index=0,
                                key="link_policy"
                            )
                            
                            if st.button("Link to Policy"):
                                policy_id = selected_policy if selected_policy != 0 else None
                                success = self.obligation_repository.update_obligation(
                                    selected_id, policy_id=policy_id
                                )
                                if success:
                                    if policy_id:
                                        st.success(f"Linked to policy: {policy_options[policy_id]}")
                                    else:
                                        st.success("Policy link removed")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to update policy link")
                                    
                        elif action == "Accept Risk":
                            risk_accepted = st.checkbox(
                                "Accept Risk for this Obligation",
                                value=selected_obligation["risk_accepted"],
                                key="accept_risk"
                            )
                            risk_notes = st.text_area("Risk Acceptance Notes")
                            
                            if st.button("Save Risk Decision"):
                                # Update risk acceptance status
                                success = self.obligation_repository.update_obligation(
                                    selected_id, 
                                    risk_accepted=risk_accepted,
                                    status="Accepted Risk" if risk_accepted else "Open"
                                )
                                if success:
                                    st.success("Risk decision saved")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to save risk decision")
                                    
                        elif action == "Delete":
                            st.warning("This action cannot be undone!")
                            if st.button("Delete Obligation"):
                                success = self.obligation_repository.delete_obligation(selected_id)
                                if success:
                                    st.success("Obligation deleted")
                                    st.experimental_rerun()
                                else:
                                    st.error("Failed to delete obligation")
    
    def sensitivity_obligations_page(self):
        """Display the Sensitivity Obligations page with mappings from sensitivity to standard obligations."""
        st.header("Sensitivity-Based Obligations")
        st.markdown("Define standard obligations that should be applied based on data sensitivity levels.")
        
        # Get all sensitivities
        sensitivities = self.glossary_repository.get_sensitivities()
        
        # Create a filter for sensitivity
        sensitivity_options = {s["id"]: s["name"] for s in sensitivities}
        sensitivity_options[0] = "All Sensitivities"
        
        selected_sensitivity_id = st.selectbox(
            "Filter by Sensitivity Level",
            options=list(sensitivity_options.keys()),
            format_func=lambda x: sensitivity_options[x],
            index=0,
            key="sensitivity_filter"
        )
        
        # Get sensitivity obligations with filter
        sensitivity_id = None if selected_sensitivity_id == 0 else selected_sensitivity_id
        sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
        
        if sensitivity_obligations:
            # Convert to DataFrame for display
            df = pd.DataFrame(sensitivity_obligations)
            # Rename columns for better display
            df = df.rename(columns={
                "id": "ID",
                "sensitivity_name": "Sensitivity Level",
                "obligation_name": "Standard Obligation",
                "obligation_description": "Description",
                "control_type": "Control Type",
                "priority": "Priority"
            })
            
            # Reorder columns for better display
            display_columns = ["ID", "Sensitivity Level", "Standard Obligation", "Description", "Control Type", "Priority"]
            df = df[display_columns]
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sensitivity-obligation mappings found with the selected filter.")
        
        # Add new sensitivity obligation mapping
        with st.expander("Add New Sensitivity Obligation", expanded=False):
            with st.form("add_sensitivity_obligation_form"):
                sens_id = st.selectbox(
                    "Sensitivity Level",
                    options=[s["id"] for s in sensitivities],
                    format_func=lambda x: next((s["name"] for s in sensitivities if s["id"] == x), "Unknown"),
                    key="new_sens_obligation_sensitivity"
                )
                
                obligation_name = st.text_input("Standard Obligation Name")
                obligation_desc = st.text_area("Description")
                obligation_control = st.selectbox(
                    "Control Type",
                    ["Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"],
                    key="new_sens_obligation_control"
                )
                obligation_priority = st.selectbox(
                    "Priority",
                    ["High", "Medium", "Low"],
                    index=1,  # Default to Medium
                    key="new_sens_obligation_priority"
                )
                
                submitted = st.form_submit_button("Add Sensitivity Obligation")
                if submitted:
                    if sens_id and obligation_name and obligation_desc:
                        # Add the sensitivity obligation to the repository
                        new_id = self.obligation_repository.add_sensitivity_obligation(
                            sens_id, obligation_name, obligation_desc, 
                            obligation_control, obligation_priority
                        )
                        if new_id:
                            st.success(f"Sensitivity obligation mapping added successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to add sensitivity obligation mapping. Please try again.")
                    else:
                        st.warning("All fields are required.")
        
        # Generate obligations from sensitivity
        with st.expander("Generate Obligations from Sensitivity", expanded=False):
            st.markdown("Generate actual obligations based on sensitivity level templates.")
            
            selected_sens_id = st.selectbox(
                "Select Sensitivity Level",
                options=[s["id"] for s in sensitivities],
                format_func=lambda x: next((s["name"] for s in sensitivities if s["id"] == x), "Unknown"),
                key="generate_obligations_sensitivity"
            )
            
            if st.button("Generate Obligations"):
                created_ids = self.obligation_repository.generate_obligations_from_sensitivity(selected_sens_id)
                if created_ids:
                    st.success(f"Generated {len(created_ids)} new obligations based on sensitivity level!")
                    st.experimental_rerun()
                else:
                    st.info("No new obligations were generated. They may already exist.")
    
    def obligation_inference_page(self):
        """Display the Obligation Inference page to infer obligations based on data sensitivity."""
        st.header("Obligation Inference API")
        st.markdown("Infer appropriate obligations based on data sensitivity levels.")
        
        # Create two columns for the form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Get all sensitivities for the dropdown
            sensitivities = self.glossary_repository.get_sensitivities()
            
            st.subheader("Input Parameters")
            selected_sensitivity_id = st.selectbox(
                "Data Sensitivity Level",
                options=[s["id"] for s in sensitivities],
                format_func=lambda x: next((s["name"] for s in sensitivities if s["id"] == x), "Unknown"),
                key="infer_obligations_sensitivity"
            )
            
            analyze_button = st.button("Analyze Obligations")
        
        with col2:
            st.subheader("Inferred Obligations")
            
            if analyze_button and selected_sensitivity_id:
                # Get the sensitivity name for display
                sensitivity_name = next((s["name"] for s in sensitivities if s["id"] == selected_sensitivity_id), "Unknown")
                
                # Get obligations for this sensitivity level
                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(selected_sensitivity_id)
                
                if sensitivity_obligations:
                    st.markdown(f"### Recommended Obligations for {sensitivity_name} Data")
                    
                    # Group by control type for better organization
                    control_types = set(so["control_type"] for so in sensitivity_obligations)
                    
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        control_obligations = [so for so in sensitivity_obligations if so["control_type"] == control_type]
                        
                        # Sort by priority
                        priority_order = {"High": 0, "Medium": 1, "Low": 2}
                        control_obligations.sort(key=lambda x: priority_order.get(x["priority"], 99))
                        
                        for obligation in control_obligations:
                            with st.expander(f"{obligation['obligation_name']} ({obligation['priority']} Priority)", expanded=True):
                                st.markdown(f"**Description:** {obligation['obligation_description']}")
                                
                                # Add a button to create this obligation
                                if st.button(f"Create Obligation: {obligation['obligation_name']}", key=f"create_{obligation['id']}"):
                                    # Check if this obligation already exists
                                    existing_obligations = self.obligation_repository.get_obligations()
                                    exists = any(o["name"] == obligation["obligation_name"] for o in existing_obligations)
                                    
                                    if not exists:
                                        new_id = self.obligation_repository.add_obligation(
                                            obligation["obligation_name"],
                                            obligation["obligation_description"],
                                            f"Sensitivity: {sensitivity_name}",
                                            obligation["control_type"],
                                            "Open"
                                        )
                                        if new_id:
                                            st.success(f"Created obligation: {obligation['obligation_name']}")
                                        else:
                                            st.error("Failed to create obligation")
                                    else:
                                        st.info(f"Obligation '{obligation['obligation_name']}' already exists")
                else:
                    st.info(f"No standard obligations defined for {sensitivity_name} sensitivity level.")
            else:
                st.markdown("""Select a sensitivity level and click 'Analyze Obligations' to see recommended obligations.
                
The Obligation Inference API helps you determine what security and privacy controls should be implemented based on the sensitivity of the data you're handling.
                """)
                
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


        if not selected_law:
            return

        # Retrieve and filter metadata for the selected law
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        law_dst_de_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
        law_dst_dc_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()


        filtered_law_jurisdictions = [item for item in law_jurisdictions if item["law_name"] == selected_law]
        filtered_law_legal_bases = [item for item in law_legal_bases if item["law_name"] == selected_law]
        filtered_law_dst_de_sensitivities = [item for item in law_dst_de_sensitivities if item["law_name"] == selected_law]
        filtered_law_dst_dc_sensitivities = [item for item in law_dst_dc_sensitivities if item["law_name"] == selected_law]


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
                    <li><strong>Parameter-Based Lookup:</strong> Checks for sensitivity classifications matching all input parameters</li>
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

                {"id": "lookup", "label": "Sensitivity Lookup", "color": "#2ecc71", "shape": "box", "size": 25, 
                 "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                        <h3>Sensitivity Lookup Process</h3>
                        <p>This lookup process determines data sensitivity by:</p>
                        <ol>
                            <li>Checking the <b>Law Data Subject Type Data Element Sensitivity</b> table for exact matches</li>
                            <li>If no match, checking the <b>Law Data Subject Type Data Category Sensitivity</b> table</li>

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

                {"source": "law", "target": "lookup", "label": ""},
                {"source": "dst", "target": "lookup", "label": ""},

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
                        
                        According to the regulatory metadata, when processing the data element '{selected_data}' 
                        for a '{selected_dst}' under '{selected_law}', the appropriate sensitivity classification is '{sensitivity}'.
                        """)
                    else:
                        st.markdown(f"""
                        The sensitivity level was determined based on the following factors:
                        - **Law**: {selected_law}
                        - **Data Subject Type**: {selected_dst}
                        - **Data Category**: {selected_data}
                        
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
    
    def _infer_sensitivity(self, law, data_subject_type, data_value, data_type):
        """Internal method to infer sensitivity based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            data_subject_type (str): The name of the data subject type
            data_value (str): The name of the data element or category
            data_type (str): Either "Data Element" or "Data Category"
            
        Returns:
            str: The inferred sensitivity level or None if not found
        """
        
        # Check data element sensitivity
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
                
    def policy_inference_api(self):
        """Implement the Policy Inference API for access governance.
        This helps determine whether access to data is permitted based on purpose limitation principles.
        """
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Inference API</div>", unsafe_allow_html=True)
        
        # Description
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Inference API</strong> determines whether access to data is permitted based on purpose limitation principles and organizational policies.</p>
            <p>This API helps enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations.</p>
            <br>
            <ul>
                <li>Enforces purpose limitation principles</li>
                <li>Determines data access permissions based on business purpose</li>
                <li>Applies policy-based restrictions on data usage</li>
                <li>Provides clear decision rationale</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for input form and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Parameters")
            
            # Get purposes for dropdown selection
            try:
                purposes = self.glossary_repository.get_purposes()
                purpose_options = [purpose["name"] for purpose in purposes] if purposes else ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
            except Exception as e:
                st.warning(f"Error loading purposes: {e}")
                purpose_options = ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
                
            selected_purpose = st.selectbox("Select Business Purpose", options=purpose_options, key="policy_purpose")
            
            # Get data elements for multiselect
            try:
                data_elements = self.glossary_repository.get_data_elements()
                data_element_options = [de["name"] for de in data_elements] if data_elements else ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
            except Exception as e:
                st.warning(f"Error loading data elements: {e}")
                data_element_options = ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
                
            selected_data_elements = st.multiselect("Select Data Elements", options=data_element_options, key="policy_data_elements")
            
            # Operation selection
            operations = ["read", "write", "share"]
            selected_operation = st.selectbox("Select Operation", options=operations, key="policy_operation")
            
            try:
                jurisdictions = self.glossary_repository.get_jurisdictions()
                jurisdiction_options = ["Any"] + [j["name"] for j in jurisdictions] if jurisdictions else ["Any", "California", "European Union", "United Kingdom", "Canada"]
            except Exception as e:
                jurisdiction_options = ["Any", "California", "European Union", "United Kingdom", "Canada"]
                
            selected_jurisdiction = st.selectbox("Select Jurisdiction (Optional)", options=jurisdiction_options, key="policy_jurisdiction")
            
            # Add a button to trigger inference with custom styling
            st.markdown("""
            <style>
            div[data-testid="stButton"] > button#policy_analysis_btn {
                background-color: #3498db;
                color: white;
                border: 2px solid #3498db;
                padding: 0.5rem 1rem;
                font-weight: 600;
                border-radius: 4px;
                text-align: center;
                margin: 1rem 0;
                display: block;
                width: 100%;
            }
            div[data-testid="stButton"] > button#policy_analysis_btn:hover {
                background-color: #2980b9;
                border-color: #2980b9;
            }
            </style>
            """, unsafe_allow_html=True)
            
            analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")
            
            # Define nodes for the decision tree
            nodes = [
                {"id": "request", "label": "Access Request", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "purpose", "label": "Business Purpose", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "policy", "label": "Applicable Policy", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "data_elements", "label": "Data Elements", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "operation", "label": "Operation Type", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Policy Compliance Check", "color": "#1abc9c", "shape": "box", "size": 25},
                {"id": "allowed", "label": "Access Decision", "color": "#3498db", "shape": "box", "size": 25},
                {"id": "restrictions", "label": "Usage Restrictions", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "rationale", "label": "Decision Rationale", "color": "#e74c3c", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "request", "target": "purpose", "arrows": "to", "label": "has"},
                {"source": "purpose", "target": "policy", "arrows": "to", "label": "governed by"},
                {"source": "request", "target": "data_elements", "arrows": "to", "label": "requests"},
                {"source": "request", "target": "operation", "arrows": "to", "label": "performs"},
                {"source": "purpose", "target": "lookup", "arrows": "to"},
                {"source": "data_elements", "target": "lookup", "arrows": "to"},
                {"source": "operation", "target": "lookup", "arrows": "to"},
                {"source": "policy", "target": "lookup", "arrows": "to"},
                {"source": "lookup", "target": "allowed", "arrows": "to"},
                {"source": "lookup", "target": "restrictions", "arrows": "to"},
                {"source": "lookup", "target": "rationale", "arrows": "to"}
            ]
            
            # Render the decision tree
            self._render_decision_tree(nodes, edges, title="Policy Decision Tree")
        
        with col2:
            st.subheader("Policy Compliance Analysis")
            
            if analyze_button:
                if not selected_purpose or not selected_data_elements:
                    st.warning("Please select both Purpose and at least one Data Element")
                else:
                    self._analyze_policy_compliance(
                        selected_purpose, 
                        selected_data_elements,
                        selected_operation,
                        selected_jurisdiction if selected_jurisdiction != "Any" else None
                    )
            else:
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">Sample Result</h3>
                    <p>Policy compliance analysis will appear here after analysis...</p>
                </div>
                """, unsafe_allow_html=True)

    def _analyze_policy_compliance_for_activity(self, purpose, data_elements, operation):
        """Analyze policy compliance for a processing activity.
        This is a simplified version of _analyze_policy_compliance for use in the Processing Activities section.
        
        Args:
            purpose (str): The business purpose for data access
            data_elements (list): List of data elements being accessed
            operation (str): The operation type (read, write, share)
        """
        # Get policies from the database
        policies = self.glossary_repository.get_policies()
        
        # Find the access control policy
        access_control_policy = None
        for policy in policies:
            if policy["policy_type"] == "Access Control":
                access_control_policy = policy
                break
        
        if not access_control_policy:
            st.error("No Access Control Policy found in the database.")
            return
        
        # Get purpose ID
        purpose_id = None
        purposes = self.glossary_repository.get_purposes()
        for p in purposes:
            if p["name"] == purpose:
                purpose_id = p["id"]
                break
        
        if not purpose_id:
            st.error(f"Purpose '{purpose}' not found in the database.")
            return
        
        # Get data element IDs
        data_element_ids = {}
        all_data_elements = self.glossary_repository.get_data_elements()
        for data_element in data_elements:
            for de in all_data_elements:
                if de["name"] == data_element:
                    data_element_ids[data_element] = de["id"]
                    break
        
        # Display applicable policy
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <p><strong>Applicable Policy:</strong> {access_control_policy['name']} ({access_control_policy['policy_type']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get policy purpose data elements
        policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
            policy_id=access_control_policy['id'], 
            purpose_id=purpose_id
        )
        
        # Get policy purpose data usages
        policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
            policy_id=access_control_policy['id'], 
            purpose_id=purpose_id
        )
        
        # Create a DataFrame to hold the decisions
        decisions_data = {
            "Data Element": [],
            "Operation": [],
            "Decision": [],
            "Restrictions": []
        }
        
        # Process each data element using the policy data from the repository
        denied_operations = False
        for data_element in data_elements:
            data_element_id = data_element_ids.get(data_element)
            
            # Default values if no specific rules found
            decision = "Denied"
            restrictions = "No explicit permission in policy"
            decision_color = "#e74c3c"
            
            # Check if there's a usage rule for this data element, purpose, and operation
            for usage in policy_purpose_data_usages:
                if (usage["data_element_name"] == data_element and 
                    usage["operation"] == operation):
                    
                    if usage["allowed"]:
                        if usage["restrictions"]:
                            decision = "Allowed with Restrictions"
                            restrictions = usage["restrictions"]
                            decision_color = "#f39c12"
                        else:
                            decision = "Allowed"
                            restrictions = "None"
                            decision_color = "#2ecc71"
                    else:
                        decision = "Denied"
                        restrictions = usage["restrictions"] if usage["restrictions"] else "Operation not allowed for this purpose"
                        decision_color = "#e74c3c"
                        denied_operations = True
                    break
            
            # If no specific usage rule found, check if the data element is allowed for this purpose
            if decision == "Denied" and restrictions == "No explicit permission in policy":
                for element in policy_purpose_data_elements:
                    if element["data_element_name"] == data_element:
                        if element["access_allowed"]:
                            # Default to allowed for read operations if no specific rule exists
                            if operation == "read":
                                decision = "Allowed"
                                restrictions = "None"
                                decision_color = "#2ecc71"
                            else:
                                # For write/share, still require explicit permission
                                denied_operations = True
                        else:
                            denied_operations = True
                        break
            
            # Add row to the DataFrame
            decisions_data["Data Element"].append(data_element)
            decisions_data["Operation"].append(operation)
            decisions_data["Decision"].append(decision)
            decisions_data["Restrictions"].append(restrictions)
        
        # Create and display the DataFrame
        decisions_df = pd.DataFrame(decisions_data)
        
        # Apply styling to the Decision column based on the decision
        def highlight_decision(val):
            if val == "Allowed":
                return 'background-color: #d4edda; color: #155724'
            elif val == "Allowed with Restrictions":
                return 'background-color: #fff3cd; color: #856404'
            else:  # Denied
                return 'background-color: #f8d7da; color: #721c24'
        
        # Display the styled DataFrame
        st.dataframe(decisions_df.style.applymap(highlight_decision, subset=['Decision']), use_container_width=True)
        
        # Add compliance recommendations if there are denied operations
        if denied_operations:
            st.markdown("""
            <div style="margin-top: 20px; background-color: #fef9e7; padding: 15px; border-radius: 5px; border-left: 5px solid #f39c12;">
                <h4 style="color: #f39c12; margin-top: 0;">Compliance Issues Detected</h4>
                <p>This processing activity has potential policy compliance issues. Consider:</p>
                <ul>
                    <li>Limiting data access to only what is necessary for the stated purpose</li>
                    <li>Using anonymized or pseudonymized data when possible</li>
                    <li>Documenting the business justification for accessing sensitive data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def _analyze_policy_compliance(self, purpose, data_elements, operation, jurisdiction=None):
        """Analyze policy compliance based on purpose, data elements, and operation.
        
        Args:
            purpose (str): The business purpose for data access
            data_elements (list): List of data elements being accessed
            operation (str): The operation type (read, write, share)
            jurisdiction (str, optional): The applicable jurisdiction. Defaults to None.
        """
        # Get policies from the database
        policies = self.glossary_repository.get_policies()
        
        # Find the access control policy
        access_control_policy = None
        for policy in policies:
            if policy["policy_type"] == "Access Control":
                access_control_policy = policy
                break
        
        if not access_control_policy:
            st.error("No Access Control Policy found in the database.")
            return
        
        # Get purpose ID
        purpose_id = None
        purposes = self.glossary_repository.get_purposes()
        for p in purposes:
            if p["name"] == purpose:
                purpose_id = p["id"]
                break
        
        if not purpose_id:
            st.error(f"Purpose '{purpose}' not found in the database.")
            return
        
        # Get data element IDs
        data_element_ids = {}
        all_data_elements = self.glossary_repository.get_data_elements()
        for data_element in data_elements:
            for de in all_data_elements:
                if de["name"] == data_element:
                    data_element_ids[data_element] = de["id"]
                    break
                
        # Display applicable policy
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <h4 style="color: #3498db;">Applicable Policy</h4>
            <p><strong>Policy:</strong> {access_control_policy['name']}</p>
            <p><strong>Type:</strong> {access_control_policy['policy_type']}</p>
            <p><strong>Status:</strong> {access_control_policy['status']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get policy purpose data elements
        policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
            policy_id=access_control_policy['id'], 
            purpose_id=purpose_id
        )
        
        # Get policy purpose data usages
        policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
            policy_id=access_control_policy['id'], 
            purpose_id=purpose_id
        )
        
        # Prepare data for the decisions table
        st.subheader("Data Access Decisions")
        
        # Create a DataFrame to hold the decisions
        decisions_data = {
            "Data Element": [],
            "Operation": [],
            "Decision": [],
            "Restrictions": []
        }
        
        # Process each data element using the policy data from the repository
        denied_operations = False
        for data_element in data_elements:
            data_element_id = data_element_ids.get(data_element)
            
            # Default values if no specific rules found
            decision = "Denied"
            restrictions = "No explicit permission in policy"
            decision_color = "#e74c3c"
            
            # Check if there's a usage rule for this data element, purpose, and operation
            for usage in policy_purpose_data_usages:
                if (usage["data_element_name"] == data_element and 
                    usage["operation"] == operation):
                    
                    if usage["allowed"]:
                        if usage["restrictions"]:
                            decision = "Allowed with Restrictions"
                            restrictions = usage["restrictions"]
                            decision_color = "#f39c12"
                        else:
                            decision = "Allowed"
                            restrictions = "None"
                            decision_color = "#2ecc71"
                    else:
                        decision = "Denied"
                        restrictions = usage["restrictions"] if usage["restrictions"] else "Operation not allowed for this purpose"
                        decision_color = "#e74c3c"
                        denied_operations = True
                    break
            
            # If no specific usage rule found, check if the data element is allowed for this purpose
            if decision == "Denied" and restrictions == "No explicit permission in policy":
                for element in policy_purpose_data_elements:
                    if element["data_element_name"] == data_element:
                        if element["access_allowed"]:
                            # Default to allowed for read operations if no specific rule exists
                            if operation == "read":
                                decision = "Allowed"
                                restrictions = "None"
                                decision_color = "#2ecc71"
                            else:
                                # For write/share, still require explicit permission
                                denied_operations = True
                        else:
                            denied_operations = True
                        break
            
            # Add row to the DataFrame
            decisions_data["Data Element"].append(data_element)
            decisions_data["Operation"].append(operation)
            decisions_data["Decision"].append(decision)
            decisions_data["Restrictions"].append(restrictions)
        
        # Create and display the DataFrame
        decisions_df = pd.DataFrame(decisions_data)
        
        # Apply styling to the Decision column based on the decision
        def highlight_decision(val):
            if val == "Allowed":
                return 'background-color: #d4edda; color: #155724'
            elif val == "Allowed with Restrictions":
                return 'background-color: #fff3cd; color: #856404'
            else:  # Denied
                return 'background-color: #f8d7da; color: #721c24'
        
        # Display the styled DataFrame
        st.dataframe(decisions_df.style.applymap(highlight_decision, subset=['Decision']), use_container_width=True)
        
        # Add decision rationale
        st.markdown("""
        <div style="margin-top: 20px;">
            <h4 style="color: #3498db;">Decision Rationale</h4>
            <p>The policy compliance decision is based on:</p>
            <ul>
                <li>Purpose limitation principles defined in the Data Access Control Policy</li>
                <li>Data element sensitivity classification</li>
                <li>Operation type and associated risks</li>
                <li>Purpose-specific data access rules</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Add compliance recommendations if there are denied operations
        if denied_operations:
            st.markdown("""
            <div style="margin-top: 20px; background-color: #fef9e7; padding: 15px; border-radius: 5px; border-left: 5px solid #f39c12;">
                <h4 style="color: #f39c12; margin-top: 0;">Compliance Recommendations</h4>
                <p>To ensure policy compliance:</p>
                <ul>
                    <li>Limit data access to only what is necessary for the stated purpose</li>
                    <li>Use anonymized or pseudonymized data when possible</li>
                    <li>Document the business justification for accessing sensitive data</li>
                    <li>Implement additional security controls for sensitive data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

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
