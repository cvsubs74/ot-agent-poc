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
from core.asset_policy_inference import AssetPolicyInference
from UX.data_use_governance_overview import DataUseGovernanceOverview
from UX.faq_page import FAQPage
from UX.policy_authoring_page import PolicyAuthoringPage
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
    SensitivityPoliciesPage,
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
from repositories.PolicyRepository import PolicyRepository
from repositories.ObligationRepository import ObligationRepository
from repositories.CatalogRepository import CatalogRepository
from repositories.ConsentRepository import ConsentRepository
from repositories.DataAccessRepository import DataAccessRepository
from repositories.KnowledgeRepository import KnowledgeRepository
from repositories.PolicyRepository import PolicyRepository

class DataMap:
    def __init__(self):
        """Initialize the DataMap application with repositories."""
        self.database_manager = DatabaseManager()
        self.glossary_repository = GlossaryRepository(self.database_manager.connection)
        self.regulatory_metadata_repository = RegulatoryMetadataRepository(self.database_manager.connection)
        self.inventory_repository = InventoryRepository(self.database_manager.connection)
        self.obligation_repository = ObligationRepository(self.database_manager.connection)
        self.catalog_repository = CatalogRepository(self.database_manager.connection)
        self.policy_repository = PolicyRepository(self.database_manager.connection)
        self.consent_repository = ConsentRepository(self.database_manager.connection)
        self.data_access_repository = DataAccessRepository(self.database_manager.connection)
        self.knowledge_repository = KnowledgeRepository(self.database_manager.connection)
        self.policy_repository = PolicyRepository(self.database_manager.connection)
        self.asset_policy_inference = AssetPolicyInference(
            self.catalog_repository,
            self.regulatory_metadata_repository,
            self.glossary_repository,
            self.inventory_repository,
            self.policy_repository
        )
        
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
        
        # Define all tab names and their handler lambdas
        tab_definitions = [
            ("Law Jurisdiction", lambda: LawJurisdictionPage(self.regulatory_metadata_repository).render()),
            ("Law Legal Basis", lambda: LawLegalBasisPage(self.regulatory_metadata_repository).render()),
            ("Law Incident Breach Notification", lambda: LawIncidentBreachNotificationPage(self.regulatory_metadata_repository).render()),
            ("Law Transfer", lambda: LawTransferPage(self.regulatory_metadata_repository).render()),
            ("Data Subject Access Request", lambda: DataSubjectAccessRequestPage(self.regulatory_metadata_repository).render()),
            ("Data Category Data Element", lambda: DataCategoryDataElementPage(self.regulatory_metadata_repository).render()),
            ("Law Data Subject Type Data Element Sensitivity", lambda: LawDataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()),
            ("Law Data Subject Type Data Category Sensitivity", lambda: LawDataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()),
            ("Data Subject Type Data Category Sensitivity", lambda: DataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()),
            ("Data Subject Type Data Element Sensitivity", lambda: DataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()),
            ("Law Purpose Category Legal Basis", lambda: LawPurposeCategoryLegalBasisPage(self.regulatory_metadata_repository).render()),
            ("Legal Basis Requirements", lambda: LegalBasisRequirementsPage(self.regulatory_metadata_repository).render()),
            ("Policy Purpose", lambda: PolicyPurposePage(self.regulatory_metadata_repository).render()),
            ("Policy Purpose Data Element", lambda: PolicyPurposeDataElementPage(self.regulatory_metadata_repository).render()),
            ("Policy Purpose Data Usage", lambda: PolicyPurposeDataUsagePage(self.regulatory_metadata_repository).render()),
            ("Sensitivity Policies", lambda: SensitivityPoliciesPage(self.glossary_repository, self.regulatory_metadata_repository).render()),
            ("Framework Control", lambda: FrameworkControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()),
            ("Policy Control", lambda: PolicyControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()),
            ("Risk Control", lambda: RiskControlPage(self.regulatory_metadata_repository, self.glossary_repository).render()),
        ]

        all_tab_names = [name for name, _ in tab_definitions]

        # Define which tabs are used by each inference API
        inference_api_mappings = {
            "All": list(range(len(all_tab_names))),  # All tabs
            "Law Inference": [0],  # Law Jurisdiction tab
            "Legal Basis Inference": [1, 10, 11],  # Law Legal Basis tab, Law Purpose Category Legal Basis, Legal Basis Requirements
            "Breach Notification Inference": [2],  # Law Incident Breach Notification tab
            "Transfer Mechanism Inference": [3],  # Law Transfer tab
            "Data Subject Rights Inference": [4],  # Data Subject Access Request tab
            "Data Sensitivity Inference": [5, 6, 7, 8, 9, 15],  # Various sensitivity-related tabs including Sensitivity Policies
            "Obligation Inference": [5, 6, 7, 8, 9, 15],  # Same tabs as Data Sensitivity Inference + Sensitivity Policies
            "Risk Inference": [5, 6, 7, 8, 9, 15],  # All tabs from Sensitivity Inference, Obligation Inference
            "Control Inference": [16, 17, 18]  # Framework Control, Policy Control, Risk Control tabs
        }

        # Create a filter for inference APIs
        st.markdown("<h3>Filter by Inference API</h3>", unsafe_allow_html=True)
        st.caption("Filter to view only the mapping tables used by each specific inference API. Each inference API uses different tables to make regulatory determinations.")

        inference_api_options = list(inference_api_mappings.keys())
        selected_inference_api = st.selectbox(
            "Select an Inference API",
            inference_api_options,
            key="inference_api_filter"
        )

        visible_tab_indices = inference_api_mappings[selected_inference_api]
        visible_tab_names = [all_tab_names[i] for i in visible_tab_indices]
        tabs = st.tabs(visible_tab_names)

        # Add explanation about how the selected inference API uses the mapping tables
        if selected_inference_api == "Law Inference":
            from UX.law_inference_page import LawInferencePage
            LawInferencePage.explain()
        elif selected_inference_api == "Legal Basis Inference":
            from UX.regulatory_metadata_pages import LawLegalBasisPage
            LawLegalBasisPage.explain()
        elif selected_inference_api == "Breach Notification Inference":
            from UX.breach_notification_page import BreachNotificationPage
            BreachNotificationPage.explain()

        elif selected_inference_api == "Transfer Mechanism Inference":
            from UX.regulatory_metadata_pages import LawTransferPage
            LawTransferPage.explain()

        elif selected_inference_api == "Data Subject Rights Inference":
            from UX.data_subject_rights_page import DataSubjectRightsPage
            DataSubjectRightsPage.explain()

        elif selected_inference_api == "Data Sensitivity Inference":
            from UX.sensitivity_inference_page import SensitivityInferencePage
            SensitivityInferencePage.explain()



        elif selected_inference_api == "Obligation Inference":
            from UX.obligation_inference_page import ObligationInferencePage    
            ObligationInferencePage.explain()

        elif selected_inference_api == "Risk Inference":
            from UX.risk_inference_page import RiskInferencePage    
            RiskInferencePage.explain()
            
        elif selected_inference_api == "Control Inference":
            from UX.control_inference_page import ControlInferencePage    
            ControlInferencePage.explain()
        
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
                    from UX.regulatory_metadata_pages import LawLegalBasisPage
                    LawLegalBasisPage(self.regulatory_metadata_repository).render()
        
                # Law Incident Breach Notification tab
                elif tab_idx == 2:
                    from UX.regulatory_metadata_pages import LawIncidentBreachNotificationPage
                    LawIncidentBreachNotificationPage(self.regulatory_metadata_repository).render()
        
                # Law Transfer tab
                elif tab_idx == 3:
                    from UX.regulatory_metadata_pages import LawTransferPage
                    LawTransferPage(self.regulatory_metadata_repository).render()

                elif tab_idx == 4:                        
                    from UX.regulatory_metadata_pages import DataSubjectAccessRequestPage
                    DataSubjectAccessRequestPage(self.regulatory_metadata_repository).render()
        
                # Data Category Data Element tab
                elif tab_idx == 5:
                    from UX.regulatory_metadata_pages import DataCategoryDataElementPage
                    DataCategoryDataElementPage(self.regulatory_metadata_repository).render()
        
                # Law Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 6:
                    from UX.regulatory_metadata_pages import LawDataSubjectTypeDataElementSensitivityPage
                    LawDataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()
        
                # Law Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 7:                        
                    from UX.regulatory_metadata_pages import LawDataSubjectTypeDataCategorySensitivityPage
                    LawDataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()
        
                # Data Subject Type Data Category Sensitivity tab
                elif tab_idx == 8:
                    from UX.regulatory_metadata_pages import DataSubjectTypeDataCategorySensitivityPage
                    DataSubjectTypeDataCategorySensitivityPage(self.regulatory_metadata_repository).render()
        
                # Data Subject Type Data Element Sensitivity tab
                elif tab_idx == 9:
                    from UX.regulatory_metadata_pages import DataSubjectTypeDataElementSensitivityPage
                    DataSubjectTypeDataElementSensitivityPage(self.regulatory_metadata_repository).render()
            
                # Law Purpose Category Legal Basis tab
                elif tab_idx == 10:
                    from UX.regulatory_metadata_pages import LawPurposeCategoryLegalBasisPage
                    LawPurposeCategoryLegalBasisPage(self.regulatory_metadata_repository).render()
                
                # Legal Basis Requirements tab
                elif tab_idx == 11:
                    from UX.regulatory_metadata_pages import LegalBasisRequirementsPage
                    LegalBasisRequirementsPage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose tab
                elif tab_idx == 12:
                    from UX.regulatory_metadata_pages import PolicyPurposePage
                    PolicyPurposePage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose Data Element tab
                elif tab_idx == 13:
                    from UX.regulatory_metadata_pages import PolicyPurposeDataElementPage
                    PolicyPurposeDataElementPage(self.regulatory_metadata_repository).render()
                
                # Policy Purpose Data Usage tab
                elif tab_idx == 14:
                    from UX.regulatory_metadata_pages import PolicyPurposeDataUsagePage
                    PolicyPurposeDataUsagePage(self.regulatory_metadata_repository).render()
                 
                # Sensitivity Policies tab
                elif tab_idx == 15:
                    from UX.regulatory_metadata_pages import SensitivityPoliciesPage
                    SensitivityPoliciesPage(self.glossary_repository, self.regulatory_metadata_repository).render()
                
                # Framework Control tab
                elif tab_idx == 16:
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
            self.catalog_repository,
            self.sensitivity_inference,
            self.regulatory_metadata_repository,
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
        PolicyCompliancePage(self.glossary_repository, self.regulatory_metadata_repository).render()
        
    def policy_authoring_page(self):
        """Display the Policy Authoring page for creating and managing data governance policies."""
        PolicyAuthoringPage(
            self.inventory_repository,
            self.glossary_repository,
            self.catalog_repository,
            SensitivityInference(self.glossary_repository, self.regulatory_metadata_repository),
            self.regulatory_metadata_repository,
            self.policy_repository
        ).render()
        
    def policy_applied_page(self):
        """Display the Policy Applied page showing how policies are applied at the table column level."""
        PolicyAppliedPage(
            self.glossary_repository,
            self.regulatory_metadata_repository,
            self.catalog_repository,
            self.policy_applied_repository,
            self.inventory_repository
        ).render()
        
    def roles_page(self):
        """Display the External Roles page with information about imported roles."""
        from UX.roles_page import RolesPage
        RolesPage(self.glossary_repository, self.regulatory_metadata_repository, self.policy_repository, self.inventory_repository).render()
    def run(self):
        """Main function to run the Streamlit app."""
        self.configure_page()
        
        # Clear session state and set default page to User Journey Overview
        # This ensures we always start with the User Journey Overview page
        if 'initialized' not in st.session_state:
            # First time initialization - clear any existing state and set our page
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Set the Data Use Governance Overview page as the default page
            # This provides a high-level overview of purpose-based access controls
            # using purpose-based roles and masking policies with IS_ROLE_IN_SESSION()
            st.session_state['current_section'] = 'DUG Overview'
            st.session_state['initialized'] = True

        self.divider(2)
        
        # Create sidebar with navigation
        with st.sidebar:
            
            # First section: Knowledge Base
            st.markdown("<div class='sidebar-section-header'>Knowledge Base</div>", unsafe_allow_html=True)
            
            # Knowledge Base FAQ menu item
            if st.button("❓ Knowledge Base FAQ", key="faq_btn", use_container_width=True):
                st.session_state['current_section'] = 'FAQ'
            
            # Second section: User Journeys
            st.markdown("<div class='sidebar-section-header'>User Journeys</div>", unsafe_allow_html=True)
            
            # Data Use Governance Overview menu item
            if st.button("📊 Overview", key="journey_overview_btn", use_container_width=True):
                st.session_state['current_section'] = 'DUG Overview'
            
            # Data Access Request Journey menu item
            if st.button("🔑 Data Access Request Journey", key="user_journey_btn", use_container_width=True):
                st.session_state['current_section'] = 'User Journey Overview'
            
            # Second section: Regulatory Intelligence
            st.markdown("<div class='sidebar-section-header'>Regulatory Intelligence</div>", unsafe_allow_html=True)
            
            # Core Constructs menu item
            if st.button("📚 Core Constructs", key="core_constructs_button", use_container_width=True):
                st.session_state['current_section'] = 'Core'
                
            # Regulatory Metadata menu item
            if st.button("📋 Regulatory Metadata", key="regulatory_btn", use_container_width=True):
                st.session_state['current_section'] = 'Regulatory'
                
            # Decision Tree menu item
            if st.button("🌳 Decision Tree", key="decision_tree_btn", use_container_width=True):
                st.session_state['current_section'] = 'Decision Tree'
            
            # Third section: Inference APIs
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
            

            
            # Risk Inference menu item
            if st.button("⚠️ Risk Inference", key="risk_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Risk API'

            # Control Inference menu item
            if st.button("⚠️ Control Inference", key="control_api_btn", use_container_width=True):
                st.session_state['current_section'] = 'Control API'                
            
            # Fourth section: Data Use Governance
            st.markdown("<div class='sidebar-section-header'>Data Use Governance</div>", unsafe_allow_html=True)
            
            # Data Use Governance section description
            
            # Purposes menu item
            if st.button("🎯 Purposes", key="purposes_btn", use_container_width=True):
                st.session_state['current_section'] = 'Purposes'
            
            # Policies menu item
            if st.button("📋 Policies", key="policies_btn", use_container_width=True):
                st.session_state['current_section'] = 'Policies'
            
            # Roles menu item
            if st.button("👥 Roles", key="roles_btn", use_container_width=True):
                st.session_state['current_section'] = 'Roles'
            
            # Consent Management menu item
            if st.button("🔐 Consents", key="consent_btn", use_container_width=True):
                st.session_state['current_section'] = 'Consent Management'
            
            # Request Data Access menu item
            if st.button("🔑 Request Data Access", key="data_access_btn", use_container_width=True):
                st.session_state['current_section'] = 'Data Access Request'
            
            # Policy Authoring menu item
            if st.button("✏️ Policy Authoring", key="policy_authoring_btn", use_container_width=True):
                st.session_state['current_section'] = 'Policy Authoring'
            
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
        section_handlers = {
            'Core': self.core_constructs_section,
            'Regulatory': self.regulatory_metadata_section,
            'Decision Tree': self.decision_tree_section,
            'Assets': self.assets_section,
            'Processing Activities': self.processing_activities_section,
            'Law API': self.law_inference_page,
            'Sensitivity API': self.sensitivity_inference_page,
            'Legal Basis API': self.legal_basis_inference_page,
            'Breach API': self.breach_notification_page,
            'Transfer API': self.transfer_mechanism_page,
            'DSR API': self.data_subject_rights_page,
            'Obligation API': self.obligation_inference_page,
            'Risk API': self.risk_inference_page,
            'DUG Overview': self.data_use_governance_overview,
            'Purposes': self.purposes_page,
            'Policies': self.policies_page,
            'Roles': self.roles_page,
            'Consent Management': self.consent_management_page,
            'Data Access Request': self.data_access_request_page,
            'User Journey Overview': self.user_journey_overview,
            'FAQ': self.faq_page,
            'Policy Compliance': self.policy_compliance,
            'Policy Authoring': self.policy_authoring_page,
            'Applied Policies': self.policy_applied_page,
            'Control API': self.control_inference_page,
        }
        handler = section_handlers.get(st.session_state['current_section'])
        if handler:
            handler()
       
    def data_use_governance_overview(self):
        """Display the Data Use Governance Overview page with diagrams and explanations."""
        from UX.data_use_governance_overview import DataUseGovernanceOverview
        DataUseGovernanceOverview(self.glossary_repository, self.regulatory_metadata_repository, self.policy_repository).render()
        
    def user_journey_overview(self):
        """Display the User Journey Overview page with data access request journey."""
        from UX.user_journey_overview import UserJourneyOverview
        UserJourneyOverview(
            self.glossary_repository, 
            self.regulatory_metadata_repository, 
            self.inventory_repository,
            self.policy_repository, 
            self.data_access_repository,
            self.catalog_repository,
            self.asset_policy_inference
        ).render()
        
    def faq_page(self):
        """Display the Knowledge Base FAQ page."""
        from UX.faq_page import FAQPage
        FAQPage(self.knowledge_repository).render()
        
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
            
    def risk_inference_page(self):
        """Render the Risk Inference page using the new RiskInferencePage class."""
        
        RiskInferencePage(
            self.glossary_repository,
            self.regulatory_metadata_repository,
            self.obligation_repository
        ).render()
        
    def consent_management_page(self):
        """Render the Consent Management page to manage user consents linked to purposes."""
        from UX.consent_management import ConsentManagementPage
        page = ConsentManagementPage(
            consent_repo=self.consent_repository,
            glossary_repo=self.glossary_repository,
            policy_repo=self.policy_repository
        )
        page.render()
        
    def data_access_request_page(self):
        """Render the Data Access Request page to request access to specific tables for specific purposes."""
        from UX.data_access_request_page import DataAccessRequestPage
        page = DataAccessRequestPage(
            glossary_repository=self.glossary_repository,
            catalog_repository=self.catalog_repository,
            inventory_repository=self.inventory_repository,
            asset_policy_inference=self.asset_policy_inference,
            data_access_repository=self.data_access_repository
        )
        page.render()

if __name__ == "__main__":
    app = DataMap()
    app.run()
