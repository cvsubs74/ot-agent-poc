import streamlit as st
import pandas as pd

class AssetsPage:
    def __init__(self, inventory_repository, glossary_repository, obligation_repository, sensitivity_inference):
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.sensitivity_inference = sensitivity_inference

    def render(self):
        """Render the Assets page with asset inventory, filtering, and inference actions."""
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
                    run_analysis = st.button("Run Data Element Analysis", key=f"run_analysis_{selected_asset['id']}")
                    if run_analysis:
                        # 1. Infer sensitivities
                        data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                        if not data_element_sensitivities:
                            st.warning("Could not determine sensitivities for the data elements.")
                            return
                        st.subheader("Data Element Sensitivity Analysis")
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
                        st.subheader("Recommended Obligations (by Data Element)")
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

                        # 3. Derive policies
                        st.subheader("Recommended Policies (by Data Element)")
                        all_policies = []
                        for de_name, de_obligations in obligations_by_de.items():
                            for obligation in de_obligations:
                                obligation_id = obligation["id"]
                                obligation_name = obligation["name"]
                                policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
                                for policy in policies:
                                    all_policies.append({
                                        "Data Element": de_name,
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

                        # 4. Derive risks
                        st.subheader("Potential Risks (by Data Element)")
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
                else:
                    st.info(f"No data elements associated with {selected_asset['name']}")
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
        st.subheader("Recommended Policies (by Data Element)")
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
        
        st.subheader("Potential Risks")
        
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
            st.subheader("Risk Assessment Summary")
            
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