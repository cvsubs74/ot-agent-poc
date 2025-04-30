import streamlit as st
import pandas as pd
import random
import string
import datetime
import json
from components.DDLGenerator import DDLGenerator

class DataAccessRequestPage:
    def __init__(self, glossary_repository, catalog_repository, asset_policy_inference, data_access_repository=None):
        """Initialize the Data Access Request page with required repositories."""
        self.glossary_repository = glossary_repository
        self.catalog_repository = catalog_repository
        self.asset_policy_inference = asset_policy_inference
        self.data_access_repository = data_access_repository
        self.ddl_generator = DDLGenerator()
    
    def render(self):
        """Render the Data Access Request page with tabs for request creation and monitoring."""
        st.markdown("<div class='page-header'><i class='fas fa-key'></i> &nbsp;Data Access Management</div>", unsafe_allow_html=True)
        
        # Add CSS for green expanders - matching the assets_page.py styling
        st.markdown("""
        <style>
        /* Target only the expander components */
        div[data-testid="stExpander"] {
            border: 1px solid #27ae60 !important;
            border-radius: 4px !important;
            margin-bottom: 10px !important;
            background-color: #eaf7ea !important;
        }
        div[data-testid="stExpander"] > div:first-child {
            background-color: #eaf7ea !important;
            border-bottom: 1px solid #27ae60 !important;
            padding: 0.5rem !important;
        }
        div[data-testid="stExpander"] details summary p {
            color: #27ae60 !important;
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section allows you to request access to specific tables in an asset for specific purposes.
            The system will analyze your request against existing policies and generate the necessary
            access controls, including:</p>
            <ul>
                <li>Purpose-based role hierarchy for proper access management</li>
                <li>Row-level security policies based on user consents</li>
                <li>Column-level masking for sensitive data elements</li>
                <li>Secure views with appropriate access controls</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Create tabs for request creation and monitoring
        tabs = st.tabs([
            "Request Data Access",
            "Access Requests Monitor"
        ])
        
        with tabs[0]:
            self._render_request_form()
            
        with tabs[1]:
            self._render_request_monitor()
    
    def _render_request_form(self):
        """Render the form for creating a new data access request."""
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>Request Data Access:</b><br>
            Complete this form to request access to specific tables in an asset for specific purposes.
            The system will analyze your request against existing policies and generate the necessary access controls.
        </div>
        ''', unsafe_allow_html=True)
        
        # User information form
        st.markdown("#### Requester Information")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                requester_name = st.text_input("Your Name", key="requester_name")
            with col2:
                requester_email = st.text_input("Your Email", key="requester_email")
        
        # Request details form
        st.markdown("#### Request Details")
        with st.container(border=True):
            # Get assets for selection
            assets = self.glossary_repository.get_assets()
            asset_options = {asset[0]: asset[1] for asset in assets}
            
            # Asset selection
            selected_asset_id = st.selectbox(
                "Select an asset to request access to:",
                options=list(asset_options.keys()),
                format_func=lambda x: asset_options.get(x, ""),
                key="data_access_asset_select"
            )
            
            if selected_asset_id:
                # Get tables for the selected asset
                catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(selected_asset_id)
                
                # Extract unique tables
                tables = {}
                for entry in catalog_entries:
                    table_key = f"{entry['schema_name']}.{entry['table_name']}"
                    if table_key not in tables:
                        tables[table_key] = {
                            "schema": entry['schema_name'],
                            "table": entry['table_name'],
                            "full_name": table_key
                        }
                
                # Table selection (multi-select)
                if tables:
                    table_options = list(tables.keys())
                    selected_tables = st.multiselect(
                        "Select tables to request access to:",
                        options=table_options,
                        key="data_access_table_select"
                    )
                    
                    # Get purposes for selection
                    purposes = self.glossary_repository.get_purposes()
                    purpose_options = {purpose['id']: purpose['name'] for purpose in purposes}
                    
                    # Purpose selection
                    selected_purposes = st.multiselect(
                        "Select purposes for data access:",
                        options=list(purpose_options.keys()),
                        format_func=lambda x: purpose_options.get(x, ""),
                        key="data_access_purpose_select"
                    )
                    
                    # Notes field
                    notes = st.text_area("Additional Notes", key="request_notes", 
                                       placeholder="Explain why you need access to this data...")
                    
                    # Request button
                    if selected_tables and selected_purposes:
                        if st.button("Submit Access Request", key="request_access_button", type="primary"):
                            if not requester_name or not requester_email:
                                st.error("Please provide your name and email address.")
                            else:
                                # Run policy analysis on the asset
                                df = self.asset_policy_inference.get_applied_policies_for_asset_purpose(
                                    asset_id=selected_asset_id,
                                    purpose_id=selected_purposes,
                                    policy_type=["all"],
                                    role_id=["all"]
                                )
                                
                                # Filter the results by the selected tables
                                if not df.empty:
                                    # Create table filter condition
                                    table_filter = df.apply(
                                        lambda row: f"{row['schema_name']}.{row['table_name']}" in selected_tables, 
                                        axis=1
                                    )
                                    
                                    # Apply the filter
                                    filtered_df = df[table_filter]
                                    
                                    if not filtered_df.empty:
                                        # Build the JSON from the filtered DataFrame
                                        policy_json = self._build_json_for_access_request(
                                            filtered_df, 
                                            selected_asset_id, 
                                            selected_tables,
                                            selected_purposes,
                                            purpose_options
                                        )
                                        
                                        # Generate a random role name
                                        role_name = f"DATA_ACCESS_{self._generate_random_suffix()}"
                                        
                                        # Generate the DDL for the role
                                        ddl = self.ddl_generator.generate_access_role_ddl(policy_json, role_name)
                                        
                                        # Save the request to the repository if available
                                        request_id = -1
                                        if self.data_access_repository:
                                            # Save the actual user request
                                            request_id = self.data_access_repository.create_request(
                                                requester_name=requester_name,
                                                requester_email=requester_email,
                                                asset_id=selected_asset_id,
                                                asset_name=asset_options[selected_asset_id],
                                                tables=selected_tables,
                                                purposes=[purpose_options[p_id] for p_id in selected_purposes],
                                                purpose_ids=selected_purposes,
                                                role_name=role_name,
                                                ddl=ddl,
                                                policy_json=json.dumps(policy_json),
                                                notes=notes
                                            )
                                            
                                            # Just display a success message, no tab switching
                                            if request_id > 0:
                                                st.success(f"Request saved with ID: {request_id}")
                                        
                                        # Display the results
                                        st.markdown(f"""
                                        <div class="success-card card">
                                        <h3>✅ Access Request Submitted Successfully!</h3>
                                        <p>Your request has been processed and is pending approval.</p>
                                        <p><strong>Request ID:</strong> {request_id if request_id > 0 else 'N/A'}</p>
                                        <p><strong>Role Name:</strong> {role_name}</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Display the JSON policy specification
                                        with st.expander("View Policy JSON"):
                                            st.markdown('<style>div.stExpander details summary p {color: #27ae60;}</style>', unsafe_allow_html=True)
                                            st.json(policy_json)
                                        
                                        # Display the DDL
                                        with st.expander("View Generated DDL"):
                                            st.markdown('<style>div.stExpander details summary p {color: #27ae60;}</style>', unsafe_allow_html=True)
                                            st.code(ddl, language="sql")
                                        
                                        # Add a download button for the DDL
                                        st.download_button(
                                            label="Download DDL Script",
                                            data=ddl,
                                            file_name=f"{role_name}_access.sql",
                                            mime="text/plain",
                                            key=f"download_ddl_{role_name}"
                                        )
                                    else:
                                        st.warning("No policies found for the selected tables and purposes.")
                                else:
                                    st.warning("No policies found for the selected asset and purposes.")
                    else:
                        st.info("Please select at least one table and one purpose to request access.")
                else:
                    st.info("No tables found for the selected asset.")
    
    def _render_request_monitor(self):
        """Render the monitoring view for data access requests."""
        st.markdown('''
        <div style="background-color: #e6f3ff; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #3498db;">
            <b>Access Requests Monitor:</b><br>
            View and manage all data access requests. You can approve or reject pending requests, 
            view request details, and download generated DDL scripts.
        </div>
        ''', unsafe_allow_html=True)
        
        if not self.data_access_repository:
            st.warning("Data Access Repository is not available. Request monitoring is disabled.")
            return
            
        # Get all requests from the repository
        requests = self.data_access_repository.get_all_requests()
        
        if not requests:
            st.info("No data access requests found.")
            return
            
        # Create a DataFrame for display
        df_data = []
        for req in requests:
            # Format the request date
            request_date = req.get('request_date', '')
            if request_date:
                try:
                    request_date = datetime.datetime.fromisoformat(request_date).strftime('%Y-%m-%d %H:%M')
                except:
                    pass
                    
            # Format the tables as a comma-separated list
            tables_str = ", ".join(req.get('tables', []))
            if len(tables_str) > 50:
                tables_str = tables_str[:47] + "..."
                
            # Format the purposes as a comma-separated list
            purposes_str = ", ".join(req.get('purposes', []))
            if len(purposes_str) > 50:
                purposes_str = purposes_str[:47] + "..."
                
            df_data.append({
                "ID": req.get('id'),
                "Requester": req.get('requester_name'),
                "Asset": req.get('asset_name'),
                "Tables": tables_str,
                "Purposes": purposes_str,
                "Role Name": req.get('role_name'),
                "Status": req.get('status'),
                "Request Date": request_date
            })
            
        df = pd.DataFrame(df_data)
        
        # Add filters with All option
        col1, col2, col3 = st.columns(3)
        with col1:
            status_options = sorted(df["Status"].unique())
            status_filter = st.multiselect(
                "Filter by Status",
                options=["All"] + status_options,
                default=["All"],
                key="status_filter"
            )
            # Handle All selection
            if "All" in status_filter:
                status_filter = status_options
                
        with col2:
            asset_options = sorted(df["Asset"].unique())
            asset_filter = st.multiselect(
                "Filter by Asset",
                options=["All"] + asset_options,
                default=["All"],
                key="asset_filter"
            )
            # Handle All selection
            if "All" in asset_filter:
                asset_filter = asset_options
                
        with col3:
            requester_options = sorted(df["Requester"].unique())
            requester_filter = st.multiselect(
                "Filter by Requester",
                options=["All"] + requester_options,
                default=["All"],
                key="requester_filter"
            )
            # Handle All selection
            if "All" in requester_filter:
                requester_filter = requester_options
            
        # Apply filters
        filtered_df = df[
            df["Status"].isin(status_filter) &
            df["Asset"].isin(asset_filter) &
            df["Requester"].isin(requester_filter)
        ]
        
        # Display the filtered DataFrame
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            # Request details section
            st.markdown("#### Request Details")
            selected_request_id = st.selectbox(
                "Select a request to view details",
                options=filtered_df["ID"].tolist(),
                format_func=lambda x: f"Request #{x} - {filtered_df[filtered_df['ID'] == x]['Role Name'].values[0]}",
                key="selected_request_id"
            )
            
            if selected_request_id:
                request = self.data_access_repository.get_request(selected_request_id)
                if request:
                    # Format status badge
                    status = request.get('status', 'Pending')
                    status_class = {
                        "Pending": "status-pending",
                        "Approved": "status-approved",
                        "Rejected": "status-rejected"
                    }.get(status, "status-pending")
                    
                    # Add enhanced card styling with status-based borders
                    st.markdown('''
                    <style>
                    .request-card {
                        border-radius: 10px;
                        padding: 20px;
                        background-color: #f8f9fa;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-bottom: 20px;
                        transition: all 0.3s ease;
                        position: relative;
                        overflow: hidden;
                    }
                    .request-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
                    }
                    .request-card-pending {
                        border-left: 5px solid #ffc107;
                    }
                    .request-card-approved {
                        border-left: 5px solid #28a745;
                    }
                    .request-card-rejected {
                        border-left: 5px solid #dc3545;
                    }
                    .status-indicator {
                        position: absolute;
                        top: 0;
                        right: 0;
                        padding: 5px 10px;
                        color: white;
                        font-weight: bold;
                        border-bottom-left-radius: 8px;
                    }
                    .status-pending {
                        background-color: #ffc107;
                    }
                    .status-approved {
                        background-color: #28a745;
                    }
                    .status-rejected {
                        background-color: #dc3545;
                    }
                    </style>
                    ''', unsafe_allow_html=True)
                    
                    # Display request details in a single card with status indicator
                    st.markdown(f"""
                    <div class="request-card request-card-{status.lower()}">
                        <div class="status-indicator status-{status.lower()}">{status}</div>
                        <h4>Request #{request.get('id')} - {request.get('role_name')}</h4>
                        <p><strong>Requester:</strong> {request.get('requester_name')} ({request.get('requester_email')})</p>
                        <p><strong>Asset:</strong> {request.get('asset_name')}</p>
                        <p><strong>Tables:</strong> {', '.join(request.get('tables', []))}</p>
                        <p><strong>Purposes:</strong> {', '.join(request.get('purposes', []))}</p>
                        <p><strong>Request Date:</strong> {request.get('request_date')}</p>
                        <p><strong>Notes:</strong> {request.get('notes', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Admin actions
                    if status == "Pending":
                        st.markdown("#### Admin Actions")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Approve Request", key=f"approve_{selected_request_id}", type="primary"):
                                # Set expiry date to 90 days from now
                                expiry_date = (datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
                                if self.data_access_repository.approve_request(selected_request_id, expiry_date=expiry_date):
                                    st.success("Request approved successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to approve request.")
                        with col2:
                            if st.button("Reject Request", key=f"reject_{selected_request_id}", type="secondary"):
                                reject_reason = st.text_area("Rejection Reason", key="reject_reason")
                                if reject_reason and self.data_access_repository.reject_request(selected_request_id, notes=reject_reason):
                                    st.success("Request rejected successfully!")
                                    st.rerun()
                                else:
                                    st.error("Please provide a reason for rejection.")
                    
                    # View DDL
                    with st.expander("View DDL Script"):
                        st.code(request.get('ddl', 'DDL not available'), language="sql")
                        
                        # Add a download button for the DDL
                        st.download_button(
                            label="Download DDL Script",
                            data=request.get('ddl', ''),
                            file_name=f"{request.get('role_name')}_access.sql",
                            mime="text/plain",
                            key=f"download_monitor_ddl_{request.get('id')}"
                        )
        else:
            st.info("No requests match the selected filters.")

    
    def _build_json_for_access_request(self, df, asset_id, selected_tables, selected_purposes, purpose_options):
        """
        Build a JSON structure for the access request based on the filtered policy analysis.
        
        Args:
            df: DataFrame containing filtered policy analysis results
            asset_id: ID of the asset
            selected_tables: List of selected tables
            selected_purposes: List of selected purpose IDs
            purpose_options: Dictionary mapping purpose IDs to names
            
        Returns:
            Dictionary containing policies organized for the access request
        """
        # Initialize the result dictionary
        result = {
            "asset_id": asset_id,
            "tables": {},
            "role_name": f"DATA_ACCESS_{self._generate_random_suffix()}",
            "purposes": [purpose_options[p_id] for p_id in selected_purposes],
            "purpose_ids": selected_purposes
        }
        
        # Get asset name
        assets = self.glossary_repository.get_assets()
        for asset in assets:
            if asset[0] == asset_id:
                result["asset_name"] = asset[1]
                break
        
        # Get all catalog entries for this asset to include ALL columns
        all_columns = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        
        # Filter catalog entries to only include selected tables
        filtered_columns = [
            col for col in all_columns 
            if f"{col['schema_name']}.{col['table_name']}" in selected_tables
        ]
        
        # Create a dictionary of all selected tables and their columns
        for col in filtered_columns:
            schema_name = col.get('schema_name')
            table_name = col.get('table_name')
            column_name = col.get('column_name')
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Initialize table if not exists
            if table_key not in result["tables"]:
                result["tables"][table_key] = {
                    "schema": schema_name,
                    "table": table_name,
                    "columns": {}
                }
            
            # Add column to the table (even if it has no policies)
            if column_name not in result["tables"][table_key]["columns"]:
                result["tables"][table_key]["columns"][column_name] = {
                    "data_element_id": col.get('data_element_id'),
                    "data_element_name": col.get('data_element_name'),
                    "data_type": col.get('data_type'),
                    "roles": {}
                }
        
        # Now add policy information to the columns that have policies
        for _, row in df.iterrows():
            schema_name = row.get('schema_name')
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            purpose_name = row.get('purpose_name')
            role_name = row.get('role_name')
            role_id_val = row.get('role_id', 'default')
            policy_type_name = row.get('policy_type').lower()
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Skip if this table is not in our selected tables
            if table_key not in selected_tables:
                continue
                
            # Initialize role if not exists for this column
            if role_name not in result["tables"][table_key]["columns"][column_name]["roles"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name] = {
                    "role_id": role_id_val,
                    "purposes": {}
                }
            
            # Initialize purpose if not exists for this role and column
            if purpose_name not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name] = {}
            
            # Add policy based on its type
            if policy_type_name == 'security':
                if "security" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["security"] = {
                        "policy_name": row.get('policy_name'),
                        "encryption_required": row.get('encryption_required'),
                        "encryption_algorithm": row.get('encryption_algorithm'),
                        "masking_required": row.get('masking_required'),
                        "masking_format": row.get('masking_format'),
                        "is_override": row.get('is_override', False)
                    }
            elif policy_type_name == 'usage':
                if "usage" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"].append({
                    "policy_name": row.get('policy_name'),
                    "operation": row.get('operation'),
                    "allowed": row.get('allowed'),
                    "restrictions": row.get('restrictions')
                })
            elif policy_type_name == 'retention':
                if "retention" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"].append({
                    "policy_name": row.get('policy_name'),
                    "retention_period": row.get('retention_period'),
                    "retention_condition": row.get('retention_condition'),
                    "is_override": row.get('is_override', False)
                })
        
        return result
    
    def _generate_random_suffix(self, length=4):
        """Generate a random alphanumeric suffix for the role name."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
