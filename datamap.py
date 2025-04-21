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
from UX.policy_compliance_page import PolicyCompliancePage
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
            self.glossary_repository,
            self.regulatory_metadata_repository
        )

        self.policy_compliance_page = PolicyCompliancePage(
            self.glossary_repository,
            self.regulatory_metadata_repository
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
        from UX.assets_page import AssetsPage
        AssetsPage(
            self.inventory_repository,
            self.glossary_repository,
            self.obligation_repository,
            self.sensitivity_inference
        ).render()
    
    def processing_activities_section(self):
        """Handle the Processing Activities section with purposes and data elements."""
        from UX.processing_activities_page import ProcessingActivitiesPage
        ProcessingActivitiesPage(self.inventory_repository, self.glossary_repository, self.regulatory_metadata_repository).render()
        
    def purposes_page(self):
        """Render the Purposes page using the new PurposesPage class."""
        from UX.purposes_page import PurposesPage
        PurposesPage(self.glossary_repository).render()
    
    def policies_page(self):
        """Display the Policies page with tabs for Policy Purpose, Policy Purpose Data Usage, and Policy Purpose Data Element."""
        from UX.policies_page import PoliciesPage
        PoliciesPage(self.glossary_repository, self.regulatory_metadata_repository).render()

    def policy_compliance(self):
        """Display the Policy Compliance page with the policy compliance analysis tool."""        
        self.policy_compliance_page.render()

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
            self.policy_recommendation_page()
        elif st.session_state['current_section'] == 'Risk API':
            self.risk_inference_page()
        elif st.session_state['current_section'] == 'Purposes':
            self.purposes_page()
        elif st.session_state['current_section'] == 'Policies':
            self.policies_page()
        elif st.session_state['current_section'] == 'Policy Compliance':
            self.policy_compliance()
        elif st.session_state['current_section'] == 'Control API':
            self.control_inference_page()            

    def control_inference_page(self):
        """Display the Control Inference page to recommend controls based on frameworks, policies, or risks."""
        from UX.control_inference_page import ControlInferencePage
        ControlInferencePage(self.glossary_repository, self.regulatory_metadata_repository).render()
        
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
        from UX.policy_inference_page import PolicyInferencePage
        PolicyInferencePage(self.glossary_repository).render()

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
            
    def policy_recommendation_page(self):
        """Render the Policy Recommendation API page using the new PolicyRecommendationPage class."""
        from UX.policy_recommendation_page import PolicyRecommendationPage
        PolicyRecommendationPage(
            self.glossary_repository,
            self.obligation_repository,
            self.sensitivity_inference
        ).render()
                    
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
