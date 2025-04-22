import streamlit as st
import pandas as pd

from UX.decision_tree_renderer import DecisionTreeRenderer

class PolicyInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository=None):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    @staticmethod
    def explain():
        st.markdown(
            """
            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                <h4 style=\"margin-top: 0;\">How Policy Inference Works</h4>
                <p>The Policy Inference API uses sensitivity and obligation mappings to recommend organizational policies based on data sensitivity and obligations:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories for classification.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Determines sensitivity levels for data categories.</li>
                    <li><strong>Sensitivity Obligations</strong>: Maps sensitivity levels to security and privacy obligations.</li>
                    <li><strong>Obligation Policy</strong>: Maps security and privacy obligations to organizational policies that should be implemented.</li>
                </ul>
                <p>The Policy Inference process follows these steps:</p>
                <ol>
                    <li>First, determine the sensitivity level of the data using the Data Sensitivity Inference algorithm</li>
                    <li>Identify applicable security and privacy obligations based on the sensitivity level</li>
                    <li>Map these obligations to relevant organizational policies using the Obligation Policy mapping</li>
                    <li>Calculate a relevance score for each policy based on how many obligations it addresses</li>
                    <li>Present a prioritized list of recommended policies to implement</li>
                </ol>
                <p>This approach helps organizations implement a comprehensive policy framework that addresses their specific data protection requirements and ensures compliance with relevant regulations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render(self):
        """Implement the Policy Inference API for access governance.
        This helps determine whether access to data is permitted based on purpose limitation principles.
        """
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Inference API</div>", unsafe_allow_html=True)
        
        # Description
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Inference API</strong> determines whether access to data is permitted based on purpose limitation principles and organizational policies.</p>
            <p>This API helps enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations.</p>
            <br>
            <ul>
                <li>Enforces purpose limitation principles</li>
                <li>Determines data access permissions based on business purpose</li>
                <li>Applies policy-based restrictions on data usage</li>
                <li>Provides clear decision rationale</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get purposes for dropdown selection
        try:
            purposes = self.glossary_repository.get_purposes()
            purpose_options = [purpose["name"] for purpose in purposes] if purposes else ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
        except Exception as e:
            st.warning(f"Error loading purposes: {e}")
            purpose_options = ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
            
        selected_purpose = st.selectbox("Select Business Purpose", options=purpose_options, key="policy_purpose")
        
        # Get data elements for multiselect
        try:
            data_elements = self.glossary_repository.get_data_elements()
            data_element_options = [de["name"] for de in data_elements] if data_elements else ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
        except Exception as e:
            st.warning(f"Error loading data elements: {e}")
            data_element_options = ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
            
        selected_data_elements = st.multiselect("Select Data Elements", options=data_element_options, key="policy_data_elements")
        
        # Operation selection
        operations = ["read", "write", "share"]
        selected_operation = st.selectbox("Select Operation", options=operations, key="policy_operation")
        
        try:
            jurisdictions = self.glossary_repository.get_jurisdictions()
            jurisdiction_options = ["Any"] + [j["name"] for j in jurisdictions] if jurisdictions else ["Any", "California", "European Union", "United Kingdom", "Canada"]
        except Exception as e:
            jurisdiction_options = ["Any", "California", "European Union", "United Kingdom", "Canada"]
            
        selected_jurisdiction = st.selectbox("Select Jurisdiction (Optional)", options=jurisdiction_options, key="policy_jurisdiction")
        
        analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")
        
        # Define nodes for the decision tree
        nodes = [
            {"id": "request", "label": "Access Request", "color": "#3498db", "shape": "ellipse", "size": 30},
            {"id": "purpose", "label": "Business Purpose", "color": "#e74c3c", "shape": "box", "size": 25},
            {"id": "policy", "label": "Applicable Policy", "color": "#9b59b6", "shape": "box", "size": 25},
            {"id": "data_elements", "label": "Data Elements", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "operation", "label": "Operation Type", "color": "#2ecc71", "shape": "box", "size": 25},
            {"id": "lookup", "label": "Policy Compliance Check", "color": "#1abc9c", "shape": "box", "size": 25},
            {"id": "allowed", "label": "Access Decision", "color": "#3498db", "shape": "box", "size": 25},
            {"id": "restrictions", "label": "Usage Restrictions", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "rationale", "label": "Decision Rationale", "color": "#e74c3c", "shape": "box", "size": 25}
        ]
        
        # Define edges for the decision tree
        edges = [
            {"source": "request", "target": "purpose", "arrows": "to", "label": "has"},
            {"source": "purpose", "target": "policy", "arrows": "to", "label": "governed by"},
            {"source": "request", "target": "data_elements", "arrows": "to", "label": "requests"},
            {"source": "request", "target": "operation", "arrows": "to", "label": "performs"},
            {"source": "purpose", "target": "lookup", "arrows": "to"},
            {"source": "data_elements", "target": "lookup", "arrows": "to"},
            {"source": "operation", "target": "lookup", "arrows": "to"},
            {"source": "policy", "target": "lookup", "arrows": "to"},
            {"source": "lookup", "target": "allowed", "arrows": "to"},
            {"source": "lookup", "target": "restrictions", "arrows": "to"},
            {"source": "lookup", "target": "rationale", "arrows": "to"}
        ]
        
        if analyze_button:
            if not selected_data_elements:
                st.warning("Please select at least one Data Element")
            else:
                # Get data element IDs for the selected data elements
                data_elements = self.glossary_repository.get_data_elements()
                selected_data_element_ids = []
                
                for de_name in selected_data_elements:
                    # Find the data element ID for this name
                    data_element = next((de for de in data_elements if de['name'] == de_name), None)
                    if data_element:
                        selected_data_element_ids.append(data_element['id'])
                
                if not selected_data_element_ids:
                    st.warning("Could not find the selected data elements in the database.")
                    return
                
                # 1. Data Element Level Policies
                st.subheader("Data Element Level Policies")
                st.markdown("These policies apply to the data elements regardless of purpose or role.")
                
                # For each data element, get the policy details
                for i, de_name in enumerate(selected_data_elements):
                    if i < len(selected_data_element_ids):
                        data_element_id = selected_data_element_ids[i]
                        
                        # Get policy details for this data element
                        policy_details = self.regulatory_metadata_repository.get_data_element_policies(data_element_id)
                        
                        if any(policy_details.values()):
                            with st.expander(f"Policy Details for {de_name}"):
                                # Show usage policies
                                if policy_details.get('usage'):
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
                                if policy_details.get('retention'):
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
                                if policy_details.get('security'):
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
                
                # 2. Purpose-Specific Policies
                if selected_purpose:
                    st.subheader(f"Purpose-Specific Policies: {selected_purpose}")
                    st.markdown("These policies apply to the data elements when used for the selected purpose.")
                    
                    # Get purpose ID
                    purposes = self.glossary_repository.get_purposes()
                    purpose_id = next((p['id'] for p in purposes if p['name'] == selected_purpose), None)
                    
                    if purpose_id:
                        for i, de_name in enumerate(selected_data_elements):
                            if i < len(selected_data_element_ids):
                                data_element_id = selected_data_element_ids[i]
                                
                                # Get policy-purpose-data element details
                                with st.expander(f"{de_name} - {selected_purpose} Policies"):
                                    # Get policy purpose data element relationships
                                    ppde = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
                                        purpose_id=purpose_id
                                    )
                                    
                                    # Filter for the current data element
                                    ppde = [p for p in ppde if p['data_element_id'] == data_element_id]
                                    
                                    if ppde:
                                        # Display usage rules
                                        usage_rules = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                                            purpose_id=purpose_id,
                                            data_element_id=data_element_id
                                        )
                                        
                                        if usage_rules:
                                            st.write("**Usage Rules:**")
                                            usage_data = {
                                                "Policy": [],
                                                "Operation": [],
                                                "Allowed": [],
                                                "Restrictions": []
                                            }
                                            
                                            for rule in usage_rules:
                                                usage_data["Policy"].append(rule['policy_name'])
                                                usage_data["Operation"].append(rule['operation'])
                                                usage_data["Allowed"].append("Yes" if rule['allowed'] else "No")
                                                usage_data["Restrictions"].append(rule['restrictions'] or "")
                                            
                                            st.dataframe(pd.DataFrame(usage_data), use_container_width=True)
                                        
                                        # Display retention rules
                                        retention_rules = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                                            purpose_id=purpose_id,
                                            data_element_id=data_element_id
                                        )
                                        
                                        if retention_rules:
                                            st.write("**Retention Rules:**")
                                            retention_data = {
                                                "Policy": [],
                                                "Retention Period": [],
                                                "Retention Basis": [],
                                                "Exceptions": []
                                            }
                                            
                                            for rule in retention_rules:
                                                retention_data["Policy"].append(rule['policy_name'])
                                                retention_data["Retention Period"].append(rule['retention_period'])
                                                retention_data["Retention Basis"].append(rule['retention_basis'] or "")
                                                retention_data["Exceptions"].append(rule['exceptions'] or "")
                                            
                                            st.dataframe(pd.DataFrame(retention_data), use_container_width=True)
                                        
                                        # Display security rules
                                        security_rules = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                            purpose_id=purpose_id,
                                            data_element_id=data_element_id
                                        )
                                        
                                        if security_rules:
                                            st.write("**Security Rules:**")
                                            security_data = {
                                                "Policy": [],
                                                "Encryption": [],
                                                "Masking": [],
                                                "Access Logging": []
                                            }
                                            
                                            for rule in security_rules:
                                                security_data["Policy"].append(rule['policy_name'])
                                                security_data["Encryption"].append("Yes - " + rule['encryption_algorithm'] if rule['encryption_required'] and rule['encryption_algorithm'] else "Yes" if rule['encryption_required'] else "No")
                                                security_data["Masking"].append("Yes - " + rule['masking_format'] if rule['masking_required'] and rule['masking_format'] else "Yes" if rule['masking_required'] else "No")
                                                security_data["Access Logging"].append("Yes" if rule['access_logging'] else "No")
                                            
                                            st.dataframe(pd.DataFrame(security_data), use_container_width=True)
                                    else:
                                        st.info(f"No specific policies defined for {de_name} when used for {selected_purpose}.")
                    else:
                        st.warning(f"Could not find purpose '{selected_purpose}' in the database.")
                
                # 3. Role-Specific Overrides
                if selected_purpose:
                    st.subheader("Role-Specific Policy Overrides")
                    st.markdown("These overrides apply to specific roles when accessing the data elements for the selected purpose.")
                    
                    # Get external roles
                    roles = self.glossary_repository.get_external_roles()
                    
                    if roles:
                        role_options = [role['name'] for role in roles]
                        selected_role = st.selectbox("Select Role", options=["None"] + role_options)
                        
                        if selected_role != "None":
                            role_id = next((r['id'] for r in roles if r['name'] == selected_role), None)
                            
                            if role_id and purpose_id:
                                for i, de_name in enumerate(selected_data_elements):
                                    if i < len(selected_data_element_ids):
                                        data_element_id = selected_data_element_ids[i]
                                        
                                        # Get policy purpose data element ID
                                        ppde = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
                                            purpose_id=purpose_id
                                        )
                                        
                                        # Filter for the current data element
                                        ppde = [p for p in ppde if p['data_element_id'] == data_element_id]
                                        
                                        if ppde:
                                            ppde_id = ppde[0]['id']
                                            
                                            with st.expander(f"{selected_role} Overrides for {de_name}"):
                                                # Get usage overrides
                                                usage_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_usage(
                                                    policy_purpose_data_element_id=ppde_id,
                                                    external_role_id=role_id
                                                )
                                                
                                                if usage_overrides:
                                                    st.write("**Usage Overrides:**")
                                                    usage_data = {
                                                        "Operation": [],
                                                        "Allowed": [],
                                                        "Restrictions": []
                                                    }
                                                    
                                                    for override in usage_overrides:
                                                        usage_data["Operation"].append(override['operation'])
                                                        usage_data["Allowed"].append("Yes" if override['allowed'] else "No")
                                                        usage_data["Restrictions"].append(override['restrictions'] or "")
                                                    
                                                    st.dataframe(pd.DataFrame(usage_data), use_container_width=True)
                                                else:
                                                    st.info(f"No usage overrides for {selected_role} role.")
                                                
                                                # Get retention overrides
                                                retention_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_retention(
                                                    policy_purpose_data_element_id=ppde_id,
                                                    external_role_id=role_id
                                                )
                                                
                                                if retention_overrides:
                                                    st.write("**Retention Overrides:**")
                                                    retention_data = {
                                                        "Retention Period": [],
                                                        "Justification": []
                                                    }
                                                    
                                                    for override in retention_overrides:
                                                        retention_data["Retention Period"].append(override['retention_period'])
                                                        retention_data["Justification"].append(override['retention_justification'] or "")
                                                    
                                                    st.dataframe(pd.DataFrame(retention_data), use_container_width=True)
                                                else:
                                                    st.info(f"No retention overrides for {selected_role} role.")
                                                
                                                # Get security overrides
                                                security_overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_security(
                                                    policy_purpose_data_element_id=ppde_id,
                                                    external_role_id=role_id
                                                )
                                                
                                                if security_overrides:
                                                    st.write("**Security Overrides:**")
                                                    security_data = {
                                                        "Security Rule ID": []
                                                    }
                                                    
                                                    for override in security_overrides:
                                                        security_data["Security Rule ID"].append(override['security_rule_id'])
                                                    
                                                    st.dataframe(pd.DataFrame(security_data), use_container_width=True)
                                                else:
                                                    st.info(f"No security overrides for {selected_role} role.")
                                        else:
                                            st.info(f"No policy-purpose-data element relationship found for {de_name}.")
                    else:
                        st.info("No external roles defined in the system.")
                
                # Render the decision tree to visualize the policy inference process
                self._render_decision_tree(nodes, edges, title="Policy Inference Process")

    def _render_decision_tree(self, nodes, edges, title="Policy Decision Tree"):
        # This method should delegate to the main app's decision tree rendering logic if possible
        # For now, assume it is implemented elsewhere or provide a placeholder
        st.markdown(f"#### {title}")
        DecisionTreeRenderer.render(nodes, edges)
