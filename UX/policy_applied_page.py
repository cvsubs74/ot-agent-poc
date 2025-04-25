import streamlit as st
import pandas as pd

class PolicyAppliedPage:
    """
    Page to display policies applied at the table column level for a given asset and purpose.
    """
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, catalog_repository, policy_applied_repository):
        """
        Initialize the PolicyAppliedPage with required repositories.
        
        Args:
            glossary_repository: Repository for accessing glossary data
            regulatory_metadata_repository: Repository for accessing policy metadata
            catalog_repository: Repository for accessing catalog data
            policy_applied_repository: Repository for accessing applied policy data
        """
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.catalog_repository = catalog_repository
        self.policy_applied_repository = policy_applied_repository
    
    def render(self):
        """Display the Policy Applied page."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Applied Policies</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This page shows how policies are applied at the table column level for a given asset and purpose.</p>
            <ul>
                <li>Select an asset and purpose to see the applied policies</li>
                <li>The table shows how security policies (encryption and masking) are applied to each column</li>
                <li>Role-specific overrides are displayed when they exist</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Get assets for dropdown
        assets = self.glossary_repository.get_assets()
        asset_options = {}
        for asset in assets:
            asset_id, asset_name, _ = asset
            asset_options[asset_id] = asset_name
        
        # Get purposes for dropdown
        purposes = self.glossary_repository.get_purposes()
        purpose_options = {}
        for purpose in purposes:
            purpose_id = purpose["id"]
            purpose_name = purpose["name"]
            purpose_options[purpose_id] = purpose_name
        
        # Create filters
        col1, col2 = st.columns(2)
        with col1:
            selected_asset = st.selectbox(
                "Select Asset:",
                options=list(asset_options.keys()),
                format_func=lambda x: asset_options.get(x, ""),
                key="applied_asset_filter"
            )
        
        with col2:
            selected_purpose = st.selectbox(
                "Select Purpose:",
                options=list(purpose_options.keys()),
                format_func=lambda x: purpose_options.get(x, ""),
                key="applied_purpose_filter"
            )
        
        # Add a button to refresh the data
        if st.button("Show Applied Policies"):
            if selected_asset and selected_purpose:
                with st.spinner("Loading applied policies..."):
                    # Get applied policies
                    df = self.policy_applied_repository.get_applied_policies_for_asset_purpose(
                        asset_id=selected_asset,
                        purpose_id=selected_purpose
                    )
                    
                    if not df.empty:
                        # Format boolean columns as checkboxes
                        formatted_df = self.policy_applied_repository.format_boolean_as_checkbox(df)
                        
                        # Rename columns for better display
                        column_mapping = {
                            "schema_name": "Schema",
                            "table_name": "Table",
                            "column_name": "Column",
                            "data_type": "Data Type",
                            "data_element_name": "Data Element",
                            "purpose_name": "Purpose",
                            "role_name": "Role",
                            "policy_name": "Policy",
                            "encryption_required": "Encryption Required",
                            "encryption_algorithm": "Encryption Algorithm",
                            "masking_required": "Masking Required",
                            "masking_format": "Masking Format",
                            "is_override": "Is Override"
                        }
                        formatted_df.columns = [column_mapping.get(col, col) for col in formatted_df.columns]
                        
                        # Add a note about encryption settings for non-Default Role Assignment purposes
                        if purpose_options[selected_purpose] != "Default Role Assignment":
                            st.info("Note: Encryption settings are controlled by the Default Role Assignment purpose for all other purposes.")
                        
                        # Display the dataframe
                        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
                        
                        # Add an expander with additional information
                        with st.expander("About Applied Policies"):
                            st.markdown("""
                            ### Understanding Applied Policies
                            
                            - **Encryption Required**: Indicates whether the column data must be encrypted
                            - **Encryption Algorithm**: The algorithm used for encryption (only configurable for Default Role Assignment purpose)
                            - **Masking Required**: Indicates whether the column data must be masked
                            - **Masking Format**: The format used for masking (configurable for all purposes)
                            - **Is Override**: Indicates whether this policy is a role-specific override
                            
                            ### Default Role Assignment Purpose
                            
                            The Default Role Assignment purpose controls encryption settings for all purposes. 
                            Other purposes inherit these settings but can have their own masking settings.
                            """)
                    else:
                        st.info(f"No policies found for the selected asset and purpose. This could be because there are no data elements mapped to this asset, or no policies defined for the selected purpose.")
            else:
                st.warning("Please select both an asset and a purpose to view applied policies.")
