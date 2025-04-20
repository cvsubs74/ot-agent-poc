import streamlit as st
import pandas as pd

from core.sensitivity_inference import SensitivityInference

class ObligationInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository, obligation_repository):
        self.glossary_repository = glossary_repository
        self.obligation_repository = obligation_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.sensitivity_inference = SensitivityInference(
            self.glossary_repository,
            self.regulatory_metadata_repository
        )

    def render(self):
        """Implement an obligation inference API based on data sensitivity."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Obligation Inference</div>", unsafe_allow_html=True)
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Obligation Inference API</strong> determines what security and privacy controls should be implemented based on the sensitivity of the data you're handling.</p>
            <ul>
                <li>Analyzes data elements to determine their sensitivity levels</li>
                <li>Maps sensitivities to appropriate security and privacy obligations</li>
                <li>Prioritizes obligations based on data sensitivity</li>
                <li>Groups obligations by control type for easier implementation</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="obligation_law")

        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="obligation_dst")
        else:
            st.warning("No data subject types available.")
            return

        data_elements = self.glossary_repository.get_data_elements()
        if not data_elements:
            st.warning("No data elements available.")
            return
        data_element_options = [de["name"] for de in data_elements]
        selected_data_elements = st.multiselect(
            "Select Data Elements",
            options=data_element_options,
            key="api_infer_obligations_data_elements"
        )
        analyze_button = st.button("Run Obligation Inference API")

        if analyze_button and selected_data_elements:
            st.subheader("Inferred Sensitivities for Selected Data Elements")
            sensitivity_data = []
            data_element_sensitivities = {}
            for data_element in selected_data_elements:
                sensitivity = self.sensitivity_inference.infer_sensitivity(
                    selected_law, selected_dst, data_element, "Data Element"
                )
                if sensitivity:
                    data_element_sensitivities[data_element] = sensitivity
                    sensitivity_data.append({
                        "Data Element": data_element,
                        "Sensitivity": sensitivity,
                        "Source": f"Inferred from {selected_law} for {selected_dst}"
                    })
                else:
                    data_element_sensitivities[data_element] = "Unknown"
                    sensitivity_data.append({
                        "Data Element": data_element,
                        "Sensitivity": "Unknown",
                        "Source": "No sensitivity mapping found"
                    })
            sensitivity_df = pd.DataFrame(sensitivity_data)
            st.dataframe(sensitivity_df, use_container_width=True)
            st.subheader("Recommended Obligations Based on Sensitivities")
            all_sensitivities = self.glossary_repository.get_sensitivities()
            sensitivity_name_to_id = {s["name"]: s["id"] for s in all_sensitivities}
            obligations_by_type = {}
            for data_element, sensitivity in data_element_sensitivities.items():
                if sensitivity != "Unknown" and sensitivity in sensitivity_name_to_id:
                    sensitivity_id = sensitivity_name_to_id[sensitivity]
                    sensitivity_obligations = self.obligation_repository.get_sensitivity_obligations(sensitivity_id)
                    for obligation in sensitivity_obligations:
                        control_type = obligation["control_type"]
                        if control_type not in obligations_by_type:
                            obligations_by_type[control_type] = []
                        obligations_by_type[control_type].append({
                            "Data Element": data_element,
                            "Sensitivity": sensitivity,
                            "Obligation Name": obligation["obligation_name"],
                            "Description": obligation["obligation_description"],
                            "Priority": obligation["priority"]
                        })
            if obligations_by_type:
                all_obligations = []
                for control_type, obligations in obligations_by_type.items():
                    for obligation in obligations:
                        all_obligations.append({
                            "Control Type": control_type,
                            "Data Element": obligation["Data Element"],
                            "Sensitivity": obligation["Sensitivity"],
                            "Obligation": obligation["Obligation Name"],
                            "Description": obligation["Description"],
                            "Priority": obligation["Priority"]
                        })
                df = pd.DataFrame(all_obligations)
                col1, col2, col3 = st.columns(3)
                with col1:
                    control_types = ["All"] + sorted(list(set(df["Control Type"])))
                    selected_control = st.selectbox(
                        "Filter by Control Type",
                        control_types,
                        key="obligation_api_control_filter"
                    )
                with col2:
                    priorities = ["All"] + sorted(list(set(df["Priority"])))
                    selected_priority = st.selectbox(
                        "Filter by Priority",
                        priorities,
                        key="obligation_api_priority_filter"
                    )
                with col3:
                    data_elements_filter = ["All"] + sorted(list(set(df["Data Element"])))
                    selected_data_element = st.selectbox(
                        "Filter by Data Element",
                        data_elements_filter,
                        key="obligation_api_data_element_filter"
                    )
                filtered_df = df.copy()
                if selected_control != "All":
                    filtered_df = filtered_df[filtered_df["Control Type"] == selected_control]
                priority_order = {"High": 0, "Medium": 1, "Low": 2}
                all_obligations.sort(key=lambda x: priority_order.get(x["Priority"], 99))
                obligations_df = pd.DataFrame(all_obligations)
                st.dataframe(obligations_df, use_container_width=True)
                st.markdown("""
                <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                                <h4 style=\"margin-top: 0;\">How the Obligation Inference Algorithm Works</h4>
                                <p>The algorithm follows this functional flow:</p>
                                <ul>
                                    <li><strong>Input:</strong> Data elements from the selected asset</li>
                                    <li><strong>Sensitivity Analysis:</strong> Determine sensitivity level for each data element</li>
                                    <li><strong>Obligation Mapping:</strong> Match sensitivities to relevant security and privacy obligations</li>
                                    <li><strong>Priority Assignment:</strong> Assign implementation priority based on data sensitivity</li>
                                    <li><strong>Output:</strong> Prioritized list of security and privacy obligations</li>
                                </ul>
                                <p>The recommendations are prioritized as follows:</p>
                                <ul>
                                    <li><strong>High Priority:</strong> Critical controls that must be implemented to protect sensitive data</li>
                                    <li><strong>Medium Priority:</strong> Important controls that should be implemented in most cases</li>
                                    <li><strong>Low Priority:</strong> Recommended controls that enhance protection but may be optional</li>
                                </ul>
                            </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No obligations found for the inferred sensitivity levels.")
        elif analyze_button and not selected_data_elements:
            st.warning("Please select at least one data element.")
