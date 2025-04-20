import streamlit as st

class ControlInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Display the Control Inference page to recommend controls based on frameworks, policies, or risks."""
        st.header("Control Inference API")
        st.markdown("Recommend appropriate controls based on frameworks, policies, or risks.")
        
        # Create tabs for different inference sources
        source_tabs = st.tabs(["Policy-Based", "Risk-Based", "Framework-Based"])
        
        # Policy-Based Control Inference
        with source_tabs[0]:
            policies = self.glossary_repository.get_policies()
            if not policies:
                st.warning("No policies available in the database.")
                return
            selected_policy_id = st.selectbox(
                "Select Policy",
                options=[p["id"] for p in policies],
                format_func=lambda x: next((p["name"] for p in policies if p["id"] == x), "Unknown"),
                key="policy_control_inference"
            )
            analyze_button = st.button("Recommend Controls", key="policy_controls_button")
            if analyze_button and selected_policy_id:
                policy_name = next((p["name"] for p in policies if p["id"] == selected_policy_id), "Unknown")
                policy_controls_list = self.regulatory_metadata_repository.get_policy_controls(policy_id=selected_policy_id)
                policy_controls = {}
                if policy_controls_list:
                    policy_controls[selected_policy_id] = policy_controls_list
                if selected_policy_id in policy_controls:
                    controls = policy_controls[selected_policy_id]
                    control_types = set(c["control_type"] for c in controls)
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        type_controls.sort(key=lambda x: x["relevance_score"], reverse=True)
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Relevance: {control['relevance_score']:.1f})", expanded=True):
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_policy_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {policy_name}.")
        
        # Risk-Based Control Inference
        with source_tabs[1]:
            risks = self.glossary_repository.get_risks()
            if not risks:
                st.warning("No risks available in the database.")
                return
            selected_risk_id = st.selectbox(
                "Select Risk",
                options=[r["id"] for r in risks],
                format_func=lambda x: next((r["name"] for r in risks if r["id"] == x), "Unknown"),
                key="risk_control_inference"
            )
            analyze_button = st.button("Recommend Controls", key="risk_controls_button")
            if analyze_button and selected_risk_id:
                risk_name = next((r["name"] for r in risks if r["id"] == selected_risk_id), "Unknown")
                risk_controls_list = self.regulatory_metadata_repository.get_risk_controls(risk_id=selected_risk_id)
                risk_controls = {}
                if risk_controls_list:
                    risk_controls[selected_risk_id] = risk_controls_list
                if selected_risk_id in risk_controls:
                    controls = risk_controls[selected_risk_id]
                    control_types = set(c["control_type"] for c in controls)
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        mitigation_order = {"High": 0, "Medium": 1, "Low": 2}
                        type_controls.sort(key=lambda x: mitigation_order.get(x["mitigation_level"], 99))
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Mitigation: {control['mitigation_level']})", expanded=True):
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_risk_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {risk_name}.")
        
        # Framework-Based Control Inference
        with source_tabs[2]:
            frameworks = self.glossary_repository.get_frameworks()
            if not frameworks:
                st.warning("No frameworks available in the database.")
                return
            st.subheader("Input Parameters")
            selected_framework_id = st.selectbox(
                "Select Framework",
                options=[f["id"] for f in frameworks],
                format_func=lambda x: next((f["name"] for f in frameworks if f["id"] == x), "Unknown"),
                key="framework_control_inference"
            )
            analyze_button = st.button("Recommend Controls", key="framework_controls_button")
            if analyze_button and selected_framework_id:
                framework_name = next((f["name"] for f in frameworks if f["id"] == selected_framework_id), "Unknown")
                framework_controls_list = self.regulatory_metadata_repository.get_framework_controls(framework_id=selected_framework_id)
                framework_controls = {}
                if framework_controls_list:
                    framework_controls[selected_framework_id] = framework_controls_list
                if selected_framework_id in framework_controls:
                    controls = framework_controls[selected_framework_id]
                    control_types = set(c["control_type"] for c in controls)
                    for control_type in control_types:
                        st.markdown(f"#### {control_type} Controls")
                        type_controls = [c for c in controls if c["control_type"] == control_type]
                        type_controls.sort(key=lambda x: x["relevance_score"], reverse=True)
                        for control in type_controls:
                            with st.expander(f"{control['control_name']} (Relevance: {control['relevance_score']:.1f})", expanded=True):
                                st.markdown(f"**Control Type:** {control['control_type']}")
                                st.markdown(f"**Implementation Status:** {control['implementation_status']}")
                                st.markdown(f"**Priority:** {control['priority']}")
                                if st.button(f"Implement Control: {control['control_name']}", key=f"implement_framework_{control['control_id']}"):
                                    st.success(f"Implementation of '{control['control_name']}' has been initiated.")
                else:
                    st.info(f"No control recommendations available for {framework_name}.")
