import streamlit as st

from UX.decision_tree_renderer import DecisionTreeRenderer

class PolicyCompliancePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Display the Policy Compliance page with the policy compliance analysis tool."""
        st.markdown("<div class='page-header'><i class='fas fa-balance-scale'></i> &nbsp;Policy Compliance</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Compliance Analysis</strong> determines whether access to data is permitted based on purpose limitation principles and organizational policies.</p>
            <p>This tool helps enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations.</p>
            <br>
            <ul>
                <li>Enforces purpose limitation principles</li>
                <li>Determines data access permissions based on business purpose</li>
                <li>Applies policy-based restrictions on data usage</li>
                <li>Provides clear decision rationale</li>
                <li>Considers role-based policy overrides</li>
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
        
        # Get external roles for dropdown selection
        try:
            roles = self.glossary_repository.get_external_roles()
            role_options = [(None, "No Role (Default Policy)")] + [(role[0], f"{role[1]} ({role[3]})" if role[3] else role[1]) for role in roles]
        except Exception as e:
            st.warning(f"Error loading external roles: {e}")
            role_options = [(None, "No Role (Default Policy)")]
        
        selected_role = st.selectbox(
            "Select External Role (Optional)", 
            options=[option[1] for option in role_options],
            key="policy_role"
        )
        # Get the role_id from the selected role name
        selected_role_id = None
        if selected_role != "No Role (Default Policy)":
            for role_option in role_options:
                if role_option[1] == selected_role:
                    selected_role_id = role_option[0]
                    break
        
        analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")

        st.write("")
        # Show results (decision tree, etc.) below the input parameters
        if analyze_button and selected_purpose and selected_data_elements and selected_operation:
            self.analyze_policy_compliance(selected_purpose, selected_data_elements, selected_operation, selected_role_id)
        elif analyze_button:
            st.warning("Please select a purpose, at least one data element, and an operation to analyze compliance.")

    def analyze_policy_compliance(self, purpose, data_elements, operation, external_role_id=None, jurisdiction=None):
        """Analyze policy compliance for Access Control, Data Security, and Data Retention policies."""
        import pandas as pd
        st = __import__('streamlit')
        # Get all policies
        policies = self.glossary_repository.get_policies()
        access_control_policy = None
        data_security_policy = None
        data_retention_policy = None
        for policy in policies:
            if policy["policy_type"] == "Access Control":
                access_control_policy = policy
            elif policy["policy_type"] == "Security":
                data_security_policy = policy
            elif policy["policy_type"] == "Retention":
                data_retention_policy = policy

        # Get purpose ID
        purposes = self.glossary_repository.get_purposes()
        purpose_id = None
        for p in purposes:
            if p["name"] == purpose:
                purpose_id = p["id"]
                break
        if not purpose_id:
            st.error(f"Purpose '{purpose}' not found in the database.")
            return

        # Get data element IDs
        all_data_elements = self.glossary_repository.get_data_elements()
        data_element_ids = {de["name"]: de["id"] for de in all_data_elements}

        denied_operations = False

        # --- Access Control Policy Compliance ---
        access_decisions = {"Data Element": [], "Operation": [], "Decision": [], "Restrictions": [], "Role Override": []}
        if access_control_policy:
            policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
                policy_id=access_control_policy['id'], purpose_id=purpose_id)
            policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                policy_id=access_control_policy['id'], purpose_id=purpose_id)
                
            # Get policy_purpose_data_element_ids for each data element to use with role overrides
            ppde_map = {}
            for ppde in policy_purpose_data_elements:
                if ppde["data_element_name"] in data_elements:
                    ppde_map[ppde["data_element_name"]] = ppde["id"]
                    
            # Get role-level overrides if a role is selected
            role_overrides = {}
            if external_role_id:
                for data_element in data_elements:
                    if data_element in ppde_map:
                        ppde_id = ppde_map[data_element]
                        role_usages = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_usages(
                            policy_purpose_data_element_id=ppde_id, external_role_id=external_role_id)
                        for role_usage in role_usages:
                            if role_usage["operation"] == operation:
                                key = (data_element, operation)
                                role_overrides[key] = role_usage
            
            for data_element in data_elements:
                decision = "Denied"
                restrictions = "No explicit permission in policy"
                role_override_applied = "No"
                
                # Check if there's a role override for this data element and operation
                key = (data_element, operation)
                if key in role_overrides:
                    role_usage = role_overrides[key]
                    if role_usage["allowed"]:
                        if role_usage["restrictions"]:
                            decision = "Allowed with Restrictions"
                            restrictions = role_usage["restrictions"]
                        else:
                            decision = "Allowed"
                            restrictions = "None"
                    else:
                        decision = "Denied"
                        restrictions = role_usage["restrictions"] or "Operation not allowed for this role and purpose"
                        denied_operations = True
                    role_override_applied = "Yes"
                else:
                    # No role override, use default policy
                    for usage in policy_purpose_data_usages:
                        if usage["data_element_name"] == data_element and usage["operation"] == operation:
                            if usage["allowed"]:
                                if usage["restrictions"]:
                                    decision = "Allowed with Restrictions"
                                    restrictions = usage["restrictions"]
                                else:
                                    decision = "Allowed"
                                    restrictions = "None"
                            else:
                                decision = "Denied"
                                restrictions = usage["restrictions"] or "Operation not allowed for this purpose"
                                denied_operations = True
                            break
                    if decision == "Denied" and restrictions == "No explicit permission in policy":
                        for element in policy_purpose_data_elements:
                            if element["data_element_name"] == data_element:
                                if element.get("access_allowed") and operation == "read":
                                    decision = "Allowed"
                                    restrictions = "None"
                                else:
                                    denied_operations = True
                                break
                access_decisions["Data Element"].append(data_element)
                access_decisions["Operation"].append(operation)
                access_decisions["Decision"].append(decision)
                access_decisions["Restrictions"].append(restrictions)
                access_decisions["Role Override"].append(role_override_applied)
            st.markdown("<h5>Access Control Policies</h5>", unsafe_allow_html=True)
            access_df = pd.DataFrame(access_decisions)
            def highlight_decision(val):
                if val == "Allowed":
                    return 'background-color: #d4edda; color: #155724'
                elif val == "Denied":
                    return 'background-color: #f8d7da; color: #721c24'
                elif val == "Allowed with Restrictions":
                    return 'background-color: #fff3cd; color: #856404'
                return ''
            st.dataframe(access_df.style.applymap(highlight_decision, subset=["Decision"]))
        else:
            st.warning("No Access Control Policy found in the database.")

        # --- Data Security Policy Compliance ---
        security_decisions = {"Data Element": [], "Encryption Required": [], "Encryption Algorithm": [], "Masking Required": [], "Masking Format": [], "Access Logging": [], "Role Override": []}
        if data_security_policy:
            policy_purpose_data_security = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                policy_id=data_security_policy['id'], purpose_id=purpose_id)
            
            # Get all data elements with their default masking formats
            all_data_elements = self.glossary_repository.get_data_elements()
            data_element_defaults = {de["name"]: de.get("default_masking_format") for de in all_data_elements}
            
            # Get policy_purpose_data_element_ids for each data element to use with role overrides
            ppde_map = {}
            for ppde in policy_purpose_data_elements:
                if ppde["data_element_name"] in data_elements:
                    ppde_map[ppde["data_element_name"]] = ppde["id"]
                    
            # Get role-level security overrides if a role is selected
            role_security_overrides = {}
            if external_role_id:
                for data_element in data_elements:
                    if data_element in ppde_map:
                        ppde_id = ppde_map[data_element]
                        role_security = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_security(
                            policy_purpose_data_element_id=ppde_id, external_role_id=external_role_id)
                        if role_security:
                            role_security_overrides[data_element] = role_security[0]
            
            for data_element in data_elements:
                security_decisions["Data Element"].append(data_element)
                role_override_applied = "No"
                
                # Check if there's a role override for this data element
                if data_element in role_security_overrides:
                    role_sec = role_security_overrides[data_element]
                    security_decisions["Encryption Required"].append("Yes" if role_sec.get("requires_encryption") else "No")
                    security_decisions["Encryption Algorithm"].append(role_sec.get("encryption_algorithm") or "-")
                    security_decisions["Masking Required"].append("Yes" if role_sec.get("requires_masking") else "No")
                    
                    # Use role override masking format if specified, otherwise use data element default
                    masking_format = role_sec.get("masking_format") or data_element_defaults.get(data_element)
                    security_decisions["Masking Format"].append(masking_format or "-")
                    
                    security_decisions["Access Logging"].append("Yes" if role_sec.get("requires_access_logging") else "No")
                    role_override_applied = "Yes"
                else:
                    # No role override, use default policy
                    sec = next((s for s in policy_purpose_data_security if s["data_element_name"] == data_element), None)
                    if sec:
                        security_decisions["Encryption Required"].append("Yes" if sec["encryption_required"] else "No")
                        security_decisions["Encryption Algorithm"].append(sec["encryption_algorithm"] or "-")
                        security_decisions["Masking Required"].append("Yes" if sec["masking_required"] else "No")
                        
                        # Use policy masking format if specified, otherwise use data element default
                        masking_format = sec["masking_format"] or data_element_defaults.get(data_element)
                        security_decisions["Masking Format"].append(masking_format or "-")
                        
                        security_decisions["Access Logging"].append("Yes" if sec["access_logging"] else "No")
                    else:
                        security_decisions["Encryption Required"].append("-")
                        security_decisions["Encryption Algorithm"].append("-")
                        security_decisions["Masking Required"].append("-")
                        
                        # Use data element default masking format if no policy rule exists
                        default_format = data_element_defaults.get(data_element)
                        security_decisions["Masking Format"].append(default_format or "-")
                        
                        security_decisions["Access Logging"].append("-")
                
                security_decisions["Role Override"].append(role_override_applied)
            st.markdown("<h5>Data Security Policies</h5>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(security_decisions))
        else:
            st.warning("No Data Security Policy found in the database.")

        # --- Data Retention Policy Compliance ---
        retention_decisions = {"Data Element": [], "Retention Period": [], "Retention Trigger": [], "Retention Basis": [], "Exceptions": [], "Role Override": []}
        if data_retention_policy:
            policy_purpose_data_retentions = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                policy_id=data_retention_policy['id'], purpose_id=purpose_id)
                
            # Get role-level retention overrides if a role is selected
            role_retention_overrides = {}
            if external_role_id:
                for data_element in data_elements:
                    if data_element in ppde_map:
                        ppde_id = ppde_map[data_element]
                        role_retentions = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_retentions(
                            policy_purpose_data_element_id=ppde_id, external_role_id=external_role_id)
                        if role_retentions:
                            role_retention_overrides[data_element] = role_retentions[0]
                
            for data_element in data_elements:
                retention_decisions["Data Element"].append(data_element)
                role_override_applied = "No"
                
                # Check if there's a role override for this data element
                if data_element in role_retention_overrides:
                    role_ret = role_retention_overrides[data_element]
                    retention_decisions["Retention Period"].append(role_ret["retention_period"] or "-")
                    retention_decisions["Retention Trigger"].append(role_ret.get("retention_trigger") or "-")
                    retention_decisions["Retention Basis"].append(role_ret.get("retention_justification") or "-")
                    retention_decisions["Exceptions"].append(role_ret.get("exceptions") or "-")
                    role_override_applied = "Yes"
                else:
                    # No role override, use default policy
                    ret = next((r for r in policy_purpose_data_retentions if r["data_element_name"] == data_element), None)
                    if ret:
                        retention_decisions["Retention Period"].append(ret["retention_period"] or "-")
                        retention_decisions["Retention Trigger"].append(ret["retention_trigger"] or "-")
                        retention_decisions["Retention Basis"].append(ret["retention_basis"] or "-")
                        retention_decisions["Exceptions"].append(ret["exceptions"] or "-")
                    else:
                        retention_decisions["Retention Period"].append("-")
                        retention_decisions["Retention Trigger"].append("-")
                        retention_decisions["Retention Basis"].append("-")
                        retention_decisions["Exceptions"].append("-")
                
                retention_decisions["Role Override"].append(role_override_applied)
            st.markdown("<h5>Data Retention Policies</h5>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(retention_decisions))
        else:
            st.warning("No Data Retention Policy found in the database.")

        # --- Decision Rationale and Recommendations ---
        st.markdown("""
        <div style="margin-top: 20px;">
            <h5>Decision Rationale</h5>
            <p>The policy compliance decision is based on:</p>
            <ul>
                <li>Purpose limitation principles defined in the Access Control Policy</li>
                <li>Data security requirements for each data element</li>
                <li>Retention rules for each data element</li>
                <li>Operation type and associated risks</li>
                <li>Purpose-specific data access rules</li>
                <li>Role-based policy overrides when applicable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if denied_operations:
            st.markdown("""
            <div style="margin-top: 20px; background-color: #fef9e7; padding: 15px; border-radius: 5px; border-left: 5px solid #f39c12;">
                <h4 style="color: #f39c12; margin-top: 0;">Compliance Recommendations</h4>
                <p>To ensure policy compliance:</p>
                <ul>
                    <li>Limit data access to only what is necessary for the stated purpose</li>
                    <li>Use anonymized or pseudonymized data when possible</li>
                    <li>Document the business justification for accessing sensitive data</li>
                    <li>Implement additional security controls for sensitive data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        # --- Decision Tree Visualization ---
        # Build nodes and edges representing the compliance decision path
        nodes = []
        edges = []
        # Root node: Purpose
        purpose_node_id = f"purpose_{purpose_id}"
        nodes.append({
            "id": purpose_node_id,
            "label": f"Purpose: {purpose}",
            "color": "#3498db",
            "shape": "ellipse",
            "size": 30
        })
        # Data Elements
        data_element_ids_list = []
        for data_element in data_elements:
            de_id = f"de_{data_element_ids.get(data_element, data_element)}"
            data_element_ids_list.append(de_id)
            nodes.append({
                "id": de_id,
                "label": f"Data Element: {data_element}",
                "color": "#f39c12",
                "shape": "box",
                "size": 25
            })
            edges.append({
                "source": purpose_node_id,
                "target": de_id,
                "label": "includes"
            })

        # Only for Access Control: add operation node and connect to data elements
        if access_control_policy and operation in ["read", "write", "share"]:
            op_node_id = f"operation_{operation}"
            nodes.append({
                "id": op_node_id,
                "label": f"Operation: {operation}",
                "color": "#2ecc71",
                "shape": "box",
                "size": 25
            })
            for de_id in data_element_ids_list:
                edges.append({
                    "source": de_id,
                    "target": op_node_id,
                    "label": "operation"
                })
            # Access Control Node (only for operation)
            access_node_id = f"access_{purpose_id}_{operation}"
            access_actions = []
            for i, data_element in enumerate(data_elements):
                if i < len(access_decisions["Decision"]):
                    access_actions.append(f"{data_element}: {access_decisions['Decision'][i]} ({access_decisions['Restrictions'][i]})")
            access_label = "Access Control Actions:\n" + "\n".join(access_actions)
            nodes.append({
                "id": access_node_id,
                "label": access_label,
                "color": "#9b59b6",
                "shape": "box",
                "size": 25,
                "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
            })
            edges.append({
                "source": op_node_id,
                "target": access_node_id,
                "label": "Access Control"
            })

        # Data Security nodes (connect directly to data elements)
        security_node_id = f"security_{purpose_id}_{operation}"
        security_actions = []
        for i, data_element in enumerate(data_elements):
            if i < len(security_decisions["Encryption Required"]):
                sec = security_decisions["Encryption Required"][i]
                if sec == "No":
                    security_actions.append(f"Implement encryption for '{data_element}' as required by policy.")
            if i < len(security_decisions["Masking Required"]) and security_decisions["Masking Required"][i] == "Yes":
                security_actions.append(f"Apply data masking to '{data_element}' ({security_decisions['Masking Format'][i]})")
            if i < len(security_decisions["Access Logging"]) and security_decisions["Access Logging"][i] == "No":
                security_actions.append(f"Enable access logging for '{data_element}'.")
        if not security_actions:
            security_actions.append("All security controls are in place.")
        security_label = "Data Security Actions:\n" + "\n".join(security_actions)
        nodes.append({
            "id": security_node_id,
            "label": security_label,
            "color": "#16a085",
            "shape": "box",
            "size": 25,
            "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
        })
        for de_id in data_element_ids_list:
            edges.append({
                "source": de_id,
                "target": security_node_id,
                "label": "Data Security"
            })

        # Data Retention nodes (connect directly to data elements)
        retention_node_id = f"retention_{purpose_id}_{operation}"
        retention_actions = []
        for i, data_element in enumerate(data_elements):
            if i < len(retention_decisions["Retention Period"]):
                ret = retention_decisions["Retention Period"][i]
                if ret == "-":
                    retention_actions.append(f"Define retention period for '{data_element}'.")
        if not retention_actions:
            retention_actions.append("All retention periods are defined as required.")
        retention_label = "Data Retention Actions:\n" + "\n".join(retention_actions)
        nodes.append({
            "id": retention_node_id,
            "label": retention_label,
            "color": "#e67e22",
            "shape": "box",
            "size": 25,
            "font": {"size": 14, "color": "black", "face": "Arial", "multi": True}
        })
        for de_id in data_element_ids_list:
            edges.append({
                "source": de_id,
                "target": retention_node_id,
                "label": "Data Retention"
            })

        # NO overall compliance leaf node; the tree ends with the above actionable nodes
        DecisionTreeRenderer.render(nodes, edges, title="Policy Compliance Decision Tree")
