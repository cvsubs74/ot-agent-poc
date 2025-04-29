import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import json

# Add parent directory to path to import repositories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositories.ConsentRepository import ConsentRepository
from repositories.GlossaryRepository import GlossaryRepository
from repositories.PolicyRepository import PolicyRepository

class ConsentManagementPage:
    def __init__(self, consent_repo, glossary_repo, policy_repo):
        """Initialize the Consent Management page with database connections.
        
        Args:
            consent_repo: ConsentRepository instance.
            glossary_repo: GlossaryRepository instance.
            policy_repo: PolicyRepository instance.
        """
        self.consent_repo = consent_repo
        self.glossary_repo = glossary_repo
        self.policy_repo = policy_repo
        
    def render(self):
        """Render the main consent management page."""
        st.markdown("""
        <style>
            .page-header {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 5px solid #3498db;
            }
            .subsection-header {
                background-color: #eaf7ea;
                padding: 16px;
                border-radius: 10px;
                margin-bottom: 16px;
                border-left: 5px solid #27ae60;
            }
            .filter-container {
                background-color: #fff;
                padding: 16px;
                border-radius: 10px;
                margin-bottom: 16px;
                border: 1px solid #e0e0e0;
            }
            .status-granted {
                background-color: #e8f5e9;
                color: #2e7d32;
                padding: 4px 8px;
                border-radius: 4px;
            }
            .status-denied {
                background-color: #fce4ec;
                color: #c62828;
                padding: 4px 8px;
                border-radius: 4px;
            }
            .status-withdrawn {
                background-color: #fff3e0;
                color: #f57c00;
                padding: 4px 8px;
                border-radius: 4px;
            }
            .status-expired {
                background-color: #e8eaf6;
                color: #3949ab;
                padding: 4px 8px;
                border-radius: 4px;
            }
            .filter-label {
                font-weight: bold;
                margin-bottom: 4px;
            }
            .filter-select {
                width: 100%;
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='page-header'>
            <i class='fas fa-user-shield'></i> &nbsp;Consent Management
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <h3>Overview</h3>
            <p>This section provides tools to manage user consents linked to specific data processing purposes, enabling compliance with privacy regulations.</p>
            <ul>
                <li><strong>Consent Profiles:</strong> Manage user identity information for consent tracking</li>
                <li><strong>Consent Records:</strong> View and manage consents organized by profiles and purposes</li>
                <li><strong>Consent Status:</strong> Track whether consent is granted, denied, withdrawn, or expired</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two tabs
        profile_tab, consent_tab = st.tabs(["Consent Profiles", "Consents"])
        
        with profile_tab:
            self._render_consent_profiles()
        
        with consent_tab:
            self._render_consents()

    def _render_consent_profiles(self):
        # Add filters
        col1, col2 = st.columns(2)
        
        with col1:
            search_name = st.text_input("Search by Name", key="profile_name_search")
        
        with col2:
            search_email = st.text_input("Search by Email", key="profile_email_search")
        
        # Display existing profiles
        profiles = self.consent_repo.get_consent_profiles()
        if profiles:
            # Convert tuples to dictionaries for easier access
            profiles = [dict(zip(['id', 'email', 'name', 'user_id', 'created_at', 'updated_at'], profile)) for profile in profiles]
            
            # Convert datetime objects to strings for JSON serialization
            for p in profiles:
                if 'created_at' in p and p['created_at'] is not None:
                    p['created_at'] = p['created_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(p['created_at'], 'strftime') else str(p['created_at'])
                if 'updated_at' in p and p['updated_at'] is not None:
                    p['updated_at'] = p['updated_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(p['updated_at'], 'strftime') else str(p['updated_at'])
            
            # Apply filters
            if search_name:
                profiles = [p for p in profiles if search_name.lower() in p['name'].lower()]
            
            if search_email:
                profiles = [p for p in profiles if search_email.lower() in p['email'].lower()]
            
            # Convert to DataFrame for easier display
            df = pd.DataFrame(profiles)
            
            if not df.empty:
                # Define column configuration for better display
                column_config = {
                    "id": st.column_config.NumberColumn(
                        "ID",
                        width="small"
                    ),
                    "name": st.column_config.TextColumn(
                        "Name",
                        width="medium"
                    ),
                    "email": st.column_config.TextColumn(
                        "Email",
                        width="medium"
                    ),
                    "user_id": st.column_config.TextColumn(
                        "User ID",
                        width="medium"
                    ),
                    "created_at": st.column_config.DatetimeColumn(
                        "Created At",
                        format="MMM DD, YYYY, h:mm a",
                        width="medium"
                    ),
                    "updated_at": st.column_config.DatetimeColumn(
                        "Updated At",
                        format="MMM DD, YYYY, h:mm a",
                        width="medium"
                    )
                }
                
                # Show dataframe with proper styling
                st.dataframe(
                    df,
                    column_config=column_config,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No profiles found matching the search criteria")
        else:
            st.info("No consent profiles found")

    def _render_consents(self):
        # Add JavaScript to handle filter changes
        st.markdown("""
        <script>
            function updateFilters() {
                const profileSelect = document.getElementById('profile_filter');
                const purposeSelect = document.getElementById('purpose_filter');
                
                // Get selected values
                const profileValue = profileSelect.value;
                const purposeValue = purposeSelect.value;
                
                // Update URL parameters
                const urlParams = new URLSearchParams(window.location.search);
                if (profileValue) {
                    urlParams.set('profile', profileValue);
                } else {
                    urlParams.delete('profile');
                }
                if (purposeValue) {
                    urlParams.set('purpose', purposeValue);
                } else {
                    urlParams.delete('purpose');
                }
                
                // Update URL without reloading
                window.history.replaceState({}, '', `${window.location.pathname}?${urlParams.toString()}`);
                
                // Trigger Streamlit rerun
                window.dispatchEvent(new Event('resize'));
            }
            
            // Add change event listeners
            document.getElementById('profile_filter').addEventListener('change', updateFilters);
            document.getElementById('purpose_filter').addEventListener('change', updateFilters);
            
            // Initialize filters from URL parameters
            const urlParams = new URLSearchParams(window.location.search);
            const profileParam = urlParams.get('profile');
            const purposeParam = urlParams.get('purpose');
            
            if (profileParam) {
                document.getElementById('profile_filter').value = profileParam;
            }
            if (purposeParam) {
                document.getElementById('purpose_filter').value = purposeParam;
            }
        </script>
        """, unsafe_allow_html=True)
        
        # Get profiles and convert to dictionaries
        profiles = self.consent_repo.get_consent_profiles()
        profile_dict = [dict(zip(['id', 'email', 'name', 'user_id', 'created_at', 'updated_at'], profile)) for profile in profiles]
        
        # Convert datetime objects to strings for JSON serialization
        for p in profile_dict:
            if 'created_at' in p and p['created_at'] is not None:
                p['created_at'] = p['created_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(p['created_at'], 'strftime') else str(p['created_at'])
            if 'updated_at' in p and p['updated_at'] is not None:
                p['updated_at'] = p['updated_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(p['updated_at'], 'strftime') else str(p['updated_at'])
        
        # Get purposes using the glossary repository
        purposes = self.glossary_repo.get_purposes()
        purpose_dict = purposes
        
        # Add filters using Streamlit components instead of JavaScript
        col1, col2 = st.columns(2)
        
        with col1:
            profile_filter = st.selectbox(
                "Filter by Profile",
                ["All Profiles"] + [f"{p['name']} ({p['email']})" for p in profile_dict],
                key="profile_filter"
            )
        
        with col2:
            purpose_filter = st.selectbox(
                "Filter by Purpose",
                ["All Purposes"] + [f"{p['name']} - {p['risk_level']} Risk" for p in purpose_dict],
                key="purpose_filter"
            )
        
        # Apply filters
        consents = self.consent_repo.get_consents()
        if consents:
            # Convert tuples to dictionaries for easier access
            consents = [dict(zip(['id', 'profile_id', 'purpose_id', 'status', 'created_at', 'updated_at'], consent)) for consent in consents]
            
            # Apply filters
            if profile_filter != "All Profiles":
                profile_email = profile_filter.split('(')[1].split(')')[0]
                profile_id = next((p['id'] for p in profile_dict if p['email'] == profile_email), None)
                if profile_id:
                    consents = [c for c in consents if c['profile_id'] == profile_id]
            
            if purpose_filter != "All Purposes":
                # Extract the purpose name from the filter string (before the ' - ' separator)
                purpose_name = purpose_filter.split(' - ')[0]
                purpose_id = next((p['id'] for p in purpose_dict if p['name'] == purpose_name), None)
                if purpose_id:
                    consents = [c for c in consents if c['purpose_id'] == purpose_id]
            
            # Convert to DataFrame for display
            df = pd.DataFrame(consents)
            
            # Add profile and purpose names to the display
            if not df.empty:
                profile_map = {p['id']: f"{p['name']} ({p['email']})" for p in profile_dict}
                purpose_map = {p['id']: p['name'] for p in purpose_dict}
                
                df['profile'] = df['profile_id'].map(profile_map)
                df['purpose'] = df['purpose_id'].map(purpose_map)
                
                # Format datetime fields
                if 'created_at' in df.columns:
                    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                if 'updated_at' in df.columns:
                    df['updated_at'] = pd.to_datetime(df['updated_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Define column configuration for better display
                column_config = {
                    "profile": "Profile",
                    "purpose": "Purpose",
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Current consent status",
                        width="medium",
                        options=[
                            "granted", "denied", "withdrawn", "expired"
                        ],
                        required=True
                    ),
                    "created_at": st.column_config.DatetimeColumn(
                        "Created At",
                        format="MMM DD, YYYY, h:mm a",
                        width="medium"
                    ),
                    "updated_at": st.column_config.DatetimeColumn(
                        "Updated At",
                        format="MMM DD, YYYY, h:mm a",
                        width="medium"
                    )
                }
                
                # Show only relevant columns
                display_columns = ['profile', 'purpose', 'status', 'created_at', 'updated_at']
                
                # Display the dataframe with proper styling
                st.dataframe(
                    df[display_columns],
                    column_config=column_config,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No consents found matching the filters")
        else:
            st.info("No consents found")

# Main function to run the page when executed directly
def main():
    # Set up page configuration when run standalone
    st.set_page_config(
        page_title="Consent Management",
        page_icon="🔐",
        layout="wide"
    )
    page = ConsentManagementPage(ConsentRepository(), GlossaryRepository(), PolicyRepository())
    page.render()

if __name__ == "__main__":
    main()
