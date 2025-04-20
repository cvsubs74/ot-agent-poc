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
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        infer_obligations = st.button("Infer Obligations", key=f"infer_obligations_{selected_asset['id']}")
                    with col2:
                        recommend_policies = st.button("Recommend Policies", key=f"recommend_policies_{selected_asset['id']}")
                    with col3:
                        recommend_risks = st.button("Recommend Risks", key=f"recommend_risks_{selected_asset['id']}")
                    if infer_obligations:
                        data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                        if data_element_sensitivities:
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
                            self.show_sensitivity_based_obligations(data_element_sensitivities)
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                    if recommend_policies:
                        data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                        if data_element_sensitivities:
                            sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
                            all_sensitivities = self.glossary_repository.get_sensitivities()
                            sensitivity_ids = {}
                            for sensitivity in all_sensitivities:
                                if sensitivity['name'] in sensitivity_levels:
                                    sensitivity_ids[sensitivity['name']] = sensitivity['id']
                            all_obligations = []
                            for sensitivity_name, sensitivity_id in sensitivity_ids.items():
                                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                                if sensitivity_obligations:
                                    for so in sensitivity_obligations:
                                        all_obligations.append({
                                            "id": so["obligation_id"],
                                            "name": so["obligation_name"],
                                            "control_type": so["control_type"],
                                            "priority": so["priority"]
                                        })
                            if all_obligations:
                                self.show_obligation_based_policies(all_obligations)
                            else:
                                st.warning("No obligations found for the sensitivities.")
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                    if recommend_risks:
                        data_element_sensitivities = self.sensitivity_inference.infer_data_element_sensitivities(data_elements)
                        if data_element_sensitivities:
                            sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
                            all_sensitivities = self.glossary_repository.get_sensitivities()
                            sensitivity_ids = {}
                            for sensitivity in all_sensitivities:
                                if sensitivity['name'] in sensitivity_levels:
                                    sensitivity_ids[sensitivity['name']] = sensitivity['id']
                            all_obligations = []
                            for sensitivity_name, sensitivity_id in sensitivity_ids.items():
                                sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                                if sensitivity_obligations:
                                    for so in sensitivity_obligations:
                                        all_obligations.append({
                                            "id": so["obligation_id"],
                                            "name": so["obligation_name"],
                                            "control_type": so["control_type"],
                                            "priority": so["priority"]
                                        })
                            if all_obligations:
                                self.show_obligation_based_risks(all_obligations)
                            else:
                                st.warning("No obligations found for the sensitivities.")
                        else:
                            st.warning("Could not determine sensitivities for the data elements.")
                else:
                    st.info(f"No data elements associated with {selected_asset['name']}")
                st.markdown('</div>', unsafe_allow_html=True)

    def show_sensitivity_based_obligations(self, data_element_sensitivities):
        """Show obligations based on data element sensitivities.
        
        Args:
            data_element_sensitivities: Dictionary mapping data element names to sensitivity info dictionaries
                                        with 'sensitivity' and 'source' keys
        """
        if not data_element_sensitivities:
            st.warning("No sensitivity information available.")
            return
        
        # Get unique sensitivity levels
        sensitivity_levels = set(item['sensitivity'] for item in data_element_sensitivities.values())
        
        # Get sensitivity IDs for these levels
        all_sensitivities = self.glossary_repository.get_sensitivities()
        sensitivity_ids = {}
        for sensitivity in all_sensitivities:
            if sensitivity['name'] in sensitivity_levels:
                sensitivity_ids[sensitivity['name']] = sensitivity['id']
        # Get obligations for these sensitivity levels
        st.subheader("Recommended Obligations")
        
        all_obligations = []
        for sensitivity_name, sensitivity_id in sensitivity_ids.items():
            # Get sensitivity obligations
            sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
            
            if sensitivity_obligations:
                # Group by control type
                for so in sensitivity_obligations:
                    all_obligations.append({
                        "Sensitivity": sensitivity_name,
                        "Obligation": so["obligation_name"],
                        "Description": so["obligation_description"],
                        "Control Type": so["control_type"],
                        "Priority": so["priority"]
                    })
        
        if all_obligations:
            # Create a DataFrame
            df = pd.DataFrame(all_obligations)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                control_types = ["All"] + sorted(list(set(df["Control Type"])))
                selected_control = st.selectbox(
                    "Filter by Control Type",
                    control_types,
                    key="obligation_control_filter"
                )
            
            with col2:
                priorities = ["All"] + sorted(list(set(df["Priority"])))
                selected_priority = st.selectbox(
                    "Filter by Priority",
                    priorities,
                    key="obligation_priority_filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_control != "All":
                filtered_df = filtered_df[filtered_df["Control Type"] == selected_control]
            if selected_priority != "All":
                filtered_df = filtered_df[filtered_df["Priority"] == selected_priority]
            
            # Sort by Priority and Control Type
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            filtered_df["Priority Order"] = filtered_df["Priority"].map(priority_order)
            filtered_df = filtered_df.sort_values(by=["Priority Order", "Control Type"])
            filtered_df = filtered_df.drop(columns=["Priority Order"])
            
            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True)
            
            # Add explanation
            st.markdown("""
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How the Obligation Inference Algorithm Works</h4>
                <p>The algorithm follows this functional flow:</p>
                <ul>
                    <li><strong>Input:</strong> Data elements from the selected asset</li>
                    <li><strong>Sensitivity Analysis:</strong> Determine sensitivity level for each data element</li>
                    <li><strong>Obligation Mapping:</strong> Match sensitivities to relevant security and privacy obligations</li>
                    <li><strong>Control Categorization:</strong> Group obligations by control type (Encryption, Access Control, etc.)</li>
                    <li><strong>Priority Assignment:</strong> Assign implementation priority based on data sensitivity</li>
                    <li><strong>Output:</strong> Prioritized list of security and privacy obligations</li>
                </ul>
                <p>The recommendations are prioritized as follows:</p>
                <ul>
                    <li><strong>High Priority:</strong> Critical controls that must be implemented to protect sensitive data</li>
                    <li><strong>Medium Priority:</strong> Important controls that should be implemented in most cases</li>
                    <li><strong>Low Priority:</strong> Recommended controls that enhance protection but may be optional</li>
                </ul>
                <p>These obligations can be used to guide your security and compliance implementation for this asset.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No obligations defined for these sensitivity levels.")

    def show_obligation_based_policies(self, obligations):
        """Show policies based on obligations.
        
        Args:
            obligations: List of obligation dictionaries with 'id', 'name', 'control_type', and 'priority' keys
        """
        if not obligations:
            st.warning("No obligation information available.")
            return
        
        st.subheader("Recommended Policies")
        
        # Get policies for the given obligations from the repository
        all_policies = []
        obligation_ids = [o["id"] for o in obligations]
        
        # Get policies for each obligation using the repository
        for obligation_id in obligation_ids:
            policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
            obligation_name = next((o["name"] for o in obligations if o["id"] == obligation_id), "Unknown")
            
            for policy in policies:
                all_policies.append({
                    "Obligation": obligation_name,
                    "Policy": policy["name"],
                    "Control Type": policy.get("control_type", ""),
                    "Relevance Score": policy["relevance_score"]
                })
        
        if all_policies:
            # Create a DataFrame
            df = pd.DataFrame(all_policies)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                policy_names = ["All"] + sorted(list(set(df["Policy"])))
                selected_policy = st.selectbox(
                    "Filter by Policy",
                    policy_names,
                    key="policy_name_filter"
                )
            
            with col2:
                control_types = ["All"] + sorted(list(set(df["Control Type"])))
                selected_control = st.selectbox(
                    "Filter by Control Type",
                    control_types,
                    key="policy_control_filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_policy != "All":
                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
            if selected_control != "All":
                filtered_df = filtered_df[filtered_df["Control Type"] == selected_control]
            
            # Sort by Relevance Score (descending)
            filtered_df = filtered_df.sort_values(by=["Relevance Score"], ascending=False)
            
            # Display the dataframe
            st.dataframe(filtered_df, use_container_width=True)
            
            # Group policies by type
            policy_groups = filtered_df.groupby("Policy")["Relevance Score"].max().sort_values(ascending=False)
            top_policies = policy_groups.index.tolist()
            
            # Display top policies summary
            st.subheader("Policy Implementation Summary")
            st.markdown("""
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">Recommended Policy Implementation</h4>
                <p>Based on the data elements in this asset and their sensitivity levels, the following policies should be implemented:</p>
                <ol>
            """, unsafe_allow_html=True)
            
            for policy in top_policies[:5]:  # Show top 5 policies
                st.markdown(f"<li><strong>{policy}</strong></li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ol>
                <p>These policies will address the compliance obligations required for the sensitive data in this asset.</p>
            </div>
            
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How the Policy Recommendation Algorithm Works</h4>
                <p>The algorithm follows this functional flow:</p>
                <ul>
                    <li><strong>Input:</strong> Security and privacy obligations from sensitivity analysis</li>
                    <li><strong>Policy Discovery:</strong> Identify organizational policies that address each obligation</li>
                    <li><strong>Relevance Assessment:</strong> Determine how relevant each policy is to the specific obligations</li>
                    <li><strong>Policy Prioritization:</strong> Rank policies by their relevance to the identified obligations</li>
                    <li><strong>Policy Grouping:</strong> Group related policies to provide comprehensive coverage</li>
                    <li><strong>Output:</strong> Prioritized list of policies to implement for the asset</li>
                </ul>
                <p>The relevance score indicates how important each policy is for addressing the identified obligations.</p>
            </div>
            """, unsafe_allow_html=True)
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
                    "Obligation": obligation_name,
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
            display_columns = ["Risk", "Risk Category", "Likelihood", "Impact", "Risk Rating", "Obligation"]
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