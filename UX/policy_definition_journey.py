import streamlit as st
import pandas as pd
import json

class PolicyDefinitionJourney:
    """Page for defining data governance policies."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, policy_repository, inventory_repository=None):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_repository = policy_repository
        self.inventory_repository = inventory_repository or glossary_repository
    
    def render(self):
        """Render the policy definition journey."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Definition</div>", unsafe_allow_html=True)
        
        # Add CSS for styled components
        st.markdown("""
        <style>
        /* Target only the expander components */
        div[data-testid="stExpander"] {
            border: 1px solid #3498db !important;
            border-radius: 4px !important;
            margin-bottom: 10px !important;
            background-color: #eaf2f8 !important;
        }
        div[data-testid="stExpander"] > div:first-child {
            background-color: #eaf2f8 !important;
            border-bottom: 1px solid #3498db !important;
            padding: 0.5rem !important;
        }
        div[data-testid="stExpander"] details summary p {
            color: #3498db !important;
            font-weight: 600 !important;
        }
        
        /* Form styling */
        div[data-testid="stForm"] {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
        
        /* Results container styling */
        .results-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #3498db;
        }
        
        /* Policy type badges */
        .policy-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
        }
        .security-badge {
            background-color: #e74c3c;
            color: white;
        }
        .access-badge {
            background-color: #3498db;
            color: white;
        }
        .retention-badge {
            background-color: #2ecc71;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Introduction
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>Define comprehensive policies to govern how data is accessed, secured, and retained across your organization. 
            Policies can be scoped by purpose, role, and data elements to create a flexible governance framework.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Policy type selection - outside form so it can trigger UI updates
        st.markdown("### Policy Information")
        policy_type = st.selectbox(
            "Policy Type",
            options=["Access Control", "Retention", "Security"],
            help="Select the type of policy you want to define"
        )
        
        # Main policy definition form - using a unique key
        with st.form("policy_definition_journey_form"):
            
            # Policy name and description
            col1, col2 = st.columns(2)
            with col1:
                policy_name = st.text_input("Policy Name", placeholder="Enter policy name")
            with col2:
                policy_status = st.selectbox("Status", options=["Draft", "Active", "Under Review", "Deprecated"])
            
            policy_description = st.text_area("Policy Description", placeholder="Enter policy description")
            
            # Purpose and role selection
            st.markdown("### Scope")
            
            # Purpose selection - simplified
            purpose_options = ["Marketing", "Analytics", "Customer Support", "Fraud Detection", "Compliance"]
            selected_purpose = st.selectbox(
                "Select Purpose",
                options=["None"] + purpose_options,
                format_func=lambda x: x if x != "None" else "No specific purpose",
                help="Select a purpose to scope this policy (optional)"
            )
            
            # Role selection - simplified
            if selected_purpose != "None":
                if selected_purpose == "Marketing":
                    role_options = ["Marketing Analyst", "Campaign Manager", "Social Media Specialist"]
                elif selected_purpose == "Analytics":
                    role_options = ["Data Analyst", "Business Intelligence", "Data Scientist"]
                elif selected_purpose == "Customer Support":
                    role_options = ["Support Agent", "Support Manager", "Technical Support"]
                elif selected_purpose == "Fraud Detection":
                    role_options = ["Fraud Analyst", "Risk Manager", "Security Specialist"]
                elif selected_purpose == "Compliance":
                    role_options = ["Compliance Officer", "Legal Counsel", "Auditor"]
                else:
                    role_options = []
                
                if role_options:
                    selected_role = st.selectbox(
                        "Select Role",
                        options=["None"] + role_options,
                        format_func=lambda x: x if x != "None" else "No specific role",
                        help="Select a role to further scope this policy (optional)"
                    )
                else:
                    st.info("No roles are mapped to this purpose. The policy will apply to all roles with this purpose.")
                    selected_role = "None"
            else:
                selected_role = "None"
            
            # Data element selection - simplified
            st.markdown("### Data Elements")
            
            # Create tabs for elements and categories
            tab1, tab2 = st.tabs(["Data Elements", "Data Categories"])
            
            with tab1:
                element_options = ["Email Address", "Phone Number", "Full Name", "Date of Birth", 
                                 "Social Security Number", "Credit Card Number", "Address", "IP Address"]
                
                selected_elements = st.multiselect(
                    "Select Data Elements",
                    options=element_options,
                    help="Select the data elements this policy will apply to"
                )
            
            with tab2:
                category_options = ["Personal Identifiable Information", "Financial Data", "Health Information", 
                                  "Behavioral Data", "Device Information", "Location Data"]
                
                selected_categories = st.multiselect(
                    "Select Data Categories",
                    options=category_options,
                    help="Select the data categories this policy will apply to"
                )
            
            # Policy-specific configuration
            st.markdown("### Policy Configuration")
            
            # Different form fields based on policy type
            if policy_type == "Access Control":
                # Operations allowed
                st.markdown("#### Operations Allowed")
                col1, col2, col3 = st.columns(3)
                with col1:
                    read_allowed = st.checkbox("Read", value=True)
                with col2:
                    write_allowed = st.checkbox("Write")
                with col3:
                    share_allowed = st.checkbox("Share")
                
                # Access conditions
                conditions = st.text_area("Conditions for Access", 
                                         placeholder="e.g., Only for identity verification, With explicit consent")
                
                # Approval requirements
                requires_approval = st.checkbox("Requires Approval")
                
                if requires_approval:
                    approval_workflow = st.selectbox(
                        "Approval Workflow",
                        options=["Manager", "Compliance", "Manager and Compliance", "Custom"]
                    )
                else:
                    approval_workflow = None
                
                # Expiration settings
                auto_expires = st.checkbox("Auto Expires")
                
                if auto_expires:
                    expiry_period = st.text_input("Expiry Period", placeholder="e.g., 24 hours, 30 days")
                else:
                    expiry_period = None
            
            elif policy_type == "Retention":
                # Retention period
                retention_period = st.text_input("Retention Period", placeholder="e.g., 7 years, 90 days")
                
                # Retention trigger
                retention_trigger = st.selectbox(
                    "Retention Trigger",
                    options=["Collection", "Last Access", "Last Modification", "Account Closure", "Contract Termination", "Custom"]
                )
                
                # Retention basis
                retention_basis = st.selectbox(
                    "Retention Basis",
                    options=["Legal Requirement", "Business Need", "Contractual Obligation", "Consent", "Legitimate Interest"]
                )
                
                # Exceptions
                exceptions = st.text_area("Exceptions", placeholder="e.g., Litigation hold, Ongoing investigation")
                
                # Auto-delete
                auto_delete = st.checkbox("Auto Delete", value=True)
            
            elif policy_type == "Security":
                # Encryption settings
                st.markdown("#### Encryption")
                encryption_required = st.checkbox("Requires Encryption", value=True)
                
                if encryption_required:
                    encryption_algorithm = st.selectbox(
                        "Encryption Algorithm",
                        options=["AES-256", "Database Default", "RSA", "Custom"]
                    )
                else:
                    encryption_algorithm = None
                
                # Masking settings
                st.markdown("#### Masking")
                masking_required = st.checkbox("Requires Masking", value=True)
                
                if masking_required:
                    masking_format = st.selectbox(
                        "Masking Format",
                        options=["Full", "Partial (Last 4)", "Partial (First 4)", "Tokenized", "Hashed", "Custom"]
                    )
                else:
                    masking_format = None
                
                # Logging settings
                st.markdown("#### Logging")
                logging_enabled = st.checkbox("Enable Logging", value=True)
                alerts_enabled = st.checkbox("Enable Alerts")
            
            # Submit button
            submitted = st.form_submit_button("Create Policy")
            
            if submitted:
                # Validate inputs
                if not policy_name:
                    st.error("Please enter a policy name.")
                elif not (selected_elements or selected_categories):
                    st.error("Please select at least one data element or data category.")
                else:
                    # Create policy config based on policy type
                    if policy_type == "Access Control":
                        # Collect operations
                        operations = []
                        if read_allowed:
                            operations.append("read")
                        if write_allowed:
                            operations.append("write")
                        if share_allowed:
                            operations.append("share")
                        
                        policy_config = {
                            "operations": operations,
                            "conditions": conditions if conditions else None,
                            "requires_approval": requires_approval,
                            "approval_workflow": approval_workflow if requires_approval else None,
                            "auto_expires": auto_expires,
                            "expiry_period": expiry_period if auto_expires else None
                        }
                    
                    elif policy_type == "Retention":
                        policy_config = {
                            "retention_period": retention_period,
                            "retention_trigger": retention_trigger,
                            "retention_basis": retention_basis,
                            "exceptions": exceptions if exceptions else None,
                            "auto_delete": auto_delete
                        }
                    
                    elif policy_type == "Security":
                        policy_config = {
                            "encryption": {
                                "required": encryption_required,
                                "algorithm": encryption_algorithm if encryption_required else None
                            },
                            "masking": {
                                "required": masking_required,
                                "format": masking_format if masking_required else None
                            },
                            "logging": {
                                "enabled": logging_enabled,
                                "alerts": alerts_enabled
                            }
                        }
                    
                    # Save policy to database
                    try:
                        # 1. Create the policy
                        policy_id = self.policy_repository.create_policy(
                            name=policy_name,
                            description=policy_description,
                            policy_type=policy_type,
                            status=policy_status
                        )
                        
                        if not policy_id:
                            st.error("Failed to create policy in the database.")
                            return
                        
                        # 2. Add purpose mapping if selected
                        policy_purpose_id = None
                        if selected_purpose != "None":
                            # Find purpose ID by name (in a real implementation, you'd have the actual ID)
                            # For this simplified version, we'll create a mapping to purpose ID 1
                            purpose_id = 1  # Default to first purpose
                            # In a real implementation, you'd look up the purpose ID by name
                            # purpose_id = self.glossary_repository.get_purpose_id_by_name(selected_purpose)
                            
                            policy_purpose_id = self.policy_repository.add_policy_purpose(policy_id, purpose_id)
                            if not policy_purpose_id:
                                st.warning("Failed to associate purpose with policy.")
                        
                        # 3. Add data elements
                        data_element_mappings = []
                        if selected_elements and policy_purpose_id:
                            for element_name in selected_elements:
                                # In a real implementation, you'd look up the data element ID by name
                                # For this simplified version, we'll create a mapping to data element ID 1
                                data_element_id = 1  # Default to first data element
                                
                                mapping_id = self.policy_repository.add_policy_data_element(
                                    policy_purpose_id, data_element_id)
                                if mapping_id:
                                    data_element_mappings.append(mapping_id)
                        
                        # 4. Add policy-specific configuration
                        if policy_type == "Access Control" and data_element_mappings:
                            for mapping_id in data_element_mappings:
                                self.policy_repository.add_policy_data_usage(
                                    mapping_id, policy_config["operations"])
                        
                        elif policy_type == "Retention" and data_element_mappings:
                            for mapping_id in data_element_mappings:
                                self.policy_repository.add_policy_data_retention(
                                    mapping_id, 
                                    policy_config["retention_period"],
                                    policy_config["retention_trigger"],
                                    policy_config["retention_basis"],
                                    policy_config["auto_delete"]
                                )
                        
                        elif policy_type == "Security" and data_element_mappings:
                            for mapping_id in data_element_mappings:
                                self.policy_repository.add_policy_data_security(
                                    mapping_id,
                                    policy_config["encryption"]["required"],
                                    policy_config["encryption"]["algorithm"],
                                    policy_config["masking"]["required"],
                                    policy_config["masking"]["format"],
                                    policy_config["logging"]["enabled"]
                                )
                        
                        # Display success message and policy details
                        st.success(f"Policy '{policy_name}' created successfully and saved to the database!")
                        
                        # Show policy details
                        st.markdown("### Policy Details")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Name:** {policy_name}")
                            st.markdown(f"**Type:** {policy_type}")
                            st.markdown(f"**Status:** {policy_status}")
                            st.markdown(f"**Policy ID:** {policy_id}")
                        with col2:
                            st.markdown(f"**Purpose:** {selected_purpose if selected_purpose != 'None' else 'Not specified'}")
                            st.markdown(f"**Role:** {selected_role if selected_role != 'None' else 'Not specified'}")
                        
                        st.markdown("#### Description")
                        st.markdown(policy_description if policy_description else "No description provided.")
                        
                        st.markdown("#### Data Elements")
                        if selected_elements:
                            for element in selected_elements:
                                st.markdown(f"- {element}")
                        
                        st.markdown("#### Data Categories")
                        if selected_categories:
                            for category in selected_categories:
                                st.markdown(f"- {category}")
                        
                        st.markdown("#### Configuration")
                        st.json(policy_config)
                    
                    except Exception as e:
                        st.error(f"Error saving policy to database: {str(e)}")
                        st.markdown("#### Policy Configuration (Not Saved)")
                        st.json(policy_config)
