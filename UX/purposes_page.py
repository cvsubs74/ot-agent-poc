import streamlit as st
import pandas as pd

class PurposesPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        """Display the Purposes page with all purposes from the repository."""
        st.markdown("<div class='page-header'><i class='fas fa-bullseye'></i> &nbsp;Purposes</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of business purposes for data processing activities.</p>
            <ul>
                <li>Business purposes define why data is collected and processed</li>
                <li>Each purpose has an associated risk level</li>
                <li>Purposes are used in policy compliance analysis</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        # Get purposes from repository
        purposes = self.glossary_repository.get_purposes()
        
        if purposes:
            # Create a DataFrame for display
            purposes_data = {
                "Purpose": [],
                "Category": [],
                "Risk Level": [],
                "Description": []
            }
            
            for purpose in purposes:
                purposes_data["Purpose"].append(purpose["name"])
                purposes_data["Category"].append(purpose["category_name"] if purpose.get("category_name") else "N/A")
                purposes_data["Risk Level"].append(purpose["risk_level"] if purpose.get("risk_level") else "N/A")
                purposes_data["Description"].append(purpose["description"] if purpose.get("description") else "")
            
            # Convert to DataFrame
            df = pd.DataFrame(purposes_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            
            with col1:
                # Get unique categories
                categories = sorted(list(set(df["Category"].tolist())))
                selected_category = st.selectbox("Filter by Category", ["All"] + categories)
            
            with col2:
                # Get unique risk levels
                risk_levels = sorted(list(set(df["Risk Level"].tolist())))
                selected_risk_level = st.selectbox("Filter by Risk Level", ["All"] + risk_levels)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Category"] == selected_category]
            
            if selected_risk_level != "All":
                filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk_level]
            
            # Display filtered data
            if not filtered_df.empty:
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.warning("No purposes match the selected filters.")
        else:
            st.warning("No purposes available in the database.")
