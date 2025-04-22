import streamlit as st
import pandas as pd

class RolesPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Display the External Roles page with information about imported roles."""
        st.markdown("<div class='page-header'><i class='fas fa-users'></i> &nbsp;External Roles</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of roles imported from external systems such as Snowflake, Databricks, or other access management platforms.</p>
            <ul>
                <li>External roles are used for access governance and policy compliance</li>
                <li>Roles can have specific overrides for data usage, retention, and security policies</li>
                <li>Role-based policy enforcement ensures proper access controls across systems</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Get external roles
        roles = self.glossary_repository.get_external_roles()
        
        if roles:
            # Create a DataFrame for display
            role_data = {
                "Name": [],
                "Description": [],
                "Source System": [],
                "Source Role Name": []
            }
            
            for role in roles:
                role_data["Name"].append(role[1])
                role_data["Description"].append(role[2] if role[2] else "")
                role_data["Source System"].append(role[3] if role[3] else "")
                role_data["Source Role Name"].append(role[4] if role[4] else "")
            
            # Display roles
            st.markdown("<h5>External Roles</h5>", unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(role_data), use_container_width=True)
            
            # Display role policy overrides
            st.markdown("<h5>Role Policy Overrides</h5>", unsafe_allow_html=True)
            
            # Usage overrides
            st.markdown("<h6>Usage Policy Overrides</h6>", unsafe_allow_html=True)
            usage_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_usage()
            if usage_overrides:
                st.dataframe(pd.DataFrame(usage_overrides), use_container_width=True)
            else:
                st.info("No role-purpose data usage overrides defined.")
            
            # Retention overrides
            st.markdown("<h6>Retention Policy Overrides</h6>", unsafe_allow_html=True)
            retention_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_retention()
            if retention_overrides:
                st.dataframe(pd.DataFrame(retention_overrides), use_container_width=True)
            else:
                st.info("No role-purpose data retention overrides defined.")
            
            # Security overrides
            st.markdown("<h6>Security Policy Overrides</h6>", unsafe_allow_html=True)
            security_overrides = self.regulatory_metadata_repository.get_all_policy_override_role_purpose_data_security()
            if security_overrides:
                st.dataframe(pd.DataFrame(security_overrides), use_container_width=True)
            else:
                st.info("No role-purpose data security overrides defined.")
        else:
            st.info("No external roles have been imported yet.")
