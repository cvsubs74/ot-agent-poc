import streamlit as st
import pandas as pd
from UX.policy_authoring_page import PolicyAuthoringPage

class PolicyAuthoringJourney:
    """Class to render the Policy Authoring Journey page."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, inventory_repository, 
                 policy_repository, catalog_repository, sensitivity_inference):
        """Initialize with repositories."""
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.inventory_repository = inventory_repository
        self.policy_repository = policy_repository
        self.catalog_repository = catalog_repository
        self.sensitivity_inference = sensitivity_inference
        
    def render(self):
        """Render the Policy Authoring Journey page."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Authoring Journey</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This page demonstrates the complete policy authoring journey through the Data Use Governance platform. 
            It shows how to define, generate, and document data governance policies for both sensitivity-based and purpose-based scenarios.</p>
        </div>''', unsafe_allow_html=True)
        
        # Create tabs for different journey sections
        tabs = st.tabs([
            "Overview",
            "Policy Creation Process",
            "Author Policies"
        ])
        
        # Overview tab
        with tabs[0]:
            self._render_overview()
            
        # Policy Creation Process tab
        with tabs[1]:
            self._render_policy_creation_process()
            
        # Author Policies tab
        with tabs[2]:
            if self.catalog_repository and self.sensitivity_inference:
                PolicyAuthoringPage(
                    self.inventory_repository,
                    self.glossary_repository,
                    self.catalog_repository,
                    self.sensitivity_inference,
                    self.regulatory_metadata_repository,
                    self.policy_repository
                ).render()
            else:
                st.warning("Policy Authoring functionality requires catalog repository and sensitivity inference. Please navigate to the main Policy Authoring page.")
                st.button("Go to Policy Authoring", on_click=lambda: st.session_state.update({"current_section": "Policy Authoring"}))
    
    def _render_overview(self):
        """Render the overview of the policy authoring journey."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Authoring Journey</h3>
        """, unsafe_allow_html=True)
        
        # Journey steps
        journey_steps = [
            {
                "step": "Select Data Elements",
                "description": "Choose the data elements for which you need to create governance policies. These could be sensitive data like PII, financial information, or health data.",
                "icon": "🔍",
                "color": "#1E88E5"
            },
            {
                "step": "Define Context",
                "description": "Specify the jurisdiction and data subject type to ensure policies comply with relevant regulations like GDPR, CCPA, or HIPAA.",
                "icon": "🌍",
                "color": "#43A047"
            },
            {
                "step": "Generate Sensitivity-Based Policies",
                "description": "Create policies based on the inherent sensitivity of data elements, such as security controls for PII or usage restrictions for financial data.",
                "icon": "🔒",
                "color": "#FB8C00"
            },
            {
                "step": "Generate Purpose-Based Policies",
                "description": "Define policies based on specific business purposes like marketing, analytics, or customer support, ensuring data is only used for approved purposes.",
                "icon": "🎯",
                "color": "#E53935"
            },
            {
                "step": "Review & Document",
                "description": "Review the generated policies and create a comprehensive policy document that can be shared with stakeholders and used for compliance purposes.",
                "icon": "📄",
                "color": "#8E24AA"
            }
        ]
        
        # Display journey steps in a more integrated horizontal layout
        for step in journey_steps:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid {step['color']};">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: {step['color']}; color: white; padding: 10px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 20px;">
                        {step['icon']}
                    </div>
                    <div>
                        <h4 style="color: {step['color']}; margin: 0;">{step['step']}</h4>
                    </div>
                </div>
                <p style="margin-top: 10px; margin-left: 55px;">{step['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Benefits section
        st.markdown("""
        <h3 style="color: #1565C0;">Benefits of Policy Authoring</h3>
        """, unsafe_allow_html=True)
        
        benefits = [
            {
                "benefit": "Regulatory Compliance",
                "description": "Ensure data handling practices comply with relevant regulations like GDPR, CCPA, HIPAA, etc.",
                "icon": "⚖️"
            },
            {
                "benefit": "Standardized Governance",
                "description": "Create consistent data governance policies across the organization.",
                "icon": "📏"
            },
            {
                "benefit": "Risk Mitigation",
                "description": "Reduce the risk of data breaches, misuse, and regulatory penalties.",
                "icon": "🛡️"
            },
            {
                "benefit": "Operational Efficiency",
                "description": "Streamline policy creation and enforcement, reducing manual effort and inconsistencies.",
                "icon": "⚙️"
            },
            {
                "benefit": "Transparent Documentation",
                "description": "Generate clear, comprehensive policy documentation for stakeholders and auditors.",
                "icon": "📊"
            }
        ]
        
        # Display benefits in a 2-column layout
        cols = st.columns(2)
        for i, benefit in enumerate(benefits):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4>{benefit['icon']} {benefit['benefit']}</h4>
                    <p>{benefit['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _render_policy_creation_process(self):
        """Render the policy creation process details."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Creation Process</h3>
        """, unsafe_allow_html=True)
        
        # Process explanation
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <p>The policy creation process involves several steps that work together to generate comprehensive data governance policies.
            Here's how the system works:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Process steps with detailed explanations
        process_steps = [
            {
                "title": "Data Element Analysis",
                "content": """
                <div style="margin-bottom: 15px;">
                    <p>When you select data elements, the system analyzes:</p>
                    <ul>
                        <li><strong>Sensitivity Classification:</strong> Determines if the data is PII, financial, health-related, etc.</li>
                        <li><strong>Regulatory Requirements:</strong> Identifies applicable regulations based on data type and jurisdiction</li>
                        <li><strong>Risk Level:</strong> Assesses the potential impact of data exposure or misuse</li>
                    </ul>
                </div>
                """
            },
            {
                "title": "Sensitivity-Based Policy Generation",
                "content": """
                <div style="margin-bottom: 15px;">
                    <p>For sensitivity-based policies, the system:</p>
                    <ul>
                        <li><strong>Maps Data Elements to Sensitivity Levels:</strong> Categorizes data as high, medium, or low sensitivity</li>
                        <li><strong>Applies Security Controls:</strong> Determines appropriate encryption, masking, and access controls</li>
                        <li><strong>Defines Usage Restrictions:</strong> Sets limitations on how data can be used based on sensitivity</li>
                        <li><strong>Establishes Retention Rules:</strong> Determines how long data should be kept based on regulations</li>
                    </ul>
                </div>
                """
            },
            {
                "title": "Purpose-Based Policy Generation",
                "content": """
                <div style="margin-bottom: 15px;">
                    <p>For purpose-based policies, the system:</p>
                    <ul>
                        <li><strong>Maps Business Purposes to Data Elements:</strong> Identifies which data elements are needed for each purpose</li>
                        <li><strong>Determines Legal Basis:</strong> Establishes the legal basis for processing (consent, legitimate interest, etc.)</li>
                        <li><strong>Sets Access Controls:</strong> Defines who can access the data for each purpose</li>
                        <li><strong>Creates Purpose-Specific Retention Rules:</strong> Determines how long data can be kept for each purpose</li>
                    </ul>
                </div>
                """
            },
            {
                "title": "Policy Document Generation",
                "content": """
                <div style="margin-bottom: 15px;">
                    <p>When generating the policy document, the system:</p>
                    <ul>
                        <li><strong>Consolidates Policies:</strong> Combines sensitivity and purpose-based policies into a comprehensive document</li>
                        <li><strong>Formats for Readability:</strong> Organizes policies in a clear, structured format</li>
                        <li><strong>Includes Metadata:</strong> Adds information about policy creation date, version, and applicable regulations</li>
                        <li><strong>Generates Implementation Guidance:</strong> Provides technical recommendations for implementing the policies</li>
                    </ul>
                </div>
                """
            }
        ]
        
        # Display process steps
        for step in process_steps:
            with st.expander(step["title"], expanded=True):
                st.markdown(step["content"], unsafe_allow_html=True)
        
        # Sample policy document
        with st.expander("Sample Policy Document", expanded=False):
            st.markdown("""
            # Data Governance Policy Document
            
            ## 1. Introduction
            
            This document outlines the data governance policies for handling sensitive data elements within the organization. These policies are designed to ensure compliance with relevant regulations, protect data subjects' rights, and maintain data security and privacy.
            
            ## 2. Scope
            
            These policies apply to all employees, contractors, and third parties who handle the specified data elements. The policies cover data collection, storage, processing, sharing, and deletion.
            
            ## 3. Policies
            
            ### 3.1 Sensitivity-Based Policies
            
            #### Email Address (Medium Sensitivity)
            * **Usage Policy:** Email Usage Restriction - Email addresses can only be used for account management and communication
            * **Retention Policy:** Contact Retention - Email addresses must be deleted 2 years after last interaction
            
            #### Credit Card Number (High Sensitivity)
            * **Security Policy:** PCI Compliance Policy - Credit card numbers must be masked and encrypted
            * **Retention Policy:** Payment Data Retention - Must be deleted after transaction completion
            
            #### Home Address (Medium Sensitivity)
            * **Usage Policy:** Address Usage Restriction - Home addresses can only be used for shipping and billing
            * **Security Policy:** Address Protection - Must be encrypted in databases
            
            #### Date of Birth (Medium Sensitivity)
            * **Retention Policy:** DOB Retention Policy - Date of birth must be deleted after 7 years
            * **Security Policy:** DOB Masking - Should display only month and day for general use
            
            ### 3.2 Purpose-Based Policies
            
            #### Marketing Purpose
            * **Email Address:**
              * Usage Policy: Marketing Email Policy - Email can be used for marketing with explicit consent
              * Retention Policy: Contact Retention - Retained until consent withdrawal
            
            * **Purchase History:**
              * Retention Policy: Purchase History Retention - Purchase history retained for 2 years for marketing
              * Usage Policy: Purchase Analysis - Can be used for personalized recommendations
            
            #### Customer Support Purpose
            * **Customer ID:**
              * Security Policy: Customer ID Security - Customer IDs must be masked for support staff
              * Usage Policy: Support Identification - Used only for customer verification
            
            #### Analytics Purpose
            * **Browsing History:**
              * Usage Policy: Analytics Usage Policy - Browsing history must be anonymized for analytics
              * Retention Policy: Analytics Data Retention - Retained for 90 days
            
            ## 4. Compliance and Enforcement
            
            All employees, contractors, and third parties handling the data elements covered by this policy must comply with these governance policies. Non-compliance may result in disciplinary action, up to and including termination of employment or contract.
            
            Regular audits will be conducted to ensure compliance with these policies. Any exceptions to these policies must be documented and approved by the Data Governance Committee.
            
            ## 5. Policy Review
            
            This policy document will be reviewed annually or whenever there are significant changes to the data landscape, regulatory requirements, or business needs.
            """)
    
    def render_embedded(self):
        """Render the Policy Authoring Journey page embedded within another page."""
        # Create tabs for different journey sections
        tabs = st.tabs([
            "Overview",
            "Policy Creation Process",
            "Author Policies"
        ])
        
        # Overview tab
        with tabs[0]:
            self._render_overview()
            
        # Policy Creation Process tab
        with tabs[1]:
            self._render_policy_creation_process()
            
        # Author Policies tab
        with tabs[2]:
            if self.catalog_repository and self.sensitivity_inference:
                PolicyAuthoringPage(
                    self.inventory_repository,
                    self.glossary_repository,
                    self.catalog_repository,
                    self.sensitivity_inference,
                    self.regulatory_metadata_repository,
                    self.policy_repository
                ).render()
            else:
                st.warning("Policy Authoring functionality requires catalog repository and sensitivity inference. Please navigate to the main Policy Authoring page.")
                st.button("Go to Policy Authoring", on_click=lambda: st.session_state.update({"current_section": "Policy Authoring"}))
