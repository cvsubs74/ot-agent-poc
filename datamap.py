import os
import time
from core.sensitivity_inference import SensitivityInference
from core.law_inference import LawInference
from core.legal_basis_inference import LegalBasisInference
from UX.page_configurator import PageConfigurator   
from UX.breach_notification_page import BreachNotificationPage
from UX.sensitivity_inference_page import SensitivityInferencePage
from UX.legal_basis_inference_page import LegalBasisInferencePage   
from UX.transfer_mechanism_page import TransferMechanismPage
from UX.risk_inference_page import RiskInferencePage
from UX.core_constructs_pages import (
    LawPage,
    JurisdictionsPage,
    LegalBasisPage,
    DataElementsPage,
    DataSubjectTypesPage,
    ObligationsPage,
    RisksPage,
    FrameworksPage,
    ControlsPage,
    DataCategoriesPage,
    SensitivityPage,
    PurposeCategoriesPage,
    BreachTypesPage,
)

from UX.regulatory_metadata_pages import (
    LawJurisdictionPage,
    LawTransferPage,
    LawLegalBasisPage,
    LawIncidentBreachNotificationPage,
    DataSubjectAccessRequestPage,
    DataCategoryDataElementPage,
    LawDataSubjectTypeDataElementSensitivityPage,
    LawDataSubjectTypeDataCategorySensitivityPage,
    DataSubjectTypeDataCategorySensitivityPage,
    DataSubjectTypeDataElementSensitivityPage,
    LawPurposeCategoryLegalBasisPage,
    LegalBasisRequirementsPage,
    PolicyPurposePage,
    PolicyPurposeDataElementPage,
    PolicyPurposeDataUsagePage,
    SensitivityObligationsPage,
    ObligationPolicyPage,
    ObligationRiskPage,
    FrameworkControlPage,
    PolicyControlPage,
    RiskControlPage
)

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
        
        # Initialize inference classes
        self.sensitivity_inference = SensitivityInference(
            self.regulatory_metadata_repository,
            self.glossary_repository
        )
        
        self.law_inference = LawInference(
            self.regulatory_metadata_repository,
            self.glossary_repository
        )
                
    @staticmethod
    def divider(height=1):
        """Utility function to create a divider with specified height."""
        st.markdown(
            f"<hr style='height:{height}px; margin-top: 0; margin-bottom: 0; border-width:0; background: lightblue;'>",
            unsafe_allow_html=True
        )

    def configure_page(self):
        PageConfigurator.configure_page()

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
            "Data Subject Types", "Data Categories", "Sensitivity", "Purpose Categories", "Breach Types", "Obligations", "Risks",
            "Frameworks", "Controls"
        ])
        with tabs[0]:
            LawPage(self.glossary_repository, self.regulatory_metadata_repository, self.obligation_repository).render()
        with tabs[1]:
            JurisdictionsPage(self.glossary_repository).render()
        with tabs[2]:
            LegalBasisPage(self.glossary_repository).render()
        with tabs[3]:
            DataElementsPage(self.glossary_repository).render()
        with tabs[4]:
            DataSubjectTypesPage(self.glossary_repository).render()
        with tabs[5]:
            DataCategoriesPage(self.glossary_repository).render()
        with tabs[6]:
            SensitivityPage(self.glossary_repository).render()
        with tabs[7]:
            PurposeCategoriesPage(self.glossary_repository).render()
        with tabs[8]:
            BreachTypesPage(self.glossary_repository).render()
        with tabs[9]:
            ObligationsPage(self.obligation_repository).render()
        with tabs[10]:
            RisksPage(self.glossary_repository).render()
        with tabs[11]:
            FrameworksPage(self.glossary_repository).render()
        with tabs[12]:
            ControlsPage(self.glossary_repository).render()

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
            "Obligation Risk",
            "Framework Control",
            "Policy Control",
            "Risk Control"
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
            "Obligation Inference": [5, 6, 7, 8, 9, 15],  # Same tabs as Data Sensitivity Inference + Sensitivity Obligations
            "Policy Inference": [5, 6, 7, 8, 9, 15, 16],  # All tabs from Sensitivity Inference, Obligation Inference + Obligation Policy
            "Risk Inference": [5, 6, 7, 8, 9, 15, 17],  # All tabs from Sensitivity Inference, Obligation Inference + Obligation Risk
            "Control Inference": [18, 19, 20]  # Framework Control, Policy Control, Risk Control tabs
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
                <p>The Policy Inference API uses sensitivity and obligation mappings to recommend organizational policies based on data sensitivity and obligations:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories for classification.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Determines sensitivity levels for data categories.</li>
                    <li><strong>Sensitivity Obligations</strong>: Maps sensitivity levels to security and privacy obligations.</li>
                    <li><strong>Obligation Policy</strong>: Maps security and privacy obligations to organizational policies that should be implemented.</li>
                </ul>
                <p>The Policy Inference process follows these steps:</p>
                <ol>
                    <li>First, determine the sensitivity level of the data using the Data Sensitivity Inference algorithm</li>
                    <li>Identify applicable security and privacy obligations based on the sensitivity level</li>
                    <li>Map these obligations to relevant organizational policies using the Obligation Policy mapping</li>
                    <li>Calculate a relevance score for each policy based on how many obligations it addresses</li>
                    <li>Present a prioritized list of recommended policies to implement</li>
                </ol>
                <p>This approach helps organizations implement a comprehensive policy framework that addresses their specific data protection requirements and ensures compliance with relevant regulations.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Obligation Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Obligation Inference Works</h4>
                <p>The Obligation Inference API uses sensitivity mapping tables to determine what security and privacy controls should be implemented based on data sensitivity:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories for hierarchical classification.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Determines sensitivity levels for data categories.</li>
                    <li><strong>Sensitivity Obligations</strong>: Maps sensitivity levels to specific security and privacy obligations.</li>
                </ul>
                <p>The Obligation Inference process follows these steps:</p>
                <ol>
                    <li>First, determine the sensitivity level of the data using the Data Sensitivity Inference algorithm</li>
                    <li>Based on the inferred sensitivity, identify all applicable security and privacy obligations</li>
                    <li>Group obligations by control type (e.g., Technical, Administrative, Physical)</li>
                    <li>Prioritize obligations based on their importance (High, Medium, Low)</li>
                </ol>
                <p>This approach ensures organizations implement appropriate safeguards proportional to the sensitivity of the data they process, helping maintain compliance with privacy regulations and security best practices.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Risk Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Risk Inference Works</h4>
                <p>The Risk Inference API uses sensitivity and obligation mappings to identify potential risks if security and privacy obligations are not implemented:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories for classification.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Determines sensitivity levels for data categories.</li>
                    <li><strong>Sensitivity Obligations</strong>: Maps sensitivity levels to security and privacy obligations.</li>
                    <li><strong>Obligation Risk</strong>: Maps security and privacy obligations to potential risks if not implemented.</li>
                </ul>
                <p>The Risk Inference process follows these steps:</p>
                <ol>
                    <li>First, determine the sensitivity level of the data using the Data Sensitivity Inference algorithm</li>
                    <li>Identify applicable security and privacy obligations based on the sensitivity level</li>
                    <li>Map these obligations to potential risks using the Obligation Risk mapping</li>
                    <li>Evaluate the likelihood and impact of each risk</li>
                    <li>Calculate an overall risk rating (Critical, High, Medium, Low)</li>
                </ol>
                <p>This risk-based approach helps organizations prioritize their compliance efforts based on the potential consequences of non-compliance, focusing resources on mitigating the most significant risks first.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_inference_api == "Control Inference":
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Control Inference Works</h4>
                <p>The Control Inference API suggests appropriate security and privacy controls based on frameworks, policies, or risks:</p>
                <ul>
                    <li><strong>Framework Control</strong>: Maps security and compliance frameworks to specific controls that help implement the framework requirements.</li>
                    <li><strong>Policy Control</strong>: Maps organizational policies to specific controls that help enforce those policies.</li>
                    <li><strong>Risk Control</strong>: Maps identified risks to specific controls that help mitigate those risks.</li>
                </ul>
                <p>The Control Inference process follows these steps:</p>
                <ol>
                    <li>Identify the input context (framework, policy, or risk) that requires control recommendations</li>
                    <li>Query the appropriate mapping table (Framework Control, Policy Control, or Risk Control)</li>
                    <li>Retrieve controls with their relevance scores or mitigation levels</li>
                    <li>Rank controls based on their effectiveness for the given context</li>
                    <li>Present a prioritized list of recommended controls</li>
                </ol>
                <p>This approach ensures that organizations implement the most effective controls for their specific compliance requirements and risk profile, optimizing their security and privacy investments.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a mapping from filtered tab index to original tab index
        tab_index_mapping = {i: visible_tab_indices[i] for i in range(len(visible_tab_indices))}
        
        # Loop through visible tabs and render content based on the original tab index
        for i, tab_idx in enumerate(visible_tab_indices):
            with tabs[i]:
                # Law Jurisdiction tab
                if tab_idx == 0:
                    LawJurisdictionPage(self.regulatory_metadata_repository).render()
        
                # Law Legal Basis tab
                elif tab_idx == 1:
                    LawLegalBasisPage(self.regulatory_metadata_repository).render()
        
                # Law Incident Breach Notification tab
                elif tab_idx == 2:
                    LawIncidentBreachNotificationPage(self.regulatory_metadata_repository).render()
        
                # Law Transfer tab
                elif tab_idx == 3:
                    LawTransferPage(self.regulatory_metadata_repository).render()

                elif tab_idx == 4:                        
                    DataSubjectAccessRequestPage(self.regulatory_metadata_repository).render()
        
                # Data Category Data Element tab
                elif tab_idx == 5:
                    DataCategoryDataElementPage(self.regulatory_metadata_repository).render()
        
                # Law Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 6:
                    LawDataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()
        
                # Law Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 7:                        
                    LawDataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()
        
                # Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 8:
                    DataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()
        
                # Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 9:
                    DataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()
            
                # Law Purpose Category Legal Basis tab
                elif tab_idx == 10:
                    LawPurposeCategoryLegalBasisPage(self.regulatory_metadata_repository).render()
                
                # Legal Basis Requirements tab
                elif tab_idx == 11:
                    LegalBasisRequirementsPage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose tab
                elif tab_idx == 12:
                    PolicyPurposePage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose Data Element tab
                elif tab_idx == 13:
                    PolicyPurposeDataElementPage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose Data Usage tab
                elif tab_idx == 14:
                    PolicyPurposeDataUsagePage(self.regulatory_metadata_repository).render()
                 
                # Sensitivity Obligations tab
                elif tab_idx == 15:
                    SensitivityObligationsPage(self.glossary_repository, self.obligation_repository).render()
                
                # Obligation Policy tab
                elif tab_idx == 16:
                    ObligationPolicyPage(self.glossary_repository, self.obligation_repository).render()
                
                # Obligation Risk tab
                elif tab_idx == 17:
                    ObligationRiskPage(self.glossary_repository, self.obligation_repository).render()
                
                # Framework Control tab
                elif tab_idx == 18:
                    FrameworkControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()
                
                # Policy Control tab
                elif tab_idx == 19:
                    PolicyControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()
                
                # Risk Control tab
                elif tab_idx == 20:
                    RiskControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()
                    
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
        
        tabs = st.tabs(["Policies", "Policy Purpose", "Policy Purpose Data Element", "Policy Purpose Data Usage", "Policy Purpose Data Retention", "Policy Purpose Data Security"])
        
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
        
        # Policy Purpose Data Retention tab
        with tabs[4]:
            # Get policy purpose data retentions from repository
            policy_purpose_data_retentions = self.regulatory_metadata_repository.get_policy_purpose_data_retentions()
            
            if policy_purpose_data_retentions:
                # Create a DataFrame for display
                ppdr_data = {
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Retention Period": [],
                    "Retention Trigger": [],
                    "Retention Basis": [],
                    "Exceptions": []
                }
                
                for rule in policy_purpose_data_retentions:
                    ppdr_data["Policy"].append(rule["policy_name"])
                    ppdr_data["Purpose"].append(rule["purpose_name"])
                    ppdr_data["Data Element"].append(rule["data_element_name"])
                    ppdr_data["Retention Period"].append(rule["retention_period"])
                    ppdr_data["Retention Trigger"].append(rule["retention_trigger"])
                    ppdr_data["Retention Basis"].append(rule["retention_basis"] if rule["retention_basis"] else "Not specified")
                    ppdr_data["Exceptions"].append(rule["exceptions"] if rule["exceptions"] else "None")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppdr_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppdr_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppdr_purpose")
                
                # Second row of filters
                col3, col4 = st.columns(2)
                
                with col3:
                    # Get unique retention triggers
                    triggers = sorted(list(set(df["Retention Trigger"].tolist())))
                    selected_trigger = st.selectbox("Filter by Retention Trigger", ["All"] + triggers, key="ppdr_trigger")
                
                with col4:
                    # Get unique retention periods
                    periods = sorted(list(set(df["Retention Period"].tolist())))
                    selected_period = st.selectbox("Filter by Retention Period", ["All"] + periods, key="ppdr_period")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppdr_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_trigger != "All":
                    filtered_df = filtered_df[filtered_df["Retention Trigger"] == selected_trigger]
                
                if selected_period != "All":
                    filtered_df = filtered_df[filtered_df["Retention Period"] == selected_period]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data retention rules match the selected filters.")
            else:
                st.warning("No policy-purpose-data retention rules available in the database.")
    
        # Policy Purpose Data Security tab
        with tabs[5]:
            st.markdown("### Policy Purpose Data Security")
            security_rules = self.regulatory_metadata_repository.get_policy_purpose_data_security()
            if security_rules:
                df = pd.DataFrame(security_rules)
                # Add filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    policies = sorted(df["policy_name"].unique())
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppds_policy")
                with col2:
                    purposes = sorted(df["purpose_name"].unique())
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppds_purpose")
                with col3:
                    elements = sorted(df["data_element_name"].unique())
                    selected_element = st.selectbox("Filter by Data Element", ["All"] + elements, key="ppds_element")

                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["policy_name"] == selected_policy]
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["purpose_name"] == selected_purpose]
                if selected_element != "All":
                    filtered_df = filtered_df[filtered_df["data_element_name"] == selected_element]

                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.warning("No policy purpose data security rules available.")

        # Add a section for defining new policies on purposes
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Define New Policy on Purpose")
        st.markdown("Create a new policy that defines rules for data access and usage based on specific purposes.")
        
        # Get existing policy-purpose relationships
        existing_policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
        existing_purpose_ids = set()
        if existing_policy_purposes:
            for pp in existing_policy_purposes:
                existing_purpose_ids.add(pp["purpose_id"])
        
        # Get all purposes for selection
        purposes = self.glossary_repository.get_purposes()
        
        # Filter out purposes that already have policies defined
        available_purposes = [p for p in purposes if p["id"] not in existing_purpose_ids] if purposes else []
        purpose_options = {p["id"]: p["name"] for p in available_purposes}
        
        # Get all data elements for selection
        data_elements = self.glossary_repository.get_data_elements()
        data_element_options = {de["id"]: de["name"] for de in data_elements} if data_elements else {}
        
        # Get data categories for selection
        data_categories = self.glossary_repository.get_data_categories()
        data_category_options = {dc["id"]: dc["name"] for dc in data_categories} if data_categories else {}
        
        # Selection mode (outside the form)
        st.markdown("Select how you want to define the policy:")
        selection_mode = st.radio(
            "Selection Mode", 
            ["By Data Category", "By Individual Data Elements"]
        )
        
        # Create a form for defining a new policy on a purpose
        with st.form(key="define_policy_form"):
            # Purpose selection (first step)
            if purpose_options:
                selected_purpose_id = st.selectbox(
                    "Select Purpose", 
                    options=list(purpose_options.keys()),
                    format_func=lambda x: purpose_options[x]
                )
                if selected_purpose_id:
                    purpose_name = purpose_options[selected_purpose_id]
            else:
                st.warning("No available purposes found in the database. All purposes already have policies defined.")
                selected_purpose_id = None
                
            # Get policies of the selected type from the RegulatoryMetadataRepository
            filtered_policies = self.glossary_repository.get_policies()
            
            # Create a dictionary of filtered policies for the selectbox
            filtered_policy_options = {p["id"]: p["name"] for p in filtered_policies}
            
            # Select an existing policy
            if filtered_policy_options:
                selected_policy_id = st.selectbox(
                    "Select Policy", 
                    options=list(filtered_policy_options.keys()),
                    format_func=lambda x: filtered_policy_options[x]
                )
                
            # Data selection based on the selection mode
            selected_data_element_ids = []
            
            if selection_mode == "By Data Category":
                # Data category selection
                if data_category_options:
                    selected_category_ids = st.multiselect(
                        "Select Data Categories",
                        options=list(data_category_options.keys()),
                        format_func=lambda x: data_category_options[x]
                    )
                    
                    # Get all data elements in the selected categories
                    if selected_category_ids:
                        # Map to show which category each element belongs to
                        element_category_map = {}
                        
                        # For each selected category, get its data elements
                        for category_id in selected_category_ids:
                            category_elements = self.regulatory_metadata_repository.get_data_category_data_elements(category_id=category_id)
                            if category_elements:
                                for element in category_elements:
                                    element_id = element["data_element_id"]
                                    if element_id not in selected_data_element_ids:  # Avoid duplicates
                                        selected_data_element_ids.append(element_id)
                                    element_category_map[element_id] = data_category_options[category_id]
                        
                        # Show the count of data elements in each category
                        if element_category_map:
                            st.info(f"Selected {len(selected_data_element_ids)} data elements from {len(selected_category_ids)} categories")
                            
                            # Show a sample of the selected data elements
                            with st.expander("View Selected Data Elements"):
                                for category_id in selected_category_ids:
                                    category_name = data_category_options[category_id]
                                    category_elements = [de_id for de_id, cat in element_category_map.items() if cat == category_name]
                                    if category_elements:
                                        st.markdown(f"**{category_name}:** {len(category_elements)} elements")
                else:
                    st.warning("No data categories found in the database.")
            else:  # By Individual Data Elements
                # Show all data elements in a multiselect
                if data_elements:
                    # Create a multiselect for all data elements
                    selected_data_element_ids = st.multiselect(
                        "Select Data Elements",
                        options=list(data_element_options.keys()),
                        format_func=lambda x: data_element_options[x]
                    )
                    
                    # Show count of selected elements
                    if selected_data_element_ids:
                        st.info(f"Selected {len(selected_data_element_ids)} data elements")
                else:
                    st.warning("No data elements found in the database.")
                    selected_data_element_ids = []
            
            # Create a multiselect for operations
            operations = ["read", "write", "share"]
            selected_operations = st.multiselect(
                    "Select allowed operations",
                    options=operations,
                    default=operations,  # Default to all operations selected
                    format_func=lambda x: x.capitalize()
                )
                
            # Optional restrictions for selected operations
            operation_restrictions = {}
            if selected_operations:
                with st.expander("Add restrictions for operations (optional)"):
                    for operation in selected_operations:
                        operation_restrictions[operation] = st.text_input(
                            f"Restrictions for {operation.capitalize()}",
                            placeholder=f"Enter any restrictions for {operation} operation",
                            key=f"rest_{operation}"
                        )
            
            # Create a dictionary to store permissions
            permissions = {}
                
            # Set the same permissions for all selected data elements
            for data_element_id in selected_data_element_ids:
                permissions[data_element_id] = {}
                
                # Set permissions based on selected operations
                for operation in operations:
                    permissions[data_element_id][operation] = operation in selected_operations
                    if operation in selected_operations and operation_restrictions.get(operation):
                        permissions[data_element_id][f"{operation}_restrictions"] = operation_restrictions[operation]
                    else:
                        permissions[data_element_id][f"{operation}_restrictions"] = None
            
            # Show a summary of the selected operations
            if selected_operations:
                st.info(f"Selected operations: {', '.join(op.capitalize() for op in selected_operations)}")
            else:
                st.warning("No operations selected. All operations will be denied.")
        
            # Submit button
            submit_button = st.form_submit_button("Create Policy Definition")
        
        if submit_button:
            # Validate inputs
            if not selected_purpose_id:
                st.error("Please select a purpose.")
                return
            
            if not selected_data_element_ids:
                st.error("Please select at least one data element.")
                return
            
            if not selected_policy_id:
                st.error("Please select an existing policy.")
                return
            
            # Create policy-purpose relationship
            success = self.regulatory_metadata_repository.add_policy_purpose(
                policy_id=selected_policy_id,
                purpose_id=selected_purpose_id
            )
            
            if not success:
                st.error("Failed to create the policy-purpose relationship. Please try again.")
                return
            
            # Create policy-purpose-data element relationships and usage rules
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            total_operations = len(selected_data_element_ids) * (1 + (3 if selected_policy_id else 0))
            completed_operations = 0
            
            all_success = True
            for data_element_id in selected_data_element_ids:
                data_element_name = data_element_options[data_element_id]
                progress_text.text(f"Processing: {data_element_name}")
                
                # Add policy-purpose-data element relationship
                success = self.regulatory_metadata_repository.add_policy_purpose_data_element(
                    policy_id=selected_policy_id,
                    purpose_id=selected_purpose_id,
                    data_element_id=data_element_id,
                    access_allowed=True  # Default to allowed, operations will be controlled by usage rules
                )
                
                completed_operations += 1
                progress_bar.progress(completed_operations / total_operations)
                        
                if not success:
                    all_success = False
                    continue
                
                # Add operation permissions based on selected operations
                for operation in ["read", "write", "share"]:
                    progress_text.text(f"Processing: {data_element_name} - {operation}")
                    
                    # Add policy-purpose-data-element-usage relationship
                    # The operation is allowed only if it was selected in the multiselect
                    is_allowed = operation in selected_operations
                    restrictions = operation_restrictions.get(operation) if is_allowed else None
                    
                    success = self.regulatory_metadata_repository.add_policy_purpose_data_usage(
                        policy_id=selected_policy_id,
                        purpose_id=selected_purpose_id,
                        data_element_id=data_element_id,
                        operation=operation,
                        allowed=is_allowed,
                        restrictions=restrictions
                    )
                    
                    if not success:
                        all_success = False
                    
                    completed_operations += 1
                    progress_bar.progress(completed_operations / total_operations)
            
            progress_text.empty()
            progress_bar.empty()
            
            if all_success:
                st.success("Successfully created policy for purpose: {}".format(purpose_name))
            else:
                st.error("Failed to create policy for purpose: {}".format(purpose_name))

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
        
        analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")

        st.write("")
        # Show results (decision tree, etc.) below the input parameters
        if analyze_button and selected_purpose and selected_data_elements and selected_operation:
            self._analyze_policy_compliance(selected_purpose, selected_data_elements, selected_operation)
        elif analyze_button:
            st.warning("Please select a purpose, at least one data element, and an operation to analyze compliance.")

    def run(self):
        """Main function to run the Streamlit app."""
        self.configure_page()

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
            
            # Obligation Inference menu item
            if st.button("🔒 Obligation Inference", key="obligation_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Obligation API'
            
            # Policy Inference menu item
            if st.button("📋 Policy Inference", key="policy_inference_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Policy Inference API'
            
            # Risk Inference menu item
            if st.button("⚠️ Risk Inference", key="risk_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Risk API'

            # Control Inference menu item
            if st.button("⚠️ Control Inference", key="control_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Control API'                
            
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
            self.law_inference_page()
        elif st.session_state['current_section'] == 'Sensitivity API':
            self.sensitivity_inference_page()
        elif st.session_state['current_section'] == 'Legal Basis API':
            self.legal_basis_inference_page()
        elif st.session_state['current_section'] == 'Breach API':
            self.breach_notification_page()
        elif st.session_state['current_section'] == 'Transfer API':
            self.transfer_mechanism_page()
        elif st.session_state['current_section'] == 'DSR API':
            self.data_subject_rights_page()
        elif st.session_state['current_section'] == 'Obligation API':
            self.obligation_inference_page()
        elif st.session_state['current_section'] == 'Policy Inference API':
            self.policy_recommendation_api()
        elif st.session_state['current_section'] == 'Risk API':
            self.risk_inference_page()
        elif st.session_state['current_section'] == 'Purposes':
            self.purposes_page()
        elif st.session_state['current_section'] == 'Policies':
            self.policies_page()
        elif st.session_state['current_section'] == 'Policy Compliance':
            self.policy_compliance_page()
        elif st.session_state['current_section'] == 'Control API':
            self.control_inference_page()            

    def control_inference_page(self):
        """Display the Control Inference page to recommend controls based on frameworks, policies, or risks."""
        st.header("Control Inference API")
        st.markdown("Recommend appropriate controls based on frameworks, policies, or risks.")
        
        # Create tabs for different inference sources
        source_tabs = st.tabs(["Policy-Based", "Risk-Based", "Framework-Based"])
        
        # Policy-Based Control Inference
        with source_tabs[0]:
            # Get all policies from the repository
            policies = self.glossary_repository.get_policies()
            if not policies:
                st.warning("No policies available in the database.")
                return
            
            selected_policy_id = st.selectbox(
                "Select Policy",
                options=[p["id"] for p in policies],
                format_func=lambda x: next((p["name"] for p in policies if p["id"] == x), "Unknown"),
                key="policy_control_inference"
            )
            
            analyze_button = st.button("Recommend Controls", key="policy_controls_button")
            
            if analyze_button and selected_policy_id:
                # Get the policy name for display
                policy_name = next((p["name"] for p in policies if p["id"] == selected_policy_id), "Unknown")
                
                # Get policy controls from the repository
                policy_controls_list = self.regulatory_metadata_repository.get_policy_controls(policy_id=selected_policy_id)
                
                # Convert to a dictionary format for easier access
                policy_controls = {}
                if policy_controls_list:
                    policy_controls[selected_policy_id] = policy_controls_list
                
                if selected_policy_id in policy_controls:
                    controls = policy_controls[selected_policy_id]
                    
                    # Group by control type for better organization
                    control_types = set(c["control_type"] for c in controls)
                    
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        
                        # Sort by relevance score
                        type_controls.sort(key=lambda x: x["relevance_score"], reverse=True)
                        
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Relevance: {control['relevance_score']:.1f})", expanded=True):
                                # Use control_type and implementation_status instead of description
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                
                                # Add a button to implement this control
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_policy_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {policy_name}.")
        
        # Risk-Based Control Inference
        with source_tabs[1]:
            # Get all risks from the repository
            risks = self.glossary_repository.get_risks()
            if not risks:
                st.warning("No risks available in the database.")
                return
            
            selected_risk_id = st.selectbox(
                "Select Risk",
                options=[r["id"] for r in risks],
                format_func=lambda x: next((r["name"] for r in risks if r["id"] == x), "Unknown"),
                key="risk_control_inference"
            )
            
            analyze_button = st.button("Recommend Controls", key="risk_controls_button")
                
            if analyze_button and selected_risk_id:
                # Get the risk name for display
                risk_name = next((r["name"] for r in risks if r["id"] == selected_risk_id), "Unknown")
                
                # Get risk controls from the repository
                risk_controls_list = self.regulatory_metadata_repository.get_risk_controls(risk_id=selected_risk_id)
                
                # Convert to a dictionary format for easier access
                risk_controls = {}
                if risk_controls_list:
                    risk_controls[selected_risk_id] = risk_controls_list
                
                if selected_risk_id in risk_controls:
                    controls = risk_controls[selected_risk_id]
                    
                    # Group by control type for better organization
                    control_types = set(c["control_type"] for c in controls)
                    
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        
                        # Sort by mitigation level
                        mitigation_order = {"High": 0, "Medium": 1, "Low": 2}
                        type_controls.sort(key=lambda x: mitigation_order.get(x["mitigation_level"], 99))
                        
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Mitigation: {control['mitigation_level']})", expanded=True):
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                
                                # Add a button to implement this control
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_risk_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {risk_name}.")
        
        # Framework-Based Control Inference
        with source_tabs[2]:
            # Get all frameworks from the repository
            frameworks = self.glossary_repository.get_frameworks()
            if not frameworks:
                st.warning("No frameworks available in the database.")
                return
            
            st.subheader("Input Parameters")
            selected_framework_id = st.selectbox(
                "Select Framework",
                options=[f["id"] for f in frameworks],
                format_func=lambda x: next((f["name"] for f in frameworks if f["id"] == x), "Unknown"),
                key="framework_control_inference"
            )
            
            analyze_button = st.button("Recommend Controls", key="framework_controls_button")
            
            if analyze_button and selected_framework_id:
                # Get the framework name for display
                framework_name = next((f["name"] for f in frameworks if f["id"] == selected_framework_id), "Unknown")
                
                # Get framework controls from the repository
                framework_controls_list = self.regulatory_metadata_repository.get_framework_controls(framework_id=selected_framework_id)
                
                # Convert to a dictionary format for easier access
                framework_controls = {}
                if framework_controls_list:
                    framework_controls[selected_framework_id] = framework_controls_list
                
                if selected_framework_id in framework_controls:
                    controls = framework_controls[selected_framework_id]
                    
                    # Group by control type for better organization
                    control_types = set(c["control_type"] for c in controls)
                    
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        
                        # Sort by relevance score
                        type_controls.sort(key=lambda x: x["relevance_score"], reverse=True)
                        
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Relevance: {control['relevance_score']:.1f})", expanded=True):
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                
                                # Add a button to implement this control
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_framework_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {framework_name}.")
        
    def decision_tree_section(self):
        """Visualize the regulatory ontology and association rules as a decision tree using PyVis."""
        from UX.ontology_graph_page import OntologyGraphPage
        OntologyGraphPage().render()

    def sensitivity_inference_page(self):
        """Render the Sensitivity Inference page using the new SensitivityInferencePage class."""
        SensitivityInferencePage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        ).render()

    def legal_basis_inference_page(self):
        """Render the Legal Basis Inference page using the new LegalBasisInferencePage class."""
        LegalBasisInferencePage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        ).render()
    
    def transfer_mechanism_page(self):
        """Render the Transfer Mechanism Inference page using the new TransferMechanismPage class."""
        TransferMechanismPage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        ).render()
    
    def breach_notification_page(self):
        """Implement an incident breach notification API based on regulatory metadata.
        This helps users determine notification requirements for data breaches.
        """
        BreachNotificationPage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        ).render()
    
    def data_subject_rights_page(self):
        """Render the Data Subject Rights Inference page using the new DataSubjectRightsPage class."""
        from UX.data_subject_rights_page import DataSubjectRightsPage
        DataSubjectRightsPage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        ).render()
                
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

                # Render the decision tree
                self._render_decision_tree(nodes, edges, title="Policy Decision Tree")
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
        """Analyze policy compliance for Access Control, Data Security, and Data Retention policies."""
        import pandas as pd
        st = __import__('streamlit')
        # Get all policies
        policies = self.glossary_repository.get_policies()
        access_control_policy = None
        data_security_policy = None
        data_retention_policy = None
        for policy in policies:
            if policy["policy_type"] == "Access Control":
                access_control_policy = policy
            elif policy["policy_type"] == "Security":
                data_security_policy = policy
            elif policy["policy_type"] == "Retention":
                data_retention_policy = policy

        # Get purpose ID
        purposes = self.glossary_repository.get_purposes()
        purpose_id = None
        for p in purposes:
            if p["name"] == purpose:
                purpose_id = p["id"]
                break
        if not purpose_id:
            st.error(f"Purpose '{purpose}' not found in the database.")
            return

        # Get data element IDs
        all_data_elements = self.glossary_repository.get_data_elements()
        data_element_ids = {de["name"]: de["id"] for de in all_data_elements}

        denied_operations = False

        # --- Access Control Policy Compliance ---
        access_decisions = {"Data Element": [], "Operation": [], "Decision": [], "Restrictions": []}
        if access_control_policy:
            policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
                policy_id=access_control_policy['id'], purpose_id=purpose_id)
            policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                policy_id=access_control_policy['id'], purpose_id=purpose_id)
            for data_element in data_elements:
                decision = "Denied"
                restrictions = "No explicit permission in policy"
                for usage in policy_purpose_data_usages:
                    if usage["data_element_name"] == data_element and usage["operation"] == operation:
                        if usage["allowed"]:
                            if usage["restrictions"]:
                                decision = "Allowed with Restrictions"
                                restrictions = usage["restrictions"]
                            else:
                                decision = "Allowed"
                                restrictions = "None"
                        else:
                            decision = "Denied"
                            restrictions = usage["restrictions"] or "Operation not allowed for this purpose"
                            denied_operations = True
                        break
                if decision == "Denied" and restrictions == "No explicit permission in policy":
                    for element in policy_purpose_data_elements:
                        if element["data_element_name"] == data_element:
                            if element.get("access_allowed") and operation == "read":
                                decision = "Allowed"
                                restrictions = "None"
                            else:
                                denied_operations = True
                            break
                access_decisions["Data Element"].append(data_element)
                access_decisions["Operation"].append(operation)
                access_decisions["Decision"].append(decision)
                access_decisions["Restrictions"].append(restrictions)
            st.markdown("<h5>Access Control Policies</h5>", unsafe_allow_html=True)
            access_df = pd.DataFrame(access_decisions)
            def highlight_decision(val):
                if val == "Allowed":
                    return 'background-color: #d4edda; color: #155724'
                elif val == "Denied":
                    return 'background-color: #f8d7da; color: #721c24'
                elif val == "Allowed with Restrictions":
                    return 'background-color: #fff3cd; color: #856404'
                return ''
            st.dataframe(access_df.style.applymap(highlight_decision, subset=["Decision"]))
        else:
            st.warning("No Access Control Policy found in the database.")

        # --- Data Security Policy Compliance ---
        security_decisions = {"Data Element": [], "Encryption Required": [], "Encryption Algorithm": [], "Masking Required": [], "Masking Format": [], "Access Logging": []}
        if data_security_policy:
            policy_purpose_data_security = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                policy_id=data_security_policy['id'], purpose_id=purpose_id)
            
            # Get all data elements with their default masking formats
            all_data_elements = self.glossary_repository.get_data_elements()
            data_element_defaults = {de["name"]: de.get("default_masking_format") for de in all_data_elements}
            
            for data_element in data_elements:
                sec = next((s for s in policy_purpose_data_security if s["data_element_name"] == data_element), None)
                security_decisions["Data Element"].append(data_element)
                
                if sec:
                    security_decisions["Encryption Required"].append("Yes" if sec["encryption_required"] else "No")
                    security_decisions["Encryption Algorithm"].append(sec["encryption_algorithm"] or "-")
                    security_decisions["Masking Required"].append("Yes" if sec["masking_required"] else "No")
                    
                    # Use policy masking format if specified, otherwise use data element default
                    masking_format = sec["masking_format"] or data_element_defaults.get(data_element)
                    security_decisions["Masking Format"].append(masking_format or "-")
                    
                    security_decisions["Access Logging"].append("Yes" if sec["access_logging"] else "No")
                else:
                    security_decisions["Encryption Required"].append("-")
                    security_decisions["Encryption Algorithm"].append("-")
                    security_decisions["Masking Required"].append("-")
                    
                    # Use data element default masking format if no policy rule exists
                    default_format = data_element_defaults.get(data_element)
                    security_decisions["Masking Format"].append(default_format or "-")
                    
                    security_decisions["Access Logging"].append("-")
            st.markdown("<h5>Data Security Policies</h5>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(security_decisions))
        else:
            st.warning("No Data Security Policy found in the database.")

        # --- Data Retention Policy Compliance ---
        retention_decisions = {"Data Element": [], "Retention Period": [], "Retention Trigger": [], "Retention Basis": [], "Exceptions": []}
        if data_retention_policy:
            policy_purpose_data_retentions = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                policy_id=data_retention_policy['id'], purpose_id=purpose_id)
            for data_element in data_elements:
                ret = next((r for r in policy_purpose_data_retentions if r["data_element_name"] == data_element), None)
                retention_decisions["Data Element"].append(data_element)
                if ret:
                    retention_decisions["Retention Period"].append(ret["retention_period"] or "-")
                    retention_decisions["Retention Trigger"].append(ret["retention_trigger"] or "-")
                    retention_decisions["Retention Basis"].append(ret["retention_basis"] or "-")
                    retention_decisions["Exceptions"].append(ret["exceptions"] or "-")
                else:
                    retention_decisions["Retention Period"].append("-")
                    retention_decisions["Retention Trigger"].append("-")
                    retention_decisions["Retention Basis"].append("-")
                    retention_decisions["Exceptions"].append("-")
            st.markdown("<h5>Data Retention Policies</h5>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(retention_decisions))
        else:
            st.warning("No Data Retention Policy found in the database.")

        # --- Decision Rationale and Recommendations ---
        st.markdown("""
        <div style="margin-top: 20px;">
            <h4 style="color: #3498db;">Decision Rationale</h4>
            <p>The policy compliance decision is based on:</p>
            <ul>
                <li>Purpose limitation principles defined in the Access Control Policy</li>
                <li>Data security requirements for each data element</li>
                <li>Retention rules for each data element</li>
                <li>Operation type and associated risks</li>
                <li>Purpose-specific data access rules</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
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
        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Decision Tree Visualization ---
        # Build nodes and edges representing the compliance decision path
        nodes = []
        edges = []
        # Root node: Purpose
        purpose_node_id = f"purpose_{purpose_id}"
        nodes.append({
            "id": purpose_node_id,
            "label": f"Purpose: {purpose}",
            "color": "#3498db",
            "shape": "ellipse",
            "size": 30
        })
        # Data Elements
        data_element_ids_list = []
        for data_element in data_elements:
            de_id = f"de_{data_element_ids.get(data_element, data_element)}"
            data_element_ids_list.append(de_id)
            nodes.append({
                "id": de_id,
                "label": f"Data Element: {data_element}",
                "color": "#f39c12",
                "shape": "box",
                "size": 25
            })
            edges.append({
                "source": purpose_node_id,
                "target": de_id,
                "label": "includes"
            })

        # Only for Access Control: add operation node and connect to data elements
        if access_control_policy and operation in ["read", "write", "share"]:
            op_node_id = f"operation_{operation}"
            nodes.append({
                "id": op_node_id,
                "label": f"Operation: {operation}",
                "color": "#2ecc71",
                "shape": "box",
                "size": 25
            })
            for de_id in data_element_ids_list:
                edges.append({
                    "source": de_id,
                    "target": op_node_id,
                    "label": "operation"
                })
            # Access Control Node (only for operation)
            access_node_id = f"access_{purpose_id}_{operation}"
            access_actions = []
            for i, data_element in enumerate(data_elements):
                if i < len(access_decisions["Decision"]):
                    access_actions.append(f"{data_element}: {access_decisions['Decision'][i]} ({access_decisions['Restrictions'][i]})")
            access_label = "Access Control Actions:\n" + "\n".join(access_actions)
            nodes.append({
                "id": access_node_id,
                "label": access_label,
                "color": "#9b59b6",
                "shape": "box",
                "size": 25,
                "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
            })
            edges.append({
                "source": op_node_id,
                "target": access_node_id,
                "label": "Access Control"
            })

        # Data Security nodes (connect directly to data elements)
        security_node_id = f"security_{purpose_id}_{operation}"
        security_actions = []
        for i, data_element in enumerate(data_elements):
            if i < len(security_decisions["Encryption Required"]):
                sec = security_decisions["Encryption Required"][i]
                if sec == "No":
                    security_actions.append(f"Implement encryption for '{data_element}' as required by policy.")
            if i < len(security_decisions["Masking Required"]) and security_decisions["Masking Required"][i] == "Yes":
                security_actions.append(f"Apply data masking to '{data_element}' ({security_decisions['Masking Format'][i]})")
            if i < len(security_decisions["Access Logging"]) and security_decisions["Access Logging"][i] == "No":
                security_actions.append(f"Enable access logging for '{data_element}'.")
        if not security_actions:
            security_actions.append("All security controls are in place.")
        security_label = "Data Security Actions:\n" + "\n".join(security_actions)
        nodes.append({
            "id": security_node_id,
            "label": security_label,
            "color": "#16a085",
            "shape": "box",
            "size": 25,
            "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
        })
        for de_id in data_element_ids_list:
            edges.append({
                "source": de_id,
                "target": security_node_id,
                "label": "Data Security"
            })

        # Data Retention nodes (connect directly to data elements)
        retention_node_id = f"retention_{purpose_id}_{operation}"
        retention_actions = []
        for i, data_element in enumerate(data_elements):
            if i < len(retention_decisions["Retention Period"]):
                ret = retention_decisions["Retention Period"][i]
                if ret == "-":
                    retention_actions.append(f"Define retention period for '{data_element}'.")
        if not retention_actions:
            retention_actions.append("All retention periods are defined as required.")
        retention_label = "Data Retention Actions:\n" + "\n".join(retention_actions)
        nodes.append({
            "id": retention_node_id,
            "label": retention_label,
            "color": "#e67e22",
            "shape": "box",
            "size": 25,
            "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
        })
        for de_id in data_element_ids_list:
            edges.append({
                "source": de_id,
                "target": retention_node_id,
                "label": "Data Retention"
            })

        # NO overall compliance leaf node; the tree ends with the above actionable nodes
        self._render_decision_tree(nodes, edges, title="Policy Compliance Decision Tree")

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
    
    def law_inference_page(self):
        """Render the Law Inference page using the new LawInferencePage class."""
        from UX.law_inference_page import LawInferencePage
        LawInferencePage(
            self.regulatory_metadata_repository,
            self.glossary_repository
        ).render()

    def obligation_inference_page(self):
        """Render the Obligation Inference page using the new ObligationInferencePage class."""
        from UX.obligation_inference_page import ObligationInferencePage
        ObligationInferencePage(
            self.glossary_repository,
            self.regulatory_metadata_repository,
            self.obligation_repository
        ).render()
            
    def policy_recommendation_api(self):
        """Implement a policy recommendation API based on data sensitivity and obligations.
        This allows users to input data elements and get policy recommendations.
        """
        st.markdown("<div class='page-header'><i class='fas fa-file-contract'></i> &nbsp;Policy Inference API</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Inference API</strong> recommends organizational policies that should be implemented based on the sensitivity of data and associated obligations.</p>
            <ul>
                <li>Analyzes data elements to determine their sensitivity levels</li>
                <li>Identifies security and privacy obligations based on sensitivity</li>
                <li>Maps obligations to relevant organizational policies</li>
                <li>Ranks policies by relevance to the identified obligations</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
            
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="policy_law")
        
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="policy_dst")
        else:
            st.warning("No data subject types available.")
            return
        
        # Option to select either data element or data category
        data_type = st.radio("Select Data Type", ["Data Element", "Data Category"], key="policy_data_type")
        
        if data_type == "Data Element":
            data_elements = self.glossary_repository.get_data_elements()
            if data_elements:
                de_options = [de["name"] for de in data_elements]
                selected_data = st.selectbox("Select Data Element", options=de_options, key="policy_data_element")
            else:
                st.warning("No data elements available.")
                return
        else:  # Data Category
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data = st.selectbox("Select Data Category", options=dc_options, key="policy_data_category")
            else:
                st.warning("No data categories available.")
                return
        
        # Add a button to trigger inference
        infer_button = st.button("Infer Policies", key="recommend_policies_button")
        
        # Show results below the button
        if infer_button:
            st.subheader("Policy Recommendations")
            # First, infer the sensitivity of the data
            sensitivity = self._infer_sensitivity(selected_law, selected_dst, selected_data, data_type)
            
            if sensitivity:
                st.success(f"Data sensitivity inferred: **{sensitivity}**")
                
                # Get sensitivity ID
                all_sensitivities = self.glossary_repository.get_sensitivities()
                sensitivity_id = None
                for s in all_sensitivities:
                    if s["name"] == sensitivity:
                        sensitivity_id = s["id"]
                        break
                
                if sensitivity_id:
                    # Get obligations for this sensitivity
                    sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                    
                    if sensitivity_obligations:
                        # Create a list of obligations for policy lookup
                        all_obligations = []
                        for so in sensitivity_obligations:
                            all_obligations.append({
                                "id": so["obligation_id"],
                                "name": so["obligation_name"],
                                "control_type": so["control_type"],
                                "priority": so["priority"]
                            })
                        
                        # Get policies for these obligations
                        st.subheader("Recommended Policies")
                        
                        # Get policies for the given obligations from the repository
                        all_policies = []
                        obligation_ids = [o["id"] for o in all_obligations]
                        
                        # Get policies for each obligation using the repository
                        for obligation_id in obligation_ids:
                            policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
                            obligation_name = next((o["name"] for o in all_obligations if o["id"] == obligation_id), "Unknown")
                            
                            for policy in policies:
                                all_policies.append({
                                    "Obligation": obligation_name,
                                    "Policy": policy["name"],
                                    "Description": policy["description"],
                                    "Status": policy["status"],
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
                                    key="policy_api_name_filter"
                                )
                            
                            with col2:
                                statuses = ["All"] + sorted(list(set(df["Status"])))
                                selected_status = st.selectbox(
                                    "Filter by Status",
                                    statuses,
                                    key="policy_api_status_filter"
                                )
                            
                            # Apply filters
                            filtered_df = df.copy()
                            if selected_policy != "All":
                                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                            if selected_status != "All":
                                filtered_df = filtered_df[filtered_df["Status"] == selected_status]
                            
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
                            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                                <h4 style="margin-top: 0;">Recommended Policy Implementation</h4>
                                <p>Based on the data elements and their sensitivity levels, the following policies should be implemented:</p>
                                <ol>
                            """, unsafe_allow_html=True)
                            
                            for policy in top_policies[:5]:  # Show top 5 policies
                                st.markdown(f"<li><strong>{policy}</strong></li>", unsafe_allow_html=True)
                            
                            st.markdown("""
                                </ol>
                                <p>These policies will address the compliance obligations required for the sensitive data.</p>
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
                    else:
                        st.info(f"No obligations defined for {sensitivity} sensitivity level.")
                else:
                    st.warning(f"Could not find sensitivity ID for {sensitivity}.")
            else:
                st.warning("Could not determine sensitivity for the selected data.")
                    
    def risk_inference_page(self):
        """Render the Risk Inference page using the new RiskInferencePage class."""
        
        RiskInferencePage(
            self.glossary_repository,
            self.regulatory_metadata_repository,
            self.obligation_repository
        ).render()

if __name__ == "__main__":
    app = DataMap()
    app.run()
