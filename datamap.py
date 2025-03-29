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
                <h3>What is a Law?</h3>
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
                <h3>What are Jurisdictions?</h3>
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
                <h3>What is a Legal Basis?</h3>
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
                <h3>What are Data Elements?</h3>
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
                <h3>What are Data Subject Types?</h3>
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
                <h3>What are Data Categories?</h3>
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
                <h3>What is Context?</h3>
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
                <h3>What is Sensitivity?</h3>
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
            st.title("Data Map")
            st.markdown("### Navigation")
            
            # Create navigation menu in sidebar
            
            # Store the current section in session state if not already there
            if 'current_section' not in st.session_state:
                st.session_state['current_section'] = 'Glossary'
            
            # Navigation buttons
            if st.button("Glossary", key="glossary_btn"):
                st.session_state['current_section'] = 'Glossary'
            
            if st.button("Regulatory", key="regulatory_btn"):
                st.session_state['current_section'] = 'Regulatory'
            
            if st.button("Inventory", key="inventory_btn"):
                st.session_state['current_section'] = 'Inventory'
            
            # Highlight active section
            st.markdown(f"""
            <style>
            div[data-testid="stButton"] > button[kind="secondary"] {{
                background-color: #3498db;
                color: white;
            }}
            div[data-testid="stButton"] > button#{'glossary_btn' if st.session_state['current_section'] == 'Glossary' else 
                                                 'regulatory_btn' if st.session_state['current_section'] == 'Regulatory' else
                                                 'inventory_btn'} {{
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
        elif st.session_state['current_section'] == 'Inventory':
            self.inventory_section()


if __name__ == "__main__":
    app = DataMap()
    app.run()
