import streamlit as st
import pandas as pd
from components.DDLGenerator import DDLGenerator
from components.SimpleIdentifierMatcher import SimpleIdentifierMatcher
from components.JSONGenerator import JSONGenerator

class AssetsPage:
    def __init__(self, inventory_repository, glossary_repository, obligation_repository, sensitivity_inference, catalog_repository, regulatory_metadata_repository, asset_policy_inference=None):
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.sensitivity_inference = sensitivity_inference
        self.catalog_repository = catalog_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.asset_policy_inference = asset_policy_inference
        self.ddl_generator = DDLGenerator()
        self.identifier_matcher = SimpleIdentifierMatcher()
        self.json_generator = JSONGenerator(glossary_repository, catalog_repository)
        
    # The _build_column_based_json_from_df method has been refactored to the JSONGenerator class
        
    # The _find_identifier_columns method has been moved to the IdentifierMatcher class

    def render(self):
        """Render the Assets page with asset inventory, filtering, and inference actions."""
        # Add CSS for green expanders - targeting only the expander elements
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
        </style>
        """, unsafe_allow_html=True)
        
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


        assets = self.inventory_repository.get_assets()
        if not assets:
            st.warning("No assets available in the database.")
            return
        asset_data_elements = self.inventory_repository.get_asset_data_elements()
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
        
        filtered_assets = assets
        
        asset_data = {
            "Asset": [],
            "Description": [],
            "Type": [],
            "Status": [],
            "Data Element Count": []
        }
        for asset in filtered_assets:
            data_elements = asset_to_data_elements.get(asset['id'], [])
            asset_data["Asset"].append(asset['name'])
            asset_data["Description"].append(asset['description'])
            asset_data["Type"].append(asset.get('type', 'N/A'))
            asset_data["Status"].append(asset.get('status', 'Active'))
            asset_data["Data Element Count"].append(len(data_elements))

        asset_names = [asset['name'] for asset in filtered_assets]
        if asset_names:
            selected_asset_name = st.selectbox("Select an asset to view details", asset_names)
            selected_asset = next((asset for asset in filtered_assets if asset['name'] == selected_asset_name), None)
            with st.container():
                card_header = f'''
                <div style="background-color: white; border-radius: 10px 10px 0 0; padding: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">
                    <h3 style="color: #2c3e50; margin-top: 0;">{selected_asset['name']}</h3>
                    <p style="color: #7f8c8d;">{selected_asset['description']}</p>
                    <p><span style="background-color: #e8f4f8; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">{selected_asset.get('status', 'Active')}</span></p>
                </div>
                '''
                st.markdown(card_header, unsafe_allow_html=True)
                card_body = '<div style="background-color: white; border-radius: 0 0 10px 10px; padding: 0 15px 15px 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">'
                st.markdown(card_body, unsafe_allow_html=True)
                data_elements = asset_to_data_elements.get(selected_asset['id'], [])
                if data_elements:
                    with st.expander(f"Data Elements ({len(data_elements)})"): 
                        de_data = {
                            "Data Element": [],
                            "Description": []
                        }
                        for de in data_elements:
                            de_data["Data Element"].append(de['name'])
                            de_data["Description"].append(de['description'])
                        st.dataframe(pd.DataFrame(de_data), use_container_width=True)
                
                # Add catalog functionality
                catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(selected_asset['id'])
                
                # Add a scan button
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("🔍 Scan Database", key=f"scan_btn_{selected_asset['id']}"):
                        with st.spinner(f"Scanning {selected_asset['name']} database structure..."):
                            num_entries = self.catalog_repository.scan_asset(selected_asset['id'])
                            # Refresh catalog entries after scan
                            catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(selected_asset['id'])
                            st.success(f"Scan complete! Found {num_entries} database columns.")
                
                with col1:
                    st.write(f"Database Catalog for {selected_asset['name']}")
                
                # Display catalog data
                if catalog_entries:
                    with st.expander(f"Database Catalog ({len(catalog_entries)} columns)", expanded=True): 
                        # Group catalog entries by schema and table
                        schemas = {}
                        for entry in catalog_entries:
                            schema_name = entry['schema_name']
                            table_name = entry['table_name']
                            
                            if schema_name not in schemas:
                                schemas[schema_name] = {}
                            
                            if table_name not in schemas[schema_name]:
                                schemas[schema_name][table_name] = []
                            
                            schemas[schema_name][table_name].append(entry)
                        
                        # Create tabs for each schema
                        if len(schemas) > 0:
                            schema_tabs = st.tabs(list(schemas.keys()))
                            
                            for i, (schema_name, tables) in enumerate(schemas.items()):
                                with schema_tabs[i]:
                                    # Create tabs for each table in the schema
                                    table_tabs = st.tabs(list(tables.keys()))
                                    
                                    for j, (table_name, columns) in enumerate(tables.items()):
                                        with table_tabs[j]:
                                            # Create a dataframe for the columns
                                            columns_data = {
                                                "Column": [],
                                                "Data Type": [],
                                                "Classification": [],
                                                "Sample Data": [],
                                                "Last Scanned": []
                                            }
                                            
                                            for col in columns:
                                                columns_data["Column"].append(col['column_name'])
                                                columns_data["Data Type"].append(col['data_type'])
                                                columns_data["Classification"].append(col['data_element_name'] if col['data_element_name'] else "Unclassified")
                                                columns_data["Sample Data"].append(col['sample_data'] if col['sample_data'] else "")
                                                columns_data["Last Scanned"].append(col['last_scanned'])
                                            
                                            # Display the columns dataframe
                                            st.dataframe(pd.DataFrame(columns_data), use_container_width=True)
                                            
                                            # For each classified column, show policy implementations
                                            classified_columns = [col for col in columns if col['data_element_id'] is not None]
                                            if classified_columns:
                                                st.markdown("<h5>Policy Implementation Status</h5>", unsafe_allow_html=True)
                                                for col in classified_columns:
                                                    policy_implementations = self.catalog_repository.get_policy_implementations_by_catalog(col['id'])
                                                    if policy_implementations:
                                                        st.write(f"**{col['column_name']}** ({col['data_element_name']})")
                                                        
                                                        # Create a dataframe for the policy implementations
                                                        policy_data = {
                                                            "Policy": [],
                                                            "Status": [],
                                                            "Masking": [],
                                                            "Encryption": [],
                                                            "Access Control": [],
                                                            "Retention": [],
                                                            "Audit Logging": []
                                                        }
                                                        
                                                        for impl in policy_implementations:
                                                            policy_data["Policy"].append(impl['policy_name'])
                                                            policy_data["Status"].append(impl['implementation_status'])
                                                            
                                                            # Masking info
                                                            masking_info = "No"
                                                            if impl['is_masked']:
                                                                masking_info = f"Yes - {impl['masking_format']}" if impl['masking_format'] else "Yes"
                                                            policy_data["Masking"].append(masking_info)
                                                            
                                                            # Encryption info
                                                            encryption_info = "No"
                                                            if impl['is_encrypted']:
                                                                encryption_info = f"Yes - {impl['encryption_algorithm']}" if impl['encryption_algorithm'] else "Yes"
                                                            policy_data["Encryption"].append(encryption_info)
                                                            
                                                            # Access control info
                                                            access_control_info = "No"
                                                            if impl['has_access_control']:
                                                                access_control_info = f"Yes - {impl['access_control_type']}" if impl['access_control_type'] else "Yes"
                                                            policy_data["Access Control"].append(access_control_info)
                                                            
                                                            # Retention info
                                                            retention_info = "No"
                                                            if impl['has_retention_policy']:
                                                                retention_info = f"Yes - {impl['retention_period']}" if impl['retention_period'] else "Yes"
                                                            policy_data["Retention"].append(retention_info)
                                                            
                                                            # Audit logging info
                                                            audit_info = "No"
                                                            if impl['has_audit_logging']:
                                                                audit_info = f"Yes - {impl['audit_level']}" if impl['audit_level'] else "Yes"
                                                            policy_data["Audit Logging"].append(audit_info)
                                                        
                                                        # Display the policy implementations dataframe
                                                        st.dataframe(pd.DataFrame(policy_data), use_container_width=True)
                else:
                    st.info(f"No catalog data available for {selected_asset['name']}. Click 'Scan Database' to discover database structure.")
                
                # Add purpose selection for policy analysis
                st.markdown("### Analysis Options")
                
                # Get purposes for dropdown
                purposes = self.glossary_repository.get_purposes()
                purpose_options = {}
                for purpose in purposes:
                    purpose_id = purpose["id"]
                    purpose_name = purpose["name"]
                    purpose_options[purpose_id] = purpose_name
                    
                # Add 'All Purposes' option
                purpose_options['all'] = "All Purposes"
                    
                # Create two columns for the dropdowns
                col_purpose, col_policy_type = st.columns(2)
                
                with col_purpose:
                    # Purpose selection multi-select
                    selected_purposes = st.multiselect(
                        "Select Purpose(s):",
                        options=list(purpose_options.keys()),
                        default=["all"],
                        format_func=lambda x: purpose_options.get(x, ""),
                        key=f"purpose_select_{selected_asset['id']}"
                    )
                    
                    # Default to 'all' if nothing is selected
                    if not selected_purposes:
                        selected_purposes = ["all"]
                
                with col_policy_type:
                    # Policy type selection multi-select
                    policy_type_options = {
                        "all": "All Policy Types",
                        "security": "Data Security Policies",
                        "usage": "Data Usage Policies",
                        "retention": "Data Retention Policies"
                    }
                    
                    selected_policy_types = st.multiselect(
                        "Select Policy Type(s):",
                        options=list(policy_type_options.keys()),
                        default=["all"],
                        format_func=lambda x: policy_type_options.get(x, ""),
                        key=f"policy_type_select_{selected_asset['id']}"
                    )
                    
                    # Default to 'all' if nothing is selected
                    if not selected_policy_types:
                        selected_policy_types = ["all"]
                
                # Get external roles for this asset
                external_roles = self.glossary_repository.get_external_roles_by_asset(asset_id=selected_asset['id'])
                
                # Create a dictionary of role options with an 'All Roles' option
                role_options = {}
                for role in external_roles:
                    # External roles are returned as tuples: (id, name, description, source_system, source_role_name, asset_id)
                    role_options[role[0]] = role[1]  # role[0] is id, role[1] is name
                role_options['all'] = "All Roles"
                
                # Default to 'all' if nothing is selected
                selected_roles = ["all"]
                
                # Create three columns for the buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    # Run analysis button
                    run_analysis = st.button("Run Asset Analysis", key=f"run_analysis_{selected_asset['id']}")
                with col2:
                    # Run policy analysis button
                    run_policy_analysis = st.button("Run Policy Analysis", key=f"run_policy_analysis_{selected_asset['id']}")
                with col3:
                    # Generate JSON policy specification button
                    generate_json = st.button("Generate Target Policy JSON", key=f"generate_json_{selected_asset['id']}")
                with col4:
                    # Generate Security Policy DDL button
                    generate_ddl = st.button("Generate Target Policy DDL", key=f"generate_ddl_{selected_asset['id']}")
                # Removed the explanation section from here - it will be shown after the results                    
                
                # Variables to store policy analysis results
                policy_analysis = None
                purpose_display = ""
                policy_type_display = ""
                role_display = ""
                
                # Handle the Generate JSON Policy Spec button click or DDL generation
                if (generate_json or generate_ddl) and self.asset_policy_inference:
                    # Format display strings for selected options
                    if "all" in selected_purposes:
                        purpose_display = "All Purposes"
                    else:
                        purpose_names = [purpose_options.get(p, "") for p in selected_purposes]
                        purpose_display = ", ".join(purpose_names)
                    
                    if "all" in selected_policy_types:
                        policy_type_display = "All Policy Types"
                    else:
                        policy_type_names = [policy_type_options.get(pt, "") for pt in selected_policy_types]
                        policy_type_display = ", ".join(policy_type_names)
                    
                    if "all" in selected_roles:
                        role_display = "All Roles"
                    else:
                        role_names = [role_options.get(r, "") for r in selected_roles]
                        role_display = ", ".join(role_names)
                    
                    # Get the policy analysis results
                    if generate_json or generate_ddl:
                        # First get the policy analysis DataFrame for display
                        df = self.asset_policy_inference.get_applied_policies_for_asset_purpose(
                            asset_id=selected_asset['id'],
                            purpose_id=selected_purposes,
                            policy_type=selected_policy_types,
                            role_id=selected_roles
                        )
                        
                        # Check if we have data to display
                        if not df.empty:
                            # Build the JSON from the DataFrame (needed for both JSON display and DDL generation)
                            policy_analysis = self.json_generator.build_column_based_json_from_df(df, selected_asset['id'])
                            
                            # If Generate JSON button was clicked, show the JSON
                            if generate_json:
                                # First show the policy analysis table
                                st.markdown(f"<h4>Policy Analysis for {selected_asset['name']}</h4>", unsafe_allow_html=True)
                                
                                # Format boolean columns as checkboxes
                                formatted_df = self.asset_policy_inference.format_boolean_as_checkbox(df)
                                
                                # Rename columns for better display
                                column_mapping = {
                                    "schema_name": "Schema",
                                    "table_name": "Table",
                                    "column_name": "Column",
                                    "data_type": "Data Type",
                                    "data_element_name": "Data Element",
                                    "purpose_name": "Purpose",
                                    "role_name": "Role",
                                    "policy_name": "Policy",
                                    "encryption_required": "Encryption Required",
                                    "encryption_algorithm": "Encryption Algorithm",
                                    "masking_required": "Masking Required",
                                    "masking_format": "Masking Format",
                                    "is_override": "Is Override"
                                }
                                formatted_df.columns = [column_mapping.get(col, col) for col in formatted_df.columns]
                                
                                # Display the DataFrame
                                st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                                
                                # Then display the JSON policy specification
                                st.markdown(f"<h4>JSON Policy Specification for {selected_asset['name']}</h4>", unsafe_allow_html=True)
                                
                                # Add a download button for the JSON
                                import json
                                json_str = json.dumps(policy_analysis, indent=2)
                                st.download_button(
                                    label="Download JSON",
                                    data=json_str,
                                    file_name=f"{selected_asset['name'].lower().replace(' ', '_')}_policy_spec.json",
                                    mime="application/json"
                                )
                                
                                # Display the JSON in an expandable section
                                with st.expander("View JSON Policy Specification", expanded=True):
                                    st.json(policy_analysis)
                            
                            # Process DDL generation if that button was clicked
                            if generate_ddl:
                                # Generate DDL using the policy analysis results
                                ddl_content = None
                                with st.spinner(f"Generating DDL for {selected_asset['name']} with {purpose_display}, {policy_type_display}, and {role_display}..."):
                                    ddl_content = self.ddl_generator.generate_snowflake_ddl(policy_analysis)
                                
                                if ddl_content:
                                    # Display the DDL
                                    st.markdown(f"<h4>Snowflake Security Policy DDL for {selected_asset['name']}</h4>", unsafe_allow_html=True)
                                    
                                    # Create a data-driven explanation based on the actual DDL and JSON
                                    # Extract key information from the policy_analysis JSON
                                    tables_count = len(policy_analysis.get('tables', {}))
                                    
                                    # Get table names and details
                                    table_names = []
                                    tables_with_row_filtering = []
                                    table_details = {}
                                    
                                    for table_key, table_info in policy_analysis.get('tables', {}).items():
                                        table_names.append(table_key)
                                        table_details[table_key] = {
                                            'schema': table_info.get('schema', ''),
                                            'table': table_info.get('table', ''),
                                            'columns_count': len(table_info.get('columns', {})),
                                            'sensitive_columns': [],
                                            'has_row_filtering': 'row_filtering' in table_info,
                                            'purposes': set()
                                        }
                                        
                                        if 'row_filtering' in table_info:
                                            tables_with_row_filtering.append(table_key)
                                            if 'purposes' in table_info['row_filtering']:
                                                table_details[table_key]['row_filtering_purposes'] = table_info['row_filtering'].get('purposes', [])
                                    
                                    # Count the number of columns with security policies and collect details
                                    columns_with_security = 0
                                    sensitive_columns = []
                                    purpose_role_mapping = {}
                                    column_policy_details = {}
                                    
                                    for table_key, table_info in policy_analysis.get('tables', {}).items():
                                        for col_name, col_info in table_info.get('columns', {}).items():
                                            column_has_security = False
                                            column_key = f"{table_key}.{col_name}"
                                            column_policy_details[column_key] = {
                                                'masking': False,
                                                'encryption': False,
                                                'purposes': set(),
                                                'roles': set()
                                            }
                                            
                                            for role_name, role_info in col_info.get('roles', {}).items():
                                                column_policy_details[column_key]['roles'].add(role_name)
                                                
                                                # Track purpose-role mapping
                                                if role_name not in purpose_role_mapping:
                                                    purpose_role_mapping[role_name] = set()
                                                
                                                for purpose_name, purpose_info in role_info.get('purposes', {}).items():
                                                    purpose_role_mapping[role_name].add(purpose_name)
                                                    column_policy_details[column_key]['purposes'].add(purpose_name)
                                                    table_details[table_key]['purposes'].add(purpose_name)
                                                    
                                                    if 'security' in purpose_info:
                                                        column_has_security = True
                                                        security_info = purpose_info['security']
                                                        
                                                        # Check for masking
                                                        if security_info.get('masking_required'):
                                                            column_policy_details[column_key]['masking'] = True
                                                            column_policy_details[column_key]['masking_format'] = security_info.get('masking_format')
                                                            sensitive_columns.append(column_key)
                                                            table_details[table_key]['sensitive_columns'].append(col_name)
                                                        
                                                        # Check for encryption
                                                        if security_info.get('encryption_required'):
                                                            column_policy_details[column_key]['encryption'] = True
                                                            column_policy_details[column_key]['encryption_algorithm'] = security_info.get('encryption_algorithm')
                                            
                                            if column_has_security:
                                                columns_with_security += 1
                                    
                                    # Get unique purposes and roles
                                    all_purposes = set()
                                    all_roles = set()
                                    for role, purposes in purpose_role_mapping.items():
                                        all_roles.add(role)
                                        all_purposes.update(purposes)
                                    
                                    # Format for display
                                    purpose_list = ", ".join([f"'{p}'" for p in all_purposes]) if all_purposes else "All Purposes"
                                    role_list = ", ".join([f"'{r}'" for r in all_roles]) if all_roles else "All Roles"
                                    
                                    # Select an example table and column for the user access example
                                    example_table = tables_with_row_filtering[0] if tables_with_row_filtering else (table_names[0] if table_names else "example_table")
                                    example_column = table_details[example_table]['sensitive_columns'][0] if table_details[example_table]['sensitive_columns'] else "email"
                                    example_purpose = list(table_details[example_table]['purposes'])[0] if table_details[example_table]['purposes'] else "Marketing"
                                    example_role = None
                                    for role, purposes in purpose_role_mapping.items():
                                        if example_purpose in purposes:
                                            example_role = role
                                            break
                                    if not example_role and all_roles:
                                        example_role = list(all_roles)[0]
                                    
                                    # Analyze the DDL content to extract key information
                                    role_creation_count = ddl_content.count("CREATE ROLE")
                                    view_creation_count = ddl_content.count("CREATE OR REPLACE SECURE VIEW")
                                    row_policy_count = ddl_content.count("CREATE OR REPLACE ROW ACCESS POLICY")
                                    masking_policy_count = ddl_content.count("CREATE OR REPLACE MASKING POLICY")
                                    
                                    # Create a user-friendly explanation using HTML component with scrolling
                                    html_content = f"""
                                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db; font-size: 16px; line-height: 1.5; max-height: 600px; overflow-y: auto;">
                                        <h3 style="color: #2c3e50; font-size: 22px;">How This Security Policy Works</h3>
                                        
                                        <p>This DDL script creates a comprehensive security policy system for <strong>{selected_asset['name']}</strong>, implementing protections for <strong>{tables_count} tables</strong> with <strong>{columns_with_security} sensitive columns</strong>. Here's what it implements:</p>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔐 Role-Based Access Control</h4>
                                        <ul>
                                            <li>Creates <strong>{role_creation_count} roles</strong> to manage access to your data</li>
                                            <li>Establishes purpose-specific roles for: {purpose_list}</li>
                                            <li>Configures role hierarchy to enforce least privilege access principles</li>
                                        </ul>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔍 Row-Level Security</h4>
                                        <ul>
                                            <li>Implements <strong>{row_policy_count} row access policies</strong> for data filtering</li>
                                            <li>Applies row-level security to <strong>{len(tables_with_row_filtering)} tables</strong> based on user consent</li>
                                            <li>Creates a consent tracking system that filters data in real-time based on purpose</li>
                                        </ul>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🛡️ Column-Level Protection</h4>
                                        <ul>
                                            <li>Creates <strong>{masking_policy_count} masking policies</strong> for sensitive data</li>
                                            <li>Protects <strong>{len(sensitive_columns)} columns</strong> with dynamic data masking</li>
                                            <li>Implements <strong>{view_creation_count} secure views</strong> with appropriate masking</li>
                                        </ul>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">📎 Protected Tables & Applied Policies</h4>
                                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px; max-height: 200px; overflow-y: auto;">
                                            {''.join([f'''
                                            <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #ccc;">
                                                <p><strong>Table:</strong> {table_key}</p>
                                                <p><strong>Columns:</strong> {table_details[table_key]['columns_count']}</p>
                                                <p><strong>Sensitive Columns:</strong> {', '.join(table_details[table_key]['sensitive_columns']) if table_details[table_key]['sensitive_columns'] else 'None'}</p>
                                                <p><strong>Row Filtering:</strong> {'Yes - filters by consent for: ' + ', '.join(table_details[table_key].get('row_filtering_purposes', [])) if table_details[table_key]['has_row_filtering'] else 'No'}</p>
                                                <p><strong>Purposes:</strong> {', '.join(table_details[table_key]['purposes']) if table_details[table_key]['purposes'] else 'All'}</p>
                                            </div>''' for table_key in table_names])}
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔗 Purpose-Role Mapping</h4>
                                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px; max-height: 200px; overflow-y: auto;">
                                            {''.join([f'''
                                            <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #ccc;">
                                                <p><strong>Role:</strong> {role}</p>
                                                <p><strong>Authorized Purposes:</strong> {', '.join(purposes)}</p>
                                            </div>''' for role, purposes in purpose_role_mapping.items()])}
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">📋 Your Configuration Summary</h4>
                                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                            <p><strong>Asset:</strong> {selected_asset['name']}</p>
                                            <p><strong>Tables Protected:</strong> {tables_count}</p>
                                            <p><strong>Purposes:</strong> {purpose_list}</p>
                                            <p><strong>Roles:</strong> {role_list}</p>
                                            <p><strong>Policy Types:</strong> {policy_type_display}</p>
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">📚 Privacy & Compliance Rationale</h4>
                                        <div style="background-color: #f0f9ff; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                            <p><strong>Regulatory Compliance:</strong> This security policy implementation helps meet requirements from regulations like GDPR, CCPA, HIPAA, and industry standards.</p>
                                            <p><strong>Data Governance:</strong> Establishes clear boundaries for data usage based on purpose, ensuring data is only used for its intended purposes.</p>
                                            <p><strong>Risk Mitigation:</strong> Reduces the risk of data breaches by limiting access to sensitive information and providing audit trails.</p>
                                            <p><strong>Privacy by Design:</strong> Implements privacy controls directly in the database layer, making privacy a fundamental part of data access.</p>
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">💡 Access Example</h4>
                                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                            <p><strong>Example Scenario:</strong> Accessing the <code>{example_table}</code> table</p>
                                            
                                            <div style="margin-top: 10px; padding: 10px; background-color: #fff; border-radius: 5px; border-left: 3px solid #27ae60;">
                                                <p><strong>User WITH Role '{example_role}' and Purpose '{example_purpose}':</strong></p>
                                                <ul>
                                                    <li>Can see all rows where users have consented to '{example_purpose}'</li>
                                                    <li>Sees unmasked data for the <code>{example_column}</code> column</li>
                                                    <li>Has all access logged for audit purposes</li>
                                                </ul>
                                            </div>
                                            
                                            <div style="margin-top: 10px; padding: 10px; background-color: #fff; border-radius: 5px; border-left: 3px solid #e74c3c;">
                                                <p><strong>User WITHOUT Role '{example_role}' or Purpose '{example_purpose}':</strong></p>
                                                <ul>
                                                    <li>Cannot see any rows from the table</li>
                                                    <li>Sees masked/redacted data for sensitive columns</li>
                                                    <li>All access attempts are logged and can trigger alerts</li>
                                                </ul>
                                            </div>
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔄 Continuous Data Governance</h4>
                                        <div style="background-color: #f0f9ff; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                            <p>This implementation enables continuous data governance through:</p>
                                            <ul>
                                                <li><strong>Real-time Consent Enforcement:</strong> Access policies check consent status in real-time, so consent changes are immediately reflected</li>
                                                <li><strong>Comprehensive Audit Logging:</strong> All data access is logged, enabling monitoring and compliance reporting</li>
                                                <li><strong>Centralized Policy Management:</strong> Security policies are managed centrally, allowing for consistent updates</li>
                                                <li><strong>Dynamic Access Control:</strong> As users' roles change, their data access automatically adjusts</li>
                                                <li><strong>Automated Compliance:</strong> The system automatically enforces privacy rules without manual intervention</li>
                                            </ul>
                                        </div>
                                        
                                        <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">💻 Technical Implementation</h4>
                                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                            <p>This DDL creates the following database objects:</p>
                                            <ul>
                                                <li><strong>{role_creation_count} roles</strong> for purpose-based access control</li>
                                                <li><strong>{row_policy_count} row access policies</strong> for consent-based filtering</li>
                                                <li><strong>{masking_policy_count} masking policies</strong> for sensitive data protection</li>
                                                <li><strong>{view_creation_count} secure views</strong> that enforce all security policies</li>
                                            </ul>
                                            <p>After running this DDL, users will need to be granted the appropriate roles to access the data according to their job functions and authorized purposes.</p>
                                        </div>
                                    </div>
                                    """
                                    st.components.v1.html(html_content, height=700)
                                    
                                    # Add a download button for the DDL
                                    st.download_button(
                                        label="Download Security Policy DDL",
                                        data=ddl_content,
                                        file_name=f"{selected_asset['name'].lower().replace(' ', '_')}_security_policies.sql",
                                        mime="text/plain"
                                    )
                                    
                                    # Display the DDL in an expandable section
                                    with st.expander("View Snowflake Security Policy DDL", expanded=True):
                                        st.code(ddl_content, language="sql")
                
                        # Show info box about analysis workflow after the results
                        st.markdown('''
                        <div style="background-color: #eaf7ea; padding: 18px 20px; border-radius: 10px; margin-bottom: 18px; border-left: 5px solid #27ae60;">
                        <h4 style="margin-top: 0; color: #229954;">Policy Analysis, JSON Generation, and DDL Creation Process</h4>
                        <ul style="margin-bottom: 0;">
                            <li><strong>Policy Analysis:</strong> When you click "Run Policy Analysis", the system analyzes policies applied to the selected asset based on:</li>
                            <ul>
                                <li>The selected business purposes (e.g., Customer Support, Marketing)</li>
                                <li>The selected policy types (Security, Usage, Retention)</li>
                                <li>The selected roles (e.g., Data Analyst, Data Engineer)</li>
                            </ul>
                            <li><strong>JSON Policy Specification:</strong> When you click "Generate JSON Policy Spec", the system:</li>
                            <ul>
                                <li>Uses the same data source as the policy analysis to ensure consistency</li>
                                <li>Creates a hierarchical JSON structure organizing policies by role, table, column, and purpose</li>
                                <li>Groups all policies under their respective roles for clearer organization</li>
                                <li>Specifies security requirements including masking and encryption details</li>
                            </ul>
                            <li><strong>Security Policy DDL Generation:</strong> When you click "Generate Security Policy DDL", the system:</li>
                            <ul>
                                <li>Processes the JSON policy specification through a GenAI model (Gemini)</li>
                                <li>Creates Snowflake DDL statements that implement the specified policies</li>
                                <li>Generates purpose-based roles (e.g., PURPOSE_CUSTOMER_SUPPORT)</li>
                                <li>Creates GRANT statements to associate purpose-based roles with original Snowflake roles</li>
                                <li>Implements column-level masking policies based on the masking formats in the JSON</li>
                            </ul>
                            <li><strong>End Result:</strong> You get executable Snowflake DDL that implements your security policies with proper role-based access controls and data protection measures.</li>
                        </ul>
                        </div>
                        ''', unsafe_allow_html=True) 

                # Show info box about analysis workflow after the results   
                # No need to store unique data elements for filtering anymore
                
                # Handle the Run Policy Analysis button click
                if run_policy_analysis and self.asset_policy_inference:
                    # Format display strings for selected options
                    if "all" in selected_purposes:
                        purpose_display = "All Purposes"
                    else:
                        purpose_names = [purpose_options.get(p, "") for p in selected_purposes]
                        purpose_display = ", ".join(purpose_names)
                    
                    if "all" in selected_policy_types:
                        policy_type_display = "All Policy Types"
                    else:
                        policy_type_names = [policy_type_options.get(pt, "") for pt in selected_policy_types]
                        policy_type_display = ", ".join(policy_type_names)
                    
                    if "all" in selected_roles:
                        role_display = "All Roles"
                    else:
                        role_names = [role_options.get(r, "") for r in selected_roles]
                        role_display = ", ".join(role_names)
                    
                    with st.spinner(f"Analyzing policy application for {selected_asset['name']} with {purpose_display}, {policy_type_display}, and {role_display}..."):
                        # Get applied policies for the selected asset, purpose, policy type, and role
                        df = self.asset_policy_inference.get_applied_policies_for_asset_purpose(
                            asset_id=selected_asset['id'],
                            purpose_id=selected_purposes,
                            policy_type=selected_policy_types,
                            role_id=selected_roles
                        )
                        
                        if not df.empty:
                            # Format boolean columns as checkboxes
                            formatted_df = self.asset_policy_inference.format_boolean_as_checkbox(df)
                            
                            # No need to store results in session state anymore
                            
                            # Rename columns for better display
                            column_mapping = {
                                "schema_name": "Schema",
                                "table_name": "Table",
                                "column_name": "Column",
                                "data_type": "Data Type",
                                "data_element_name": "Data Element",
                                "purpose_name": "Purpose",
                                "role_name": "Role",
                                "policy_name": "Policy",
                                "encryption_required": "Encryption Required",
                                "encryption_algorithm": "Encryption Algorithm",
                                "masking_required": "Masking Required",
                                "masking_format": "Masking Format",
                                "is_override": "Is Override"
                            }
                            formatted_df.columns = [column_mapping.get(col, col) for col in formatted_df.columns]
                            
                            # Add a note about encryption settings for non-Default Role Assignment purposes
                            if "all" in selected_purposes or any(purpose_options.get(p) != "Default Role Assignment" for p in selected_purposes):
                                st.markdown(f"<h4>Applied Policies for {selected_asset['name']}</h4>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<h4>Applied Policies for {selected_asset['name']} with Purpose(s): {purpose_display}</h4>", unsafe_allow_html=True)
                            
                            # Display the DataFrame without filters
                            st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                        else:
                            # If no results were found
                            st.warning(f"No policies found for {selected_asset['name']} with the selected purpose(s): {purpose_display}. This could be because there are no data elements mapped to this asset, or no policies defined for the selected purpose(s).")                
                        
                # No longer need to handle previous policy analysis results from session state

                # Handle the Run Asset Analysis button click
                if run_analysis:
                    # 1. Infer sensitivities
                    data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                    if not data_element_sensitivities:
                        st.warning("Could not determine sensitivities for the data elements.")
                        return
                    st.markdown("<h5>Data Element Sensitivity Analysis</h5>", unsafe_allow_html=True)
                    sens_data = {
                        "Data Element": [],
                        "Sensitivity": [],
                        "Source": []
                    }
                    for de_name, sensitivity_info in data_element_sensitivities.items():
                        sens_data["Data Element"].append(de_name)
                        sens_data["Sensitivity"].append(sensitivity_info['sensitivity'])
                        sens_data["Source"].append(sensitivity_info['source'])
                    st.dataframe(pd.DataFrame(sens_data), use_container_width=True)

                    # 2. Derive obligations
                    st.markdown("<h5>Recommended Obligations</h5>", unsafe_allow_html=True)
                    all_sensitivities = self.glossary_repository.get_sensitivities()
                    all_obligations = []
                    obligations_by_de = {}
                    for de_name, sensitivity_info in data_element_sensitivities.items():
                        sensitivity = sensitivity_info['sensitivity']
                        sensitivity_id = next((s['id'] for s in all_sensitivities if s['name'] == sensitivity), None)
                        if sensitivity_id:
                            sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                            for so in sensitivity_obligations:
                                obligation_row = {
                                    "id": so["obligation_id"],
                                    "name": so["obligation_name"],
                                    "control_type": so["control_type"],
                                    "priority": so["priority"],
                                    "data_element_name": de_name
                                }
                                all_obligations.append(obligation_row)
                                # For policies/risks
                                obligations_by_de.setdefault(de_name, []).append(obligation_row)
                    if all_obligations:
                        df = pd.DataFrame([{
                            "Data Element": o["data_element_name"],
                            "Obligation": o["name"],
                            "Control Type": o["control_type"],
                            "Priority": o["priority"]
                        } for o in all_obligations])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No obligations defined for these data elements.")

                    # Get detailed policy recommendations for each data element with significant sensitivities
                    st.markdown("<h5>Detailed Policy Recommendations</h5>", unsafe_allow_html=True)
                    
                    # Define which sensitivities require policies
                    # Using the actual sensitivity values from the database
                    sensitivities_requiring_policies = ["Internal", "Confidential", "Restricted", "Special Category"]
                    
                    # Filter data elements based on their sensitivity
                    policy_required_elements = {}
                    
                    for de_name, sensitivity_info in data_element_sensitivities.items():
                        sensitivity = sensitivity_info['sensitivity']
                        if sensitivity in sensitivities_requiring_policies:
                            policy_required_elements[de_name] = sensitivity
                    
                    if not policy_required_elements:
                        st.info("No data elements with sensitivities that require specific policies were found.")
                    else:
                        st.write(f"Found {len(policy_required_elements)} data elements that require specific policies based on their sensitivity.")
                        
                        # For each data element with significant sensitivity, get the policy details
                        for de_name, sensitivity in policy_required_elements.items():
                            # Get the data element ID
                            data_element = next((de for de in self.glossary_repository.get_data_elements() if de['name'] == de_name), None)
                            if data_element:
                                data_element_id = data_element['id']
                                
                                # Get policy details for this data element
                                policy_details = self.regulatory_metadata_repository.get_data_element_policies(data_element_id)
                                
                                if any(policy_details.values()):
                                    with st.expander(f"Policy Details for {de_name}"):
                                        # Show usage policies
                                        if policy_details['usage']:
                                                st.markdown("<h5>Usage Policies</h5>", unsafe_allow_html=True)
                                                usage_data = {
                                                    "Policy": [],
                                                    "Operation": [],
                                                    "Allowed": [],
                                                    "Restrictions": []
                                                }
                                                for usage in policy_details['usage']:
                                                    usage_data["Policy"].append(usage['policy_name'])
                                                    usage_data["Operation"].append(usage['operation'])
                                                    usage_data["Allowed"].append("Yes" if usage['allowed'] else "No")
                                                    usage_data["Restrictions"].append(usage['restrictions'] or "")
                                                    
                                                st.dataframe(pd.DataFrame(usage_data), use_container_width=True)
                                        
                                        # Show retention policies
                                        if policy_details['retention']:
                                                st.markdown("<h5>Retention Policies</h5>", unsafe_allow_html=True)
                                                retention_data = {
                                                    "Policy": [],
                                                    "Retention Period": [],
                                                    "Retention Basis": [],
                                                    "Exceptions": []
                                                }
                                                for retention in policy_details['retention']:
                                                    retention_data["Policy"].append(retention['policy_name'])
                                                    retention_data["Retention Period"].append(retention['retention_period'])
                                                    retention_data["Retention Basis"].append(retention['retention_basis'] or "")
                                                    retention_data["Exceptions"].append(retention['exceptions'] or "")
                                                    
                                                st.dataframe(pd.DataFrame(retention_data), use_container_width=True)
                                        
                                        # Show security policies
                                        if policy_details['security']:
                                            st.markdown("<h5>Security Policies</h5>", unsafe_allow_html=True)
                                            security_data = {
                                                "Policy": [],
                                                "Encryption": [],
                                                "Masking": [],
                                                "Access Control": []
                                            }
                                            for security in policy_details['security']:
                                                security_data["Policy"].append(security['policy_name'])
                                                
                                                # Encryption info
                                                encryption_info = "No"
                                                if security['requires_encryption']:
                                                    encryption_info = f"Yes - {security['encryption_algorithm']}" if security['encryption_algorithm'] else "Yes"
                                                security_data["Encryption"].append(encryption_info)
                                                
                                                # Masking info
                                                masking_info = "No"
                                                if security['requires_masking']:
                                                    masking_info = f"Yes - {security['masking_format']}" if security['masking_format'] else "Yes"
                                                security_data["Masking"].append(masking_info)
                                                
                                                # Access control info
                                                access_control_info = "No"
                                                if security['requires_access_control']:
                                                    access_control_info = f"Yes - {security['access_control_type']}" if security['access_control_type'] else "Yes"
                                                security_data["Access Control"].append(access_control_info)
                                            
                                            st.dataframe(pd.DataFrame(security_data), use_container_width=True)

                    # 4. Derive risks
                    st.markdown("<h5>Potential Risks (by Data Element)</h5>", unsafe_allow_html=True)
                    all_risks = []
                    for de_name, de_obligations in obligations_by_de.items():
                        for obligation in de_obligations:
                            obligation_id = obligation["id"]
                            obligation_name = obligation["name"]
                            risks = self.obligation_repository.get_risks_for_obligation(obligation_id)
                            for risk in risks:
                                all_risks.append({
                                    "Data Element": de_name,
                                    "Obligation": obligation_name,
                                    "Risk": risk["name"],
                                    "Risk Category": risk["category"],
                                    "Likelihood": risk["likelihood"],
                                    "Impact": risk["impact"]
                                })
                    if all_risks:
                        df = pd.DataFrame(all_risks)
                        # Add risk rating
                        def get_risk_rating(row):
                            likelihood = row['Likelihood']
                            impact = row['Impact']
        
                            if likelihood == 'High' and impact == 'High':
                                return 'Critical'
                            elif (likelihood == 'High' and impact == 'Medium') or (likelihood == 'Medium' and impact == 'High'):
                                return 'High'
                            elif (likelihood == 'Medium' and impact == 'Medium') or (likelihood == 'High' and impact == 'Low') or (likelihood == 'Low' and impact == 'High'):
                                return 'Medium'
                            else:
                                return 'Low'
            
                        df["Risk Rating"] = df.apply(get_risk_rating, axis=1)
                        display_columns = ["Data Element", "Obligation", "Risk", "Risk Category", "Likelihood", "Impact", "Risk Rating"]
                        st.dataframe(df[display_columns], use_container_width=True)
                    else:
                        st.info("No risks identified for the obligations.")
                st.markdown('</div>', unsafe_allow_html=True)

    def show_sensitivity_based_obligations(self, data_element_sensitivities):
        """Show obligations based on data element sensitivities. Each row includes the data element name."""
        if not data_element_sensitivities:
            st.warning("No sensitivity information available.")
            return
        st.subheader("Recommended Obligations (by Data Element)")
        all_obligations = []
        all_sensitivities = self.glossary_repository.get_sensitivities()
        for de_name, sensitivity_info in data_element_sensitivities.items():
            sensitivity = sensitivity_info['sensitivity']
            sensitivity_id = next((s['id'] for s in all_sensitivities if s['name'] == sensitivity), None)
            if sensitivity_id:
                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                for so in sensitivity_obligations:
                    all_obligations.append({
                        "Data Element": de_name,
                        "Sensitivity": sensitivity,
                        "Obligation": so["obligation_name"],
                        "Description": so["obligation_description"],
                        "Control Type": so["control_type"],
                        "Priority": so["priority"]
                    })
        if all_obligations:
            df = pd.DataFrame(all_obligations)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No obligations defined for these data elements.")

    def show_obligation_based_policies(self, obligations):
        """Show policies based on obligations. Each row includes the data element name if available."""
        if not obligations:
            st.warning("No obligation information available.")
            return
        st.markdown("<h5>Recommended Policies (by Data Element)</h5>", unsafe_allow_html=True)
        all_policies = []
        # Try to get data element mapping from obligations if present
        for obligation in obligations:
            obligation_id = obligation["id"]
            obligation_name = obligation.get("name", "Unknown")
            data_element_name = obligation.get("data_element_name", "Unknown")
            policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
            for policy in policies:
                all_policies.append({
                    "Data Element": data_element_name,
                    "Obligation": obligation_name,
                    "Policy": policy["name"],
                    "Control Type": policy.get("control_type", ""),
                    "Relevance Score": policy["relevance_score"]
                })
        if all_policies:
            df = pd.DataFrame(all_policies)
            st.dataframe(df, use_container_width=True)
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
        
        st.markdown("<h5>Potential Risks</h5>", unsafe_allow_html=True)
        
        # Get risks for the given obligations from the repository
        all_risks = []
        obligation_ids = [o["id"] for o in obligations]
        
        # Get risks for each obligation using the repository
        for obligation_id in obligation_ids:
            risks = self.obligation_repository.get_risks_for_obligation(obligation_id)
            obligation_name = next((o["name"] for o in obligations if o["id"] == obligation_id), "Unknown")
            
            for risk in risks:
                all_risks.append({
                    "Data Element": obligation_name,
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
            display_columns = ["Data Element", "Risk", "Risk Category", "Likelihood", "Impact", "Risk Rating"]
            filtered_df = filtered_df[display_columns]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            # Display risk summary
            st.markdown("<h5>Risk Assessment Summary</h5>", unsafe_allow_html=True)
            
            # Count risks by rating
            risk_counts = filtered_df["Risk Rating"].value_counts()
            
            # Create a summary message based on risk counts
            summary_message = """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h5 style="margin-top: 0;">Risk Assessment</h5>
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