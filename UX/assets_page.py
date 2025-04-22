import streamlit as st
import pandas as pd

class AssetsPage:
    def __init__(self, inventory_repository, glossary_repository, obligation_repository, sensitivity_inference, catalog_repository, regulatory_metadata_repository):
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.sensitivity_inference = sensitivity_inference
        self.catalog_repository = catalog_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

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
        data_element_options = list(data_element_names)
        data_element_options.sort()
        selected_data_elements = st.multiselect(
            "Filter by Data Element",
            options=data_element_options,
            help="Select one or more data elements to filter assets"
        )
        filtered_assets = assets
        if selected_data_elements:
            filtered_asset_ids = set()
            for asset_id, data_elements in asset_to_data_elements.items():
                de_names = {de['name'] for de in data_elements}
                if all(de_name in de_names for de_name in selected_data_elements):
                    filtered_asset_ids.add(asset_id)
            filtered_assets = [asset for asset in assets if asset['id'] in filtered_asset_ids]
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
        df = pd.DataFrame(asset_data)
        df = df.dropna(how='all')
        st.dataframe(df, use_container_width=True, height=min(400, len(df) * 35 + 38))
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
                                                st.markdown("<h4>Policy Implementation Status:</h4>", unsafe_allow_html=True)
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
                
                run_analysis = st.button("Run Asset Analysis", key=f"run_analysis_{selected_asset['id']}")
                # Show info box about analysis workflow
                st.markdown('''
                <div style="background-color: #eaf7ea; padding: 18px 20px; border-radius: 10px; margin-bottom: 18px; border-left: 5px solid #27ae60;">
                    <h4 style="margin-top: 0; color: #229954;">How Policy Recommendation and Risk Analysis Work</h4>
                    <ul style="margin-bottom: 0;">
                        <li><strong>Input:</strong> The analysis starts with the data elements associated with each asset.</li>
                        <li><strong>Sensitivity Inference:</strong> Sensitivity levels for each data element are inferred using regulatory mappings and business logic.</li>
                        <li><strong>Obligation Mapping:</strong> Based on sensitivities, relevant security and privacy obligations are determined for each data element.</li>
                        <li><strong>Policy Recommendation:</strong> For each obligation, recommended policies and controls are identified to help ensure compliance.</li>
                        <li><strong>Risk Analysis:</strong> Potential risks are derived for each obligation if not properly implemented, including likelihood and impact assessment.</li>
                        <li><strong>Risk Rating:</strong> Risks are categorized as Critical, High, Medium, or Low based on a matrix of likelihood and impact.</li>
                        <li><strong>Summary:</strong> The workflow provides a prioritized list of obligations, recommended policies, and potential risks to guide remediation and compliance actions.</li>
                    </ul>
                </div>
                ''', unsafe_allow_html=True)                    
                
                if run_analysis:
                        # 1. Infer sensitivities
                        data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                        if not data_element_sensitivities:
                            st.warning("Could not determine sensitivities for the data elements.")
                            return
                        st.markdown("<h4>Data Element Sensitivity Analysis:</h4>", unsafe_allow_html=True)
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
                        st.markdown("<h4>Recommended Obligations:</h4>", unsafe_allow_html=True)
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
                        st.markdown("<h4>Detailed Policy Recommendations:</h4>", unsafe_allow_html=True)
                        
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
                                                    st.write("**Usage Policies:**")
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
                                                    st.write("**Retention Policies:**")
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
                                                st.write("**Security Policies:**")
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
                        st.markdown("<h4>Potential Risks (by Data Element):</h4>", unsafe_allow_html=True)
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
        st.markdown("<h4>Recommended Policies (by Data Element):</h4>", unsafe_allow_html=True)
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
        
        st.markdown("<h4>Potential Risks:</h4>", unsafe_allow_html=True)
        
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
            st.markdown("<h4>Risk Assessment Summary:</h4>", unsafe_allow_html=True)
            
            # Count risks by rating
            risk_counts = filtered_df["Risk Rating"].value_counts()
            
            # Create a summary message based on risk counts
            summary_message = """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">Risk Assessment</h4>
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