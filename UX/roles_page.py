import streamlit as st
import pandas as pd
import random
import time

class RolesPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository, policy_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_repository = policy_repository
        
    def format_boolean_as_checkbox(self, df, boolean_columns):
        """Format boolean columns in a dataframe as checkboxes.
        
        Args:
            df: The pandas DataFrame to format
            boolean_columns: List of column names containing boolean values
            
        Returns:
            A new DataFrame with formatted boolean columns
        """
        # Create a copy to avoid modifying the original
        formatted_df = df.copy()
        
        # Format each boolean column
        for col in boolean_columns:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].apply(
                    lambda val: "✅" if val is True else "❌" if val is False else val
                )
                
        return formatted_df

    def render(self):
        """Display the External Roles page with information about imported roles."""
        # Add CSS for green expanders and blue form buttons
        st.markdown("""
        <style>
        /* Target only the expander components */
        div[data-testid="stExpander"] {
            border: 1px solid #27ae60 !important;
            border-radius: 4px !important;
            margin-bottom: 10px !important;
            background-color: #eaf7ea !important;
        }
        
        /* Target only the header of the expander */
        div[data-testid="stExpander"] > div:first-child {
            background-color: #eaf7ea !important;
            border-left: 5px solid #27ae60 !important;
        }
        
        /* Target only the content area of the expander */
        div[data-testid="stExpander"] > div:nth-child(2) {
            border-left: 5px solid #27ae60 !important;
            background-color: #eaf7ea !important;
        }
        
        /* Style for form submit buttons only */
        div[data-testid="stForm"] button[type="submit"] {
            background-color: #3498db !important;
            color: white !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: 4px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        /* Hover effect for form submit buttons */
        div[data-testid="stForm"] button[type="submit"]:hover {
            background-color: #2980b9 !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
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
            "Purpose Role",
            "Usage Policy Overrides",
            "Retention Policy Overrides",
            "Security Policy Overrides"
        ])
        
        # External Roles tab
        with tabs[0]:
            # Asset filter section
            st.markdown("<h5>External Roles by Asset</h5>", unsafe_allow_html=True)
            st.markdown("Filter external roles by the asset they belong to.")
            
            # Get all assets for the dropdown
            assets = self.glossary_repository.get_assets()
            
            # Create a dictionary mapping asset names to IDs for the selectbox
            asset_dict = {}
            for asset in assets:
                asset_id, asset_name, _ = asset
                asset_dict[asset_name] = asset_id
            
            # Create the asset filter dropdown
            asset_options = ["All Assets"] + [name for _, name, _ in assets]
            selected_asset = st.selectbox(
                "Filter by Asset:",
                options=asset_options,
                key="asset_filter"
            )
            
            # Get the selected asset ID
            selected_asset_id = None
            if selected_asset != "All Assets":
                selected_asset_id = asset_dict.get(selected_asset)
            
            # Add new external role section
            st.markdown("<h5>Add New External Role</h5>", unsafe_allow_html=True)
            st.markdown("Add a new external role to the system.")
            
            # Create columns for form and existing roles
            col1, col2 = st.columns(2)
            
            with col1:
                # Create a form for adding a new external role
                with st.form(key="add_external_role_form"):
                    role_name = st.text_input("Role Name:", key="role_name_input")
                    role_description = st.text_area("Description:", key="role_description_input")
                    source_system = st.selectbox(
                        "Source System:",
                        options=["Snowflake", "Databricks", "AWS", "Azure", "GCP", "Other"],
                        key="source_system_select"
                    )
                    source_role_name = st.text_input("Source Role Name:", key="source_role_name_input")
                    
                    # Add asset selection dropdown
                    st.markdown("<h6>Link to Asset (Optional)</h6>", unsafe_allow_html=True)
                    link_to_asset = st.checkbox("Link this role to an asset", key="link_asset_checkbox")
                    
                    asset_for_role = None
                    if link_to_asset:
                        asset_options = [name for _, name, _ in assets]
                        asset_for_role = st.selectbox(
                            "Select Asset:",
                            options=asset_options,
                            key="asset_for_role_select"
                        )
                    
                    submit_button = st.form_submit_button(label="Add External Role")
                    
                    if submit_button and role_name and source_system and source_role_name:
                        try:
                            # Get the asset ID if an asset was selected
                            asset_id = None
                            if link_to_asset and asset_for_role:
                                asset_id = asset_dict.get(asset_for_role)
                            
                            # Add the external role and get its ID
                            role_id = self.glossary_repository.add_external_role(
                                role_name, 
                                role_description, 
                                source_system, 
                                source_role_name,
                                asset_id  # Pass the asset_id directly to add_external_role
                            )
                            
                            if role_id:
                                st.success(f"Added new external role: {role_name}")
                                if link_to_asset and asset_for_role and asset_id:
                                    st.success(f"Linked role to asset: {asset_for_role}")
                                time.sleep(1)  # Short delay to show the success message
                                st.rerun()  # Refresh the page to show the new role
                            else:
                                st.warning(f"Role may already exist or could not be added")
                        except Exception as e:
                            st.error(f"Error adding external role: {str(e)}")
            
            with col2:
                # Display existing roles based on the selected asset
                st.markdown("<h5>External Roles</h5>", unsafe_allow_html=True)
                
                # Get roles based on the selected asset
                if selected_asset_id is None:
                    filtered_roles = self.glossary_repository.get_external_roles_by_asset()
                else:
                    filtered_roles = self.glossary_repository.get_external_roles_by_asset(selected_asset_id)
                
                if filtered_roles and len(filtered_roles) > 0:
                    # Create a DataFrame for display
                    columns = ['ID', 'Name', 'Description', 'Source System', 'Source Role Name', 'Asset ID']
                    if len(filtered_roles[0]) > 6:  # Check if asset_name is included
                        columns.append('Asset Name')
                    
                    df = pd.DataFrame(filtered_roles, columns=columns)
                    
                    # Drop the Asset ID column if we're already filtering by asset
                    if selected_asset_id and selected_asset_id != "all":
                        if 'Asset ID' in df.columns:
                            df = df.drop(columns=['Asset ID'])
                    
                    # Display the DataFrame
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    if selected_asset_id and selected_asset_id != "all":
                        st.info(f"No external roles found for the selected asset.")
                    else:
                        st.info("No external roles found in the system.")
        
        # Purpose Role tab
        with tabs[1]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Purpose-Role:</b><br>
                Purpose-Role mappings define which external roles are authorized to use data for specific purposes. This tab allows you to create mappings and define policy overrides for specific role-purpose combinations.
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h6>Add Purpose-Role Mapping</h6>", unsafe_allow_html=True)
                
                # Get purposes for dropdown
                purposes = self.glossary_repository.get_purposes()
                
                # Create a dictionary mapping purpose names to IDs for the selectbox
                purpose_options = {}
                for purpose in purposes:
                    purpose_id = purpose["id"]
                    purpose_name = purpose["name"]
                    purpose_options[purpose_name] = purpose_id
                
                # Get all assets for the dropdown
                assets = self.glossary_repository.get_assets()
                
                # Create a dictionary mapping asset names to IDs for the selectbox
                asset_dict = {}
                for asset in assets:
                    asset_id, asset_name, _ = asset
                    asset_dict[asset_name] = asset_id
                
                # Add "All Assets" option
                asset_options = ["All Assets"] + [name for _, name, _ in assets]
                
                # Add asset filter dropdown outside the form so it updates immediately
                st.markdown("<h6>Filter Roles by Asset</h6>", unsafe_allow_html=True)
                selected_asset = st.selectbox(
                    "Select Asset:",
                    options=asset_options,
                    key="asset_filter_select"
                )
                
                # Get the selected asset ID
                selected_asset_id = None
                if selected_asset != "All Assets":
                    selected_asset_id = asset_dict.get(selected_asset)
                
                # Get roles based on the selected asset
                if selected_asset_id is None:
                    filtered_roles = self.glossary_repository.get_external_roles_by_asset()
                else:
                    filtered_roles = self.glossary_repository.get_external_roles_by_asset(selected_asset_id)
                
                # Create role options dictionary
                role_options = {}
                for role in filtered_roles:
                    # Format: id, name, description, source_system, source_role_name, asset_id, asset_name
                    role_id, role_name = role[0], role[1]
                    role_options[role_name] = role_id
                    
                # Log the roles for debugging
                print(f"Available roles for mapping: {list(role_options.keys())}")
                
                # Create the form for adding a new purpose-role mapping
                with st.form(key="add_purpose_role_form"):
                    selected_purpose = st.selectbox(
                        "Select Purpose:",
                        options=list(purpose_options.keys()),
                        key="purpose_select"
                    )
                    
                    # Use the current_time in the key to force refresh when the page reloads
                    # This ensures newly added roles appear in the dropdown
                    selected_roles = st.multiselect(
                        "Select Roles:",
                        options=list(role_options.keys()),
                        key=f"roles_multiselect_{current_time}"
                    )
                    submit_button = st.form_submit_button(label="Add Mapping")
                    
                    if submit_button and selected_purpose and selected_roles:
                        purpose_id = purpose_options[selected_purpose]
                        for role_name in selected_roles:
                            role_id = role_options[role_name]
                            success = self.policy_repository.add_purpose_role(purpose_id, role_id)
                            if success:
                                st.success(f"Added mapping between {selected_purpose} and {role_name}")
                            else:
                                st.warning(f"Mapping between {selected_purpose} and {role_name} already exists or could not be added")
                        st.rerun()
            
            with col2:
                st.markdown("<h6>Existing Purpose-Role Mappings</h6>", unsafe_allow_html=True)
                
                # Get all purpose-role mappings
                purpose_roles = self.policy_repository.get_purpose_roles()
                
                if purpose_roles:
                    # Create a DataFrame from the data
                    df_data = []
                    for pr in purpose_roles:
                        pr_id, purpose_id, purpose_name, role_id, role_name, source_system, asset_name = pr
                        df_data.append({
                            "ID": pr_id,
                            "Purpose": purpose_name,
                            "Role": role_name,
                            "Source System": source_system,
                            "Asset": asset_name if asset_name else "N/A"
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Add a section to delete mappings
                    st.markdown("<h6>Delete Purpose-Role Mapping</h6>", unsafe_allow_html=True)
                    
                    # Create a dictionary mapping display strings to mapping IDs
                    mapping_options = {}
                    for pr in purpose_roles:
                        pr_id, _, purpose_name, _, role_name, _, _ = pr
                        mapping_options[f"{purpose_name} - {role_name}"] = pr_id
                    
                    # Create the form for deleting a purpose-role mapping
                    with st.form(key="delete_purpose_role_form"):
                        selected_mapping = st.selectbox(
                            "Select Mapping to Delete:",
                            options=list(mapping_options.keys()),
                            key="mapping_select"
                        )
                        

                        
                        delete_button = st.form_submit_button(label="Delete Mapping")
                        
                        if delete_button and selected_mapping:
                            mapping_id = mapping_options[selected_mapping]
                            success = self.policy_repository.delete_purpose_role(mapping_id)
                            if success:
                                st.success(f"Deleted mapping: {selected_mapping}")
                            else:
                                st.error(f"Failed to delete mapping: {selected_mapping}")
                            st.rerun()
                else:
                    st.info("No purpose-role mappings defined yet.")
                    
            # Policy Override functionality
            st.markdown("<h5>Policy Overrides</h5>", unsafe_allow_html=True)
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Overrides:</b><br>
                This section allows you to define exceptions to default policies for specific external roles and purposes. Select a policy and a role to override values.
            </div>
            ''', unsafe_allow_html=True)
            
            # Get purposes for dropdown
            purposes = self.glossary_repository.get_purposes()
            purpose_options = {p["id"]: p["name"] for p in purposes} if purposes else {}
            
            # Get external roles
            roles = self.glossary_repository.get_external_roles()
            
            if roles and len(roles) > 0:
                # Create role data dictionary for display
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
                if selected_purpose:
                    # Set role ID and name based on selection
                    if is_all_roles:
                        selected_role_id = None
                        selected_role_name = "All Roles"
                    else:
                        selected_role_id = role_data["ID"][selected_role_idx]
                        selected_role_name = role_data["Name"][selected_role_idx]
                    
                    # Get policies
                    policies = self.glossary_repository.get_policies()
                    
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
                                    # Get the purpose name for the selected purpose ID
                                    purpose_name = None
                                    for purpose in self.glossary_repository.get_purposes():
                                        if purpose['id'] == selected_purpose:
                                            purpose_name = purpose['name']
                                            break
                                    
                                    # For all purposes, show the data elements
                                    for idx, sec_policy in enumerate(sec_policies):
                                        st.write(f"**{sec_policy['data_element_name']}**")
                                        
                                        # Create a unique key for this policy
                                        policy_key = f"security_{policy['id']}_{sec_policy['data_element_name']}"
                                        
                                        # Allow editing encryption settings only for Default Role Assignment purpose
                                        if purpose_name == "Default Role Assignment":
                                            encryption_required = st.checkbox(
                                                "Encryption Required", 
                                                value=sec_policy.get("encryption_required", True),
                                                key=f"{policy_key}_encryption"
                                            )
                                            
                                            # Add encryption algorithm selection for Default Role Assignment purpose
                                            encryption_algorithm_options = ["AES-128", "AES-256", "AES-256-GCM"]
                                            encryption_algorithm = st.selectbox(
                                                "Encryption Algorithm",
                                                options=encryption_algorithm_options,
                                                index=encryption_algorithm_options.index(sec_policy.get("encryption_algorithm", "AES-256")) if sec_policy.get("encryption_algorithm") in encryption_algorithm_options else 1,
                                                key=f"{policy_key}_encryption_algorithm"
                                            )
                                            
                                            st.write("Encryption settings can only be modified for the Default Role Assignment purpose.")
                                        else:
                                            # Display encryption as read-only for other purposes
                                            st.write(f"Encryption Required: {sec_policy.get('encryption_required', True)} (controlled by Default Role Assignment purpose)")
                                            if sec_policy.get("encryption_algorithm"):
                                                st.write(f"Encryption Algorithm: {sec_policy.get('encryption_algorithm')} (controlled by Default Role Assignment purpose)")
                                            # Store the existing encryption value to maintain it
                                            encryption_required = sec_policy.get("encryption_required", True)
                                            encryption_algorithm = None  # Will be fetched from Default Role Assignment purpose
                                        
                                        # Allow editing masking settings for all purposes
                                        masking_required = st.checkbox(
                                            "Masking Required", 
                                            value=sec_policy.get("masking_required", True),
                                            key=f"{policy_key}_masking"
                                        )
                                        
                                        # Add masking format input field for all purposes
                                        masking_format = st.text_input(
                                            "Masking Format",
                                            value=sec_policy.get("masking_format", ""),
                                            key=f"{policy_key}_masking_format",
                                            help="Specify the format for masking (e.g., 'xxxx@####.com' for emails, '###-##-####' for SSNs)"
                                        )
                                        
                                        # Store the edited values
                                        if policy_key not in st.session_state.edited_policies['security']:
                                            st.session_state.edited_policies['security'][policy_key] = {
                                                'ppde_id': None,  # Will be set when creating overrides
                                                'data_element_name': sec_policy['data_element_name'],
                                                'encryption_required': encryption_required,
                                                'encryption_algorithm': encryption_algorithm if purpose_name == "Default Role Assignment" else None,
                                                'masking_required': masking_required,
                                                'masking_format': masking_format if masking_format else None,
                                                'policy_id': policy['id']
                                            }
                                        else:
                                            st.session_state.edited_policies['security'][policy_key]['encryption_required'] = encryption_required
                                            if purpose_name == "Default Role Assignment":
                                                st.session_state.edited_policies['security'][policy_key]['encryption_algorithm'] = encryption_algorithm
                                            st.session_state.edited_policies['security'][policy_key]['masking_required'] = masking_required
                                            st.session_state.edited_policies['security'][policy_key]['masking_format'] = masking_format if masking_format else None
                                        
                                        st.markdown("---")
                                
                                # Display the original policies in a table
                                sec_df = pd.DataFrame(sec_policies)
                                
                                # Define columns to display, including the new ones
                                display_columns = ["data_element_name", "encryption_required", "encryption_algorithm", "masking_required", "masking_format"]
                                
                                # Filter to only include columns that exist in the dataframe
                                available_columns = [col for col in display_columns if col in sec_df.columns]
                                
                                # Create a copy of the dataframe with the selected columns
                                display_df = sec_df[available_columns].copy()
                                
                                # Rename columns for better display
                                column_mapping = {
                                    "data_element_name": "Data Element",
                                    "encryption_required": "Encryption Required",
                                    "encryption_algorithm": "Encryption Algorithm",
                                    "masking_required": "Masking Required",
                                    "masking_format": "Masking Format"
                                }
                                display_df.columns = [column_mapping[col] for col in available_columns]
                                
                                # Format boolean columns as checkboxes
                                boolean_columns = ["Encryption Required", "Masking Required"]
                                formatted_df = self.format_boolean_as_checkbox(display_df, boolean_columns)
                                
                                # Display the dataframe with formatting
                                st.dataframe(formatted_df, use_container_width=True)
                
                # Update the button text based on role selection
                button_text = "Create Role Policy Overrides" if not is_all_roles else "Create Policy Overrides is disabled for 'All' selection"
                button_disabled = is_all_roles  # Disable the button if "All" is selected
                
                # Ensure the policy override tables exist with the correct structure
                try:
                    # Create the security policy overrides table
                    self.regulatory_metadata_repository.create_policy_override_role_purpose_data_security_table()
                    print("DEBUG - Security policy overrides table created or verified")
                except Exception as e:
                    print(f"ERROR creating security policy overrides table: {e}")
                
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
                                                try:
                                                    self.regulatory_metadata_repository.add_policy_override_role_purpose_data_usage(
                                                        ppde_id, selected_role_id, operation, allowed, restrictions
                                                    )
                                                    # Explicitly commit after each override
                                                    self.regulatory_metadata_repository.connection.commit()
                                                except Exception as e:
                                                    print(f"Error creating usage policy override: {e}")
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
                                                try:
                                                    self.regulatory_metadata_repository.add_policy_override_role_purpose_data_usage(
                                                        ppde_id, selected_role_id, operation, allowed, restrictions
                                                    )
                                                    # Explicitly commit after each override
                                                    self.regulatory_metadata_repository.connection.commit()
                                                except Exception as e:
                                                    print(f"Error creating default usage policy override: {e}")
                                    
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
                                            try:
                                                self.regulatory_metadata_repository.add_policy_override_role_purpose_data_retention(
                                                    ppde_id, selected_role_id, retention_period, retention_basis
                                                )
                                                # Explicitly commit after each override
                                                self.regulatory_metadata_repository.connection.commit()
                                            except Exception as e:
                                                print(f"Error creating retention policy override: {e}")
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
                                            try:
                                                self.regulatory_metadata_repository.add_policy_override_role_purpose_data_retention(
                                                    ppde_id, selected_role_id, retention_period, retention_basis
                                                )
                                                # Explicitly commit after each override
                                                self.regulatory_metadata_repository.connection.commit()
                                            except Exception as e:
                                                print(f"Error creating default retention policy override: {e}")
                                    
                                    # Create security override using edited values
                                    if policy["policy_type"] == "Security":
                                        # Get the purpose name for the selected purpose ID
                                        purpose_name = None
                                        for purpose in self.glossary_repository.get_purposes():
                                            if purpose['id'] == selected_purpose:
                                                purpose_name = purpose['name']
                                                break
                                        
                                        # Create a key to look up edited values
                                        policy_key = f"security_{policy['id']}_{data_element_name}"
                                        
                                        # Check if we have edited values for this policy
                                        if policy_key in st.session_state.edited_policies['security']:
                                            # Use the edited values
                                            edited_policy = st.session_state.edited_policies['security'][policy_key]
                                            
                                            # Update the ppde_id in the edited policy for future reference
                                            st.session_state.edited_policies['security'][policy_key]['ppde_id'] = ppde_id
                                            
                                            # Get the masking setting from the edited policy
                                            masking_required = edited_policy['masking_required']
                                            
                                            # For encryption, only use edited value if it's the Default Role Assignment purpose
                                            if purpose_name == "Default Role Assignment":
                                                encryption_required = edited_policy['encryption_required']
                                            else:
                                                # For other purposes, get the encryption setting from the Default Role Assignment purpose
                                                default_purpose_id = None
                                                for purpose in self.glossary_repository.get_purposes():
                                                    if purpose['name'] == "Default Role Assignment":
                                                        default_purpose_id = purpose['id']
                                                        break
                                                
                                                if default_purpose_id:
                                                    # Get security policies from Default Role Assignment purpose
                                                    default_sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                                        policy_id=policy['id'], purpose_id=default_purpose_id
                                                    )
                                                    
                                                    # Find matching policy for this data element
                                                    default_encryption = True  # Default if not found
                                                    for sec_policy in default_sec_policies:
                                                        if sec_policy["data_element_name"] == data_element_name:
                                                            default_encryption = sec_policy.get("encryption_required", True)
                                                            break
                                                    
                                                    encryption_required = default_encryption
                                                else:
                                                    # Fallback to default if Default Role Assignment purpose not found
                                                    encryption_required = True
                                            
                                            # Use the edited encryption and masking settings
                                            encryption_required = edited_policy['encryption_required']
                                            masking_required = edited_policy['masking_required']
                                            encryption_algorithm = edited_policy.get('encryption_algorithm')
                                            masking_format = edited_policy.get('masking_format')
                                            
                                            # Create the override with the edited settings
                                            try:
                                                # Debug output
                                                print(f"DEBUG - Creating security override with: ppde_id={ppde_id}, role_id={selected_role_id}, encryption={encryption_required}, masking={masking_required}, algorithm={encryption_algorithm}, format={masking_format}")
                                                
                                                # Check if values are valid
                                                if ppde_id is None or selected_role_id is None:
                                                    print(f"ERROR - Invalid values for security override: ppde_id={ppde_id}, role_id={selected_role_id}")
                                                else:
                                                    # Convert boolean values if needed
                                                    encryption_required = bool(encryption_required)
                                                    masking_required = bool(masking_required)
                                                    
                                                    self.regulatory_metadata_repository.add_policy_override_role_purpose_data_security(
                                                        ppde_id, selected_role_id, encryption_required, masking_required, encryption_algorithm, masking_format
                                                    )
                                                    # Explicitly commit after each override
                                                    self.regulatory_metadata_repository.connection.commit()
                                                    print(f"DEBUG - Successfully committed security override to database")
                                            except Exception as e:
                                                print(f"Error creating security policy override: {e}")
                                                import traceback
                                                traceback.print_exc()
                                            
                                        # Handle case where there are no edited values
                                        if purpose_name == "Default Role Assignment" and policy_key not in st.session_state.edited_policies['security']:
                                            # If no edited values, use default encryption and masking settings
                                            encryption_required = True
                                            masking_required = True
                                            
                                            # Get existing security policies to base defaults on
                                            sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                                policy_id=policy['id'], purpose_id=selected_purpose
                                            )
                                            
                                            # Find matching policy for masking settings
                                            masking_required = True  # Default value
                                            for sec_policy in sec_policies:
                                                if sec_policy["data_element_name"] == data_element_name:
                                                    masking_required = sec_policy.get("masking_required", True)
                                                    break
                                            
                                            # For encryption, get settings from Default Role Assignment purpose
                                            encryption_required = True  # Default value
                                            
                                            # Only use purpose-specific encryption settings for Default Role Assignment
                                            if purpose_name == "Default Role Assignment":
                                                for sec_policy in sec_policies:
                                                    if sec_policy["data_element_name"] == data_element_name:
                                                        encryption_required = sec_policy.get("encryption_required", True)
                                                        break
                                            else:
                                                # For other purposes, get encryption from Default Role Assignment
                                                default_purpose_id = None
                                                for purpose in self.glossary_repository.get_purposes():
                                                    if purpose['name'] == "Default Role Assignment":
                                                        default_purpose_id = purpose['id']
                                                        break
                                                
                                                if default_purpose_id:
                                                    # Get security policies from Default Role Assignment purpose
                                                    default_sec_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                                        policy_id=policy['id'], purpose_id=default_purpose_id
                                                    )
                                                    
                                                    # Find matching policy for this data element
                                                    for sec_policy in default_sec_policies:
                                                        if sec_policy["data_element_name"] == data_element_name:
                                                            encryption_required = sec_policy.get("encryption_required", True)
                                                            break
                                            
                                            # Create the override with the determined values
                                            try:
                                                # Debug output
                                                print(f"DEBUG - Creating default security override with: ppde_id={ppde_id}, role_id={selected_role_id}, encryption={encryption_required}, masking={masking_required}")
                                                
                                                # Check if values are valid
                                                if ppde_id is None or selected_role_id is None:
                                                    print(f"ERROR - Invalid values for default security override: ppde_id={ppde_id}, role_id={selected_role_id}")
                                                else:
                                                    # Convert boolean values if needed
                                                    encryption_required = bool(encryption_required)
                                                    masking_required = bool(masking_required)
                                                    
                                                    # Get encryption algorithm and masking format from the security policy
                                                    encryption_algorithm = None
                                                    masking_format = None
                                                    
                                                    # Find matching policy to get algorithm and format
                                                    for sec_policy in sec_policies:
                                                        if sec_policy["data_element_name"] == data_element_name:
                                                            encryption_algorithm = sec_policy.get("encryption_algorithm")
                                                            masking_format = sec_policy.get("masking_format")
                                                            break
                                                    
                                                    self.regulatory_metadata_repository.add_policy_override_role_purpose_data_security(
                                                        ppde_id, selected_role_id, encryption_required, masking_required, encryption_algorithm, masking_format
                                                    )
                                                    # Explicitly commit after each override
                                                    self.regulatory_metadata_repository.connection.commit()
                                                    print(f"DEBUG - Successfully committed default security override to database")
                                            except Exception as e:
                                                print(f"Error creating default security policy override: {e}")
                                                import traceback
                                                traceback.print_exc()
                        
                        # Ensure all changes are committed to the database
                        try:
                            # Explicitly commit any pending transactions
                            self.regulatory_metadata_repository.connection.commit()
                            
                            # Clear the edited policies from session state to ensure fresh data on reload
                            if 'edited_policies' in st.session_state:
                                st.session_state.edited_policies = {
                                    'usage': {},
                                    'retention': {},
                                    'security': {}
                                }
                            
                            # Add a flag to indicate that overrides were just created
                            st.session_state.overrides_created = True
                            st.session_state.selected_role_id = selected_role_id
                            st.session_state.selected_purpose_id = selected_purpose
                            
                            st.success(f"Successfully created policy overrides for {selected_role_name}")
                            time.sleep(1)  # Shorter delay for better UX
                            st.rerun()  # Rerun the app to refresh all data
                        except Exception as e:
                            st.error(f"Error committing changes to database: {e}")
                    else:
                        st.warning("No roles available to create overrides for")
            else:
                st.info("No external roles have been imported yet. Import roles first to create overrides.")
        
        # Usage Policy Overrides tab
        with tabs[2]:
            # Check if we just created overrides and should show a notification
            if 'overrides_created' in st.session_state and st.session_state.overrides_created:
                st.success("Policy overrides have been created successfully. They are now visible in this tab.")
                # We don't reset the flag here as it will be shown in all tabs
                
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Usage Policy Overrides:</b><br>
                This tab displays existing usage policy overrides. To create or modify policy overrides, please use the Policy Overrides section in the Purpose Role tab.
            </div>
            ''', unsafe_allow_html=True)
            
            # Get purposes for dropdown
            purposes = self.glossary_repository.get_purposes()
            purpose_options = {"All": "All"}
            for purpose in purposes:
                purpose_id = purpose["id"]
                purpose_name = purpose["name"]
                purpose_options[purpose_id] = purpose_name
            
            # Get roles for dropdown
            roles = self.glossary_repository.get_external_roles()
            role_options = {"All": "All"}
            for role in roles:
                role_id, role_name = role[0], role[1]
                role_options[role_id] = role_name
            
            # Create filters
            col1, col2 = st.columns(2)
            with col1:
                selected_purpose = st.selectbox(
                    "Filter by Purpose:",
                    options=list(purpose_options.keys()),
                    format_func=lambda x: purpose_options.get(x, ""),
                    key="usage_purpose_filter"
                )
            
            with col2:
                selected_role = st.selectbox(
                    "Filter by Role:",
                    options=list(role_options.keys()),
                    format_func=lambda x: role_options.get(x, ""),
                    key="usage_role_filter"
                )
                
            # Get and display filtered usage policy overrides
            usage_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_usage()
            if usage_overrides:
                # Filter the overrides based on selected purpose and role
                filtered_overrides = []
                for override in usage_overrides:
                    purpose_match = selected_purpose == "All" or override.get("purpose_id") == selected_purpose
                    role_match = selected_role == "All" or override.get("role_id") == selected_role
                    if purpose_match and role_match:
                        filtered_overrides.append(override)
                
                if filtered_overrides:
                    # Create a DataFrame from the filtered data
                    df = pd.DataFrame(filtered_overrides)
                    
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
                        
                        # Format boolean columns as checkboxes
                        boolean_columns = ["Encryption Required", "Masking Required"]
                        formatted_df = self.format_boolean_as_checkbox(display_df, boolean_columns)
                        
                        # Add a note about encryption settings for non-Default Role Assignment purposes
                        # First, check if we have the Purpose column and if there are non-Default Role Assignment purposes
                        if "Purpose" in formatted_df.columns:
                            # Add a note column to explain encryption settings
                            formatted_df["Note"] = ""
                            
                            # For each row, add a note if it's not the Default Role Assignment purpose
                            for idx, row in formatted_df.iterrows():
                                if row["Purpose"] != "Default Role Assignment" and "Encryption Required" in formatted_df.columns:
                                    formatted_df.at[idx, "Note"] = "Encryption settings controlled by Default Role Assignment purpose"
                        
                        # Set the table style to left-align all columns
                        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                    else:
                        # If none of the expected columns exist, just display the raw data
                        st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No usage policy overrides match the selected filters.")
            else:
                st.info("No role-purpose data usage overrides defined yet.")
        
        # Retention Policy Overrides tab
        with tabs[3]:
            # Check if we just created overrides and should show a notification
            if 'overrides_created' in st.session_state and st.session_state.overrides_created:
                st.success("Policy overrides have been created successfully. They are now visible in this tab.")
                # We don't reset the flag here as it will be shown in all tabs
                
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Retention Policy Overrides:</b><br>
                This tab displays existing retention policy overrides. To create or modify policy overrides, please use the Policy Overrides section in the Purpose Role tab.
            </div>
            ''', unsafe_allow_html=True)
            
            # Get purposes for dropdown
            purposes = self.glossary_repository.get_purposes()
            purpose_options = {"All": "All"}
            for purpose in purposes:
                purpose_id = purpose["id"]
                purpose_name = purpose["name"]
                purpose_options[purpose_id] = purpose_name
            
            # Get roles for dropdown
            roles = self.glossary_repository.get_external_roles()
            role_options = {"All": "All"}
            for role in roles:
                role_id, role_name = role[0], role[1]
                role_options[role_id] = role_name
            
            # Create filters
            col1, col2 = st.columns(2)
            with col1:
                selected_purpose = st.selectbox(
                    "Filter by Purpose:",
                    options=list(purpose_options.keys()),
                    format_func=lambda x: purpose_options.get(x, ""),
                    key="retention_purpose_filter"
                )
            
            with col2:
                selected_role = st.selectbox(
                    "Filter by Role:",
                    options=list(role_options.keys()),
                    format_func=lambda x: role_options.get(x, ""),
                    key="retention_role_filter"
                )
                
            # Get and display filtered retention policy overrides
            retention_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_retention()
            if retention_overrides:
                # Filter the overrides based on selected purpose and role
                filtered_overrides = []
                for override in retention_overrides:
                    purpose_match = selected_purpose == "All" or override.get("purpose_id") == selected_purpose
                    role_match = selected_role == "All" or override.get("role_id") == selected_role
                    if purpose_match and role_match:
                        filtered_overrides.append(override)
                
                if filtered_overrides:
                    # Create a DataFrame from the filtered data
                    df = pd.DataFrame(filtered_overrides)
                    
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
                        
                        # Format boolean columns as checkboxes
                        boolean_columns = ["Encryption Required", "Masking Required"]
                        formatted_df = self.format_boolean_as_checkbox(display_df, boolean_columns)
                        
                        # Add a note about encryption settings for non-Default Role Assignment purposes
                        # First, check if we have the Purpose column and if there are non-Default Role Assignment purposes
                        if "Purpose" in formatted_df.columns:
                            # Add a note column to explain encryption settings
                            formatted_df["Note"] = ""
                            
                            # For each row, add a note if it's not the Default Role Assignment purpose
                            for idx, row in formatted_df.iterrows():
                                if row["Purpose"] != "Default Role Assignment" and "Encryption Required" in formatted_df.columns:
                                    formatted_df.at[idx, "Note"] = "Encryption settings controlled by Default Role Assignment purpose"
                        
                        # Set the table style to left-align all columns
                        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                    else:
                        # If none of the expected columns exist, just display the raw data
                        st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No retention policy overrides match the selected filters.")
            else:
                st.info("No role-purpose data retention overrides defined yet.")
        
        
        # Security Policy Overrides tab
        with tabs[4]:
            # Check if we just created overrides and should show a notification
            if 'overrides_created' in st.session_state and st.session_state.overrides_created:
                st.success("Policy overrides have been created successfully. They are now visible in this tab.")
                # Reset the flag after showing the notification
                st.session_state.overrides_created = False
                
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Security Policy Overrides:</b><br>
                This tab displays existing security policy overrides. To create or modify policy overrides, please use the Policy Overrides section in the Purpose Role tab.
            </div>
            ''', unsafe_allow_html=True)
            
            # Get purposes for dropdown
            purposes = self.glossary_repository.get_purposes()
            purpose_options = {"All": "All"}
            for purpose in purposes:
                purpose_id = purpose["id"]
                purpose_name = purpose["name"]
                purpose_options[purpose_id] = purpose_name
            
            # Get roles for dropdown
            roles = self.glossary_repository.get_external_roles()
            role_options = {"All": "All"}
            for role in roles:
                role_id, role_name = role[0], role[1]
                role_options[role_id] = role_name
            
            # Create filters
            col1, col2 = st.columns(2)
            with col1:
                selected_purpose = st.selectbox(
                    "Filter by Purpose:",
                    options=list(purpose_options.keys()),
                    format_func=lambda x: purpose_options.get(x, ""),
                    key="security_purpose_filter"
                )
            
            with col2:
                selected_role = st.selectbox(
                    "Filter by Role:",
                    options=list(role_options.keys()),
                    format_func=lambda x: role_options.get(x, ""),
                    key="security_role_filter"
                )
                
            # Get and display filtered security policy overrides
            # Force refresh of data from database
            security_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_security()
            
            # If we have selected role and purpose from the session state (after creating overrides),
            # use those values for the filters
            if 'selected_role_id' in st.session_state and 'selected_purpose_id' in st.session_state:
                if st.session_state.selected_role_id is not None and st.session_state.selected_purpose_id is not None:
                    selected_role = st.session_state.selected_role_id
                    selected_purpose = st.session_state.selected_purpose_id
                    # Clear these values after using them
                    st.session_state.selected_role_id = None
                    st.session_state.selected_purpose_id = None
            
            if security_overrides:
                # Filter the overrides based on selected purpose and role
                filtered_overrides = []
                for override in security_overrides:
                    # Check if the required keys exist
                    purpose_id = override.get("purpose_id")
                    external_role_id = override.get("external_role_id")
                    
                    # More flexible matching
                    purpose_match = selected_purpose == "All" or str(purpose_id) == str(selected_purpose)
                    role_match = selected_role == "All" or str(external_role_id) == str(selected_role)
                    
                    if purpose_match and role_match:
                        filtered_overrides.append(override)
                
                if filtered_overrides:
                    # Create a DataFrame from the filtered data
                    df = pd.DataFrame(filtered_overrides)
                    
                    # Check which columns exist in the dataframe
                    columns_to_display = []
                    column_mapping = {
                        "role_name": "Role",
                        "data_element_name": "Data Element",
                        "encryption_required": "Encryption Required",
                        "encryption_algorithm": "Encryption Algorithm",
                        "masking_required": "Masking Required",
                        "masking_format": "Masking Format",
                        "purpose_name": "Purpose",
                        "policy_name": "Policy",
                        "external_role_id": "Role ID",
                        "purpose_id": "Purpose ID"
                    }
                    
                    for col in column_mapping.keys():
                        if col in df.columns:
                            columns_to_display.append(col)
                    
                    if columns_to_display:
                        # Create a DataFrame with only the columns that exist
                        display_df = df[columns_to_display]
                        
                        # Rename columns for better display
                        display_df.columns = [column_mapping[col] for col in columns_to_display]
                        
                        # Format boolean columns as checkboxes
                        boolean_columns = ["Encryption Required", "Masking Required"]
                        formatted_df = self.format_boolean_as_checkbox(display_df, boolean_columns)
                        
                        # Add a note about encryption settings for non-Default Role Assignment purposes
                        # First, check if we have the Purpose column and if there are non-Default Role Assignment purposes
                        if "Purpose" in formatted_df.columns:
                            # Add a note column to explain encryption settings
                            formatted_df["Note"] = ""
                            
                            # For each row, add a note if it's not the Default Role Assignment purpose
                            for idx, row in formatted_df.iterrows():
                                if row["Purpose"] != "Default Role Assignment" and "Encryption Required" in formatted_df.columns:
                                    formatted_df.at[idx, "Note"] = "Encryption settings controlled by Default Role Assignment purpose"
                        
                        # Set the table style to left-align all columns
                        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                    else:
                        # If none of the expected columns exist, just display the raw data
                        st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No security policy overrides match the selected filters.")
            else:
                st.info("No role-purpose data security overrides defined yet.")
