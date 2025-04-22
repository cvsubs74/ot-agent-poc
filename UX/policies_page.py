import streamlit as st
import pandas as pd

class PoliciesPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Display the Policies page with tabs for Policy Purpose, Policy Purpose Data Usage, and Policy Purpose Data Element."""
        # --- BEGIN FULL LOGIC MOVED FROM datamap.py ---
        st.markdown("<div class='page-header'><i class='fas fa-clipboard-list'></i> &nbsp;Policies</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of data policies that govern how data is managed, protected, and used within the organization.</p>
            <ul>
                <li>Policies define rules for data access and usage</li>
                <li>Policy-purpose relationships establish what purposes are allowed for each policy</li>
                <li>Data element rules specify what data can be accessed for each purpose</li>
                <li>Usage rules define permitted operations (read, write, share) for each data element</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        tabs = st.tabs([
            "Policies",
            "Policy Purpose",
            "Policy Purpose Data Element",
            "Policy Purpose Data Usage",
            "Policy Purpose Data Retention",
            "Policy Purpose Data Security",
            "Policy Data Element Usage",
            "Policy Data Element Retention",
            "Policy Data Element Security",
        ])
        
        # Policies tab
        with tabs[0]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policies:</b><br>
                Policies are formal rules that govern how data is managed, protected, and used within the organization. They set the foundation for compliance, security, and responsible data stewardship by defining what is allowed or required for data handling.
            </div>
            ''', unsafe_allow_html=True)
            # Get policies data from repository
            policies = self.glossary_repository.get_policies()
            if policies:
                policy_data = {
                    "Policy": [],
                    "Type": [],
                    "Status": [],
                    "Description": []
                }
                for policy in policies:
                    policy_data["Policy"].append(policy["name"])
                    policy_data["Type"].append(policy["policy_type"] if policy.get("policy_type") else "")
                    policy_data["Status"].append(policy["status"] if policy.get("status") else "")
                    policy_data["Description"].append(policy["description"] if policy.get("description") else "")
                
                # Convert to DataFrame
                df = pd.DataFrame(policy_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policy types
                    policy_types = sorted(list(set([t for t in df["Type"].tolist() if t])))
                    selected_type = st.selectbox("Filter by Policy Type", ["All"] + policy_types)
                
                with col2:
                    # Get unique statuses
                    statuses = sorted(list(set([s for s in df["Status"].tolist() if s])))
                    selected_status = st.selectbox("Filter by Status", ["All"] + statuses)
                
                # Apply filters
                filtered_df = df.copy()
                if selected_type != "All":
                    filtered_df = filtered_df[filtered_df["Type"] == selected_type]
                
                if selected_status != "All":
                    filtered_df = filtered_df[filtered_df["Status"] == selected_status]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policies match the selected filters.")
            else:
                st.warning("No data available in the database.")
        
        # Policy Purpose tab
        with tabs[1]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Purposes:</b><br>
                Policy Purposes define the legitimate reasons or objectives for which data may be processed under a given policy. They ensure that data use is aligned with business needs and regulatory expectations, supporting purpose limitation and transparency.
            </div>
            ''', unsafe_allow_html=True)
            # Get policy purposes from repository
            policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
            
            if policy_purposes:
                # Create a DataFrame for display
                policy_purpose_data = {
                    "Policy": [],
                    "Purpose": []
                }
                
                for relation in policy_purposes:
                    policy_purpose_data["Policy"].append(relation["policy_name"])
                    policy_purpose_data["Purpose"].append(relation["purpose_name"])
                
                # Convert to DataFrame
                df = pd.DataFrame(policy_purpose_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="policy_purpose_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="policy_purpose_purpose")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose relationships match the selected filters.")
            else:
                st.warning("No policy-purpose relationships available in the database.")
        
        # Policy Purpose Data Element tab
        with tabs[2]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Purpose Data Elements:</b><br>
                This construct maps which specific data elements are governed by each policy-purpose combination. It enables organizations to control and audit what pieces of data are accessible for each business purpose, supporting data minimization and access governance.
            </div>
            ''', unsafe_allow_html=True)
            # Get policy purpose data elements from repository
            policy_purpose_data_elements = self.regulatory_metadata_repository.get_policy_purpose_data_elements()
            
            if policy_purpose_data_elements:
                # Create a DataFrame for display
                ppde_data = {
                    "ID": [],
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Access Allowed": []
                }
                
                for relation in policy_purpose_data_elements:
                    ppde_data["ID"].append(relation["id"])
                    ppde_data["Policy"].append(relation["policy_name"])
                    ppde_data["Purpose"].append(relation["purpose_name"])
                    ppde_data["Data Element"].append(relation["data_element_name"])
                    ppde_data["Access Allowed"].append("Yes" if relation["access_allowed"] else "No")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppde_data)
                
                # Add filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppde_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppde_purpose")
                
                with col3:
                    # Filter by access allowed
                    selected_access = st.selectbox("Filter by Access", ["All", "Yes", "No"], key="ppde_access")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppde_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_access != "All":
                    filtered_df = filtered_df[filtered_df["Access Allowed"] == selected_access]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data element relationships match the selected filters.")
            else:
                st.warning("No policy-purpose-data element relationships available in the database.")
        
        # Policy Purpose Data Usage tab
        with tabs[3]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Purpose Data Usage:</b><br>
                This construct specifies which operations (such as read, write, share) are permitted on each data element for a given policy and purpose. It enforces usage controls and ensures that data is only used in ways that are authorized and appropriate.
            </div>
            ''', unsafe_allow_html=True)
            # Get policy purpose data usages from repository
            policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages()
            
            if policy_purpose_data_usages:
                # Create a DataFrame for display
                ppdu_data = {
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Operation": [],
                    "Allowed": [],
                    "Restrictions": []
                }
                
                for rule in policy_purpose_data_usages:
                    ppdu_data["Policy"].append(rule["policy_name"])
                    ppdu_data["Purpose"].append(rule["purpose_name"])
                    ppdu_data["Data Element"].append(rule["data_element_name"])
                    ppdu_data["Operation"].append(rule["operation"])
                    ppdu_data["Allowed"].append("Yes" if rule["allowed"] else "No")
                    ppdu_data["Restrictions"].append(rule["restrictions"] if rule["restrictions"] else "None")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppdu_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppdu_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppdu_purpose")
                
                # Second row of filters
                col3, col4, col5 = st.columns(3)
                
                with col3:
                    # Get unique operations
                    operations = sorted(list(set(df["Operation"].tolist())))
                    selected_operation = st.selectbox("Filter by Operation", ["All"] + operations, key="ppdu_operation")
                
                with col4:
                    # Filter by allowed
                    selected_allowed = st.selectbox("Filter by Allowed", ["All", "Yes", "No"], key="ppdu_allowed")
                
                with col5:
                    # Filter by restrictions
                    has_restrictions = st.selectbox("Has Restrictions", ["All", "Yes", "No"], key="ppdu_restrictions")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppdu_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_operation != "All":
                    filtered_df = filtered_df[filtered_df["Operation"] == selected_operation]
                
                if selected_allowed != "All":
                    filtered_df = filtered_df[filtered_df["Allowed"] == selected_allowed]
                
                if has_restrictions != "All":
                    if has_restrictions == "Yes":
                        filtered_df = filtered_df[filtered_df["Restrictions"] != "None"]
                    else:
                        filtered_df = filtered_df[filtered_df["Restrictions"] == "None"]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data usage rules match the selected filters.")
            else:
                st.warning("No policy-purpose-data usage rules available in the database.")
        
        # Policy Purpose Data Retention tab
        with tabs[4]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Purpose Data Retention:</b><br>
                This construct defines the retention requirements for each data element under specific policy-purpose contexts. It ensures that data is only kept for as long as necessary, supporting compliance with data retention and deletion obligations.
            </div>
            ''', unsafe_allow_html=True)
            # Get policy purpose data retentions from repository
            policy_purpose_data_retentions = self.regulatory_metadata_repository.get_policy_purpose_data_retentions()
            
            if policy_purpose_data_retentions:
                # Create a DataFrame for display
                ppdr_data = {
                    "Policy": [],
                    "Purpose": [],
                    "Data Element": [],
                    "Retention Period": [],
                    "Retention Trigger": [],
                    "Retention Basis": [],
                    "Exceptions": []
                }
                
                for rule in policy_purpose_data_retentions:
                    ppdr_data["Policy"].append(rule["policy_name"])
                    ppdr_data["Purpose"].append(rule["purpose_name"])
                    ppdr_data["Data Element"].append(rule["data_element_name"])
                    ppdr_data["Retention Period"].append(rule["retention_period"])
                    ppdr_data["Retention Trigger"].append(rule["retention_trigger"])
                    ppdr_data["Retention Basis"].append(rule["retention_basis"] if rule["retention_basis"] else "Not specified")
                    ppdr_data["Exceptions"].append(rule["exceptions"] if rule["exceptions"] else "None")
                
                # Convert to DataFrame
                df = pd.DataFrame(ppdr_data)
                
                # Add filters
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get unique policies
                    policies = sorted(list(set(df["Policy"].tolist())))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppdr_policy")
                
                with col2:
                    # Get unique purposes
                    purposes = sorted(list(set(df["Purpose"].tolist())))
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppdr_purpose")
                
                # Second row of filters
                col3, col4 = st.columns(2)
                
                with col3:
                    # Get unique retention triggers
                    triggers = sorted(list(set(df["Retention Trigger"].tolist())))
                    selected_trigger = st.selectbox("Filter by Retention Trigger", ["All"] + triggers, key="ppdr_trigger")
                
                with col4:
                    # Get unique retention periods
                    periods = sorted(list(set(df["Retention Period"].tolist())))
                    selected_period = st.selectbox("Filter by Retention Period", ["All"] + periods, key="ppdr_period")
                
                # Add data element search
                data_element_search = st.text_input("Search Data Elements", "", key="ppdr_search")
                
                # Apply filters
                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["Policy"] == selected_policy]
                
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["Purpose"] == selected_purpose]
                
                if selected_trigger != "All":
                    filtered_df = filtered_df[filtered_df["Retention Trigger"] == selected_trigger]
                
                if selected_period != "All":
                    filtered_df = filtered_df[filtered_df["Retention Period"] == selected_period]
                
                if data_element_search:
                    filtered_df = filtered_df[filtered_df["Data Element"].str.contains(data_element_search, case=False)]
                
                # Display filtered data
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("No policy-purpose-data retention rules match the selected filters.")
            else:
                st.warning("No policy-purpose-data retention rules available in the database.")
    
        # Policy Purpose Data Security tab
        with tabs[5]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Purpose Data Security:</b><br>
                This construct captures the security requirements and controls (such as encryption or masking) that must be applied to data elements for each policy-purpose context. It helps enforce security best practices and regulatory mandates.
            </div>
            ''', unsafe_allow_html=True)
            security_rules = self.regulatory_metadata_repository.get_policy_purpose_data_security()
            if security_rules:
                df = pd.DataFrame(security_rules)
                # Add filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    policies = sorted(df["policy_name"].unique())
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="ppds_policy")
                with col2:
                    purposes = sorted(df["purpose_name"].unique())
                    selected_purpose = st.selectbox("Filter by Purpose", ["All"] + purposes, key="ppds_purpose")
                with col3:
                    elements = sorted(df["data_element_name"].unique())
                    selected_element = st.selectbox("Filter by Data Element", ["All"] + elements, key="ppds_element")

                filtered_df = df.copy()
                if selected_policy != "All":
                    filtered_df = filtered_df[filtered_df["policy_name"] == selected_policy]
                if selected_purpose != "All":
                    filtered_df = filtered_df[filtered_df["purpose_name"] == selected_purpose]
                if selected_element != "All":
                    filtered_df = filtered_df[filtered_df["data_element_name"] == selected_element]

                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.warning("No policy purpose data security rules available.")

        # Policy Data Element Usage tab
        with tabs[6]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Data Element Usage:</b><br>
                This construct defines default usage rules for data elements across all purposes. It specifies what operations (collect, store, share, etc.) are allowed for each data element under a specific policy, regardless of purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            usage_rules = self.regulatory_metadata_repository.get_policy_data_element_usage()
            if usage_rules:
                # Add filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    policies = sorted(list(set([rule["policy_name"] for rule in usage_rules])))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="pde_usage_policy")
                with col2:
                    data_elements = sorted(list(set([rule["data_element_name"] for rule in usage_rules])))
                    selected_data_element = st.selectbox("Filter by Data Element", ["All"] + data_elements, key="pde_usage_element")
                with col3:
                    operations = sorted(list(set([rule["operation"] for rule in usage_rules])))
                    selected_operation = st.selectbox("Filter by Operation", ["All"] + operations, key="pde_usage_operation")
                
                # Apply filters
                filtered_rules = usage_rules
                if selected_policy != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["policy_name"] == selected_policy]
                if selected_data_element != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["data_element_name"] == selected_data_element]
                if selected_operation != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["operation"] == selected_operation]
                
                # Create DataFrame for display
                usage_data = {
                    "Policy": [],
                    "Data Element": [],
                    "Operation": [],
                    "Allowed": [],
                    "Restrictions": []
                }
                
                for rule in filtered_rules:
                    usage_data["Policy"].append(rule["policy_name"])
                    usage_data["Data Element"].append(rule["data_element_name"])
                    usage_data["Operation"].append(rule["operation"])
                    usage_data["Allowed"].append("Yes" if rule["allowed"] else "No")
                    usage_data["Restrictions"].append(rule["restrictions"] if rule["restrictions"] else "")
                
                # Display the data
                if usage_data["Policy"]:
                    st.dataframe(pd.DataFrame(usage_data), use_container_width=True)
                else:
                    st.warning("No policy data element usage rules match the selected filters.")
            else:
                st.warning("No policy data element usage rules available in the database.")
        
        # Policy Data Element Retention tab
        with tabs[7]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Data Element Retention:</b><br>
                This construct defines default retention periods for data elements across all purposes. It specifies how long each data element should be retained under a specific policy, regardless of purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            retention_rules = self.regulatory_metadata_repository.get_policy_data_element_retention()
            if retention_rules:
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    policies = sorted(list(set([rule["policy_name"] for rule in retention_rules])))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="pde_retention_policy")
                with col2:
                    data_elements = sorted(list(set([rule["data_element_name"] for rule in retention_rules])))
                    selected_data_element = st.selectbox("Filter by Data Element", ["All"] + data_elements, key="pde_retention_element")
                
                # Apply filters
                filtered_rules = retention_rules
                if selected_policy != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["policy_name"] == selected_policy]
                if selected_data_element != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["data_element_name"] == selected_data_element]
                
                # Create DataFrame for display
                retention_data = {
                    "Policy": [],
                    "Data Element": [],
                    "Retention Period": [],
                    "Retention Basis": [],
                    "Exceptions": []
                }
                
                for rule in filtered_rules:
                    retention_data["Policy"].append(rule["policy_name"])
                    retention_data["Data Element"].append(rule["data_element_name"])
                    retention_data["Retention Period"].append(rule["retention_period"])
                    retention_data["Retention Basis"].append(rule["retention_basis"] if rule["retention_basis"] else "")
                    retention_data["Exceptions"].append(rule["exceptions"] if rule["exceptions"] else "")
                
                # Display the data
                if retention_data["Policy"]:
                    st.dataframe(pd.DataFrame(retention_data), use_container_width=True)
                else:
                    st.warning("No policy data element retention rules match the selected filters.")
            else:
                st.warning("No policy data element retention rules available in the database.")
        
        # Policy Data Element Security tab
        with tabs[8]:
            st.markdown('''
            <div style="background-color: #eaf7ea; padding: 16px; border-radius: 10px; margin-bottom: 16px; border-left: 5px solid #27ae60;">
                <b>About Policy Data Element Security:</b><br>
                This construct defines default security requirements for data elements across all purposes. It specifies what security controls (encryption, masking, access control) should be applied to each data element under a specific policy, regardless of purpose.
            </div>
            ''', unsafe_allow_html=True)
            
            security_rules = self.regulatory_metadata_repository.get_policy_data_element_security()
            if security_rules:
                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    policies = sorted(list(set([rule["policy_name"] for rule in security_rules])))
                    selected_policy = st.selectbox("Filter by Policy", ["All"] + policies, key="pde_security_policy")
                with col2:
                    data_elements = sorted(list(set([rule["data_element_name"] for rule in security_rules])))
                    selected_data_element = st.selectbox("Filter by Data Element", ["All"] + data_elements, key="pde_security_element")
                
                # Apply filters
                filtered_rules = security_rules
                if selected_policy != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["policy_name"] == selected_policy]
                if selected_data_element != "All":
                    filtered_rules = [rule for rule in filtered_rules if rule["data_element_name"] == selected_data_element]
                
                # Create DataFrame for display
                security_data = {
                    "Policy": [],
                    "Data Element": [],
                    "Encryption": [],
                    "Masking": [],
                    "Access Control": []
                }
                
                for rule in filtered_rules:
                    security_data["Policy"].append(rule["policy_name"])
                    security_data["Data Element"].append(rule["data_element_name"])
                    
                    # Encryption info
                    encryption_info = "No"
                    if rule["requires_encryption"]:
                        encryption_info = f"Yes - {rule['encryption_algorithm']}" if rule["encryption_algorithm"] else "Yes"
                    security_data["Encryption"].append(encryption_info)
                    
                    # Masking info
                    masking_info = "No"
                    if rule["requires_masking"]:
                        masking_info = f"Yes - {rule['masking_format']}" if rule["masking_format"] else "Yes"
                    security_data["Masking"].append(masking_info)
                    
                    # Access control info
                    access_control_info = "No"
                    if rule["requires_access_control"]:
                        access_control_info = f"Yes - {rule['access_control_type']}" if rule["access_control_type"] else "Yes"
                    security_data["Access Control"].append(access_control_info)
                
                # Display the data
                if security_data["Policy"]:
                    st.dataframe(pd.DataFrame(security_data), use_container_width=True)
                else:
                    st.warning("No policy data element security rules match the selected filters.")
            else:
                st.warning("No policy data element security rules available in the database.")
        




def create_policy():
    # Add a section for defining new policies on purposes
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Define New Policy on Purpose")
    st.markdown("Create a new policy that defines rules for data access and usage based on specific purposes.")
    
    # Get existing policy-purpose relationships
    existing_policy_purposes = self.regulatory_metadata_repository.get_policy_purposes()
    existing_purpose_ids = set()
    if existing_policy_purposes:
        for pp in existing_policy_purposes:
            existing_purpose_ids.add(pp["purpose_id"])
    
    # Get all purposes for selection
    purposes = self.glossary_repository.get_purposes()
    
    # Filter out purposes that already have policies defined
    available_purposes = [p for p in purposes if p["id"] not in existing_purpose_ids] if purposes else []
    purpose_options = {p["id"]: p["name"] for p in available_purposes}
    
    # Get all data elements for selection
    data_elements = self.glossary_repository.get_data_elements()
    data_element_options = {de["id"]: de["name"] for de in data_elements} if data_elements else {}
    
    # Get data categories for selection
    data_categories = self.glossary_repository.get_data_categories()
    data_category_options = {dc["id"]: dc["name"] for dc in data_categories} if data_categories else {}
    
    # Selection mode (outside the form)
    st.markdown("Select how you want to define the policy:")
    selection_mode = st.radio(
        "Selection Mode", 
        ["By Data Category", "By Individual Data Elements"]
    )
    
    # Create a form for defining a new policy on a purpose
    with st.form(key="define_policy_form"):
        # Purpose selection (first step)
        if purpose_options:
            selected_purpose_id = st.selectbox(
                "Select Purpose", 
                options=list(purpose_options.keys()),
                format_func=lambda x: purpose_options[x]
            )
            if selected_purpose_id:
                purpose_name = purpose_options[selected_purpose_id]
        else:
            st.warning("No available purposes found in the database. All purposes already have policies defined.")
            selected_purpose_id = None
            
        # Get policies of the selected type from the RegulatoryMetadataRepository
        filtered_policies = self.glossary_repository.get_policies()
        
        # Create a dictionary of filtered policies for the selectbox
        filtered_policy_options = {p["id"]: p["name"] for p in filtered_policies}
        
        # Select an existing policy
        if filtered_policy_options:
            selected_policy_id = st.selectbox(
                "Select Policy", 
                options=list(filtered_policy_options.keys()),
                format_func=lambda x: filtered_policy_options[x]
            )
            
        # Data selection based on the selection mode
        selected_data_element_ids = []
        
        if selection_mode == "By Data Category":
            # Data category selection
            if data_category_options:
                selected_category_ids = st.multiselect(
                    "Select Data Categories",
                    options=list(data_category_options.keys()),
                    format_func=lambda x: data_category_options[x]
                )
                
                # Get all data elements in the selected categories
                if selected_category_ids:
                    # Map to show which category each element belongs to
                    element_category_map = {}
                    
                    # For each selected category, get its data elements
                    for category_id in selected_category_ids:
                        category_elements = self.regulatory_metadata_repository.get_data_category_data_elements(category_id=category_id)
                        if category_elements:
                            for element in category_elements:
                                element_id = element["data_element_id"]
                                if element_id not in selected_data_element_ids:  # Avoid duplicates
                                    selected_data_element_ids.append(element_id)
                                element_category_map[element_id] = data_category_options[category_id]
                    
                    # Show the count of data elements in each category
                    if element_category_map:
                        st.info(f"Selected {len(selected_data_element_ids)} data elements from {len(selected_category_ids)} categories")
                        
                        # Show a sample of the selected data elements
                        with st.expander("View Selected Data Elements"):
                            for category_id in selected_category_ids:
                                category_name = data_category_options[category_id]
                                category_elements = [de_id for de_id, cat in element_category_map.items() if cat == category_name]
                                if category_elements:
                                    st.markdown(f"**{category_name}:** {len(category_elements)} elements")
            else:
                st.warning("No data categories found in the database.")
        else:  # By Individual Data Elements
            # Show all data elements in a multiselect
            if data_elements:
                # Create a multiselect for all data elements
                selected_data_element_ids = st.multiselect(
                    "Select Data Elements",
                    options=list(data_element_options.keys()),
                    format_func=lambda x: data_element_options[x]
                )
                
                # Show count of selected elements
                if selected_data_element_ids:
                    st.info(f"Selected {len(selected_data_element_ids)} data elements")
            else:
                st.warning("No data elements found in the database.")
                selected_data_element_ids = []
        
        # Create a multiselect for operations
        operations = ["read", "write", "share"]
        selected_operations = st.multiselect(
                "Select allowed operations",
                options=operations,
                default=operations,  # Default to all operations selected
                format_func=lambda x: x.capitalize()
            )
            
        # Optional restrictions for selected operations
        operation_restrictions = {}
        if selected_operations:
            with st.expander("Add restrictions for operations (optional)"):
                for operation in selected_operations:
                    operation_restrictions[operation] = st.text_input(
                        f"Restrictions for {operation.capitalize()}",
                        placeholder=f"Enter any restrictions for {operation} operation",
                        key=f"rest_{operation}"
                    )
        
        # Create a dictionary to store permissions
        permissions = {}
            
        # Set the same permissions for all selected data elements
        for data_element_id in selected_data_element_ids:
            permissions[data_element_id] = {}
            
            # Set permissions based on selected operations
            for operation in operations:
                permissions[data_element_id][operation] = operation in selected_operations
                if operation in selected_operations and operation_restrictions.get(operation):
                    permissions[data_element_id][f"{operation}_restrictions"] = operation_restrictions[operation]
                else:
                    permissions[data_element_id][f"{operation}_restrictions"] = None
        
        # Show a summary of the selected operations
        if selected_operations:
            st.info(f"Selected operations: {', '.join(op.capitalize() for op in selected_operations)}")
        else:
            st.warning("No operations selected. All operations will be denied.")
    
        # Submit button
        submit_button = st.form_submit_button("Create Policy Definition")
    
    if submit_button:
        # Validate inputs
        if not selected_purpose_id:
            st.error("Please select a purpose.")
            return
        
        if not selected_data_element_ids:
            st.error("Please select at least one data element.")
            return
        
        if not selected_policy_id:
            st.error("Please select an existing policy.")
            return
        
        # Create policy-purpose relationship
        success = self.regulatory_metadata_repository.add_policy_purpose(
            policy_id=selected_policy_id,
            purpose_id=selected_purpose_id
        )
        
        if not success:
            st.error("Failed to create the policy-purpose relationship. Please try again.")
            return
        
        # Create policy-purpose-data element relationships and usage rules
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        total_operations = len(selected_data_element_ids) * (1 + (3 if selected_policy_id else 0))
        completed_operations = 0
        
        all_success = True
        for data_element_id in selected_data_element_ids:
            data_element_name = data_element_options[data_element_id]
            progress_text.text(f"Processing: {data_element_name}")
            
            # Add policy-purpose-data element relationship
            success = self.regulatory_metadata_repository.add_policy_purpose_data_element(
                policy_id=selected_policy_id,
                purpose_id=selected_purpose_id,
                data_element_id=data_element_id,
                access_allowed=True  # Default to allowed, operations will be controlled by usage rules
            )
            
            completed_operations += 1
            progress_bar.progress(completed_operations / total_operations)
                    
            if not success:
                all_success = False
                continue
            
            # Get the policy_purpose_data_element_id for the relationship we just created
            ppde_id = self.regulatory_metadata_repository.get_policy_purpose_data_element_id(
                policy_id=selected_policy_id,
                purpose_id=selected_purpose_id,
                data_element_id=data_element_id
            )
            
            if not ppde_id:
                all_success = False
                continue
            
            # Add operation permissions based on selected operations
            for operation in ["read", "write", "share"]:
                progress_text.text(f"Processing: {data_element_name} - {operation}")
                
                # Add policy-purpose-data-element-usage relationship
                # The operation is allowed only if it was selected in the multiselect
                is_allowed = operation in selected_operations
                restrictions = operation_restrictions.get(operation) if is_allowed else None
                
                success = self.regulatory_metadata_repository.add_policy_purpose_data_usage(
                    policy_purpose_data_element_id=ppde_id,
                    operation=operation,
                    allowed=is_allowed,
                    restrictions=restrictions
                )
                
                if not success:
                    all_success = False
                
                completed_operations += 1
                progress_bar.progress(completed_operations / total_operations)
        
        progress_text.empty()
        progress_bar.empty()
        
        if all_success:
            st.success("Successfully created policy for purpose: {}".format(purpose_name))
        else:
            st.error("Failed to create policy for purpose: {}".format(purpose_name))