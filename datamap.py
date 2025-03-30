import os
# Set environment variables to avoid config issues
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "500"

import streamlit as st
import pandas as pd

from repositories.GlossaryRepository import GlossaryRepository
from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.DatabaseManager import DatabaseManager

class DataMap:
    def __init__(self):
        """Initialize the DataMap application with repositories."""
        self.database_manager = DatabaseManager()
        self.glossary_repository = GlossaryRepository(self.database_manager.connection)
        self.regulatory_metadata_repository = RegulatoryMetadataRepository(self.database_manager.connection)
        
        # Initialize database tables if connection is available
        if self.database_manager.connection:
            # Setup tables
            self.glossary_repository.setup_tables()
            self.regulatory_metadata_repository.setup_tables()
            
            # Check if data needs to be seeded
            laws = self.glossary_repository.get_laws()
            if not laws:
                # Seed glossary data first
                self.glossary_repository.seed_all_data()
                # Then seed regulatory metadata that depends on glossary data
                self.regulatory_metadata_repository.seed_all_data()

    @staticmethod
    def divider(height=1):
        """Utility function to create a divider with specified height."""
        st.markdown(
            f"<hr style='height:{height}px; margin-top: 0; margin-bottom: 0; border-width:0; background: lightblue;'>",
            unsafe_allow_html=True
        )

    def configure_page(self):
        """Configure the Streamlit page settings."""
        st.set_page_config(page_title="Data Map - Regulatory and Data Mapping Tool", layout="wide")

        # Inject custom CSS for styling
        st.markdown("""
        <style>
        /* Main styling */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #2c3e50;
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
        
        /* Button styling */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 15px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #2980b9;
            color: white;
        }
        
        /* Sidebar menu styling */
        .sidebar-menu {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            background-color: #34495e;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .sidebar-menu:hover {
            background-color: #2c3e50;
        }
        
        .sidebar-menu.active {
            background-color: #1abc9c;
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

    def glossary_section(self):
        """Handle the Glossary section with its tabs."""
        st.header("Glossary")
        
        tabs = st.tabs([
            "Law", "Jurisdictions", "Legal Basis", "Data Elements", 
            "Data Subject Types", "Data Categories", "Context", "Sensitivity"
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

    def regulatory_metadata_section(self):
        """Handle the Regulatory Metadata section with its tabs."""
        st.header("Regulatory Metadata")
        
        tabs = st.tabs([
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
            "Context Data Subject Type Data Category Sensitivity"
        ])
        
        # Law Jurisdiction tab
        with tabs[0]:
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
                
                st.dataframe(pd.DataFrame(law_jurisdiction_data))
            else:
                st.warning("No data available in the database.")
        
        # Law Legal Basis tab
        with tabs[1]:
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
                
                st.dataframe(pd.DataFrame(law_legal_basis_data))
            else:
                st.warning("No data available in the database.")
        
        # Law Incident Breach Notification tab
        with tabs[2]:
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
                
                st.dataframe(pd.DataFrame(law_breach_data))
            else:
                st.warning("No data available in the database.")
        
        # Law Transfer tab
        with tabs[3]:
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
                
                st.dataframe(pd.DataFrame(law_transfer_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Subject Access Request tab
        with tabs[4]:
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
                
                st.dataframe(pd.DataFrame(dsar_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Category Data Element tab
        with tabs[5]:
            st.markdown("""
            <div class="card">
                <h3>Data Category Data Element Mapping</h3>
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
                
                st.dataframe(pd.DataFrame(mapping_data))
            else:
                st.warning("No data available in the database.")
        
        # Law Data Subject Type Data Element Sensitivity tab
        with tabs[6]:
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
                
                st.dataframe(pd.DataFrame(mapping_data))
            else:
                st.warning("No data available in the database.")
        
        # Law Data Subject Type Data Category Sensitivity tab
        with tabs[7]:
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
                
                st.dataframe(pd.DataFrame(mapping_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Subject Type Data Category Sensitivity tab
        with tabs[8]:
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
                
                st.dataframe(pd.DataFrame(mapping_data))
            else:
                st.warning("No data available in the database.")
        
        # Data Subject Type Data Element Sensitivity tab
        with tabs[9]:
            st.markdown("""
            <div class="card">
                <h3>Data Subject Type Data Element Sensitivity</h3>
                <p>This section maps data subject types to specific data elements and their sensitivity levels, independent of specific laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            
            mappings = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            
            mapping_data = {
                "Data Subject Type": [],
                "Data Element": [],
                "Sensitivity": []
            }
            for mapping in mappings:
                mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                mapping_data["Data Element"].append(mapping["data_element_name"])
                mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
            
            st.dataframe(pd.DataFrame(mapping_data))
            
        # Law Context Data Subject Type Data Category Sensitivity tab
        with tabs[10]:
            st.markdown("""
            <div class="card">
                <h3>Law Context Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps laws, processing contexts, data subject types, data categories, and their sensitivity levels, providing a comprehensive view of contextual data protection requirements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            mappings = self.regulatory_metadata_repository.get_law_context_data_subject_type_data_category_sensitivities()
            
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
            
            st.dataframe(pd.DataFrame(mapping_data))
        
        # Context Data Subject Type Data Category Sensitivity tab
        with tabs[11]:
            st.markdown("""
            <div class="card">
                <h3>Context Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps processing contexts, data subject types, data categories, and their sensitivity levels, independent of specific laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            
            mappings = self.regulatory_metadata_repository.get_context_data_subject_type_data_category_sensitivities()
            
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
            
            st.dataframe(pd.DataFrame(mapping_data))
            

    def inventory_section(self):
        """Handle the Inventory section with its tabs."""
        st.header("Inventory")
        
        tabs = st.tabs([
            "Assets", "Processing Activities", "Legal Entities", "Vendors"
        ])
        
        # Assets tab
        with tabs[0]:
            st.subheader("Assets Inventory")
            st.markdown("""
            <div class="card">
                <h3>Data Assets</h3>
                <p>This section provides an inventory of data assets within the organization, including databases, 
                applications, and other systems that store or process personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # For now, we'll use sample data since we haven't created an assets table yet
            assets_data = {
                "Asset Name": ["Customer Database", "Marketing Platform", "HR System", "Mobile App"],
                "Type": ["Database", "SaaS Application", "Internal System", "Mobile Application"],
                "Data Categories": ["Customer PII", "Marketing Data", "Employee Data", "User Data"],
                "Risk Level": ["High", "Medium", "High", "Medium"],
                "Owner": ["Data Team", "Marketing", "HR Department", "Product Team"]
            }
            st.dataframe(pd.DataFrame(assets_data))
            
            # Add a note about future integration
            st.info("This section will be integrated with the database in a future update. Currently showing sample data.")
            
            # Add a form to add new assets (placeholder for now)
            with st.expander("Add New Asset"):
                st.text_input("Asset Name")
                st.selectbox("Asset Type", ["Database", "SaaS Application", "Internal System", "Mobile Application", "Website", "API", "Other"])
                
                # Get data categories from repository for the multi-select
                
                data_categories = self.glossary_repository.get_data_categories()
                if data_categories:
                    category_options = [dc["name"] for dc in data_categories]
                    st.multiselect("Data Categories", options=category_options)
                else:
                    st.multiselect("Data Categories", options=["Customer PII", "Marketing Data", "Employee Data", "User Data"])
                
                st.selectbox("Risk Level", ["Low", "Medium", "High"])
                st.text_input("Owner")
                st.button("Add Asset")
        
        # Processing Activities tab
        with tabs[1]:
            st.subheader("Processing Activities")
            st.markdown("""
            <div class="card">
                <h3>Data Processing Activities</h3>
                <p>This section catalogs the various data processing activities performed by the organization, 
                as required by many data protection regulations including GDPR Article 30.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # For now, we'll use sample data since we haven't created a processing activities table yet
            processing_data = {
                "Activity Name": ["Customer Onboarding", "Marketing Campaigns", "Employee Management", "App Analytics"],
                "Purpose": ["Service Provision", "Marketing", "Employment", "Product Improvement"],
                "Data Categories": ["Identity, Contact", "Contact, Preferences", "HR Data, Financial", "Usage Data"],
                "Legal Basis": ["Contract", "Consent", "Legal Obligation", "Legitimate Interest"],
                "Retention Period": ["7 years", "3 years", "Duration of employment + 5 years", "2 years"]
            }
            st.dataframe(pd.DataFrame(processing_data))
            
            # Add a note about future integration
            st.info("This section will be integrated with the database in a future update. Currently showing sample data.")
            
            # Add a form to add new processing activities (placeholder for now)
            with st.expander("Add New Processing Activity"):
                st.text_input("Activity Name")
                
                # Get purposes (contexts) from repository for the select box
                
                contexts = self.glossary_repository.get_contexts()
                if contexts:
                    purpose_options = [ctx["name"] for ctx in contexts]
                    st.selectbox("Purpose", options=purpose_options)
                else:
                    st.selectbox("Purpose", options=["Service Provision", "Marketing", "Employment", "Product Improvement"])
                
                # Get data categories from repository for the multi-select
                
                data_categories = self.glossary_repository.get_data_categories()
                if data_categories:
                    category_options = [dc["name"] for dc in data_categories]
                    st.multiselect("Data Categories", options=category_options)
                else:
                    st.multiselect("Data Categories", options=["Identity", "Contact", "Preferences", "HR Data", "Financial", "Usage Data"])
                
                # Get legal bases from repository for the select box
                
                legal_bases = self.glossary_repository.get_legal_bases()
                if legal_bases:
                    legal_basis_options = [lb["name"] for lb in legal_bases]
                    st.selectbox("Legal Basis", options=legal_basis_options)
                else:
                    st.selectbox("Legal Basis", options=["Consent", "Contract", "Legal Obligation", "Legitimate Interest"])
                
                st.text_input("Retention Period")
                st.button("Add Processing Activity")
        
        # Legal Entities tab
        with tabs[2]:
            st.subheader("Legal Entities")
            st.markdown("""
            <div class="card">
                <h3>Legal Entities</h3>
                <p>This section provides an inventory of legal entities relevant to data protection compliance, 
                such as controllers, processors, and joint controllers.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # For now, we'll use sample data since we haven't created a legal entities table yet
            legal_entities_data = {
                "Entity Name": ["Main Company Inc.", "Subsidiary LLC", "Partner Corp", "Vendor Inc."],
                "Type": ["Controller", "Joint Controller", "Processor", "Sub-processor"],
                "Country": ["United States", "United Kingdom", "Germany", "India"],
                "Role": ["Parent Company", "Subsidiary", "Partner", "Service Provider"]
            }
            st.dataframe(pd.DataFrame(legal_entities_data))
            
            # Add a note about future integration
            st.info("This section will be integrated with the database in a future update. Currently showing sample data.")
            
            # Add a form to add new legal entities (placeholder for now)
            with st.expander("Add New Legal Entity"):
                st.text_input("Entity Name")
                st.selectbox("Type", options=["Controller", "Joint Controller", "Processor", "Sub-processor"])
                st.text_input("Country")
                st.text_input("Role")
                st.button("Add Legal Entity")
        
        # Vendors tab
        with tabs[3]:
            st.subheader("Vendors")
            st.markdown("""
            <div class="card">
                <h3>Vendors</h3>
                <p>This section provides an inventory of vendors that process personal data on behalf of the organization, 
                including details about their data protection practices and contractual arrangements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # For now, we'll use sample data since we haven't created a vendors table yet
            vendors_data = {
                "Vendor Name": ["Cloud Provider Inc.", "Marketing Platform LLC", "HR Software Corp", "Analytics Co."],
                "Service Type": ["Cloud Storage", "Email Marketing", "HR Management", "Web Analytics"],
                "Data Categories": ["All Company Data", "Customer Contact Info", "Employee Data", "Website Usage Data"],
                "Contract Status": ["Active", "Active", "Active", "Under Review"],
                "DPA in Place": ["Yes", "Yes", "Yes", "Pending"]
            }
            st.dataframe(pd.DataFrame(vendors_data))
            
            # Add a note about future integration
            st.info("This section will be integrated with the database in a future update. Currently showing sample data.")
            
            # Add a form to add new vendors (placeholder for now)
            with st.expander("Add New Vendor"):
                st.text_input("Vendor Name")
                st.text_input("Service Type")
                
                # Get data categories from repository for the multi-select
                
                data_categories = self.glossary_repository.get_data_categories()
                if data_categories:
                    category_options = [dc["name"] for dc in data_categories]
                    st.multiselect("Data Categories", options=category_options)
                else:
                    st.multiselect("Data Categories", options=["Customer PII", "Marketing Data", "Employee Data", "User Data"])
                
                st.selectbox("Contract Status", options=["Active", "Pending", "Expired", "Under Review"])
                st.selectbox("DPA in Place", options=["Yes", "No", "Pending"])
                st.button("Add Vendor")

    def run(self):
        """Main function to run the Streamlit app."""
        # Configure the page
        self.configure_page()

        # Main header and introduction
        if 'current_section' not in st.session_state or st.session_state['current_section'] == 'Glossary':
            st.title("DataMap: Privacy Regulation Mapping Tool")
            
            st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>This is a comprehensive tool designed to help organizations navigate the complex landscape of privacy regulations. 
                This application provides a structured view of privacy laws, their requirements, and how they relate to different types of data and processing activities.</p>
                </div>''', unsafe_allow_html=True)

            self.divider(2)
        
        # Create sidebar with navigation
        with st.sidebar:
            st.title("Regulatory Metamodel")
            
            # Create navigation menu in sidebar
            
            # Store the current section in session state if not already there
            if 'current_section' not in st.session_state:
                st.session_state['current_section'] = 'Glossary'
            
            # Navigation buttons
            if st.button("Glossary", key="glossary_btn"):
                st.session_state['current_section'] = 'Glossary'
            
            if st.button("Regulatory Metadata", key="regulatory_btn"):
                st.session_state['current_section'] = 'Regulatory'
                
            if st.button("Decision Tree", key="decision_tree_btn"):
                st.session_state['current_section'] = 'Decision Tree'
                
            if st.button("Sensitivity Inference API", key="sensitivity_api_btn"):
                st.session_state['current_section'] = 'Sensitivity API'
                
            if st.button("Legal Basis Inference API", key="legal_basis_api_btn"):
                st.session_state['current_section'] = 'Legal Basis API'
                
            if st.button("Breach Notification API", key="breach_api_btn"):
                st.session_state['current_section'] = 'Breach API'
            
            # Highlight active section
            st.markdown(f"""
            <style>
            div[data-testid="stButton"] > button[kind="secondary"] {{
                background-color: #3498db;
                color: white;
            }}
            div[data-testid="stButton"] > button#{'glossary_btn' if st.session_state['current_section'] == 'Glossary' else 
                                                 'regulatory_btn' if st.session_state['current_section'] == 'Regulatory' else
                                                 'decision_tree_btn' if st.session_state['current_section'] == 'Decision Tree' else
                                                 'sensitivity_api_btn' if st.session_state['current_section'] == 'Sensitivity API' else
                                                 'legal_basis_api_btn' if st.session_state['current_section'] == 'Legal Basis API' else
                                                 'breach_api_btn'} {{
                background-color: #1abc9c;
                color: white;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            # Add some space
            st.markdown("<br>", unsafe_allow_html=True)
            self.divider()
            
        # Main content area based on selected section
        if st.session_state['current_section'] == 'Glossary':
            self.glossary_section()
        elif st.session_state['current_section'] == 'Regulatory':
            self.regulatory_metadata_section()
        elif st.session_state['current_section'] == 'Decision Tree':
            self.decision_tree_section()
        elif st.session_state['current_section'] == 'Sensitivity API':
            self.sensitivity_inference_api()
        elif st.session_state['current_section'] == 'Legal Basis API':
            self.legal_basis_inference_api()
        elif st.session_state['current_section'] == 'Breach API':
            self.breach_notification_api()

    def decision_tree_section(self):
        """Visualize the regulatory metadata as a decision tree using PyVis with physics.
        Initially the network stabilizes (nodes become static) but if you drag a node the physics
        simulation restarts and nodes bounce. A legend is shown below the graph.
        """
        import os
        import tempfile
        from pyvis.network import Network
        import streamlit.components.v1 as components

        st.header("Regulatory Decision Tree (PyVis)")
        st.markdown("""
        <div class="card">
            <p>This section visualizes the regulatory metadata as a decision tree using PyVis with a physics-based layout.
            The graph will stabilize initially, but dragging a node will re-enable physics and cause a bouncing effect.</p>
        </div>
        """, unsafe_allow_html=True)

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
        st.header("Sensitivity Inference API")
        
        st.markdown("""
        <div class="card">
            <p>This API allows you to determine the sensitivity level of data based on regulatory metadata. 
            Select the relevant attributes and the system will infer the appropriate sensitivity level 
            according to applicable regulations.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.header("Legal Basis Inference API")
        
        st.markdown("""
        <div class="card">
            <p>This API helps determine the appropriate legal basis for processing personal data 
            based on regulatory metadata. Select the relevant parameters and the system will 
            recommend suitable legal bases according to applicable regulations.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                selected_context = st.selectbox("Select Processing Purpose", options=context_options)
            else:
                selected_context = None
            
            # Get data categories
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data_category = st.selectbox("Select Data Category", options=dc_options)
            else:
                st.warning("No data categories available.")
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
        
        with col2:
            st.subheader("Legal Basis Recommendations")
            
            if infer_button:
                # Display a spinner while "processing"
                with st.spinner("Analyzing regulatory metadata..."):
                    # Get legal bases based on the selected parameters
                    legal_bases = self._infer_legal_basis(
                        selected_law, 
                        selected_jurisdiction,
                        selected_dst, 
                        selected_context, 
                        selected_data_category,
                        selected_sensitivity
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
                            
                            # Add compliance requirements based on the legal basis
                            st.markdown("#### Compliance Requirements:")
                            
                            if "consent" in legal_basis['name'].lower():
                                st.markdown("""
                                - Must be freely given, specific, informed, and unambiguous
                                - Clear affirmative action required (no pre-ticked boxes)
                                - Must be as easy to withdraw as to give consent
                                - Keep records of when and how consent was obtained
                                - For children, obtain parental/guardian consent where required
                                - Regular review and refresh of consent may be necessary
                                """)
                            elif "contract" in legal_basis['name'].lower():
                                st.markdown("""
                                - Processing must be necessary for the performance of a contract
                                - Cannot process more data than needed for the contract
                                - Document the contractual necessity for the processing
                                - Ensure data subject is a party to the contract
                                - Consider alternative legal bases for any ancillary processing
                                """)
                            elif "legal obligation" in legal_basis['name'].lower():
                                st.markdown("""
                                - Clearly identify the specific legal obligation
                                - Document the legal provision requiring the processing
                                - Process only what is necessary to comply with the obligation
                                - Inform data subjects about the legal requirement
                                - Maintain records of the legal basis assessment
                                """)
                            elif "vital interest" in legal_basis['name'].lower():
                                st.markdown("""
                                - Only use in life-or-death situations or serious harm prevention
                                - Document why other legal bases are not applicable
                                - Process only what is necessary to protect vital interests
                                - Switch to another legal basis once the emergency has passed
                                - Consider whether the data subject can provide consent
                                """)
                            elif "public interest" in legal_basis['name'].lower() or "official authority" in legal_basis['name'].lower():
                                st.markdown("""
                                - Must be based on EU or Member State law
                                - Document the public interest or official authority
                                - Process only what is necessary for the specified purpose
                                - Consider data minimization principles
                                - Implement appropriate safeguards
                                - Respect data subject rights, including right to object
                                """)
                            elif "legitimate interest" in legal_basis['name'].lower():
                                st.markdown("""
                                - Conduct and document a Legitimate Interest Assessment (LIA)
                                - Balance your interests against the individual's rights
                                - Consider reasonable expectations of data subjects
                                - Implement appropriate safeguards and transparency
                                - Respect the right to object to processing
                                - Regularly review the legitimate interest assessment
                                """)
                            else:
                                st.markdown("- Document your assessment of this legal basis")
                                st.markdown("- Ensure processing is necessary for the stated purpose")
                                st.markdown("- Implement appropriate safeguards")
                                st.markdown("- Maintain records of processing activities")
                            
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
                    - **Data Subject Type**: {selected_dst}
                    - **Processing Purpose**: {selected_context}
                    - **Data Category**: {selected_data_category}
                    - **Sensitivity Level**: {selected_sensitivity}
                    
                    According to the regulatory metadata, when processing {selected_data_category} data 
                    for {selected_dst} under {selected_law} for the purpose of {selected_context}, 
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
    
    def _infer_legal_basis(self, law, jurisdiction, data_subject_type, context, data_category, sensitivity):
        """Internal method to infer appropriate legal bases based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            jurisdiction (str): The name of the jurisdiction (can be None)
            data_subject_type (str): The name of the data subject type
            context (str): The name of the context/purpose
            data_category (str): The name of the data category
            sensitivity (str): The sensitivity level
            
        Returns:
            list: A list of recommended legal bases or None if not found
        """
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
        recommended_legal_bases = [lb for lb in all_legal_bases if lb["name"] in legal_basis_names]
        
        # Sort legal bases based on appropriateness for the given parameters
        # This is a simplified logic - in a real system, this would be more sophisticated
        
        # For high sensitivity data, prioritize explicit consent and legal obligation
        if sensitivity.lower() == "high":
            recommended_legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "legal obligation" in lb["name"].lower()), 
                reverse=True)
        # For medium sensitivity, legitimate interests might be appropriate
        elif sensitivity.lower() == "medium":
            recommended_legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "contract" in lb["name"].lower(), 
                 "legitimate" in lb["name"].lower()), 
                reverse=True)
        # For low sensitivity, contract and legitimate interests are often suitable
        else:
            recommended_legal_bases.sort(key=lambda lb: 
                ("contract" in lb["name"].lower(), "legitimate" in lb["name"].lower(), 
                 "consent" in lb["name"].lower()), 
                reverse=True)
        
        return recommended_legal_bases
        
    def breach_notification_api(self):
        """Implement an incident breach notification API based on regulatory metadata.
        This helps users determine notification requirements for data breaches.
        """
        st.header("Incident Breach Notification API")
        
        st.markdown("""
        <div class="card">
            <p>This API helps determine the notification requirements for data breaches based on regulatory metadata. 
            Input the details of the breach incident, and the system will provide guidance on notification 
            requirements, timelines, and authorities to notify.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                affected_data_categories = st.multiselect("Affected Data Categories", options=dc_options)
            else:
                st.warning("No data categories available.")
                return
            
            # Get data subject types
            data_subject_types = self.glossary_repository.get_data_subject_types()
            if data_subject_types:
                dst_options = [dst["name"] for dst in data_subject_types]
                affected_data_subjects = st.multiselect("Affected Data Subject Types", options=dst_options)
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
            
            # Add a button to trigger analysis
            analyze_button = st.button("Analyze Notification Requirements")
        
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


if __name__ == "__main__":
    app = DataMap()
    app.run()
