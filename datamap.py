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
            self._check_and_seed_data()
    
    def _check_and_seed_data(self):
        """Check if data exists in the database and seed it if necessary."""
        if self.database_manager.connection:
            # Check if any laws exist
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
            if self.database_manager.connection:
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
                    st.warning("No law data available in the database.")
            else:
                # Fallback to sample data if no database connection
                law_data = {
                    "Law Name": ["GDPR", "CCPA/CPRA", "LGPD", "PIPEDA"],
                    "Region": ["European Union", "California, USA", "Brazil", "Canada"],
                    "Effective Date": ["May 25, 2018", "Jan 1, 2020/Jan 1, 2023", "Aug 15, 2020", "Jan 1, 2004"],
                    "Key Features": [
                        "Data subject rights, DPO requirement, 72-hour breach notification",
                        "Right to know, delete, opt-out of sale, non-discrimination",
                        "Similar to GDPR, includes data subject rights and DPO requirements",
                        "Consent requirements, access rights, oversight by Privacy Commissioner"
                    ]
                }
                st.dataframe(pd.DataFrame(law_data))
                st.info("Using sample data - no database connection available.")
        
        # Jurisdictions tab
        with tabs[1]:
            st.subheader("Jurisdictions")
            st.markdown("""
            <div class="card">
                <h3>What is a Jurisdiction?</h3>
                <p>A jurisdiction refers to the geographic area over which a legal authority extends, such as a country, 
                state, or region. Different jurisdictions may have different data protection laws and requirements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get jurisdiction data from repository
            if self.database_manager.connection:
                jurisdictions = self.glossary_repository.get_jurisdictions()
                if jurisdictions:
                    jurisdiction_data = {
                        "Jurisdiction": []
                    }
                    for jurisdiction in jurisdictions:
                        jurisdiction_data["Jurisdiction"].append(jurisdiction["name"])
                    
                    # Get law-jurisdiction relationships
                    law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
                    if law_jurisdictions:
                        # Create a mapping of jurisdictions to laws
                        jurisdiction_to_laws = {}
                        for lj in law_jurisdictions:
                            if lj["jurisdiction_name"] not in jurisdiction_to_laws:
                                jurisdiction_to_laws[lj["jurisdiction_name"]] = []
                            jurisdiction_to_laws[lj["jurisdiction_name"]].append(lj["law_name"])
                        
                        # Add laws to the jurisdiction data
                        jurisdiction_data["Key Laws"] = []
                        for j in jurisdiction_data["Jurisdiction"]:
                            if j in jurisdiction_to_laws:
                                jurisdiction_data["Key Laws"].append(", ".join(jurisdiction_to_laws[j]))
                            else:
                                jurisdiction_data["Key Laws"].append("")
                    
                    st.dataframe(pd.DataFrame(jurisdiction_data))
                else:
                    st.warning("No jurisdiction data available in the database.")
            else:
                # Fallback to sample data if no database connection
                jurisdiction_data = {
                    "Jurisdiction": ["European Union", "United States", "California", "Brazil", "Canada", "United Kingdom"],
                    "Type": ["Supranational", "Federal", "State", "National", "National", "National"],
                    "Key Laws": ["GDPR", "Various Federal Laws", "CCPA/CPRA", "LGPD", "PIPEDA", "UK GDPR, DPA 2018"]
                }
                st.dataframe(pd.DataFrame(jurisdiction_data))
                st.info("Using sample data - no database connection available.")
        
        # Legal Basis tab
        with tabs[2]:
            st.subheader("Legal Basis")
            st.markdown("""
            <div class="card">
                <h3>What is a Legal Basis?</h3>
                <p>A legal basis is the lawful ground for processing personal data. Under most data protection laws, 
                organizations must have a valid legal basis before they can process personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get legal basis data from repository
            if self.database_manager.connection:
                legal_bases = self.glossary_repository.get_legal_bases()
                if legal_bases:
                    legal_basis_data = {
                        "Legal Basis": [],
                        "Description": []
                    }
                    for lb in legal_bases:
                        legal_basis_data["Legal Basis"].append(lb["name"])
                        legal_basis_data["Description"].append(lb["description"])
                    
                    st.dataframe(pd.DataFrame(legal_basis_data))
                else:
                    st.warning("No legal basis data available in the database.")
            else:
                # Fallback to sample data
                legal_basis_data = {
                    "Legal Basis": ["Consent", "Contract", "Legal Obligation", "Vital Interests", "Public Task", "Legitimate Interests"],
                    "Description": [
                        "The data subject has given clear consent for processing their personal data for a specific purpose.",
                        "Processing is necessary for the performance of a contract with the data subject.",
                        "Processing is necessary for compliance with a legal obligation.",
                        "Processing is necessary to protect the vital interests of the data subject or another person.",
                        "Processing is necessary for the performance of a task carried out in the public interest.",
                        "Processing is necessary for the purposes of legitimate interests pursued by the controller."
                    ]
                }
                st.dataframe(pd.DataFrame(legal_basis_data))
                st.info("Using sample data - no database connection available.")
        
        # Data Elements tab
        with tabs[3]:
            st.subheader("Data Elements")
            st.markdown("""
            <div class="card">
                <h3>What are Data Elements?</h3>
                <p>Data elements are specific pieces of personal information that can be collected and processed. 
                They are the building blocks of personal data and can include identifiers, characteristics, and other information.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get data element data from repository
            if self.database_manager.connection:
                data_elements = self.glossary_repository.get_data_elements()
                if data_elements:
                    data_element_data = {
                        "Data Element": [],
                        "Description": []
                    }
                    for de in data_elements:
                        data_element_data["Data Element"].append(de["name"])
                        data_element_data["Description"].append(de["description"])
                    
                    st.dataframe(pd.DataFrame(data_element_data))
                else:
                    st.warning("No data element data available in the database.")
            else:
                # Fallback to sample data
                data_element_data = {
                    "Data Element": ["Name", "Email Address", "Phone Number", "Address", "IP Address", "Device ID"],
                    "Description": [
                        "An individual's first name, last name, or full name.",
                        "An individual's email address used for electronic communication.",
                        "An individual's telephone number used for voice communication.",
                        "An individual's physical address including street, city, state, and postal code.",
                        "A unique identifier assigned to a device connected to a network.",
                        "A unique identifier assigned to a specific device."
                    ]
                }
                st.dataframe(pd.DataFrame(data_element_data))
                st.info("Using sample data - no database connection available.")
        
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
            if self.database_manager.connection:
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
                    st.warning("No data subject type data available in the database.")
            else:
                # Fallback to sample data
                data_subject_type_data = {
                    "Data Subject Type": ["Customer", "Employee", "Contractor", "Job Applicant", "Website Visitor", "Minor"],
                    "Description": [
                        "An individual who purchases goods or services from an organization.",
                        "An individual who works for an organization under an employment contract.",
                        "An individual who provides services to an organization but is not an employee.",
                        "An individual who applies for a job at an organization.",
                        "An individual who visits an organization's website.",
                        "An individual under the age of 18 or the age of majority in their jurisdiction."
                    ]
                }
                st.dataframe(pd.DataFrame(data_subject_type_data))
                st.info("Using sample data - no database connection available.")
        
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
            if self.database_manager.connection:
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
                    st.warning("No data category data available in the database.")
            else:
                # Fallback to sample data
                data_category_data = {
                    "Data Category": ["Personal Identifiers", "Financial Information", "Health Information", "Biometric Information", "Location Data", "Online Activity"],
                    "Description": [
                        "Information that can directly identify an individual, such as name, email address, or phone number.",
                        "Information related to an individual's financial status, such as bank account details, credit card numbers, or income.",
                        "Information related to an individual's health status, medical history, or treatment.",
                        "Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data.",
                        "Information about an individual's physical location, such as GPS coordinates or IP address geolocation.",
                        "Information about an individual's online behavior, such as browsing history or search queries."
                    ]
                }
                st.dataframe(pd.DataFrame(data_category_data))
                st.info("Using sample data - no database connection available.")
        
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
            if self.database_manager.connection:
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
                    st.warning("No context data available in the database.")
            else:
                # Fallback to sample data
                context_data = {
                    "Context": ["Marketing", "Customer Service", "Human Resources", "Finance", "Legal", "IT Security"],
                    "Description": [
                        "Processing personal data for marketing purposes, such as sending promotional emails or targeted advertising.",
                        "Processing personal data to provide customer service, such as responding to inquiries or resolving complaints.",
                        "Processing personal data for human resources purposes, such as payroll, benefits administration, or performance management.",
                        "Processing personal data for financial purposes, such as billing, accounting, or tax compliance.",
                        "Processing personal data for legal purposes, such as contract enforcement, litigation, or regulatory compliance.",
                        "Processing personal data for IT security purposes, such as access control, threat detection, or incident response."
                    ]
                }
                st.dataframe(pd.DataFrame(context_data))
                st.info("Using sample data - no database connection available.")
        
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
            if self.database_manager.connection:
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
                    st.warning("No sensitivity data available in the database.")
            else:
                # Fallback to sample data
                sensitivity_data = {
                    "Sensitivity Level": ["Public", "Internal", "Confidential", "Restricted", "Special Category"],
                    "Description": [
                        "Information that is publicly available and poses minimal risk if disclosed.",
                        "Information that is intended for internal use within an organization but poses minimal risk if disclosed.",
                        "Information that requires protection and poses moderate risk if disclosed.",
                        "Information that requires strict protection and poses significant risk if disclosed.",
                        "Information that is considered sensitive under data protection laws, such as health data, biometric data, or data revealing racial or ethnic origin."
                    ]
                }
                st.dataframe(pd.DataFrame(sensitivity_data))
                st.info("Using sample data - no database connection available.")

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
            if self.database_manager.connection:
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
                    st.warning("No law jurisdiction data available in the database.")
            else:
                # Fallback to sample data
                law_jurisdiction_data = {
                    "Law": ["GDPR", "GDPR", "CCPA/CPRA", "LGPD", "PIPEDA"],
                    "Jurisdiction": ["European Union", "EEA Countries", "California, USA", "Brazil", "Canada"],
                    "Applicability": [
                        "All EU member states", 
                        "Norway, Iceland, Liechtenstein", 
                        "Businesses serving California residents", 
                        "All of Brazil", 
                        "All of Canada (with some provincial exceptions)"
                    ]
                }
                st.dataframe(pd.DataFrame(law_jurisdiction_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Legal Basis tab
        with tabs[1]:
            st.markdown("""
            <div class="card">
                <h3>Law Legal Basis</h3>
                <p>This section maps data protection laws to their applicable legal bases for processing personal data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get law legal basis data from repository
            if self.database_manager.connection:
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
                    st.warning("No law legal basis data available in the database.")
            else:
                # Fallback to sample data
                law_legal_basis_data = {
                    "Law": ["GDPR", "GDPR", "GDPR", "CCPA", "LGPD", "PIPEDA"],
                    "Legal Basis": ["Consent", "Contract", "Legitimate Interests", "Consent", "Consent", "Consent"],
                    "Description": [
                        "The data subject has given clear consent for processing their personal data for a specific purpose.",
                        "Processing is necessary for the performance of a contract with the data subject.",
                        "Processing is necessary for the purposes of legitimate interests pursued by the controller.",
                        "The consumer has given explicit consent for processing their personal data.",
                        "The data subject has given consent for processing their personal data.",
                        "The individual has given consent for processing their personal data."
                    ]
                }
                st.dataframe(pd.DataFrame(law_legal_basis_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Incident Breach Notification tab
        with tabs[2]:
            st.markdown("""
            <div class="card">
                <h3>Law Incident Breach Notification</h3>
                <p>This section provides information about breach notification requirements across different data protection regulations.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get law incident breach guidance data from repository
            if self.database_manager.connection:
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
                    st.warning("No law incident breach guidance data available in the database.")
            else:
                # Fallback to sample data
                law_breach_data = {
                    "Law": ["GDPR", "CCPA", "LGPD", "PIPEDA"],
                    "Threshold": [
                        "Risk to rights and freedoms",
                        "Unauthorized acquisition of unencrypted data",
                        "Security incidents with risk to data subjects",
                        "Real risk of significant harm"
                    ],
                    "Timeframe": ["72 hours", "Most expedient time", "Reasonable time", "As soon as feasible"],
                    "Authority": ["Supervisory Authority", "Attorney General", "ANPD", "Privacy Commissioner"]
                }
                st.dataframe(pd.DataFrame(law_breach_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Transfer tab
        with tabs[3]:
            st.markdown("""
            <div class="card">
                <h3>Law Transfer Requirements</h3>
                <p>This section provides information about cross-border data transfer requirements across different data protection regulations.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get law transfer data from repository
            if self.database_manager.connection:
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
                    st.warning("No law transfer data available in the database.")
            else:
                # Fallback to sample data
                law_transfer_data = {
                    "Law": ["GDPR", "CCPA", "LGPD", "PIPEDA"],
                    "Adequacy Countries": [
                        "Andorra, Argentina, Canada, Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, UK, Uruguay",
                        "N/A",
                        "Countries with adequate level of protection as determined by ANPD",
                        "Countries with substantially similar legislation"
                    ],
                    "Transfer Mechanisms": [
                        "SCCs, BCRs, Codes of Conduct, Certification",
                        "Service provider contracts",
                        "SCCs, BCRs, Codes of Conduct, Certification, Specific Contractual Clauses",
                        "Contractual or other means"
                    ],
                    "Additional Requirements": [
                        "Transfer Impact Assessment (TIA), Supplementary Measures",
                        "N/A",
                        "Specific authorization from the ANPD may be required",
                        "N/A"
                    ]
                }
                st.dataframe(pd.DataFrame(law_transfer_data))
                st.info("Using sample data - no database connection available.")
        
        # Data Subject Access Request tab
        with tabs[4]:
            st.markdown("""
            <div class="card">
                <h3>Data Subject Access Request Requirements</h3>
                <p>This section provides information about data subject rights and access request requirements across different data protection regulations.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get DSAR data from repository
            if self.database_manager.connection:
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
                    st.warning("No data subject access request requirement data available in the database.")
            else:
                # Fallback to sample data
                dsar_data = {
                    "Law": ["GDPR", "GDPR", "CCPA", "LGPD", "PIPEDA"],
                    "Right": ["Right of Access", "Right to Erasure", "Right to Know", "Right of Access", "Right of Access"],
                    "Description": [
                        "Data subjects have the right to obtain confirmation as to whether personal data concerning them is being processed, and if so, access to that data.",
                        "Data subjects have the right to have personal data erased in certain circumstances.",
                        "Consumers have the right to request that a business disclose what personal information it collects, uses, shares, or sells.",
                        "Data subjects have the right to obtain confirmation of the existence of processing and access to their personal data.",
                        "Individuals have the right to access their personal information held by an organization."
                    ],
                    "Timeframe": [
                        "1 month (can be extended by 2 additional months where necessary)",
                        "1 month (can be extended by 2 additional months where necessary)",
                        "45 days (can be extended by additional 45 days where necessary)",
                        "Immediately (simplified format) or 15 days (complete declaration)",
                        "30 days (can be extended where necessary)"
                    ]
                }
                st.dataframe(pd.DataFrame(dsar_data))
                st.info("Using sample data - no database connection available.")
        
        # Data Category Data Element tab
        with tabs[5]:
            st.markdown("""
            <div class="card">
                <h3>Data Category Data Element Mapping</h3>
                <p>This section maps data categories to their constituent data elements, providing a hierarchical view of data classification.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get data category data element mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        st.warning("No data category to data element mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving data category data element mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Data Category": [
                        "Contact Information", "Contact Information", "Contact Information",
                        "Financial Information", "Financial Information",
                        "Identity Information", "Identity Information"
                    ],
                    "Data Element": [
                        "Email Address", "Phone Number", "Mailing Address",
                        "Credit Card Number", "Bank Account Number",
                        "Government ID", "Full Name"
                    ]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Data Subject Type Data Element Sensitivity tab
        with tabs[6]:
            st.markdown("""
            <div class="card">
                <h3>Law Data Subject Type Data Element Sensitivity</h3>
                <p>This section maps laws to data subject types, data elements, and their sensitivity levels, providing a comprehensive view of data protection requirements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        st.warning("No law data subject type data element sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving law data subject type data element sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Law": ["GDPR", "GDPR", "CCPA", "LGPD"],
                    "Data Subject Type": ["Customer", "Employee", "Consumer", "Data Subject"],
                    "Data Element": ["Government ID", "Health Record", "Credit Card Number", "Biometric Data"],
                    "Sensitivity": ["High", "Special Category", "High", "Special Category"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Data Subject Type Data Category Sensitivity tab
        with tabs[7]:
            st.markdown("""
            <div class="card">
                <h3>Law Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps laws to data subject types, data categories, and their sensitivity levels, providing a higher-level view of data protection requirements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        st.warning("No law data subject type data category sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving law data subject type data category sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Law": ["GDPR", "GDPR", "CCPA", "LGPD"],
                    "Data Subject Type": ["Customer", "Employee", "Consumer", "Data Subject"],
                    "Data Category": ["Identity Information", "Health Information", "Financial Information", "Biometric Information"],
                    "Sensitivity": ["High", "Special Category", "High", "Special Category"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Data Subject Type Data Category Sensitivity tab
        with tabs[8]:
            st.markdown("""
            <div class="card">
                <h3>Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps data subject types to data categories and their sensitivity levels, independent of specific laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        st.warning("No data subject type data category sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving data subject type data category sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Data Subject Type": ["Customer", "Employee", "Patient", "Minor"],
                    "Data Category": ["Contact Information", "Employment Information", "Health Information", "Education Information"],
                    "Sensitivity": ["Medium", "High", "Special Category", "High"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Data Subject Type Data Element Sensitivity tab
        with tabs[9]:
            st.markdown("""
            <div class="card">
                <h3>Data Subject Type Data Element Sensitivity</h3>
                <p>This section maps data subject types to specific data elements and their sensitivity levels, independent of specific laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        
                        st.dataframe(pd.DataFrame(mapping_data))
                    else:
                        st.warning("No data subject type data element sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving data subject type data element sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Data Subject Type": ["Customer", "Employee", "Patient", "Minor"],
                    "Data Element": ["Email Address", "Salary Information", "Medical Record", "School Record"],
                    "Sensitivity": ["Medium", "High", "Special Category", "High"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Law Context Data Subject Type Data Category Sensitivity tab
        with tabs[10]:
            st.markdown("""
            <div class="card">
                <h3>Law Context Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps laws, processing contexts, data subject types, data categories, and their sensitivity levels, providing a comprehensive view of contextual data protection requirements.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        
                        st.dataframe(pd.DataFrame(mapping_data))
                    else:
                        st.warning("No law context data subject type data category sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving law context data subject type data category sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Law": ["GDPR", "GDPR", "CCPA", "LGPD"],
                    "Context": ["Marketing", "HR", "Sales", "Customer Service"],
                    "Data Subject Type": ["Customer", "Employee", "Consumer", "Data Subject"],
                    "Data Category": ["Contact Information", "Employment Information", "Financial Information", "Contact Information"],
                    "Sensitivity": ["Medium", "High", "High", "Medium"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")
        
        # Context Data Subject Type Data Category Sensitivity tab
        with tabs[11]:
            st.markdown("""
            <div class="card">
                <h3>Context Data Subject Type Data Category Sensitivity</h3>
                <p>This section maps processing contexts, data subject types, data categories, and their sensitivity levels, independent of specific laws.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get mappings from repository
            if self.database_manager.connection:
                try:
                    # This method needs to be implemented in the repository
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
                        
                        st.dataframe(pd.DataFrame(mapping_data))
                    else:
                        st.warning("No context data subject type data category sensitivity mappings available in the database.")
                except Exception as e:
                    st.error(f"Error retrieving context data subject type data category sensitivity mappings: {e}")
            else:
                # Fallback to sample data
                mapping_data = {
                    "Context": ["Marketing", "HR", "Sales", "Customer Service"],
                    "Data Subject Type": ["Customer", "Employee", "Consumer", "Customer"],
                    "Data Category": ["Contact Information", "Employment Information", "Financial Information", "Contact Information"],
                    "Sensitivity": ["Medium", "High", "High", "Medium"]
                }
                st.dataframe(pd.DataFrame(mapping_data))
                st.info("Using sample data - no database connection available.")

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
                if self.database_manager.connection:
                    data_categories = self.glossary_repository.get_data_categories()
                    if data_categories:
                        category_options = [dc["name"] for dc in data_categories]
                        st.multiselect("Data Categories", options=category_options)
                    else:
                        st.multiselect("Data Categories", options=["Customer PII", "Marketing Data", "Employee Data", "User Data"])
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
                if self.database_manager.connection:
                    contexts = self.glossary_repository.get_contexts()
                    if contexts:
                        purpose_options = [ctx["name"] for ctx in contexts]
                        st.selectbox("Purpose", options=purpose_options)
                    else:
                        st.selectbox("Purpose", options=["Service Provision", "Marketing", "Employment", "Product Improvement"])
                else:
                    st.selectbox("Purpose", options=["Service Provision", "Marketing", "Employment", "Product Improvement"])
                
                # Get data categories from repository for the multi-select
                if self.database_manager.connection:
                    data_categories = self.glossary_repository.get_data_categories()
                    if data_categories:
                        category_options = [dc["name"] for dc in data_categories]
                        st.multiselect("Data Categories", options=category_options)
                    else:
                        st.multiselect("Data Categories", options=["Identity", "Contact", "Preferences", "HR Data", "Financial", "Usage Data"])
                else:
                    st.multiselect("Data Categories", options=["Identity", "Contact", "Preferences", "HR Data", "Financial", "Usage Data"])
                
                # Get legal bases from repository for the select box
                if self.database_manager.connection:
                    legal_bases = self.glossary_repository.get_legal_bases()
                    if legal_bases:
                        legal_basis_options = [lb["name"] for lb in legal_bases]
                        st.selectbox("Legal Basis", options=legal_basis_options)
                    else:
                        st.selectbox("Legal Basis", options=["Consent", "Contract", "Legal Obligation", "Legitimate Interest"])
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
                if self.database_manager.connection:
                    data_categories = self.glossary_repository.get_data_categories()
                    if data_categories:
                        category_options = [dc["name"] for dc in data_categories]
                        st.multiselect("Data Categories", options=category_options)
                    else:
                        st.multiselect("Data Categories", options=["Customer PII", "Marketing Data", "Employee Data", "User Data"])
                else:
                    st.multiselect("Data Categories", options=["Customer PII", "Marketing Data", "Employee Data", "User Data"])
                
                st.selectbox("Contract Status", options=["Active", "Pending", "Expired", "Under Review"])
                st.selectbox("DPA in Place", options=["Yes", "No", "Pending"])
                st.button("Add Vendor")

    def run(self):
        """Main function to run the Streamlit app."""
        # Configure the page
        self.configure_page()

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
