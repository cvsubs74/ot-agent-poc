import streamlit as st
import pandas as pd
import datetime
import json
from components.DDLGenerator import DDLGenerator
from components.JSONGenerator import JSONGenerator

class DataAccessRequestPage:
    def __init__(self, glossary_repository, catalog_repository, asset_policy_inference, data_access_repository=None):
        """Initialize the Data Access Request page with required repositories."""
        self.glossary_repository = glossary_repository
        self.catalog_repository = catalog_repository
        self.asset_policy_inference = asset_policy_inference
        self.data_access_repository = data_access_repository
        self.ddl_generator = DDLGenerator()
        self.json_generator = JSONGenerator(glossary_repository, catalog_repository)
    
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
                                        # Build the JSON from the filtered DataFrame using the JSONGenerator
                                        policy_json = self.json_generator.build_json_for_access_request(
                                            filtered_df, 
                                            selected_asset_id, 
                                            selected_tables,
                                            selected_purposes,
                                            purpose_options
                                        )
                                        
                                        # The role name is now generated by the JSONGenerator class
                                        role_name = policy_json["role_name"]
                                        
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
                                            
                                        # Display the results - simplified success message
                                        st.markdown(f"""
                                        <div class="success-card card">
                                        <h3>✅ Access Request Submitted Successfully!</h3>
                                        <p><strong>Role Name:</strong> {role_name}</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Display a user-friendly explanation of what the DDL will accomplish
                                        # Get the purposes for a more user-friendly explanation
                                        purpose_names = [purpose_options[p_id] for p_id in selected_purposes]
                                        purpose_list = ", ".join([f"'{p}'" for p in purpose_names])
                                        
                                        # Create a user-friendly explanation using HTML component with scrolling
                                        html_content = f"""
                                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db; font-size: 16px; line-height: 1.5; max-height: 600px; overflow-y: auto;">
                                            <h3 style="color: #2c3e50; font-size: 22px;">How This Data Access Control Works</h3>
                                            
                                            <p>This DDL script creates a secure access control system for the selected tables. Here's what happens when users access this data:</p>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔐 Role-Based Access</h4>
                                            <ul>
                                                <li>A new role <code>{role_name}</code> is created specifically for this access request.</li>
                                                <li>Purpose-specific roles are created for each purpose: {purpose_list}.</li>
                                                <li>Users must be assigned to both the main role and the appropriate purpose roles to access data.</li>
                                            </ul>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔍 Row-Level Security</h4>
                                            <ul>
                                                <li>Users will only see rows where the data subject has explicitly consented to the purposes: {purpose_list}.</li>
                                                <li>Even if a user has the role, they won't see data for individuals who haven't provided consent.</li>
                                                <li>The system checks consent records in real-time when queries are executed.</li>
                                            </ul>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🛡️ Column-Level Masking</h4>
                                            <ul>
                                                <li>Sensitive data like emails, phone numbers, and personal identifiers are masked by default.</li>
                                                <li>Users will only see unmasked sensitive data if they have the appropriate purpose role.</li>
                                                <li>Non-sensitive data is always visible (if row-level access is granted).</li>
                                            </ul>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">🔒 Secure Implementation</h4>
                                            <ul>
                                                <li>Original tables are protected - users can only access secure views.</li>
                                                <li>All access is logged and auditable.</li>
                                                <li>No administrative privileges are granted to regular users.</li>
                                            </ul>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">📋 Your Configuration Summary</h4>
                                            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                                <p><strong>Asset:</strong> {policy_json.get('asset_name', 'Selected Asset')}</p>
                                                <p><strong>Tables:</strong> {', '.join(selected_tables)}</p>
                                                <p><strong>Purposes:</strong> {purpose_list}</p>
                                                <p><strong>Role Created:</strong> <code>{role_name}</code></p>
                                            </div>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">📚 Privacy & Compliance Rationale</h4>
                                            <div style="background-color: #f0f9ff; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                                <p><strong>Data Privacy Compliance:</strong> This access control system ensures that data is only accessed in accordance with privacy regulations like GDPR, CCPA, and HIPAA.</p>
                                                <p><strong>Purpose Limitation:</strong> By creating purpose-specific roles, we enforce the principle that data should only be used for the specific purposes for which consent was given.</p>
                                                <p><strong>Data Minimization:</strong> Users only see the specific tables and columns they need for their authorized purposes, reducing unnecessary data exposure.</p>
                                                <p><strong>Consent Management:</strong> The row-level security ensures that only data from individuals who have explicitly consented to the specified purposes is accessible.</p>
                                                <p><strong>Auditability:</strong> All access is logged and can be audited to demonstrate compliance with privacy regulations.</p>
                                            </div>
                                            
                                            <h4 style="color: #2980b9; font-size: 18px; margin-top: 20px;">💡 Example Scenario</h4>
                                            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                                <p>When a user with role <code>{role_name}</code> and purpose role <code>PURPOSE_{purpose_names[0].upper().replace(' ', '_')}</code> 
                                                queries the data, they will only see records for individuals who have explicitly consented to <code>{purpose_names[0]}</code>. 
                                                Sensitive fields will only be visible for that specific purpose, and all access will be logged for audit purposes.</p>
                                                
                                                <p>For example, if a marketing analyst needs to access customer data for a campaign, they will only see data for customers who have consented to marketing communications, 
                                                and sensitive information like full addresses or financial details will remain masked unless specifically authorized.</p>
                                            </div>
                                        </div>
                                        """
                                        st.components.v1.html(html_content, height=700)
                                        
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

    
    # The _build_json_for_access_request method has been refactored to the JSONGenerator class
    
    # The _generate_random_suffix method has been refactored to the JSONGenerator class
