import streamlit as st
import pandas as pd

class LawLegalBasisPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    @staticmethod
    def explain():
        st.markdown(
            """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Legal Basis Inference Works</h4>
                <p>The Legal Basis Inference API uses these mapping tables to determine the appropriate legal basis for processing personal data:</p>
                <ol>
                    <li><strong>Law Legal Basis</strong>: Maps laws to their supported legal bases, establishing which legal bases are valid under each regulation.</li>
                    <li><strong>Law Purpose Category Legal Basis</strong>: Provides recommended legal bases for specific processing purposes under each law, with preference ordering.</li>
                    <li><strong>Legal Basis Requirements</strong>: Details the compliance requirements for each legal basis, helping organizations implement the necessary safeguards.</li>
                </ol>
                <p>When making a legal basis determination, the system considers:</p>
                <ul>
                    <li>The applicable law (e.g., GDPR, CCPA)</li>
                    <li>The processing purpose (e.g., Marketing, Security)</li>
                    <li>Data sensitivity level</li>
                    <li>Specific context of processing</li>
                </ul>
                <p>The system then recommends appropriate legal bases in order of preference, along with their compliance requirements.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Legal Basis:</b><br>
            This section maps data protection laws to their applicable legal bases for processing personal data. These mappings help organizations understand which legal grounds are valid for data processing under different regulatory frameworks.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get law legal basis data from repository
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        if law_legal_bases:
            law_legal_basis_data = {
                "Law": [],
                "Legal Basis": [],
                "Description": []
            }
            for llb in law_legal_bases:
                law_legal_basis_data["Law"].append(llb["law_name"])
                law_legal_basis_data["Legal Basis"].append(llb["legal_basis_name"])
                law_legal_basis_data["Description"].append(llb["legal_basis_description"])
    
            # Create a DataFrame
            df = pd.DataFrame(law_legal_basis_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_legal_basis_law_filter")
            
            with col2:
                legal_bases = sorted(df["Legal Basis"].unique())
                selected_legal_basis = st.selectbox("Filter by Legal Basis", ["All"] + list(legal_bases), key="law_legal_basis_lb_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_legal_basis != "All":
                filtered_df = filtered_df[filtered_df["Legal Basis"] == selected_legal_basis]
            
            # Sort by Law and Legal Basis
            filtered_df = filtered_df.sort_values(by=["Law", "Legal Basis"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")

class RiskControlPage:
    def __init__(self, regulatory_metadata_repository, glossary_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Risk Control:</b><br>
            This section maps identified risks to specific controls that help mitigate those risks. These mappings provide a comprehensive view of risk management strategies and their implementation through appropriate controls.
        </div>
        ''', unsafe_allow_html=True)

        # Get all risks from the repository
        risks = self.glossary_repository.get_risks()
        if not risks:
            st.warning("No risks available in the database.")
            return
        risk_options = {r["id"]: r["name"] for r in risks}
        risk_options[0] = "All Risks"

        # Get all controls from the repository
        controls = self.glossary_repository.get_controls()
        if not controls:
            st.warning("No controls available in the database.")
            return
        control_options = {c["id"]: c["name"] for c in controls}
        control_options[0] = "All Controls"

        # Create filters
        col1, col2 = st.columns(2)
        with col1:
            selected_risk_id = st.selectbox(
                "Filter by Risk",
                options=list(risk_options.keys()),
                format_func=lambda x: risk_options[x],
                key="risk_control_risk_filter"
            )
        with col2:
            selected_control_id = st.selectbox(
                "Filter by Control",
                options=list(control_options.keys()),
                format_func=lambda x: control_options[x],
                key="risk_control_control_filter"
            )

        # Get risk-control mappings from the repository
        if selected_risk_id != 0 and selected_control_id != 0:
            # Both risk and control selected
            risk_controls = self.regulatory_metadata_repository.get_risk_controls(
                risk_id=selected_risk_id,
                control_id=selected_control_id
            )
        elif selected_risk_id != 0:
            # Only risk selected
            risk_controls = self.regulatory_metadata_repository.get_risk_controls(
                risk_id=selected_risk_id
            )
        elif selected_control_id != 0:
            # Only control selected
            risk_controls = self.regulatory_metadata_repository.get_risk_controls(
                control_id=selected_control_id
            )
        else:
            # No filters selected
            risk_controls = self.regulatory_metadata_repository.get_risk_controls()

        if risk_controls:
            # Create a DataFrame
            df = pd.DataFrame(risk_controls)
            # Rename columns for better display
            column_mapping = {
                "risk_name": "Risk",
                "risk_category": "Risk Category",
                "risk_likelihood": "Likelihood",
                "risk_impact": "Impact",
                "control_name": "Control",
                "control_type": "Control Type",
                "implementation_status": "Implementation Status",
                "priority": "Priority",
                "mitigation_level": "Mitigation Level"
            }
            # Only rename columns that exist
            existing_columns = set(df.columns).intersection(set(column_mapping.keys()))
            rename_mapping = {col: column_mapping[col] for col in existing_columns}
            df = df.rename(columns=rename_mapping)
            # Define display columns in preferred order
            display_columns = [
                "Risk", "Risk Category", "Likelihood", "Impact", 
                "Control", "Control Type", "Implementation Status", "Priority", "Mitigation Level"
            ]
            # Only include columns that exist in the DataFrame
            available_columns = [col for col in display_columns if col in df.columns]
            if available_columns:
                df = df[available_columns]
                # Sort by risk and control
                sort_columns = []
                if "Risk" in df.columns:
                    sort_columns.append("Risk")
                if "Control" in df.columns:
                    sort_columns.append("Control")
                if "Mitigation Level" in df.columns:
                    sort_columns.append("Mitigation Level")
                if sort_columns:
                    df = df.sort_values(by=sort_columns, ascending=[True, True, False])
                # Display the filtered data
                st.dataframe(df)
        else:
            st.info("No risk-control mappings found with the selected filters.")


class PolicyControlPage:
    def __init__(self, regulatory_metadata_repository, glossary_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Policy Control:</b><br>
            This section maps organizational policies to specific controls that help enforce those policies. These mappings show how policies are implemented through concrete security and privacy controls.
        </div>
        ''', unsafe_allow_html=True)

        # Get all policies from the repository
        policies = self.glossary_repository.get_policies()
        if not policies:
            st.warning("No policies available in the database.")
            return
        policy_options = {p["id"]: p["name"] for p in policies}
        policy_options[0] = "All Policies"

        # Get all controls from the repository
        controls = self.glossary_repository.get_controls()
        if not controls:
            st.warning("No controls available in the database.")
            return
        control_options = {c["id"]: c["name"] for c in controls}
        control_options[0] = "All Controls"

        # Create filters
        col1, col2 = st.columns(2)
        with col1:
            selected_policy_id = st.selectbox(
                "Filter by Policy",
                options=list(policy_options.keys()),
                format_func=lambda x: policy_options[x],
                key="policy_control_policy_filter"
            )
        with col2:
            selected_control_id = st.selectbox(
                "Filter by Control",
                options=list(control_options.keys()),
                format_func=lambda x: control_options[x],
                key="policy_control_control_filter"
            )

        # Get policy-control mappings from the repository
        if selected_policy_id != 0 and selected_control_id != 0:
            # Both policy and control selected
            policy_controls = self.regulatory_metadata_repository.get_policy_controls(
                policy_id=selected_policy_id,
                control_id=selected_control_id
            )
        elif selected_policy_id != 0:
            # Only policy selected
            policy_controls = self.regulatory_metadata_repository.get_policy_controls(
                policy_id=selected_policy_id
            )
        elif selected_control_id != 0:
            # Only control selected
            policy_controls = self.regulatory_metadata_repository.get_policy_controls(
                control_id=selected_control_id
            )
        else:
            # No filters selected
            policy_controls = self.regulatory_metadata_repository.get_policy_controls()

        if policy_controls:
            # Create a DataFrame
            df = pd.DataFrame(policy_controls)
            # Rename columns for better display
            column_mapping = {
                "policy_name": "Policy",
                "policy_type": "Policy Type",
                "control_name": "Control",
                "control_type": "Control Type",
                "implementation_status": "Implementation Status",
                "priority": "Priority",
                "relevance_score": "Relevance Score"
            }
            # Only rename columns that exist
            existing_columns = set(df.columns).intersection(set(column_mapping.keys()))
            rename_mapping = {col: column_mapping[col] for col in existing_columns}
            df = df.rename(columns=rename_mapping)
            # Define display columns in preferred order
            display_columns = [
                "Policy", "Policy Type", "Control", "Control Type", 
                "Implementation Status", "Priority", "Relevance Score"
            ]
            # Only include columns that exist in the DataFrame
            available_columns = [col for col in display_columns if col in df.columns]
            if available_columns:
                df = df[available_columns]
                # Sort by policy and control
                sort_columns = []
                if "Policy" in df.columns:
                    sort_columns.append("Policy")
                if "Control" in df.columns:
                    sort_columns.append("Control")
                if "Relevance Score" in df.columns:
                    sort_columns.append("Relevance Score")
                if sort_columns:
                    df = df.sort_values(by=sort_columns, ascending=[True, True, False])
                # Display the filtered data
                st.dataframe(df)
        else:
            st.info("No policy-control mappings found with the selected filters.")


class FrameworkControlPage:
    def __init__(self, regulatory_metadata_repository, glossary_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Framework Control:</b><br>
            This section maps security and compliance frameworks to specific controls that help implement the framework requirements. These mappings show how different security and privacy frameworks are implemented through concrete controls.
        </div>
        ''', unsafe_allow_html=True)

        # Get all frameworks from the repository
        frameworks = self.glossary_repository.get_frameworks()
        if not frameworks:
            st.warning("No frameworks available in the database.")
            return
        framework_options = {f["id"]: f["name"] for f in frameworks}
        framework_options[0] = "All Frameworks"

        # Get all controls from the repository
        controls = self.glossary_repository.get_controls()
        if not controls:
            st.warning("No controls available in the database.")
            return
        control_options = {c["id"]: c["name"] for c in controls}
        control_options[0] = "All Controls"

        # Create filters
        col1, col2 = st.columns(2)
        with col1:
            selected_framework_id = st.selectbox(
                "Filter by Framework",
                options=list(framework_options.keys()),
                format_func=lambda x: framework_options[x],
                key="framework_control_framework_filter"
            )
        with col2:
            selected_control_id = st.selectbox(
                "Filter by Control",
                options=list(control_options.keys()),
                format_func=lambda x: control_options[x],
                key="framework_control_control_filter"
            )

        # Get framework-control mappings from the repository
        if selected_framework_id != 0 and selected_control_id != 0:
            # Both framework and control selected
            framework_controls = self.regulatory_metadata_repository.get_framework_controls(
                framework_id=selected_framework_id,
                control_id=selected_control_id
            )
        elif selected_framework_id != 0:
            # Only framework selected
            framework_controls = self.regulatory_metadata_repository.get_framework_controls(
                framework_id=selected_framework_id
            )
        elif selected_control_id != 0:
            # Only control selected
            framework_controls = self.regulatory_metadata_repository.get_framework_controls(
                control_id=selected_control_id
            )
        else:
            # No filters selected
            framework_controls = self.regulatory_metadata_repository.get_framework_controls()

        if framework_controls:
            # Create a DataFrame
            df = pd.DataFrame(framework_controls)
            # Rename columns for better display
            column_mapping = {
                "framework_name": "Framework",
                "framework_category": "Framework Category",
                "framework_version": "Version",
                "control_name": "Control",
                "control_type": "Control Type",
                "implementation_status": "Implementation Status",
                "priority": "Priority",
                "relevance_score": "Relevance Score"
            }
            # Only rename columns that exist
            existing_columns = set(df.columns).intersection(set(column_mapping.keys()))
            rename_mapping = {col: column_mapping[col] for col in existing_columns}
            df = df.rename(columns=rename_mapping)
            # Define display columns in preferred order
            display_columns = [
                "Framework", "Framework Category", "Version", 
                "Control", "Control Type", "Implementation Status", "Priority", "Relevance Score"
            ]
            # Only include columns that exist in the DataFrame
            available_columns = [col for col in display_columns if col in df.columns]
            if available_columns:
                df = df[available_columns]
                # Sort by framework and control
                sort_columns = []
                if "Framework" in df.columns:
                    sort_columns.append("Framework")
                if "Control" in df.columns:
                    sort_columns.append("Control")
                if "Relevance Score" in df.columns:
                    sort_columns.append("Relevance Score")
                if sort_columns:
                    df = df.sort_values(by=sort_columns, ascending=[True, True, False])
                # Display the filtered data
                st.dataframe(df)
        else:
            st.info("No framework-control mappings found with the selected filters.")


class SensitivityPoliciesPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Sensitivity Policies:</b><br>
            This section defines standard security and privacy policies that should be applied based on data sensitivity levels. These mappings help organizations implement appropriate safeguards for different types of data based on their sensitivity classification.
        </div>
        ''', unsafe_allow_html=True)

        # Get all sensitivities
        sensitivities = self.glossary_repository.get_sensitivities()

        # Create a filter for sensitivity
        sensitivity_options = {s["id"]: s["name"] for s in sensitivities}
        sensitivity_options[0] = "All Sensitivities"

        selected_sensitivity_id = st.selectbox(
            "Filter by Sensitivity Level",
            options=list(sensitivity_options.keys()),
            format_func=lambda x: sensitivity_options[x],
            index=0,
            key="sensitivity_policy_filter"
        )

        # Get policies for the selected sensitivity
        if selected_sensitivity_id == 0:
            # Get policies for all sensitivities
            all_policies = []
            for sensitivity in sensitivities:
                policies = self.regulatory_metadata_repository.get_policies_by_sensitivity(sensitivity["id"])
                all_policies.extend(policies)
            sensitivity_policies = all_policies
        else:
            # Get policies for the selected sensitivity
            sensitivity_policies = self.regulatory_metadata_repository.get_policies_by_sensitivity(selected_sensitivity_id)

        if sensitivity_policies:
            # Enhance policies with security, usage, and retention details
            enhanced_policies = []
            for policy in sensitivity_policies:
                policy_id = policy['id']
                enhanced_policy = dict(policy)
                
                # Get data elements associated with this sensitivity level
                cursor = self.regulatory_metadata_repository.connection.cursor()
                try:
                    # Extract sensitivity_id from the policy
                    sensitivity_id = None
                    for s in sensitivities:
                        if s['name'] == policy['sensitivity_name']:
                            sensitivity_id = s['id']
                            break
                    
                    if sensitivity_id is not None:
                        cursor.execute('''
                            SELECT de.id
                            FROM data_element de
                            JOIN data_element_sensitivity des ON de.id = des.data_element_id
                            WHERE des.sensitivity_id = %s
                        ''', (sensitivity_id,))
                    
                    data_element_ids = [row[0] for row in cursor.fetchall()]
                    
                    # If no data elements found for this sensitivity, use a representative one
                    if not data_element_ids:
                        cursor.execute("SELECT id FROM data_element LIMIT 1")
                        de_row = cursor.fetchone()
                        if de_row:
                            data_element_ids = [de_row[0]]
                except Exception as e:
                    print(f"Error getting data elements: {e}")
                    data_element_ids = []
                finally:
                    cursor.close()
                
                # Only proceed if we have data elements
                if data_element_ids:
                    # Get security policies
                    security_policies = []
                    for de_id in data_element_ids:
                        sec_policies = self.regulatory_metadata_repository.get_policy_data_element_security(
                            policy_id=policy_id, data_element_id=de_id)
                        security_policies.extend(sec_policies)
                    
                    # Get usage policies
                    usage_policies = []
                    for de_id in data_element_ids:
                        use_policies = self.regulatory_metadata_repository.get_policy_data_element_usage(
                            policy_id=policy_id, data_element_id=de_id)
                        usage_policies.extend(use_policies)
                    
                    # Get retention policies
                    retention_policies = []
                    for de_id in data_element_ids:
                        ret_policies = self.regulatory_metadata_repository.get_policy_data_element_retention(
                            policy_id=policy_id, data_element_id=de_id)
                        retention_policies.extend(ret_policies)
                    
                    # Add security details
                    if security_policies:
                        enhanced_policy['requires_encryption'] = any(p['requires_encryption'] for p in security_policies)
                        encryption_algos = [p['encryption_algorithm'] for p in security_policies if p['encryption_algorithm']]
                        enhanced_policy['encryption_algorithm'] = encryption_algos[0] if encryption_algos else None
                        
                        enhanced_policy['requires_masking'] = any(p['requires_masking'] for p in security_policies)
                        masking_formats = [p['masking_format'] for p in security_policies if p['masking_format']]
                        enhanced_policy['masking_format'] = masking_formats[0] if masking_formats else None
                        
                        enhanced_policy['requires_access_control'] = any(p['requires_access_control'] for p in security_policies)
                        access_types = [p['access_control_type'] for p in security_policies if p['access_control_type']]
                        enhanced_policy['access_control_type'] = access_types[0] if access_types else None
                    else:
                        # Default values if no security policies found
                        enhanced_policy['requires_encryption'] = False
                        enhanced_policy['encryption_algorithm'] = None
                        enhanced_policy['requires_masking'] = False
                        enhanced_policy['masking_format'] = None
                        enhanced_policy['requires_access_control'] = False
                        enhanced_policy['access_control_type'] = None
                    
                    # Add usage details
                    if usage_policies:
                        operations = [p['operation'] for p in usage_policies]
                        allowed = [p['allowed'] for p in usage_policies]
                        enhanced_policy['usage_operations'] = ', '.join(operations)
                        enhanced_policy['usage_allowed'] = 'Yes' if all(allowed) else 'No' if not any(allowed) else 'Partial'
                    else:
                        enhanced_policy['usage_operations'] = None
                        enhanced_policy['usage_allowed'] = None
                    
                    # Add retention details
                    if retention_policies:
                        retention_periods = [p['retention_period'] for p in retention_policies if p['retention_period']]
                        enhanced_policy['retention_period'] = retention_periods[0] if retention_periods else None
                        
                        retention_bases = [p['retention_basis'] for p in retention_policies if p['retention_basis']]
                        enhanced_policy['retention_basis'] = retention_bases[0] if retention_bases else None
                    else:
                        enhanced_policy['retention_period'] = None
                        enhanced_policy['retention_basis'] = None
                
                enhanced_policies.append(enhanced_policy)
            
            # Convert to DataFrame for display
            df = pd.DataFrame(enhanced_policies)
            
            # Add policy type filter if we have policy types
            if "policy_type" in df.columns:
                policy_types = sorted(df["policy_type"].unique())
                selected_policy_type = st.selectbox(
                    "Filter by Policy Type",
                    options=["All"] + list(policy_types),
                    index=0,
                    key="policy_type_filter"
                )
                if selected_policy_type != "All":
                    df = df[df["policy_type"] == selected_policy_type]
            
            # Rename columns for better display
            column_mapping = {
                "id": "ID",
                "sensitivity_name": "Sensitivity Level",
                "name": "Policy Name",
                "description": "Description",
                "policy_type": "Policy Type",
                "requires_encryption": "Encryption Required",
                "encryption_algorithm": "Encryption Algorithm",
                "requires_masking": "Masking Required",
                "masking_format": "Masking Format",
                "requires_access_control": "Access Control Required",
                "access_control_type": "Access Control Type",
                "usage_operations": "Usage Operations",
                "usage_allowed": "Usage Allowed",
                "retention_period": "Retention Period",
                "retention_basis": "Retention Basis"
            }
            # Only rename columns that exist in the DataFrame
            rename_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df.rename(columns=rename_cols)

            # Define display columns (only include columns that exist)
            all_display_columns = ["ID", "Sensitivity Level", "Policy Name", "Description", "Policy Type", 
                                 "Encryption Required", "Encryption Algorithm", "Masking Required", "Masking Format", 
                                 "Access Control Required", "Access Control Type", "Usage Operations", "Usage Allowed",
                                 "Retention Period", "Retention Basis"]
            display_columns = [col for col in all_display_columns if col in df.columns]

            # Sort by sensitivity level and policy name
            df = df.sort_values(by=["Sensitivity Level", "Policy Name"])

            # Format boolean columns to Yes/No
            boolean_columns = ["Encryption Required", "Masking Required", "Access Control Required"]
            for col in boolean_columns:
                if col in df.columns:
                    df[col] = df[col].map({True: "Yes", False: "No"})

            # Display the dataframe
            st.dataframe(df[display_columns], use_container_width=True)

            # Add explanation
            st.markdown("""
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">How Sensitivity Policies Work</h4>
                <p>This mapping table defines the standard security and privacy policies that should be applied based on data sensitivity:</p>
                <ul>
                    <li><strong>Special Category Data:</strong> Requires the highest level of protection with strict encryption, access controls, and monitoring</li>
                    <li><strong>Restricted Data:</strong> Requires strong protection measures including encryption and access restrictions</li>
                    <li><strong>Confidential Data:</strong> Requires moderate protection with basic encryption and access controls</li>
                    <li><strong>Internal Data:</strong> Requires standard organizational controls</li>
                    <li><strong>Public Data:</strong> Requires basic integrity controls</li>
                </ul>
                <p>These mappings are used by the Policy Inference API to recommend appropriate controls based on data sensitivity.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No sensitivity policies available for the selected sensitivity level.")


class PolicyPurposeDataUsagePage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Policy Purpose Data Usage Mapping:</b><br>
            This section defines how data can be used (read, write, share) for each purpose-policy-data element combination, with specific restrictions. These mappings help organizations implement appropriate data usage controls based on their policies and purposes.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get policy purpose data usage data from repository
        policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages()
        if policy_purpose_data_usages:
            ppdu_data = {
                "Policy": [],
                "Purpose": [],
                "Data Element": [],
                "Operation": [],
                "Allowed": [],
                "Restrictions": []
            }
            for ppdu in policy_purpose_data_usages:
                ppdu_data["Policy"].append(ppdu["policy_name"])
                ppdu_data["Purpose"].append(ppdu["purpose_name"])
                ppdu_data["Data Element"].append(ppdu["data_element_name"])
                ppdu_data["Operation"].append(ppdu["operation"])
                ppdu_data["Allowed"].append("Yes" if ppdu["allowed"] else "No")
                ppdu_data["Restrictions"].append(ppdu["restrictions"] if ppdu["restrictions"] else "")
            
            # Create a DataFrame
            df = pd.DataFrame(ppdu_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                policies = sorted(df["Policy"].unique())
                selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="ppdu_policy_filter")
            
            with col2:
                purposes = sorted(df["Purpose"].unique())
                selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="ppdu_purpose_filter")
            
            col3, col4 = st.columns(2)
            with col3:
                data_elements = sorted(df["Data Element"].unique())
                selected_data_element = st.selectbox("Filter by Data Element", ["All"] + list(data_elements), key="ppdu_data_element_filter")
                
            with col4:
                operations = sorted(df["Operation"].unique())
                selected_operation = st.selectbox("Filter by Operation", ["All"] + list(operations), key="ppdu_operation_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_policy != "All":
                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
            if selected_purpose != "All":
                filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
            if selected_data_element != "All":
                filtered_df = filtered_df[filtered_df["Data Element"] == selected_data_element]
            if selected_operation != "All":
                filtered_df = filtered_df[filtered_df["Operation"] == selected_operation]
            
            # Sort by Policy, Purpose, Data Element, and Operation
            filtered_df = filtered_df.sort_values(by=["Policy", "Purpose", "Data Element", "Operation"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No Policy Purpose Data Usage mappings available in the database.")


class PolicyPurposeDataElementPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Policy Purpose Data Element Mapping:</b><br>
            This section defines which data elements can be accessed for specific policy-purpose combinations, a key component of purpose-based access control. These mappings are essential for implementing proper data access controls in compliance with privacy regulations.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get policy purpose data element data from repository
        policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements()
        if policy_purpose_data_elements:
            ppde_data = {
                "Policy": [],
                "Purpose": [],
                "Data Element": [],
                "Access Allowed": []
            }
            for ppde in policy_purpose_data_elements:
                ppde_data["Policy"].append(ppde["policy_name"])
                ppde_data["Purpose"].append(ppde["purpose_name"])
                ppde_data["Data Element"].append(ppde["data_element_name"])
                ppde_data["Access Allowed"].append("Yes" if ppde["access_allowed"] else "No")
            
            # Create a DataFrame
            df = pd.DataFrame(ppde_data)
            
            # Add filters
            col1, col2, col3 = st.columns(3)
            with col1:
                policies = sorted(df["Policy"].unique())
                selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="ppde_policy_filter")
            
            with col2:
                purposes = sorted(df["Purpose"].unique())
                selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="ppde_purpose_filter")
                
            with col3:
                data_elements = sorted(df["Data Element"].unique())
                selected_data_element = st.selectbox("Filter by Data Element", ["All"] + list(data_elements), key="ppde_data_element_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_policy != "All":
                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
            if selected_purpose != "All":
                filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
            if selected_data_element != "All":
                filtered_df = filtered_df[filtered_df["Data Element"] == selected_data_element]
            
            # Sort by Policy, Purpose, and Data Element
            filtered_df = filtered_df.sort_values(by=["Policy", "Purpose", "Data Element"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No Policy Purpose Data Element mappings available in the database.")


class PolicyPurposePage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Policy to Purpose Mapping:</b><br>
            This section maps organizational policies to business purposes, establishing which purposes are governed by which policies. These mappings help organizations ensure that all data processing activities are covered by appropriate policies.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get policy purpose data from repository
        policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
        if policy_purposes:
            policy_purpose_data = {
                "Policy": [],
                "Purpose": []
            }
            for pp in policy_purposes:
                policy_purpose_data["Policy"].append(pp["policy_name"])
                policy_purpose_data["Purpose"].append(pp["purpose_name"])
            
            # Create a DataFrame
            df = pd.DataFrame(policy_purpose_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                policies = sorted(df["Policy"].unique())
                selected_policy = st.selectbox("Filter by Policy", ["All"] + list(policies), key="policy_purpose_policy_filter")
            
            with col2:
                purposes = sorted(df["Purpose"].unique())
                selected_purpose = st.selectbox("Filter by Purpose", ["All"] + list(purposes), key="policy_purpose_purpose_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_policy != "All":
                filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
            if selected_purpose != "All":
                filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
            
            # Sort by Policy and Purpose
            filtered_df = filtered_df.sort_values(by=["Policy", "Purpose"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No Policy Purpose mappings available in the database.")


class LegalBasisRequirementsPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Legal Basis Requirements:</b><br>
            This section provides detailed compliance requirements for each legal basis, helping organizations understand what they need to do to properly rely on a specific legal basis for processing.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get legal basis requirements from repository
        legal_basis_requirements = self.regulatory_metadata_repository.get_legal_basis_requirements()
        if legal_basis_requirements:
            requirements_data = {
                "Legal Basis": [],
                "Requirement": []
            }
            for req in legal_basis_requirements:
                requirements_data["Legal Basis"].append(req["legal_basis_name"])
                requirements_data["Requirement"].append(req["requirement"])
            
            # Create a DataFrame
            df = pd.DataFrame(requirements_data)
            
            # Add filter for Legal Basis
            legal_bases = sorted(df["Legal Basis"].unique())
            selected_legal_basis = st.selectbox("Filter by Legal Basis", ["All"] + list(legal_bases), key="legal_basis_requirements_filter")
            
            # Apply filter
            filtered_df = df.copy()
            if selected_legal_basis != "All":
                filtered_df = filtered_df[filtered_df["Legal Basis"] == selected_legal_basis]
            
            # Sort by Legal Basis
            filtered_df = filtered_df.sort_values(by=["Legal Basis"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No Legal Basis Requirements available in the database.")


class LawPurposeCategoryLegalBasisPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Purpose Category Legal Basis:</b><br>
            This section maps data protection laws to purpose categories and their applicable legal bases, helping organizations determine the appropriate legal basis for different processing purposes under various laws. These mappings are essential for the Legal Basis Inference API, providing recommendations on which legal grounds to use for specific processing activities.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get law purpose category legal basis data from repository
        law_purpose_legal_bases = self.regulatory_metadata_repository.get_law_purpose_category_legal_bases()
        if law_purpose_legal_bases:
            law_purpose_legal_basis_data = {
                "Law": [],
                "Purpose Category": [],
                "Legal Basis": [],
                "Preference Order": [],
                "Notes": []
            }
            for mapping in law_purpose_legal_bases:
                law_purpose_legal_basis_data["Law"].append(mapping["law_name"])
                law_purpose_legal_basis_data["Purpose Category"].append(mapping["purpose_category_name"])
                law_purpose_legal_basis_data["Legal Basis"].append(mapping["legal_basis_name"])
                law_purpose_legal_basis_data["Preference Order"].append(mapping["preference_order"])
                law_purpose_legal_basis_data["Notes"].append(mapping["description"] if mapping.get("description") else "")
    
            # Create a DataFrame and display it
            df = pd.DataFrame(law_purpose_legal_basis_data)
    
            # Add filters for Law and Purpose Category
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws))
    
            with col2:
                purpose_categories = sorted(df["Purpose Category"].unique())
                selected_purpose = st.selectbox("Filter by Purpose Category", ["All"] + list(purpose_categories))
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_purpose != "All":
                filtered_df = filtered_df[filtered_df["Purpose Category"] == selected_purpose]
    
            # Sort by Law, Purpose Category, and Preference Order
            filtered_df = filtered_df.sort_values(by=["Law", "Purpose Category", "Preference Order"])
    
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No Law Purpose Category Legal Basis mappings available in the database.")


class DataSubjectTypeDataElementSensitivityPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Data Subject Type Data Element Sensitivity:</b><br>
            This section maps data subject types to specific data elements and their sensitivity levels, independent of specific laws.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get mappings from repository
        mappings = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
        if mappings:
            mapping_data = {
                "Data Subject Type": [],
                "Data Element": [],
                "Sensitivity": []
            }
            for mapping in mappings:
                mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                mapping_data["Data Element"].append(mapping["data_element_name"])
                mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                subject_types = sorted(df["Data Subject Type"].unique())
                selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="dst_de_sens_dst_filter")
            
            with col2:
                elements = sorted(df["Data Element"].unique())
                selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="dst_de_sens_element_filter")
            
            col3, _ = st.columns(2)
            with col3:
                sensitivities = sorted(df["Sensitivity"].unique())
                selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="dst_de_sens_sensitivity_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_subject_type != "All":
                filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
            if selected_element != "All":
                filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
            if selected_sensitivity != "All":
                filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
    
            # Sort by Data Subject Type, Data Element
            filtered_df = filtered_df.sort_values(by=["Data Subject Type", "Data Element"])
    
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class DataSubjectTypeDataCategorySensitivityPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Data Subject Type Data Category Sensitivity:</b><br>
                This section maps data subject types to data categories and their sensitivity levels, independent of specific laws.
            </div>
            ''', unsafe_allow_html=True)
        
        # Get mappings from repository
        mappings = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
        if mappings:
            mapping_data = {
                "Data Subject Type": [],
                "Data Category": [],
                "Sensitivity": []
            }
            for mapping in mappings:
                mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                mapping_data["Data Category"].append(mapping["data_category_name"])
                mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                subject_types = sorted(df["Data Subject Type"].unique())
                selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="dst_dc_sens_dst_filter")
            
            with col2:
                categories = sorted(df["Data Category"].unique())
                selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="dst_dc_sens_category_filter")
            
            col3, _ = st.columns(2)
            with col3:
                sensitivities = sorted(df["Sensitivity"].unique())
                selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="dst_dc_sens_sensitivity_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_subject_type != "All":
                filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
            if selected_sensitivity != "All":
                filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
    
            # Sort by Data Subject Type, Data Category
            filtered_df = filtered_df.sort_values(by=["Data Subject Type", "Data Category"])
    
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class DataCategoryDataElementPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Data Category Data Element:</b><br>
            This section maps data categories to their constituent data elements, providing a hierarchical view of data classification. These mappings help organize data elements into logical groups for more effective policy application and sensitivity analysis.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get data category data element mappings from repository
        data_category_elements = self.regulatory_metadata_repository.get_data_category_data_elements()
        if data_category_elements:
            mapping_data = {
                "Data Category": [],
                "Data Element": []
            }
            for mapping in data_category_elements:
                mapping_data["Data Category"].append(mapping["data_category_name"])
                mapping_data["Data Element"].append(mapping["data_element_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                categories = sorted(df["Data Category"].unique())
                selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="data_category_element_category_filter")
            
            with col2:
                elements = sorted(df["Data Element"].unique())
                selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="data_category_element_element_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
            if selected_element != "All":
                filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
            
            # Sort by Data Category and Data Element
            filtered_df = filtered_df.sort_values(by=["Data Category", "Data Element"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class LawDataSubjectTypeDataCategorySensitivityPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Data Subject Type Data Category Sensitivity:</b><br>
            This section maps laws to data subject types, data categories, and their sensitivity levels, providing a comprehensive view of data protection requirements. These mappings are used by the Data Sensitivity Inference API to determine appropriate sensitivity classifications for different categories of data.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get mappings from repository
        mappings = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
        if mappings:
            mapping_data = {
                "Law": [],
                "Data Subject Type": [],
                "Data Category": [],
                "Sensitivity": []
            }
            for mapping in mappings:
                mapping_data["Law"].append(mapping["law_name"])
                mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                mapping_data["Data Category"].append(mapping["data_category_name"])
                mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_dst_dc_sens_law_filter")
            
            with col2:
                subject_types = sorted(df["Data Subject Type"].unique())
                selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="law_dst_dc_sens_dst_filter")
            
            col3, col4 = st.columns(2)
            with col3:
                categories = sorted(df["Data Category"].unique())
                selected_category = st.selectbox("Filter by Data Category", ["All"] + list(categories), key="law_dst_dc_sens_category_filter")
            
            with col4:
                sensitivities = sorted(df["Sensitivity"].unique())
                selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="law_dst_dc_sens_sensitivity_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_subject_type != "All":
                filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Data Category"] == selected_category]
            if selected_sensitivity != "All":
                filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
            
            # Sort by Law, Data Subject Type, Data Category
            filtered_df = filtered_df.sort_values(by=["Law", "Data Subject Type", "Data Category"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class LawDataSubjectTypeDataElementSensitivityPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Data Subject Type Data Element Sensitivity:</b><br>
            This section maps laws to data subject types, data elements, and their sensitivity levels, providing a comprehensive view of data protection requirements. These mappings are crucial for the Data Sensitivity Inference API, helping determine the appropriate sensitivity level for specific data elements under different regulatory frameworks.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get mappings from repository
        mappings = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
        if mappings:
            mapping_data = {
                "Law": [],
                "Data Subject Type": [],
                "Data Element": [],
                "Sensitivity": []
            }
            for mapping in mappings:
                mapping_data["Law"].append(mapping["law_name"])
                mapping_data["Data Subject Type"].append(mapping["data_subject_type_name"])
                mapping_data["Data Element"].append(mapping["data_element_name"])
                mapping_data["Sensitivity"].append(mapping["sensitivity_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(mapping_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_dst_de_sens_law_filter")
            
            with col2:
                subject_types = sorted(df["Data Subject Type"].unique())
                selected_subject_type = st.selectbox("Filter by Data Subject Type", ["All"] + list(subject_types), key="law_dst_de_sens_dst_filter")
            
            col3, col4 = st.columns(2)
            with col3:
                elements = sorted(df["Data Element"].unique())
                selected_element = st.selectbox("Filter by Data Element", ["All"] + list(elements), key="law_dst_de_sens_element_filter")
            
            with col4:
                sensitivities = sorted(df["Sensitivity"].unique())
                selected_sensitivity = st.selectbox("Filter by Sensitivity", ["All"] + list(sensitivities), key="law_dst_de_sens_sensitivity_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_subject_type != "All":
                filtered_df = filtered_df[filtered_df["Data Subject Type"] == selected_subject_type]
            if selected_element != "All":
                filtered_df = filtered_df[filtered_df["Data Element"] == selected_element]
            if selected_sensitivity != "All":
                filtered_df = filtered_df[filtered_df["Sensitivity"] == selected_sensitivity]
            
            # Sort by Law, Data Subject Type, Data Element
            filtered_df = filtered_df.sort_values(by=["Law", "Data Subject Type", "Data Element"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class DataSubjectAccessRequestPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    @staticmethod
    def explain():
        import streamlit as st
        st.markdown(
            """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Data Subject Rights Inference Works</h4>
                <p>The Data Subject Rights Inference API uses the Data Subject Access Request mapping table to determine rights and response requirements:</p>
                <ul>
                    <li>Identifies applicable laws based on data subject location</li>
                    <li>Determines available rights (access, deletion, portability, etc.)</li>
                    <li>Calculates response timeframes</li>
                    <li>Identifies valid exemptions and conditions</li>
                    <li>Provides guidance on verification requirements</li>
                </ul>
                <p>The system helps organizations respond appropriately to data subject requests while maintaining compliance with various privacy regulations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Data Subject Access Request Requirements:</b><br>
            This section provides information about data subject rights and access request requirements across different data protection regulations. It outlines the rights individuals have regarding their personal data and how organizations must respond to these requests.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get DSAR data from repository
        dsar_guidances = self.regulatory_metadata_repository.get_data_subject_right_implementation_steps()
        if dsar_guidances:
            dsar_data = {   
                "Law": [],
                "Right": [],
                "Description": []
            }
            for dsar in dsar_guidances:
                dsar_data["Law"].append(dsar["law_name"])
                dsar_data["Right"].append(dsar["right_type"])
                dsar_data["Description"].append(dsar["description"])
    
            # Create a DataFrame
            df = pd.DataFrame(dsar_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="dsar_law_filter")
            
            with col2:
                rights = sorted(df["Right"].unique())
                selected_right = st.selectbox("Filter by Right", ["All"] + list(rights), key="dsar_right_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_right != "All":
                filtered_df = filtered_df[filtered_df["Right"] == selected_right]
            
            # Sort by Law and Right
            filtered_df = filtered_df.sort_values(by=["Law", "Right"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class LawTransferPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    @staticmethod
    def explain():
        import streamlit as st
        st.markdown(
            """
            <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                <h4 style="margin-top: 0;">How Transfer Mechanism Inference Works</h4>
                <p>The Transfer Mechanism Inference API uses the Law Transfer mapping table to determine appropriate safeguards for cross-border data transfers:</p>
                <ul>
                    <li>Identifies source and destination jurisdictions</li>
                    <li>Determines applicable data protection laws</li>
                    <li>Evaluates adequacy decisions and existing agreements</li>
                    <li>Recommends appropriate transfer mechanisms (e.g., SCCs, BCRs)</li>
                    <li>Highlights additional requirements for specific transfers</li>
                </ul>
                <p>The system helps organizations implement compliant data transfer frameworks while navigating complex international data protection requirements.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Transfer Requirements:</b><br>
            This section provides information about cross-border data transfer requirements across different data protection regulations. It outlines the conditions under which personal data can be transferred to countries outside the jurisdiction of the originating law.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get law transfer data from repository
        law_transfers = self.regulatory_metadata_repository.get_law_transfers()
        if law_transfers:
            law_transfer_data = {
                "Law": [],
                "Adequacy Countries": [],
                "Transfer Mechanisms": [],
                "Additional Requirements": []
            }
            for lt in law_transfers:
                law_transfer_data["Law"].append(lt["law_name"])
                law_transfer_data["Adequacy Countries"].append(lt["adequacy_countries"] or "N/A")
                law_transfer_data["Transfer Mechanisms"].append(lt["transfer_mechanisms"] or "N/A")
                law_transfer_data["Additional Requirements"].append(lt["additional_requirements"] or "N/A")
    
            # Create a DataFrame
            df = pd.DataFrame(law_transfer_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_transfer_law_filter")
            
            with col2:
                mechanisms = sorted([m for m in df["Transfer Mechanisms"].unique() if m != "N/A"])
                selected_mechanism = st.selectbox("Filter by Transfer Mechanism", ["All"] + list(mechanisms), key="law_transfer_mechanism_filter")
            
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_mechanism != "All":
                filtered_df = filtered_df[filtered_df["Transfer Mechanisms"].str.contains(selected_mechanism, na=False)]
            
            # Sort by Law
            filtered_df = filtered_df.sort_values(by=["Law"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class LawIncidentBreachNotificationPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law Incident Breach Notification:</b><br>
            This section provides information about breach notification requirements across different data protection regulations. It outlines when and how organizations must notify authorities and affected individuals about data breaches, including timeframes and content requirements.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get law incident breach guidance data from repository
        law_breach_guidances = self.regulatory_metadata_repository.get_law_incident_breach_guidances()
        if law_breach_guidances:
            law_breach_data = {
                "Law": [],
                "Threshold": [],
                "Timeframe": [],
                "Authority": [],
                "Content": []
            }
            for lbg in law_breach_guidances:
                law_breach_data["Law"].append(lbg["law_name"])
                law_breach_data["Threshold"].append(lbg["threshold"])
                law_breach_data["Timeframe"].append(lbg["timeframe"])
                law_breach_data["Authority"].append(lbg["authority"])
                law_breach_data["Content"].append(lbg["content"])
    
            # Create a DataFrame
            df = pd.DataFrame(law_breach_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_breach_law_filter")
            
            with col2:
                timeframes = sorted(df["Timeframe"].unique())
                selected_timeframe = st.selectbox("Filter by Timeframe", ["All"] + list(timeframes), key="law_breach_timeframe_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_timeframe != "All":
                filtered_df = filtered_df[filtered_df["Timeframe"] == selected_timeframe]
    
            # Sort by Law
            filtered_df = filtered_df.sort_values(by=["Law"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")


class LawJurisdictionPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown('''
        <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
            <b>About Law to Jurisdiction Mapping:</b><br>
            This section maps data protection laws to their applicable jurisdictions, helping organizations understand which laws apply in which geographic areas. These mappings are essential for determining the territorial scope of various data protection regulations.
        </div>
        ''', unsafe_allow_html=True)
        
        # Get law jurisdiction data from repository
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        if law_jurisdictions:
            law_jurisdiction_data = {
                "Law": [],
                "Jurisdiction": []
            }
            for lj in law_jurisdictions:
                law_jurisdiction_data["Law"].append(lj["law_name"])
                law_jurisdiction_data["Jurisdiction"].append(lj["jurisdiction_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(law_jurisdiction_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_jurisdiction_law_filter")
            
            with col2:
                jurisdictions = sorted(df["Jurisdiction"].unique())
                selected_jurisdiction = st.selectbox("Filter by Jurisdiction", ["All"] + list(jurisdictions), key="law_jurisdiction_jurisdiction_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_jurisdiction != "All":
                filtered_df = filtered_df[filtered_df["Jurisdiction"] == selected_jurisdiction]
            
            # Sort by Law and Jurisdiction
            filtered_df = filtered_df.sort_values(by=["Law", "Jurisdiction"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")
