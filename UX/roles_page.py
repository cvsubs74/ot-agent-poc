import streamlit as st
import pandas as pd
import random

class RolesPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Display the External Roles page with information about imported roles."""
        st.markdown("<div class='page-header'><i class='fas fa-users'></i> &nbsp;External Roles</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of roles imported from external systems such as Snowflake, Databricks, or other access management platforms.</p>
            <ul>
                <li>External roles are used for access governance and policy compliance</li>
                <li>Roles can have specific overrides for data usage, retention, and security policies</li>
                <li>Role-based policy enforcement ensures proper access controls across systems</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Create tabs for the different sections
        tabs = st.tabs([
            "External Roles",
            "Usage Policy Overrides",
            "Retention Policy Overrides",
            "Security Policy Overrides"
        ])
        
        # Get external roles
        roles = self.glossary_repository.get_external_roles()
        
        # External Roles tab
        with tabs[0]:
            # Import roles section
            st.markdown("<h5>Import External Roles</h5>", unsafe_allow_html=True)
            st.markdown("Import roles from external systems like Snowflake, Databricks, or other access management platforms.")
            
            col1, col2 = st.columns(2)
            with col1:
                # Snowflake roles import
                st.markdown("<h6>Snowflake Roles</h6>", unsafe_allow_html=True)
                if st.button("Import Snowflake Roles", key="import_snowflake"):
                    # Simulate importing Snowflake roles
                    snowflake_roles = [
                        ("MARKETING_ANALYST", "Marketing data analysis role", "Snowflake", "MARKETING_ANALYST"),
                        ("MARKETING_ADMIN", "Marketing administration role", "Snowflake", "MARKETING_ADMIN"),
                        ("CUSTOMER_SUPPORT_REP", "Customer support representative", "Snowflake", "CUSTOMER_SUPPORT_REP"),
                        ("FINANCE_ANALYST", "Financial data analysis role", "Snowflake", "FINANCE_ANALYST")
                    ]
                    
                    for role in snowflake_roles:
                        self.glossary_repository.add_external_role(*role)
                    
                    st.success(f"Successfully imported {len(snowflake_roles)} Snowflake roles")
            
            with col2:
                # Databricks roles import
                st.markdown("<h6>Databricks Roles</h6>", unsafe_allow_html=True)
                if st.button("Import Databricks Roles", key="import_databricks"):
                    # Simulate importing Databricks roles
                    databricks_roles = [
                        ("Product_Analytics_User", "Product usage analytics role", "Databricks", "PRODUCT_ANALYTICS"),
                        ("Research_Scientist", "Research and development data science role", "Databricks", "RESEARCH_SCIENTIST"),
                        ("Fraud_Detection_Analyst", "Fraud detection and prevention", "Databricks", "FRAUD_ANALYST"),
                        ("Compliance_Officer", "Regulatory compliance monitoring", "Databricks", "COMPLIANCE_OFFICER")
                    ]
                    
                    for role in databricks_roles:
                        self.glossary_repository.add_external_role(*role)
                    
                    st.success(f"Successfully imported {len(databricks_roles)} Databricks roles")
            
            # Display existing roles
            st.markdown("<h5>External Roles</h5>", unsafe_allow_html=True)
            if roles:
                # Create a DataFrame for display
                role_data = {
                    "ID": [],
                    "Name": [],
                    "Description": [],
                    "Source System": [],
                    "Source Role Name": []
                }
                
                for role in roles:
                    role_data["ID"].append(role[0])
                    role_data["Name"].append(role[1])
                    role_data["Description"].append(role[2] if role[2] else "")
                    role_data["Source System"].append(role[3] if role[3] else "")
                    role_data["Source Role Name"].append(role[4] if role[4] else "")
                
                role_df = pd.DataFrame(role_data)
                st.dataframe(role_df, use_container_width=True)
                
                # Create role overrides section
                st.markdown("<h5>Create Role Policy Overrides</h5>", unsafe_allow_html=True)
                st.markdown("Create policy overrides for specific roles based on their purpose and function.")
                
                # Get purposes for dropdown
                purposes = self.glossary_repository.get_purposes()
                purpose_options = {p["id"]: p["name"] for p in purposes} if purposes else {}
                
                # Select role and purpose
                col1, col2 = st.columns(2)
                with col1:
                    # Add "All" option to the role selection
                    role_options = ["All"] + [f"{role_data['Name'][i]} ({role_data['Source System'][i]})" for i in range(len(role_data["ID"]))]
                    selected_role_option = st.selectbox("Select Role", options=role_options)
                    
                    # Determine if "All" is selected or a specific role
                    is_all_roles = selected_role_option == "All"
                    
                    # If a specific role is selected, get its index
                    if not is_all_roles:
                        selected_role_idx = role_options.index(selected_role_option) - 1  # Subtract 1 to account for "All"
                
                with col2:
                    selected_purpose = st.selectbox("Select Purpose for Policy", list(purpose_options.keys()), 
                                                   format_func=lambda x: purpose_options.get(x, ""))
                
                # Create a session state to store editable policy values
                if 'edited_policies' not in st.session_state:
                    st.session_state.edited_policies = {
                        'usage': {},
                        'retention': {},
                        'security': {}
                    }
                
                # Process based on role selection
                if len(role_data["ID"]) > 0 and selected_purpose:
                    # Set role ID and name based on selection
                    if is_all_roles:
                        selected_role_id = None
                        selected_role_name = "All Roles"
                    else:
                        selected_role_id = role_data["ID"][selected_role_idx]
                        selected_role_name = role_data["Name"][selected_role_idx]
                    
                    # Get policies
                    policies = self.glossary_repository.get_policies()
                    
                    # Display a message indicating what we're showing
                    if is_all_roles:
                        st.info(f"Showing purpose-level policies for {purpose_options.get(selected_purpose, '')}")
                    else:
                        st.info(f"Showing role-specific policies for {selected_role_name} with purpose {purpose_options.get(selected_purpose, '')}")
                    
                    # Get and display existing usage policies with edit options
                    access_policies = [p for p in policies if p["policy_type"] == "Access Control"]
                    if access_policies:
                        st.write("**Usage Policies:**")
                        for policy in access_policies:
                            # If "All" is selected, show purpose-level policies
                            # Otherwise, check for role-specific overrides first
                            if not is_all_roles:
                                # Check if there are role-specific overrides
                                role_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_usages(
                                    external_role_id=selected_role_id
                                )
                                
                                if role_overrides:
                                    # Filter overrides for the selected purpose and policy
                                    filtered_overrides = []
                                    for override in role_overrides:
                                        if override.get("purpose_id") == selected_purpose and override.get("policy_id") == policy['id']:
                                            filtered_overrides.append(override)
                                    
                                    if filtered_overrides:
                                        st.write(f"Policy: {policy['name']} (Role Override)")
                                        usage_policies = filtered_overrides
                                    else:
                                        # Fall back to purpose-level policies if no role overrides for this purpose/policy
                                        usage_policies = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                                            policy_id=policy['id'], purpose_id=selected_purpose
                                        )
                                        if usage_policies:
                                            st.write(f"Policy: {policy['name']} (Purpose Level)")
                                else:
                                    # No role overrides, show purpose-level policies
                                    usage_policies = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                                        policy_id=policy['id'], purpose_id=selected_purpose
                                    )
                                    if usage_policies:
                                        st.write(f"Policy: {policy['name']} (Purpose Level)")
                            else:
                                # "All" is selected, show purpose-level policies
                                usage_policies = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                                    policy_id=policy['id'], purpose_id=selected_purpose
                                )
                                if usage_policies:
                                    st.write(f"Policy: {policy['name']} (Purpose Level)")
                            
                            # Continue with displaying the policies if we have any
                            if 'usage_policies' in locals() and usage_policies:
                                # Create an expander for each policy to allow editing
                                with st.expander("Edit Usage Policy Overrides"):
                                    for idx, usage_policy in enumerate(usage_policies):
                                        st.write(f"**{usage_policy['data_element_name']} - {usage_policy['operation']}**")
                                        
                                        # Create a unique key for this policy
                                        policy_key = f"usage_{policy['id']}_{usage_policy['data_element_name']}_{usage_policy['operation']}"
                                        
                                        # Allow editing allowed status
                                        allowed = st.checkbox(
                                            "Allowed", 
                                            value=usage_policy["allowed"],
                                            key=f"{policy_key}_allowed"
                                        )
                                        
                                        # Allow editing restrictions
                                        restrictions = st.text_input(
                                            "Restrictions", 
                                            value=usage_policy["restrictions"] or "",
                                            key=f"{policy_key}_restrictions"
                                        )
                                        
                                        # Store the edited values
                                        if policy_key not in st.session_state.edited_policies['usage']:
                                            st.session_state.edited_policies['usage'][policy_key] = {
                                                'ppde_id': None,  # Will be set when creating overrides
                                                'data_element_name': usage_policy['data_element_name'],
                                                'operation': usage_policy['operation'],
                                                'allowed': allowed,
                                                'restrictions': restrictions,
                                                'policy_id': policy['id']
                                            }
                                        else:
                                            st.session_state.edited_policies['usage'][policy_key]['allowed'] = allowed
                                            st.session_state.edited_policies['usage'][policy_key]['restrictions'] = restrictions
                                        
                                        st.markdown("---")
                                
                                # Display the original policies in a table
                                usage_df = pd.DataFrame(usage_policies)
                                st.dataframe(usage_df[["data_element_name", "operation", "allowed", "restrictions"]], use_container_width=True)
                    
                    # Get and display existing retention policies with edit options
                    retention_policies = [p for p in policies if p["policy_type"] == "Retention"]
                    if retention_policies:
                        st.write("**Retention Policies:**")
                        for policy in retention_policies:
                            # If "All" is selected, show purpose-level policies
                            # Otherwise, check for role-specific overrides first
                            if not is_all_roles:
                                # Check if there are role-specific overrides
                                role_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_retentions(
                                    external_role_id=selected_role_id
                                )
                                
                                if role_overrides:
                                    # Filter overrides for the selected purpose and policy
                                    filtered_overrides = []
                                    for override in role_overrides:
                                        if override.get("purpose_id") == selected_purpose and override.get("policy_id") == policy['id']:
                                            filtered_overrides.append(override)
                                    
                                    if filtered_overrides:
                                        st.write(f"Policy: {policy['name']} (Role Override)")
                                        ret_policies = filtered_overrides
                                    else:
                                        # Fall back to purpose-level policies if no role overrides for this purpose/policy
                                        ret_policies = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                                            policy_id=policy['id'], purpose_id=selected_purpose
                                        )
                                        if ret_policies:
                                            st.write(f"Policy: {policy['name']} (Purpose Level)")
                                else:
                                    # No role overrides, show purpose-level policies
                                    ret_policies = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                                        policy_id=policy['id'], purpose_id=selected_purpose
                                    )
                                    if ret_policies:
                                        st.write(f"Policy: {policy['name']} (Purpose Level)")
                            else:
                                # "All" is selected, show purpose-level policies
                                ret_policies = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                                    policy_id=policy['id'], purpose_id=selected_purpose
                                )
                                if ret_policies:
                                    st.write(f"Policy: {policy['name']} (Purpose Level)")
                                    
                            # Continue with displaying the policies if we have any
                            if 'ret_policies' in locals() and ret_policies:
                                
                                # Create an expander for each policy to allow editing
                                with st.expander("Edit Retention Policy Overrides"):
                                    for idx, ret_policy in enumerate(ret_policies):
                                        st.write(f"**{ret_policy['data_element_name']}**")
                                        
                                        # Create a unique key for this policy
                                        policy_key = f"retention_{policy['id']}_{ret_policy['data_element_name']}"
                                        
                                        # Allow editing retention period
                                        retention_period = st.text_input(
                                            "Retention Period", 
                                            value=ret_policy["retention_period"] or "",
                                            key=f"{policy_key}_period"
                                        )
                                        
                                        # Allow editing retention basis
                                        retention_basis = st.text_input(
                                            "Retention Basis", 
                                            value=ret_policy["retention_basis"] or "",
                                            key=f"{policy_key}_basis"
                                        )
                                        
                                        # Store the edited values
                                        if policy_key not in st.session_state.edited_policies['retention']:
                                            st.session_state.edited_policies['retention'][policy_key] = {
                                                'ppde_id': None,  # Will be set when creating overrides
                                                'data_element_name': ret_policy['data_element_name'],
                                                'retention_period': retention_period,
                                                'retention_basis': retention_basis,
                                                'policy_id': policy['id']
                                            }
                                        else:
                                            st.session_state.edited_policies['retention'][policy_key]['retention_period'] = retention_period
                                            st.session_state.edited_policies['retention'][policy_key]['retention_basis'] = retention_basis
                                        
                                        st.markdown("---")
                                
                                # Display the original policies in a table
                                ret_df = pd.DataFrame(ret_policies)
                                st.dataframe(ret_df[["data_element_name", "retention_period", "retention_basis"]], use_container_width=True)
                    
                    # Get and display existing security policies with edit options
                    security_policies = [p for p in policies if p["policy_type"] == "Security"]
                    if security_policies:
                        st.write("**Security Policies:**")
                        for policy in security_policies:
                            # If "All" is selected, show purpose-level policies
                            # Otherwise, check for role-specific overrides first
                            if not is_all_roles:
                                # Check if there are role-specific overrides
                                role_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_security(
                                    external_role_id=selected_role_id
                                )
                                
                                if role_overrides:
                                    # Filter overrides for the selected purpose and policy
                                    filtered_overrides = []
                                    for override in role_overrides:
                                        if override.get("purpose_id") == selected_purpose and override.get("policy_id") == policy['id']:
                                            filtered_overrides.append(override)
                                    
                                    if filtered_overrides:
                                        st.write(f"Policy: {policy['name']} (Role Override)")
                                        sec_policies = filtered_overrides
                                    else:
                                        # Fall back to purpose-level policies if no role overrides for this purpose/policy
                                        sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                            policy_id=policy['id'], purpose_id=selected_purpose
                                        )
                                        if sec_policies:
                                            st.write(f"Policy: {policy['name']} (Purpose Level)")
                                else:
                                    # No role overrides, show purpose-level policies
                                    sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                        policy_id=policy['id'], purpose_id=selected_purpose
                                    )
                                    if sec_policies:
                                        st.write(f"Policy: {policy['name']} (Purpose Level)")
                            else:
                                # "All" is selected, show purpose-level policies
                                sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                    policy_id=policy['id'], purpose_id=selected_purpose
                                )
                                if sec_policies:
                                    st.write(f"Policy: {policy['name']} (Purpose Level)")
                                    
                            # Continue with displaying the policies if we have any
                            if 'sec_policies' in locals() and sec_policies:
                                
                                # Create an expander for each policy to allow editing
                                with st.expander("Edit Security Policy Overrides"):
                                    for idx, sec_policy in enumerate(sec_policies):
                                        st.write(f"**{sec_policy['data_element_name']}**")
                                        
                                        # Create a unique key for this policy
                                        policy_key = f"security_{policy['id']}_{sec_policy['data_element_name']}"
                                        
                                        # Allow editing encryption settings
                                        encryption_required = st.checkbox(
                                            "Encryption Required", 
                                            value=sec_policy.get("encryption_required", True),
                                            key=f"{policy_key}_encryption"
                                        )
                                        
                                        # Allow editing masking settings
                                        masking_required = st.checkbox(
                                            "Masking Required", 
                                            value=sec_policy.get("masking_required", True),
                                            key=f"{policy_key}_masking"
                                        )
                                        
                                        # Store the edited values
                                        if policy_key not in st.session_state.edited_policies['security']:
                                            st.session_state.edited_policies['security'][policy_key] = {
                                                'ppde_id': None,  # Will be set when creating overrides
                                                'data_element_name': sec_policy['data_element_name'],
                                                'encryption_required': encryption_required,
                                                'masking_required': masking_required,
                                                'policy_id': policy['id']
                                            }
                                        else:
                                            st.session_state.edited_policies['security'][policy_key]['encryption_required'] = encryption_required
                                            st.session_state.edited_policies['security'][policy_key]['masking_required'] = masking_required
                                        
                                        st.markdown("---")
                                
                                # Display the original policies in a table
                                sec_df = pd.DataFrame(sec_policies)
                                st.dataframe(sec_df[["data_element_name", "encryption_required", "masking_required"]], use_container_width=True)
                
                # Update the button text based on role selection
                button_text = "Create Role Policy Overrides" if not is_all_roles else "Create Policy Overrides is disabled for 'All' selection"
                button_disabled = is_all_roles  # Disable the button if "All" is selected
                
                if st.button(button_text, key="create_overrides", disabled=button_disabled):
                    if len(role_data["ID"]) > 0 and selected_purpose and not is_all_roles:
                        selected_role_id = role_data["ID"][selected_role_idx]
                        selected_role_name = role_data["Name"][selected_role_idx]
                        
                        # Get policy purpose data elements for the selected purpose
                        policies = self.glossary_repository.get_policies()
                        for policy in policies:
                            # Get policy purpose data elements
                            policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
                                policy_id=policy['id'], purpose_id=selected_purpose
                            )
                            
                            if policy_purpose_data_elements:
                                # Create overrides for each policy purpose data element
                                for ppde in policy_purpose_data_elements:
                                    ppde_id = ppde["id"]
                                    data_element_name = ppde["data_element_name"]
                                    
                                    # Create usage overrides using edited values
                                    if policy["policy_type"] == "Access Control":
                                        operations = ["read", "write", "share"]
                                        for operation in operations:
                                            # Create a key to look up edited values
                                            policy_key = f"usage_{policy['id']}_{data_element_name}_{operation}"
                                            
                                            # Check if we have edited values for this policy
                                            if policy_key in st.session_state.edited_policies['usage']:
                                                # Use the edited values
                                                edited_policy = st.session_state.edited_policies['usage'][policy_key]
                                                allowed = edited_policy['allowed']
                                                restrictions = edited_policy['restrictions']
                                                
                                                # Update the ppde_id in the edited policy for future reference
                                                st.session_state.edited_policies['usage'][policy_key]['ppde_id'] = ppde_id
                                                
                                                # Create the override with edited values
                                                self.regulatory_metadata_repository.add_policy_override_role_purpose_data_usage(
                                                    ppde_id, selected_role_id, operation, allowed, restrictions
                                                )
                                            else:
                                                # If no edited values, use defaults
                                                allowed = True if operation == "read" else False
                                                restrictions = None if operation == "read" else "Operation restricted for this role"
                                                
                                                # Get existing usage policies to base defaults on
                                                usage_policies = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                                                    policy_id=policy['id'], purpose_id=selected_purpose
                                                )
                                                
                                                # Find matching policy
                                                for usage_policy in usage_policies:
                                                    if usage_policy["data_element_name"] == data_element_name and usage_policy["operation"] == operation:
                                                        allowed = usage_policy["allowed"]
                                                        restrictions = usage_policy["restrictions"]
                                                        break
                                                
                                                # Create the override with default values
                                                self.regulatory_metadata_repository.add_policy_override_role_purpose_data_usage(
                                                    ppde_id, selected_role_id, operation, allowed, restrictions
                                                )
                                    
                                    # Create retention override using edited values
                                    if policy["policy_type"] == "Retention":
                                        # Create a key to look up edited values
                                        policy_key = f"retention_{policy['id']}_{data_element_name}"
                                        
                                        # Check if we have edited values for this policy
                                        if policy_key in st.session_state.edited_policies['retention']:
                                            # Use the edited values
                                            edited_policy = st.session_state.edited_policies['retention'][policy_key]
                                            retention_period = edited_policy['retention_period']
                                            retention_basis = edited_policy['retention_basis']
                                            
                                            # Update the ppde_id in the edited policy for future reference
                                            st.session_state.edited_policies['retention'][policy_key]['ppde_id'] = ppde_id
                                            
                                            # Create the override with edited values
                                            self.regulatory_metadata_repository.add_policy_override_role_purpose_data_retention(
                                                ppde_id, selected_role_id, retention_period, retention_basis
                                            )
                                        else:
                                            # If no edited values, use defaults
                                            retention_period = f"{random.randint(30, 90)} days"
                                            retention_basis = "Role-specific retention requirement"
                                            
                                            # Get existing retention policies to base defaults on
                                            retention_policies = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                                                policy_id=policy["id"],
                                                purpose_id=selected_purpose,
                                                data_element_id=ppde["data_element_id"]
                                            )
                                            
                                            # Use existing policy if available
                                            if retention_policies:
                                                ret_policy = retention_policies[0]
                                                if ret_policy["retention_period"]:
                                                    retention_period = ret_policy["retention_period"]
                                                if ret_policy["retention_basis"]:
                                                    retention_basis = ret_policy["retention_basis"]
                                            
                                            # Create the override with default values
                                            self.regulatory_metadata_repository.add_policy_override_role_purpose_data_retention(
                                                ppde_id, selected_role_id, retention_period, retention_basis
                                            )
                                    
                                    # Create security override using edited values
                                    if policy["policy_type"] == "Security":
                                        # Create a key to look up edited values
                                        policy_key = f"security_{policy['id']}_{data_element_name}"
                                        
                                        # Check if we have edited values for this policy
                                        if policy_key in st.session_state.edited_policies['security']:
                                            # Use the edited values
                                            edited_policy = st.session_state.edited_policies['security'][policy_key]
                                            
                                            # Update the ppde_id in the edited policy for future reference
                                            st.session_state.edited_policies['security'][policy_key]['ppde_id'] = ppde_id
                                            
                                            # Use the edited encryption and masking settings
                                            encryption_required = edited_policy['encryption_required']
                                            masking_required = edited_policy['masking_required']
                                            
                                            # Create the override with the edited settings
                                            self.regulatory_metadata_repository.add_policy_override_role_purpose_data_security(
                                                ppde_id, selected_role_id, encryption_required, masking_required
                                            )
                                        else:
                                            # If no edited values, use default encryption and masking settings
                                            encryption_required = True
                                            masking_required = True
                                            
                                            # Get existing security policies to base defaults on
                                            sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                                policy_id=policy['id'], purpose_id=selected_purpose
                                            )
                                            
                                            # Find matching policy
                                            for sec_policy in sec_policies:
                                                if sec_policy["data_element_name"] == data_element_name:
                                                    encryption_required = sec_policy.get("encryption_required", True)
                                                    masking_required = sec_policy.get("masking_required", True)
                                                    break
                                            
                                            # Create the override with default values
                                            self.regulatory_metadata_repository.add_policy_override_role_purpose_data_security(
                                                ppde_id, selected_role_id, encryption_required, masking_required
                                            )
                        
                        st.success(f"Successfully created policy overrides for {selected_role_name}")
                    else:
                        st.warning("No roles available to create overrides for")
            else:
                st.info("No external roles have been imported yet. Import roles first to create overrides.")
        
        # Usage Policy Overrides tab
        with tabs[1]:
            st.markdown("<h5>Usage Policy Overrides</h5>", unsafe_allow_html=True)
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Usage Policy Overrides:</b><br>
                This construct allows you to define exceptions to default data usage policies for specific external roles and purposes. Use it to grant or restrict operations (read, write, share, etc.) on data elements for a given role and purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            usage_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_usage()
            if usage_overrides:
                # Create a DataFrame from the data
                df = pd.DataFrame(usage_overrides)
                
                # Check which columns exist in the dataframe
                columns_to_display = []
                column_mapping = {
                    "role_name": "Role",
                    "data_element_name": "Data Element",
                    "operation": "Operation",
                    "allowed": "Allowed",
                    "restrictions": "Restrictions",
                    "purpose_name": "Purpose"
                }
                
                for col in column_mapping.keys():
                    if col in df.columns:
                        columns_to_display.append(col)
                
                if columns_to_display:
                    # Create a DataFrame with only the columns that exist
                    display_df = df[columns_to_display]
                    
                    # Rename columns for better display
                    display_df.columns = [column_mapping[col] for col in columns_to_display]
                    
                    # Set the table style to left-align all columns
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    # If none of the expected columns exist, just display the raw data
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No role-purpose data usage overrides defined yet.")
        
        # Retention Policy Overrides tab
        with tabs[2]:
            st.markdown("<h5>Retention Policy Overrides</h5>", unsafe_allow_html=True)
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Retention Policy Overrides:</b><br>
                This construct allows you to define exceptions to default data retention policies for specific external roles and purposes. Use it to set custom retention periods for data elements for a given role and purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            retention_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_retention()
            if retention_overrides:
                # Create a DataFrame from the data
                df = pd.DataFrame(retention_overrides)
                
                # Check which columns exist in the dataframe
                columns_to_display = []
                column_mapping = {
                    "role_name": "Role",
                    "data_element_name": "Data Element",
                    "retention_period": "Retention Period",
                    "retention_basis": "Retention Basis",
                    "purpose_name": "Purpose"
                }
                
                for col in column_mapping.keys():
                    if col in df.columns:
                        columns_to_display.append(col)
                
                if columns_to_display:
                    # Create a DataFrame with only the columns that exist
                    display_df = df[columns_to_display]
                    
                    # Rename columns for better display
                    display_df.columns = [column_mapping[col] for col in columns_to_display]
                    
                    # Set the table style to left-align all columns
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    # If none of the expected columns exist, just display the raw data
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No role-purpose data retention overrides defined yet.")
        
        # Security Policy Overrides tab
        with tabs[3]:
            st.markdown("<h5>Security Policy Overrides</h5>", unsafe_allow_html=True)
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Security Policy Overrides:</b><br>
                This construct allows you to define exceptions to default data security policies for specific external roles and purposes. Use it to specify unique security requirements for a role and purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            security_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_security()
            if security_overrides:
                # Create a DataFrame from the data
                df = pd.DataFrame(security_overrides)
                
                # Check which columns exist in the dataframe
                columns_to_display = []
                column_mapping = {
                    "role_name": "Role",
                    "data_element_name": "Data Element",
                    "encryption_required": "Encryption Required",
                    "masking_required": "Masking Required",
                    "purpose_name": "Purpose"
                }
                
                for col in column_mapping.keys():
                    if col in df.columns:
                        columns_to_display.append(col)
                
                if columns_to_display:
                    # Create a DataFrame with only the columns that exist
                    display_df = df[columns_to_display]
                    
                    # Rename columns for better display
                    display_df.columns = [column_mapping[col] for col in columns_to_display]
                    
                    # Set the table style to left-align all columns
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    # If none of the expected columns exist, just display the raw data
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No role-purpose data security overrides defined yet.")
