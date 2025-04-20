import streamlit as st
import pandas as pd

class PolicyRecommendationPage:
    def __init__(self, glossary_repository, obligation_repository, sensitivity_inference):
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.sensitivity_inference = sensitivity_inference

    def render(self):
        """Implement a policy recommendation API based on data sensitivity and obligations.
        This allows users to input data elements and get policy recommendations.
        """
        st.markdown("<div class='page-header'><i class='fas fa-file-contract'></i> &nbsp;Policy Inference API</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Inference API</strong> recommends organizational policies that should be implemented based on the sensitivity of data and associated obligations.</p>
            <ul>
                <li>Analyzes data elements to determine their sensitivity levels</li>
                <li>Identifies security and privacy obligations based on sensitivity</li>
                <li>Maps obligations to relevant organizational policies</li>
                <li>Ranks policies by relevance to the identified obligations</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
            
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="policy_law")
        
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="policy_dst")
        else:
            st.warning("No data subject types available.")
            return
        
        # Option to select either data element or data category
        data_type = st.radio("Select Data Type", ["Data Element", "Data Category"], key="policy_data_type")
        
        if data_type == "Data Element":
            data_elements = self.glossary_repository.get_data_elements()
            if data_elements:
                de_options = [de["name"] for de in data_elements]
                selected_data = st.selectbox("Select Data Element", options=de_options, key="policy_data_element")
            else:
                st.warning("No data elements available.")
                return
        else:  # Data Category
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data = st.selectbox("Select Data Category", options=dc_options, key="policy_data_category")
            else:
                st.warning("No data categories available.")
                return
        
        # Add a button to trigger inference
        infer_button = st.button("Infer Policies", key="recommend_policies_button")
        
        # Show results below the button
        if infer_button:
            st.subheader("Policy Recommendations")
            # First, infer the sensitivity of the data
            sensitivity = self.sensitivity_inference.infer_sensitivity(selected_law, selected_dst, selected_data, data_type)
            
            if sensitivity:
                st.success(f"Data sensitivity inferred: **{sensitivity}**")
                
                # Get sensitivity ID
                all_sensitivities = self.glossary_repository.get_sensitivities()
                sensitivity_id = None
                for s in all_sensitivities:
                    if s["name"] == sensitivity:
                        sensitivity_id = s["id"]
                        break
                
                if sensitivity_id:
                    # Get obligations for this sensitivity
                    sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                    
                    if sensitivity_obligations:
                        # Create a list of obligations for policy lookup
                        all_obligations = []
                        for so in sensitivity_obligations:
                            all_obligations.append({
                                "id": so["obligation_id"],
                                "name": so["obligation_name"],
                                "control_type": so["control_type"],
                                "priority": so["priority"]
                            })
                        
                        # Get policies for these obligations
                        st.subheader("Recommended Policies")
                        
                        # Get policies for the given obligations from the repository
                        all_policies = []
                        obligation_ids = [o["id"] for o in all_obligations]
                        
                        # Get policies for each obligation using the repository
                        for obligation_id in obligation_ids:
                            policies = self.obligation_repository.get_policies_for_obligation(obligation_id)
                            obligation_name = next((o["name"] for o in all_obligations if o["id"] == obligation_id), "Unknown")
                            
                            for policy in policies:
                                all_policies.append({
                                    "Obligation": obligation_name,
                                    "Policy": policy["name"],
                                    "Description": policy["description"],
                                    "Status": policy["status"],
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
                                    key="policy_api_name_filter"
                                )
                            
                            with col2:
                                statuses = ["All"] + sorted(list(set(df["Status"])))
                                selected_status = st.selectbox(
                                    "Filter by Status",
                                    statuses,
                                    key="policy_api_status_filter"
                                )
                            
                            # Apply filters
                            filtered_df = df.copy()
                            if selected_policy != "All":
                                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                            if selected_status != "All":
                                filtered_df = filtered_df[filtered_df["Status"] == selected_status]
                            
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
                            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                                <h4 style=\"margin-top: 0;\">Recommended Policy Implementation</h4>
                                <p>Based on the data elements and their sensitivity levels, the following policies should be implemented:</p>
                                <ol>
                            """, unsafe_allow_html=True)
                            
                            for policy in top_policies[:5]:  # Show top 5 policies
                                st.markdown(f"<li><strong>{policy}</strong></li>", unsafe_allow_html=True)
                            
                            st.markdown("""
                                </ol>
                                <p>These policies will address the compliance obligations required for the sensitive data.</p>
                            </div>
                            
                            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                                <h4 style=\"margin-top: 0;\">How the Policy Recommendation Algorithm Works</h4>
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
                    else:
                        st.info(f"No obligations defined for {sensitivity} sensitivity level.")
                else:
                    st.warning(f"Could not find sensitivity ID for {sensitivity}.")
            else:
                st.warning("Could not determine sensitivity for the selected data.")
