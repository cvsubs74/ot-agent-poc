import streamlit as st
import pandas as pd
import json
from datetime import datetime

class PolicyManagementJourney:
    """A user journey for managing policies, policy groups, and context-specific overrides."""
    
    def __init__(self, policy_definition_repository, glossary_repository, regulatory_metadata_repository):
        """Initialize the Policy Management Journey with required repositories."""
        self.policy_definition_repository = policy_definition_repository
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
    
    def render(self):
        """Render the Policy Management Journey page."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Management Journey</div>", unsafe_allow_html=True)
        
        # Introduction with standard Streamlit components
        st.markdown("This journey demonstrates how to manage policies based on purposes, ensuring data is protected according to its sensitivity and intended use.")
        
        # Create tabs for different sections of the journey using standard Streamlit tabs
        tabs = st.tabs(["Overview", "Policy Types", "Define Policies", "Policy Groups & Overrides"])
        
        # Render content based on selected tab
        with tabs[0]:  # Overview
            self._render_overview()
        with tabs[1]:  # Policy Types
            self._render_policy_types()
        with tabs[2]:  # Define Policies
            self._render_define_policies()
        with tabs[3]:  # Policy Groups & Overrides
            self._render_policy_groups()
    
    def _render_overview(self):
        """Render the overview of policy management."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Management Overview</h3>
        """, unsafe_allow_html=True)
        
        # Overview content
        st.write("""
        Policy management is a critical component of data governance, allowing organizations to define and enforce rules 
        for how data can be accessed, used, and retained. This journey demonstrates how to:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Key Components")
            st.markdown("""
            - **Policy Types**: Define categories of policies (Access Control, Security, Retention)
            - **Policies**: Create specific rules targeting data elements, categories, or sensitivity levels
            - **Policy Groups**: Organize related policies for easier management
            - **Context Overrides**: Apply different policies based on purpose, role, or region
            """)
        
        with col2:
            st.markdown("#### Benefits")
            st.markdown("""
            - **Consistent Governance**: Apply standardized rules across your data landscape
            - **Purpose-Based Access**: Ensure data is only used for legitimate purposes
            - **Compliance**: Meet regulatory requirements for data protection
            - **Flexibility**: Adapt policies to different contexts and requirements
            """)
        
        st.info("Navigate through the tabs above to explore different aspects of policy management.")
    
    def _render_policy_types(self):
        """Render the policy types section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Types</h3>
        <p>Understand the different types of policies available in the system.</p>
        """, unsafe_allow_html=True)
        
        # Policy types
        policy_types = [
            {
                "name": "Access Control",
                "description": "Defines who can access what data and under what conditions",
                "schema": {
                    "type": "Access Control",
                    "read": "boolean",
                    "write": "boolean",
                    "share": "boolean"
                },
                "icon": "🔒"
            },
            {
                "name": "Security",
                "description": "Specifies security measures like encryption and masking",
                "schema": {
                    "encryption_required": "boolean",
                    "encryption_algorithm": "string (optional)",
                    "masking_required": "boolean",
                    "masking_format": "string (optional)",
                    "access_logging": "boolean"
                },
                "icon": "🛡️"
            },
            {
                "name": "Retention",
                "description": "Defines how long data should be kept and when it should be deleted",
                "schema": {
                    "retention_period": "string (e.g., '7 years')",
                    "retention_trigger": "string (e.g., 'creation_date', 'last_accessed')",
                    "retention_basis": "string (e.g., 'Legal Requirement')",
                    "exceptions": "string (optional)"
                },
                "icon": "⏱️"
            }
        ]
        
        # Display policy types in expandable sections
        for policy_type in policy_types:
            with st.expander(f"{policy_type['icon']} {policy_type['name']}", expanded=True):
                st.markdown(f"**Description**: {policy_type['description']}")
                st.markdown("**Schema**:")
                schema_df = pd.DataFrame(
                    [[k, v] for k, v in policy_type['schema'].items()],
                    columns=["Property", "Type"]
                )
                st.table(schema_df)
                
                # Example JSON
                st.markdown("**Example JSON**:")
                
                # Create realistic example JSON based on policy type
                if policy_type['name'] == "Access Control":
                    example_json = json.dumps({
                        "type": "Access Control",
                        "read": True,
                        "write": False,
                        "share": False,
                        "target": {
                            "type": "data_element",
                            "id": "DE12345",
                            "name": "Customer PII"
                        },
                        "purpose": "Marketing",
                        "effective_from": "2025-01-01"
                    }, indent=2)
                elif policy_type['name'] == "Security":
                    example_json = json.dumps({
                        "type": "Security",
                        "encryption_required": True,
                        "encryption_algorithm": "AES-256",
                        "masking_required": True,
                        "masking_format": "XXXX-XXXX-XXXX-####",
                        "access_logging": True,
                        "target": {
                            "type": "sensitivity_level",
                            "id": "SL789",
                            "name": "Highly Confidential"
                        },
                        "effective_from": "2025-01-01"
                    }, indent=2)
                elif policy_type['name'] == "Retention":
                    example_json = json.dumps({
                        "type": "Retention",
                        "retention_period": "7 years",
                        "retention_trigger": "creation_date",
                        "retention_basis": "Legal Requirement",
                        "exceptions": "Litigation hold may extend retention period",
                        "target": {
                            "type": "data_category",
                            "id": "DC456",
                            "name": "Financial Records"
                        },
                        "effective_from": "2025-01-01",
                        "effective_to": "2030-01-01"
                    }, indent=2)
                
                st.code(example_json, language="json")
    
    def _render_define_policies(self):
        """Render the policy definition section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Define Policies</h3>
        <p>Create and manage policies of different types to protect your data assets.</p>
        """, unsafe_allow_html=True)
        
        # Policy creation form
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                policy_name = st.text_input("Policy Name")
                effective_from = st.date_input("Effective From", value=datetime.now().date())
            
            with col2:
                policy_description = st.text_area("Description (Optional)")
                effective_to = st.date_input("Effective To (Optional)", value=None)
            
            # Get policy types for dropdown
            policy_types = self.policy_definition_repository.get_all_policy_types() if self.policy_definition_repository else []
            
            if not policy_types:
                st.warning("No policy types available. Please define policy types first.")
                return
                
            policy_type_options = {pt["id"]: pt["name"] for pt in policy_types}
            
            # Policy type selection
            selected_policy_type_id = st.selectbox(
                "Select Policy Type",
                options=list(policy_type_options.keys()),
                format_func=lambda x: policy_type_options.get(x, "Unknown")
            )
            
            policy_type_name = policy_type_options.get(selected_policy_type_id)
            
            # Update policy name based on policy type
            if not policy_name and policy_type_name:
                policy_name = f"{policy_type_name} Policy"
            
            # Target selection tabs
            target_tab = st.radio(
                "Target Type",
                ["Data Element", "Data Category", "Sensitivity Level"],
                horizontal=True
            )
            
            # Target selection based on tab
            selected_targets = []
            selected_target_names = []
            
            if target_tab == "Data Element":
                data_elements = self.glossary_repository.get_data_elements() if self.glossary_repository else []
                
                if not data_elements:
                    st.warning("No data elements available. Please define data elements first.")
                else:
                    data_element_options = {de["id"]: de["name"] for de in data_elements}
                    
                    # Multi-select for data elements
                    selected_target_ids = st.multiselect(
                        "Select Data Elements",
                        options=list(data_element_options.keys()),
                        format_func=lambda x: data_element_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_element",
                            "id": target_id,
                            "name": data_element_options.get(target_id)
                        })
                        selected_target_names.append(data_element_options.get(target_id))
            
            elif target_tab == "Data Category":
                data_categories = self.glossary_repository.get_data_categories() if self.glossary_repository else []
                
                if not data_categories:
                    st.warning("No data categories available. Please define data categories first.")
                else:
                    data_category_options = {dc["id"]: dc["name"] for dc in data_categories}
                    
                    # Multi-select for data categories
                    selected_target_ids = st.multiselect(
                        "Select Data Categories",
                        options=list(data_category_options.keys()),
                        format_func=lambda x: data_category_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_category",
                            "id": target_id,
                            "name": data_category_options.get(target_id)
                        })
                        selected_target_names.append(data_category_options.get(target_id))
            
            elif target_tab == "Sensitivity Level":
                sensitivity_levels = self.glossary_repository.get_sensitivities() if self.glossary_repository else []
                
                if not sensitivity_levels:
                    st.warning("No sensitivity levels available. Please define sensitivity levels first.")
                else:
                    sensitivity_options = {sl["id"]: sl["name"] for sl in sensitivity_levels}
                    
                    # Multi-select for sensitivity levels
                    selected_target_ids = st.multiselect(
                        "Select Sensitivity Levels",
                        options=list(sensitivity_options.keys()),
                        format_func=lambda x: sensitivity_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "sensitivity_level",
                            "id": target_id,
                            "name": sensitivity_options.get(target_id)
                        })
                        selected_target_names.append(sensitivity_options.get(target_id))
            
            # Update policy name based on selected targets
            if selected_target_names and (not policy_name or policy_name == f"{policy_type_name} Policy"):
                if len(selected_target_names) == 1:
                    policy_name = f"{policy_type_name} Policy for {selected_target_names[0]}"
                else:
                    target_type = target_tab.replace(" Level", "")
                    policy_name = f"{policy_type_name} Policy for {len(selected_target_names)} {target_type}s"
            
            # Dynamic policy configuration based on selected policy type
            policy_config = {}
            
            if policy_type_name == "Access Control" and selected_targets:
                st.write("Set specific permissions for each selected target:")
                
                # Create a dictionary to store permissions for each target
                target_permissions = {}
                
                # Create a table-like interface for setting permissions
                for i, target in enumerate(selected_targets):
                    st.markdown(f"**{i+1}. {target['name']} ({target['type']}):**")
                    
                    cols = st.columns([3, 2, 2, 2])
                    with cols[1]:
                        read = st.checkbox("Read", value=True, key=f"read_{target['id']}", help="Allow reading/viewing the data")
                    with cols[2]:
                        write = st.checkbox("Write", value=False, key=f"write_{target['id']}", help="Allow modifying the data")
                    with cols[3]:
                        share = st.checkbox("Share", value=False, key=f"share_{target['id']}", help="Allow sharing the data with others")
                    
                    # Store permissions for this target
                    target_permissions[target['id']] = {
                        "read": read,
                        "write": write,
                        "share": share
                    }
                    
                    # Add a separator between targets
                    st.markdown("---")
                
                # Update the policy config to include per-target permissions
                policy_config = {
                    "type": "Access Control",
                    "target_permissions": target_permissions
                }
            
            elif policy_type_name == "Security":
                # Initialize default security settings
                global_encryption_required = True
                global_masking_required = False
                access_logging = True
                global_encryption_algorithm = "AES-256"
                global_masking_format = "XXXX-XXXX-XXXX-####"
                
                # Define appropriate masking formats for different data element types
                masking_formats = {
                    "Email Address": "****@****.com",
                    "Phone Number": "(XXX) XXX-####",
                    "Social Security Number": "XXX-XX-####",
                    "Credit Card Number": "XXXX-XXXX-XXXX-####",
                    "Date of Birth": "XXXX-XX-DD",
                    "Address": "*** ****** ****",
                    "Name": "**** *****",
                    "IP Address": "XXX.XXX.XXX.XXX",
                    "Bank Account Number": "XXXXXXXX####"
                }
                
                # Initialize target_security dictionary to store per-target security settings
                policy_config["target_security"] = {}
                
                # Per-target security settings
                if selected_targets:
                    st.markdown("---")
                    st.subheader("Security Settings")
                    st.write("Configure security settings for each selected target.")
                    
                    # For each target, create an expander with security settings
                    for target in selected_targets:
                        with st.expander(f"Security settings for {target['name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                target_encryption = st.checkbox(
                                    "Encryption Required", 
                                    value=global_encryption_required,
                                    key=f"encrypt_{target['id']}"
                                )
                                
                                target_masking = st.checkbox(
                                    "Masking Required", 
                                    value=global_masking_required,
                                    key=f"mask_{target['id']}"
                                )
                            
                            # Encryption algorithm if encryption is required
                            if target_encryption:
                                encryption_algo = st.text_input(
                                    "Encryption Algorithm", 
                                    value=global_encryption_algorithm or "AES-256",
                                    key=f"algo_{target['id']}"
                                )
                            else:
                                encryption_algo = None
                            
                            # Masking format if masking is required
                            if target_masking:
                                # Use data element-specific masking format if available
                                default_format = masking_formats.get(target['name'], global_masking_format)
                                masking_format = st.text_input(
                                    "Masking Format", 
                                    value=default_format,
                                    key=f"format_{target['id']}"
                                )
                            else:
                                masking_format = None
                            
                            # Store the target's security settings
                            policy_config["target_security"][target["id"]] = {
                                "encryption_required": target_encryption,
                                "encryption_algorithm": encryption_algo,
                                "masking_required": target_masking,
                                "masking_format": masking_format
                            }
                
                # Global settings (applied to targets without specific settings)
                policy_config.update({
                    "encryption_required": global_encryption_required,
                    "encryption_algorithm": global_encryption_algorithm,
                    "masking_required": global_masking_required,
                    "masking_format": global_masking_format,
                    "access_logging": access_logging
                })
            
            elif policy_type_name == "Retention":
                # Initialize default retention settings
                global_retention_period = "7 years"
                global_retention_basis = "Legal Requirement"
                global_retention_trigger = "creation_date"
                global_exceptions = ""
                
                # Initialize target_retention dictionary to store per-target retention settings
                policy_config = {"target_retention": {}}
                
                # Per-target retention settings
                if selected_targets:
                    st.markdown("---")
                    st.subheader("Retention Settings")
                    st.write("Configure retention settings for each selected target.")
                    
                    # For each target, create an expander with retention settings
                    for target in selected_targets:
                        with st.expander(f"Retention settings for {target['name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                target_retention_period = st.text_input(
                                    "Retention Period", 
                                    value=global_retention_period,
                                    key=f"period_{target['id']}"
                                )
                                
                                target_retention_basis = st.text_input(
                                    "Retention Basis", 
                                    value=global_retention_basis,
                                    key=f"basis_{target['id']}"
                                )
                            
                            with col2:
                                target_retention_trigger = st.selectbox(
                                    "Retention Trigger",
                                    options=["creation_date", "last_modified", "last_accessed", "custom_event"],
                                    key=f"trigger_{target['id']}"
                                )
                            
                            target_exceptions = st.text_area(
                                "Exceptions (Optional)", 
                                value=global_exceptions,
                                key=f"exceptions_{target['id']}"
                            )
                            
                            # Store the target's retention settings
                            policy_config["target_retention"][target["id"]] = {
                                "retention_period": target_retention_period,
                                "retention_trigger": target_retention_trigger,
                                "retention_basis": target_retention_basis,
                                "exceptions": target_exceptions
                            }
                
                # Global settings (applied to targets without specific settings)
                policy_config.update({
                    "retention_period": global_retention_period,
                    "retention_trigger": global_retention_trigger,
                    "retention_basis": global_retention_basis,
                    "exceptions": global_exceptions
                })
            
            # Preview policy before submission
            if selected_targets:
                with st.expander("Preview Policy", expanded=True):
                    
                    # Optimized JSON preview
                    st.subheader("Policy Preview")
                    
                    # Create a more concise policy representation
                    if policy_type_name == "Access Control":
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For Access Control, show a simplified version with target permissions
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            }
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                        
                        # Add target permissions in a more readable format
                        target_permissions = {}
                        for target in selected_targets:
                            perms = policy_config.get("target_permissions", {}).get(target['id'], {})
                            # Only include ID and permissions, not type (since it's specified at the top level)
                            target_permissions[target['name']] = {
                                "id": target['id'],
                                "read": perms.get("read", False),
                                "write": perms.get("write", False),
                                "share": perms.get("share", False)
                            }
                        
                        optimized_json["permissions"] = target_permissions
                    elif policy_type_name == "Security" or policy_type_name == "Retention":
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For Security/Retention policies, show a simplified version with target-specific settings
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            }
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                        
                        if policy_type_name == "Security":
                            # Add security settings in a more readable format
                            security_settings = {}
                            for target in selected_targets:
                                target_security = policy_config.get("target_security", {}).get(target['id'], {})
                                
                                # Create attribute-based security settings
                                target_settings = {
                                    "id": target['id'],
                                    "encryption": {
                                        "required": target_security.get("encryption_required", False),
                                        "algorithm": target_security.get("encryption_algorithm") if target_security.get("encryption_required", False) else None
                                    },
                                    "masking": {
                                        "required": target_security.get("masking_required", False),
                                        "format": target_security.get("masking_format") if target_security.get("masking_required", False) else None
                                    }
                                }
                                
                                security_settings[target['name']] = target_settings
                            
                            optimized_json["security_settings"] = security_settings
                        elif policy_type_name == "Retention":
                            # Add retention settings in a more readable format
                            retention_settings = {}
                            for target in selected_targets:
                                target_retention = policy_config.get("target_retention", {}).get(target['id'], {})
                                
                                # Create attribute-based retention settings
                                target_settings = {
                                    "id": target['id'],
                                    "period": target_retention.get("retention_period", policy_config.get("retention_period")),
                                    "basis": target_retention.get("retention_basis", policy_config.get("retention_basis")),
                                    "trigger": target_retention.get("retention_trigger", policy_config.get("retention_trigger")),
                                    "exceptions": target_retention.get("exceptions", policy_config.get("exceptions"))
                                }
                                
                                retention_settings[target['name']] = target_settings
                            
                            optimized_json["retention_settings"] = retention_settings
                    else:
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For other policy types, use a similar structure but with the specific config
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "targets": [
                                {
                                    "id": t["id"],
                                    "name": t["name"]
                                    # No type field here since it's specified at the top level
                                } for t in selected_targets
                            ],
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            },
                            "config": policy_config
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                    
                    # Display the optimized JSON
                    st.json(optimized_json)
            else:
                st.warning("Please select at least one target to create a policy.")
            
            # Submit button
            if st.button("Create Policy", type="primary"):
                # Validate inputs
                validation_errors = []
                
                if not policy_name or policy_name.strip() == "":
                    validation_errors.append("Policy name is required.")
                
                if not selected_targets:
                    validation_errors.append("At least one data element, category, or sensitivity level must be selected.")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    created_policies = []
                    failed_policies = []
                    
                    # Create a policy for each target
                    for target in selected_targets:
                        try:
                            # Determine target type and ID
                            data_element_id = None
                            data_category_id = None
                            sensitivity_id = None
                            
                            if target['type'] == 'data_element':
                                data_element_id = target['id']
                            elif target['type'] == 'data_category':
                                data_category_id = target['id']
                            elif target['type'] == 'sensitivity_level':
                                sensitivity_id = target['id']
                                
                            # Convert dates to string format
                            effective_from_str = effective_from.strftime('%Y-%m-%d') if effective_from else None
                            effective_to_str = effective_to.strftime('%Y-%m-%d') if effective_to else None
                                
                            # Generate a specific policy name for this target
                            target_policy_name = policy_name
                            
                            # If we're creating multiple policies, append the target name to make each unique
                            if len(selected_targets) > 1:
                                # Different naming patterns based on policy type
                                if policy_type_name == "Access Control":
                                    # For Access Control, include the permissions in the name
                                    perms = policy_config.get("target_permissions", {}).get(target['id'], {})
                                    operations = []
                                    if perms.get("read", False):
                                        operations.append("Read")
                                    if perms.get("write", False):
                                        operations.append("Write")
                                    if perms.get("share", False):
                                        operations.append("Share")
                                    
                                    operations_str = "/".join(operations) if operations else "No Access"
                                    target_policy_name = f"{policy_name} - {target['name']} ({operations_str})"
                                elif policy_type_name == "Security":
                                    # For Security, include the security measures in the name
                                    security_settings = policy_config.get("target_security", {}).get(target['id'], {})
                                    measures = []
                                    if security_settings.get("encryption_required", False):
                                        measures.append("Encrypted")
                                    if security_settings.get("masking_required", False):
                                        measures.append("Masked")
                                    
                                    measures_str = "/".join(measures) if measures else "No Security"
                                    target_policy_name = f"{policy_name} - {target['name']} ({measures_str})"
                                elif policy_type_name == "Retention":
                                    # For Retention, include the retention period in the name
                                    retention_settings = policy_config.get("target_retention", {}).get(target['id'], {})
                                    retention_period = retention_settings.get("retention_period", policy_config.get("retention_period", "7 years"))
                                    target_policy_name = f"{policy_name} - {target['name']} ({retention_period})"
                                else:
                                    # For other policy types, just append the target name
                                    target_policy_name = f"{policy_name} - {target['name']}"
                            
                            # Create policy in repository
                            policy_id = self.policy_definition_repository.create_policy(
                                policy_type_id=selected_policy_type_id,
                                data_element_id=data_element_id,
                                data_category_id=data_category_id,
                                sensitivity_id=sensitivity_id,
                                policy_config=policy_config,
                                effective_from=effective_from_str,
                                effective_to=effective_to_str,
                                name=target_policy_name
                            )
                                
                            if policy_id:
                                created_policies.append({
                                    'id': policy_id,
                                    'target_name': target['name'],
                                    'target_type': target['type']
                                })
                            else:
                                failed_policies.append({
                                    'target_name': target['name'],
                                    'target_type': target['type']
                                })
                        except Exception as e:
                            st.error(f"Error creating policy for {target['name']}: {str(e)}")
                            failed_policies.append({
                                'target_name': target['name'],
                                'target_type': target['type'],
                                'error': str(e)
                            })
                    
                    # Show results
                    if created_policies:
                        st.success(f"Successfully created {len(created_policies)} policies!")
                        
                        # Show created policies in a table
                        created_df = pd.DataFrame(
                            [[p['id'], p['target_name'], p['target_type']] for p in created_policies],
                            columns=["Policy ID", "Target Name", "Target Type"]
                        )
                        st.dataframe(created_df, use_container_width=True)
                    
                    if failed_policies:
                        st.error(f"Failed to create {len(failed_policies)} policies.")
                        for failed in failed_policies:
                            st.write(f"- {failed['target_name']} ({failed['target_type']}): {failed.get('error', 'Unknown error')}")
                    
                    # Refresh the policy list
                    st.rerun()
        
        # Existing policies section
        st.markdown("---")
        st.subheader("Existing Policies")
        
        # Get policies
        policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
        
        if not policies:
            st.info("No policies defined yet.")
        else:
            # Display policies as expandable JSON objects
            for i, policy in enumerate(policies):
                # Get policy name (use the dedicated name field if available)
                policy_name = policy.get("name")
                
                # Determine target name and type
                target_name = policy.get("data_element_name") or policy.get("data_category_name") or policy.get("sensitivity_name") or "Global"
                target_type = "data_element" if policy.get("data_element_name") else \
                             "data_category" if policy.get("data_category_name") else \
                             "sensitivity_level" if policy.get("sensitivity_name") else "global"
                
                # Parse policy config to extract read/write/share settings
                policy_config = {}
                if policy.get("policy_config"):
                    try:
                        if isinstance(policy.get("policy_config"), str):
                            policy_config = json.loads(policy.get("policy_config"))
                        else:
                            policy_config = policy.get("policy_config")
                    except:
                        policy_config = {}
                
                # Create a clean policy representation
                policy_json = {
                    "id": policy.get("id"),
                    "name": policy.get("name", "Unknown"),
                    "type": policy.get("policy_type_name", "Unknown"),
                    "target_type": target_type,
                    "target": {
                        "id": policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id"),
                        "name": target_name
                    },
                    "effective_dates": {
                        "from": str(policy.get("effective_from", "Immediately")),
                        "to": str(policy.get("effective_to", "Indefinite"))
                    }
                }
                
                # Add permissions for Access Control policies
                if policy.get("policy_type_name") == "Access Control":
                    # Extract permissions from policy config
                    permissions = {
                        "read": policy_config.get("read", False),
                        "write": policy_config.get("write", False),
                        "share": policy_config.get("share", False)
                    }
                    
                    # If using target_permissions structure
                    target_id = policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id")
                    if policy_config.get("target_permissions") and policy_config["target_permissions"].get(target_id):
                        target_perms = policy_config["target_permissions"].get(target_id)
                        permissions = {
                            "read": target_perms.get("read", False),
                            "write": target_perms.get("write", False),
                            "share": target_perms.get("share", False)
                        }
                    
                    policy_json["permissions"] = permissions
                # Add security settings for Security policies
                elif policy.get("policy_type_name") == "Security":
                    # Extract global security settings
                    security_settings = {
                        "encryption_required": policy_config.get("encryption_required", False),
                        "encryption_algorithm": policy_config.get("encryption_algorithm"),
                        "masking_required": policy_config.get("masking_required", False),
                        "masking_format": policy_config.get("masking_format"),
                        "access_logging": policy_config.get("access_logging", False)
                    }
                    
                    # If using target_security structure
                    target_id = policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id")
                    if policy_config.get("target_security") and policy_config["target_security"].get(target_id):
                        target_security = policy_config["target_security"].get(target_id)
                        security_settings = {
                            "encryption_required": target_security.get("encryption_required", False),
                            "encryption_algorithm": target_security.get("encryption_algorithm"),
                            "masking_required": target_security.get("masking_required", False),
                            "masking_format": target_security.get("masking_format"),
                            "access_logging": policy_config.get("access_logging", False)  # Global setting
                        }
                    
                    policy_json["security_settings"] = security_settings
                else:
                    # For other policy types, include the full config
                    policy_json["config"] = policy_config
                
                # Display the policy with an expander
                with st.expander(f"{policy_json['name']} ({target_name})", expanded=i==0):
                    st.json(policy_json)
    
    def _render_policy_groups(self):
        """Render the policy groups and overrides section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Groups & Overrides</h3>
        <p>Organize related policies into groups and define context-specific overrides.</p>
        """, unsafe_allow_html=True)
        
        # Two columns layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Policy Groups
            st.subheader("Policy Groups")
            
            # Create new policy group form
            with st.expander("Create New Policy Group"):
                group_name = st.text_input("Group Name", key="group_name_input")
                group_description = st.text_area("Description", key="group_desc_input")
                group_version = st.text_input("Version", value="1.0", key="group_version_input")
                is_active = st.checkbox("Active", value=True, key="group_active_checkbox")
                
                if st.button("Create Group", key="create_group_btn"):
                    if self.policy_definition_repository and group_name:
                        self.policy_definition_repository.create_policy_group(group_name, group_description, group_version, is_active)
                        st.success("Policy group created successfully!")
                        # Rerun the app to refresh the UI
                        st.experimental_rerun()
                    elif not group_name:
                        st.warning("Please enter a group name.")
            
            # View Policy Group Contents
            st.markdown("---")
            st.subheader("View Policy Group Contents")
            
            # Get all policy groups for the dropdown
            policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
            
            if not policy_groups:
                st.info("No policy groups defined yet.")
            else:
                # Create a dropdown to select a policy group
                group_options = {g["id"]: f"{g['name']} (v{g['version']})" for g in policy_groups}
                selected_group_id = st.selectbox(
                    "Select Policy Group",
                    options=list(group_options.keys()),
                    format_func=lambda x: group_options.get(x, "Unknown"),
                    key="view_policy_group_select"
                )
                
                # Display the policies in the selected group
                if selected_group_id:
                    # Get the selected group details
                    selected_group = next((g for g in policy_groups if g["id"] == selected_group_id), None)
                    
                    if selected_group:
                        st.write(f"**Description:** {selected_group['description']}")
                        st.write(f"**Status:** {'Active' if selected_group['is_active'] else 'Inactive'}")
                        
                        # Get policies in the group
                        group_policies = self.policy_definition_repository.get_policies_in_group(selected_group_id) if self.policy_definition_repository else []
                        
                        if not group_policies:
                            st.info(f"No policies in group '{selected_group['name']}' yet.")
                        else:
                            # Display policies in a table
                            st.write(f"**Policies in {selected_group['name']}:**")
                            
                            # Create a DataFrame for the policies
                            policy_data = []
                            for p in group_policies:
                                target_name = p.get("data_element_name") or p.get("data_category_name") or p.get("sensitivity_name") or "Global"
                                policy_data.append({
                                    "Policy Type": p.get("policy_type_name", "Unknown"),
                                    "Target": target_name,
                                    "Target System": p.get("target_system", ""),
                                })
                            
                            if policy_data:
                                policy_df = pd.DataFrame(policy_data)
                                st.dataframe(policy_df, use_container_width=True)
            
            # Manage Policy Groups
            st.markdown("---")
            st.subheader("Manage Policy Groups")
            
            if not policy_groups:
                st.info("No policy groups defined yet.")
            else:
                for group in policy_groups:
                    with st.container():
                        st.markdown(f"### {group['name']} (v{group['version']})")
                        
                        # Group details
                        st.write(f"**Description:** {group['description']}")
                        st.write(f"**Status:** {'Active' if group['is_active'] else 'Inactive'}")
                        
                        # Add policy to group
                        with st.expander("Add Policies to this Group"):
                            # Get all policies
                            all_policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
                            
                            if not all_policies:
                                st.warning("No policies available. Please create policies first.")
                            else:
                                policy_options = {p["id"]: f"{p.get('policy_type_name', 'Unknown')} - {p.get('data_element_name') or p.get('data_category_name') or p.get('sensitivity_name') or 'Global'}" for p in all_policies}
                                
                                selected_policy_ids = st.multiselect(
                                    "Select Policies to Add",
                                    options=list(policy_options.keys()),
                                    format_func=lambda x: policy_options.get(x, "Unknown"),
                                    key=f"group_{group['id']}_policy_select"
                                )
                                
                                target_system = st.text_input("Target System (Optional)", key=f"group_{group['id']}_target_input")
                                
                                add_button = st.button("Add Policies", key=f"group_{group['id']}_add_policy_btn")
                                if add_button and selected_policy_ids:
                                    # Add each selected policy to the group
                                    for policy_id in selected_policy_ids:
                                        if self.policy_definition_repository:
                                            self.policy_definition_repository.add_policy_to_group(group['id'], policy_id, target_system)
                                    
                                    st.success(f"{len(selected_policy_ids)} policies added to group {group['name']}")
                                    # Rerun the app to refresh the UI
                                    st.experimental_rerun()
                                elif add_button and not selected_policy_ids:
                                    st.warning("Please select at least one policy to add to the group.")
                        
                        # Delete group button
                        if st.button("Delete Group", key=f"delete_group_{group['id']}_btn"):
                            if self.policy_definition_repository:
                                self.policy_definition_repository.delete_policy_group(group['id'])
                                st.success("Policy group deleted successfully!")
                                # Rerun the app to refresh the UI
                                st.experimental_rerun()
                            else:
                                st.error("Failed to delete policy group.")
            
            # Create new context override form
            with st.expander("Create New Override"):
                # Get policy groups
                policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
                
                if not policy_groups:
                    st.warning("No policy groups available. Please create a policy group first.")
                else:
                    policy_group_options = {pg["id"]: pg["name"] for pg in policy_groups}
                    
                    selected_policy_group_id = st.selectbox(
                        "Select Policy Group",
                        options=list(policy_group_options.keys()),
                        format_func=lambda x: policy_group_options.get(x, "Unknown"),
                        key="override_group_select"
                    )
                    
                    # Context selectors
                    st.markdown("### Context Criteria")
                    
                    # Purpose selector
                    purposes = self.glossary_repository.get_purposes() if self.glossary_repository else []
                    
                    if purposes:
                        purpose_options = {p["id"]: p["name"] for p in purposes}
                        selected_purpose_id = st.selectbox(
                            "Select Purpose (Optional)",
                            options=[None] + list(purpose_options.keys()),
                            format_func=lambda x: purpose_options.get(x, "Any") if x else "Any",
                            key="override_purpose_select"
                        )
                    else:
                        st.info("No purposes available.")
                        selected_purpose_id = None
                    
                    # Role selector
                    roles = self.glossary_repository.get_external_roles() if self.glossary_repository else []
                    
                    if roles:
                        # Handle roles as tuples (id, name, description, source_system, source_role_name, asset_id)
                        role_options = {r[0]: r[1] for r in roles}  # Use index 0 for id, index 1 for name
                        selected_role_id = st.selectbox(
                            "Select Role (Optional)",
                            options=[None] + list(role_options.keys()),
                            format_func=lambda x: role_options.get(x, "Any") if x else "Any",
                            key="override_role_select"
                        )
                    else:
                        st.info("No roles available.")
                        selected_role_id = None
                    
                    # Region selector
                    regions = self.policy_definition_repository.get_all_regions() if self.policy_definition_repository else []
                    
                    if regions:
                        region_options = {r["id"]: r["name"] for r in regions}
                        selected_region_id = st.selectbox(
                            "Select Region (Optional)",
                            options=[None] + list(region_options.keys()),
                            format_func=lambda x: region_options.get(x, "Any") if x else "Any",
                            key="override_region_select"
                        )
                    else:
                        st.info("No regions available.")
                        selected_region_id = None
                    
                    # Context tags
                    context_tags = st.text_area("Context Tags (JSON format)", key="context_tags_textarea")
                    
                    # Priority and dates
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        manual_priority = st.number_input("Priority", min_value=0, max_value=100, value=10, key="priority_input")
                        effective_from = st.date_input("Effective From", value=datetime.now().date(), key="override_from_date")
                    
                    with col2:
                        is_active = st.checkbox("Active", value=True, key="override_active_checkbox")
                        effective_to = st.date_input("Effective To (Optional)", value=None, key="override_to_date")
                    
                    if st.button("Create Override", key="create_override_btn"):
                        if not selected_group_id:
                            st.error("Please select a policy group.")
                        else:
                            # Format dates properly for database
                            from_date = effective_from.strftime('%Y-%m-%d') if effective_from else None
                            to_date = effective_to.strftime('%Y-%m-%d') if effective_to else None
                            
                            # Validate and parse context tags if provided
                            tags_json = None
                            if context_tags:
                                try:
                                    tags_json = json.dumps(json.loads(context_tags))
                                except json.JSONDecodeError:
                                    st.error("Context tags must be valid JSON. Please check the format.")
                                    return
                            
                            # Create the context policy group
                            if self.policy_definition_repository:
                                result = self.policy_definition_repository.create_context_policy_group(
                                    purpose_id=selected_purpose_id,
                                    external_role_id=selected_role_id,
                                    region_id=selected_region_id,
                                    policy_group_id=selected_group_id,
                                    manual_priority=manual_priority,
                                    context_tags=tags_json,
                                    effective_from=from_date,
                                    effective_to=to_date
                                )
                                
                                if result:
                                    st.success("Context override created successfully!")
                                    # Rerun the app to refresh the UI
                                    st.rerun()
                                else:
                                    st.error("Failed to create context override. Please check the logs for details.")
                            else:
                                st.error("Repository not available. Cannot create context override.")
            
            # Existing context overrides
            st.markdown("---")
            st.subheader("Existing Overrides")
            
            context_policy_groups = self.policy_definition_repository.get_all_context_policy_groups() if self.policy_definition_repository else []
            
            if not context_policy_groups:
                st.info("No context overrides defined yet.")
            else:
                for cpg in context_policy_groups:
                    with st.container():
                        st.markdown(f"### Override for {cpg.get('policy_group_name', 'Unknown Group')}")
                        
                        # Context criteria
                        criteria = []
                        if cpg.get('purpose_name'):
                            criteria.append(f"Purpose: {cpg.get('purpose_name')}")
                        if cpg.get('external_role_name'):
                            criteria.append(f"Role: {cpg.get('external_role_name')}")
                        if cpg.get('region_name'):
                            criteria.append(f"Region: {cpg.get('region_name')}")
                        
                        if criteria:
                            st.markdown(", ".join(criteria))
                        else:
                            st.markdown("Global override (no specific context)")
                        
                        # Details
                        cols = st.columns([2, 2, 1])
                        with cols[0]:
                            st.markdown(f"Priority: {cpg.get('manual_priority', 0)}")
                        with cols[1]:
                            st.markdown(f"Effective: {cpg.get('effective_from', 'Always')} to {cpg.get('effective_to', 'Indefinite')}")
                        with cols[2]:
                            if st.button("Delete", key=f"delete_override_{cpg['id']}_btn"):
                                st.warning("Override deleted")
