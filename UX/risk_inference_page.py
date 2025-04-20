import streamlit as st
import pandas as pd
from core.sensitivity_inference import SensitivityInference
class RiskInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository, obligation_repository):
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.sensitivity_inference = SensitivityInference(
            self.glossary_repository,
            self.regulatory_metadata_repository
        )

    def render(self):
        """Implement a risk inference API based on data sensitivity and obligations.
        This allows users to input data elements and get risk assessments.
        """
        st.markdown("<div class='page-header'><i class='fas fa-exclamation-triangle'></i> &nbsp;Risk Inference API</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Risk Inference API</strong> identifies potential risks if security and privacy obligations are not properly implemented.</p>
            <ul>
                <li>Analyzes data elements to determine their sensitivity levels</li>
                <li>Identifies security and privacy obligations based on sensitivity</li>
                <li>Maps obligations to potential risks if not implemented</li>
                <li>Assesses likelihood and impact of each risk</li>
                <li>Calculates overall risk ratings based on likelihood and impact</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="risk_law")
        
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="risk_dst")
        else:
            st.warning("No data subject types available.")
            return
        
        # Option to select either data element or data category
        data_type = st.radio("Select Data Type", ["Data Element", "Data Category"], key="risk_data_type")
        
        if data_type == "Data Element":
            data_elements = self.glossary_repository.get_data_elements()
            if data_elements:
                de_options = [de["name"] for de in data_elements]
                selected_data = st.selectbox("Select Data Element", options=de_options, key="risk_data_element")
            else:
                st.warning("No data elements available.")
                return
        else:  # Data Category
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data = st.selectbox("Select Data Category", options=dc_options, key="risk_data_category")
            else:
                st.warning("No data categories available.")
                return
        
        # Add a button to trigger inference
        infer_button = st.button("Infer Risks", key="identify_risks_button")
        
        # Show results below the button
        if infer_button:
            st.subheader("Risk Recommendations")
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
                        # Create a list of obligations for risk lookup
                        all_obligations = []
                        for so in sensitivity_obligations:
                            all_obligations.append({
                                "id": so["obligation_id"],
                                "name": so["obligation_name"],
                                "control_type": so["control_type"],
                                "priority": so["priority"]
                            })
                        
                        # Get risks for these obligations
                        st.subheader("Potential Risks")
                        
                        # Get risks for the given obligations from the repository
                        all_risks = []
                        obligation_ids = [o["id"] for o in all_obligations]
                        
                        # Get risks for each obligation using the repository
                        for obligation_id in obligation_ids:
                            risks = self.obligation_repository.get_risks_for_obligation(obligation_id)
                            obligation_name = next((o["name"] for o in all_obligations if o["id"] == obligation_id), "Unknown")
                            
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
                                    key="risk_api_category_filter"
                                )
                            with col2:
                                likelihoods = ["All"] + sorted(list(set(df["Likelihood"])))
                                selected_likelihood = st.selectbox(
                                    "Filter by Likelihood",
                                    likelihoods,
                                    key="risk_api_likelihood_filter"
                                )
                            with col3:
                                impacts = ["All"] + sorted(list(set(df["Impact"])))
                                selected_impact = st.selectbox(
                                    "Filter by Impact",
                                    impacts,
                                    key="risk_api_impact_filter"
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
                            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                                <h4 style=\"margin-top: 0;\">Risk Assessment</h4>
                                <p>If the recommended obligations are not implemented, this data may be exposed to the following risks:</p>
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
                            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                                <h4 style=\"margin-top: 0;\">How the Risk Recommendation Algorithm Works</h4>
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
                    else:
                        st.info(f"No obligations defined for {sensitivity} sensitivity level.")
                else:
                    st.warning(f"Could not find sensitivity ID for {sensitivity}.")
