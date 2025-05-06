import streamlit as st
import pandas as pd
from UX.data_access_request_page import DataAccessRequestPage
from UX.policy_authoring_journey import PolicyAuthoringJourney

class UserJourneyOverview:
    """Class to render the User Journey Overview page."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, inventory_repository, policy_repository, data_access_repository, catalog_repository=None, asset_policy_inference=None, sensitivity_inference=None):
        """Initialize with repositories."""
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.inventory_repository = inventory_repository
        self.policy_repository = policy_repository
        self.data_access_repository = data_access_repository
        self.catalog_repository = catalog_repository
        self.asset_policy_inference = asset_policy_inference
        self.sensitivity_inference = sensitivity_inference
        
    def render(self):
        """Render the Data Access Request Journey page."""
        st.markdown("<div class='page-header'><i class='fas fa-route'></i> &nbsp;Data Access Request Journey</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This page demonstrates the complete data access request journey through the Data Use Governance platform. 
            It shows how different components work together to implement purpose-based access controls for sensitive data.</p>
        </div>''', unsafe_allow_html=True)
        
        # Create tabs for different user journeys
        tabs = st.tabs([
            "Overview",
            "Manage Policies",
            "Request Data Access"
        ])
        
        # Overview tab
        with tabs[0]:
            self._render_overview()
            
        # View Policies by Purpose tab
        with tabs[1]:
            self._render_policies_by_purpose()
            
        # Request Data Access tab
        with tabs[2]:
            if self.catalog_repository and self.asset_policy_inference:
                DataAccessRequestPage(
                    self.glossary_repository,
                    self.catalog_repository,
                    self.inventory_repository,
                    self.asset_policy_inference,
                    self.data_access_repository
                ).render_embedded()
            else:
                st.warning("Data Access Request functionality requires catalog repository and asset policy inference. Please navigate to the main Data Access Request page.")
                st.button("Go to Data Access Request", on_click=lambda: st.session_state.update({"current_section": "Data Access Request"}))
        
    # This method has been merged into the render method
    
    def _render_policy_authoring_journey(self):
        """Render the Policy Authoring Journey page."""
        if self.catalog_repository and self.sensitivity_inference:
            PolicyAuthoringJourney(
                self.glossary_repository,
                self.regulatory_metadata_repository,
                self.inventory_repository,
                self.policy_repository,
                self.catalog_repository,
                self.sensitivity_inference
            ).render_embedded()
        else:
            st.warning("Policy Authoring Journey requires catalog repository and sensitivity inference. Please navigate to the main Policy Authoring page.")
            st.button("Go to Policy Authoring", on_click=lambda: st.session_state.update({"current_section": "Policy Authoring"}))
    
    def _render_overview(self):
        """Render the overview of user journeys."""
        st.markdown("""
        <h3 style="color: #1565C0;">Overview</h3>
        """, unsafe_allow_html=True)
        
        # Journey steps
        journey_steps = [
            {
                "step": "Manage Policies",
                "description": "Define and manage policies by purposes. For example, create a 'Marketing Analytics' purpose with specific data usage, retention, and security policies for customer data elements.",
                "icon": "📋",
                "color": "#1E88E5"
            },
            {
                "step": "Submit Data Access Request",
                "description": "Users submit a formal request specifying the data they need access to and the business purpose. For example, a data analyst requests access to customer transaction data for the 'Marketing Analytics' purpose.",
                "icon": "🔑",
                "color": "#43A047"
            },
            {
                "step": "Automatic Policy Evaluation",
                "description": "The system evaluates the request against existing policies and determines appropriate access controls. For example, it identifies that PII fields require masking and transaction data needs row-level filtering based on consent.",
                "icon": "⚙️",
                "color": "#8E24AA"
            },
            {
                "step": "Security Policy Generation",
                "description": "Based on the evaluation, the system generates purpose-based security policies. For example, it creates PURPOSE_MARKETING_ANALYTICS role with appropriate masking policies using IS_ROLE_IN_SESSION() for sensitive fields.",
                "icon": "🛡️",
                "color": "#E53935"
            },
            {
                "step": "Access Granted",
                "description": "The user receives access to the requested data with appropriate security controls in place. For example, the analyst can now query customer data with email addresses masked and only see records with marketing consent.",
                "icon": "✅",
                "color": "#00ACC1"
            }
        ]
        
        # Display the journey as a modern timeline with cards
        for i, step in enumerate(journey_steps):
            st.markdown(f"""
            <div style="border-left: 4px solid {step['color']}; background-color: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); transition: all 0.3s ease; position: relative; z-index: 1;" onmouseover="this.style.transform='translateY(-8px) translateX(5px)'; this.style.boxShadow='0 12px 20px rgba(0, 0, 0, 0.15)'; this.style.zIndex='2';" onmouseout="this.style.transform='translateY(0) translateX(0)'; this.style.boxShadow='0 2px 4px rgba(0, 0, 0, 0.05)'; this.style.zIndex='1';">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: {step['color']}; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i+1}</div>
                    <div>
                        <h3 style="margin: 0; font-size: 1.2rem; color: {step['color']}">{step['step']}</h3>
                        <p style="margin: 5px 0 0 0; color: #616161;">{step['description']}</p>
                    </div>
                    <div style="margin-left: auto; font-size: 24px;">{step['icon']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add connector line between steps
            if i < len(journey_steps) - 1:
                st.markdown(f"<div style='border-left: 2px dashed #E0E0E0; height: 20px; margin-left: 15px;'></div>", unsafe_allow_html=True)
    
    def _render_policies_by_purpose(self):
        """Render the policies by purpose view."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policies by Purpose</h3>
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <p>This view shows all policies associated with a selected purpose, including data security, data usage, and data retention policies.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get purposes for dropdown
        purposes = self.glossary_repository.get_purposes()
        if not purposes:
            st.warning("No purposes defined in the system.")
            return
            
        purpose_options = {p["id"]: p["name"] for p in purposes}
        selected_purpose_id = st.selectbox(
            "Select Purpose", 
            options=list(purpose_options.keys()),
            format_func=lambda x: purpose_options.get(x, "Unknown")
        )
        
        if selected_purpose_id:
            selected_purpose_name = purpose_options[selected_purpose_id]
            st.markdown(f"<h4>Policies for: {selected_purpose_name}</h4>", unsafe_allow_html=True)
            
            # Create tabs for different policy types
            policy_tabs = st.tabs([
                "Data Usage Policies",
                "Data Retention Policies",
                "Data Security Policies"
            ])
            
            # Usage Policies
            with policy_tabs[0]:
                self._render_usage_policies(selected_purpose_id)
                
            # Retention Policies
            with policy_tabs[1]:
                self._render_retention_policies(selected_purpose_id)
                
            # Security Policies
            with policy_tabs[2]:
                self._render_security_policies(selected_purpose_id)
    
    def _render_usage_policies(self, purpose_id):
        """Render usage policies for the selected purpose."""
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #1565C0;">
            <b>About Usage Policies:</b><br>
            Usage policies define what operations (read, write, share) are permitted on data elements for a specific purpose.
        </div>
        """, unsafe_allow_html=True)
        
        # Get all policy-purpose mappings
        all_policy_purpose_mappings = self.regulatory_metadata_repository.get_policy_purposes()
        
        # Filter to get only the mappings for this purpose
        policy_purpose_mappings = [mapping for mapping in all_policy_purpose_mappings if mapping["purpose_id"] == purpose_id]
        
        if not policy_purpose_mappings:
            st.info("No policies associated with this purpose.")
            return
            
        # Extract policy IDs
        policy_ids = [mapping["policy_id"] for mapping in policy_purpose_mappings]
        
        # Get usage policies for these policies
        all_usage_policies = []
        for policy_id in policy_ids:
            usage_policies = self.regulatory_metadata_repository.get_policy_data_element_usage(policy_id=policy_id)
            all_usage_policies.extend(usage_policies)
        
        if all_usage_policies:
            # Create a DataFrame for display
            usage_data = {
                "Policy": [],
                "Data Element": [],
                "Operation": [],
                "Allowed": [],
                "Restrictions": []
            }
            
            for policy in all_usage_policies:
                usage_data["Policy"].append(policy["policy_name"])
                usage_data["Data Element"].append(policy["data_element_name"])
                usage_data["Operation"].append(policy["operation"])
                usage_data["Allowed"].append("✅" if policy["allowed"] else "❌")
                usage_data["Restrictions"].append(policy["restrictions"] if policy["restrictions"] else "None")
            
            # Convert to DataFrame and display
            df = pd.DataFrame(usage_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No usage policies defined for this purpose.")

    
    def _render_retention_policies(self, purpose_id):
        """Render retention policies for the selected purpose."""
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #1565C0;">
            <b>About Retention Policies:</b><br>
            Retention policies define how long data can be kept and what happens when the retention period expires.
        </div>
        """, unsafe_allow_html=True)
        
        # Get all policy-purpose mappings
        all_policy_purpose_mappings = self.regulatory_metadata_repository.get_policy_purposes()
        
        # Filter to get only the mappings for this purpose
        policy_purpose_mappings = [mapping for mapping in all_policy_purpose_mappings if mapping["purpose_id"] == purpose_id]
        
        if not policy_purpose_mappings:
            st.info("No policies associated with this purpose.")
            return
            
        # Extract policy IDs
        policy_ids = [mapping["policy_id"] for mapping in policy_purpose_mappings]
        
        # Get retention policies for these policies
        all_retention_policies = []
        for policy_id in policy_ids:
            retention_policies = self.regulatory_metadata_repository.get_policy_data_element_retention(policy_id=policy_id)
            all_retention_policies.extend(retention_policies)
        
        if all_retention_policies:
            # Create a DataFrame for display
            retention_data = {
                "Policy": [],
                "Data Element": [],
                "Retention Period": [],
                "Retention Basis": [],
                "Exceptions": []
            }
            
            for policy in all_retention_policies:
                retention_data["Policy"].append(policy["policy_name"])
                retention_data["Data Element"].append(policy["data_element_name"])
                retention_data["Retention Period"].append(policy["retention_period"])
                retention_data["Retention Basis"].append(policy["retention_basis"])
                retention_data["Exceptions"].append(policy["exceptions"] if policy["exceptions"] else "None")
            
            # Convert to DataFrame and display
            df = pd.DataFrame(retention_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No retention policies defined for this purpose.")
    
    def _render_security_policies(self, purpose_id):
        """Render security policies for the selected purpose."""
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #1565C0;">
            <b>About Security Policies:</b><br>
            Security policies define how data is protected, including masking, encryption, and access controls.
        </div>
        """, unsafe_allow_html=True)
        
        # Get all policy-purpose mappings
        all_policy_purpose_mappings = self.regulatory_metadata_repository.get_policy_purposes()
        
        # Filter to get only the mappings for this purpose
        policy_purpose_mappings = [mapping for mapping in all_policy_purpose_mappings if mapping["purpose_id"] == purpose_id]
        
        if not policy_purpose_mappings:
            st.info("No policies associated with this purpose.")
            return
            
        # Extract policy IDs
        policy_ids = [mapping["policy_id"] for mapping in policy_purpose_mappings]
        
        # Get security policies for these policies
        all_security_policies = []
        for policy_id in policy_ids:
            security_policies = self.regulatory_metadata_repository.get_policy_data_element_security(policy_id=policy_id)
            all_security_policies.extend(security_policies)
        
        if all_security_policies:
            # Create a DataFrame for display
            security_data = {
                "Policy": [],
                "Data Element": [],
                "Encryption": [],
                "Masking": [],
                "Access Control": []
            }
            
            for policy in all_security_policies:
                security_data["Policy"].append(policy["policy_name"])
                security_data["Data Element"].append(policy["data_element_name"])
                
                # Format encryption info
                encryption_info = "Not Required"
                if policy["requires_encryption"]:
                    encryption_info = f"Required ({policy['encryption_algorithm']})"
                security_data["Encryption"].append(encryption_info)
                
                # Format masking info
                masking_info = "Not Required"
                if policy["requires_masking"]:
                    masking_info = f"Required ({policy['masking_format']})"
                security_data["Masking"].append(masking_info)
                
                # Format access control info
                access_control_info = "Not Required"
                if policy["requires_access_control"]:
                    access_control_info = f"Required ({policy['access_control_type']})"
                security_data["Access Control"].append(access_control_info)
            
            # Convert to DataFrame and display
            df = pd.DataFrame(security_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No security policies defined for this purpose.")
